import pickle
allMessages = pickle.load(open( "familyGroup.p", "rb" ))
#print allMessages[len(allMessages) - 1]

sortedMessages = sorted(allMessages, key=lambda message: len(message['favorited_by']), reverse=True)
print len(sortedMessages[0]['favorited_by'])
count = 0
idx = 0
while count < 10:
    if len(sortedMessages[idx]['attachments']) == 0:
        idx = idx + 1
        continue
    # It's an image.
    print sortedMessages[idx]
    idx = idx + 1
    count = count + 1
