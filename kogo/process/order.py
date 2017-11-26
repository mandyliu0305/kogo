# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import glob
import codecs
import pprint
import argparse

from kogo.general import email_utils


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
            return matches[0]

    return None


def find_order_info(message_summary):
    if "text" not in message_summary:
        return message_summary

    order_info = {
        "order_number": [],
        "tracking_number": []
    }
    msg_splits = [part for part in message_summary["text"].splitlines() if len(part)]
    for msg_split in msg_splits:
        raw_text = msg_split.lower()
        order_number = search_tag(raw_text, "order", 2)
        if order_number and order_number not in order_info["order_number"]:
            order_info["order_number"].append(order_number)
        tracking_number = search_tag(raw_text, "tracking", 3)
        if tracking_number and tracking_number not in order_info["tracking_number"]:
            order_info["tracking_number"] = tracking_number

    del message_summary["text"]
    message_summary.update(order_info)
    return message_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="kogo library")
    parser.add_argument("-f", "--file", dest="file", help="Path to input file", default=None)
    parser.add_argument("-d", "--directory", dest="directory", help="Path to input directory", default="./")
    args = parser.parse_args()

    if args.file:
        input_file = args.file
        with codecs.open(input_file, "r", "utf-8") as f:
            raw_msg = f.read()
            message_summary = email_utils.parse_email_with_headers(raw_msg)
            order_info = find_order_info(message_summary)
            pprint.pprint(order_info)

    elif args.directory:
        input_files = glob.glob(args.directory + "*.txt")
        for input_file in input_files:
            with codecs.open(input_file, "r", "utf-8") as f:
                raw_msg = f.read()
                message_summary = email_utils.parse_email_with_headers(raw_msg)
                order_info = find_order_info(message_summary)
                pprint.pprint(order_info)