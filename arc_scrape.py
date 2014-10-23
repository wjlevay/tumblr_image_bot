### ARC IMAGE OF THE DAY
### Scrape the ARC gallery pages for images and image metadata, write to json (then create Tumblr posts -- TO DO)

from bs4 import BeautifulSoup
import requests, json

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



#create an empty main dictionary for the images
arc_images = {}

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
		image_meta = image_link['title']
		image_id = image_link['data-image-id']

		#write to the sub-dict
		arc_image['image_url'] = image_url
		arc_image['image_meta'] = image_meta
		arc_image['gallery'] = gallery_title
		arc_image['posted_to_tumblr'] = 'false'

		#write sub-dict to the main dict with id as key
		#TO DO: we'll want a check here to see if the image is already in the dict, and check the status of the posted_to_tumblr flag

		if image_id not in arc_images:
			arc_images[image_id] = arc_image

	print('We now have images from', gallery_title)

#print the dict
#print(arc_images)

#write it to json
arc_dump = json.dumps(arc_images, indent=4)

#TO DO: need to make this re-writable, only add new images, update posted_to_tumblr status
with open('arc_image_of_the_day.json', 'w') as arc_json:
	arc_json.write(arc_dump)

print('We just dumped everthing to arc_image_of_the_day.json')