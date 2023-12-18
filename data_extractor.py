#Script 2: Scraping all article data from thestandard.co
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
import csv


# Web driver options
my_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(f"--user-agent={my_user_agent}")
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')

# Initialize the Chrome WebDriver with some options (Sometime when Driver get the url it will have issue about handshake fail So we ignore certificate errors)
driver = webdriver.Chrome(options=chrome_options)

count = 0

with open('items.txt', 'r') as file:
    for link in file:
        

        # Scrape the data
        # Example url: https://thestandard.co/mfp-guidelines-for-educational-development/
        url = f'{link.strip()}'

        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        mockup = []

        # Get the title
        title = soup.find('h1', class_='title').text.strip()
        mockup.append(title)

        # Get the category
        category = soup.find('span', class_='category')
        category = [cat.text.strip() for cat in category.find_all('a')] 
        mockup.append(category)


        # Get the meta author
        author = soup.find('div', class_='meta-author').text.strip().split('\n')[1]
        mockup.append(author)

        # Get the meta date
        date = soup.find('div', class_='meta-date').text.strip()
        mockup.append(date)

        # Get the entry-view
        # Example element: <span class="entry-view" data-content-id="875240" data-content-slug="vertu-returns-to-thailand" data-views="94" title="94 views"><div><i class="fa fa-eye"></i></div><span>94</span></span>
        # Get data-views
        entry_view = soup.find('span', class_='entry-view')['data-views']
        mockup.append(entry_view)

        # Get the entry-content
        # Replace \n\xa0\n with double space
        content = soup.find('div', class_='entry-content').text.strip()
        content = soup.find('div', class_='entry-content')
        # merge all content in list to string
        content = ' '.join([c.text.strip() for c in content])

        mockup.append(content.strip())

        # Get the entry-tags
        tags = soup.find('div', class_='entry-tag')
        # Data you will get from tags : 
        # Example : 
        # <div class="entry-tag" style="border:none">
        # <h4 class="title">TAGS:  </h4>
        # <div class="tags">
        # <a href="https://thestandard.co/tag/%e0%b8%aa%e0%b8%a1%e0%b8%b2%e0%b8%a3%e0%b9%8c%e0%b8%97%e0%b9%82%e0%b8%9f%e0%b8%99/" rel="tag">สมาร์ทโฟน</a><a href="https://thestandard.co/tag/luxury/" rel="tag">Luxury</a><a href="https://thestandard.
        # co/tag/vertu-%e0%b9%80%e0%b8%a7%e0%b8%ad%e0%b8%a3%e0%b9%8c%e0%b8%97%e0%b8%b9/" rel="tag">VERTU (เวอร์ทู)</a><a href="https://thestandard.co/tag/%e0%b9%82%e0%b8%97%e0%b8%a3%e0%b8%a8%e0%b8%b1%e0%b8%9e%e0%b8%97%e0%b9%8c%e0%b8%a1%e0%b8%b7%e0
        # %b8%ad%e0%b8%96%e0%b8%b7%e0%b8%ad/" rel="tag">โทรศัพท์มือถือ</a> </div>
        # </div>
        # need only text from a tag
        tags = [tag.text.strip() for tag in tags.find_all('a')]
        mockup.append(tags)

        def append_to_csv(data, filename='scraped_data.csv', mode='a'):
            with open(filename, mode, newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(data)

        append_to_csv(mockup)
        count += 1
        print(f"{count} articles passed")

print(f"Total {count} articles")