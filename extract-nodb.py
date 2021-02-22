import tweepy
import json
from tweepy import StreamListener

consumer_key="wTLFTGNSJWn15NGzUFbXLIc3g"
consumer_key_secret="baHOUMlet7QhOUiatcwBPg8uCAzjVanZxl5NJt0ByErkDVyfCY"
access_token="4138078402-kSFVjvbGPrm5TeCO3Ldz4b0jg7muQc7MxBReC0L"
access_token_secret="0uvKDNBD5tAt9WgFB6PmcfdmjcYdFG1r8rxRnPqFEGch8"

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)

auth.set_access_token(access_token, access_token_secret)

api=tweepy.API(auth, wait_on_rate_limit=True,
               wait_on_rate_limit_notify=True)

usr=api.get_user('JeanCaUsagi')
id=usr.id_str
print(id)
"""
data=(tweepy.Cursor(api.user_timeline, screen_name=account, tweet_mode="extended", lang="es").items(0))
i=0
for user in data:

    datajson=json.dumps(user._json,indent=2)
    datajson=json.loads(datajson)
    print(user._json['full_text'])
    print("\n---------------\n")
    i=i+1

print(i)
"""
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
        print("tweet guardado")
        print(id)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener, tweet_mode="extended")
myStream.filter(follow=[id]).



