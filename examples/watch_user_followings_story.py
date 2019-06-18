"""
    Watch user followings stories!
    This script could be very useful to attract someone's audience to your account.

    If you will not specify the user_id, the script will use your likers as targets.

    Dependencies:
        pip install -U instabot

    How to use:
    python watch_stories.py -u username -p password kimkardashian

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
parser.add_argument('users', type=str, nargs='+', help='users')
args = parser.parse_args()
args.users = ''.join(args.users)

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)


if len(sys.argv) >= 3:
    print(
        """
            Going to get '%s' likers and watch their stories (and stories of their likers too).
        """ % (args.users)
    )
    user_to_get_likers_of = bot.convert_to_user_id(args.users)

current_user_id = user_to_get_likers_of
while True:
    try:
        # GET USER FOLLOWERS
        if not bot.api.get_user_followings(current_user_id):
            print("Can't get followers of user_id=%s" % current_user_id)

        # GET USER FROM FOLLOWERS
        scraped_user = random.choice(bot.api.last_json["users"])
        user_id = scraped_user["pk"]

        # WATCH USERS STORIES
        if bot.watch_users_reels(user_id):
            print("Total stories viewed: %d" % bot.total["stories_viewed"])


    except Exception as e:
        # If something went wrong - sleep long and start again
        print("Exception:", str(e))
        current_user_id = user_to_get_likers_of
        time.sleep(10 * random.random() + 10)
