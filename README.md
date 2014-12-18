Your Friendly Tumblr Image Bot
====================
A project for LIS 664 - Programming for Cultural Heritage<br>
by Bill Levay<br>
Pratt Institute School of Information and Library Science

These scripts allow a user to scrape image-gallery style web pages to collect image URLs and metadata and then publish those images as Tumblr photo posts.

Developed specifically for the [ARChive of Contemporary Music](http://arcmusic.org) as an "Image of the Day" social media robot.

## How to Use

There are two components that can be used separately or in concert:
1. The web scraper grabs image URLs and metadata and writes them to a JSON file
2. The photo post creater sends a user-determined number of photo posts to Tumblr, then marks those images as "posted" in the JSON file.

You'll need to rename ```settings-example.py``` to ```settings.py``` in order to tailor these scripts to your needs.

### Web Scraper

To run:
```
$ python3 scrape.py
```

TO DO...

### Tumblr Poster

This script utilizes [pytumblr](https://github.com/tumblr/pytumblr), a Tumblr API v2 Client. This module is not currently compatible with Python 3. I've been running it successfully in Python 2.7. 

Set up a Tumblr blog, then follow the [instructions](https://github.com/tumblr/pytumblr#create-a-client) for pytumblr to get your API credentials.

You may want to use Tumblr's queue and scheduler to post your images. In this case, be sure to set the `state` variable in settings.py to `queue`. Or you may want to set this script to publish posts directly. In that case, the state should be `published`.

If you already have image data and would like to use this component without first scraping a web page, your data should be in the following format:

```
{
    "344": {
        "posted_to_tumblr": false, 
        "image_meta": "Mohammed El-Bakkar and his Oriental Ensemble<br><strong>The Magic Carpet</strong><br>Audio Fidelity, USA, AFLP 1895, LP, 12\", 33 rpm, n.d.", 
        "image_url": "http://arcmusic.org/wp-content/gallery/bellydance/belly_magic_carpet.jpg", 
        "gallery": "Bellydance", 
        "gallery_url": "http://arcmusic.org/galleries/bellydance/"
    }
}
```

And your filename should be `images.json`

Be sure to go through the settings.py file and tailor it to your needs.

When you're ready to test, be sure your post state is set to queue. This way you can easily delete your test posts. After testing, you should edit your images.json file and set any "true" values back to "false."

To run:
```
$ python2.7 post.py
```

The program will ask how many posts to create. Enter a numeral and hit return. You should see "Created photo post for: [url]" messages for each post.

Go to Tumblr and check your queue. Hopefully the images, captions, and tags are correct. If you're planning to use Tumblr's post scheduler, make sure it's set up the way you want it. 

#### Social Media Hub

You may want to send these image posts to other social media channels as well. Tumblr itself can interact with Facebook and Twitter, but for finer control I suggest a third-party service like IFTTT.
