

from bs4 import BeautifulSoup
import requests

#page = requests.get('https://finance.yahoo.com/quote/FNZ.NZ/')
page = requests.get('https://www.nzx.com/instruments/NZG/')

soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())
section = soup.find_all('section', class_='instrument-snapshot')
h1 = soup.find_all('h1')
price = h1[1].text.strip().replace('$', '')
print(float(price))
