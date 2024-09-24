import asyncio
import os
import re
import aiohttp
from twikit import Client
import pandas as pd
from urllib.parse import urlparse
from datetime import datetime, timezone

async def main():
    #login to twitter or load session if already active
    client = Client('en-US')

    if os.path.exists('cookies.json'):
        print('Loading Cookies...')
        # Load cookies if the file exists
        client.load_cookies(path='cookies.json')
    else:
        # Login and save cookies if the file does not exist
        print('Logging in...')
        await client.login(
            auth_info_1='JohnMitche12483',
            password='EnsureSafe87!!',
        )
        client.save_cookies('cookies.json')

    # Inquire from the user for a text document name
    text_file = input("Enter the name of the text file: ")

    # Open the text file
    with open(text_file, 'r') as file:
        tweet_links = file.readlines()

    # Save the tweet links from the file in a list
    tweet_links = [link.strip() for link in tweet_links]

    tweets_to_store = []

    #loop through each link and collect data
    for link in tweet_links:
        # Parse the user handle and tweet ID from the link
        parsed_url = urlparse(link)
        path_parts = parsed_url.path.strip('/').split('/')
        user_handle = path_parts[0]
        tweet_id = path_parts[-1]

        # Fetch the user details
        user = await client.get_user_by_screen_name(user_handle)

        # Parse the account creation date for later
        user_created_at = datetime.strptime(user.created_at, '%a %b %d %H:%M:%S %z %Y')

        # Calculate ghe posting frequency
        account_age_days = (datetime.now(timezone.utc) - user_created_at).days
        posting_frequency = user.statuses_count / account_age_days if account_age_days > 0 else 0

        # Fetch the tweet details
        tweet = await client.get_tweet_by_id(tweet_id)

        #get the tweet creation date for later
        tweet_created_at = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S %z %Y')

        # Grab tweet media
        async with aiohttp.ClientSession() as session:
            for i, media in enumerate(tweet.media):
                media_url = media.get('media_url_https')
                extension = media_url.rsplit('.', 1)[-1]

                async with session.get(media_url) as response:
                    content = await response.read()

                # Create the directory if it doesn't exist
                os.makedirs('twitter_media', exist_ok=True)

                # Format the filename
                created_at_str = tweet_created_at.strftime('%Y-%m-%d-%H-%M-%S')
                filename = f'twitter_media/{tweet.user.screen_name}_{created_at_str}_{i}.{extension}'

                # Save the media file
                with open(filename, 'wb') as f:
                    f.write(content)  # Ensure binary data is written

        # Parse hashtags from the tweet
        full_text = tweet.full_text
        hashtags = []
        words = full_text.split()
        for word in words:
            if word.startswith('#'):
                hashtags.append(word)

        # Store the tweet information
        tweets_to_store.append({
            'Post ID': tweet.id,
            'URL to tweet': link,
            'creation_date': tweet.created_at,
            'likes': tweet.favorite_count,
            'caption': full_text.replace('\n', ' '),
            'retweet_count': tweet.retweet_count,
            'comment_count': tweet.reply_count,
            'view_count': tweet.view_count,
            'poster_handle': user.screen_name,
            'poster_display_name': user.name,
            'poster_follower_count': user.followers_count,
            'poster_frequency': posting_frequency,
            'total_posts': user.statuses_count,
            'hashtags': ', '.join(hashtags),
            'image_filename': filename
        })

    # Make the data into a pandas dataframe and store it as a CSV file
    df = pd.DataFrame(tweets_to_store)
    csv_file = 'tweets.csv'

    # Check if the CSV file already exists
    if os.path.isfile(csv_file):
        df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file, mode='w', header=True, index=False)
    print(df.sort_values(by='likes', ascending=False))

# Run main 
asyncio.run(main())