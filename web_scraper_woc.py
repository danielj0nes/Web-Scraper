#!usr/bin/python3
#Daniel Jones
from bs4 import BeautifulSoup
import requests
"""BBC Coventry and Warwickshire Scrape"""
def get_top_story_bbc():
	"""Function to get BBC's Coventry and Warwickshire top story. Returns an array of two elements where the first it the top story title and the second the contents"""
	topStory = []
	response = requests.get('https://www.bbc.co.uk/news/england/coventry_and_warwickshire')
	bbcContent = BeautifulSoup(response.content, 'html.parser')
	articleTitles = bbcContent.findAll('span', {'class' : 'title-link__title-text'}) 
	articleContents = bbcContent.findAll('p', {'class' : 'skylark__summary'})
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
def get_university_news():
	"""Returns posts with links from the CUMoodle 'University News' section, returns an array where each block of 2 elements are relative"""
	response = requests.get('https://cumoodle.coventry.ac.uk')
	cuMoodle = BeautifulSoup(response.content, 'html.parser')
	titles = cuMoodle.findAll('div',{'class':'subject'})
	links = cuMoodle.findAll('div',{'class':'posting shortenedpost'})
	headings = []
	postLinks =[]
	edata = []
	for link in links:
		postLinks.append(link.a['href']) #Post links
	for title in titles:
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