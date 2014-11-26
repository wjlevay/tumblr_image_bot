### Friendly Neighborhood Tumblr Bot

import json, settings, pytumblr, codecs, random, read_write

# get some settings
username = settings.username
state = settings.state
random_image = settings.random_image
exclusions = settings.post_exclusions
more = settings.more

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    settings.consumer_key,
    settings.consumer_secret,
    settings.oauth_token,
    settings.oauth_secret,
)

# open the json file for reading and load to dict
images = read_write.read('images')

# set the count
count = 0

# ask user how many posts (up to 300)
user_count = input('>> How many images to you want to send to Tumblr? (300 max): ')

# Should we parse the dictionary randomly?
if random_image == True:
	sample = random.sample(images.keys(), len(images))
else:
	sample = images

for image in sample:

	# Assign some variables
	url = images[image]['image_url'].encode('utf-8')
	caption = images[image]['image_meta'].encode('utf-8')
	gallery_url = images[image]['gallery_url'].encode('utf-8')
	gallery = images[image]['gallery'].encode('utf-8')
	posted = images[image]['posted_to_tumblr']
	tags = []

	# Assign some tags
	# Append gallery title as a tag
	if settings.gallery_as_tag == True and gallery != '':
		tags.append(gallery)

	# Get tags by gallery title
	tags_by_gallery = settings.tags_by_gallery
	if tags_by_gallery:
		for tbg in tags_by_gallery:
			if tbg == gallery or tbg == gallery_url:
				for a_tag_by_gallery in tags_by_gallery[tbg]:
					tags.append(a_tag_by_gallery)
			else:
				if tags_by_gallery['default']:
					for a_default_tag in tags_by_gallery['default']:
						tags.append(a_default_tag)

	# Append tags by term in caption
	tags_by_caption = settings.tags_by_caption
	if tags_by_caption:
		for tbc in tags_by_caption:
			if tbc in caption:
				for a_tag_by_caption in tags_by_caption[tbc]:
					tags.append(a_tag_by_caption)

	# Append universal tag
	universal_tags = settings.universal_tags
	if universal_tags:
		for t in universal_tags:
			tags.append(t)

	# Exclude any galleries from posting?
	# if we haven't posted this one yet, let's make a post.
	if gallery not in exclusions and posted == False or gallery_url not in exclusions and posted == False:

		#Creates a photo post using a source URL
		client.create_photo(username, state=state, tags=tags, source=url, caption=caption+'<br>'+more+': '+gallery_url)

		#Give us a status update
		print ('Created photo post for: ', url)

		#change 'posted_to_tumblr' flag to true
		images[image]['posted_to_tumblr'] = True

		#increase the count
		count += 1

	#check the count within the for loop. If we hit our limit, break out of the loop.
	if count == user_count:
		print 'We hit our limit'
		break

print ('We have', count, 'posts heading to Tumblr!')

#open the file for writing & dump
read_write.write('images', images)