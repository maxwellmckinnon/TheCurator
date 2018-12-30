#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Grab a top photo from Google, upload it to the account
"""
import os
import tempfile
from google_images_download import google_images_download
import datetime
import random
import UploadPhoto
import time


def download_photo(keywords="Interesting Plants", offset=0):
    """
    Use google_images_download to download one image and return the path to it
    :return:
    """
    tmpdir = tempfile.mkdtemp()
    print(f"Temp dir: {tmpdir}")
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords": keywords,
        "limit": offset,  # if lower than offset, doesn't download anything
        "color": "green",
        "size": ">800*600",
        "print_urls": True,
        "output_directory": tmpdir,
        "offset": offset  # In the future, probably need to randomize this and pull just one or so images
    }
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


def download_and_post_photo():
    """
    Downloads a photo and posts it to account

    :return:
    """
    caption = "#plantsofinstagram #plantsmakepeoplehappy #orchid #orchids #orchidsofinstagram #instaorchid #wild #wildlifeplanet #plantlivesmatter #plantlove #plantatree #plant #plants #beautiful #nature"

    r = random.Random()
    rint = r.randint(0, 100)
    print(f"Random offset: {rint}")
    photo_path = download_photo(offset=rint)

    # Randomly sample and downsize from the hashtags
    caption_choices = caption.split()
    random.shuffle(caption_choices)
    perc_70 = int(7/10 * len(caption_choices))
    caption_choices = caption_choices[:perc_70]
    final_caption_choices = " ".join(caption_choices)
    print(f"Using captions: {final_caption_choices}")
    UploadPhoto.upload_photo(photo_path, final_caption_choices)


if __name__ == '__main__':
    test = True
    if test:
        for _ in range(4):
            try:
                download_and_post_photo()
            except Exception as e:
                print(f"e: {e}")
            time.sleep(10)
    else:
        while True:
            download_and_post_photo()
            time.sleep(1*60*60*24)  # Sleep 1 day