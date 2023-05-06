import json
import requests
from bs4 import BeautifulSoup
import os



script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data.txt")



def page_number(soup):
    pagination = soup.find('ul', {'class':'page-list clearfix text-sm-center'})
    if pagination:
        page_links = pagination.find_all('a')
        return int(page_links[-2].text)
    else: return 1




def get_product(value,page):
    page_url = f"{value}?page={page}"
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'lxml')
    return page_soup.find_all('div', {'class': 'product-description thumbnail-description'})



def get_product_content(key,link):

    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    name = soup.find('h1', {'class': 'product-name'}).text.strip() 
    price = soup.find('span', {'itemprop': 'price'}).text.strip() 
    if soup.find('span', {'itemprop': 'sku'}) is not None:ref=soup.find('span', {'itemprop': 'sku'}).text.strip() 
    else:ref=""
    description = soup.find('div', {'class': 'product-short-description'}).text.strip() 
    image_link = soup.find('img', {'class': 'js-qv-product-cover'})['src']
    return {"categorie": key,"link": link,"name": name,"price": price,"image": image_link,"ref": ref,"description": description}




def main_skymil():
    data_list=[]
    dic={'Config sur mesure': 'https://skymil-informatique.com/pc-sur-mesure', 'Bon Plan': 'https://skymil-informatique.com/201-bon-plan', 'Powered By MSI': 'https://skymil-informatique.com/152-powred-by-msi-tunisie', 'Powered By ASUS': 'https://skymil-informatique.com/129-powered-by-asus', 'Nice Dayz - Entry Level': 'https://skymil-informatique.com/116-Pc-gamer-dayz-tunisie', 'Config R3ad - Mid Range': 'https://skymil-informatique.com/149-pc-gamer-r3ad-tunisie', 'Gaming Guru - High End': 'https://skymil-informatique.com/157-Pc-gaming-guru-tunisie', 'Config 3jeja - Last Chance<': 'https://skymil-informatique.com/154-Pc-gamer-3jeja-tunisie', 'Achkingone Choice': 'https://skymil-informatique.com/199-achkingone-choice', 'NÃ©omorphe': 'https://skymil-informatique.com/165-Pc-gamer-neomorphe', 'Full Setup': 'https://skymil-informatique.com/151-full-setup-Tunisie', 'Pc Portable': 'https://skymil-informatique.com/121-pc-portable-gamer-tunisie', 'Pc Portable Pro': 'https://skymil-informatique.com/170-pc-portable-pro', 'Stockage pour Pc Portable': 'https://skymil-informatique.com/202-stockage-pour-pc-portable', 'Ram pour Pc Portable': 'https://skymil-informatique.com/206-ram-pour-pc-portable', 'Accessoires PC Portable': 'https://skymil-informatique.com/190-accessoires-pc-portable', 'Workstation KIMERA': 'https://skymil-informatique.com/207-workstation-kimera', 'Workstation Intel': 'https://skymil-informatique.com/99-workstation-intel', 'Workstation AMD': 'https://skymil-informatique.com/142-workstation-amd', 'All in one': 'https://skymil-informatique.com/23-pc-all-in-one-tunisie', 'Bureautique': 'https://skymil-informatique.com/96-ordinateur-tunisie', 'Ecran Gamer': 'https://skymil-informatique.com/17-ecrans-gamer', 'Ecrans Pro': 'https://skymil-informatique.com/100-ecrans-pro', 'Processeur Intel': 'https://skymil-informatique.com/25-processeur-intel', 'Carte Mère Intel': 'https://skymil-informatique.com/28-intel-tunisie', 'Processeur AMD': 'https://skymil-informatique.com/131-processeur-amd', 'Carte Mère AMD': 'https://skymil-informatique.com/132-amd-tunisie', 'Carte graphique': 'https://skymil-informatique.com/29-carte-graphique-tunisie', 'Barrette memoire': 'https://skymil-informatique.com/30-memoire-ram-tunisie', 'Disque dur / SSD / Nvme': 'https://skymil-informatique.com/31-ssd-nvme-tunisie', "Bloc d'alimentation": 'https://skymil-informatique.com/32-alimentation-psu-tunisie', 'Boitier': 'https://skymil-informatique.com/33-boitier-gamer-tunisie', "Carte D'extension": 'https://skymil-informatique.com/84-tunisie-carte-extension', 'Disque Dur Externe': 'https://skymil-informatique.com/64-disque-dur-externe-tunisie', 'Ventilateurs et Led-Strip': 'https://skymil-informatique.com/134-ventilateurs-rgb-tunisie', 'Aircooling': 'https://skymil-informatique.com/167-aircooling', 'Watercooling': 'https://skymil-informatique.com/86-watercooling-tunisie', 'pate Thermique': 'https://skymil-informatique.com/175-pate-thermique-tunisie', 'reseau Informatique': 'https://skymil-informatique.com/176-reseau-tunisie', 'Tablette Graphique': 'https://skymil-informatique.com/186-tablette-graphique', 'Multiprises et protection': 'https://skymil-informatique.com/208-multiprises-et-protection', 'Level Up Processeur': 'https://skymil-informatique.com/172-processeur-tunisie', 'Level Up Carte Graphique': 'https://skymil-informatique.com/173-carte-graphique-tunisie', 'Level Up Stockage': 'https://skymil-informatique.com/171-stockage-tunisie', 'Level Up Refroidissement': 'https://skymil-informatique.com/174-refroidissement-tunisie', 'Level Up peripheriques': 'https://skymil-informatique.com/139-peripheriques-tunisie', 'Clavier Gamer': 'https://skymil-informatique.com/101-clavier-gamer-tunisie', 'Souris Gamer': 'https://skymil-informatique.com/102-souris-gamer-tunisie', 'Tapis Gamer': 'https://skymil-informatique.com/103-tapis-gamer-tunisie', 'Micro-casque Gamer': 'https://skymil-informatique.com/104-micro-casque-tunisie', 'Ensemble': 'https://skymil-informatique.com/159-clavier-souris-tunisie', 'Webcam HD': 'https://skymil-informatique.com/136-webcam-hd-tunisie', 'Microphone Gamer': 'https://skymil-informatique.com/138-micro-gamer-tunisie', 'Stockage Console De Jeux': 'https://skymil-informatique.com/158-stockage-console-de-jeux', 'Racing Wheel': 'https://skymil-informatique.com/160-racing-wheel', 'Manette de jeux': 'https://skymil-informatique.com/120-manette-de-jeux', 'Haut parleur': 'https://skymil-informatique.com/128-haut-parleur-tunisie', 'siege Gamer': 'https://skymil-informatique.com/118-siege-gamer-tunisie', 'Sac a dos Gamer': 'https://skymil-informatique.com/180-sac-a-dos-gamer', 'Bureaux Gamer': 'https://skymil-informatique.com/189-bureaux-gamer', 'Console de jeux': 'https://skymil-informatique.com/188-console-de-jeux', 'Impression': 'https://skymil-informatique.com/204-impression', 'TV-Son-Photos': 'https://skymil-informatique.com/205-tv-son-photos'}
    for key, value in dic.items():
        response = requests.get(value)
        soup = BeautifulSoup(response.content, 'lxml')
        for page in range(1,page_number(soup)+1):
            for product_div in get_product(value,page):
                url = product_div.find("a")['content']
                data=get_product_content(key,url)
                if data not in data_list:
                    data_list.append(data)
    with open('data.json', 'w') as f:
        json.dump(data_list, f)
