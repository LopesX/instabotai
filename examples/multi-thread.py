import argparse
import threading
import os
from multiprocessing import Pool
import sys
import time
import random
sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

def watchstories():
    number = 0
    while True:
        hashtags = ["instagood", "love","photooftheday","fashion","beautiful","happy","cute","like4like","followme","picoftheday","follow","me","summer","art","instadaily","friends","repost","nature","girl","fun","style","smile","food","instalike","follow4follow","igers","life","beauty","amazing","instagram","instagood","photooftheday","fashion","beautiful","happy","cute","tbt","like4like","followme","picoftheday","follow","me","selfie","summer","art","instadaily","friends","repost","nature","girl","fun","style","smile","food","instalike","family","travel","likeforlike","fitness","follow4follow","igers","tagsforlikes","nofilter","life","beauty","amazing","instagram","photography","photo","vscocam","sun","music","followforfollow","beach","ootd","bestoftheday","sunset","dog","sky","makeup","foodporn","f4f","hair","pretty","cat","model","swag","motivation","girls","party","baby","cool","gym","lol","design","instapic","funny","healthy","christmas","night","lifestyle","yummy","flowers","tflers","hot","handmade","instafood","wedding","fit","black","pink","blue","workout","work","blackandwhite","drawing","inspiration","holiday","home","london","nyc","sea","instacool","winter","goodmorning","blessed",]
        print("Dette er en loop")
        bot.api.get_hashtag_stories(random.choice(hashtags))
        json = bot.api.last_json
        try:
            for w in json["story"]["items"]:
                print(w["user"]["username"])
                if bot.api.see_reels(w) == True:
                    print(bot.api.see_reels(w))
                    number += 1
                    print("Story Watched. Total: " + str(number))
                    time.sleep(15)
                if bot.api.see_reels(w) == False:
                    print(bot.api.see_reels(w))
                    print("Falling asleep")
                    time.sleep(200 + random.random())
        except:
            print("error")
            pass

def like_self_media_comments():
    x = 0
    while True:
        try:
            for medias in bot.get_total_user_medias(bot.user_id):
                bot.like_media_comments(medias)
                print("sleeping for 120 seconds")
                time.sleep(120)
                x += 1
                print("Like comments on next picture")
        except:
            time.sleep(120)
            print("Like comments on next picture")
            like_self_media_comments()

def reply_pending_messages():
    reply_pending = 0
    while True:
        try:
            bot.api.get_pending_inbox()
            for w in bot.api.last_json["inbox"]["threads"]:
                thread_id = w["thread_id"]
                username = w["users"][0]["username"]
                full_name = w["users"][0]["full_name"]
                userid = bot.get_user_id_from_username(username)
                reply_pending += 1
                print("Reply pending message " + thread_id)
                print("Replied Pending messages: " + str(reply_pending))
                bot.api.approve_pending_thread(thread_id)
                bot.send_message("Thanks " +str(full_name) +  ", please comment and like all my pictures also follow me", userid, thread_id=thread_id)
                time.sleep(60)
        except:
            time.sleep(160)
            pass

def reply_messages():
    replied = 0
    while True:
        try:
            bot.api.getv2Inbox()
            for w in bot.api.last_json["inbox"]["threads"]:
                thread_id = w["thread_id"]
                username = w["users"][0]["username"]
                full_name = w["users"][0]["full_name"]
                userid = bot.get_user_id_from_username(username)
                print("reply message to " + thread_id)
                replied += 1
                print("Replied messages " + replied)
                bot.send_message("Thanks again " +str(full_name) +  ", please do it for me!", userid, thread_id=thread_id)
                time.sleep(60)
        except:
            time.sleep(160)
            pass





#thread1 = threading.Timer(5.0, watchstories)
thread2 = threading.Timer(3.0, like_self_media_comments)
#thread3 = threading.Timer(7.0, reply_messages)
thread4 = threading.Timer(10.0, reply_pending_messages)
#thread1.start()
thread2.start()
#thread3.start()
thread4.start()
