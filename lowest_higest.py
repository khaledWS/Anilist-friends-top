import json

def find_title_lowest_rank_with_highest_count(json_file):
    # Load JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    highest_count = -1
    lowest_rank = float('inf')
    title_with_lowest_rank = None
    
    # Iterate through the JSON entries
    for entry_id, entry in data.items():
        count = entry.get('count', 0)
        rank = entry.get('rank', float('inf'))
        title = entry.get('title', 'Unknown Title')
        
        # Update highest_count and lowest_rank
        if count > highest_count:
            highest_count = count
            lowest_rank = rank
            title_with_lowest_rank = title
        elif count == highest_count and rank < lowest_rank:
            lowest_rank = rank
            title_with_lowest_rank = title
    
    return title_with_lowest_rank

# Example usage
json_file = 'manga_ratings_4.json'
result = find_title_lowest_rank_with_highest_count(json_file)
print(f"The title with the lowest rank and highest count is: {result}")
