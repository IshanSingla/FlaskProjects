import requests
response = requests.get("https://inducedflask.herokuapp.com")
print(response.text)