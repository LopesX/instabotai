"""
    Instabotai Like all comments example
    Workflow:
        Like All replied image comments pictures.
        Find Feed images -> find x image_id -> Like x image comments
"""

import argparse
import os
import sys
import time
import json

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
x = 0

while True:
    try:
        bot.api.get_self_user_feed()
        item = bot.api.last_json["items"][x]["caption"]["media_id"]
        bot.like_media_comments(item)
        time.sleep(1)
        x += 1
        print("Like comments on next picture")
    except:
        print("Like comments on next picture")
        x += 1
