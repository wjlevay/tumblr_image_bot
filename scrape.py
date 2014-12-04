### Image Scraper

from bs4 import BeautifulSoup
import requests, json, codecs, read_write, settings

# get some settings
base_url = settings.base_url

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

if settings.gallery_link_list == True:

	gallery_link_info = settings.gallery_link_info

	# get the gallery urls
	gallery_list = soup.find(attrs = gallery_link_info)
	gallery_links = gallery_list.find_all('a')

	# set up a list based on the settings file
	gallery_urls = settings.gallery_urls

	# get any exclusions
	exclusions = settings.scrape_exclusions

	# put the urls in the list
	for gallery_link in gallery_links:

		gallery_url = gallery_link['href']

		if gallery_link['href'] not in exclusions:
			
			gallery_urls.append(gallery_url)

	print('We have a list of URLs!')
	print(gallery_urls)

###################################

# open the json file for reading and load to dict
json_dict = read_write.read('images')

if json_dict:
	images = json_dict
else:
	images = {}

###################################

# here we start looking at each page
for url in gallery_urls:

	# get the page
	gallery = requests.get(url)

	# check if we get an error code
	if gallery.status_code !=200:
		print ('There was an error with: ', url)

	# get the text of the page
	gallery_html = gallery.text

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
		image = {}

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