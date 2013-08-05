# -*- coding: utf-8 -*-

##GPL Licence ??? 2/3 ?

#---------- Import
import tweepy
import sqlite3
import time
import conf

#Use SQLite for history
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()
cursor.execute("create table if not exists apero (date date, lieu text, lieu_url text, description text, oui integer, non integer, ouinon integer, actif bool)")

#Use Tweepy api
auth = tweepy.OAuthHandler(conf.consumer_key, conf.consumer_secret)
auth.set_access_token(conf.access_token, conf.access_token_secret)
bot = tweepy.API(auth)

#Checking private message
for msg in bot.direct_messages():
    #msg = {"date" : "12/11/2013 14:00", "lieu" : "At home", "description" : "Party at home !", "lieu_url" : "http://t.co/GiBmA6jZCR"}
    try:
        data = eval(msg.text)
        #Get infos
        date_apero = time.strptime(data["date"], "%d/%m/%Y %H:%M")
        lieu_apero = data["lieu"]
        description_apero = data["description"]
        lieu_url = data["lieu_url"]
        actif_apero = True
        #Insert into datatable
        cursor.execute("insert into apero (date, lieu, lieu_url, description, actif) values (%s, '%s', '%s', '%s', %s)" %(date_apero, lieu_apero, lieu_url, description_apero, actif_apero))
        
        #Retweet for user
        bot.send_direct_message(user_id = msg.sender_id, text = "OK")
        
    except:
        print "Not a valid msg ..."
        
        #Retweet for user
        bot.send_direct_message(user_id = msg.sender_id, text = "Not a valid msg")
        
    #Destroy msg
    msg.destroy()
