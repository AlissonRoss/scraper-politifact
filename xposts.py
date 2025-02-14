from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

# Set up the Chrome WebDriver
service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument('--headless')  # Headless mode to run in the background
driver = webdriver.Chrome(service=service, options=options)

# URL to scrape (Politifact fact-checks about tweets)
url = 'https://www.politifact.com/factchecks/list/?speaker=tweets'

# Open the page
driver.get(url)

# Wait for the fact-check elements to be visible (adjust waiting condition)
try:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'o-factcheck-summary')))
except:
    print("Timeout: Couldn't find fact-check entries.")
    driver.quit()
    exit()

# Parse the page with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Lists to store the scraped data
users = []
source_urls = []

# Find all the fact-check elements (each tweet fact-check entry)
fact_check_elements = soup.find_all('li', class_='o-factcheck-summary')

# Iterate through the fact-checks and extract data
for fact_check in fact_check_elements:
    # Find the link to the detailed fact-check page
    quote_link = fact_check.find('a', class_='m-statement_quote')
    if quote_link:
        # Click on the link to open the fact-check page
        fact_check_url = 'https://www.politifact.com' + quote_link['href']
        driver.get(fact_check_url)  # Navigate to the fact-check page

        # Wait for the tweet's user and URL to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-tweet__user')))
        
        # Parse the new page
        fact_check_page_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract the source user (the user who posted the tweet)
        user = fact_check_page_soup.find('a', class_='c-tweet__user')
        if user:
            users.append(user.text.strip())
        else:
            users.append(None)
        
        # Extract the source URL (the link to the original tweet, not the Politifact URL)
        tweet_link = fact_check_page_soup.find('a', href=True)
        if tweet_link and 'x.com' in tweet_link['href']:
            source_urls.append(tweet_link['href'])  # Direct link to the tweet
        else:
            source_urls.append(None)

        # Go back to the main page to continue scraping
        driver.back()
        
        # Optional: Add a small delay to avoid being flagged as a bot
        time.sleep(2)

# Create a DataFrame to store the data
data = pd.DataFrame({
    'user': users,
    'source_url': source_urls
})

# Show the first 5 rows of the data
print(data.head())

# Save the data to a CSV file
data.to_csv('politifact_x_sources.csv', index=False)

# Close the browser
driver.quit()

