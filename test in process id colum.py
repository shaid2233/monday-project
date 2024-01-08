

import requests
import json

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwNTc5NjI0MCwiYWFpIjoxMSwidWlkIjo0ODAyMDIyMSwiaWFkIjoiMjAyNC0wMS0wMVQxNDozODowNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.Rb509K9gkxYaFh2IoZYRq8uQKYoNgOZekepaJcryAIQ"  # Replace with your actual API key
board_id = "1258969323"  # Replace with your actual board ID
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization": apiKey}

query = '''
{
  boards(ids: [%s]) {
    columns {
      id
      title
      type
    }
  }
}
''' % board_id

response = requests.post(apiUrl, json={'query': query}, headers=headers)

if response.status_code == 200:
    columns = response.json()['data']['boards'][0]['columns']
    for column in columns:
        if column['title'] == "In Process" and column['type'] == "status":
            print(f"The ID of the 'In Process' status column is: {column['id']}")
else:
    print("Failed to fetch columns:", response.text)
