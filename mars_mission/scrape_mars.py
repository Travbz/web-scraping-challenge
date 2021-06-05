import pandas as pd
from bs4 import BeautifulSoup
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
from splinter import Browser
def scrape():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    client.drop_database('mars_db')

    db = client.mars_db
    collection = db.articles

    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    mars_dic = {'title':[],'image_url':[], 'news title':[], 'news article':[], 'featured image url':[]}
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find_all('div',class_='content_title')[1].a.text
    article = soup.find_all('div', class_='article_teaser_body')[0].text
    mars_dic['news title'].append(title)
    mars_dic['news article'].append(article)

    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find('div', class_='header')
    link = image.find('img', class_='headerimage')['src']
    print(link)

    base_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    mars_dic['featured image url'].append(base_url+link)
    print(featured_image_url)

    mars_dic

    space_url = "https://space-facts.com/mars/"
    space_table = pd.read_html(space_url)[0]
    space_table.columns = ['Specs', 'Mars']
    space_table.set_index('Specs', inplace=True)
    mars_table = space_table.to_html('templates/space table.html')
    space_table

    mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='description')

    for name in results:
        title = name.find('h3').text
        mars_dic['title'].append(title)
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.find_all('img')[5]['src']
        base_url = 'https://astrogeology.usgs.gov'
        mars_dic['image_url'].append(base_url + img)
        image_urls.append(mars_dic)
        browser.back()
        
    mars_dic
            
    browser.quit()
return mars_dic