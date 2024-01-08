import requests
import json
import time

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwNTc5NjI0MCwiYWFpIjoxMSwidWlkIjo0ODAyMDIyMSwiaWFkIjoiMjAyNC0wMS0wMVQxNDozODowNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.Rb509K9gkxYaFh2IoZYRq8uQKYoNgOZekepaJcryAIQ"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization": apiKey}
board_id = "1258969323"
status_column_id = "multiple_person"  # Replace with your actual status column ID
person_x_id = "48020221"  # The unique ID of Person X
new_deals_group_id = "new_group29179"  # The group ID for "New Deals"

def check_and_move_items():
    # Query to fetch items with their status and assigned person
    query = f'''
    {{
      boards(ids: {board_id}) {{
        items {{
          id
          name
          column_values(ids: ["{status_column_id}", "person"]) {{
            id
            text
          }}
        }}
      }}
    }}
    '''
    response = requests.post(apiUrl, json={'query': query}, headers=headers)
    items = response.json()['data']['boards'][0]['items']

    # Check each item's status and assigned person
    for item in items:
        status = None
        assigned_person = None
        for column in item['column_values']:
            if column['id'] == status_column_id:
                status = column['text']
            elif column['id'] == 'person':
                assigned_person = column['text']
        
        # Move item if status is "In Process" and assigned to Person X
        if status == "In Process" and str(person_x_id) in assigned_person:
            move_item_to_group(item['id'], new_deals_group_id)

def move_item_to_group(item_id, group_id):
    # Mutation to move the item to the specified group
    mutation = f'''
    mutation {{
      move_item_to_group (item_id: {item_id}, group_id: "{group_id}") {{
        id
      }}
    }}
    '''
    response = requests.post(apiUrl, json={'query': mutation}, headers=headers)
    print(f"Moved item {item_id} to group {group_id}: {response.json()}")

# Check the board periodically (e.g., every 60 seconds)
while True:
    check_and_move_items()
    time.sleep(10)
