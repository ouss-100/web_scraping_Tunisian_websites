import json
import requests
from bs4 import BeautifulSoup
import os
import re
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data.txt")






#----get soup function----#
def get_soup(url):  
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')





def get_category():
    soup = get_soup('https://www.mytek.tn/')
    categories = soup.find('ul', class_='vertical-list clearfix')
    categories = categories.find_all('li', class_='category-item')
    dictionary={}
    for category in categories:
        name = category.find('a').text.strip()
        link = category.find('a')['href']
        if re.match(re.compile(r'^(?:http|ftp)s?://'), link):
            dictionary[name] = link
    return dictionary




#get the number of subpages in this category
def page_number(soup):
    pagination = soup.find('ul', {'class':'items pages-items'})
    if pagination:
        last_page_link = pagination.find_all('a')[-2]['href']
        return int(last_page_link.split('=')[-1])
    else: return 1






#get the products of subpages
def get_product(value,page):
    soup = get_soup(value +"?p="+str(page))
    return soup.find_all('li', {'class': 'item product product-item'})







def main_mytek():
    data_list=[]
    dic=get_category()
    for key, value in dic.items():
            soup = get_soup(value)
            for page in range(1, page_number(soup)+1):
                for container in get_product(value,page):
                    name = container.find('a', {'class': 'product-item-link'}).text.strip()
                    link = container.find('a', {'class': 'product-item-link'})['href']
                    price = container.find('div', {'class': 'price-box price-final_price'}).text.strip() if soup.find('div', {'class': 'price-box price-final_price'}) else ""
                    image_link = container.find('img')['src'] 
                    ref=soup.find('div', {"class":"skuDesktop"}).text.strip() if soup.find('div', {"class":"skuDesktop"}) else ""
                    if container.find('p') is not None:description = container.find('p').text.strip() 
                    else:description=""
                    data = {"categorie": key,"link": link,"name": name,"price": price,"image": image_link,"ref": ref,"description": description}
                    if data not in data_list:
                            data_list.append(data)
    with open('data.json', 'w') as f:
        json.dump(data_list, f)