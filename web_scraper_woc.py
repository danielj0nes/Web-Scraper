#!usr/bin/python3
#Daniel Jones
#import sqlite3 #Possible sqlite3 conversion
import json
from bs4 import BeautifulSoup
import requests
import numpy
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
	images = []
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
	for image in cusuContent.findAll('span',{'class':'msl_event_image'}):
		images.append("https://www.cusu.org"+image.img['src']) #Image links
	for i in range(len(events)):
		edata.append(events[i])
		edata.append(times[i])
		edata.append(locations[i])
		edata.append(descriptions[i])
		edata.append(images[i])
	x = numpy.array_split(numpy.array(edata),len(events))
	return x
def get_university_news():
	"""Returns a string of posts with links and dates from the CUMoodle 'University News' section"""
	response = requests.get('https://cumoodle.coventry.ac.uk')
	moodleContent = BeautifulSoup(response.content, 'html.parser')
	postLinks =[]
	headings = []
	dates = []
	data = ""
	for title in moodleContent.findAll('div',{'class':'subject'}):
		headings.append(title.text+"</a>")
	for link in moodleContent.findAll('div',{'class':'link'}):
		postLinks.append("<a href = '"+link.a['href']+"'>") #Post links
	for date in moodleContent.findAll('div',{'class':'author'}):
		dates.append(""+date.text[18:]+"<br/>")
	results = zip(postLinks, headings, dates)
	for result in results:
		data+=(''.join(result))
	print(data)
	return data
if __name__ == '__main__':
	#Example usage
	bbcStory = get_top_story_bbc()
	cusuUpdate = get_updates_cusu()
	moodleUpdate = get_university_news()
	#print(moodleUpdate)
	bbcStoryToWeb = ' - '.join(list(bbcStory))
	"""with open('data.json', 'w') as fp:
					json.dump(bbcStory, fp, indent=4) 							#json incorporation
					for i in range(len(cusuUpdate)):
						json.dump(cusuUpdate[i].tolist(), fp, indent=4)
					json.dump(moodleUpdate, fp, indent=4)"""
			
	webpage = '''<!DOCTYPE HTML>
<html>
	<head>
		<title>What's On Coventry</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<meta name="description" content="" />
		<meta name="keywords" content="" />
		<link rel="stylesheet" href="assets/css/main.css" />
	</head>
    <body class="is-preload">

        <!-- Header -->
        <header id="header">
            <a class="logo" href="index.html">What's On Coventry</a>
            <nav>
                <a href="#menu">Menu</a>
            </nav>
        </header>

        <!-- Nav -->
        <nav id="menu">
            <ul class="links">
                <li><a href="index.html">Home</a></li>
                <li><a href="elements.html">Elements</a></li>
                <li><a href="visit.html">Visit</a></li>
                <li><a href="webscraper.html">Latest news</a></li>
            </ul>
        </nav>

        <!-- Heading -->
        <div id="heading">
            <h1 style="font-weight:bold;">Latest news</h1>
        </div>
		

        <!-- Main -->
        <section id="main" class="wrapper">
            <div class="inner">
                <div class="content">
                    <header>
                        <h2 style="font-size:300%; text-align:center; font-style:bolder; font-weight:bolder;">Coventry's Latest News and Events</h2>
                        <h4 style="font-size:125%; text-align:center; font-style:bolder; font-weight:bolder;">A collaboration of useful news specific to Coventry and Warwickshire</h4>
						<hr>
                    </header>
					<h6 style="font-size:200%; text-align:left; font-weight:bold;" > BBC Coventry & Warwickshire Top Story</h6>
                     <p style="font-size:120%;">{bbcTop}</p>
                    	<hr />
                    	
                    <h6 style="font-size:200%; text-align:left; font-weight:bold;" >Student Union News</h6>
                  		
                     <p style="font-size:120%;">placeholder</p>
						<hr />
					<h6 style="font-size:200%; text-align:left; font-weight:bold;" >Coventry University News</h6>
                  		
                     <p style="font-size:120%;">{moodleUpdate}</p><br /><br />
                     
                     
						<hr />
					<p>This page is powered by a Python script written and developed by Daniel Jones</p>
                </div>
                
            </div>
        </section>

        <footer id="footer">
            <div class="inner">
                <div class="content">
                    <section>
                        <h3>About the project</h3>
                        <p>What's on Coventry is a project brought to you by Daniel Jones, Adam Smith, Jennifer Wan, Ricards Veveris, Thomas Walczak, Ross Woolfenden, Razcan Danciulescu and Ridvan Karaman. We aim to bring you a fast, convenient, and effective way of getting the most recent and accurate information about the city and university of Coventry</p>
                    </section>

                    <section>
                        <h4>Social media</h4>
                        <ul class="plain">
                            <li><a href="https://twitter.com/WhatOnCoventry"><i class="icon fa-twitter">&nbsp;</i>Twitter</a></li>
                            <li><a href="https://www.facebook.com/Whats-On-Coventry-1960577907395132"><i class="icon fa-facebook">&nbsp;</i>Facebook</a></li>
                            <li><a href="#"><i class="icon fa-instagram">&nbsp;</i>Instagram</a></li>
                            <li><a href="https://www.youtube.com/watch?v=WagR3jaBW34"><i class="icon fa-youtube">&nbsp;</i>YouTube</a></li>
                        </ul>
                    </section>
                </div>
                <div class="copyright">
                    &copy; Coventry University
                </div>
            </div>
        </footer>

        <!-- Scripts -->
        <script src="assets/js/jquery.min.js"></script>
        <script src="assets/js/browser.min.js"></script>
        <script src="assets/js/breakpoints.min.js"></script>
        <script src="assets/js/util.js"></script>
        <script src="assets/js/main.js"></script>
		<script type="text/javascript">function add_chatinline(){{var hccid=72962215;var nt=document.createElement("script");nt.async=true;nt.src="https://mylivechat.com/chatinline.aspx?hccid="+hccid;var ct=document.getElementsByTagName("script")[0];ct.parentNode.insertBefore(nt,ct);}}
add_chatinline(); </script>

    </body>
</html>
			'''.format(bbcTop=bbcStoryToWeb, moodleUpdate=moodleUpdate)		
	with open('webscraper.html', 'w') as htmlPage:
		htmlPage.write(webpage)				
	htmlPage.close()
	"""conn = sqlite3.connect('webscraper.db') #Sql test
				sql = conn.cursor()
				sql.execute("INSERT INTO BBCTopStory (Article) VALUES (?)",[bbcStory])			#SQL incorporation
				conn.commit()
				sql.close()
				conn.close"""
