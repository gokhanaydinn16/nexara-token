import os, tweepy
from dotenv import load_dotenv
load_dotenv()

client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
)

tweet = """Nexara (NXR) is LIVE on Ethereum!

Stake $NXR to access the Superajan AI trading bot and earn revenue share.

- 2% burn on every transfer
- 12% APY staking
- Anti-whale protection
- 24/7 bot on Binance USD-M

Contract: 0xa14F7e4DE163Bc05297AF005B6cD44A770842187

nexara-token.netlify.app

#NXR #Nexara #DeFi #Ethereum #Crypto"""

try:
    resp = client.create_tweet(text=tweet)
    tid = resp.data["id"]
    print("TWEET ATILDI!")
    print("Link: https://x.com/NexaraNXR/status/" + str(tid))
except Exception as e:
    print("HATA: " + str(e))
