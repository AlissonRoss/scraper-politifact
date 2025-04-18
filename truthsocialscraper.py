from dotenv import load_dotenv
import os
from truthbrush import TruthSocial

ts = TruthSocial()
# Load .env variables
load_dotenv()

# Truth Social credentials
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

print(f"Logging in with {username}")

#This gets the recent statuses of a given user
posts = ts.get_user_statuses('arosss')

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