import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from random import randint

# Path to your ChromeDriver
chrome_driver_path = r"C:\Users\Jonah\Research\WebDriver\chromedriver-win64\chromedriver.exe"

# Setup headless Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment if you want headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the Service object with the ChromeDriver path
service = Service(executable_path=chrome_driver_path)

# Initialize the driver with the specified Service and options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Path to the cookies file
cookies_file_path = "cookies1.json"

# Function to load cookies
def load_cookies(driver, cookies_file_path):
    if os.path.exists(cookies_file_path):
        with open(cookies_file_path, 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)

# Function to save cookies
def save_cookies(driver, cookies_file_path):
    cookies = driver.get_cookies()
    with open(cookies_file_path, 'w') as file:
        json.dump(cookies, file)

# Ensure "comments" folder exists
if not os.path.exists("comments"):
    os.makedirs("comments")

# Load cookies before navigating to the login page
driver.get("https://x.com")  # Navigate to the main page to set the domain for cookies
time.sleep(3)  # Wait for the page to load

# Load cookies if they exist
load_cookies(driver, cookies_file_path)

# Refresh to apply the loaded cookies
driver.get("https://x.com")  # Refresh to apply cookies

try:
    # Check if cookies were loaded and attempt to login
    if driver.get_cookie("auth_token") or driver.get_cookie("kdt") or driver.get_cookie("twid"):
        print("Already logged in!")
    else:
        # Navigate to the login page
        driver.get("https://x.com/login")  
        time.sleep(3)  # Wait for the page to load

        # Wait for the username field to be present and send keys
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username_field.send_keys("JohnMitche12483")  # Enter your username

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']/.."))
        )
        next_button.click()  # Click the "Next" button

        # Wait for the password field to be present
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys("EnsureSafe87!!")  # Enter your password

        login = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']/.."))
        )
        login.click()  # Click the "Log in" button
        
        time.sleep(2)  # Wait for the login process to complete
        
        # Save cookies after successful login
        save_cookies(driver, cookies_file_path)  
        
except Exception as e:
    print(f"An error occurred during login: {e}")

# After logging in and navigating to the post
with open("tweets.txt", "r") as file:
    urls = [line.strip() for line in file]
time.sleep(3)  # Wait for the post to load

for i, url in enumerate(urls):
    url = url.strip()  # Remove any trailing spaces or newlines

    # Navigate to each post
    driver.get(url)
    time.sleep(5)  # Wait for the post to load

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, ".//div[@data-testid='tweetText']")))
    
    # Locate all comment divs by their data-testid attribute
        comment_divs = driver.find_elements(By.XPATH, ".//div[@data-testid='tweetText']")

        comments = []
        for comment_div in comment_divs:
            # Directly extract the text from the comment div
            comment_text = comment_div.text.replace('\n', ' ')
            if comment_divs.index(comment_div) != 0:  # Skip the original tweet
                comments.append(comment_text)

        # Limit to 50 comments if more than that are found
        comments = comments[:50]

        # Save all comments for this URL in one CSV filet
        column_headers = [f"Comment {i+1}" for i in range(len(comments))]
        
        # Save each comment as its own CSV file
        df = pd.DataFrame([comments], columns=column_headers)
        
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        username = path_parts[0]
        random_number = randint(1, 1000)

        # Save the CSV with a unique name (based on the username) in the "comments" folder
        csv_filename = os.path.join("comments", f"{username}--{random_number}_comments.csv")
        df.to_csv(csv_filename, index=False)

        tweets_df = pd.read_csv("tweets.csv")
        tweets_df.loc[tweets_df['URL to tweet'] == url, 'comment_file'] = csv_filename
        tweets_df.to_csv("tweets.csv", index=False)

        print(f"Saved {len(comments)} comments to {csv_filename}")
    except Exception as e:
        print(f"An error occurred for {url}: {e}")

# Quit the driver
driver.quit()