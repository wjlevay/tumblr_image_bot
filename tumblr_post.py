### ARC IMAGE OF THE DAY
### (Scrape the ARC gallery pages for images and image metadata, write to json) then create Tumblr posts!
### To be merged with arc_scrape.py?

import json, secret, pytumblr, codecs, random, read_write

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    secret.consumer_key,
    secret.consumer_secret,
    secret.oauth_token,
    secret.oauth_secret,
)

#open the json file for reading and load to dict
arc_images = read_write.read('arc_image_of_the_day')

with codecs.open('arc_image_of_the_day.json', encoding='utf-8') as arc_json:
	arc_images = json.load(arc_json)

#close the file
arc_json.close

#set the count
count = 0

#ask user how many posts (up to 300)
user_count = input('>> How many images to you want to send to the Tumblr queue? (300 max): ')

#parse the dictionary randomly and assign variables
for arc_image in random.sample(arc_images.keys(), len(arc_images)):

	url = arc_images[arc_image]['image_url'].encode('utf-8')
	caption = arc_images[arc_image]['image_meta'].encode('utf-8')
	gallery_url = arc_images[arc_image]['gallery_url'].encode('utf-8')
	gallery = arc_images[arc_image]['gallery'].encode('utf-8')
	tags = [gallery]
	posted = arc_images[arc_image]['posted_to_tumblr']

	#assign the medium as a tag
	if gallery == 'Pop music pulp paperbacks':
		tags.append('books')
	elif gallery == '45 adaptors':
		tags.append('objects')
	elif gallery == 'LA punk flyers':
		tags.append('ephemera')
	else:
		tags.append('records')

	#what other tags can we add?
	if '33 rpm' in caption or '45 rpm' in caption:
		tags.append('vinyl')

	#if we haven't posted this one yet, let's make a post. We're excluding "Adopt-a-record" right now.
	if gallery != 'Adopt-a-record' and posted == False:

		#Creates a photo post using a source URL
		client.create_photo('arcnyc', state="queue", tags=tags, source=url, caption=caption+'<br>more like this: '+gallery_url)

		#Give us a status update
		print ('Created image post for: ', url)

		#change 'posted_to_tumblr' flag to true
		arc_images[arc_image]['posted_to_tumblr'] = True

		#increase the count
		count += 1

	#check the count within the for loop. If we hit our limit, break out of the loop.
	if count == user_count:
		print 'We hit our limit'
		break

print ('We have', count, 'posts heading to the Tumblr queue!')

#open the file for writing & dump
read_write.write('arc_image_of_the_day', arc_images)


