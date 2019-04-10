#! /usr/bin/python3
"""
    Instagram Scraper with autoposter
    Intro:
    This bot autoscrape users from variable insta_profiles
    and repost them to your instagram, it also save your
    cookie,session and user stats.

    Github:
    https://github.com/reliefs/Instagram-scraper-with-autopost

    Workflow:
    Repost best photos from users to your account
    By default bot checks username_database.txt
    The file should contain one username per line!
"""
import face_recognition
import random
import argparse
import os
import sys
import json
import time
import csv
from tqdm import tqdm
import instagram_scraper as insta
from instabot import Bot, utils


# Instagram Info
InstaUsername = "siliconeheaven"


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

    global InstaUsername
    time.sleep(1)
    with open('username_database.txt', 'w') as f:
        f.write(InstaUsername)

number_last_photos = 1
x = 0

sys.path.append(os.path.join(sys.path[0], '../'))


USERNAME_DATABASE = 'username_database.txt'
POSTED_MEDIAS = 'posted_medias.txt'


def repost_best_photos(bot, users, amount=1):
    medias = get_not_used_medias_from_users(bot, users)
    medias = sort_best_medias(bot, medias, amount)
    for media in tqdm(medias, desc='Reposting photos'):
        repost_photo(bot, media)


# Sort best media this is not executed yet
def sort_best_medias(bot, media_ids, amount=1):
    best_medias = [bot.get_media_info(media)[0] for media in
                   tqdm(media_ids, desc='Getting media info')]
    best_medias = sorted(best_medias, key=lambda x:
                         (x['like_count'], x['comment_count']), reverse=True)
    return [best_media['pk'] for best_media in best_medias[:amount]]


def get_not_used_medias_from_users(bot, users=None,
                                   users_path=USERNAME_DATABASE):
    if not users:
        users = utils.file(users_path).list
    users = map(str, users)
    total_medias = []
    for user in users:
        medias = bot.get_user_medias(user, filtration=False)
        medias = [media for media in medias if not
                  exists_in_posted_medias(media)]
        total_medias.extend(medias)
    return total_medias


def exists_in_posted_medias(new_media_id, path=POSTED_MEDIAS):
    medias = utils.file(path).list
    return str(new_media_id) in medias


def update_posted_medias(new_media_id, path=POSTED_MEDIAS):
    medias = utils.file(path)
    medias.append(str(new_media_id))
    return True


def repost_photo(bot, new_media_id, path=POSTED_MEDIAS):
    if bot.upload_photo(instapath, tags):
        update_posted_medias(new_media_id, path)
        bot.logger.info('Media_id {0} is saved in {1}'
                        .format(new_media_id, path))


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('-file', type=str, help="users filename")
parser.add_argument('-amount', type=int, help="amount", default=1)
parser.add_argument('users', type=str, nargs='*', help='users')
args = parser.parse_args()


# Instagram image scraper
def InstaImageScraper():
    imgScraper = insta.InstagramScraper(usernames=[insta_profiles[x]],
                                        maximum=number_last_photos,
                                        media_metadata=True, latest=True,
                                        media_types=['image'])
    imgScraper.scrape()
    print("image scraping is running or not")


# Face recognition if face not detected scrape next profile
def recognize_face():
    # Locate Face On image scraped
    image = face_recognition.load_image_file(instapath)
    face_locations = face_recognition.face_locations(image)
    # If no face located scrape the next profile
    if not face_locations:
        print("There is no Face Detected scraping next profile")
        global x
        x += 1
        print(scraped_user)
        time.sleep(5)
        instascraper()
    else:
        print("There is a Face Detected scraping and posting this image")
        print(scraped_user)
        time.sleep(5)
    print(face_locations)
    print(instapath)


# Instagram manipulate image and repost them
# While x is less than instaprofiles loop this
def instascraper(bot, new_media_id, path=POSTED_MEDIAS):
    InstaImageScraper()
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
                print(json_data)
                time.sleep(5)
                newstr = (json_data["GraphImages"][0]["display_url"])
                print(newstr)
                time.sleep(5)
                imgUrl = newstr.split('?')[0].split('/')[-1]
                global instapath
                instapath = insta_profiles[x] + '/' + imgUrl
                print(instapath)
                time.sleep(5)
                global tags
                # If image have been posted goto next picture
                print(imgUrl)
                tags = f'''@{insta_profiles[x]} ##Model #Modeling #modelo
                #modellife #modelling #modelagency #Modelos #modelphotography
                #modelsearch #ModelStatus #modelingagency #modelfitness
                #ModelsWanted #modelshoot #modella #modelmanagement
                #modelscout #modeltest #modelindonesia #modele #modelife
                #modelmayhem #modelgirl #modell #modelslife #topmodel
                #modelcall #modelpose #ModelBehaviors'''

                # Execute Face recognition
                recognize_face()
                # Append username info to csv file
                try:
                    with open(f'{username}.tsv', 'a+') as f:
                        f.write(str(saveStats))
                    with open(f'{username}.tsv', 'r') as f:
                        last_line = f.readlines()[-2].replace("False", "")
                    print("Date - Time - Followers - Following - Posts")
                    print(last_line)

                # Write username tsv file if it does not exist
                except:
                    with open(f'{username}.tsv', 'w+') as f:
                        f.write(str(saveStats))
                    with open(f'{username}.tsv', 'r') as f:
                        last_line = f.readlines()[-1]
                    print("Date - Time - Followers - Following - Posts")
                    print(last_line)

                # Append username info to csv file
                try:
                    with open(f'{username}_posted.tsv', 'a+') as f:
                        f.write(str(imgUrl + "\n"))
                    with open(f'{username}_posted.tsv', 'r') as f:
                        last_line = f.readlines()[-1]
                    with open(f'{username}_posted.tsv', 'r') as f:
                        all_lines = f.readlines()[0:-2]
                        all_lines = (str(all_lines))
                    print("Posted Media")
                    print(last_line)
                    print("all posted medias")
                    print(all_lines)
                    # if imgurl is in file username_posted scrape next profile
                    if str(imgUrl) in str(all_lines):
                        try:
                            print(f"""Image found in database
                                  scraping next profile""")
                            x += 1
                            print("image found of: ", scraped_user)
                            time.sleep(5)
                            instascraper(bot, new_media_id, path=POSTED_MEDIAS)

                        except:
                            print("image found of: ", scraped_user)
                            x += 1
                            time.sleep(5)
                            instascraper(bot, new_media_id, path=POSTED_MEDIAS)

                # Write username tsv file if it does not exist
                except:
                    with open(f'{username}_posted.tsv', 'a+') as f:
                        f.write(str(imgUrl + "\n"))
                    with open(f'{username}_posted.tsv', 'r') as f:
                        last_line = str(f.readlines()[-1])
                        all_lines = str(f.readlines()[0:-2])

                    print("Posted media")
                    print(last_line)
                    print("All Posted Medias")
                    print(all_lines)
                    if imgUrl in all_lines:
                        print("Image found in database scraping next profile")
                        x += 1
                        print("image of ", scraped_user)
                        time.sleep(5)
                        instascraper()

            # Execute the repost function
            time.sleep(4)
            repost_best_photos(bot, users, args.amount)
            print("Posting Instagram")
            os.remove("posted_medias.txt")
            time.sleep(1000|1600)
        except:
            print("image set to private", scraped_user)
            x += 1
            time.sleep(5)
            instascraper(bot, new_media_id, path=POSTED_MEDIAS)

        x += 1
    x = 0
    instascraper()


# All main stuff gets executed
open_profiles()
time.sleep(5)
bot = Bot()
bot.login(username=InstaUsername)
user_id = bot.get_user_id_from_username(InstaUsername)
username = bot.get_username_from_user_id(user_id)
#print(f"Welcome {username} your userid is {user_id}")
saveStats = bot.save_user_stats(username)
users = None
if args.users:
    users = args.users
elif args.file:
    users = utils.file(args.file).list
instascraper(bot, users, args.amount)
