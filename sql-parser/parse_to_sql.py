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

cur = con.cursor()

skip=1_700_000

def main():
    relationships = []
    try:
        # 10KB compression buffer
        i=0
        iterations=0
        f=open(WIKI_XML_FILE, 'rb')
        tree = etree.iterparse(f)
        for event,element in tree:
            if element.tag.endswith("page"):
                i+=1
                iterations+=1

                if (iterations < skip):
                    element.clear()
                    continue

                if i >= 1_000:
                    i=0
                    print(f'\r{iterations:_}', end="")
                    con.commit()

                title = element.find(XML_HEADER+"title").text # title element
                if ':' in title: # special links
                    continue

                redirectElement = element.find(XML_HEADER+"redirect") # redirect element
                if redirectElement != None: ## title redirect to redirectElement
                    redirectTitle = redirectElement.values()[0]
                    # print("redirect",title,"->",redirectTitle)
                    query = 'INSERT INTO Page (title, redirect) VALUES (%s,%s)'
                    try:
                        cur.execute(query, (title, redirectTitle))
                    except mysql.connector.errors.IntegrityError: # duplicate entry
                        pass
                else:
                    textElement = element.find(XML_HEADER+"revision").find(XML_HEADER+"text")
                    content = textElement.text
                    # print("title",title)
                    query = 'INSERT INTO Page (title, content) VALUES (%s,%s)'
                    try:
                        cur.execute(query, (title, content))
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
                                    relationships.append([title, link])
                                    

                # dont cache / store in ram
                element.clear()
    except etree.XMLSyntaxError: ## happens when at the end of the wiki file
        pass
    except Exception as e:
        raise e
    # create relationships
    for src,dest in relationships:
        print(src,dest)

    print()
    print(done)



def createRedisCommand(src,dest):
    command = "SADD "
    command += escapeRedisParam(src)
    command += " "
    command += escapeRedisParam(dest)
    return command

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
    return base64.b64encode(hashlib.md5(title.encode('utf-8')).digest())[:8].decode('utf8')

if __name__ == '__main__':
    main()