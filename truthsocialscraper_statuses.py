from dotenv import load_dotenv
import os
import csv
from truthbrush.api import Api
from bs4 import BeautifulSoup
import cloudscraper
import time

# Create Cloudflare scraper to bypass the security check
scraper = cloudscraper.create_scraper()

# Check Cloudflare bypass (optional)
response = scraper.get("https://www.truthsocial.com")
print(response.status_code)  # Should print 200 if successful

# Load environment variables
load_dotenv()

# Load username and password from .env
username = os.getenv("USERNAME_TRUTH")
password = os.getenv("PASSWORD")

# Check if both username and password are present
if not username or not password:
    raise ValueError("Missing USERNAME or PASSWORD in .env")

print(f"Loaded Username: {username}")

# Login with the API
api = Api(username=username, password=password)

# Fetch posts from a specific user (e.g., WhiteHouse)
try:
    posts = api.pull_statuses("WhiteHouse")
except Exception as e:
    print(f"Error fetching posts: {e}")
    posts = []

# Function to clean HTML tags from content
def clean_html(raw_html):
    return BeautifulSoup(raw_html, "html.parser").get_text()

# Write data to CSV
with open("user_statuses.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the headers for the CSV
    writer.writerow(["Post ID", "Content", "Created At"])

    # Check if posts are available
    if not posts:
        print("No posts found.")
    else:
        # Loop through each post and save the data
        for post in posts:
            post_id = post.get("id", "N/A")
            content = post.get("content", "No content available")
            created_at = post.get("created_at", "Unknown date")

            # Clean HTML content from the post
            clean_content = clean_html(content)

            # Write the post data to the CSV file
            writer.writerow([post_id, clean_content, created_at])
            
            # Optional: add a delay between requests to avoid hitting the rate limit
            time.sleep(1)

print("Statuses saved to user_statuses.csv")


#However, truthbrush does not automatically paginate to get all of a user's posts dynamically
#So, we must figure another way to get all of their statuses OR find the one in specific.
#Also it is good to note that Truthbrush does not support the collection of re-truths
#However, here are some of the items it can collect:
'''Commands:
  search            Search for users, statuses or hashtags.
  statuses          Pull a user's statuses.
  suggestions       Pull the list of suggested users.
  tags              Pull trendy tags.
  trends            Pull trendy Truths.
  ads               Pull ads.
  user              Pull a user's metadata.
  likes             Pull the list of users who liked a post
  comments          Pull the list of oldest comments on a post
  groupposts        Pull posts from a groups's timeline
  grouptags         Pull trending group tags.
  grouptrends       Pull trending groups.
  groupsuggestions  Pull list of suggested groups.
'''