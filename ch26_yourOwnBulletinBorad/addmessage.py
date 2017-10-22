#!/usr/bin/python3
# addmessage.py
import mysql.connector

dbconfig = {'host':'127.0.0.1',
            'user':'foo',
            'password':'bar',
            'database':'baz',}

conn = mysql.connector.connect(**dbconfig)
curs = conn.cursor()

reply_to = input('Reply to: ')
subject = input('Subject: ')
sender = input('Sender: ')
text = input('Text: ')

if reply_to:
    query = """
    INSERT INTO messages (reply_to, sender, subject, text)
    VALUES ({}, '{}', '{}', '{}')""".format(reply_to, sender, subject, text)
else:
    query = """
    INSERT INTO messages(sender, subject, text)
    VALUES('{}', '{}', '{}')""".format(sender, subject, text)
curs.execute(query)
conn.commit()