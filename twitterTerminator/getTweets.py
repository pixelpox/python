from lxml import html
import requests
import mechanicalsoup
import json
from bs4 import BeautifulSoup
import sys
import csv

#https://www.pythoncircle.com/post/522/python-script-7-scraping-tweets-using-beautifulsoup/

def get_tweet_text(tweet):
    tweet_text_box = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    images_in_tweet_tag = tweet_text_box.find_all("a", {"class": "twitter-timeline-link u-hidden"})
    tweet_text = tweet_text_box.text
    for image_in_tweet_tag in images_in_tweet_tag:
        tweet_text = tweet_text.replace(image_in_tweet_tag.text, '')

    return tweet_text

def get_this_page_tweets(soup):
    tweets_list = list()
    tweets = soup.find_all("li", {"data-item-type": "tweet"})
    for tweet in tweets:
        tweet_data = None
        try:
            tweet_data = get_tweet_text(tweet)
        except Exception as e:
            continue
            #ignore if there is any loading or tweet error

        if tweet_data:
            tweets_list.append(tweet_data)
            print(".", end="")
            sys.stdout.flush()

    return tweets_list


def get_tweets_data(username, soup):
    tweets_list = list()
    tweets_list.extend(get_this_page_tweets(soup))

def ppGetIdsFromJSON(soup):
    tweets = soup.find_all("li")

    #1215713752894537728
    for tweet in tweets:
        print("\n================================")
        print(tweet.get('data-item-id'))
        if tweet.get('data-item-id') != None:
            print("tweet")
            ps = tweet.find_all('p')

            for p in ps:
               tweetText = p.get_text()
               if tweetText.find("REMINDER:") != -1:
                    print("DELETE")
            print(tweetText)
        print("\n================================")



def getMoreTweets(browser , twitterUsername):
    tweets_list = list()
    next_pointer = browser.get_current_page().find("div", {"class": "stream-container"})["data-min-position"]

    #nextpointer = '1221928376346333190'
    while True:
        next_url = "https://twitter.com/i/profiles/show/" + twitterUsername + \
                    "/timeline/tweets?include_available_features=1&" \
                    "include_entities=1&max_position=" + next_pointer + "&reset_error_state=false"

        next_response = None
        try:
            next_response = requests.get(next_url)
        except Exception as e:
            # in case there is some issue with request. None encountered so far.
            print(e)
            return tweets_list

        tweets_data = next_response.text
        tweets_obj = json.loads(tweets_data)
        if not tweets_obj["has_more_items"] and not tweets_obj["min_position"]:
            # using two checks here bcz in one case has_more_items was false but there were more items
            print("\nNo more tweets returned")
            break
        next_pointer = tweets_obj["min_position"]
        html = tweets_obj["items_html"]
        soup = BeautifulSoup(html, 'lxml')
        ppGetIdsFromJSON(soup)
        #tweets_list.extend(get_this_page_tweets(soup))

        return tweets_list


############################################################################################
twitterUsername = "shhmakers"
browser = mechanicalsoup.StatefulBrowser()
browser.open("https://twitter.com/"+twitterUsername)
page = browser.get_current_page()
#browser.launch_browser()
arrTweets = []

#example tweet to delete
##data-conversation-id="1227279969161818114"
#page 2 id 1221844145129578497
#another page 2 example 1220402122602225665


links = browser.get_current_page().find_all('a')

#get all tweet cards
tags = browser.get_current_page().findAll("div", class_="tweet")


for tag in tags:
    tweetId = tag.get('data-conversation-id')
    ps = tag.find_all('p')

    for p in ps:
        tweetText = p.get_text()
        if tweetText.find("REMINDER:") != -1:
            record = [tweetId, "DELETE" , tweetText]
        else:
            record = [tweetId, "" , tweetText]
        
        arrTweets.append(record)


#tweets_list = getMoreTweets(browser , twitterUsername)


with open('C:\\Users\\simon\\git\\python\\twitterTerminator\\tweets.csv', 'w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
    writer.writerows(arrTweets)