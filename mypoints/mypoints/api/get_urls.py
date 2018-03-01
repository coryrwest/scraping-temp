import sys, imaplib, email, email.header, datetime, json, urllib, html, numpy, os
from bs4 import BeautifulSoup

script_dir = os.path.dirname(__file__)
json_file = open(os.path.join(script_dir, 'mypoints.json'))
emails = json.load(json_file)
EMAIL_FOLDER = "INBOX"

def get_emails(M):
    links = []
    point = 0
    # Get all messages
    rv, data = M.uid('SEARCH', 'ALL')
    if rv != 'OK':
        print("No messages found!")
        return
    
    for uid in data[0].split():
        success = False
        noLinks = True
        # Get the body for this message
        rv, data = M.uid('FETCH', uid, '(BODY[2])')
        if rv != 'OK':
            print('ERROR getting message', int(uid), '. Error:', data)
            continue
        
        body = data[0][1]
        if type(body) is int:
            rv, data = M.uid('FETCH', uid, '(BODY[1])')
            body = data[0][1]
        email_body = body.decode('ascii')
        html_body = html.unescape(email_body)
        bs_body = BeautifulSoup(html_body, 'html.parser')
        for img in bs_body.findAll("img"):
            alt = img.get('alt')
            if alt == 'Get Points':
                link = img.find_parent('a')
                href = link.get('href')
                links.append(href)
                success = True
                noLinks = False
        if noLinks:
            print('Email contains no links, deleting')
            success = True
        for span in bs_body.findAll("span"):
            if span.next is not None:
                try:
                    if len(span.next) > 1 and 'PTS' in span.next:
                        content = span.next.strip()
                        if 'PTS' in content:
                            pointText = content.replace(' PTS', '')
                            if int(pointText) > point:
                                point = int(pointText)
                except Exception as e:
                    print(e)
                    if point == 0:
                        point = -1
        # Delete message after link found
        if success:
            M.uid('STORE', uid, '+FLAGS', '\\Deleted')
            M.expunge()
        
    return [links, point]
        
def loop_emails():
    emailData = []
    cont = True
    for email in emails:
        links = []
        points = 0
        M = imaplib.IMAP4_SSL(email["imap"])
        try:
            rv, data = M.login(email["email"], email["password"])
        except imaplib.IMAP4.error as e:
            print ("LOGIN FAILED!!! ")
            print(e)
            cont = False
        
        #print(rv, data)
        
        if cont is True:
            rv, mailboxes = M.list()
            if rv == 'OK':
                print("Got Mailboxes for " + email['email'])
                #print(mailboxes)
            
            rv, data = M.select(EMAIL_FOLDER)
            if rv == 'OK':
                #print("Processing mailbox...\n")
                new_links_points = get_emails(M)
                if new_links_points is not None:
                    links = links + new_links_points[0]
                    points = new_links_points[1]
                M.close()
            else:
                print("ERROR: Unable to open mailbox ", rv)
            
            M.logout()
            emailData.append([email['email'], points, links])
    return emailData

if __name__ == "__main__":
    loop_emails()