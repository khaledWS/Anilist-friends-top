import json

# Function to read JSON data from a file
def load_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Function to save JSON data to a file
def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Load the media ratings data from JSON file
media_data = load_from_json('media_ratings_FINAL.json')

# Sort media_data based on average_rating in descending order
sorted_media_data = dict(sorted(media_data.items(), key=lambda item: item[1].get('new_weighted_score', 0), reverse=True))

# Save the sorted media data back to JSON file
save_to_json(sorted_media_data, 'media_ratings_FINAL_order_avg.json')

print("Media ratings have been sorted by average rating and saved to 'media_ratings_FINAL.json.json'.")
