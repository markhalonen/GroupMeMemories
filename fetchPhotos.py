import requests
import pickle

# response = requests.get('https://api.groupme.com/v3/groups?token=fc590e2090b601343be70d176227746f')
# print response
# data = response.json()

def getOldestMessageID(response):
    messages = response['response']['messages']
    return messages[len(messages) - 1]['id']


allMessages = []

def requestMessages(limit, since_id = 0):
    payload = {"limit" : limit, "before_id" : since_id}
    if since_id == 0:
        payload = {"limit" : limit}
    print payload
    response = requests.get('https://api.groupme.com/v3/groups/1514901/messages?token=', payload)
    if(response.status_code == 200):
        return response.json()

count = 0
lastId = 0
while(True):
    count = count + 1
    response = requestMessages(100, lastId)
    if response is None:
        break
    lastId = getOldestMessageID(response)
    for val in response['response']['messages']:
        allMessages.append(val)


pickle.dump( allMessages, open( "allMessages.p", "wb" ) )
# for message in allMessages:
#     print message
#     print '\n'

