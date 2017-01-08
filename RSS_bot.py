#!/usr/bin/env python
# -*- coding: utf-8 -*-


# RSS bot
# RSS bot daily crawls through personal feed of sites using feedparser module and search
# articles with predefined tags and key words. If the RSS bot finds keywords in article
# then it will add them in Pocket account with tag #RSS bot
# RSS 2.0 specification: https://cyber.harvard.edu/rss/rss.html
# Feedparser documentation: http://pythonhosted.org/feedparser/


import feedparser
import requests
import json


# Personal RSS feeds
news_urls = ['https://www.wired.com/feed/',
        	'https://www.wired.com/category/business/feed/',
        	'https://www.technologyreview.com/stories.rss',
        	'http://feeds.arstechnica.com/arstechnica/index',
        	'http://feeds.feedburner.com/TechCrunch/',
        	'http://feeds.feedburner.com/TechCrunch/startups',
        	'https://news.ycombinator.com/rss',
        	'http://thenextweb.com/feed/',
        	'http://feeds.reuters.com/reuters/businessNews'
        ]
# Keywords which RSS bot will look for in articles
keywords = ['hedge fund', 'machine learning', 'finance', 'stock', 'artificial intelligence',
            'fintech', 'IPO', 'python', 'big data', 'cryptocurrency', 'AI', 'investments',
            'investment', 'bitcoin', 'hacked', 'hacking', 'finance', 'trading', 'banking',
            'invest', 'currency', 'stocks', 'hedge', 'fund', 'roboadvising', 'investing',
            'robo-advisor']


def save_article(article_url):
    """
    Save articles in Pocket
    Article_url: string

    Returns: string ('1' - article added, '0' - error)
    """
    url_post = 'https://getpocket.com/v3/add'
    headers = {"Content-Type": "application/json; charset=UTF-8",
               "X-Accept": "application/json"}
    data = {"url": article_url, 'tags': 'RSS bot',
            "consumer_key": "62049-42ff9345436b53314c8def72",
            "access_token": "cf0b5e30-8aeb-f475-b1e9-41dfe0"}
    r = requests.post(url_post, data=json.dumps(data), headers=headers)
    status = json.loads(r.text)

    return status['status']


def reviewing_news(urls):
    """
    Check articles in RSS feed for keywords
    News_url: string

    Returns: string with number of articles added in Pocket
    """
    n = 0
    for feed in urls:
        f = feedparser.parse(feed)
        # Check each entry in RSS feed
        for i in range(len(f.entries)):
            for word in keywords:
                # Add article in Pocket if any keyword was found
                if word in f.entries[i].description or word in f.entries[i].title:
                    save_article(f.entries[i].link)
                    n += 1
    return 'RSS bot added ' + str(n) + ' articles'


print(reviewing_news(news_urls))


# --------------------------------------------------------------------------------
# Code for user authentication in Pocket using OAuth 2.0
# Documentation for Pocket app: https://getpocket.com/developer/docs/authentication
# Documentation for OAuth 2.0:

def generate_request_token(consumer_key):
    """
    Generate request token using OAuth 2.0 for authentication
    Consumer_key: Consumer key for Pocket App

    Returns: Token code (for example "0b700df8-643b-ee91-312e-4942db")
    """
    url_post = 'https://getpocket.com/v3/oauth/request'
    headers = {"Content-Type": "application/json; charset=UTF-8",
               "X-Accept": "application/json"}
    data = {"consumer_key": consumer_key,
            "redirect_uri": "pocketapp1234:authorizationFinished"}
    r = requests.post(url_post, data=json.dumps(data), headers=headers)
    request_token = json.loads(r.text)

    return request_token

key = "62049-42ff9345436b53314c8def72"

# print(generate_request_token(key))


def token_auth(user_token):
    url = 'https://getpocket.com/auth/authorize'
    data = {"request_token": user_token,
            "redirect_uri": "pocketapp1234:authorizationFinished"}
    url_full = 'https://getpocket.com/auth/authorize?request_token=a045b025-a0a1-61f4-1493-2d8abf' \
               '&redirect_uri=pocketapp1234:authorizationFinished'
    r = requests.post(url, data=json.dumps(data))
    auth_token = requests.get(url_full)

    return auth_token

user_token = 'a045b025-a0a1-61f4-1493-2d8abf'

# print(token_auth(user_token))

# access_token = "cf0b5e30-8aeb-f475-b1e9-41dfe0"