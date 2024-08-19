import json

# Function to read JSON data from a file
def load_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Function to save data to a text file with UTF-8 encoding
def save_to_text(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            media_id, info = item
            title = info.get('title', 'No Title')
            rank = info.get('rank', 'No Rank')
            f.write(f"{title} (Rank: {rank})\n")

# Load the media ratings data from JSON file
media_data = load_from_json('manga_ratings_4.json')

# Sort media_data based on new_weighted_score in descending order
sorted_media_data = sorted(media_data.items(), key=lambda item: item[1].get('new_weighted_score', 0), reverse=True)

# Save sorted media data with titles and ranks to a new text file
save_to_text(sorted_media_data, 'manga_ratings_4_text.txt')

print("Media data with titles and ranks has been sorted by new_weighted_score and saved to 'manga_ratings_4_text.txt'.")
