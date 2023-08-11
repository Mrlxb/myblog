import requests

url = 'https://cj02.xyz/'

res = requests.get(url)

print(res.text)