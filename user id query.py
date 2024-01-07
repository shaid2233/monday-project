import requests
import json

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwNTc5NjI0MCwiYWFpIjoxMSwidWlkIjo0ODAyMDIyMSwiaWFkIjoiMjAyNC0wMS0wMVQxNDozODowNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTg1MTU3MzksInJnbiI6ImV1YzEifQ.Rb509K9gkxYaFh2IoZYRq8uQKYoNgOZekepaJcryAIQ"  # Replace with your actual API key
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization": apiKey}

query = '''
{
    users {
        id
        name
        email
    }
}
'''

data = {'query': query}
response = requests.post(url=apiUrl, json=data, headers=headers)

if response.status_code == 200:
    users = response.json().get('data', {}).get('users', [])
    for user in users:
        if user['name'] == "Shai Daniel":  # Replace with the name you're looking for
            print(f"User ID: {user['id']}, Name: {user['name']}, Email: {user['email']}")
else:
    print("Failed to retrieve user information:", response.text)
