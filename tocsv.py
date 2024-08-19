import json
import csv

# Function to read JSON data from a file
def load_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Function to save data to a CSV file
def save_to_csv(data, filename):
    # Define the CSV column headers
    headers = [
        "media_id",
        "title",
        "average_rating",
        "weighted_score",
        "new_weighted_score",
        "count",
        "rank"
    ]

    # Write to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for media_id, info in data.items():
            # Prepare row data
            row = {
                "media_id": media_id,
                "title": info.get("title", ""),
                "average_rating": info.get("average_rating", ""),
                "weighted_score": info.get("weighted_score", ""),
                "new_weighted_score": info.get("new_weighted_score", ""),
                "count": info.get("count", ""),
                "rank": info.get("rank", "")
            }
            writer.writerow(row)

# Load JSON data from file
media_data = load_from_json('updated_data.json')

# Save data to CSV file
save_to_csv(media_data, 'media_ratings.csv')

print("Data has been converted to 'media_ratings.csv'.")
