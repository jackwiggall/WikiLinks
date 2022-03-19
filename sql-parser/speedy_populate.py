#!/usr/bin/env python
import sys # args, exit
import os # path exists
import re # regex
import mysql.connector
import gzip


con = mysql.connector.connect(
    host='127.0.0.1',
    user='wiki',
    passwd='L1nKz',
    db='wikilinks'
)

cur = con.cursor()

BUFFER_FILE="/data/wikipedia/relationships.gz"
SEPERATOR="<!!>"

ID_LOOKUP = {}

print("selecting rows")
cur.execute('SELECT id,title FROM Page')
rows = cur.fetchall()

print("storing rows in hashtable")
for row in rows:
  id = row[0]
  title = row[1].decode()
  ID_LOOKUP[title] = id

print("hashtable length:",len(ID_LOOKUP))

print("started inserting")
QUERY_INSERT='INSERT IGNORE INTO Link (src,dest) VALUES (%s,%s)'
with gzip.open(BUFFER_FILE, 'rb') as f:
  idPairs = []
  lineNumber = 0
  lookupFail = 0
  inserts = 0
  for line in f:
    lineNumber+=1
    if (lineNumber % 100_000 == 0):
      cur.executemany(QUERY_INSERT, idPairs)
      con.commit()
      inserts+=cur.rowcount
      print(f'\r{lineNumber:_}: lookup fails {lookupFail:_}, inserts: {inserts:_}', end="")
      idPairs.clear()
    
    line=line.decode()[:-1] ## \n
    [src,dest] = line.split("<!!>")
    

    srcId = -1
    if src in ID_LOOKUP:
      srcId = ID_LOOKUP[src]
    else:
      capSrc = src.title() # capatilize first letter
      if capSrc in ID_LOOKUP:
        srcId = ID_LOOKUP[capSrc]
      else:
        lookupFail+=1
        continue

    destId = -1
    if dest in ID_LOOKUP:
      destId = ID_LOOKUP[dest]
    else:
      capDest = dest.title() # capatilize first letter
      if capDest in ID_LOOKUP:
        destId = ID_LOOKUP[capDest]
      else:
        lookupFail+=1
        continue

    idPairs.append((srcId, destId))

print()
print("done")