from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import requests
import datetime as dt
from time import sleep

def browser_init():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)



def scrape():
    browser=browser_init()

# Headlines
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html=browser.html
    soup=bs(html, 'html.parser')

    results = soup.find_all("div", class_='list_text')
    title_list = []
    news_list = []

    for result in results:
        try:
            titles = result.find_all("div", class_="content_title")
            news = result.find_all("div", class_="article_teaser_body")

            for item in titles:
                title = item.text

            for item in news:
               headline = item.text

            title_list.append(title)
            news_list.append(headline)
            
        except Exception as e:
            print(e)

    title = title_list[0]
    headline = news_list[0]


# Space Images
  
    url="https://spaceimages-mars.com/"
    browser.visit(url) 
    html=browser.html
    soup=bs(html, 'html.parser')
    results=soup.find_all("img", class_='headerimage fade-in')

    for result in results:
        image_src=result['src']
        print (image_src)

        image_src=(f'https://spaceimages-mars.com/{image_src}')        
    
   
 # Mars Facts
   
    url="https://galaxyfacts-mars.com/"
    
    table=pd.read_html(url)  
    df=table[0]     
    df=df.rename(columns={0:'',1:"Mars", 2:"Earth"})
    cols = list(df.columns[[0]])
    df= df.set_index(cols)
    df=df.append(pd.Series(name='Description'))
    df = df.reindex(np.roll(df.index, shift=1))
    df=df.fillna("")
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')
    

    # Hemispheres
 
    import time
    time.sleep(1)

    url="https://www.marshemispheres.com/index.html"
    browser.visit(url)

    photos_url = []
    base_url='https://www.marshemispheres.com/'
    html=browser.html
    soup=bs(html, "html.parser")
    results = soup.find_all("div", attrs={"class" : "item"})

    for result in results:
        link=result.find('a')['href']
        url = base_url + link  
        photos_url.append(url)

    picture_urls = []
    picture_titles=[]
    base_url = "https://www.marshemispheres.com/"

    #Photos
    for i in photos_url:
        browser.visit(i)
        time.sleep(1)
    
        html=browser.html
        soup=bs(html, "html.parser")
   
        results = soup.find("a", href=lambda href: href and href.endswith("jpg"))
        pic_url=results["href"]
        pic_url = base_url + pic_url
        picture_urls.append(pic_url)
    
    #Titles
        
        results=soup.find_all('h2', class_="title")
        for result in results:
            hemi_title=result.text
            #hemi_title=' '.join(hemi_title.split(' ')[:-1])
            picture_titles.append(hemi_title)                
   
    browser.click_link_by_partial_href("index.html")  

    #Hemispheres
    hemispheres_img_urls = [] 
    for x,y in zip(picture_titles, picture_urls):
        dictionary = {"title": x, "img_url":y}   
        hemispheres_img_urls.append(dictionary)

    mars_info={}
    mars_info["title"] = title
    mars_info["headline"] = headline
    mars_info["image"] = image_src
    mars_info["picture_urls"] = picture_urls
    mars_info["picture_titles"] = picture_titles
    mars_info["hemispheres"] = hemispheres_img_urls
   
    browser.quit()
    return mars_info

