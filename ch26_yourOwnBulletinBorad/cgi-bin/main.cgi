#!/usr/bin/python3

print('Content-type: text/html\n')

import cgitb; cgitb.enable()

import mysql.connector

dbconfig = {'user':'foo',
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
            <h1>The Foobar Bulletin Board</h1>
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

def formatRow(row):
    print('<p><a href="view.cgi?id={id}">{subject}</a></p>'.format(**row))
    try: kids = children[row['id']]
    except KeyError: pass
    else:
        print('<blockquote>')
        for kid in kids:
            formatRow(kid)
        print('</blockquote>')
    print('<p>')

for row in toplevel:
    formatRow(row)

print("""
        </p>
        <hr />
        <p><a href="edit.cgi">Post message</a></p>
    </body>
</html>
""")