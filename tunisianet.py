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
        soup = get_soup("https://www.tunisianet.com.tn/")
        menu_element = soup.find('ul', class_='menu-content top-menu')
        menu_items = menu_element.find_all('li', class_='menu-item item-header')
        for item in menu_items:
            link = item.find('a')['href']
            menu_list.append(link)
        return menu_list


def get_brand_names(url):
    soup = get_soup(url)
    
    li_tags_container = soup.find('div', class_='af_filter clearfix m type-1 cut-off')
    li_tags = li_tags_container.find_all('li')
    brand_names = []
    for li_tag in li_tags:
        if 'no-matches' not in li_tag.get('class', []): 
            name_tag = li_tag.find('span', class_="name")
            brand_names.append(name_tag.text.strip().lower())
    return brand_names


#----function to extract number of pages exp('https://www.tunisianet.com.tn/702-ordinateur-portable')----#
def extract_number_of_pages(url):
    soup = get_soup(url)
    pagination = soup.find('ul', {'class':'page-list clearfix'})
    if pagination:
        page_links = pagination.find_all('a')
        return int(page_links[-2].text)
    else: return 1


#----function to extract products links exp('https://www.tunisianet.com.tn/702-ordinateur-portable')----#
def extract_products_links(url):
    titles_with_links = []
    soup = get_soup(url)
    items = soup.find_all('div', class_='item-product col-xs-12')

    for item in items:
        title_tag = item.find('h2', class_='h3 product-title')
        if title_tag:
            link = title_tag.a['href']
            titles_with_links.append(link)
    return titles_with_links


#----extract products details----#

def extract_categories(soup):
    breadcrumb_list = []
    breadcrumb_nav = soup.find('nav', class_='breadcrumb col-xs-12')
    
    if breadcrumb_nav:
        breadcrumb_items = breadcrumb_nav.find_all('li', itemprop='itemListElement')
        for item in breadcrumb_items[:-1]:  # Exclude the last item
            breadcrumb_text = item.find('span', itemprop='name').text.strip()
            breadcrumb_list.append(breadcrumb_text)
    
    return breadcrumb_list

def extract_product_images(soup):
    image_links = []
    images_container = soup.find('div', class_='images-container')
    
    if images_container:
        image_tags = images_container.find_all('img', itemprop='image')
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

def extract_name(soup):
    elements = soup.find('h1', itemprop='name')

    return elements.text.strip()

#----------------------------#

#-->function to receive products links and save products details
def extract_content(name, url):
    products_links= extract_products_links(url)
    for link in products_links:
        soup= get_soup(link)
        data= {
        'product name':extract_name(soup),
        'brand name':name,
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
        print(link)
        brand_names=get_brand_names(link)
        for brand_name in brand_names:
            print(brand_name,f'{link}?fabricants={brand_name}&order=product.price.asc')
            last_number = extract_number_of_pages(f'{link}?fabricants={brand_name}&order=product.price.asc')
            print(last_number)
            if last_number == 1:
                extract_content(brand_name, f'{link}?fabricants={brand_name}&order=product.price.asc')
            else:
                extract_content(brand_name, f'{link}?fabricants={brand_name}&order=product.price.asc')
                for i in range(2, last_number+1):
                    extract_content(brand_name, f'{link}?fabricants={brand_name}&page={i}&order=product.price.asc')




#----main----#
if __name__ == "__main__":
    scraper()

