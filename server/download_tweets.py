# Twitter API credentials
import tweepy
import csv

def get_all_tweets(screen_name, count):
    consumer_key = ""
    consumer_secret = ""
    access_key = ""
    access_secret = ""

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    if screen_name[0] == "@":
        print("downloading tweets of " + screen_name)
        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name=screen_name, count=count, exclude_replies=True)
    else:
        print("downloading tweets releated to keywords " + screen_name)
        new_tweets = api.search(q=screen_name,lang="en", includes_entities=False, count=count)

    print("...%s tweets downloaded" % (len(new_tweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [tweet.text.encode("utf-8") for tweet in new_tweets]
    return outtweets
