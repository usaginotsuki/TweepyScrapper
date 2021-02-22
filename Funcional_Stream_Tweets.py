import tweepy
import json
from pymongo import MongoClient
from tweepy import StreamListener

consumer_key="wTLFTGNSJWn15NGzUFbXLIc3g"
consumer_key_secret="baHOUMlet7QhOUiatcwBPg8uCAzjVanZxl5NJt0ByErkDVyfCY"
access_token="4138078402-kSFVjvbGPrm5TeCO3Ldz4b0jg7muQc7MxBReC0L"
access_token_secret="0uvKDNBD5tAt9WgFB6PmcfdmjcYdFG1r8rxRnPqFEGch8"

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)

auth.set_access_token(access_token, access_token_secret)

api=tweepy.API(auth, wait_on_rate_limit=True,
               wait_on_rate_limit_notify=True)

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
dblist=client.list_database_names()
if "tweets" in dblist:
    print("Ya existe la base de datos")
    db=client.tweets
else:
    db=client['tweets']
db = client.tweets
collection = db['Stream1']
print("Connection")


"""
data=(tweepy.Cursor(api.user_timeline, screen_name="FFAAECUADOR", tweet_mode="extended", lang="es").items(0))
i=0
for user in data:

    datajson=json.dumps(user._json,indent=2)
    datajson=json.loads(datajson)
    print(user._json['full_text'])
    print("\n---------------\n")
    db.tweets.insert_one(datajson)

print(i)
"""

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(json.dumps(status._json,indent=2))
        tweet=json.dumps(status._json, indent=2)
        tweet=json.loads(tweet)
        print(tweet)
        db.stream.insert_one(tweet)



myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode="extended")
myStream.filter(follow=['4138078402'])



