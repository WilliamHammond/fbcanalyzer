# ChatStream.py
# William Hammond


import string
import re
import numpy as np
import matplotlib.pyplot as plt

from nltk import pos_tag
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.collocations import TrigramAssocMeasures, TrigramCollocationFinder

from collections import Counter
from sets import Set

from datetime import datetime, timedelta
import dateutil.parser

STOP_WORDS = stopwords.words('english') + \
    ['i\'m', 'want', 'dont', 'don\'t', 'go', 'going', 'good', 'also',
     'got', 'though', 'know', 'want', 'there', 'really', 'right',
     'feel', 'let', 'tomorrow']
PUNCTUATION = string.punctuation


class ChatStream(object):
    def __init__(self, data):
        self.data = data
        self.tknzr = TweetTokenizer(preserve_case=False)

    def get_data(self):
        return self.data

    def by_year(self, year):
        return ChatStream([w for w in self.data if
                          self.get_year_from_iso(w['date_time']) == year])

    def by_year_range(self, start, end):
        if start > end:
            raise Exception("Start year later than the end")
        return ChatStream([w for w in self.data if
                          self.get_year_from_iso(w['date_time']) in
                          xrange(start, end)])

    def by_user(self, user):
        return ChatStream([w for w in self.data if w['user'] == user])

    def remove_non_ascii(self):
        new_data = []
        for entry in self.data:
            new_entry = dict(entry)
            new_entry['text'] = " ".join(self._strip_non_ascii(entry['text']))

            new_data.append(new_entry)
        return ChatStream(new_data)

    def _strip_non_ascii(self, words):
        return [w for w in words if self._word_is_ascii(w)]

    def _word_is_ascii(self, word):
        for c in word:
            if ord(c) > 128:
                return False
        return True

    def remove_stop_words(self):
        new_data = []
        for entry in self.data:
            new_entry = dict(entry)
            new_entry['text'] = " ".join([w for w in entry['text'] if
                                          w not in STOP_WORDS])

            new_data.append(new_entry)
        return ChatStream(new_data)

    def remove_punctuation(self):
        new_data = []
        for entry in self.data:
            new_entry = dict(entry)
            new_entry["text"] = " ".join(re.split("\W+", entry["text"]))
            new_data.append(new_entry)
        return ChatStream(new_data)

    def get_n_grams(self, n):
        tags = ["NN", "NNS", "JJ", "JJR", "JJS"]
        return list(ngrams(self._get_tags(tags), n))

    def most_common_n_grams(self, n, m):
        return Counter(self.get_n_grams(n)).most_common(m)

    def get_most_common_words(self, n):
        return Counter(self.get_word_lst()).most_common(n)

    def get_message_lst(self):
        return [msg['text'] for msg in self.data]

    def get_word_lst(self):
        return self._flatten([self.tknzr.tokenize(w) for w in
                              self.get_message_lst()])

    def get_year_from_iso(self, iso_year):
        return datetime.strptime(iso_year, "%Y-%m-%dT%H:%M:%S").year

    def get_message_count(self):
        return len(self.data)

    def get_users(self):
        return Set([w['user'] for w in self.data])

    def get_word_count(self):
        return len(self.get_word_lst())

    def best_n_bigrams(self, n, method="pmi"):
        bigram_measures = BigramAssocMeasures()
        tokens = self.get_word_lst()
        finder = BigramCollocationFinder.from_words(tokens)

        if method == "pmi":
            return finder.nbest(bigram_measures.pmi, n)
        if method == "raw_freq":
            return finder.nbest(bigram_measures.raw_freq, n)

    def best_n_trigrams(self, n, method="pmi"):
        trigram_measures = TrigramAssocMeasures()
        tokens = self.get_word_lst()
        finder = TrigramCollocationFinder.from_words(tokens)

        if method == "pmi":
            return finder.nbest(trigram_measures.pmi, n)
        if method == "raw_freq":
            return finder.nbest(trigram_measures.raw_freq, n)

    def occurence_count_by_phrase(self, phrase):
        count = 0
        for entry in self.data:
            sentence = self.tknzr.tokenize(entry['text'])
            if phrase in sentence:
                count += 1
        return count

    def phrase_count_all_users(self, phrases):
        result_format = "%s : %s"
        result = []

        for user in self.get_users():
            entry = dict()
            entry['word_count'] = 0
            for phrase in phrases:
                entry['user'] = user
                entry['word_count'] += self.by_user(user) \
                                           .occurence_count_by_phrase(phrase)

            result.append(entry)

        result = sorted(result, key=lambda k: k['word_count'])[::-1]
        print phrases
        print "Occurence count for %s" % " ".join(phrases)
        print "_____________________\n"

        for entry in result:
            if entry['word_count'] > 0:
                print result_format % (entry['user'], entry['word_count'])

    def find_first_instance_phrase(self, phrase):
        for entry in self.data[::-1]:
            if re.search("(?<![\w])%s(?![\w])" % phrase, entry["text"]):
                return entry
        print "Phrase not found."

    def find_all_instances_phrase(self, phrase):
        result = []
        for entry in self.data[::-1]:
            if re.search("(?<![\w])%s(?![\w])" % phrase, entry["text"]):
                result.append(entry)
        return result

    def phrase_frequency_over_time(self, phrase, time_interval, plot=False):
        msgs = self.find_all_instances_phrase(phrase)
        if not msgs:
            raise Exception("Phrase is never used")

        dates = [dateutil.parser.parse(msg['date_time']) for msg in msgs]
        time_interval = timedelta(days=time_interval)

        first_date = dates[0]
        last_date = dates[-1]

        bins = []
        current = first_date
        while current < last_date:
            bins.append(current)
            current += time_interval

        to_timestamp = np.vectorize(lambda x: (x - datetime(1970, 1, 1))
                                    .total_seconds())
        from_timestamp = np.vectorize(lambda x: datetime.utcfromtimestamp(x))
        hist, bin_edges = np.histogram(to_timestamp(dates))

        if plot:
            plt.title("Frequency count for phrase %s" % phrase)
            plt.bar(from_timestamp(bin_edges[0:len(bin_edges) - 1]),
                    hist, width=10)
            plt.show()

        return hist, from_timestamp(bin_edges)

    def _flatten(self, lst):
        return [item for sublist in lst for item in sublist]

    def _get_tags(self, tags):
        return [word for (word, tag) in pos_tag(self.get_word_lst())
                if tag in tags]
