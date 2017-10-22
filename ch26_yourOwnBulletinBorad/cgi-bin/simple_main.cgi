#!/usr/bin/python3

print('Content-type: text/html\n')

import cgitb; cgitb.enable()

import mysql.connector

dbconfig = {'host':'127.0.0.1',
            'user':'foo',
            'password':'bar',
            'database':'baz',}
conn = mysql.connector.connect(**dbconfig)
curs = conn.cursor(dictionary=True)

print("""
<html>
    <head>
        <title>The FooBar Bulletin Board</title>
    </head>
    <body>
        <h1>The FooBar Bulletin Board</h1>
""")

curs.execute('SELECT * FROM messages')
rows = curs.fetchall()

toplevel = []
children = {}

for row in rows:
    parent_id = row['reply_to']
    if parent_id is None:
        toplevel.append(row)
    else:
        children.setdefault(parent_id, []).append(row)

    def format(row):
        print(row['subject'])
        try: kids = children[row['id']]
        except KeyError: pass
        else:
            print('<blockquote>')
            for kid in kids:
                format(kid)
            print('</blockquote>')

for row in toplevel:
    print('<p>')
    format(row)
    print('</p>')

print("""
</body>
</html>
""")