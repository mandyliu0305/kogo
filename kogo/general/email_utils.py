# -*- coding: utf-8 -*-

from __future__ import print_function

import bs4
import email
import base64


def get_text_from_part(part):
    text = ""
    ctype = part.get_content_type()
    if ctype == "text/plain":
        content = part.get_payload(decode=True)
        text = content.decode("utf-8", "ignore")
    elif ctype == "text/html":
        content = part.get_payload(decode=True)
        soup = bs4.BeautifulSoup(content, "html.parser").get_text()
        text = soup

    return text


# Convert all email parts with text to plain text
def get_text_from_email(msg):
    text = ""
    if msg.is_multipart():
        for part in msg.walk():
            text += get_text_from_part(part)
    else:
        text += get_text_from_part(msg)

    return text.strip()


# Return email as a dictionary with sender, subject and date information
# If keyword 'order' is in the subject, add all converted text to email dictionary
def parse_email_with_headers(email_with_headers):
    msg = email.message_from_bytes(email_with_headers.encode("utf-8"))
    message_summary =  {
        "sender": msg["From"],
        "subject": msg["Subject"],
        "date": msg["Date"]
    }

    if "order" in msg["Subject"].lower():
        message_summary["text"] = get_text_from_email(msg)

    return message_summary


def get_mime_message(message):
    raw_message = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
    msg = email.message_from_bytes(raw_message)

    message_summary =  {
        "sender": msg["From"],
        "subject": msg["Subject"],
        "date": msg["Date"]
    }
    for field in message_summary:
        if isinstance(message_summary[field], email.header.Header):
            message_summary[field] = str(message_summary[field])
    try:
        if "order" in msg["Subject"].lower():
            message_summary["text"] = get_text_from_email(msg)
    except Exception as e:
        print(e)

    return message_summary