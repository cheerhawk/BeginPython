#!/usr/bin/python3

print('Content-type: text/html\n')

import cgitb; cgitb.enable()

import mysql.connector

dbconfig = {'user':'foo',
            'password':'bar',
            'database':'baz',}
conn = mysql.connector.connect(**dbconfig)
curs = conn.cursor()

import cgi, sys
form = cgi.FieldStorage()

sender = form.getvalue('sender')
subject = form.getvalue('subject')
text = form.getvalue('text')
reply_to = form.getvalue('reply_to')

if not (sender and subject and text):
    print('Please supply sender, subject, and text')
    sys.exit()

if reply_to is not None:
    query = ("""
    INSERT INTO messages(reply_to, sender, subject, text)
    VALUES(%s, %s, %s, %s)""", (int(reply_to), sender, subject, text))
else:
    query = ("""
    INSERT INTO messages(sender, subject, text)
    VALUES(%s, %s, %s)""", (sender, subject, text))

curs.execute(*query)
conn.commit()

print("""
<html>
    <head>
        <title>Messages Saved</title>
    </head>
    <body>
        <h1>Messages Saved</h1>
        <hr />
        <a href='main.cgi'>Back to the main page</a>
    </body>
    </html>
""")