"""
    Watch user likers stories!
    This script could be very useful to attract someone's audience to your account.

    If you will not specify the user_id, the script will use your likers as targets.

    Dependencies:
        pip install -U instabot

    Notes:
        You can change file and add there your comments.
"""

import os
import sys
import time
import random
import argparse



# in case if you just downloaded zip with sources
sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)
args.u = "demirosemawby"

if len(sys.argv) >= 2:
    print(
        """
            Going to get '%s' likers and watch their stories (and stories of their likers too).
        """ % (args.u)
    )
    user_to_get_likers_of = bot.convert_to_user_id(args.u)
else:
    print(
        """
            Going to get your likers and watch their stories (and stories of their likers too).
            You can specify username of another user to start (by default we use you as a starting point).
        """
    )
    user_to_get_likers_of = bot.user_id

current_user_id = user_to_get_likers_of
while True:
    try:
        # GET USER FEED
        if not bot.api.get_user_feed(current_user_id):
            print("Can't get feed of user_id=%s" % current_user_id)

        # GET MEDIA LIKERS
        user_media = random.choice(bot.api.last_json["items"])
        if not bot.api.get_media_likers(media_id=user_media["pk"]):
            print(
                "Can't get media likers of media_id='%s' by user_id='%s'" % (user_media["pk"], current_user_id)
            )

        likers = bot.api.last_json["users"]
        liker_ids = [
            str(u["pk"]) for u in likers if not u["is_private"] and "latest_reel_media" in u
        ]

        # WATCH USERS STORIES
        if bot.watch_users_reels(liker_ids[:25]):
            print("Total stories viewed: %d" % bot.total["stories_viewed"])

        # CHOOSE RANDOM LIKER TO GRAB HIS LIKERS AND REPEAT
        current_user_id = random.choice(liker_ids)

        if random.random() < 0.05:
            current_user_id = user_to_get_likers_of
            print("Sleeping and returning back to original user_id=%s" % current_user_id)
            time.sleep(10 * random.random() + 10)

    except Exception as e:
        # If something went wrong - sleep long and start again
        print("Exception:", str(e))
        current_user_id = user_to_get_likers_of
        time.sleep(10 * random.random() + 10)
