import requests
import json

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwNTc5NjI0MCwiYWFpIjoxMSwidWlkIjo0ODAyMDIyMSwiaWFkIjoiMjAyNC0wMS0wMVQxNDozODowNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.Rb509K9gkxYaFh2IoZYRq8uQKYoNgOZekepaJcryAIQ"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization": apiKey}

def check_assignee_change(item_id, target_assignee_id):
    query = '''
    {
        items(ids: %s) {
            column_values {
                id
                title
                text
            }
        }
    }
    ''' % item_id

    data = {'query': query}
    r = requests.post(url=apiUrl, json=data, headers=headers)

    print("Check Assignee Response Status Code:", r.status_code)
    print("Check Assignee Response Content:", r.content)

    if r.status_code == 200:
        response_data = r.json()
        if 'data' in response_data and 'items' in response_data['data']:
            item = response_data['data']['items'][0]
            for column_value in item['column_values']:
                if column_value['title'] == "Assignee" and str(column_value['text']).contains(str(target_assignee_id)):
                    return True  # Assignee change matches the target assignee
    return False

def move_item_to_another_group(item_id, target_group_id):
    mutation = '''
    mutation {
        move_item_to_group (item_id: %s, group_id: %s) {
            id
            name
        }
    }
    ''' % (item_id, target_group_id)

    data = {'query': mutation}
    r = requests.post(url=apiUrl, json=data, headers=headers)

    print("Move Item Response Status Code:", r.status_code)
    print("Move Item Response Content:", r.content)

    if r.status_code == 200:
        response_data = r.json()
        if 'data' in response_data and 'move_item_to_group' in response_data['data']:
            moved_item = response_data['data']['move_item_to_group']
            print(f"Item '{moved_item['name']}' (ID: {moved_item['id']}) moved successfully.")
        else:
            print("Failed to move the item. Response:", response_data)
    else:
        print("Failed to move the item:", r.text)

# Set your specific values here
item_id = "1355945601"  # New random item ID
target_assignee_id = 48020221  # User ID for Shai Daniel
target_group_id = "new_group"  # ID for the group "Deals after Check"

if check_assignee_change(item_id, target_assignee_id):
    move_item_to_another_group(item_id, target_group_id)

