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

# Read URLs, authors, and statements from the previously scraped CSV file
data_to_scrape = []

with open('politifact_data_2024.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header
    for row in reader:
        author = row[0]  # Author column
        statement = row[1]  # Statement column
        url = row[5]  # URL column (assuming it's in the 6th column)
        data_to_scrape.append([author, statement, url])

# Prepare a list to store extracted data
x_post_links_data = []

# Iterate over the URLs and visit each page
for author, statement, url in data_to_scrape:
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
            # Save the Politifact URL, post name (author/statement), and X post URL
            x_post_links_data.append([url, author, statement, x_post_link])
        
    except Exception as e:
        print(f"Error finding X post links: {e}")

# Save the extracted data (Politifact URL, author, statement, and X post links) to a new CSV file
with open('x_post_links_with_info.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Politifact URL', 'Author', 'Statement', 'X Post URL'])
    for data in x_post_links_data:
        writer.writerow(data)

print(f"Scraping complete! {len(x_post_links_data)} X post links extracted and saved to 'x_post_links_with_info.csv'.")

# Close the driver
driver.quit()
