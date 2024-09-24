Twitter Scraping Script
Overview
This Python script allows users to scrape tweets from specified links, gather user details, and save tweet media files. The script uses asynchronous programming for efficient data fetching and stores the collected data in a CSV file. It also tracks user activity by calculating the posting frequency based on account age.

Features
Login to Twitter and manage session cookies.
Scrape tweets and associated user data from provided links.
Download media (images/videos) associated with the tweets.
Store the collected data in a structured CSV format.
Automatically calculate posting frequency based on user account age.
Requirements
Before running the script, ensure you have the following Python packages installed:

aiohttp
pandas
twikit
You can install the required packages using pip:

bash
Copy code
pip install aiohttp pandas twikit
Setup
Clone the Repository: Clone this repository to your local machine.

bash
Copy code
git clone <repository-url>
cd <repository-directory>
Twitter Credentials: Replace the placeholder values for auth_info_1 and password in the script with your actual Twitter username and password.

Cookies Management: The script will create a cookies.json file to save your session cookies. The next time you run the script, it will load the cookies instead of prompting for login.

Input Text File: Prepare a text file containing the URLs of the tweets you wish to scrape. Each URL should be on a new line.

Usage
To run the script, use the following command:

bash
Copy code
python <script-name>.py
You will be prompted to enter the name of the text file containing the tweet links. Make sure the file is in the same directory as the script or provide the full path to the file.

Example Input File (tweets.txt)
ruby
Copy code
https://twitter.com/user/status/1234567890123456789
https://twitter.com/user/status/9876543210987654321
Output
CSV File: The script will generate a tweets.csv file containing the following columns:

Post ID
URL to tweet
Creation date
Likes
Caption
Retweet count
Comment count
View count
Poster handle
Poster display name
Poster follower count
Poster frequency
Total posts
Hashtags
Image filename
Media Files: All downloaded media files will be saved in a directory named twitter_media.

Important Notes
Ensure that your Twitter account has permission to access the tweets you want to scrape.
Be aware of Twitter's rate limits and policies regarding data scraping.
Avoid sharing your Twitter credentials and cookies.json file publicly.
License
This project is licensed under the MIT License.

Contributing
If you'd like to contribute to this project, feel free to submit a pull request or open an issue for discussion.

Feel free to modify any sections or add additional details based on your specific needs!
