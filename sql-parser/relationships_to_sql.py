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

BUFFER_FILE="/data/wikipedia/relationships.gz"
SEPERATOR="<!!>"



# 27_500_000
# 20_500_000
# 2_000_000
# 7_000_000
# 3_500_000
# 39_500_000
# 4_000_000
skip=114_000_000
def main():

    # create relationships
    print(f'creating relationships')
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
            iterations+=1
            if iterations < skip:
                continue
            line=line.decode()[:-1] ## \n
            [src,dest] = line.split("<!!>")
            srcCap = src[0].upper()+src[1:]
            destCap = dest
            try:
                destCap = dest[0].upper()+dest[1:]
            except:
                pass
            if (iterations % 1_000 == 0):
                print(f'\r{iterations:_}: successes {successes:_}, fails {fails:_}', end="")
                con.commit()
            try:
                cur.execute(query, (src,srcCap, dest,destCap))
                successes+=1
            except mariadb.IntegrityError as e: # duplicate entry
                fails+=1

    con.commit()
    print()
    print("done")


if __name__ == '__main__':
    main()