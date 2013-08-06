# -*- coding: utf-8 -*-

##GPL Licence ??? 2/3 ?

#---------- Import
import tweepy
import sqlite3
import datetime
import conf

msg = """@USER HERE !
%s
%s
%s
%s
"""

#Use SQLite for history
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

#Use Tweepy api
auth = tweepy.OAuthHandler(conf.consumer_key, conf.consumer_secret)
auth.set_access_token(conf.access_token, conf.access_token_secret)
bot = tweepy.API(auth)

#Get the datetime today
currentDate = datetime.datetime.today()

#Fetch all active events
resEvents = cursor.execute("select rowid, date, lieu, lieu_url, description from apero where actif = 1")

for events in resEvents.fetchall():
    #Convert date
    print events
    eventDate = datetime.datetime.strptime(events[1], "%Y-%m-%d %H:%M:%S")

    if currentDate >= eventDate:
        #Update
        cursor.execute("update apero set actif = 0 where rowid = ?", events[0])

    else:
        #Tweet msg
        bot.update_status(msg % (events[1], events[2], events[3], events[4]))
