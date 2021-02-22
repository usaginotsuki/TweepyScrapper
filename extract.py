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

account=input("Ingrese el @ de la cuenta a la que seguir\n")
usr=api.get_user(account)
id=usr.id_str
print(id)

if "tweets" in dblist:
    print("Ya existe la base de datos")
    db=client.tweets
else:
    db=client['tweets']
db = client.tweets
collection = db[account]
print("Connection")

data=(tweepy.Cursor(api.user_timeline, screen_name=account, tweet_mode="extended", lang="es").items(0))
i=0
for user in data:

    datajson=json.dumps(user._json,indent=2)
    datajson=json.loads(datajson)
    print(user._json['full_text'])
    print("\n---------------\n")
    collection.insert_one(datajson)
    i=i+1

print(i)

print("Datos guardados en la base de datos, escuchando nuevos tweets\n")

print("---------------------------------------\n")
print("---------------------------------------\n")

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweetid=status.id
        tweet=api.get_status(tweetid, tweet_mode="extended")
        datajson=json.dumps(tweet._json, indent=2)
        datajson=json.loads(datajson)
        print(datajson)
        id=collection.insert_one(datajson)
        print("tweet guardado")
        print(id)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode="extended")
myStream.filter(follow=[id])



