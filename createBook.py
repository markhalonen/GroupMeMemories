import pickle
import sys
import datetime

imageMaxWidth = 900.0
imageMaxHeight = 400.0

reload(sys)
sys.setdefaultencoding('utf8')
page = open("index4.html", "r").read()
allMessages = pickle.load(open( "familyGroup.p", "rb" ))
dateDiv = '<!----><div class="timestamp-divider" ng-if="message.formattedTimestamp" ng-bind="message.formattedTimestamp">%%Date%%</div><!---->'

def addImageMessage(page, userName, userNameUrl, text, imageurl, likes, date):
    message = open("imageMessage.html", "r").read()
    message = message.replace("%%UserName%%", userName)
    message = message.replace("%%UserNameUrl%%", userNameUrl)
    dims = imageurl.split(".com/")[1].split(".")[0]
    width = float(dims.split('x')[0])
    height = float(dims.split('x')[1])
    if width / height > imageMaxWidth / imageMaxHeight:
        #width is the limiting dimension
        message = message.replace("%%ImageWidth%%",str(int(imageMaxWidth)), 2)
        message = message.replace("%%ImageHeightPercentage%%", str(height / width * 100))
    else:
        #Height is the limiting dimension
        imgWidth = width * imageMaxHeight / imageMaxWidth
        message = message.replace("%%ImageWidth%%",str(int(imgWidth)))
        message = message.replace("%%ImageHeightPercentage%%", str(height / width * 100))
    message = message.replace("%%Text%%", text)
    message = message.replace("%%Image%%", imageurl)
    message = message.replace("%%Likes%%", likes)
    if date != "":
        dateDivCopy = dateDiv
        dateDivCopy = dateDivCopy.replace("%%Date%%", date)
        message = message.replace("%%DateDiv%%", dateDivCopy)
    else:
        message = message.replace("%%DateDiv%%", "")
    #message = message.replace("%%Date%%", date)
    message = message + "\n%%Message%%"
    return page.replace("%%Message%%", message, 1)

def addTextMessage(page, userName, userNameUrl, text, likes, date):
    message = open("textMessage.html", "r").read()
    message = message.replace("%%UserName%%", userName)
    message = message.replace("%%UserNameUrl%%", userNameUrl)
    message = message.replace("%%Text%%", text)
    message = message.replace("%%Likes%%", likes)
    if date != "":
        dateDivCopy = dateDiv
        dateDivCopy = dateDivCopy.replace("%%Date%%", date)
        message = message.replace("%%DateDiv%%", dateDivCopy)
    else:
        message = message.replace("%%DateDiv%%", "")
    #message = message.replace("%%Date%%", date)
    message = message + "\n%%Message%%"
    return page.replace("%%Message%%", message, 1)



#print allMessages[len(allMessages) - 1]

sortedMessages = sorted(allMessages, key=lambda message: len(message['favorited_by']), reverse=True)
count = 0
idx = 0
topMessages = []
while count < 40:
    if idx >= len(sortedMessages):
        break
    if len(sortedMessages[idx]['attachments']) == 0 and False:
        idx = idx + 1
        continue
    # It's an image.
    topMessages.append(sortedMessages[idx])
    idx = idx + 1
    count = count + 1

bookMessages = []
idx = 0
bookIdx = 0
timeRange = 5 * 60 #Get the messages within 5 minutes of popular post.
while idx < len(allMessages):
    #Add each message in order and those within 5 minutes
    revIdx = len(allMessages) - 1 - idx
    if allMessages[revIdx] in topMessages:
        allMessages[revIdx]['is_event'] = True
        bookMessages.append(allMessages[revIdx])
        atTime = int(allMessages[revIdx]['created_at'])
        nextIdx = revIdx - 1
        count = 1
        while int(allMessages[nextIdx]['created_at']) < atTime + timeRange:
            allMessages[nextIdx]['is_event'] = False
            bookMessages.append(allMessages[nextIdx])
            nextIdx = nextIdx - 1
            count = count + 1
        idx = idx + count
    else:
        idx = idx + 1

for message in bookMessages:

    text = message['text']
    text = '' if text is None else text
    if len(message['attachments']) == 0 or message['attachments'][0]['type'] != 'image':
        date = datetime.datetime.fromtimestamp(int(message['created_at'])).strftime("%B %d, %Y")
        if not message['is_event']:
            date = ""
        page = addTextMessage(page, message["name"], message['avatar_url'], text, str(len(message['favorited_by'])), date)
    else:
        date = datetime.datetime.fromtimestamp(int(message['created_at'])).strftime("%B %d, %Y")
        if not message['is_event']:
            date = ""
        page = addImageMessage(page, message["name"], message['avatar_url'], text, message['attachments'][0]['url'], str(len(message['favorited_by'])), date)

print page