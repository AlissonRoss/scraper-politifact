from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from datetime import datetime

# Function to check if a date is within the desired range (2024)
def is_valid_date(date_string):
    try:
        # Debugging: Print the raw date string to see its format
        print(f"Checking date: {date_string}")
        
        # Parse the date from the string (e.g., "January 30, 2025")
        date_obj = datetime.strptime(date_string, "%B %d, %Y")
        start_date = datetime(2024, 1, 1)  # January 1, 2024
        end_date = datetime(2024, 12, 31)  # December 31, 2024
        # Return True if the date is in the range, else False
        return start_date <= date_obj <= end_date
    except ValueError as ve:
        print(f"Error parsing date: {ve}")
        return False

# Function to check if the date is from 2023 or earlier
def is_invalid_date(date_string):
    try:
        date_obj = datetime.strptime(date_string, "%B %d, %Y")
        end_date_2024 = datetime(2024, 1, 1)  # Stop when we hit any date from 2023 or earlier
        return date_obj < end_date_2024
    except ValueError as ve:
        print(f"Error parsing date: {ve}")
        return False

# Set up the Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (optional)

# Set up the Chrome driver with the correct service
driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service, options=chrome_options)

# Starting URL (first page)
base_url = "https://www.politifact.com/factchecks/list/?speaker=tweets&page="

# Prepare a list to store scraped data
scraped_data = []

# Initialize the page number
page_number = 1

# Start scraping and navigating pages if needed
while True:
    # Construct the URL for the current page
    url = f"{base_url}{page_number}"
    
    # Open the URL
    driver.get(url)
    print(f"Scraping page {page_number}...")

    # Wait for the page to load and the dynamic content to appear
    time.sleep(3)  # You can adjust this time if needed

    # Collect data from the current page using the correct method
    fact_checks = driver.find_elements(By.CLASS_NAME, "o-listicle__item")

    # If no fact checks are found, we assume we've reached the end of the pages
    if not fact_checks:
        print("No more pages to scrape.")
        break

    # Iterate through the fact-checks on this page
    for fact_check in fact_checks:
        try:
            # Extract the necessary information for each fact-check item
            author = fact_check.find_element(By.CLASS_NAME, "m-statement__name").text
            statement = fact_check.find_element(By.CLASS_NAME, "m-statement__quote").text
            source_url = fact_check.find_element(By.CLASS_NAME, "m-statement__quote").find_element(By.TAG_NAME, 'a').get_attribute('href')
            
            # Extract the date from the footer (e.g., "By Sofia Ahmed • January 30, 2025")
            footer_text = fact_check.find_element(By.CLASS_NAME, "m-statement__footer").text
            print(f"Extracted footer text: {footer_text}")  # Debugging line
            date_string = footer_text.split("•")[-1].strip()

            # Check if we should stop scraping (2023 or earlier)
            if is_invalid_date(date_string):
                print(f"Encountered a post from {date_string} (2023 or earlier). Stopping scraping.")
                break  # Stop scraping entirely when we encounter a post from 2023 or earlier
            
            # Filter by date range (2024)
            if not is_valid_date(date_string):
                # Skip the post if it's from a year outside of 2024
                print(f"Skipping post from {date_string} as it's not within 2024.")
                continue  # Skip to the next fact-check if it's not within 2024

            # Extract the rating and fact-check URL
            rating = fact_check.find_element(By.CLASS_NAME, "m-statement__meter").find_element(By.TAG_NAME, 'img').get_attribute('alt')
            url = fact_check.find_element(By.CLASS_NAME, "m-statement__quote").find_element(By.TAG_NAME, 'a').get_attribute('href')

            # Add the extracted data to the list
            scraped_data.append([author, statement, source_url, date_string, rating, url])
        
        except Exception as e:
            print(f"Error extracting data: {e}")

    # If we encountered a 2023 post, break out of the loop completely and stop scraping
    if is_invalid_date(date_string):
        print(f"Breaking out of scraping due to encountering a post from {date_string}.")
        break

    # Increment the page number to load the next page
    page_number += 1

# Check if there's any data to write
if scraped_data:
    # Save the scraped data to a CSV file
    with open('politifact_data_2024.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Author', 'Statement', 'Source', 'Date', 'Rating', 'URL'])
        writer.writerows(scraped_data)
    print(f"Scraping complete! Data saved to 'politifact_data_2024.csv'")
else:
    print("No data collected to save.")

# Close the driver
driver.quit()
