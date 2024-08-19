import json

# Function to load JSON data from a file
def load_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Function to calculate the average rating across the dataset
def calculate_average_rating(media_data):
    total_ratings = []
    
    # Collect all ratings from each media item
    for media_id, info in media_data.items():
        ratings = info.get('ratings', [])
        total_ratings.extend(ratings)
    
    # Compute the average rating
    if total_ratings:
        average_rating = sum(total_ratings) / len(total_ratings)
        return average_rating
    else:
        return None  # No ratings available

# Load the media ratings data from JSON file
media_data = load_from_json('manga_ratings_fetched_3.json')

# Calculate the average rating
average_rating = calculate_average_rating(media_data)

if average_rating is not None:
    print(f"The average rating across the dataset is: {average_rating:.2f}")
else:
    print("No ratings available to calculate the average.")
