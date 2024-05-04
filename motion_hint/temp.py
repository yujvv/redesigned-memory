import requests

url = 'http://localhost:5000/ask'
response = requests.post(url, json={'query': "注意事项有什么？"})
data = response.json()
context = data['context']
print(context)

