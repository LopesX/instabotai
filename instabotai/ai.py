import os
from instabot import Bot
import argparse
import time
import threading
import random
import sys
from mtcnn.mtcnn import MTCNN
import cv2
import json
import random
import logging

try:
    input = raw_input
except NameError:
    pass

COOKIES = {}
bot = Bot(do_logout=True)

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()
username = str(args.u)


# Check if user cookie exist
bot.login(username=args.u, password=args.p, proxy=args.proxy, use_cookie=True)


class Bots:
    def __init__(self, username):
        self.username = username

    def face_detection(username):
        x = 0
        ''' Get user media and scan it for a face'''
        user_id = bot.get_user_id_from_username(username)
        medias = bot.get_user_medias(user_id, filtration=False)
        for media in medias:
            while x < 1:
                try:
                    bot.logger.info(media)
                    path = bot.download_photo(media, folder=username)
                    img = cv2.imread(path)
                    detector = MTCNN()
                    detect = detector.detect_faces(img)
                    if not detect:
                        bot.logger.info("no face detected")
                        x += 1

                    elif detect:
                        bot.logger.info("there was a face detected")
                        bot.api.like(media)
                        display_url = bot.get_link_from_media_id(media)
                        bot.logger.info("liked " + display_url + " by " + username)
                        x += 1
                    else:
                        x += 1

                except Exception as e:
                    bot.logger.info(e)
                    x += 1

    def like_followers(username, time_sleep):
        user_id = bot.get_user_id_from_username(username)
        followers = bot.get_user_followers(user_id)

        for user in followers:
            pusername = bot.get_username_from_user_id(user)
            Bots.face_detection(pusername)
            time.sleep(int(time_sleep))


    def like_following(username, time_sleep):
        user_id = bot.get_user_id_from_username(username)
        following = bot.get_user_following(user_id)

        for user in following:
            pusername = bot.get_username_from_user_id(user)
            Bots.face_detection(pusername)
            time.sleep(int(time_sleep))

    def like_hashtags(hashtag, time_sleep):
        hashtags = bot.get_hashtag_users(hashtag)
        for user in hashtags:
            pusername = bot.get_username_from_user_id(user)
            Bots.face_detection(pusername)
            time.sleep(int(time_sleep))
