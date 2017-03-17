import random
import pickle
from nltk.classify import ClassifierI
from statistics import mode
import process_tweets

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


documents_f = open("../pickle/documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()

word_features5k_f = open("../pickle/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()


def find_features(document):
    words = process_tweets.process_tweets(document)
    words = process_tweets.get_feature_vector(words)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

featuresets_f = open("../pickle/word_features5k.pickle", "rb")
featuresets = pickle.load(featuresets_f)
featuresets_f.close()

random.shuffle(featuresets)
print(len(featuresets))

testing_set = featuresets[8000:]
training_set = featuresets[:8000]



open_file = open("../pickle/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()


voted_classifier = VoteClassifier(classifier)

def sentimenttest(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)