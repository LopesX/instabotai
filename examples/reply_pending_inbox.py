"""
    instabot example
    Workflow:
        Reply to all pending messages in inbox.
        Find all pending messages in inbox -> Accept messages -> reply to message.
"""

import argparse
import os
import sys
import time

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
while True:
    try:
        bot.api.get_pending_inbox()
        for w in bot.api.last_json["inbox"]["threads"]:
            thread_id = w["thread_id"]
            username = w["users"][0]["username"]
            userid = bot.get_user_id_from_username(username)
            print(thread_id)
            bot.api.approve_pending_thread(thread_id)
            time.sleep(125|155)
            bot.send_message("Thanks please like all my pictures and follow me", userid, thread_id=thread_id)
    except:
        pass

