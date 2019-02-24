#!usr/bin/python3
#Daniel Jones
from bs4 import BeautifulSoup
import requests
"""Functions to webscrape useful information from relevant target sites"""
def get_top_story_bbc():
	"""Function to get BBC's Coventry and Warwickshire top story. Returns an array of two elements where the first it the top story title and the second the contents"""
	topStory = []
	response = requests.get('https://www.bbc.co.uk/news/england/coventry_and_warwickshire')
	bbcContent = BeautifulSoup(response.content, 'html.parser')
	topStory.append(bbcContent.findAll('span', {'class' : 'title-link__title-text'})[0].text) 
	topStory.append(bbcContent.findAll('p', {'class' : 'skylark__summary'})[0].text)
	return topStory
def get_updates_cusu():
	"""Function to get the CUSU most recent updates and stories. Returns an array where each block of 4 elements are relative"""
	events = []
	times = []
	locations = []
	descriptions = []
	edata = []
	response = requests.get('https://www.cusu.org/coventry')
	cusuContent = BeautifulSoup(response.content, 'html.parser')
	for event in cusuContent.findAll('a',{'class':'msl_event_name'}):
		events.append(event.text) #Titles
	for date in cusuContent.findAll('dd',{'class':'msl_event_time'}):
		times.append(date.text) #Dates
	for location in cusuContent.findAll('dd',{'class':'msl_event_location'}):
		locations.append(location.text) #Locations
	for description in cusuContent.findAll('dd',{'class':'msl_event_description'}):
		descriptions.append(description.text) #Descriptions
	for i in range(len(events)):
		edata.append(events[i])
		edata.append(times[i])
		edata.append(locations[i])
		edata.append(descriptions[i])
	return edata
def get_university_news():
	"""Returns posts with links from the CUMoodle 'University News' section, returns an array where each block of 2 elements are relative"""
	response = requests.get('https://cumoodle.coventry.ac.uk')
	moodleContent = BeautifulSoup(response.content, 'html.parser')
	postLinks =[]
	headings = []
	edata = []
	for link in moodleContent.findAll('div',{'class':'posting shortenedpost'}):
		postLinks.append(link.a['href']) #Post links
	for title in moodleContent.findAll('div',{'class':'subject'}):
		headings.append(title.text) #Post titles
	for i in range(len(headings)):
		edata.append(headings[i])
		edata.append(postLinks[i])
	return edata
if __name__ == '__main__':
	#Example usage
	bbcStory = get_top_story_bbc()
	cusuUpdate = get_updates_cusu()
	moodleUpdate = get_university_news()
	print(bbcStory)
	print("\n")
	print(cusuUpdate)
	print("\n")
	print(moodleUpdate)
