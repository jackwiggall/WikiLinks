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


def main():
    SEARCH_QUERY = '''
    SELECT id,redirect FROM Page WHERE redirect IS NOT NULL AND id >= ? AND id < ?
    '''
    INSERT_QUERY = '''
    INSERT INTO Link (redirect,src,dest) SELECT true,?,id FROM Page WHERE title=?
    '''

    INCREMENT=1_000
    start = 0
    end = INCREMENT
    successes=0
    fails=0
    while True:
        print(f'\rsuccesses: {successes:_}, fails: {fails:_}', end="")
        cur.execute(SEARCH_QUERY, (start,end))
        rows = cur.fetchall()
        for row in rows:
            id = row[0] # src
            redirect = row[1] # dest
            try:
                cur.execute(INSERT_QUERY, (id, redirect))
                successes+=1
            except mariadb.IntegrityError:
                fails+=1

        con.commit()

        start+=INCREMENT
        end+=INCREMENT



    con.commit()
    print()
    print("done")


if __name__ == '__main__':
    main()