import codecs, json

def read(filename):

	dictionary = {}

	with codecs.open(filename+'.json', encoding='utf-8') as filename:
		dictionary = json.load(filename)

	#close the file
	filename.close

	return dictionary

def write(filename, dictionary):

	with codecs.open(filename+'.json', 'w', encoding='utf-8') as filename:

		#write the updated dictionary to json
		dump = json.dumps(dictionary, sort_keys=True, indent=4)
		filename.write(dump)

	#close the file
	filename.close