from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd

opts = Options()
opts.add_argument(
	"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
)


search_term = input("What Do You Want to Search:")
num = 1
url = f"https://www.amazon.com/s?k={search_term}"
data=[]

driver = webdriver.Chrome(chrome_options=opts, options=options)
driver.get(url)

time.sleep(5)

soup = BeautifulSoup(driver.page_source,'html.parser')
pages = soup.find('span',class_="s-pagination-strip").find_all('span')
last_page = int(pages[-1].text)


for i in range(1,last_page+1):

	items = soup.find_all('div',class_="a-section a-spacing-base")

	for item in items:
		title = item.find('span',class_="a-size-base-plus a-color-base a-text-normal").text.strip()
		link = 'https://www.amazon.com/'+item.find('a',class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")['href']
		try:

			price = item.find('span',class_="a-price-whole").text+item.find('span',class_="a-price-fraction").text+"$"
		except:
			price = "NA"

		try:
			reviews = item.find('span',class_="a-size-base s-underline-text").text.strip()
		except:
			reviews = "NA"

		data.append({'title':title,'link':link,'price':price,'reviews':reviews})

	print('Scraped Page: '+str(i))
	time.sleep(2)
	driver.quit()

	time.sleep(2)
	driver = webdriver.Chrome(chrome_options=opts)
	driver.get(url+"&page="+str(i+1))
	soup = BeautifulSoup(driver.page_source,'html.parser')

print('Number of products Scraped: '+str(len(data)))
df = pd.DataFrame(data)
df.to_csv('log'+f'{search_term}'+'.csv', index = False, encoding='utf-8')

