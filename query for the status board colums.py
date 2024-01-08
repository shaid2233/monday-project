import requests
import json

# Your API key and the board ID you want to query
apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwNTc5NjI0MCwiYWFpIjoxMSwidWlkIjo0ODAyMDIyMSwiaWFkIjoiMjAyNC0wMS0wMVQxNDozODowNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.Rb509K9gkxYaFh2IoZYRq8uQKYoNgOZekepaJcryAIQ"
board_id = "1258969323"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization": apiKey}

# GraphQL query to fetch all columns of the specified type 'status' from the board
query = f'''
{{
  boards(ids: [{board_id}]) {{
    columns {{
      id
      title
      type
    }}
  }}
}}
'''

# Send the request to Monday.com API
response = requests.post(apiUrl, json={'query': query}, headers=headers)

# Check for errors in the response and then process the data
if response.status_code == 200:
    data = response.json()['data']['boards'][0]['columns']
    status_columns = [col for col in data if col['type'] == 'status']
    for col in status_columns:
        print(f"Status Column ID: {col['id']}, Title: {col['title']}")
else:
    print("Failed to fetch columns:", response.text)
