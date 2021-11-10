#! /usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from settings import EMAIL_SMTP_SETTINGS


def send_mail(subject, message, message_type='html'):
    message = MIMEText(message, message_type, 'utf-8')
    message['From'] = Header(EMAIL_SMTP_SETTINGS.get("display_name"), 'utf-8')
    message['To'] = Header(",".join(EMAIL_SMTP_SETTINGS.get("to_addrs")), 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    smtpObj = smtplib.SMTP()
    smtpObj.connect(EMAIL_SMTP_SETTINGS.get("host"), EMAIL_SMTP_SETTINGS.get("port"))
    smtpObj.login(EMAIL_SMTP_SETTINGS.get("username"), EMAIL_SMTP_SETTINGS.get("password"))
    smtpObj.sendmail(EMAIL_SMTP_SETTINGS.get("from_addr"), EMAIL_SMTP_SETTINGS.get("to_addrs"), message.as_string())


if __name__ == "__main__":
    send_mail("Test", "<table border='1'><tr><td>100</td></tr></table>")