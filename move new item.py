import requests
import json
import time

# Your API key, Board ID, Person X's ID, and target group ID
apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwNTc5NjI0MCwiYWFpIjoxMSwidWlkIjo0ODAyMDIyMSwiaWFkIjoiMjAyNC0wMS0wMVQxNDozODowNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.Rb509K9gkxYaFh2IoZYRq8uQKYoNgOZekepaJcryAIQ"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization": apiKey}
board_id = "1258969323"
person_x_id = "48020221"  # The unique ID of Person X
target_group_id = "new_group43041"

def fetch_items():
    query = f'''
    {{
      boards(ids: {1258969323}) {{
        items {{
          id
          column_values {{
            id
            text
          }}
        }}
      }}
    }}
    '''
    response = requests.post(apiUrl, json={'query': query}, headers=headers)
    return response.json()['data']['boards'][0]['items']

def dry_run_move_item_to_group(item_id, group_id):
    # This function now just prints what it would do
    print(f"Would move item {item_id} to group {group_id}")

while True:
    items = fetch_items()
    for item in items:
        for column in item['column_values']:
            # Assuming 'person' is the ID of the person column
            if column['id'] == 'person' and person_x_id in column['text']:
                print(f"Item {item['id']} is assigned to person {person_x_id}.")
                dry_run_move_item_to_group(item['id'], target_group_id)

    time.sleep(10)  # Short wait for testing
