import requests

url = "https://en.wikipedia.org/robots.txt"

try:
  response = requests.get(url)
  response.raise_for_status()  # Raise an exception for bad status codes
  content = response.text
  print(content)

except requests.exceptions.RequestException as e:
  print(f"Error fetching robots.txt: {e}")