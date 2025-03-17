import pandas as pd

# Load the data from the CSV file
data = pd.read_csv('politifact_factchecks_jan1_to_dec31_2024_with_urls.csv')

# Group the data by 'source' and count the number of posts for each source
source_counts = data.groupby('source').size()

# Sort the sources by the number of posts in descending order and get the top 10
top_10_sources = source_counts.sort_values(ascending=False).head(10)

# Group the data by 'rating' and count the number of posts for each rating
rating_counts = data.groupby('rating').size()

# Sort the ratings by the number of posts in descending order and get the top 10
top_10_ratings = rating_counts.sort_values(ascending=False).head(10)

# Group by 'rating' and 'source' and count the number of posts for each combination
source_rating_counts = data.groupby(['rating', 'source']).size().reset_index(name='count')

# Sort the results by rating and count in descending order
source_rating_counts_sorted = source_rating_counts.sort_values(by=['rating', 'count'], ascending=[True, False])

# For each rating, get the top 10 sources
top_10_sources_by_rating = source_rating_counts_sorted.groupby('rating').head(10)

# Output the results
print("Top 10 sources for each rating:")

# Loop over each rating to display top 10 sources
for rating in top_10_sources_by_rating['rating'].unique():
    print(f"\nRating: {rating}")
    rating_data = top_10_sources_by_rating[top_10_sources_by_rating['rating'] == rating]
    print(rating_data[['source', 'count']])
    print("-" * 40)


# Output the results
print("Top 10 sources with the most posts:")
print(top_10_sources)
print("-" * 20)
print("Top 10 ratings by the number of fact-check posts:")
print(top_10_ratings)
