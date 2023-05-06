import requests
from bs4 import BeautifulSoup
import re

def is_valid_link(link):
    # Define the regex pattern to match URLs
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # Scheme (http, https, ftp, etc.)
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # Optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # Match the link with the regex pattern
    return re.match(url_pattern, link) is not None



# Send a GET request to the URL
url = 'https://www.mytek.tn/'
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'lxml')

# Find all the category titles
categories = soup.find('ul', class_='vertical-list clearfix')
categories = categories.find_all('li')
# Extract the category names and links and print them out


def get_category():
    dictionary={}
    for category in categories:
        name = category.find('a').text.strip()
        link = category.find('a')['href']
        if is_valid_link(link):
            dictionary[name] = link
    return dictionary