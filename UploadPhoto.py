#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI

from IG_secrets import username_string, password_string  # yeah baby...


def upload_photo(photo_path, caption):
    IGAPI = InstagramAPI(username_string, password_string)
    IGAPI.login()  # login
    IGAPI.uploadPhoto(photo_path, caption=caption)


if __name__ == '__main__':
    test_path = "/Users/maxwellmckinnon/Downloads/awesome-plant-wallpaper-1.jpg"
    hashtags = "#plantsofinstagram #plantsmakepeoplehappy #orchid #orchids #orchidsofinstagram #instaorchid #wild #wildlifeplanet"
    upload_photo(test_path, caption=hashtags)
