# fbcanalyzer - Facebook Chat Analyzer

This package is meant to make it easy to get a detailed look at your personal facebook conversations.

How to Use:
-----------
First thing that needs to be done is to request your personal archive from Facebook, this will probable take a couple days. Some formatted example data is included with the package for testing. After you have data available ...

Run `python setup.py install`

Initially the `clean_messages` module needs to be imported and the method `get_csvs` needs to be used to generate csv files from Facebook's html file of all your messages. After this the `clean_messages` method needs to be used in order to build a list of dictionary entries where every entry is a messagae.

Once this lists is available, pass the list to the `ChatStream` object. `ChatStream` supports filtering functions that will return a new ChatStream with altered data and functions that return some value determined from the data.
