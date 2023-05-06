import requests
from bs4 import BeautifulSoup




url = 'https://www.zoom.com.tn/695-informatique'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


categories = soup.find('nav', class_='nav-menu')
categories=categories.find_all('li', class_='')



def get_category():
    dictionary={}
    for category in categories:
        name = category.find('a').text.strip()
        link = category.find('a')['href']
        dictionary[name] = link
    return dictionary
