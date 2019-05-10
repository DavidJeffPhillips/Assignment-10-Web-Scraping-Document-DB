from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd


def scrape():
    mars_dict = {}

    # get_ipython().system('which chromedriver')
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('div', class_='content_title')
    paragraph = soup.find('div', class_='article_teaser_body')

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_id('full_image')
    full_img_page = browser.find_link_by_partial_text('more info')
    full_img_page.click()
    browser.click_link_by_partial_href('/spaceimages/images/largesize/')
    soup = BeautifulSoup(browser.html)
    featured_img_url = soup.find('img')['src']

    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html')
    results = soup.find_all(
        'p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather = results[0].text

    url = 'https://space-facts.com/mars/'
    table_data = pd.read_html(url)
    table_data
    df = table_data[0]
    df.columns = ['Measurement', 'Mars']
    html_table = df.to_html()

    mars_dict['title'] = title
    mars_dict['paragraph'] = paragraph
    mars_dict['featured image'] = featured_img_url
    mars_dict['weather'] = mars_weather
    mars_dict['table'] = html_table

    return mars_dict
