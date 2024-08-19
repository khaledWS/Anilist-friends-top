import requests
import re
import json
import time
import os

def extract_user_tag(url):
    match = re.search(r"https://anilist.co/user/([^/]+)", url)
    if match:
        return match.group(1)
    return None

import requests
import time

def fetch_user_media_list(user_name, retries=10):
    """
    Fetch the media list for a given user from AniList API with retry mechanism.
    
    :param user_name: The username of the user to fetch the media list for.
    :param retries: Number of retries on failure.
    :return: List of media items with their ratings.
    """
    url = "https://graphql.anilist.co"
    query = """
    query getManga($userName: String) {
        MediaListCollection(userName: $userName, type: MANGA) {
            lists {
                entries {
                    id
                    media {
                        id
                        title {
                            english
                            romaji
                        }
                    }
                    status
                    score(format: POINT_10_DECIMAL)
                }
            }
        }
    }
    """
    
    variables = {
        "userName": user_name
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    for attempt in range(retries):
        print (user_name)
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            time.sleep(2 ** attempt)  # Exponential backoff
            
            # Flatten the entries from lists
            media_entries = [entry for lst in data['data']['MediaListCollection']['lists'] for entry in lst['entries']]
            
            # Prioritize English title, fallback to Romaji
            for entry in media_entries:
                media = entry['media']
                if not media['title']['english']:
                    media['title']['english'] = media['title']['romaji']
                    
            return media_entries
        
        elif response.status_code == 429:
            print("Rate limit exceeded, retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff
        
        else:
            raise Exception(f"Query failed to run with a {response.status_code} status code. {response.text}")
    
    raise Exception(f"Failed to fetch media list after {retries} attempts.")

def save_to_json(data, filename):

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)



def main(urls):
    user_names = []

    # Extract usernames from URLs
    for url in urls:
        username = extract_user_tag(url)
        if username:
            user_names.append(username)
    
    media_data = {}
    
    # Fetch media data for each user
    for username in user_names:
        user_media = fetch_user_media_list(username)
        
        
        for item in user_media:
            media_id = item['media']['id']
            score = item.get('score')
            status = item.get('status')
            if media_id not in media_data:
                media_data[media_id] = {
                    'title': item['media']['title'].get('english') or item['media']['title'].get('romaji'),
                    'ratings': []
                }
            if score is not None and score != "" and score != 0 and status !="PLANNING":
                media_data[media_id]['ratings'].append(item['score'])
            
    
    # Calculate average ratings and weighted scores
    for media_id, info in media_data.items():
        if info['ratings']:
            num_ratings = len(info['ratings'])
            average_rating = sum(info['ratings']) / num_ratings
            info['average_rating'] = average_rating
            weighted_score = average_rating * num_ratings / (num_ratings + 5) + 5 / (num_ratings + 5) * 4.1
            info['weighted_score'] = weighted_score
        else:
            info['average_rating'] = None
    
    # Sort media data by weighted score
    sorted_media_data = dict(sorted(media_data.items(), key=lambda item: item[1].get('weighted_score', 0), reverse=True))
    
    # Save data to JSON files
    # save_to_json(user_names, 'user_names_ma_FINAL.json')  # Save the extracted usernames
    save_to_json(sorted_media_data, 'manga_ratings_fetched_3.json')
    
    # print("Usernames have been saved to user_names_FINAL.json")
    print("Media ratings have been saved to manga_ratings_fetched_3.json")

if __name__ == "__main__":
    urls = [
    
    ]  # Example URLs; replace with actual user URLs
    main(urls)