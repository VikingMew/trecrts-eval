from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import requests

consumer_key="MbOgGx580do3ZXLRgrBOyhQIB"
consumer_secret="LglS7nQ5VtuZqZrBOEQRQSFP9HPsW2Zn5jxKqH3eg6KzaFiuS6"

access_token="124917841-o2EejsyfT9lrIBR0c2Ht30htdDBupoAo9LJvI8kg"
access_token_secret="5aiq4nr2i9Jdn3xktKhMQF13rSPR7zglwtjs3VzDPKVu8"
seen_tweets = set()

class RetweetListener(StreamListener):

  def on_status(self,status):
    #print(status.text.encode('utf8'))
    if hasattr(status,'retweeted_status'):
      rt_status = status.retweeted_status
#      print status.retweeted_status.id, status.retweeted_status.retweet_count
      if rt_status.retweet_count > 10000 and rt_status.id not in seen_tweets:
        print rt_status.id, rt_status.retweet_count,
        resp = requests.post("http://lab.roegiest.com:33334/tweet/%s"%rt_status.id)
        print resp.status_code
        seen_tweets.add(rt_status.id)
    return True

  def on_error(self,status_code):
    print status_code

if __name__ == '__main__':
  listener = RetweetListener()
  auth = OAuthHandler(consumer_key,consumer_secret)
  auth.set_access_token(access_token,access_token_secret)

  stream = Stream(auth,listener)
  stream.sample(languages=['en'])