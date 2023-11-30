import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
from urllib.parse import quote
from datetime import datetime

startURL = "https://lemmy.world/instances"
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

def round_seconds(dt, decimal_places=0):
    seconds = dt.second + dt.microsecond / 1_000_000.0
    rounded_seconds = round(seconds, decimal_places)
    microsecond = int(rounded_seconds * 1_000_000) % 1_000_000
    return dt.replace(second=int(rounded_seconds), microsecond=microsecond)

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

    # Check if the base URL is already a key in the data
    if base_url not in data[top_domain]:
        # If the key doesn't exist, create a new entry with links and scan date
        data[top_domain][base_url] = {
            'links': links,
            'scan_date': round_seconds(datetime.now(), 0).strftime("%Y-%m-%d %H:%M:%S")  # Format datetime as desired
        }
    elif isinstance(data[top_domain][base_url], list):
        # If the key exists but is a list, convert it to a dictionary
        existing_links = set(data[top_domain][base_url])
        new_links = [link for link in links if link not in existing_links]
        data[top_domain][base_url] = {
            'links': existing_links.union(new_links),
            'scan_date': round_seconds(datetime.now(), 0).strftime("%Y-%m-%d %H:%M:%S")  # Format datetime as desired
        }
    else:
        # If the key already exists and is a dictionary, append new links to the existing list
        existing_links = set(data[top_domain][base_url]['links'])
        new_links = [link for link in links if link not in existing_links]
        data[top_domain][base_url]['links'] = list(existing_links.union(new_links))
        # Update the scan date, rounding seconds to 2 decimal places
        data[top_domain][base_url]['scan_date'] = round_seconds(datetime.now(), 0).strftime("%Y-%m-%d %H:%M:%S")  # Format datetime as desired

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