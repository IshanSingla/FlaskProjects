import requests
response = requests.post("https://inducedflask.herokuapp.com/Ishan?Key=0")
print(response.text)