### ARC IMAGE OF THE DAY
### (Scrape the ARC gallery pages for images and image metadata, write to json) then create Tumblr posts!
### To be merged with arc_scrape.py?

import json, secret, codecs, pytumblr

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    secret.consumer_key,
    secret.consumer_secret,
    secret.oauth_token,
    secret.oauth_secret,
)

#load the json file
with codecs.open('arc_image_of_the_day.json', 'r+', encoding='utf-8') as arc_json:
	arc_images = json.load(arc_json)

	#set the count
	count = 0

	#parse the dictionary and assign variables
	for arc_image in arc_images:

		url = arc_images[arc_image]['image_url'].encode('utf-8')
		tag = arc_images[arc_image]['gallery'].encode('utf-8')
		caption = arc_images[arc_image]['image_meta'].encode('utf-8')
		posted = arc_images[arc_image]['posted_to_tumblr']
		gallery_url = arc_images[arc_image]['gallery_url'].encode('utf-8')

		#if we haven't posted this one yet, let's make a post
		if posted == False:

			#Creates a photo post using a source URL
			client.create_photo('arcnyc', state="queue", tags=[tag], source=url, caption=caption, tweet="Image of the Day! File under: "+tag)

			#Give us a status update
			print ('Created image post for: ', url)

			#change 'posted_to_tumblr' flag to true
			arc_images[arc_image]['posted_to_tumblr'] = True

			#increase the count
			count += 1

		#check the count within the for loop. If we hit our limit, break out of the loop.
		if count == 3:
			print 'We hit our limit'
			break

	print('We have,' count, 'posts heading to the Tumblr queue!')

	#write the updated dictionary to json
	arc_dump = json.dumps(arc_images, indent=4)
	arc_json.write(arc_dump)

