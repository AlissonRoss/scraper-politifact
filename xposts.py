from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Set up the Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (optional)

# Set up the Chrome driver with the correct service
driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service, options=chrome_options)

# Read URLs, source, statements, and ratings from the previously scraped CSV file
data_to_scrape = []

with open('politifact_personalities.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header
    for row in reader:
        personality = row[2]  # source column
        statement = row[1]  # Statement column
        rating = row[4]  # Rating column (assuming it's in the 5th column)
        url = row[5]  # URL column (assuming it's in the 6th column)
        data_to_scrape.append([personality, statement, rating, url])

# Prepare a list to store extracted data
x_post_links_data = []
seen_x_post_urls = set()  # Set to track seen (unique) X Post URLs

# Iterate over the URLs and visit each page
for author, statement, rating, url in data_to_scrape:
    driver.get(url)
    print(f"Visiting: {url}")

    # Wait for the page to load
    time.sleep(3)  # Adjust if necessary for your connection

    # Scroll down to the bottom to load all content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for page to load after scrolling

    try:
        # Find the "Our Sources" section and extract the X post links
        sources_section = driver.find_element(By.ID, "sources")
        x_post_elements = sources_section.find_elements(By.XPATH, "//a[contains(@href, 'x.com')]")
        
        for element in x_post_elements:
            x_post_link = element.get_attribute("href")
            
            # Check if the X post link is already seen
            if x_post_link not in seen_x_post_urls:
                seen_x_post_urls.add(x_post_link)  # Add to set to avoid duplicates
                # Add the entry with Politifact URL, Author, Statement, Rating, and X Post URL
                x_post_links_data.append([url, author, statement, rating, x_post_link])
        
    except Exception as e:
        print(f"Error finding X post links: {e}")
output_file = 'politifact_personalities_x_urls.csv'
# Save the extracted data (Politifact URL, author, statement, rating, and X post links) to a new CSV file
with open('politifact_personalities_x_urls.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Politifact URL', 'Author', 'Statement', 'Rating', 'X Post URL'])
    for data in x_post_links_data:
        writer.writerow(data)

print(f"Scraping complete! {len(x_post_links_data)} X post links extracted and saved to '{output_file}'.")

# Close the driver
driver.quit()
