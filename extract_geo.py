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

account='Ambato1'
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



"""
#Metodo con coordenadas
public_tweets = tweepy.Cursor(api.search, count=100, geocode="-1.278461,-78.639290,4km",show_user = True,tweet_mode="extended").items()
for tweet in public_tweets:
    collection.insert_one(tweet._json)
    print(tweet._json)
    
#------------------------------------------------------------------------------------------------------------------------

#Metodo de buscar los lugares cercanos
places = api.geo_search(query="Ambato", granularity="city")


for place in places:
    print("placeid:%s" % place)
public_tweets = tweepy.Cursor(api.search, count=100,q="place:%s" % place.id,since="2021-02-07",show_user = True,tweet_mode="extended").items()
for tweet in public_tweets:
    collection.insert_one(tweet._json)
    print(tweet._json)

#-------------------------------------------------------------------------------------------------------------------------

"""

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweetid = status.id
        tweet = api.get_status(tweetid, tweet_mode="extended")
        print(tweet._json)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode="extended")
myStream.filter(locations=[-79.0144,-1.7189,-78.2076,-0.8569])


    