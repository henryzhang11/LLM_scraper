import requests
from bs4 import BeautifulSoup

url = "https://data.gov"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the relevant element containing the dataset count
# You might need to inspect the website's HTML structure to determine the correct selector
dataset_count_element = soup.find(class_="dataset-count")

# Extract the number from the element
dataset_count = dataset_count_element.text.strip()

print(f"Number of datasets on data.gov: {dataset_count}")