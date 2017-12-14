# Dependencies
import pandas as pd
import matplotlib.pyplot as plt
import json
import tweepy
import seaborn as sns

# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Twitter API Keys
consumer_key = <>
consumer_secret = <>
access_token = <>
access_token_secret = <>

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Target User
news_org = ["@CNNbrk", "@BBCWorld", "@FoxNews", "@CBSNews", "@nytimes"]

post_sentiment = []

for news in news_org:
    counter = 1
    for item in tweepy.Cursor(api.user_timeline, id=news).items(100):
        tweet = json.dumps(item._json, indent=3)
        tweet = json.loads(tweet)
        text = tweet['text']
        compound = analyzer.polarity_scores(text)["compound"]
        pos = analyzer.polarity_scores(text)["pos"]
        neu = analyzer.polarity_scores(text)["neu"]
        neg = analyzer.polarity_scores(text)["neg"]
        news_dict = {
                'source':news,
                'date': tweet["created_at"],
                'text': text,
                'compound': compound,
                'positive': pos,
                'negative': neg,
                'tweets ago': counter
                }
        post_sentiment.append(news_dict)
        counter += 1


df = pd.DataFrame.from_dict(post_sentiment)
print(df.head())


fg = sns.FacetGrid(data=df, hue='source', aspect=2, size=5)
fg.map(plt.scatter, 'tweets ago', 'compound').add_legend()
plt.xlabel('Tweets Ago')
plt.ylabel('Tweet Polarity')
plt.show()
print("Most of tweets from all 5 media stayed around compound score 0.")

media_df = df.set_index('source')

for i in range(0,len(news_org)):
    fg = sns.FacetGrid(data=media_df.loc[news_org[i]], aspect=2, size=5)
    fg.map(plt.scatter, 'tweets ago', 'compound')
    plt.title("Sentiment Analysis of Tweets (%s) for %s" % (time.strftime("%x"), news_org[i]))
    plt.xlabel('Tweets Ago')
    plt.ylabel('Tweet Polarity')
    plt.show()

df_groupby = df.groupby('source').mean()
df_groupby.reset_index(inplace=True)
print(df_groupby)


sns.barplot(data=df_groupby, x='source', y='compound')
plt.show()
print("All five major medias we analyzed returned negative compound score which indicates that")
print("There were more negative events rather than positive event around the world.")
print("However even though the score was negative,")
print("all media kept their negativity around and below -0.10.")

