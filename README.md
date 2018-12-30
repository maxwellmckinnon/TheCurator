# Curator

#### Curator
tbd

See `Instagram-API-python/examples/upload_photo.py`

```python
In [3]: InstagramAPI.login()
Request return 429 error!
{'message': 'Please wait a few minutes before you try again.', 'status': 'fail'}
Request return 404 error!
Login success!

Out[3]: True

In [4]: photo_path = "/Users/maxwellmckinnon/Downloads/tumblr_o1pgscSKLA1taxd57o1_1280.jpg"

In [5]: caption = "Sun's up Dewd!"

In [6]: InstagramAPI.uploadPhoto(photo_path, caption=caption)
Out[6]: False

In [7]: caption += " #plants #plantsofinstagram #plantsmakepeoplehappy #orchid #orchids #orchidsofinstagram #instaorchid #wild #wildlifeplanet"

In [8]: caption
Out[8]: "Sun's up Dewd! #plants #plantsofinstagram #plantsmakepeoplehappy #orchid #orchids #orchidsofinstagram #instaorchid #wild #wildlifeplanet"

In [9]: InstagramAPI.uploadPhoto(photo_path, caption=caption)
Out[9]: False

```


#### Dumb likebot/followbot
python RobertPlant.py

