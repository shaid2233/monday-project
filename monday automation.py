
import requests
import json

api_key = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwNTc5NjI0MCwiYWFpIjoxMSwidWlkIjo0ODAyMDIyMSwiaWFkIjoiMjAyNC0wMS0wMVQxNDozODowNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.Rb509K9gkxYaFh2IoZYRq8uQKYoNgOZekepaJcryAIQ"  # Replace with your actual API key
board_id = "1258969323"  # Replace with your actual board ID
status_column_id = "status_15"  # Replace with the ID of your status column
api_url = "https://api.monday.com/v2"
headers = {"Authorization": api_key}

# The group IDs you want to move the items to
group_id_for_tomer = "new_group29179"  # Replace with actual group ID
group_id_for_shai = "new_group"  # Replace with actual group ID
group_id_for_dan = "new_group43041"  # Replace with actual group ID

# GraphQL query to fetch items and their status from the board
query = '''
{
  boards(ids: [%s]) {
    items {
      id
      column_values(ids: ["%s"]) {
        text
      }
    }
  }
}
''' % (board_id, status_column_id)

response = requests.post(api_url, json={'query': query}, headers=headers)

if response.status_code == 200:
    items = response.json()['data']['boards'][0]['items']
    for item in items:
        status_text = item['column_values'][0]['text']
        item_id = item['id']
        # Decide which group to move the item to based on the status
        if status_text == "Tomer":
            target_group_id = group_id_for_tomer
        elif status_text == "Shai":
            target_group_id = group_id_for_shai
        elif status_text == "Dan":
            target_group_id = group_id_for_dan
        else:
            continue  # If the status is not one of the names, do nothing
        
        # GraphQL mutation to move the item to the target group
        move_item_mutation = '''
        mutation {
          move_item_to_group (item_id: %s, group_id: "%s") {
            id
          }
        }
        ''' % (item_id, target_group_id)
        
        # Execute the move item mutation
        move_response = requests.post(api_url, json={'query': move_item_mutation}, headers=headers)
        if move_response.status_code == 200:
            print(f"Item {item_id} moved to group {target_group_id}")
        else:
            print(f"Failed to move item {item_id}. Status Code: {move_response.status_code} Response: {move_response.text}")

else:
    print("Failed to fetch items. Status Code:", response.status_code, "Response:", response.text)
