import requests
from bs4 import BeautifulSoup
startURL = "https://kuben.vgs.no"

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

            # Find all links in the HTML with 'http://' or 'https://' in the href attribute
            all_links = [a['href'] for a in soup.find_all('a', href=True)]
            http_links = [link for link in all_links if 'http://' in link or 'https://' in link]

            return http_links
        else:
            print(f"Error: Unable to fetch the URL. Status Code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []
##############################################################################################################
##############################################################################################################
##############################################################################################################

print(get_links(startURL))