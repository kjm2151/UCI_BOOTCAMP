# Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import tweepy
import time

# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Twitter API Keys
consumer_key = "B9zDsZD17rrpcsoUboPTO9MqM"
consumer_secret = "hpBYuMPoGBoMuSDmpMsnQEE4jC1jhUX1fYu327FC6hLILMWsDx"
access_token = "178789284-w1288VTQODRMmUc2IjKGY0095iq5PoKsSnwECR0c"
access_token_secret = "w5lr8Vtr9ssiLKfHnLYmjgcMhvKiYOhkVjNu4ERkUX6Tt"

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Target User
target_user = ["@CNNbrk", "@BBCWorld", "@FoxNews", "@CBSNews", "@nytimes"]
colors = []


# Counter
counter = 1

# Variables for holding sentiments
sentiments = []


# Loop through each target users
for i in range(0,len(target_user)):
    # Loop through 5 pages of tweets (total 100 tweets)
    for x in range(10):
    
        # Get all tweets from home feed
        public_tweets = api.user_timeline(target_user[i], page=(x+1))
    
        # Loop through all tweets 
        for tweet in public_tweets:
            counter = 0
            
            # Run Vader Analysis on each tweet
            compound = analyzer.polarity_scores(tweet["text"])["compound"]
            pos = analyzer.polarity_scores(tweet["text"])["pos"]
            neu = analyzer.polarity_scores(tweet["text"])["neu"]
            neg = analyzer.polarity_scores(tweet["text"])["neg"]
            tweets_ago = counter
            
            # Add sentiments for each tweet into an array
            sentiments.append({"Date": tweet["created_at"], 
                               "Compound": compound,
                               "Positive": pos,
                               "Negative": neu,
                               "Neutral": neg,
                               "Tweets Ago": tweets_ago})
            
            # Add to counter 
            counter = counter + 1
            
    # Convert sentiments to DataFrame
    sentiments_pd = pd.DataFrame.from_dict(sentiments)
    
    
    # Create plot
    plt.plot(np.arange(len(sentiments_pd["Compound"])),
             sentiments_pd["Compound"], marker="o", linewidth=0.5, linestyle = 'None',
             alpha=0.8)
    
    # # Incorporate the other graph properties
    plt.title("Sentiment Analysis of Tweets (%s) for %s" % (time.strftime("%x"), target_user[i]))
    plt.ylabel("Tweet Polarity")
    plt.xlabel("Tweets Ago")
    plt.show()

sentiment_cnn = []
sentiment_bbc = []
sentiment_fox = []
sentiment_cbs = []
sentiment_nyt = []



public_tweets = api.user_timeline(target_user[0], count=100, result_type="recent")
for tweet in public_tweets:
    # Run Vader Analysis on each tweet
    compound = analyzer.polarity_scores(tweet["text"])["compound"]
    tweets_ago = counter
        
    # Add sentiments for each tweet into an array
    sentiment_cnn.append({"Date": tweet["created_at"], 
                          "Compound": compound,
                          "Tweets Ago": tweets_ago})
        # Add to counter 
    counter = counter + 1

public_tweets = api.user_timeline(target_user[1], count=100, result_type="recent")
for tweet in public_tweets:
    # Run Vader Analysis on each tweet
    compound = analyzer.polarity_scores(tweet["text"])["compound"]
    tweets_ago = counter
        
    # Add sentiments for each tweet into an array
    sentiment_bbc.append({"Date": tweet["created_at"], 
                          "Compound": compound,
                          "Tweets Ago": tweets_ago})
        # Add to counter 
    counter = counter + 1
    
public_tweets = api.user_timeline(target_user[2], count=100, result_type="recent")
for tweet in public_tweets:
    # Run Vader Analysis on each tweet
    compound = analyzer.polarity_scores(tweet["text"])["compound"]
    tweets_ago = counter
        
    # Add sentiments for each tweet into an array
    sentiment_fox.append({"Date": tweet["created_at"], 
                          "Compound": compound,
                          "Tweets Ago": tweets_ago})
        # Add to counter 
    counter = counter + 1

public_tweets = api.user_timeline(target_user[3], count=100, result_type="recent")
for tweet in public_tweets:
    # Run Vader Analysis on each tweet
    compound = analyzer.polarity_scores(tweet["text"])["compound"]
    tweets_ago = counter
        
    # Add sentiments for each tweet into an array
    sentiment_cbs.append({"Date": tweet["created_at"], 
                          "Compound": compound,
                          "Tweets Ago": tweets_ago})
        # Add to counter 
    counter = counter + 1

public_tweets = api.user_timeline(target_user[4], count=100, result_type="recent")
for tweet in public_tweets:
    # Run Vader Analysis on each tweet
    compound = analyzer.polarity_scores(tweet["text"])["compound"]
    tweets_ago = counter
        
    # Add sentiments for each tweet into an array
    sentiment_nyt.append({"Date": tweet["created_at"], 
                          "Compound": compound,
                          "Tweets Ago": tweets_ago})
        # Add to counter 
    counter = counter + 1

sentiment_cnn_pd = pd.DataFrame.from_dict(sentiment_cnn)
sentiment_bbc_pd = pd.DataFrame.from_dict(sentiment_bbc)
sentiment_fox_pd = pd.DataFrame.from_dict(sentiment_fox)
sentiment_cbs_pd = pd.DataFrame.from_dict(sentiment_cbs)
sentiment_nyt_pd = pd.DataFrame.from_dict(sentiment_nyt)



avg_compound = (sentiment_cnn_pd["Compound"].mean(),
                sentiment_bbc_pd["Compound"].mean(),
                sentiment_fox_pd["Compound"].mean(),
                sentiment_cbs_pd["Compound"].mean(),
                sentiment_nyt_pd["Compound"].mean())

# Create dataframe to show avg compound value for each media
avg_comp_df = pd.DataFrame({'Media': target_user,
                           'avg_compound': avg_compound})
    
# Set x axis and tick locations
x_axis = np.arange(len(avg_comp_df))
tick_locations = [value+0.4 for value in x_axis]

# Create a list indicating where to write x labels and set figure size to adjust for space
plt.bar(x_axis, avg_comp_df["avg_compound"], color='r', alpha=0.5, align="edge")
plt.xticks(tick_locations, avg_comp_df["Media"], rotation="vertical")

# Set x and y limits
plt.xlim(-0.25, len(x_axis))
plt.ylim(min(avg_comp_df["avg_compound"])-0.05, max(avg_comp_df["avg_compound"])+0.05)

# Set a Title and labels
plt.title("Overall Media Sentiment based on Twitter %s" % (time.strftime("%x")))
plt.ylabel("Tweet Polarity")

plt.show()