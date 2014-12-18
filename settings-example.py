#######################################
# Tumblr Image Bot Configuration File #
#######################################

######## Web scraping settings ########

# This is the starting point. It might be the first gallery page, first image page, gallery landing page, etc.
base_url = 'http://example.com/gallery'

# Is there a section or page of the site that contains a list of all the gallery pages you want to scrape?
gallery_link_list = True 	#True or False

# If you would rather specify your own list of gallery urls, copy them below like so:
#gallery_urls = ['http://example.com/gallery1', 'http://example.com/gallery2', 'http://example.com/gallery3']
gallery_urls = []

# Enter name of galleries you wish to exclude from being scraped, like so:
#exclusions = ['http://galleryurl1', 'http://galleryurl2']
scrape_exclusions = ['http://example.com/gallery/5/']

# If so, provide some information about the container of these links, perhaps a <div>, <table> or <span>
# The scraper will create a list of gallery urls from these links
gallery_link_info = {
	'id': 'enhancedtextwidget-27',
	#'class': '',
	#'title': '',
	#'text': ''
}

# If the site uses "next" and "previous" links, enter some information about the "next" link
next_link_info = {
	#'id': '',
	#'class': '',
	#'title': '',
	#'text': ''
}

# Image info
# Where is your image meta info? Title or alt attributes? Maybe in a caption?
image_meta = 'title'


######## Tumblr settings ########

# Your tumblr username
username = 'tumblruser'

# Your Tumblr consumer key and secret, and OAuth token and secret
consumer_key = ''
consumer_secret = ''
oauth_token = ''
oauth_secret = ''

# The state of your photo posts (published, draft, queue, or private)
# NOTE: The Tumblr queue can accommodate a maximum of 300 posts
state = 'queue'

# Random images?
# i.e., should images be plucked from the list at random for posting? Or should they be processed in order?
random_image = True

# List of gallery titles or urls you wish to exclude from social media posting
post_exclusions = ['http://example.com/gallery/8/']

# Build your caption
# What should we include in the Tumblr photo post caption?
caption_meta = True			# The image_meta text
caption_meta_after = '<br>'	# What text or html should come after this?
caption_gallery = False		# The gallery title
caption_gallery_after = ''	# What text or html should come after this?

# Should we append a "more" link to the caption? e.g., "more like this: [url]"
more = True
# "More" link text - specify the text for this link
more_text = 'more like this'
more_text_after = ': '
# "More" link url - By default, the url after the more link will go to the "gallery_url" from the json file. 
# But you can specify a different url here
more_url = ''

# Assign tags to posts
# Should the gallery title be used as a tag?
gallery_as_tag = True

# List of universal tags for all posts
universal_tags = []

# Specific tags by gallery title or url
tags_by_gallery = {
	'US Presidents': ['POTUS', 'prez'],
	'http://example.com/gallery/dogs': ['pets', 'puppies'],
}

# Specific tags by meta text
tags_by_meta = {
	'33 rpm': ['vinyl'],
	'45 rpm': ['vinyl']
}