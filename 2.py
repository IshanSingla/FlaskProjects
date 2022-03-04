import requests
response = requests.post("https://inducedflask.herokuapp.com/Ishan",json={"key":"hi"})
print(response.text)