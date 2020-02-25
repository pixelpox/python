import tweepy
import os
import time
from dotenv import load_dotenv
load_dotenv()


print("hello")


#https://realpython.com/twitter-bot-python-tweepy/#how-to-make-a-twitter-bot-in-python-with-tweepy
#pip install tweepy
#pip install -U python-dotenv

#get api key and token from env file
apiKey = os.getenv("apiKey")
apiSecretKey = os.getenv("apiSecretKey")
accessToken = os.getenv("accessToken")
accessTokenSecret = os.getenv("accessTokenSecret")

# Authenticate to Twitter
auth = tweepy.OAuthHandler(apiKey, apiSecretKey)
auth.set_access_token(accessToken, accessTokenSecret)

# Create API object
api = tweepy.API(auth)

# Create a tweet
responce = api.update_status("Message will self destruct in 60 seconds")

#get responce id
print(responce.id)
print("sleep for 60 seconds")
time.sleep(60)
print("delete tweet")

#delete tweeted tweet from before
api.destroy_status(responce.id)


print("end")
