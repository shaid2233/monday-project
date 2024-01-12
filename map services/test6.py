import requests
import urllib.parse
import json

# Your monday.com API key (replace with your actual key)
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwNTc5NjI0MCwiYWFpIjoxMSwidWlkIjo0ODAyMDIyMSwiaWFkIjoiMjAyNC0wMS0wMVQxNDozODowNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.Rb509K9gkxYaFh2IoZYRq8uQKYoNgOZekepaJcryAIQ'  # Be sure to replace this with your actual API key
# The ID of the board containing the addresses
board_id = 1258969323  # Make sure this is the correct board ID

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

try:
    # Send request to monday.com API
    response = requests.post(url=monday_api_url, json={'query': query}, headers=headers)
    response.raise_for_status()  # Raises an exception if the request failed
except requests.exceptions.HTTPError as err:
    print(err)
else:
    # If the request was successful, process each item
    for item in response.json()['data']['boards'][0]['items']:
        # Extract the deal name from the item's name
        deal_name = item['name']
        # Extract the address from the column titled 'Address'
        address = next((col['text'] for col in item['column_values'] if col['title'] == 'Address'), None)
        if address:
            # URL-encode the address to create a Google Maps URL
            encoded_address = urllib.parse.quote(address)
            google_maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"

            # The ID of the column where you want to place the Google Maps link
            link_column_id = 'link'  # This should be the actual ID of your "Link" column
            
            # GraphQL mutation to update the link column with the Google Maps URL
            # Note: The value for a Link column should be a JSON object with `url` and `text` keys
            value = json.dumps({
                "url": google_maps_url,
                "text": deal_name  # Use the deal name as the display text for the link
            })
            update_query = '''
            mutation ($itemId: Int!, $columnId: String!, $value: JSON!) {
                change_column_value(item_id: $itemId, board_id: %s, column_id: $columnId, value: $value) {
                    id
                }
            }
            ''' % board_id
            
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
                print(f"Item ID: {item['id']}, Deal '{deal_name}' Google Maps URL updated.")
            except requests.exceptions.HTTPError as err:
                print(f"Failed to update item ID {item['id']}:", err)
