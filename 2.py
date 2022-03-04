import requests,time
response = requests.get("https://inducedflask.herokuapp.com/",timeout=10)
time.sleep(2)
response = requests.post("https://inducedflask.herokuapp.com/Key",json={"Key":"ishansss","Proxy":138273},timeout=10)
print(response.text)