# ChatStream.py
# William Hammond
# 8/05/2016


import string

from nltk import Text
from nltk.util import ngrams
from nltk.corpus import stopwords

from collections import Counter
from sets import Set

from datetime import datetime

STOP_WORDS = stopwords.words('english') + \
    ['i\'m', 'want', 'dont', 'don\'t', 'go', 'going', 'good', 'also',
     'got', 'though', 'know', 'want', 'there', 'really', 'right',
     'feel', 'let', 'tomorrow']
PUNCTUATION = string.punctuation


class ChatStream(object):
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def by_year(self, year):
        return ChatStream([w for w in self.data if
                          self.get_year_from_iso(w['date_time']) == year])

    def by_year_range(self, start, end):
        if start > end:
            print "End must be larger than start"
            return -1

        return ChatStream([w for w in self.data if
                          self.get_year_from_iso(w['date_time']) in range])

    def by_user(self, user):
        return ChatStream([w for w in self.data if w['user'] == user])

    def remove_non_ascii(self):
        for entry in self.data:
            entry['text'] = self.strip_non_ascii(entry['text'])
        return ChatStream(self.data)

    def remove_stop_words(self):
        for entry in self.data:
            entry['text'] = [w for w in entry['text'] if w not in STOP_WORDS]
        return ChatStream(self.data)

    def remove_punctuation(self):
        for entry in self.data:
            entry['text'] = [w for w in entry['text'] if w not in PUNCTUATION]
        return ChatStream(self.data)

    def get_n_gram(self, n):
        return list(ngrams(self.get_message_lst(), n))

    def get_most_common_words(self, n):
        return Counter(self.get_message_lst()).most_common(n)

    def get_most_common_n_gram(self, n, num_grams):
        return Counter(self.get_n_gram(n)).most_common(num_grams)

    def get_text(self):
        return Text(self.get_message_lst())

    def get_message_lst(self):
        return self.flatten([w['text'] for w in self.data])

    def get_year_from_iso(self, iso_year):
        return datetime.strptime(iso_year, "%Y-%m-%dT%H:%M:%S").year

    def get_message_count(self):
        return len(self.data)

    def get_users(self):
        return Set([w['user'] for w in self.data])

    def get_word_count(self):
        return len(self.get_message_lst())

    def occurence_count_by_phrase(self, phrase):
        count = 0
        for entry in self.data:
            sentence = " ".join(entry['text'])
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

        print "Occurence count for %s" % phrase
        print "_____________________\n"

        for entry in result:
            if entry['word_count'] > 0:
                print result_format % (entry['user'], entry['word_count'])

    def word_count_all_users(self):
        result_format = "%s : %s"
        result = []

        for user in self.get_users():
            entry = dict()
            entry['user'] = user
            entry['word_count'] = self.by_user(user).get_word_count()

            result.append(entry)

        result = sorted(result, key=lambda k: k['word_count'])[::-1]

        for entry in result:
            print result_format % (entry['user'], entry['word_count'])

    def find_first_instance_word(self, word):
        for entry in self.data[::-1]:
            if word in entry['text']:
                return (entry['user'], entry['date_time'], entry['text'])
        print "Word not found."

    def find_first_instance_phrase(self, phrase):
        for entry in self.data[::-1]:
            sentence = " ".join(entry['text'])
            if phrase in sentence:
                return (entry['user'], entry['date_time'], entry['text'])
        print "Phrase not found."

    def flatten(self, lst):
        return [item for sublist in lst for item in sublist]

    def strip_non_ascii(self, words):
        return [w for w in words if self.word_is_ascii(w)]

    def word_is_ascii(self, word):
        for c in word:
            if ord(c) > 128:
                return False
        return True
