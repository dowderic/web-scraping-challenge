#importing dependencies to scrape Mars Nasa New website
from bs4 import BeautifulSoup as bs
import requests
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser

def init_browser():
	executable_path = {'executable_path': ChromeDriverManager().install()}
	return Browser('chrome', **executable_path, headless=False)


def scrape():

	# URL of Nasa page to be scraped
	url = 'https://mars.nasa.gov/news/'
	#assigning a variable to the data processed by the requests module
	browser.visit(url)
	# response = requests.get(url)
	html=browser.html
	#assigning a variable to the parsed data from Beautiful Soup

	soup = bs(html, 'html.parser')

	sections = soup.find('div', class_='list_text')

	#Scraping and collecting the latest News Title and Paragraph Text. 
	news_titles = sections.find('div', class_='content_title').text
	para_texts = sections.find('div', class_='article_teaser_body').text

	#finding current featured image and collecting it's url
	browser2 = Browser('chrome', **executable_path, headless=False)

	url2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
	browser2.visit(url2)
	html2=browser2.html
	# response2 = requests.get(url2)
	soup2 = bs(html2, 'html.parser')
	findimages = soup2.find('div', class_='thmbgroup')

	featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{findimages.find_all('a')[1]['href']}"

	#using Pandas to scrape the table containing facts about the planet and converting it to an html sring
	import pandas as pd
	url3 = 'https://space-facts.com/mars/'
	tables = pd.read_html(url3)

	#my attempt to scrape the title and image urls from the below website and loading that data into a dictionary

	url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser4 = Browser('chrome', **executable_path, headless=False)

	hemisphere_dictionary=[]

	for row in range(4):
    	browser4.visit(url4)
    	html4=browser4.html
    	soup4 = bs(html4, 'html.parser')    
    	clicklinks = soup4.find('div',class_='description')
    	imagetitle = clicklinks.find('h3')
    	imglink= clicklinks.find('a', ['href'])
    	image_url = f"https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/{imglink}"
    	row_dictionary = {'title': imagetitle.text, 'img_url': image_url}
    	hemisphere_dictionary.append(row_dictionary)
# return one Python dictionary containing all of the scraped data.
   final_dict = {
        "news_title": news_titles,
        "news_p": para_texts,
        "featured_image_url": featured_image_url,
        "fact_table": str(tables),
        "hemisphere_images": image_url
    }


    return final_dict