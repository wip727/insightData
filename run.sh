#!/usr/bin/env bash

# ChangQing Wang
# Twitter cleaner and hashtag analyzer
# Please read README.md
python ./src/tweets_cleaned.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt
python ./src/average_degree.py ./tweet_input/tweets.txt ./tweet_output/ft2.txt




