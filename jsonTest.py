__author__ = 'brent'

bigArr = []
arr = [{"data1" : "hello"}, {"data2" : "hello"}]
print len(arr)
for val in arr:
    bigArr.append(val)
print bigArr

def getOldestMessageID(response):
    messages = response['response']['messages']
    return messages[len(messages) - 1]['id']
