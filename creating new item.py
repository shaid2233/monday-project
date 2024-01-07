import requests
import json

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwNTc5NjI0MCwiYWFpIjoxMSwidWlkIjo0ODAyMDIyMSwiaWFkIjoiMjAyNC0wMS0wMVQxNDozODowNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.Rb509K9gkxYaFh2IoZYRq8uQKYoNgOZekepaJcryAIQ"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}

query3 = 'mutation{ create_item (board_id:1258969323, item_name:"WHAT IS UP MY FRIENDS!") { id } }'
data = {'query' : query3}

r = requests.post(url=apiUrl, json=data, headers=headers) # make request
print(r.json())