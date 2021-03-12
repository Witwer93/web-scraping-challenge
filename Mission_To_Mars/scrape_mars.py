#!/usr/bin/env python
# coding: utf-8

# In[1]:


#DEPENDENCIES
import pandas as pd
import pandas_read_xml as pdx
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


url = "https://mars.nasa.gov/news/?page=0&per_page=10&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"


# In[4]:

#def scrape()
# Retrieve page with the requests module
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#data = {}
#browser.quit()
#return data
# In[4]:

#def get_news(browser)
#url = 'https://mars.nasa.gov/news/'
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[18]:


news_date = soup.find('div', class_='list_date').text == 'December  8, 2020'
news_date


# In[19]:





# In[21]:


mars_news = soup.find('ul', class_='item_list')
news_title = mars_news.find('div', class_='content_title').text
news_title


# In[23]:


news_p = mars_news.find('div', class_='article_teaser_body').text
news_p

#return news_title, news_p
# In[25]:

#def get_featured_image(browser)
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[26]:


full_image = browser.find_by_id('full_image')
full_image.click()


# In[27]:


browser.is_element_present_by_text('more info')
more_info = browser.links.find_by_partial_text('more info')
more_info.click()


# In[32]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')
main_image = soup.find('img', class_='main_image')['src']
main_image
#https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA19324_hires.jpg
url = f"https://www.jpl.nasa.gov{main_image}"
print(url)
#return main_image_url

# In[159]:

#def find_facts()
url = 'https://space-facts.com/mars/'
mars_facts_df = pd.read_html(url)[0]
mars_facts_df.columns=['Description', 'Facts']
mars_facts_df.set_index('Description', inplace = True)
mars_facts_df.head()


# In[162]:


table_string = mars_facts_df.to_html(classes = "table table-striped")

#return table_string
# In[145]:

#def make_hemi_dict(browser)
#construct hemisphere dictionary
url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[72]:


href_list = []
for i in soup.find_all('a', class_= 'itemLink product-item'):
    print(i['href'])
    href_list.append(i['href'])


# In[73]:


test_set = []
[test_set.append(x) for x in href_list if x not in test_set]
test_set


# In[157]:


base_url = 'https://astrogeology.usgs.gov/'
hemisphere_image_urls = []
for i in range(4):
    browser.visit(base_url + test_set[i])
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #retrieve title
    name = soup.find('title').text
    print("\n" + name + "\n/////\n")
    name = name.split("Enhanced")
    title = name[0]
    print(title)
    
    the_url = ""
    
    #retrieve the url for the image
    for xyz in soup.find_all('div', class_='downloads'):
        element = xyz.find('a')
        the_url = element['href']
        print(the_url)
    
    #create the dictionary
    the_dict = {"Title": title, "img_url" : the_url}
    #add it to the list
    hemisphere_image_urls.append(the_dict)
    
hemisphere_image_urls

#return hemisphere_image_urls

#if __name__ == "__main__":
    #print(scrape)
# In[155]:


names = soup.find('title').text
#names = names.split("|")
names = names.split("Enhanced")
print(names[0])
name = names[0]
print(name)


# In[133]:


for xyz in soup.find_all('div', class_='downloads'):
    fts = xyz.find('a')
    print(fts['href'])


# In[149]:





# In[ ]:




