import requests


url = "https://ion.tjhsst.edu/api/schedule/2016-04-12?format=json"
response = requests.get(url)

print(response.json())