#!/usr/bin/env python
import sys # args, exit
import os # path exists
import re # regex
import mariadb


con = mariadb.connect(
    host='127.0.0.1',
    user='wiki',
    passwd='L1nKz',
    database='wikilinks'
)
cur = con.cursor()


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
    query = '''
    SELECT id,title,redirect FROM Page WHERE id >= ? AND id < ?;
    '''

    INCREMENT=100
    start = 0
    end = INCREMENT
    while True:
        cur.execute(query, (start,end))
        rows = cur.fetchall()
        for row in rows:
            print(row)


        start+=INCREMENT
        end+=INCREMENT


    for row in rows:
        print(row)

    con.commit()
    print()
    print("done")


if __name__ == '__main__':
    main()