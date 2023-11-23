import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
from urllib.parse import quote

startURL = "https://www.oslo.kommune.no/"
SavedFile = "./SavedData/save.json"

##############################################################################################################
##############################################################################################################
##############################################################################################################
def get_links(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all unique links in the HTML with 'http://' or 'https://' in the href attribute
            unique_links = set()
            for a in soup.find_all('a', href=True):
                link = a['href']
                if 'http://' in link or 'https://' in link:
                    # Encode special characters in the URL
                    encoded_link = quote(link, safe=':/')
                    unique_links.add(encoded_link)

            return list(unique_links)
        else:
            print(f"Error: Unable to fetch the URL. Status Code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []
##############################################################################################################
##############################################################################################################
##############################################################################################################
def save_links_to_json(base_url, links):
    # Parse the base URL to get the top domain
    top_domain = urlparse(base_url).netloc

    # Load existing data if available
    try:
        with open(SavedFile, 'r') as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # Create an empty dictionary if the file is not found or is empty
        data = {}

    # Check if the top domain is already in the data
    if top_domain not in data:
        data[top_domain] = {}

    # Update links for the sub-page
    data[top_domain][base_url] = links

    # Save the updated data to the JSON file
    with open(SavedFile, 'w') as json_file:
        json.dump(data, json_file, indent=2)

##############################################################################################################
##############################################################################################################
##############################################################################################################

links = get_links(startURL)
print(links)
print(str(len(links)) + " links")
save_links_to_json(startURL, links)