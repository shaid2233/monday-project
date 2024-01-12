
import os
import requests
import urllib.parse
import json

# Your monday.com API key (replace with your actual key)
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwMzQ1OTc5NywiYWFpIjoxMSwidWlkIjo0ODAwNjMzMiwiaWFkIjoiMjAyMy0xMi0xOFQxMjoyMDozMi44MzNaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.NqcmiUk34GRgaLwLMeJZ2Pl1ceHyn5MBL3w2ywOiYR8'
# The ID of the board containing the addresses
board_id = 1258969323

# The monday.com API endpoint for querying boards
monday_api_url = 'https://api.monday.com/v2'
headers = {
    'Authorization': api_key,
    'Content-Type': 'application/json'
}

# GraphQL query to fetch items from a specific board
query = '''
{
    boards(ids: %s) {
        items {
            id
            name
            column_values {
                id
                text
                title
                value
            }
        }
    }
}
''' % board_id

# ... [previous code]

try:
    # Send request to monday.com API
    response = requests.post(url=monday_api_url, json={'query': query}, headers=headers)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    # If the request was successful, process each item
    for item in response.json()['data']['boards'][0]['items']:
        # Use the item's ID directly if that's what you mean by item_id
        item_id = item['id']

        # Your logic to use item_id here
        if item_id:
            # Example: Create a Google Maps URL using the item_id
            # Modify this logic as per your requirement
            google_maps_url = f"https://www.google.com/maps/search/?api=1&query={item_id}"

            # ... [code to update the link column in Monday.com]


            # The ID of the column where you want to place the Google Maps link
            link_column_id = 'link'
            
            # GraphQL mutation to update the link column with the Google Maps URL
            # Note: The value for a Link column should be a JSON object with `url` and `text` keys
            value = json.dumps({
                "url": google_maps_url,
                "text": "View on Google Maps"
            })
            update_query = '''
            mutation ($itemId: Int!, $columnId: String!, $value: JSON!) {
                change_column_value(item_id: $itemId, board_id: %s, column_id: $columnId, value: $value) {
                    id
                }
            }
            ''' % (board_id)
            
            # Send the update request to monday.com
            update_payload = {
                'query': update_query,
                'variables': {
                    'itemId': int(item['id']),
                    'columnId': link_column_id,
                    'value': value
                }
            }
            update_response = requests.post(url=monday_api_url, json=update_payload, headers=headers)
            try:
                update_response.raise_for_status()  # Raises an exception if the update request failed
                # Output the updated information to the console
                print(f"Item ID: {item['id']}, Google Maps URL updated.")
            except requests.exceptions.HTTPError as err:
                print(f"Failed to update item ID {item['id']}:", err)
