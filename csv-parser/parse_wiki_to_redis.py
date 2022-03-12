#!/usr/bin/env python
import sys # args, exit
import os # path exists
import re # regix
import gzip # gzip file
from lxml import etree # xml parser

HEADER = "{http://www.mediawiki.org/xml/export-0.10/}"

if (len(sys.argv) <= 3):
    print("usage:" , sys.argv[0], "<wikipedia xml file>", "<titles.csv.gz>", "<relationships.csv.gz>")
    sys.exit(1)

WIKI_XML_FILE=sys.argv[1]
TITLES_FILE=sys.argv[2]
RELATIONSHIPS_FILE=sys.argv[3]

if not os.path.exists(WIKI_XML_FILE): # wikipedia xml file not exists
    print("wikipedia xml file not found,\ndownload from https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles-multistream.xml.bz2")
    sys.exit(1)

# try to open output file
try:
    f=open(TITLES_FILE, "w")
    f.close()
    f=open(RELATIONSHIPS_FILE, "w")
    f.close()
except FileNotFoundError:
    print("cannot open output csv files", OUTPUT_FILE)
    sys.exit(1)


class GzipWriteBuffer:
    def __init__(self, maxbuffer, filename):
        self.lines = 0
        self.buffer = ""
        self.maxbuffer = maxbuffer
        self.filename = filename

    def writeLine(self, line):
        self.lines+=1

        self.buffer += line ## add line to buffer
        self.buffer += '\n' ## newline
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
    titlesFile = GzipWriteBuffer(1024*128, TITLES_FILE) ## 128KB
    relationshipsFile = GzipWriteBuffer(1024*16, RELATIONSHIPS_FILE) ## 16KB

    titlesFile.writeLine("title")
    relationshipsFile.writeLine("src, dest")
    try:
        i=0
        wikiXmlFile=open(WIKI_XML_FILE, 'rb')
        tree = etree.iterparse(wikiXmlFile)
        for event,element in tree:
            if element.tag.endswith("page"):
                ## progress
                i+=1
                if i >= 1_000:
                    i=0
                    print(f'\rtitles: {titlesFile.lines:_}, relationships: {relationshipsFile.lines:_}', end="")

                title = element.find(HEADER+"title").text

                line = makeCsvLine(title)
                titlesFile.writeLine(line)

                redirectElement = element.find(HEADER+"redirect")
                if redirectElement != None: ## title redirect to redirectElement
                    redirectTitle = redirectElement.values()[0]
                    line = makeCsvLine(title, redirectTitle)
                    relationshipsFile.writeLine(line)
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
                                    link = link.replace('\n','') ## happens with 2 titles
                                    line = makeCsvLine(title, link)
                                    relationshipsFile.writeLine(line)


                # dont cache / store in ram
                element.clear()
    except etree.XMLSyntaxError: ## happens when at the end of the wiki file
        pass
    except Exception as e:
        raise e
    finally: ## make sure files are closed and saved in event of error
        wikiXmlFile.close()
        titlesFile.flushBuffer()
        relationshipsFile.flushBuffer()

    print("\r",end="")
    print(f'Created titles file: {titlesFile.filename}, lines: {titlesFile.lines:_}')
    print(f'Created relationships file: {relationshipsFile.filename}, lines: {relationshipsFile.lines:_}')



def escapeRedisParams(arg):
    escaped = arg.replace("\\","\\\\") # "\" "\\"
    escaped = escaped.replace('"', '\\"') # """ "\""
    # i dont know how where or why but somehow newlines are in the arg string
    # "Beavis and Butt-Head" "VH1 Classic (American TV channel)\n"
    escaped = escaped.replace('\n','')
    escaped = '"' + escaped + '"'
    return escaped

def makeCsvLine(*fields):
    escapedFields = []
    for field in fields:
        escaped = field
        escaped = escaped.replace('"', '""') # escape "
        escaped = escaped.replace('\\','\\\\') # escape \
        escaped = escaped.replace("\n", "") # remove all newlines
        escaped = '"'+escaped+'"' # wrap in quotes to escape commas
        escapedFields.append(escaped)

    line = ", ".join(escapedFields)
    return line


if __name__ == '__main__':
    main()