#! /usr/bin/python3
"""
    InstabotAI - Instagram Bot With Face Detection
    Intro:
    This bot autoscrape users from variable output -l
    if a face is detected it will repost, repost to
    stories, send DM to users, like and comment that
    photo. If no face is detected in image it will
    scrape the next profile in list.

    Github:
    https://github.com/instagrambot/instabotai

    Workflow:
    Repost best photos from users to your account
    By default bot checks username_database.txt
    The file should contain one username per line!
"""
import face_recognition
import instagram_scraper as insta
from instabot import Bot, utils
import argparse
import os
import sys
import json
import time
import logging
from random import randint
from tqdm import tqdm
import random

# Config
image_comment = "Wow nice picture, i have just reposted it"

# Logging Output default settings
logging.basicConfig(stream=sys.stdout, format='',
                level=logging.INFO, datefmt=None)
log = logging.getLogger(__name__)

# Parse arguments from Cli into variables
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-l', type=str, help="therock,kimkardashian")
parser.add_argument('-t', type=str, help="#hotgirls,#models,#like4like")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('-file', type=str, help="users filename")
parser.add_argument('-amount', type=int, help="amount", default=1)
parser.add_argument('users', type=str, nargs='*', help='users')
args = parser.parse_args()
InstaUsername = args.u



## Seperate users into list file
def help_output():
    if not args.u:
        log.info('python3 example.py -u for username -p password -l therock,kimkardashian -t "#like4like#follow4follow"')
        sys.exit()

help_output()

userlist = args.l
instagramtags = args.t

username = InstaUsername

sys.path.append(os.path.join(sys.path[0], '../'))

USERNAME_DATABASE = 'username_database.txt'
POSTED_MEDIAS = 'posted_medias.txt'

with open('instaprofiles.txt', 'w') as f:
    if f:
        userlist = userlist.replace(",", "\n")
    f.write(userlist)

# Open Userdb and put them into a list also write your username to database
def open_profiles():
    # Profiles to scrape and repost
    global insta_profiles
    insta_profiles = []

    with open("instaprofiles.txt") as f:
        insta_profiles = f.read().splitlines()
        f.close()

    # Output userenames in a txt file
    global userdb
    userdb = '\n'.join(insta_profiles)+'\n'
    with open('userdb.txt', 'w') as f:
        f.write(userdb)

    global username
    time.sleep(1)
    with open('username_database.txt', 'w') as f:
        f.write(username)

number_last_photos = 3
x = 0

def watch_stories():
    args.u = InstaUsername

    if len(sys.argv) >= 2:
        print(
            """
                Going to get '%s' likers and watch their stories (and stories of their likers too).
            """ % (insta_profiles[x])
        )
        user_to_get_likers_of = bot.convert_to_user_id(insta_profiles[x])
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
            if bot.watch_users_reels(liker_ids):
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

def increment():
    global x
    x = x+1


def bot_upload_photo(instapath, tags, media_id):
    ''' Upload photo to instagram'''
    bot.api.upload_photo(instapath, tags)
    log.info("Reposted: " + media_id)

def bot_like(media_id):
    ''' Like image on instagram '''
    bot.api.like(media_id)
    log.info("Liked media id: " + media_id)

def bot_comment(media_id, image_comment):
    ''' Comment image on instagram '''
    bot.comment(media_id, image_comment)
    log.info("Commented: " + media_id)

def send_dm(scraped_user_id):
    ''' send dm on instagram '''
    bot.send_message("hi i just reposted your photo", scraped_user_id)
    log.info("Private dm send to " + scraped_user_id)
    log.info("Wait 2200 - 2600 sec for next repost")

def file_creator(file_ending, encoding, write):
    ''' File creator for log files '''
    with open(username + file_ending, encoding) as f:
        file_output = f.write(str(write))
        return file_output

def random_sleep(number1, number2):
    ''' Random sleep between two numbers'''
    time_sleep = time.sleep(randint(number1, number2))
    return time_sleep


def InstaImageScraper():
    ''' Scrape image on profiles '''
    imgScraper = insta.InstagramScraper(usernames=[insta_profiles[x]],
                                        maximum=number_last_photos,
                                        media_metadata=True, latest=True,
                                        media_types=['image'])
    imgScraper.scrape()
    print("image scraping is running, please wait 50 seconds.")

def face_detection(path_to_image, new_media_id, media_id):
    ''' Face Detection for image '''
    image = face_recognition.load_image_file(path_to_image)
    face_locations = face_recognition.face_locations(image)
    # If no face located scrape the next profile
    if not face_locations:
        log.info("There is no Face Detected scraping next profile")
        increment()
        log.info(scraped_user)
        random_sleep(1, 6)
        instascraper(bot, new_media_id, path=POSTED_MEDIAS)
    else:
        log.info("There is a Face Detected scraping and posting this image")
        log.info(scraped_user)
        random_sleep(1, 2)
        log.info("Media Id:" + str(media_id))
        log.info("Face Location: " + str(face_locations))
        log.info("Path to image: " + path_to_image)

# Instagram manipulate image and repost them
# While x is less than instaprofiles loop this
def instascraper(bot, new_media_id, path=POSTED_MEDIAS):
    InstaImageScraper()
    random_sleep(1, 5)
    global x
    while x < len(insta_profiles):
        try:
            # Open insta_profiles[x] and it's scraped
            # json file take first image location
            with open(insta_profiles[x]
                      + '/' + insta_profiles[x] + '.json', 'r') as j:
                global scraped_user
                scraped_user = insta_profiles[x]
                json_data = json.load(j)
                time.sleep(randint(1, 10))
                newstr = (json_data["GraphImages"][0]["display_url"])
                # Output media id of image
                media_id = (json_data["GraphImages"][0]["id"])
                log.info("Found media id: " + media_id)
                random_sleep(1, 5)
                logging.info("image string generated " + newstr)
                time.sleep(randint(1, 5))
                imgUrl = newstr.split('?')[0].split('/')[-1]
                global instapath
                instapath = insta_profiles[x] + '/' + imgUrl
                logging.info("Found Instagram Path to Image: " + instapath)
                random_sleep(1, 5)
                global tags
                tags = "@" + insta_profiles[x] + " " + instagramtags
                # Execute face_detection
                face_detection(instapath, new_media_id, media_id)
                # Append username info to csv file
                try:
                    file_creator('.tsv', 'a+', saveStats)
                    with open(username + '.tsv', 'r') as f:
                        last_line = f.readlines()[-2].replace("False", "")
                    log.info("Date - Time - Followers - Following - Posts")
                    log.info(last_line)

                # Write username tsv file if it does not exist
                except:
                    file_creator('.tsv', 'w+', saveStats)
                    with open(username + '.tsv', 'r') as f:
                        last_line = f.readlines()[-1]
                    log.info("Date - Time - Followers - Following - Posts")
                    log.info(last_line)

                # Append username info to csv file
                try:
                    file_creator('_posted.tsv', 'a+', imgUrl + '\n')
                    with open(username + '_posted.tsv', 'r') as f:
                        last_line = f.readlines()[-1]
                    with open(username + '_posted.tsv', 'r') as f:
                        all_lines = f.readlines()[0:-2]
                        all_lines = (str(all_lines))
                    log.info("Posted Media")
                    log.info(last_line)
                    # if imgurl is in file username_posted scrape next profile
                    if str(imgUrl) in str(all_lines):
                        try:
                            log.info("Image found in database scraping next profile")
                            x += 1
                            log.info("image found of: " + scraped_user)
                            random_sleep(1, 2)
                            instascraper(bot, new_media_id, path=POSTED_MEDIAS)

                        except:
                            log.info("image found of: " + scraped_user)
                            x += 1
                            random_sleep(1, 2)
                            instascraper(bot, new_media_id, path=POSTED_MEDIAS)

                # Write username tsv file if it does not exist
                except:
                    file_creator('_posted.tsv', 'a+', imgUrl + '\n')
                    with open(username + '_posted.tsv', 'r') as f:
                        last_line = str(f.readlines()[-1])
                        all_lines = str(f.readlines()[0:-2])

                    log.info("Posted media")
                    logging(last_line)
                    if imgUrl in all_lines:
                        log.info("Image found in database scraping next profile")
                        x += 1
                        log.info("image of " + scraped_user)
                        random_sleep(1, 2)
                        instascraper(bot, new_media_id, path=POSTED_MEDIAS)

            # Execute the repost function
            random_sleep(1, 2)
            # Repost image as story
            log.info("Waiting")
            random_sleep(100, 120)
            bot.upload_story_photo(instapath)
            log.info("Photo Uploaded to Story")
            # Like Image
            bot_like(media_id)
            random_sleep(10, 25)
            # Comment on Image
            bot_comment(media_id, image_comment)
            random_sleep(11, 26)
            # Repost image
            bot_upload_photo(instapath, tags, media_id)
            random_sleep(2, 5)
            print(user_id)
            scraped_user_id = bot.get_user_id_from_username(scraped_user)
            send_dm(scraped_user_id)
            random_sleep(2,5)
            watch_stories()
#            random_sleep(3200, 3800)
        except:
            log.info("image set to private " + scraped_user)
            x += 1
            random_sleep(10, 22)
            instascraper(bot, new_media_id, path=POSTED_MEDIAS)
        x += 1
    x = 0
    random_sleep(5, 10)
    instascraper(bot, new_media_id, path=POSTED_MEDIAS)


# All main stuff gets executed
open_profiles()
random_sleep(5, 10)
bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)
random_sleep(5, 10)
user_id = bot.get_user_id_from_username(args.u)
username = bot.get_username_from_user_id(user_id)
saveStats = bot.save_user_stats(username)
users = None
if args.users:
    users = args.users
elif args.file:
    users = utils.file(args.file).list
instascraper(bot, users, args.amount)
