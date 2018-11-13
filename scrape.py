from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_news():
    browser = init_browser()
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    news_dict = {
        "News Title":news_title,
        "News Content":news_p
    }

    browser.quit()
    return news_dict


def scrape_img():
    browser = init_browser()
    
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    
    html_img = browser.html
    soup_img = bs(html_img, 'html.parser')
    
    url_part2 = soup_img.find('div', class_='carousel_items').find('article')['style']
    
    url_part2_text = url_part2.split("'")
    url_2 = url_part2_text[1]
    url_part1_text = 'https://www.jpl.nasa.gov'
    featured_image_url = url_part1_text + url_2
    
    featured_img_dict = {
        "url": featured_image_url
    }
    browser.quit()
    
    return featured_img_dict

def scrape_weather():
    browser = init_browser()
    
    url_tweet = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_tweet)
    
    
    html_tweet = browser.html
    soup_tweet = bs(html_tweet, 'html.parser')
    
    mars_weather = soup_tweet.find('p', class_='TweetTextSize').text
    
    weather_dict = {
        "weather":mars_weather
    }
    
    browser.quit()
    
    return weather_dict

def scrape_facts():
    browser = init_browser()
    
    url_facts = 'http://space-facts.com/mars/'
    
    table = pd.read_html(url_facts)
    df = table[0]
    df = df.rename(columns={0: "Info", 1:"Value"})
    table_dicts= []

    for index, row in df.iterrows():
        table_data ={'key': row["Info"],'value': row["Value"]}
        table_dicts.append(table_data)

    html_table = df.to_html()
    html_table.replace('\n', '')
    
    html_table = df.to_html('table.html')
    
    browser.quit()
    
    return table_dicts

def scrape_hemispheres():
    browser = init_browser()
    
    url_hem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hem)
    
    html_hem = browser.html
    soup_hem = bs(html_hem, 'html.parser')
    
    section_links = soup_hem.find('div', class_='collapsible')
    list_links = section_links.find_all('div', class_='description')
    
    url_list = []
    hemisphere_image_urls = []
    
    for link in list_links:
        main_url = 'https://astrogeology.usgs.gov'
        url_part2 = link.find('a')['href']
        final_url = main_url + url_part2
        url_list.append(final_url)
    
    for url in url_list:
        page_url = url
        browser.visit(page_url)
        html_imgs = browser.html
        soup_ind_image = bs(html_imgs, 'html.parser')
        title = soup_ind_image.find('h2', class_='title').text
        img_on_page = soup_ind_image.find('div', class_='downloads')
        img_url_final = img_on_page.find('a')['href']
        hem_dict = {'title': title, 'img_url':img_url_final}
        hemisphere_image_urls.append(hem_dict)
    
    browser.quit()
    
    return hemisphere_image_urls

    
    
    
    
    
    
    
    