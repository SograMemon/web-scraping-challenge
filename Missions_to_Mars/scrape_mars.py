from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import re
import pandas as pd

def NASA_mars_news():
    try:
        url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
        news_titles=[]
        news_p=[]
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)
        time.sleep(4)
        html = browser.html
        soup = bs(html, 'html.parser')
        results = soup.find_all('div', class_='list_text')

        for result in results:
            title= result.find('div', class_='content_title').text.strip()
            p= result.find('div', class_="article_teaser_body").text.strip()
            news_titles.append(title)
            news_p.append(p)
            #print("--------------------------------------------------------")
            #print(title)
            #print(p)
            #print()
        browser.quit()  
        return (news_titles, news_p)
    except:
        return NASA_mars_news()

def JPL_mars_featured_image():
    try:
        img_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(img_url)
        time.sleep(4)
        browser.find_by_id('full_image', wait_time=1).click()
        browser.find_by_css('[id="fancybox-lock"]')[0].find_by_css('div[class="buttons"] a:nth-child(2)')[0].click()
        time.sleep(1)
        html= browser.html
        soup=bs(html, "lxml")
        result_url=soup.find("img", class_="main_image")["src"]
        featured_image_url="https://www.jpl.nasa.gov"+result_url
        browser.quit()
        return featured_image_url
    except:
        return JPL_mars_featured_image()

def mars_weather():
    try:
        twitter_url="https://twitter.com/marswxreport?lang=en"
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(twitter_url)
        time.sleep(4)
        html= browser.html
        soup=bs(html, "lxml")
        mars_weather =soup.find("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").text
        browser.quit()
        return mars_weather
    except:
        return mars_weather()

def mars_facts():
    try:
        mars_facts_url="https://space-facts.com/mars/"
        df_mars_facts=pd.read_html(mars_facts_url)[0]
        df_mars_facts.rename(columns={0:"attribute", 1:"value"}, inplace=True)
        return df_mars_facts
    except:
        return mars_facts()

def mars_hemispheres():
    try:
        base_url="https://astrogeology.usgs.gov"
        mars_hemispheres_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        hemisphere_image_urls=[]
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(mars_hemispheres_url)
        time.sleep(10)
        html= browser.html
        soup=bs(html, "lxml")
        results= soup.find_all("a", class_="itemLink product-item")
        for result in results:
            browser.visit(base_url+result["href"])
            time.sleep(1)
            html= browser.html
            soup=bs(html, "lxml")
            title=soup.find("h2", class_="title").text.replace(" Enhanced","")
            img=base_url+soup.find("img", class_="wide-image")["src"]
            mars_hemispheres_dictionary= {"title": title,
                                        "title_url": img,}
            hemisphere_image_urls.append(mars_hemispheres_dictionary)
        browser.quit()
        return hemisphere_image_urls
    except:
        return mars_hemispheres()

def scrape():
    NASA_mars_news_titles, NASA_mars_news_p= NASA_mars_news()
    scraped_dictionary={
    "NASA_mars_news_titles": NASA_mars_news_titles,
    "NASA_mars_news_p": NASA_mars_news_p,
    "JPL_mars_featured_image":JPL_mars_featured_image(),
    "mars_weather":mars_weather(),
    "mars_facts":mars_facts().to_html(index=False, classes="mars-table table table-sm text-xsmall table-bordered table-hover table-condensed", header="true"),
    "mars_hemispheres":mars_hemispheres()
    }
    return scraped_dictionary

#print(scrape())

