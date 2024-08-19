import requests
import re
import json
import time

def extract_user_tag(url):
    match = re.search(r"https://anilist.co/user/([^/]+)", url)
    if match:
        return match.group(1)
    return None

    url = "https://graphql.anilist.co"
    
    query = """
    query getUserData($name: String) {
      User(name: $name) {
        id
        name
        mediaListOptions {
          scoreFormat
        }
      }
    }
    """
    
    variables = {
        "name": user_tag
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Query failed to run with a {response.status_code} status code. {response.text}")

    data = response.json()
    
    user = data.get('data', {}).get('User', {})
    return {
        "id": user.get('id'),
        "name": user.get('name'),
        "scoreFormat": user.get('mediaListOptions', {}).get('scoreFormat')
    }

def fetch_user_data(username, retries=10):
    """
    Fetch the user ID by username using AniList GraphQL API.
    
    :param username: The username of the AniList user.
    :param retries: Number of retries on failure.
    :return: The user ID of the AniList user.
    """
    url = "https://graphql.anilist.co"
    query = """
    query getUserData($name: String) {
        User(name: $name) {
            id
            name
            mediaListOptions {
                scoreFormat
            }
        }
    }
    """
    
    variables = {
        "name": username
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    for attempt in range(retries):
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            user_data = data['data']['User']
            if user_data:
                return {
                    "id": user_data['id'],
                    "name": user_data['name'],
                    "scoreFormat": user_data['mediaListOptions']['scoreFormat']
                }
        elif response.status_code == 429:
            print("Rate limit exceeded, retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            raise Exception(f"Query failed to run with a {response.status_code} status code. {response.text}")
    
    raise Exception(f"Failed to fetch user ID after {retries} attempts.")

def fetch_user_media_list(user_id, page=1, retries=10):
    """
    Fetch the media list for a given user from AniList API with retry mechanism.
    
    :param user_id: The ID of the user to fetch the media list for.
    :param page: The page number for pagination (default is 1).
    :param retries: Number of retries on failure.
    :return: List of media items with their ratings.
    """
    url = "https://graphql.anilist.co"
    query = """
    query getAnimeListById($userId: Int, $page: Int) {
        Page(page: $page, perPage:50) {
            mediaList(userId: $userId, type: ANIME) {
                id
                media {
                    id
                    title {
                        english
                    }
                }
                status
                score(format: POINT_10_DECIMAL)
            }
        }
    }
    """
    
    variables = {
        "userId": user_id,
        "page": page
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    for attempt in range(retries):
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            time.sleep(2 ** attempt)  # Exponential backoff
            return data['data']['Page']['mediaList']
        elif response.status_code == 429:
            print("Rate limit exceeded, retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            raise Exception(f"Query failed to run with a {response.status_code} status code. {response.text}")
    
    raise Exception(f"Failed to fetch media list after {retries} attempts.")


def process_urls(urls):
    results = []
    
    for url in urls:
        user_tag = extract_user_tag(url)
        if user_tag:
            user_data = fetch_user_data(user_tag)
            results.append(user_data)
    
    return results

    
    url = "https://graphql.anilist.co"
    
    query = """
    query getAnimeListById($userId: Int, $page: Int) {
        Page(page: $page) {
            mediaList(userId: $userId, status: COMPLETED, sort: SCORE_DESC, type: ANIME) {
                id
                media {
                    title {
                        english
                    }
                }
                score(format: POINT_10_DECIMAL)
            }
        }
    }
    """
    
    variables = {
        "userId": user_id,
        "page": page
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Query failed to run with a {response.status_code} status code. {response.text}")

    data = response.json()
    
    # Extract media list from the response
    return data['data']['Page']['mediaList']

def process_media_lists(user_ids):
    
    media_ratings = {}
    
    for user_id in user_ids:
        page = 1
        while True:
            print(user_id)
            media_list = fetch_user_media_list(user_id, page)
            
            if not media_list:
                break  # No more pages, exit the loop
            
            for item in media_list:
                media_id = item['media']['id']
                score = item.get('score')  # Get the score, default to None if missing
                media_title = item['media']['title']['english']
                status = item.get('status')
                
                if score is not None and score != "" and score != 0 and status !="PLANNING":
                    if media_id not in media_ratings:
                        media_ratings[media_id] = {
                            "title": media_title,
                            "ratings": []
                        }
                    
                    media_ratings[media_id]["ratings"].append(score)
            
            page += 1
    
    return media_ratings

import requests
import time

def fetch_user_manga_list(user_name, page=1, retries=10):
    """
    Fetch the media list for a given user from AniList API with retry mechanism.
    
    :param user_name: The username of the user to fetch the media list for.
    :param page: The page number for pagination (default is 1).
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
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            time.sleep(2 ** attempt)  # Exponential backoff
            return [entry for lst in data['data']['MediaListCollection']['lists'] for entry in lst['entries']]
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
    user_data = []
    user_ids = []
    
    for url in urls:
        username = extract_user_tag(url)
        if username:
            user_info = fetch_user_data(username)
            if user_info:
                user_data.append(user_info)
                user_ids.append(user_info['id'])
    
    media_data = process_media_lists(user_ids)
    
    # Optionally, calculate average ratings
    for media_id, info in media_data.items():
        if info['ratings']:
            num_ratings = len(info['ratings'])
            average_rating = sum(info['ratings']) / len(info['ratings'])
            info['average_rating'] = average_rating
            weighted_score = average_rating * num_ratings/(num_ratings+5) + 5/(num_ratings+5) * 4.1
            info['weighted_score'] = weighted_score
        else:
            info['average_rating'] = None
    
    # sorted_media_data = dict(sorted(media_data.items(), key=lambda item: item[1].get('average_rating', 0), reverse=True))
    sorted_media_data = dict(sorted(media_data.items(), key=lambda item: item[1].get('weighted_score', 0), reverse=True))
    # Save user data and media ratings to JSON files
    save_to_json(user_data, 'user_data_FINAL_2.json')
    save_to_json(sorted_media_data, 'media_ratings_new_formela_FINAL_2.json')
    
    print("User data has been saved to user_data.json")
    print("Media ratings have been saved to media_ratings.json")

if __name__ == "__main__":
    urls = [
    
    ]  # Example URLs; replace with actual user URLs
    main(urls)

# Example URLs

    # Add more URLs as needed












# query = '''
# query ($id: Int, $page: Int, $perPage: Int, $search: String) {
#     Page (page: $page, perPage: $perPage) {
#         pageInfo {
#             total
#             currentPage
#             lastPage
#             hasNextPage
#             perPage
#         }
#         media (id: $id, search: $search) {
#             id
#             title {
#                 romaji
#             }
#         }
#     }
# }
# '''
# variables = {
#     'search': 'Fate/Zero',
#     'page': 1,
#     'perPage': 3
# }
# url = 'https://graphql.anilist.co'

# response = requests.post(url, json={'query': query, 'variables': variables});

# # Check if the request was successful
# if response.status_code == 200:
#     # Print the JSON response
#     print("Response JSON:")
#     print(response.json())
# else:
#     # Print the error message
#     print(f"Request failed with status code {response.status_code}")
#     print(response.text)






    #1 - collect users rating system and ids based on usernames
    #2 - go over every user media list and collect every media_id and score (convert the score to the needed system based on the system of the user we are collecting)
    #3 - the way you should store the data while collecting it in step 2 is if the media already exists add the new rating, else add a new media and a rating
    #4 - after collecting all ratings from all users get the avg, median for  every media in the media collection
    #5 - get the top 10 rated media and the bottom 10 rated media
#     query getManga ($user: String)  { 
#     MediaListCollection(userName: $user type: MANGA){  
#       lists {
#        entries {
#           id
#           media {
#             id
#             title {
#             english
#             romaji
#             }
#           }
#         status
#         score(format: POINT_10_DECIMAL)
#         }
      
#       }
#     }
#   }