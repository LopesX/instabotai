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
from tqdm import tqdm
import logging
from random import randint

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

with open('instaprofiles.txt', 'w') as f:
    if f:
        userlist = userlist.replace(",", "\n")
    f.write(userlist)


username = InstaUsername

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

sys.path.append(os.path.join(sys.path[0], '../'))


USERNAME_DATABASE = 'username_database.txt'
POSTED_MEDIAS = 'posted_medias.txt'

# Instagram image scraper
def InstaImageScraper():
    imgScraper = insta.InstagramScraper(usernames=[insta_profiles[x]],
                                        maximum=number_last_photos,
                                        media_metadata=True, latest=True,
                                        media_types=['image'])
    imgScraper.scrape()
    print("image scraping is running, please wait 50 seconds.")

# Instagram manipulate image and repost them
# While x is less than instaprofiles loop this
def instascraper(bot, new_media_id, path=POSTED_MEDIAS):
    InstaImageScraper()
    time.sleep(randint(1, 5))
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
                time.sleep(randint(5, 10))
                logging.info("image string generated " + newstr)
                time.sleep(randint(1, 5))
                imgUrl = newstr.split('?')[0].split('/')[-1]
                global instapath
                instapath = insta_profiles[x] + '/' + imgUrl
                logging.info("Found Instagram Path to Image: " + instapath)
                time.sleep(randint(1, 5))
                global tags
                tags = "@" + insta_profiles[x] + " " + instagramtags
                # Execute Face Detection
                # Locate Face On image scraped
                image = face_recognition.load_image_file(instapath)
                face_locations = face_recognition.face_locations(image)
                # If no face located scrape the next profile
                if not face_locations:
                    log.info("There is no Face Detected scraping next profile")
                    x += 1
                    log.info(scraped_user)
                    time.sleep(randint(5, 10))
                    instascraper(bot, new_media_id, path=POSTED_MEDIAS)
                else:
                    log.info("There is a Face Detected scraping and posting this image")
                    log.info(scraped_user)
                    time.sleep(randint(5, 10))
                    log.info("Media Id:" + str(media_id))
                    log.info("Face Location: " + str(face_locations))
                    log.info("Path to image: " + instapath)


                # Append username info to csv file
                try:
                    with open(f'{username}.tsv', 'a+') as f:
                        f.write(str(saveStats))
                    with open(f'{username}.tsv', 'r') as f:
                        last_line = f.readlines()[-2].replace("False", "")
                    log.info("Date - Time - Followers - Following - Posts")
                    log.info(last_line)

                # Write username tsv file if it does not exist
                except:
                    with open(f'{username}.tsv', 'w+') as f:
                        f.write(str(saveStats))
                    with open(f'{username}.tsv', 'r') as f:
                        last_line = f.readlines()[-1]
                    log.info("Date - Time - Followers - Following - Posts")
                    log.info(last_line)

                # Append username info to csv file
                try:
                    with open(username + '_posted.tsv', 'a+') as f:
                        f.write(str(imgUrl + "\n"))
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
                            time.sleep(randint(5, 10))
                            instascraper(bot, new_media_id, path=POSTED_MEDIAS)

                        except:
                            log.info("image found of: " + scraped_user)
                            x += 1
                            time.sleep(randint(5, 20))
                            instascraper(bot, new_media_id, path=POSTED_MEDIAS)

                # Write username tsv file if it does not exist
                except:
                    with open(username + '_posted.tsv', 'a+') as f:
                        f.write(str(imgUrl + "\n"))
                    with open(username + '_posted.tsv', 'r') as f:
                        last_line = str(f.readlines()[-1])
                        all_lines = str(f.readlines()[0:-2])

                    log.info("Posted media")
                    logging(last_line)
                    if imgUrl in all_lines:
                        log.info("Image found in database scraping next profile")
                        x += 1
                        log.info("image of " + scraped_user)
                        time.sleep(randint(5, 20))
                        instascraper(bot, new_media_id, path=POSTED_MEDIAS)

            # Execute the repost function
            time.sleep(randint(20, 40))
            # Like Image
            bot.api.like(media_id)
            log.info("Liked media id: " + media_id)
            time.sleep(randint(20, 50))
            # Comment on Image
            bot.comment(media_id, image_comment)
            log.info("Commented: " + media_id)
            time.sleep(randint(20, 40))
            # Repost image
            #repost_best_photos(bot, users, args.amount)
            bot.api.upload_photo(instapath,tags)
            log.info("Reposted: " + media_id)
            # Repost image as story
 #           time.sleep(randint(20, 50))
#            bot.upload_story_photo(instapath)
#            log.info("Photo Uploaded to Story")
            # Send private DM to user it reposted
            time.sleep(randint(20, 60))
            print(user_id)
            scraped_user_id = bot.get_user_id_from_username(scraped_user)
            bot.send_message("hi i just reposted your photo", scraped_user_id)
            log.info("Private dm send to " + scraped_user_id)
            log.info("Wait 2200 - 2600 sec for next repost")
            time.sleep(randint(3200, 3800))
        except:
            log.info("image set to private " + scraped_user)
            x += 1
            time.sleep(randint(5, 20))
            instascraper(bot, new_media_id, path=POSTED_MEDIAS)
        x += 1
    x = 0
    time.sleep(randint(10, 30))
    instascraper(bot, new_media_id, path=POSTED_MEDIAS)




open_profiles()
time.sleep(randint(5, 30))
bot = Bot()
#bot.login(username=InstaUsername)
bot.login(username=args.u, password=args.p)
time.sleep(randint(10, 30))
user_id = bot.get_user_id_from_username(args.u)
username = bot.get_username_from_user_id(user_id)
#print(f"Welcome {username} your userid is {user_id}")
saveStats = bot.save_user_stats(username)
users = None
if args.users:
    users = args.users
elif args.file:
    users = utils.file(args.file).list
instascraper(bot, users, args.amount)
