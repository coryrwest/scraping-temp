import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bs4 import BeautifulSoup
import json

email = 'heather@westroppstudios.com'
#email = 'hgtv@crwest.com'
encodedEmail = email.replace('@', '%40')

#objectId = '109603'
#source = 'diy'
#formId = '166015'

objectId = '109589'
source = 'hgtv'
formId = '166001'

tokenR = requests.get('http://xd.engagesciences.com/display/container/dc/8d2dabc0-c261-4b80-bc43-6d1abb162285/entry?source=' + source)
html = BeautifulSoup(tokenR.text, 'html.parser')
token = html.find(id="ngx_t_token")['value']

r = requests.get('https://submit.engagesciences.com/display/form/post?email=' + encodedEmail + '&apikey=a587a142-38bd-4a4b-ad68-939d090ab1d1&campaignObjectId=' + objectId + '&ngx_remember_me=true&ngx_check_entry=true&isXHR=true&cbh=http%3A%2F%2Fxd.engagesciences.com')

check = json.loads(r.text)
cont = check['state']

multipart_data = MultipartEncoder(
    fields={
            'isXHR': 'true', 
            'apikey': 'a587a142-38bd-4a4b-ad68-939d090ab1d1',
            'containerId': '52c9e4a6-1b9d-48a1-918b-4ca35986f139',
            'formId': formId,
            'campaignId': objectId,
            'container_guid': 'dc28247d-a0ab-4520-8b82-e1ed69edb2a3',
            'promotionId': '',
            'ngxInvitedFriends': '',
            'channelId': '10039',
            'medium': 'direct',
            'source': source,
            'channel': 'website',
            'content': '',
            'activity': '',
            'r': '',
            'mcmid': '80724901440834973555321824772163191592',
            'referrerCode': 'direct',
            'ngx_t_token': token,
            'email': email,
            'ngx_remember_me': 'true',
            'cbh': 'http://xd.engagesciences.com',
          }
    )

url = 'https://submit.engagesciences.com/display/form/post'

if cont == 'known_user':
    response = requests.post('https://httpbin.org/anything/:anything', data=multipart_data, headers={'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryAHJKMQBNrnu5oBpd'}, cookies=r.cookies)
    print(response)
    print(response.text)
else:
    print(r.text)