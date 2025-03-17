import pandas as pd
import re

# Input and output CSV files
input_file = "politifact_factchecks_jan1_to_dec31_2024_with_urls.csv"
output_file = "politifact_personalities.csv"

# Function to determine if an author is a real person
def is_human_author(name):
    # Exclude generic sources like "social media", "Facebook posts", etc.
    if any(word in name.lower() for word in ["social media","viral image", "facebook", "twitter", "threads", "x", "tiktok", "instagram", "posts", "post"]):
        return False
    # Check if the name looks like a real person (has at least two words with letters)
    return bool(re.match(r"^[A-Za-z]+ [A-Za-z]+", name))

# Load the CSV data using pandas
df = pd.read_csv(input_file)

# Filter the DataFrame to only include rows with human authors in the source column
df_filtered = df[df['source'].apply(is_human_author)]

# Check if filtering has worked
print(f"Filtered rows:\n {df_filtered.head()}")

# Save the filtered DataFrame to a new CSV file
df_filtered.to_csv(output_file, index=False)

print(f"Extraction complete! {len(df_filtered)} rows with human authors saved to '{output_file}'.")
