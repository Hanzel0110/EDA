#Script 1: Scraping all article urls from thestandard.co
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd

# Save the data to a file
def append_to_file(item_list):
    with open('items.txt', 'a') as file:
        for item in item_list:
            # Check if item is a list and convert to string with brackets
            if isinstance(item, list):
                item = str(item)
            file.write(item + "\n")

my_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument(f"--user-agent={my_user_agent}")
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')


# Initialize the Chrome WebDriver with some options (Sometime when Driver get the url it will have issue about handshake fail So we ignore certificate errors)
driver = webdriver.Chrome(options=chrome_options)
base_url = 'https://thestandard.co/category/news/'
categories = ['politics', 'business', 'thailand', 'world', 'tech', 'sport', 'environment', 'lgbtqia', 'science', 'china', 'on-this-day']
category = categories[int(input(f"politics : 0\nbusiness : 1\nthailand : 2\nworld : 3\ntech : 4\nsport : 5\nenvironment : 6\nlgbtqia : 7\nscience : 8\nchina : 9\non-this-day : 10\n"))]

# Get the total number of pages for the category
driver.get(f'{base_url}{category}/')
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
pages_info = soup.find('span', class_='pages')
total_pages = int(pages_info.text.split(' ')[-1].replace(',',''))

select_pages = int(input(f'How many pages you want to scraping?\n- 0 : All pages({total_pages})\n- 1 : Custom number\n'))
if select_pages == 0:
    selected_pages = total_pages
elif select_pages == 1:
    selected_pages = int(input('Input number pages : '))

# news_url = []
for page_number in range(1, selected_pages + 1): # for page_number in range(1, total_pages + 1):
    driver.get(f'{base_url}{category}/page/{page_number}/')
    time.sleep(3)
    page_soup = BeautifulSoup(driver.page_source, 'html.parser')

    news_items = page_soup.find_all('div', class_='news-item')
    article_urls = [item.find('a')['href'] for item in news_items if item.find('a')]
    del article_urls[-5:]
    # news_url.append(article_urls)
    append_to_file(article_urls)
    



driver.quit()