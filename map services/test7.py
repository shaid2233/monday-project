import requests
import urllib.parse
import json

# Your monday.com API key (replace with your actual key)
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwNTc5NjI0MCwiYWFpIjoxMSwidWlkIjo0ODAyMDIyMSwiaWFkIjoiMjAyNC0wMS0wMVQxNDozODowNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.Rb509K9gkxYaFh2IoZYRq8uQKYoNgOZekepaJcryAIQ'  # Please ensure to use a secure method to handle your API key
# The ID of the board containing the deals
board_id = 1258969323  # Ensure this is your actual board ID

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
# ... [previous code]

else:
    # If the request was successful, process each item
    for item in response.json()['data']['boards'][0]['items']:
        # Extract the custom 'Item ID' from the column titled 'Item ID'
        # Assume the column ID for 'Item ID' is 'text_column_id' - you need to replace it with the actual ID
        custom_item_id = next((col['text'] for col in item['column_values'] if col['id'] == 'text_column_id'), None)

        # Extract the address from the column titled 'Address'
        # Assume the column ID for 'Address' is 'address_column_id' - you need to replace it with the actual ID
        address = next((col['text'] for col in item['column_values'] if col['id'] == 'address_column_id'), None)

        if address:
            # URL-encode the address to create a Google Maps URL
            encoded_address = urllib.parse.quote(address)
            google_maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"

            # The ID of the column where you want to place the Google Maps link
            # Replace 'link_column_id' with the actual ID of your "Link" column
            link_column_id = 'link'

            # ... [rest of the code for mutation and update logic]
