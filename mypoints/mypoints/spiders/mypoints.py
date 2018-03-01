import scrapy
from mypoints.api.get_urls import loop_emails
from mypoints.api.emailer import send_email

class MyPointsSpider(scrapy.Spider):
    message = ''
    name = "mypoints"
    data = loop_emails()
    urls = []
    print('Done getting email data')
    print(data)
    # Go and get all the links
    for emailData in data:
        links = emailData[2]
        account = emailData[0]
        points = emailData[1]
        if len(links) > 0:
            message = message + 'User: ' + account + '. Links: ' + str(len(links)) + '. ' + str(points) + ' estimated total.\r\n'
            urls = urls + links
        else :
            message = message + 'User: ' + account + '. No emails.\r\n'
    print('Done getting links')
    status = send_email(message)
    
    start_urls = urls
    
    def parse(self, response):
        yield {
            'url-visited': response.url,
            'email-status': self.status
        }