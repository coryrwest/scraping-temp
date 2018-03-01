import smtplib
import sys
from email.mime.text import MIMEText

sender = 'corysmtpserver@gmail.com'
receivers = ['serverlogs@crwest.com']
gmail_user = 'corysmtpserver@gmail.com'
gmail_pwd = 'smtpAPI44'

def send_email(message):
    BODY = "\r\n".join((
            "From: %s" % sender,
            "To: %s" % receivers[0],
            "Subject: Clicker Update",
            "",
            message
            ))
    print(BODY)
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(gmail_user, gmail_pwd)
    smtp.sendmail(sender, receivers, BODY)
    smtp.close()
    return "Successfully sent email"
    
if __name__ == "__main__":
    send_email("TEST")