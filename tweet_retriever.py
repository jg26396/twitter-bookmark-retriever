""" 
Write a python script that automatically retrieves all bookmarks from twitter, 
checks/retrieves all threads in those bookmarks,
Adds the retrieved tweets to a db with the rest of the tweets
"""

""" 
Function to return n number of most recent bookmarks and to also check if those bookmarks have threads
associated with them
"""

""" 
Code to search for a thread of tweets based on a conversation id and author id
"""
import json
import os
import pprint
import re
import time

import requests

from twitter_bookmark_remover import delete_bookmarks


def read_json_file(filename):
    """
    Reads a JSON file from the current working directory and returns its contents.

    :param filename: The name of the JSON file to be read.
    :return: A dictionary containing the data from the JSON file.
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"The file {filename} was not found in the current working directory.")
        return None
    except json.JSONDecodeError:
        print(f"The file {filename} is not a valid JSON file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def download_bookmarks(file_name_number, max_results=100):
    with open(
        "C:.\\Notebooks\\twitter_bookmarks_retriever_simple_test\\python\\data\\twitter_access_token.txt",
        "r",
    ) as file:
        access_token = file.read()

    file_name = ""
    try:
        url = f"https://api.twitter.com/2/users/1043947355953917952/bookmarks?user.fields=username,id,name&expansions=attachments.media_keys,author_id,referenced_tweets.id,edit_history_tweet_ids,entities.mentions.username,referenced_tweets.id.author_id,in_reply_to_user_id,geo.place_id,attachments.poll_ids&tweet.fields=text,public_metrics,conversation_id,referenced_tweets,created_at,attachments,context_annotations,note_tweet,entities&max_results={max_results}&media.fields=media_key,type,url,height,width,preview_image_url,public_metrics,variants&place.fields=full_name,id,country,country_code,place_type&poll.fields=duration_minutes,end_datetime,id,options,voting_status"

        payload = {}
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.request("GET", url, headers=headers, data=payload)
        bookmarks = json.loads(response.text)
        file_name = f"./Notebooks/twitter_bookmarks_retriever_simple_test/python/data/final_{file_name_number}_{len(bookmarks['data'])}_tweets_output.json"

        with open(
            file_name,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(bookmarks, file)

        return file_name

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")

    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")

    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")

    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

    return ""


def find_and_save_tweet_threads(
    tweets_path,
    threads_file_name=".\\Notebooks\\twitter_bookmarks_retriever_simple_test\\python\\data\\final_threads.json",
    # max_results=100,
    index=None,
):
    bookmarks = read_json_file(tweets_path)

    threads = []
    tweets = 0
    if index == None:
        index = 0

    for bookmark in bookmarks["includes"]["tweets"][index:]:
        conv_id = bookmark["conversation_id"]
        author_id = bookmark["author_id"]
        tweets += 1
        print(conv_id, author_id)

        try:
            url = f"https://api.twitter.com/2/tweets/search/recent?max_results=100&query=conversation_id:{conv_id} from:{author_id} to:{author_id}&user.fields=username,id,name&expansions=attachments.media_keys,author_id,referenced_tweets.id,edit_history_tweet_ids,entities.mentions.username,referenced_tweets.id.author_id,in_reply_to_user_id,geo.place_id,attachments.poll_ids&tweet.fields=text,public_metrics,conversation_id,referenced_tweets,created_at,attachments,context_annotations,note_tweet,entities&media.fields=media_key,type,url,height,width,preview_image_url,public_metrics,variants&place.fields=full_name,id,country,country_code,place_type&poll.fields=duration_minutes,end_datetime,id,options,voting_status"

            payload = {}
            headers = {"Authorization": f"Bearer {bearer_token}"}

            response = requests.request("GET", url, headers=headers, data=payload)
            response.raise_for_status()
            thread = response.json()

            if thread["meta"]["result_count"] == 0:
                print("no thread found!")
                continue

            threads.append(
                {
                    "author_id": author_id,
                    "conversation_id": conv_id,
                    "data": thread["data"],
                    "includes": thread["includes"],
                    "meta": thread["meta"],
                }
            )
            time.sleep(0.5)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            break
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
            break
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
            break
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            break

    with open(threads_file_name, encoding="utf-8") as file:
        print(f"opening file: {threads_file_name} and reading the contents")
        threads_final = json.load(file)

    print(f"the number of threads currently stored are: {len(threads_final)}")
    print(f"the number of threads extracted from {tweets_path} is: {len(threads)}")

    threads_final.extend(threads)
    print(f"the number of threads going to be stored are: {len(threads_final)}")

    with open(threads_file_name, "w") as json_file:
        json.dump(threads_final, json_file)

    print(f"the updated number of threads currently stored are: {len(threads_final)}")

    return tweets


def retrieve_tweets_from_file(file_path_number, folder_path=None):
    if folder_path != None:
        # List all JSON files in the directory
        json_files = [
            file for file in os.listdir(folder_path) if file.endswith(".json")
        ]

        # Initialize a list to hold your JSON data
        data = []

        # Loop through the JSON files
        for file_name in json_files:
            # Create the full file path
            file_path = os.path.join(folder_path, file_name)

            # Open and read the JSON file
            with open(file_path, "r") as file:
                # Parse the JSON data and add it to the list
                data.append(json.load(file))

        # Now 'data' is a list of the parsed JSON from each file
        return data

    elif file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    else:
        return "No file was passed"


def download_twitter_videos(folder_path, tweet_id="twitter_video"):
    # URL of the Twitter video
    video_url = "https://video.twimg.com/amplify_video/1743459403817431040/vid/avc1/590x1280/1LP4Ka7hqWY5EVis.mp4?tag=14"

    # Sending a GET request to download the video
    response = requests.get(video_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the video to a file
        with open(f"./{folder_path}/{tweet_id}.mp4", "wb") as file:
            file.write(response.content)
        print("Video downloaded and saved successfully.")
    else:
        print(f"Failed to download the video. Status code: {response.status_code}")


def main():
    # Extracts the list of files that contain tweets and returns the last one in the list
    json_files = [
        file
        for file in os.listdir(
            "./Notebooks/twitter_bookmarks_retriever_simple_test/python/data"
        )
        if file.endswith(".json")
    ]
    pattern = re.compile(r"final_(\d+)_\d+_tweets_outputs?\.json")
    filtered_and_sorted_files = sorted(
        [f for f in json_files if pattern.match(f)],
        key=lambda x: int(pattern.match(x).group(1)),
    )

    file_name_number = input(
        f"Please enter the file number you would like to associate with the downloaded bookmarks\nThe previous most recent file name is: {filtered_and_sorted_files[-1]}\n\nPlease enter file name here:"
    )
    print("The file number you chose is: " + file_name_number)
    tweets_path = download_bookmarks(file_name_number=file_name_number)
    if tweets_path != "":
        print("Tweets successfully extracted from bookmarks")
        tweets_parsed = find_and_save_tweet_threads(tweets_path=tweets_path)

        checker = input("Would you like to delete your current bookmarks?: ")

        if checker == "yes":
            count = input("How many would you like to delete?: ")
            delete_bookmarks(delete=count)
            print("Done!")
        else:
            print("Done!")
    else:
        print("An error occured and no tweets were saved")


if __name__ == "__main__":
    main()
