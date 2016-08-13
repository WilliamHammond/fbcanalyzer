import unittest
from ChatStream import ChatStream


def get_conversation():
    conversation = []

    conversation.append({u'text': u'Ooohhhhh yeaaaah',
                         u'user': u'Kamath,Vijay',
                         u'date_time': u'2016-07-30T14:52:00'})
    conversation.append({u'text': u'The strokes?',
                         u'user': u'Hammond,William',
                         u'date_time': u'2016-07-30T14:50:00'})
    conversation.append({u'text': u'Just realized the first record I every\
                         bought for myself and one of my favorite albums ever,\
                         is this it, turned 15 today',
                         u'user': u'Kamath,Vijay',
                         u'date_time': u'2016-07-30T14:38:00'})
    conversation.append({u'text': u'Word', u'user': u'Kamath,Vijay',
                         u'date_time': u'2016-07-30T13:41:00'})
    conversation.append({u'text': u'Its a solid spot. $10 shock top pitchers',
                         u'user': u'Hammond,William',
                         u'date_time': u'2016-07-30T13:41:00'})
    conversation.append({u'text': u"No, but we'll see. I saw his post.I'll be\
                         down to go. Don't have plans tonight as of yet.\
                         And I've got two weeks left",
                         u'user': u'Kamath,Vijay',
                         u'date_time': u'2016-07-30T13:37:00'})
    conversation.append({u'text': u'We got rekt last night. Have you been to on\
                         the hill tavern with joey',
                         u'user': u'Hammond,William',
                         u'date_time': u'2016-07-30T13:37:00'})
    conversation.append({u'text': u'Hope you guys are doing something fun for\
                         Ryan today', u'user': u'Kamath,Vijay',
                         u'date_time': u'2016-07-30T13:36:00'})
    conversation.append({u'text': u'Nice.', u'user': u'Kamath,Vijay',
                         u'date_time': u'2016-07-30T13:35:00'})
    conversation.append({u'text': u'Good', u'user': u'Hammond,William',
                         u'date_time': u'2016-07-30T13:35:00'})
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

if __name__ == "__main__":
    unittest.main()
