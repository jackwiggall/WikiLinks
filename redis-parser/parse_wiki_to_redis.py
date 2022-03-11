#!/usr/bin/env python
import sys # args, exit
import os # path exists
import re # regix
import gzip # gzip file
from lxml import etree # xml parser

HEADER = "{http://www.mediawiki.org/xml/export-0.10/}"

if (len(sys.argv) <= 2):
    print("usage:" , sys.argv[0], "<wikipedia xml file>", "<redis output file>")
    sys.exit(1)

WIKI_XML_FILE=sys.argv[1]
OUTPUT_FILE=sys.argv[2]

if not os.path.exists(WIKI_XML_FILE): # wikipedia xml file not exists
    print("wikipedia xml file not found,\ndownload from https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles-multistream.xml.bz2")
    sys.exit(1)

# try to open output file
try:
    f=open(OUTPUT_FILE, "w")
    f.close()
except FileNotFoundError:
    print("cannot open output file,", OUTPUT_FILE)
    sys.exit(1)

# create output file
f=open(OUTPUT_FILE, "w")
f.close()

class GzipWriteBuffer:
    def __init__(self, maxbuffer, filename):
        self.buffer = ""
        self.maxbuffer = maxbuffer
        self.filename = filename

    def writeLine(self, line):
        # print(line)
        self.buffer += line
        self.buffer += '\n'
        ## check if over buffer limit
        if len(self.buffer) > self.maxbuffer:
            self.flushBuffer()

    def flushBuffer(self):
        with gzip.open(self.filename, 'at') as f:
            f.write(self.buffer)
        ## clear buffer
        self.buffer = ""


def main():
    lines = 0
    try:
        # 10KB compression buffer
        file = GzipWriteBuffer(1024*10, OUTPUT_FILE)
        i=0
        f=open(WIKI_XML_FILE, 'rb')
        tree = etree.iterparse(f)
        for event,element in tree:
            if element.tag.endswith("page"):
                if i >= 100000:
                    i=0
                    print(f'\r{lines:_}', end="")

                title = element.find(HEADER+"title").text
                redirectElement = element.find(HEADER+"redirect")
                if redirectElement != None: ## title redirect to redirectElement
                    lines+=1
                    i+=1
                    redisCmd = createRedisCommand(title, redirectElement.values()[0])
                    file.writeLine(redisCmd)
                else:
                    textElement = element.find(HEADER+"revision").find(HEADER+"text")
                    text = textElement.text
                    if text != None:
                        if ':' not in title: # if any special links sneekied their way through
                            # matches = re.findall('(?<=\[\[)[^\]]*(?=\]\])', text) ## find links
                            links = re.findall('\[\[[^\]]*\]\]', text) ## find links [[.*]]
                            for link in links:
                                link = link[2:-2] # remove [[ and ]]
                                if ':' not in link: # special links, 'File:', 'Category:'
                                    if '|' in link: # the [[thing (where)|thing]] only shows [[thing (where)]] as clickable on actual wikipedia
                                        link = link.split('|')[0]
                                    lines+=1
                                    i+=1
                                    redisCmd = createRedisCommand(title,link)
                                    file.writeLine(redisCmd)

                # dont cache / store in ram
                element.clear()
    except etree.XMLSyntaxError: ## happens when at the end of the wiki file
        pass
    except Exception as e:
        raise e
    finally: ## make sure files are closed and saved in event of error
        f.close()
        file.flushBuffer()

    print("\rCreated redis file: "+OUTPUT_FILE+" lines: "+str(lines))
    print("to populate redis database with this file run")
    print("\tzcat '"+OUTPUT_FILE+"' | redis-cli --pipe")



def createRedisCommand(src,dest):
    command = "SADD "
    command += escapeRedisParams(src)
    command += " "
    command += escapeRedisParams(dest)
    return command

def escapeRedisParams(arg):
    escaped = arg.replace("\\","\\\\") # "\" "\\"
    escaped = escaped.replace('"', '\\"') # """ "\""
    # i dont know how where or why but somehow newlines are in the arg string
    # "Beavis and Butt-Head" "VH1 Classic (American TV channel)\n"
    escaped = escaped.replace('\n','')
    escaped = '"' + escaped + '"'
    return escaped


if __name__ == '__main__':
    main()