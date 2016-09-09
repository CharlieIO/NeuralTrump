import tweepy  # https://github.com/tweepy/tweepy
import re
import os
import subprocess
import time

# Twitter API credentials
consumer_key = os.environ["consumer_key"]
consumer_secret = os.environ["consumer_secret"]
access_key = os.environ["access_key"]
access_secret = os.environ["access_secret"]
screen_name = 'realDonaldTrump' # Modify this username to mimic a different user.


def get_all_tweets():
    # Twitter only allows access to a users most recent 3240 tweets with this
    # method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed
    # count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))

    # transform the tweepy tweets into a 2D array that will populate the csv
    first = True

    for tweet in alltweets:
        text = tweet.text.encode("ascii", "ignore")
        if '"' not in text and "RT @" not in text and "http" not in text:
            if first:
                outtweets = [text.replace('\n', '').replace('&amp;', '&') + ' ']
                first = False
            else:
                outtweets += [text.replace('\n',
                                            '').replace('&amp;', '&') + ' ']

    # write the txt
    outfile = open('file.txt','w')
    outfile.write("\n".join(outtweets))
    outfile.close()

def trainer():
    p = subprocess.Popen(['python', '/mnt/c/Users/Charlie/torch-rnn/scripts/preprocess.py', '--input_txt', '/mnt/c/Users/Charlie/GoogleDrive/Projects/NeuralTrump/file.txt', '--output_h5', '/mnt/c/Users/Charlie/GoogleDrive/Projects/NeuralTrump/my_data.h5', '--output_json', '/mnt/c/Users/Charlie/GoogleDrive/Projects/NeuralTrump/my_data.json'])
    time.sleep(3) #a short buffer to ensure p finishes before t starts. Not sure if necessary.
    t = subprocess.Popen(['th', '/mnt/c/Users/Charlie/torch-rnn/train.lua', '-input_h5', '/mnt/c/Users/Charlie/GoogleDrive/Projects/NeuralTrump/my_data.h5', '-input_json', '/mnt/c/Users/Charlie/GoogleDrive/Projects/NeuralTrump/my_data.json', '-gpu', '-1', '-num_layers', '5', '-rnn_size', '512'])

# def get_output():


def main():
    get_all_tweets()
    trainer()

if __name__ == '__main__':
    main()
