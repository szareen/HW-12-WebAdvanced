from splinter import Browser
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests as req
import re


def init_browser():
    # exec_path = {'executable_path': '/usr/local/bin/chromedriver'}
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_collection = {}

    url1 = 'https://mars.nasa.gov/news/'
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url3 = 'https://twitter.com/marswxreport?lang=en'
    url4 = 'http://space-facts.com/mars/'
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find("div", class_="list_text")
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_="article_teaser_body").text

    mars_collection['news_title'] = news_title
    mars_collection['news_p'] = news_p

    browser = init_browser()
    browser.visit(url2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://jpl.nasa.gov"+image

    mars_collection['featured_image_url'] = featured_image_url

    browser = init_browser()
    browser.visit(url3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    tweet = soup.find("div", class_="content")
    mars_weather = tweet.find("div", class_ ="js-tweet-text-container").text

    mars_collection['mars_weather'] = mars_weather

    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ['Characteristics','Value']
    mars_table=df.set_index("Characteristics")
    marsdata = mars_table.to_html(classes='marsdata')
    marsdata=marsdata.replace('\n', ' ')
    
    mars_collection['marsdata'] = marsdata

    browser = init_browser()
    browser.visit(url5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('h3')
    first = title[0].text
    second = title[1].text
    third = title[2].text
    fourth = title[3].text

    def pull_url(insert):
        img_url = "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/{}_enhanced.tif/full.jpg".format(insert)
        return img_url
    first_img = pull_url(first.split(' ')[0].lower())
    second_img = pull_url(second.split(' ')[0].lower())
    third_img = pull_url(third.split(' ')[0].lower() + "_" + third.split(' ')[1].lower())
    fourth_img = pull_url(fourth.split(' ')[0].lower() + "_" + fourth.split(' ')[1].lower())

    hemisphere_image_urls = [
        {'title': first, 'img_url': first_img},
        {'title': second, 'img_url': second_img},
        {'title': third, 'img_url': third_img},
        {'title': fourth, 'img_url': fourth_img}
    ]

    mars_collection['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_collection