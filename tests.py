import unittest
from ChatStream import ChatStream


MESSAGE_COUNT = 7
WORD_COUNT = 18


def get_conversation():
    conversation = []

    conversation.append({u'text': u'Ooohhhhh yeaaaah',
                         u'user': u'Kamath,Vijay',
                         u'date_time': u'2016-07-30T14:52:00'})
    conversation.append({u'text': u'The strokes?',
                         u'user': u'Hammond,William',
                         u'date_time': u'2016-07-30T14:50:00'})
    conversation.append({u'text': u'the strokes?', u'user': u'Hammond,William',
                         u'date_time': u'2016-07-30T13:35:00'})
    conversation.append({u'text': u'the strokes? ? ! , .',
                         u'user': u'Kamath,Vijay',
                         u'date_time': u'2016-07-30T13:33:00'})
    conversation.append({u'text': u"the strokes?",
                         u'user': u'Kamath,Vijay',
                         u'date_time': u'2016-07-30T13:31:00'})
    conversation.append({u'text': u'The strokes?',
                         u'user': u'Hammond,William',
                         u'date_time': u'2015-07-30T14:50:00'})
    conversation.append({u'text': u'The strokes?',
                         u'user': u'Hammond,William',
                         u'date_time': u'2014-07-30T14:50:00'})

    return ChatStream(conversation)


class TestChatStream(unittest.TestCase):
    def test_by_year_no_year(self):
        stream = get_conversation()

        self.assertEqual(stream.by_year("0").get_data(), [])

    def test_by_year(self):
        stream = get_conversation()

        for msg in stream.by_year("2016").get_data():
            self.assertEqual(stream.get_year_from_iso(msg["date_time"]),
                             2016)

    def test_bad_year_range(self):
        stream = get_conversation()

        with self.assertRaises(Exception):
            stream.by_year_range(2020, 0)

    def test_year_range(self):
        stream = get_conversation()

        for msg in stream.by_year_range(2015, 2016).get_data():
            self.assertIn(stream.get_year_from_iso(msg["date_time"]),
                          [2015, 2016])

    def test_year_from_iso(self):
        stream = get_conversation()

        year = stream.get_year_from_iso(stream.get_data()[0]["date_time"])
        self.assertEqual(year, 2016)

    def test_message_count(self):
        stream = get_conversation()

        self.assertEqual(MESSAGE_COUNT, stream.get_message_count())

    def test_word_count(self):
        stream = get_conversation()

        self.assertEqual(WORD_COUNT, stream.get_word_count())

    def test_remove_punctuation(self):
        stream = get_conversation()

        for msg in stream.remove_punctuation().get_data():
            self.assertNotIn("?", msg["text"])
            self.assertNotIn(",", msg["text"])
            self.assertNotIn("!", msg["text"])

if __name__ == "__main__":
    unittest.main()
