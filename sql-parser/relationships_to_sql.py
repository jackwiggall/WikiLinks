#!/usr/bin/env python
import sys # args, exit
import os # path exists
import re # regex
import mariadb
from lxml import etree # xml parser
import gzip


con = mariadb.connect(
    host='127.0.0.1',
    user='wiki',
    passwd='L1nKz',
    database='wikilinks'
)

cur = con.cursor()

BUFFER_FILE="/ramdisk/relationships.gz"
SEPERATOR="<!!>"



# 2_750_000
def main():

    # create relationships
    print()
    print("creating relationships")
    with gzip.open(BUFFER_FILE, "rb") as f:
        query = '''
        INSERT INTO Link (src,dest)
            (SELECT (SELECT id FROM Page WHERE title_upper=UPPER(?)),
            id FROM Page WHERE title_upper=UPPER(?));
        '''
        iterations=0
        for line in f:
            line=line.decode()[:-1]
            [src,dest] = line.split("<!!>")
            iterations+=1
            if (iterations % 1_000 == 0):
                print(f'\r{iterations:_}', end="")
                con.commit()
            try:
                cur.execute(query, (src,dest,))
                # print(src,dest)
                # print(query % (src,dest))
                # break
            except mariadb.IntegrityError as e: # duplicate entry
                pass

    con.commit()
    print()
    print("done")


if __name__ == '__main__':
    main()