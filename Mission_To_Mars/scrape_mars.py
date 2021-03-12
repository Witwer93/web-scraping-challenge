
#DEPENDENCIES
import pandas as pd
import pandas_read_xml as pdx
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

url = "https://mars.nasa.gov/news/?page=0&per_page=10&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

def scrape():
    # Retrieve page with the requests module
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title = get_news_title(browser)
    news_p = get_news_paragraph(browser)
    featured_image = get_featured_image(browser)
    mars_facts = find_facts()
    hemispheres = make_hemi_dict(browser)
    
    data = {
        "news_title" : news_title,
        "news_paragraph" : news_p,
        "featured_image" : featured_image,
        "facts" : mars_facts,
        "hemispheres" : hemispheres    
    }
    
    browser.quit()
    return data

# In[4]:

def get_news_title(browser):

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    news_date = soup.find('div', class_='list_date').text == 'December  8, 2020'
    news_date

    mars_news = soup.find('ul', class_='item_list')
    news_title = mars_news.find('div', class_='content_title').text
    
    return news_title

def get_news_paragraph(browser):
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    mars_news = soup.find('ul', class_='item_list')
    news_p = mars_news.find('div', class_='article_teaser_body').text
    
    return news_p

def get_featured_image(browser):
    
    #visit mars images url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #find full image and use splinter to click
    full_image = browser.find_by_id('full_image')
    full_image.click()
    
    #find more info
    browser.is_element_present_by_text('more info')
    more_info = browser.links.find_by_partial_text('more info')
    more_info.click()
    
    #get new hmtl and soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #pull image href
    main_image = soup.find('img', class_='main_image')['src']

    #https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA19324_hires.jpg
    #construct full link
    url = f"https://www.jpl.nasa.gov{main_image}"
    
    return main_image_url

def find_facts():
    
    #use read_html to build dataframe
    url = 'https://space-facts.com/mars/'
    mars_facts_df = pd.read_html(url)[0]
    mars_facts_df.columns=['Description', 'Facts']
    mars_facts_df.set_index('Description', inplace = True)
    #mars_facts_df.head()
    
    #convert using to_html and specify html table
    table_string = mars_facts_df.to_html(classes = "table table-striped")

    return table_string
def make_hemi_dict(browser)
    #construct hemisphere dictionary
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    #get hmtl and soup
    browser.visit(url)    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #make a list to pull hrefs into
    href_list = []
    
    #loop through all 'itemLink product-item' elements and pull href
    for i in soup.find_all('a', class_= 'itemLink product-item'):
        
        #print(i['href'])
        href_list.append(i['href'])
    
    #remove duplicate hrefs
    clean_href_list = []
    [clean_href_list.append(x) for x in href_list if x not in clean_href_list]

    #prepare to construct full urls using clean_href_list plus base_url
    base_url = 'https://astrogeology.usgs.gov/'
    
    #container for the dictionary
    hemisphere_image_urls = []
    
    #run for each hemisphere, create dictionary for each, append to container
    for i in range(4):
        
        #visiting each hemsiphere page
        browser.visit(base_url + test_set[i])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        
        #retrieve title
        name = soup.find('title').text
        
        #split the text to get the part we want
        name = name.split("Enhanced")
        title = name[0]
        #print(title)
        
        #container for next for loops' element
        the_url = ""
        
        #retrieve the url for the image
        for xyz in soup.find_all('div', class_='downloads'):
            #not the most eficient way to scrape this but it works
            element = xyz.find('a')
            the_url = element['href']
            #print(the_url)

        #create the dictionary
        the_dict = {"Title": title, "img_url" : the_url}
        #add it to the list
        hemisphere_image_urls.append(the_dict)

    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape())
