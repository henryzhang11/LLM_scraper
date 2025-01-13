from lxml import html
from bs4 import BeautifulSoup
import requests

response = requests.get('http://www.data.gov/')
doc_gov = html.fromstring(response.text)
soup = BeautifulSoup(response.text, 'html.parser')
dataset_count_element = soup.find('span', class_='text-color-red')
dataset_count = dataset_count_element.text.strip() if dataset_count_element else "Dataset count not found"
result = dataset_count.replace(",", "")
print(result)
