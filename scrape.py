### Image Scraper

from bs4 import BeautifulSoup
import requests, json, codecs, read_write

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
base_url = ConfigSectionMap('Scrape')['base_url']

# Go to the main gallery page to get a list of gallery URLs
main_page = requests.get(base_url)

# check if we get an error code
if main_page.status_code !=200:
	print ('There was an error with: ', base_url)

# get the text
main_page_html = main_page.text

# parse it
soup = BeautifulSoup(main_page_html)

##############
# keep going with abstraction/config file

# get the gallery urls
gallery_list = soup.find('div', attrs = {'class': 'gallery-links'})
gallery_links = gallery_list.find_all('a')

# set up a list for urls
gallery_urls = []

# put the urls in the list
for gallery_link in gallery_links:

	gallery_url = gallery_link['href']
	gallery_urls.append(gallery_url)

print('We have a list of gallery URLs!')
print(gallery_urls)

###################################

# open the json file for reading and load to dict
images = read_write.read('images')

###################################

# here we start looking at each page
for url in gallery_urls:

	# get the page
	arc_gallery = requests.get(url)

	# check if we get an error code
	if arc_gallery.status_code !=200:
		print ('There was an error with: ', url)

	# get the text of the page
	gallery_html = arc_gallery.text

	# parse it with BeautifulSoup
	soup = BeautifulSoup(gallery_html)

	# get the gallery title
	gallery_title_span = soup.find('span', attrs = {'class': 'current'})
	gallery_title = gallery_title_span.text

	# find all the divs with class ngg-gallery-thumbnail
	all_thumbs = soup.find_all('div', attrs = {'class': 'ngg-gallery-thumbnail'})

	# loop through the thumbs
	for a_thumb in all_thumbs:

		# empty sub-dict
		arc_image = {}

		# get the link in the thumbnail div
		image_link = a_thumb.find('a')

		# get the url and the title info
		image_url = image_link['href']
		image_meta = image_link['title'].replace('12 - inch', '12\"').replace('12\u201d', '12\"').replace('33.3', '33')
		image_id = image_link['data-image-id']

		# write to the sub-dict
		image['image_url'] = image_url
		image['image_meta'] = image_meta
		image['gallery'] = gallery_title
		image['gallery_url'] = url
		image['posted_to_tumblr'] = False

		# write sub-dict to the main dict with id as key
		# if the image is not already in our dictionary, let's add it
		if image_id not in images:
			images[image_id] = image

		# if the image IS already in our dictionary, but hasn't been posted to social media yet, let's update the info in case something changed
		if image_id in images and images[image_id]['posted_to_tumblr'] == False:
			images[image_id] = image

	print('We now have images from', gallery_title)

#write it to json
read_write.write('images', images)

print('We just dumped', len(images), 'images to images.json')