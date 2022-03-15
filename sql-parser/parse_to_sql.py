#!/usr/bin/env python
import sys # args, exit
import os # path exists
import re # regex
import mysql.connector
from lxml import etree # xml parser


XML_HEADER = "{http://www.mediawiki.org/xml/export-0.10/}"

if (len(sys.argv) <= 1):
    print("usage:" , sys.argv[0], "<wikipedia xml file>")
    sys.exit(1)

WIKI_XML_FILE=sys.argv[1]

if not os.path.exists(WIKI_XML_FILE): # wikipedia xml file not exists
    print("wikipedia xml file not found,\ndownload from https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles-multistream.xml.bz2")
    sys.exit(1)


con = mysql.connector.connect(
    host='127.0.0.1',
    user='wiki',
    passwd='L1nKz',
    db='wikilinks'
)


BUFFER_FILE="/ramdisk/relationships.gz"
SEPERATOR="<!!>"

class GzipWriteBuffer:
    def __init__(self, maxbuffer, filename):
        f=open(filename, "w")
        f.close()
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

cur = con.cursor()

def main():
    relationshipsFile = GzipWriteBuffer(1024*8, BUFFER_FILE)
    try:
        # 10KB compression buffer
        i=0
        iterations=0
        f=open(WIKI_XML_FILE, 'rb')
        QUERY_REDIRECT = 'INSERT INTO Page (title, redirect) VALUES (%s,%s)'
        QUERY_CONTENT = 'INSERT INTO Page (title, content) VALUES (%s,%s)'

        tree = etree.iterparse(f)
        for event,element in tree:
            if element.tag.endswith("page"):
                i+=1
                iterations+=1

                if i >= 1_000:
                    i=0
                    print(f'\r{iterations:_}', end="")
                    con.commit()

                title = element.find(XML_HEADER+"title").text # title element
                if ':' in title: # special links
                    element.clear()
                    continue

                redirectElement = element.find(XML_HEADER+"redirect") # redirect element
                if redirectElement != None: ## title redirect to redirectElement
                    redirectTitle = redirectElement.values()[0]
                    # print("redirect",title,"->",redirectTitle)
                    try: 
                        cur.execute(QUERY_REDIRECT, (title, redirectTitle))
                    except mysql.connector.errors.IntegrityError: # duplicate entry
                        pass
                else:
                    textElement = element.find(XML_HEADER+"revision").find(XML_HEADER+"text")
                    content = textElement.text
                    try:
                        cur.execute(QUERY_CONTENT, (title, content))
                    except mysql.connector.errors.IntegrityError: # duplicate entry
                        pass
                    if content != None:
                        if ':' not in title: # if any special links sneekied their way through
                            # matches = re.findall('(?<=\[\[)[^\]]*(?=\]\])', text) ## find links
                            links = re.findall('\[\[[^\]]*\]\]', content) ## find links [[.*]]
                            for link in links:
                                link = link[2:-2] # remove [[ and ]]
                                if ':' not in link: # special links, 'File:', 'Category:'
                                    if '|' in link: # the [[thing (where)|thing]] only shows [[thing (where)]] as clickable on actual wikipedia
                                        link = link.split('|')[0]
                                    link = link.replace('\n','') # sometimes occurs
                                    # create record of links to create relationships with after all titles have been populated
                                    relationshipsFile.writeLine((title+"<!!>"+link)
                                    

                # dont cache / store in ram
                element.clear()
    except etree.XMLSyntaxError: ## happens when at the end of the wiki file
        pass
    except Exception as e:
        raise e
    
    relationshipsFile.flushBuffer()

    # create relationships
    print()
    print("creating relationships")
    with f as gzip.open(BUFFER_FILE, "rb"):
        query = '''
        INSERT INTO Link (src,dest)
            (SELECT (SELECT id FROM Page WHERE title=%s),
            id FROM Page WHERE title=%s);
        '''
        iterations=0
        for line in f:
            src,dest = line.split("<!!>")
            iterations+=1
            if (iterations % 1_000 == 0):
                print(f'\r{iterations:_}', end="")
                con.commit()
            cur.query(query, (src,dest))

    con.commit()
    print()
    print("done")


if __name__ == '__main__':
    main()