import json
import requests
import urllib3
from bs4 import BeautifulSoup
import os
from scoop_category import get_category


urllib3.disable_warnings()




script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data.txt")






#get the number of subpages in this category
def page_number(soup):
    pagination = soup.find('div', {'class':'pagination'})
    if pagination:
        page_links = pagination.find_all('a')
        return int(page_links[-2].text)
    else: return 1




#get the products of subpages
def get_product(value,page):
    page_url = f'{value}/page-{page}'
    page_response = requests.get(page_url,verify=False)
    page_soup = BeautifulSoup(page_response.content, 'lxml')
    return page_soup.find_all('li', {'class': 'ajax_block_product'})




def main_scoop():
    data_list=[]
    dict=get_category()
    for key, value in dict.items():
        response = requests.get(value, verify=False)
        soup = BeautifulSoup(response.content, 'lxml')
        for page in range(1, page_number(soup)+1):
            for product in get_product(value,page):
                name = product.find('h5').text.strip()
                link = product.find('a')['href']
                price = product.find('span', {'class': 'price'}).text.strip()
                image_link = product.find('img').text.strip()
                ref= product.find('span', {'class': 'ref-listeprod'}).text.strip()
                description = product.find("p",{"class":"product-desc"}).text.strip()
                data = {"categorie": key,"link": link,"name": name,"price": price,"image": image_link,"ref": ref,"description": description}
                if data not in data_list:
                    data_list.append(data)
    with open('data.json', 'w') as f:
        json.dump(data_list, f)