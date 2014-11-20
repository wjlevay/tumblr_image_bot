### Friendly Neighborhood Tumblr Bot

import json, secret, pytumblr, codecs, random, read_write, ConfigParser

# read the settings file
Config = ConfigParser.ConfigParser()
Config.read('settings.ini')

# set up the helper function for the settings
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

# get some settings
username = ConfigSectionMap('Tumblr')['username']
state = ConfigSectionMap('Tumblr')['state']
exclusions = [ConfigSectionMap('Tumblr')['exclusions']]
more = ConfigSectionMap('Tumblr')['more']

# Authenticate via OAuth
# Get the keys from the secret.py file
client = pytumblr.TumblrRestClient(
    secret.consumer_key,
    secret.consumer_secret,
    secret.oauth_token,
    secret.oauth_secret,
)

# open the json file for reading and load to dict
images = read_write.read('images')

# set the count
count = 0

# ask user how many posts (up to 300)
user_count = input('>> How many images to you want to send to the Tumblr queue? (300 max): ')

# parse the dictionary randomly and assign variables
for image in random.sample(images.keys(), len(images)):

	url = images[image]['image_url'].encode('utf-8')
	caption = images[image]['image_meta'].encode('utf-8')
	gallery_url = images[image]['gallery_url'].encode('utf-8')
	gallery = images[image]['gallery'].encode('utf-8')
	tags = [gallery]
	posted = images[image]['posted_to_tumblr']

	# separate this section out into config file
	# assign the medium as a tag
	if gallery == 'Pop music pulp paperbacks':
		tags.append('books')
		tags.append('book covers')
	elif gallery == '45 adaptors':
		tags.append('objects')
	elif gallery == 'LA punk flyers':
		tags.append('ephemera')
	else:
		tags.append('records')
		tags.append('album covers')

	# what other tags can we add?
	if '33 rpm' in caption or '45 rpm' in caption:
		tags.append('vinyl')

	# Exclude any galleries from posting?
	# if we haven't posted this one yet, let's make a post.
	if gallery not in exclusions and posted == False:

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