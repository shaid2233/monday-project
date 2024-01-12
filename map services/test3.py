import requests
import urllib.parse
import json

# Your monday.com API key (replace with your actual key)
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwNTc5NjI0MCwiYWFpIjoxMSwidWlkIjo0ODAyMDIyMSwiaWFkIjoiMjAyNC0wMS0wMVQxNDozODowNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.Rb509K9gkxYaFh2IoZYRq8uQKYoNgOZekepaJcryAIQ'
# The ID of the board containing the addresses
board_id = '1258969323'
# The monday.com API endpoint for querying boards
monday_api_url = 'https://api.monday.com/v2'
# Headers for the HTTP request including your monday.com API key
headers = {
    'Authorization': api_key,
    'Content-Type': 'application/json'
}

# GraphQL query to fetch items from a specific board
query = f'''
{{
    boards(ids: {board_id}) {{
        items {{
            id
            name
            column_values {{
                id
                text
                title
                value
            }}
        }}
    }}
}}
'''

try:
    # Send request to monday.com API
    response = requests.post(url=monday_api_url, json={'query': query}, headers=headers)
    response.raise_for_status()  # Raises an exception if the request failed
except requests.exceptions.HTTPError as err:
    print(err)
else:
    # If the request was successful, process each item
    for item in response.json()['data']['boards'][0]['items']:
        # Extract the address from the column titled 'Address'
        address = next((col['text'] for col in item['column_values'] if col['title'] == 'Address'), None)
        if address:
            # URL-encode the address to create a Google Maps URL
            encoded_address = urllib.parse.quote(address)
            google_maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"

            # Assume you have the ID of the column where you want to place the Google Maps link
            link_column_id = 'text0'
            
            # GraphQL mutation to update the link column with the Google Maps URL
            update_query = f'''
            mutation {{
                change_column_value(item_id: {item['id']}, board_id: {board_id}, column_id: "{link_column_id}", value: "{json.dumps({'url': google_maps_url, 'text': 'Google Maps'})}") {{
                    id
                }}
            }}
            '''
            # Send the update request to monday.com
            update_response = requests.post(url=monday_api_url, json={'query': update_query}, headers=headers)
            update_response.raise_for_status()  # Raises an exception if the update request failed
            # Output the updated information to the console
            print(f"Item ID: {item['id']}, Google Maps URL updated.")
