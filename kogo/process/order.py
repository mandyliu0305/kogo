# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import glob
import codecs
import argparse

import bs4
import email

from general import email_utils


def search_tag(raw_text, tag, n):
    words = raw_text.split()

    if tag not in words:
        return None

    p = re.compile('#?[\w\-*]+[\d+]+[\w\-*]+')
    tag_index = words.index(tag)
    len_words = len(words)

    # prev_word = words[max(0, tag_index-1):tag_index]
    next_word = words[tag_index+1:min(len_words, tag_index+n)]

    for word in next_word:
        matches = p.findall(word)
        if len(matches):
            print(tag, matches[0])

    return


def get_order_info(message_text):
    msg_splits = [part for part in message_text.splitlines() if len(part)]
    for msg_split in msg_splits:
        raw_text = msg_split.lower()
        search_tag(raw_text, "order", 2)
        search_tag(raw_text, "tracking", 3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="kogo library")
    parser.add_argument("-f", "--file", dest="file", help="Path to input file", default=None)
    parser.add_argument("-d", "--directory", dest="directory", help="Path to input directory", default="./")
    args = parser.parse_args()

    if args.file:
        input_file = args.file
        with codecs.open(input_file, "r", "utf-8") as f:
            raw_msg = f.read()
            msg_summary = email_utils.parse_email_with_headers(raw_msg)
            if "text" in msg_summary:
                get_order_info(msg_summary["text"])

    elif args.directory:
        input_files = glob.glob(args.directory + "*.txt")
        for input_file in input_files:
            with codecs.open(input_file, "r", "utf-8") as f:
                raw_msg = f.read()
                msg_summary = email_utils.parse_email_with_headers(raw_msg)
                if "text" in msg_summary:
                    get_order_info(msg_summary["text"])
