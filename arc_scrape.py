### ARC IMAGE OF THE DAY
### Scrape the ARC gallery pages for images and image metadata, write to json (then create Tumblr posts -- TO DO)

from bs4 import BeautifulSoup
import requests, json, codecs, read_write

#Go to the main gallery page to get a list of gallery URLs
gallery_main_url = 'http://arcmusic.org/galleries'
arc_gallery_main = requests.get(gallery_main_url)

#check if we get an error code
if arc_gallery_main.status_code !=200:
	print ('There was an error with: ', url)

#get the text
gallery_main_html = arc_gallery_main.text

#parse it
soup = BeautifulSoup(gallery_main_html)

#get the gallery urls
gallery_list = soup.find('div', attrs = {'class': 'gallery-links'})
gallery_links = gallery_list.find_all('a')

#set up a list for urls
gallery_urls = []

#put the urls in the list
for gallery_link in gallery_links:

	gallery_url = gallery_link['href']
	gallery_urls.append(gallery_url)

print('We have a list of gallery URLs!')
print(gallery_urls)

###################################

#open the json file for reading and load to dict
arc_images = read_write.read('arc_image_of_the_day')

###################################

#here we start looking at each page
for url in gallery_urls:

	#get the page
	arc_gallery = requests.get(url)

	#check if we get an error code
	if arc_gallery.status_code !=200:
		print ('There was an error with: ', url)

	#get the text of the page
	gallery_html = arc_gallery.text

	#parse it with BeautifulSoup
	soup = BeautifulSoup(gallery_html)

	#get the gallery title
	gallery_title_span = soup.find('span', attrs = {'class': 'current'})
	gallery_title = gallery_title_span.text

	#find all the divs with class ngg-gallery-thumbnail
	all_thumbs = soup.find_all('div', attrs = {'class': 'ngg-gallery-thumbnail'})

	#loop through the thumbs
	for a_thumb in all_thumbs:

		#empty sub-dict
		arc_image = {}

		#get the link in the thumbnail div
		image_link = a_thumb.find('a')

		#get the url and the title info
		image_url = image_link['href']
		image_meta = image_link['title'].replace('12 - inch', '12\"').replace('12\u201d', '12\"').replace('33.3', '33')
		image_id = image_link['data-image-id']

		#write to the sub-dict
		arc_image['image_url'] = image_url
		arc_image['image_meta'] = image_meta
		arc_image['gallery'] = gallery_title
		arc_image['gallery_url'] = url
		arc_image['posted_to_tumblr'] = False

		#write sub-dict to the main dict with id as key
		#if the image is not already in our dictionary, let's add it
		if image_id not in arc_images:
			arc_images[image_id] = arc_image

		#if the image IS already in our dictionary, but hasn't been posted to social media yet, let's update the info in case something changed
		if image_id in arc_images and arc_images[image_id]['posted_to_tumblr'] == False:
			arc_images[image_id] = arc_image

	print('We now have images from', gallery_title)

#write it to json
with codecs.open('arc_image_of_the_day.json', 'w', encoding='utf-8') as arc_json:
	arc_dump = json.dumps(arc_images, indent=4)
	arc_json.write(arc_dump)

print('We just dumped', len(arc_images), 'images to arc_image_of_the_day.json')



