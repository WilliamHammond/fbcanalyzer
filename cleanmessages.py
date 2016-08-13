# clean_messages.py
# William Hammond
# 8/05/2016

import codecs
import io

import unicodecsv as csv

from sets import Set
from bs4 import BeautifulSoup
from datetime import datetime

DATE_TIME_FORMAT = "%A, %B %d, %Y at %I:%M%p %Z"


# Writes out formatted html of facebook messages
# Input:
#   path_to_messages - path to facebook's given message html file
# Output:
#   pretty_messages.html
def get_pretty_html(path_to_messages):
    contents = codecs.open(path_to_messages, 'r')
    soup = BeautifulSoup(contents.read(), 'lxml')

    with io.open("../data/pretty_messages.html",
                 encoding="utf-8", mode='w') as pretty_html:
        pretty_html.write(soup.prettify())


# Return messages as a list of dictionary entries.
# Used to build dictionary that ChatStream expects
# Input:
#   path - Path to csv file containing message data
# Output:
#   msgs - a list of dictionary entries where every entry is a message
#          containing the user, text and datetime of a message
def get_messages(path):
    msgs = []
    with open(path, 'rb') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            msgs.append(row)
    return msgs


# Used to comebine chats. Useful for the case of multiple gropuchats that
# are mostly comprised of the same users
# Input:
#   csv_lst: List of the csv files that contain message data
#   new_group_name: File name for new chat name
def join_chats(csv_lst, new_chat_name):
    path_out = "../data/clean/"
    field_names = ['user', 'text', 'date_time']
    new_data = []

    for csv_file in csv_lst:
        file_out = path_out + csv_file
        msgs = get_messages(file_out)
        new_data += msgs

    new_data = sorted(new_data, key=lambda k: k['date_time'])[::-1]

    with open(path_out + new_chat_name, 'wb') as file_out:
        writer = csv.DictWriter(file_out,
                                fieldnames=field_names)
        writer.writeheader()
        writer.writerows(new_data)


# Generates a CSV file from each of your messages threads. Files are named by
# concatinating the users in the thread together. File names that are too long
# are named cleanMessagesLargeGroupChatx.csv
# Input:
#   path_to_messages - path to Messages.html
#   path_out - path where filed should be written
#   package_user - name of the user of the package, should be formatted as
#                  Lastnname, Firstname
def get_csvs(path_to_messages, path_out, package_user):
    contents = codecs.open(path_to_messages, 'r')
    soup = BeautifulSoup(contents.read(), 'lxml')

    threads = soup.find_all("div", class_="thread")
    for thread in threads:
        entries = []
        to_users = Set()
        num_groups = 1

        messages = thread.find_all("div", class_="message")
        for message in messages:
            entry = dict()

            date_time_raw = message.find("span", class_="meta").get_text()
            date_time = datetime.strptime(date_time_raw,
                                          DATE_TIME_FORMAT).isoformat()
            user = ",".join(message.find("span", class_="user")
                                   .get_text()
                                   .split()[::-1])

            entry['text'] = message.next_sibling.get_text()
            entry['user'] = user
            entry['date_time'] = date_time

            entries.append(entry)

            if not user == package_user:
                # Concat all users in case of group chat
                to_users.add(user)

        field_names = ['user', 'text', 'date_time']
        to_user_string = ",".join(to_users)
        # If path is too long give generic name.
        if len(to_user_string) >= 80:
            to_user_string = "LargeGroupChat" + str(num_groups)
            num_groups += 1

        with open(path_out % to_user_string, 'wb') as file_out:
            writer = csv.DictWriter(file_out, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(entries)
