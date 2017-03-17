import csv
import nltk
import re


def process_tweets(tweets):
    # convert to lower
    tweets = tweets.lower()
    # Convert www.* or https?://* to URL
    tweets = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', tweets)

    # Convert @username to AT_USER
    tweets = re.sub('@[^\s]+', 'AT_USER', tweets)

    # Convert www.* or https?://* to URL
    tweests = [[re.compile("http(.*)")] for tweet in tweets]
    # Remove additional white spaces
    tweets = re.sub('[\s]+', ' ', tweets)

    # Replace #word with word
    tweets = re.sub(r'#([^\s]+)', r'\1', tweets)
    # trim
    tweets = tweets.strip('\'"')

    # remove number
    tweets = re.sub(r'(?:(?:\d+,?)+(?:\.?\d+)?)', '', tweets)

    return tweets


# initialize stopWords
stopWords = []



def replace_two_ormore(tweets):
    # look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", tweets)


# end

# start getStopWordList
def get_stop_word_list(stop_wordlist_filename):
    # read the stopwords file and build a list
    stop_words = []
    stop_words.append('AT_USER')
    stop_words.append('URL')
    stop_words.append('rt')
    stop_words.append('im')

    fp = open(stop_wordlist_filename, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stop_words.append(word)
        line = fp.readline()
    fp.close()
    return stop_words


st = open('stop_word.txt', 'r')
stop_words = get_stop_word_list('stop_word.txt')

def get_feature_vector(tweets):
    feature_vector = []

    # split tweets into words
    word = tweets.split()
    # split two or more occurance
    for w in word:
        w = replace_two_ormore(w)

        # strip punctuation
        w = w.strip('\'"?,.')

        # check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)

        # ignore if it is a stop word
        if (w in stop_words or val is None):
            continue
        else:
            feature_vector.append(w.lower())
    return feature_vector


