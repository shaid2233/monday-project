import urllib.parse

# Example address
address = "1930 68th St, Lubbock, TX 79412"

# URL-encode the address
encoded_address = urllib.parse.quote(address)

# Create the URL for Google Maps
google_maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"

print(google_maps_url)
