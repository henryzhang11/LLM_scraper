import requests

response = requests.get("https://en.wikipedia.org/robots.txt")
test = response.text

print(test)
