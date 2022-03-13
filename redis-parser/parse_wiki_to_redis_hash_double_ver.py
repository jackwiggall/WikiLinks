#!/usr/bin/env python
import sys # args, exit
import os # path exists
import re # regix
import gzip # gzip file
import hashlib, base64 # hashing
import time
from lxml import etree # xml parser


XML_HEADER = "{http://www.mediawiki.org/xml/export-0.10/}"

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
        self.lines = 0
        self.buffer = ""
        self.maxbuffer = maxbuffer
        self.filename = filename
    
    def getSize(self):
        byteSize = os.path.getsize(self.filename)
        mbSize = byteSize // 1024 // 1024
        return mbSize

    def writeLine(self, line):
        self.lines+=1
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

'''
HSET titles <hash> <title>

SADD f<title hash> <link hash> # f=forward
SADD b<link hash> <title hash> # b=backward
'''

def main():
    lines = 0
    file = GzipWriteBuffer(1024*16, OUTPUT_FILE)
    try:
        # 10KB compression buffer
        i=0
        f=open(WIKI_XML_FILE, 'rb')
        tree = etree.iterparse(f)
        lastTime = time.time()
        lastLines = 0
        for event,element in tree:
            if element.tag.endswith("page"):
                i+=1
                if i >= 10_000:
                    i=0
                    nowTime = time.time()
                    diffTime = nowTime - lastTime
                    lastTime = nowTime
                    diffLines = file.lines - lastLines
                    lastLines = file.lines

                    # 1234 lines in 100 seconds
                    linesPerSec = int(diffLines // diffTime)
                    print(f'\rlines: {file.lines:_} ({linesPerSec:_} per second), filesize: {file.getSize()}M', end="")

                title = element.find(XML_HEADER+"title").text

                # title hash
                titleHash = hashTitle(title)
                redisCmd = f'HSET titles "{titleHash}" {escapeRedisParam(title)}'
                file.writeLine(redisCmd)

                redirectElement = element.find(XML_HEADER+"redirect")
                if redirectElement != None: ## title redirect to redirectElement
                    redirectHash = hashTitle(redirectElement.values()[0])
                    writeTwoWayFields(file, titleHash, redirectHash)
                else:
                    textElement = element.find(XML_HEADER+"revision").find(XML_HEADER+"text")
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
                                    link = link.replace('\n','') # sometimes occurs
                                    linkHash = hashTitle(link)
                                    writeTwoWayFields(file, titleHash, linkHash)

                # dont cache / store in ram
                element.clear()
    except etree.XMLSyntaxError: ## happens when at the end of the wiki file
        pass
    except Exception as e:
        raise e
    finally: ## make sure files are closed and saved in event of error
        f.close()
        file.flushBuffer()

    print()
    print("Created redis file:", file.filename, "lines:", file.lines, "filesize:", file.getSize(),"M")
    print("to populate redis database with this file run")
    print("zcat '"+file.filename+"' | redis-cli --pipe")



def writeTwoWayFields(file, srcHash,destHash):
    forwards  = f'SADD f{srcHash} {destHash}'
    file.writeLine(forwards)
    backwards = f'SADD b{destHash} {srcHash}'
    file.writeLine(backwards)


def escapeRedisParam(arg):
    escaped = arg.replace("\\","\\\\") # "\" "\\"
    escaped = escaped.replace('"', '\\"') # """ "\""
    # i dont know how where or why but somehow newlines are in the arg string
    # "Beavis and Butt-Head" "VH1 Classic (American TV channel)\n"
    escaped = escaped.replace('\n','')
    escaped = '"' + escaped + '"'
    return escaped

# first 8 base64 characters of a md5 hash
def hashTitle(title):
    return base64.b64encode(hashlib.md5(title.encode('utf-8')).digest())[:6].decode('utf8')

if __name__ == '__main__':
    main()