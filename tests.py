import unittest
from ChatStream import ChatStream


MESSAGE_COUNT = 7


def get_conversation():
    conversation = []

    conversation.append({u'text': u'Ooohhhhh yeaaaah',
                         u'user': u'Kamath,Vijay',
                         u'date_time': u'2016-07-30T14:52:00'})
    conversation.append({u'text': u'The strokes?',
                         u'user': u'Hammond,William',
                         u'date_time': u'2016-07-30T14:50:00'})
    conversation.append({u'text': u'Got a bloody Mary at the Jewish deli for\
                         brunch it was real goof', u'user': u'Hammond,William',
                         u'date_time': u'2016-07-30T13:35:00'})
    conversation.append({u'text': u'Also today is just beautiful. Perfect heat\
                         and skies, but not too hot. Nothing better than\
                         drinking a nice draft beer on a day like this.\
                         Sipping a Boston lager and waiting for lunch',
                         u'user': u'Kamath,Vijay',
                         u'date_time': u'2016-07-30T13:33:00'})
    conversation.append({u'text': u"I totally get people voting from the heart\
                         and forgetting the system, but Hillary is seriously\
                         just everyone's scapegoat.",
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
        self.assertEquals(year, 2016)

    def test_message_count(self):
        stream = get_conversation()
        self.assertEqual(MESSAGE_COUNT, stream.get_message_count())

if __name__ == "__main__":
    unittest.main()
