#!usr/bin/python3
#Daniel Jones
from bs4 import BeautifulSoup
import requests
"""BBC Coventry and Warwickshire Scrape"""
def get_top_story_bbc():
	"""Function to get BBC's Coventry and Warwickshire top story. Returns an array of two elements; 0th = title, 1st = contents"""
	topStory = []
	response = requests.get('https://www.bbc.co.uk/news/england/coventry_and_warwickshire')
	siteContent = BeautifulSoup(response.content, 'html.parser')
	articleTitles = siteContent.find_all('span', {'class' : 'title-link__title-text'}) #Look for specific title 'span' for article title
	articleContents = siteContent.find_all('p', {'class' : 'skylark__summary'}) #Look for specific summary paragraph for article paragraphs
	topStory.append(articleTitles[0].text) 
	topStory.append(articleContents[0].text)
	return topStory
def get_updates_cusu():
	"""Function to get the CUSU most recent updates and stories. Returns an array where each block of 4 elements are relative"""
	events = []
	times = []
	locations = []
	descriptions = []
	edata = []
	response = requests.get('https://www.cusu.org/coventry')
	cusuC = BeautifulSoup(response.content, 'html.parser')
	eventNames = cusuC.findAll('a',{'class':'msl_event_name'})
	eventDates = cusuC.findAll('dd',{'class':'msl_event_time'})
	eventLocations = cusuC.findAll('dd',{'class':'msl_event_location'})
	eventDescriptions = cusuC.findAll('dd',{'class':'msl_event_description'})
	for event in eventNames:
		events.append(event.text) #Titles
	for date in eventDates:
		times.append(date.text) #Dates
	for location in eventLocations:
		locations.append(location.text) #Locations
	for description in eventDescriptions:
		descriptions.append(description.text) #Descriptions
	for i in range(len(events)):
		edata.append(events[i])
		edata.append(times[i])
		edata.append(locations[i])
		edata.append(descriptions[i])
	return edata
if __name__ == '__main__':
	bbcStory = get_top_story_bbc()
	#print(' - '.join(x))
	cusuUpdate = get_updates_cusu()
	print(bbcStory)
	print(cusuUpdate)