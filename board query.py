import requests
import json

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwNTc5NjI0MCwiYWFpIjoxMSwidWlkIjo0ODAyMDIyMSwiaWFkIjoiMjAyNC0wMS0wMVQxNDozODowNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.Rb509K9gkxYaFh2IoZYRq8uQKYoNgOZekepaJcryAIQ"  
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization": apiKey}

query = '''
{
  boards(ids: 1258969323) {
    name
    groups {
      id
      title
      items {
        id
        name
      }
    }
  }
}
'''

data = {'query': query}
response = requests.post(url=apiUrl, json=data, headers=headers)

if response.status_code == 200:
    board_data = response.json().get('data', {}).get('boards', [])
    for board in board_data:
        print(f"Board Name: {board['name']}")
        for group in board.get('groups', []):
            print(f"  Group ID: {group['id']}, Group Title: {group['title']}")
            for item in group.get('items', []):
                print(f"    Item ID: {item['id']}, Item Name: {item['name']}")
else:
    print("Failed to retrieve board details:", response.text)
