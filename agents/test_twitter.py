import os, tweepy
from dotenv import load_dotenv
load_dotenv()

client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
)

try:
    me = client.get_me()
    print("BAGLANTI OK - Hesap: @" + me.data.username + " (" + me.data.name + ")")
    print("READY: Tweet atmaya hazir")
except Exception as e:
    print("HATA: " + str(e))
