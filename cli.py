from instabotai import ai
import argparse

try:
    input = raw_input
except NameError:
    pass


COOKIES = {}
bot = ai.Bot(do_logout=True)

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()
username = str(args.u)


# Check if user cookie exist
bot.login(username=args.u, password=args.p, proxy=args.proxy, use_cookie=True)
#ai.Bots.follow_users_hashtag_ai("fitness, programming", 5)
#ai.Bots.follow_users_followers_ai("japenhaven", 20)
ai.Bots.follow_users_following_ai("japanheaven", 20)
#ai.Bots.follow_users_ai("japanheaven", 20)
#ai.Bots.user_hashtag_comment("fitness, models, friends", "wow please follow me back, wow nice profile, awesome profile", 10)
#ai.Bots.like_hashtags("model", 4)
#ai.Bots.like_following("japanheaven", 20)
#ai.Bots.like_followers("japanheaven", 20)
#ai.Bots.repost_users_images("japanheaven, timferris, ariana, sjaaybee", "#models", 10)
