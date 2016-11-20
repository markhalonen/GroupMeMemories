import requests

response = requests.get('https://api.groupme.com/v3/groups?token=TOKEN')
print response
data = response.json()

for group in data['response']:
    print group
    print "\n\n"