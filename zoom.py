import requests
from bs4 import BeautifulSoup
import json


#----get soup function----#
def get_soup(url):  
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')



#----extract menu----#
def extract_menu():
        menu_list=[]
        soup = get_soup("https://zoom.com.tn/")
        menu_element = soup.find('li', class_='mm_menus_li mm_menus_li_tab sub-product mm_sub_align_full mm_has_sub')
        menu_items = menu_element.find_all('div', class_='mm_tab_li_content closed')
        for item in menu_items:
            link = item.find('a')['href']
            menu_list.append(link)
        return menu_list

#----function to extract number of pages----#
def extract_number_of_pages(url):
    soup = get_soup(url)
    pagination = soup.find('ul', {'class':'page-list'})
    if pagination:
        page_links = pagination.find_all('a')
        return int(page_links[-2].text)
    else: return 1


#----function to extract products links exp('https://www.tunisianet.com.tn/702-ordinateur-portable')----#
def extract_products_links(url):
    titles_with_links = []
    soup = get_soup(url)
    items = soup.find_all('div', class_='product-miniature js-product-miniature')

    for item in items:
        title_tag = item.find('h5', class_='product-name')
        if title_tag:
            link = title_tag.a['href']
            titles_with_links.append(link)
    return titles_with_links



#----extract products details----#

def extract_categories(soup):
    breadcrumb = soup.find('ol', class_='breadcrumb')
    breadcrumb_items = []
    for li in breadcrumb.find_all('li', class_='breadcrumb-item'):
        item_text = li.text.strip()
        breadcrumb_items.append(item_text)
    return breadcrumb_items

soup=get_soup('https://zoom.com.tn/informatique/15633-tapis-de-souris-gamer-silent-flight-680-large.html')
print(extract_categories(soup))

def extract_product_images(soup):
    image_links = []
    images_container = soup.find('ul', class_='product-images')
    
    if images_container:
        image_tags = images_container.find_all('img')
        for img in image_tags:
            image_link = img['src']
            image_links.append(image_link)
    
    return image_links


def extract_reference(soup):
    div= soup.find('div', class_='product-reference')
    if div:
            ref= div.find('span', itemprop='sku')
            return ref.text.strip()
    return None


def extract_description(soup):
    product_information_div = soup.find('div', class_='product-information')
    if product_information_div:
        description = product_information_div.find('div', itemprop='description')
        if description:
            return description.text.strip()
    return None

def extract_disponibilite_magasin(soup):
    def get_table(availability_div):
        list_magazine= []
        a= availability_div.find_all('div', class_='store-availability')
        availabilities = [availability.text.strip() for availability in a]

        disponibilite_div = store_div.find('div', string='Disponibilité').parent
        stock_div = disponibilite_div.find_all('div', class_='store-availability')
        stock = [availability.text.strip() for availability in stock_div]
        
        for i, j in zip(availabilities, stock):
            list_magazine.append([i, j])
        
        return list_magazine

    product_information_div = soup.find('div', class_='product-information')

    store_div = product_information_div.find('div', id='product-availability-store')
    store_div2 = product_information_div.find('div', id='product-availability-store-mobile')
    
    if store_div or store_div2:
        availability_div = store_div.find('div', class_='col-lg-6') if store_div else store_div2.find('div', class_='col-lg-6')
        
        if availability_div:
            return get_table(availability_div)

    return []

def extract_image_brand(soup):
    img_src = soup.find('img', class_='manufacturer-logo')['src']
    if img_src:
        return img_src
    return ""

def extract_price(soup):
    price_text = soup.find('span', itemprop='price').text.strip().replace('\xa0', ' ')
    price_int = int(''.join(filter(str.isdigit, price_text)))

    return price_int

def extract_stock(soup):
    stock = soup.find('span', class_='in-stock')
    if stock:
        return stock.text.strip()
    stock = soup.find('span', class_='later-stock')
    if stock:
        return stock.text.strip()
    return stock.text.strip()

def extract_tech_file(soup):
    elements = soup.find('section', class_='product-features')
    data_list = []
    if elements:
        for name, value in zip(soup.find_all(class_='name'), soup.find_all(class_='value')):
            data_list.append({"name": name.get_text(strip=True), "value": value.get_text(strip=True)})

    return data_list

#----------------------------#

#-->function to receive products links and save products details
def extract_content(url):
    products_links= extract_products_links(url)
    for link in products_links:
        soup= get_soup(link)
        data= {
        "Link": link,
        "categories" : extract_categories(soup),
        "product Images": extract_product_images(soup),
        "Reference": extract_reference(soup),
        "Description": extract_description(soup),
        "stock" : extract_stock(soup),
        "Disponibilite_magasin": extract_disponibilite_magasin(soup),
        "Image_brand": extract_image_brand(soup),
        "Price": extract_price(soup),
        "tech_file":extract_tech_file(soup)
        }
    
        with open('data.json', 'a') as json_file:
            json.dump(data, json_file)
            json_file.write(',\n')


#----scraper----#
def scraper():
    menu=extract_menu()
    for link in menu:
        last_number = extract_number_of_pages(link)
        if last_number == 1:
            extract_content(link)
        else:
            extract_content(link)
            for i in range(2, last_number+1):
                extract_content(f'{link}?page={i}&order=product.price.asc')


#----main----#
"""if __name__ == "__main__":
    scraper()"""

