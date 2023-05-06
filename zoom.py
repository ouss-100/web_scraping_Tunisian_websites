import json
import requests
from bs4 import BeautifulSoup
import os
from zoom_category import get_category


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data.txt")



def page_number(soup):
    pagination = soup.find('ul', {'class':'pagination'})
    if pagination:
        page_links = pagination.find_all('a')
        return int(page_links[-2].text)
    else: return 1



def get_product(url,page):
    page_url = f"{url}/page-{page}"
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'lxml')
    return page_soup.find_all("div", class_='product-container')


def get_product_content(key,link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find('h1', itemprop="name").text.strip()
    price = soup.find('span', id="our_price_display").text.strip() if soup.find('span', id="our_price_display") else ""
    ref = soup.find('span', {'itemprop': 'sku'}).text.strip() if soup.find('span', {'itemprop': 'sku'}) else ""
    image_link = soup.find('img',{'itemprop':"image"})['src']
    ref=soup.find('span', {"class":"editable"}).text.strip() if soup.find('span', {"class":"editable"}) else ""
    description = soup.find('div',id="short_description_block").text.strip() if soup.find('div',id="short_description_block") else ""
    return {"categorie": key,"link": link,"name": name,"price": price,"image": image_link,"ref": ref,"description": description}




def main_zoom():
    data_list=[]
    dic=get_category()
    for key, value in dic.items():
            response = requests.get(value)
            soup = BeautifulSoup(response.content, 'lxml')
            for page in range(1, page_number(soup)+1):
                for product in get_product(value,page):
                    link = product.find("a", {"class":"product_img_link"})['href']
                    data=get_product_content(key,link)
                    if data not in data_list:
                        data_list.append(data)
    with open('data.json', 'w') as f:
        json.dump(data_list, f)
