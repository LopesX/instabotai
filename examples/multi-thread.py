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
    while True:
        try:
            time.sleep(10)
            # GET USER FEED
            if not bot.api.get_user_feed(current_user_id):
                bot.logger.info("Can't get feed of user_id=%s" % current_user_id)

            # GET MEDIA LIKERS
            user_media = random.choice(bot.api.last_json["items"])
            if not bot.api.get_media_likers(media_id=user_media["pk"]):
                bot.logger.info(
                    "Can't get media likers of media_id='%s' by user_id='%s'" % (user_media["pk"], current_user_id)
                )

            likers = bot.api.last_json["users"]
            liker_ids = [
                str(u["pk"]) for u in likers if not u["is_private"] and "latest_reel_media" in u
            ][:20]

            # WATCH USERS STORIES
            if bot.watch_users_reels(liker_ids):
                bot.logger.info("Total stories viewed: %d" % bot.total["stories_viewed"])

            # CHOOSE RANDOM LIKER TO GRAB HIS LIKERS AND REPEAT
            current_user_id = random.choice(liker_ids)

            if random.random() < 0.05:
                current_user_id = user_to_get_likers_of
                bot.logger.info("Sleeping and returning back to original user_id=%s" % current_user_id)
                time.sleep(60 * random.random() + 60)

        except Exception as e:
            # If something went wrong - sleep long and start again
            bot.logger.info(e)
            current_user_id = user_to_get_likers_of
            time.sleep(260 * random.random() + 60)


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





thread1 = threading.Timer(5.0, watchstories)
thread2 = threading.Timer(3.0, like_self_media_comments)
#thread3 = threading.Timer(7.0, reply_messages)
thread4 = threading.Timer(10.0, reply_pending_messages)
thread1.start()
thread2.start()
#thread3.start()
thread4.start()
