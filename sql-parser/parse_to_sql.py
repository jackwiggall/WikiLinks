#!/usr/bin/env python
import sys # args, exit
import os # path exists
import re # regex
import mariadb, mysql.connector
from lxml import etree # xml parser
import gzip

XML_HEADER = "{http://www.mediawiki.org/xml/export-0.10/}"

if (len(sys.argv) <= 1):
    print("usage:" , sys.argv[0], "<wikipedia xml file>")
    sys.exit(1)

WIKI_XML_FILE=sys.argv[1]

if not os.path.exists(WIKI_XML_FILE): # wikipedia xml file not exists
    print("wikipedia xml file not found,\ndownload from https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles-multistream.xml.bz2")
    sys.exit(1)


mariaCon = mariadb.connect(
    host='127.0.0.1',
    user='wiki',
    passwd='L1nKz',
    database='wikilinks'
)
mariaCur = mariaCon.cursor()
mysqlCon = mysql.connector.connect(
    host='127.0.0.1',
    user='wiki',
    passwd='L1nKz',
    db='wikilinks'
)
mysqlCur = mysqlCon.cursor()

BUFFER_FILE="/ramdisk/relationships.gz"
SEPERATOR="<!!>"

class GzipWriteBuffer:
    def __init__(self, maxbuffer, filename):
        # f=open(filename, "w")
        # f.close()
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
    relationshipsFile = GzipWriteBuffer(1024*8, BUFFER_FILE)
    try:
        # 10KB compression buffer
        i=0
        iterations=0
        inserts=0
        fails=0
        relationships=0
        f=open(WIKI_XML_FILE, 'rb')
        QUERY_REDIRECT = 'INSERT INTO Page (title, redirect) VALUES (%s,%s)'
        QUERY_CONTENT = 'INSERT INTO Page (title) VALUES (%s)'

        tree = etree.iterparse(f)
        # skip = 8_000_000
        skip = 0
        for event,element in tree:
            if element.tag.endswith("page"):
                i+=1
                iterations+=1

                if iterations < skip:
                    if (i >= 1_000):
                        i=0
                        print(f'\rskip {iterations:_}', end="")
                    element.clear()
                    continue

                if i >= 1_000:
                    i=0
                    print(f'\rinserts {inserts:_}, fails {fails:_}', end="")
                    mysqlCon.commit()

                title = element.find(XML_HEADER+"title").text # title element
                if ':' in title: # special links
                    element.clear()
                    continue

                redirectElement = element.find(XML_HEADER+"redirect") # redirect element
                if redirectElement != None: ## title redirect to redirectElement
                    redirectTitle = redirectElement.values()[0]
                    # print("redirect",title,"->",redirectTitle)
                    try:
                        mysqlCur.execute(QUERY_REDIRECT, (title, redirectTitle,))
                        inserts+=1
                    except mysql.connector.errors.IntegrityError: # duplicate entry
                        fails+=1
                else:
                    textElement = element.find(XML_HEADER+"revision").find(XML_HEADER+"text")
                    content = textElement.text
                    try:
                        mysqlCur.execute(QUERY_CONTENT, (title,))
                        inserts+=1
                    except mysql.connector.errors.IntegrityError: # duplicate entry
                        fails+=1
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
                                    relationshipsFile.writeLine(title+"<!!>"+link)
                                    relationships+=1
                                    

                # dont (cache / store in ram)
                element.clear()
    except etree.XMLSyntaxError: ## happens when at the end of the wiki file
        pass
    except Exception as e:
        raise e
    
    relationshipsFile.flushBuffer()

    # create relationships
    print()
    print(f'creating relationships {relationships:_}')
    with gzip.open(BUFFER_FILE, "rb") as f:
        query = '''
        INSERT INTO Link (src,dest)
            (SELECT (SELECT id FROM Page WHERE title=? OR title=? LIMIT 1),
            id FROM Page WHERE title=? OR title=? LIMIT 1);
        '''
        iterations=0
        successes=0
        fails=0
        for line in f:
            line=line.decode()[:-1] ## \n
            [src,dest] = line.split("<!!>")
            srcCap = src[0].upper()+src[1:]
            destCap = dest[0].upper()+dest[1:]
            iterations+=1
            if (iterations % 1_000 == 0):
                print(f'\rsuccesses {successes:_}, fails {fails:_}', end="")
                mariaCon.commit()
            try:
                mariaCur.execute(query, (src,srcCap, dest,destCap))
                successes+=1
            except mariadb.IntegrityError as e: # duplicate entry
                fails+=1

    mariaCon.commit()
    print()
    print("done")


if __name__ == '__main__':
    main()