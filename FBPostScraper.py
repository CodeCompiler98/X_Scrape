import os
import re
import pandas as pd
from facebook_scraper import get_posts
from urllib.parse import urlparse

def scrape_facebook(fb_links, csv_file='posts.csv'):
    fb_posts_to_store = []

    for link in fb_links:
        parsed_url = urlparse(link)
        path_parts = parsed_url.path.strip('/').split('/')
        post_id = path_parts[-1]

        for post in get_posts(post_urls=[link], options={"comments": True, "progress": True}):
            
            # Save comments to a file
            comment_filename = f"fb_comments_{post_id}.txt"
            with open(comment_filename, 'w', encoding='utf-8') as f:
                for comment in post['comments_full']:
                    f.write(comment['comment_text'] + "\n")

            # Store the post information
            fb_posts_to_store.append({
                'Post ID': post['post_id'],
                'URL to tweet': link,
                'creation_date': post['time'],
                'likes': post['likes'],
                'caption': post['text'].replace('\n', ' ') if post['text'] else '',
                'retweet_count': post['shares'],
                'comment_count': post['comments'],
                'view_count': post['views'] if 'views' in post else None,
                'poster_handle': post['username'],
                'poster_display_name': post['user_name'],
                'poster_follower_count': None,  # Not available in facebook-scraper
                'poster_frequency': None,  # Not available in facebook-scraper
                'total_posts': None,  # Not available in facebook-scraper
                'hashtags': ', '.join(re.findall(r'#\w+', post['text'])) if post['text'] else '',
                'image_filename': None,  # Not handled in this example
                'comment_file': comment_filename
            })

    # Make the data into a pandas dataframe and store it as a CSV file
    df = pd.DataFrame(fb_posts_to_store)

    # Check if the CSV file already exists
    if os.path.isfile(csv_file):
        df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file, mode='w', header=True, index=False)

    print(df.sort_values(by='likes', ascending=False))

if __name__ == "__main__":
    # Example usage
    fb_links = [
        "https://www.facebook.com/USER/posts/POST_ID",
    ]
    scrape_facebook(fb_links)