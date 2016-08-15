#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import json
import tw_setting as tw

def main():
    twitter = OAuth1Session(tw.CONSUMER_KEY, tw.CONSUMER_SECRET, tw.ACCESS_TOKEN, tw.ACCESS_TOKEN_SECRET)

    params = {}
    req = twitter.get("https://api.twitter.com/1.1/statuses/home_timeline.json", params = params)

    timeline = json.loads(req.text)

    for tweet in timeline:
        print (tweet["text"])


if __name__ == '__main__':
    main()
        
