#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
For every account:
Grab a top photo (from Google, instagram, etc.)
upload it to the account
"""
import os
import tempfile
from google_images_download import google_images_download
import datetime
import random
import UploadPhoto
import time
import yaml


def download_photo(keywords="Interesting Plants", offset=0, google_search_additional_arguments={}):
    """
    Use google_images_download to download one image and return the path to it

    ISSUE: google image downloader fails often for offsets over 100
    :return:
    """
    tmpdir = tempfile.mkdtemp()
    print(f"Temp dir: {tmpdir}")
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords": keywords,
        "limit": offset,  # if lower than offset, doesn't download anything
        # "color": "green",
        # "size": ">800*600",
        "print_urls": True,
        "output_directory": tmpdir,
        "offset": offset  # In the future, probably need to randomize this and pull just one or so images
    }
    # Merge dicts
    if google_search_additional_arguments:
        for item in google_search_additional_arguments:
            arguments[item] = google_search_additional_arguments[item]

    print(f"Composed arguments: {arguments}")
    path = response.download(arguments)
    print(f"Image File Paths: {path}")

    return path[keywords][0]  # only works for one image mode


def download_bunch_photos_test():
    """
    Use google_images_download
    :return:
    """
    tmpdir = tempfile.mkdtemp()
    print(f"Temp dir: {tmpdir}")
    response = google_images_download.googleimagesdownload()
    arguments = {
        "Records": [
            {
                "keywords": "Interesting Plants",
                "limit": 30,
                "color": "green",
                "size": ">800*600",
                "print_urls": True,
                "output_directory": tmpdir,
                "offset": 0  # In the future, probably need to randomize this and pull just one or so images
            },
            {
                "keywords": "Really Interesting Plants",
                "limit": 30,
                "print_urls": True,
                "output_directory": tmpdir
            }
        ]
    }
    for record in arguments["Records"]:
        paths = response.download(record)
        print(f"Image File Paths: {paths}")


def download_and_post_photo(config):
    """
    Downloads a photo and posts it to account

    :param config: A single account dict parsed from accounts_config.yml
    :return:
    """

    r = random.Random()
    rint = r.randint(0, 100)
    print(f"Random offset: {rint}")
    keywords = config["google_search_keywords"]
    google_search_additional_arguments = config["google_search_additional_arguments"]
    photo_path = download_photo(keywords=keywords, offset=rint, google_search_additional_arguments=google_search_additional_arguments)

    # Randomly sample and downsize from the hashtags
    final_caption = generate_caption(config)
    print(f"Using captions: {final_caption}")
    password = config["password"]
    account_name = config["account_name"]
    UploadPhoto.upload_photo(photo_path, final_caption, account_name, password)


def sample_and_downsize_words(words, keep_ratio=.70):
    """
    Subsample from hashtags, intended for posting with image
    :param words: e.g. "#A #B #C"
    :return: string of subsampled hashtags

    >>> sample_and_downsize_words("#A #B #C", keep_ratio=.70)
    "#C #A"
    """
    hashtag_choices = words.split()
    random.shuffle(hashtag_choices)
    keep_amount = int(keep_ratio * len(hashtag_choices))
    hashtag_choices = hashtag_choices[:keep_amount]
    final_hashtag_choices = " ".join(hashtag_choices)
    return final_hashtag_choices


def generate_caption(config):
    """

    :param config: single config dict from secrets.yml, contains account_name
    :param hashtags:
    :return:
    """
    account_tag = "@" + config['account_name']
    maincaption = ""  # Tbd, ML generated buzz words?
    maincaption_emojis = "😇 ☘️ 🙏 ☺️"  # yaml doesn't support emoji so doing them here for now
    maincaption_emojis = sample_and_downsize_words(maincaption_emojis)
    hashtags = config['ig_hashtags']
    hashtags = sample_and_downsize_words(hashtags)
    finalcaption = f"{maincaption} {maincaption_emojis} ~*~*~*~*~ {hashtags} ~*~*~*~*~ Follow {account_tag} for more!"
    return finalcaption


if __name__ == '__main__':
    test = True
    configfile = "accounts_config.yml"
    with open(configfile, 'r') as stream:
        config = yaml.load(stream)

    for account in config:
        current_config = config[account]
        account_name = current_config['account_name']
        print(f"Account name: {account_name}")
        # if "botting" not in account_name:
        #     continue

        # Merge passwords into current_config dict
        with open("secrets.yml", 'r') as stream:
            pw = yaml.load(stream)
        print("Adding password in config")
        current_config['password'] = pw[account_name]

        if test:
            for _ in range(4):
                try:
                    download_and_post_photo(current_config)
                except Exception as e:
                    print(f"e: {e}")
                time.sleep(10)
        else:
            while True:
                download_and_post_photo()
                time.sleep(1*60*60*4)  # Sleep 4 hours