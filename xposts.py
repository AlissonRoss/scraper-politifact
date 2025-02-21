import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape the details from the URL
def scrape_post_details(url):
    try:
        # Fetch the HTML content
        response = requests.get(url)
        if response.status_code != 200:
            return None, None  # Return None if the request fails

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the poster's name and the original post's source link
        # (You may need to adjust these based on the structure of the page)
        poster_name = soup.find('span', {'class': 'author-name'})  # Adjust selector as needed
        source_link = soup.find('section', {'class': 'sources'})  # Adjust selector as needed

        poster_name = poster_name.get_text() if poster_name else "Unknown"
        source_link = source_link['href'] if source_link else "Unknown"

        return poster_name, source_link
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None, None

# Load the CSV file
df = pd.read_csv('./politifact_factchecks_jan1_to_dec31_2024_with_urls.csv')

# Iterate through each row, scrape the URL and gather details
posters = []
sources = []

for index, row in df.iterrows():
    url = row['url']
    poster_name, source_link = scrape_post_details(url)
    posters.append(poster_name)
    sources.append(source_link)

# Add the scraped details to the dataframe
df['original_poster'] = posters
df['original_source'] = sources

# Save the updated dataframe to a new CSV
df.to_csv('updated_file.csv', index=False)

print("Scraping complete and file saved!")
