import json

def calculate_weighted_score(average_rating, num_ratings):

    return (average_rating * num_ratings / (num_ratings + 6.2) + 6.2 / (num_ratings + 6.2) * 7)

def main():
    # Load JSON data from a file
    with open('manga_ratings_fetched_3.json', 'r') as file:
        data = json.load(file)
    
    updated_data = {}
    
    for entry_id, entry in data.items():
        average_rating = entry['average_rating']
        num_ratings = len(entry['ratings'])
        if(num_ratings == 0):
            break
        
        # Calculate the new weighted score
        new_weighted_score = calculate_weighted_score(average_rating, num_ratings)
        
        # Create a new entry with updated information
        updated_entry = entry.copy()
        updated_entry['new_weighted_score'] = new_weighted_score
        updated_entry['count'] = num_ratings
        
        updated_data[entry_id] = updated_entry
    
    # Sort entries by the new weighted score in descending order
    sorted_entries = sorted(updated_data.items(), key=lambda item: item[1]['new_weighted_score'], reverse=True)
    
    # Assign ranks and convert sorted entries back to a dictionary
    sorted_data = {}
    for rank, (entry_id, entry) in enumerate(sorted_entries, start=1):
        entry['rank'] = rank
        sorted_data[entry_id] = entry
    
    # Write updated JSON data to a new file
    with open('manga_ratings_4.json', 'w') as file:
        json.dump(sorted_data, file, indent=4)

if __name__ == "__main__":
    main()
