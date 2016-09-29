#! python3
import json
import requests
import pandas as pd

#Find your personal token at https://dev.groupme.com/docs/v3. In the upper right, click "Access Token". Paste your token in between the '' below. Do not give anybody else your token.
token = ''

#Go to https://dev.groupme.com/bots/new and choose the group you are interested in. Name the bot and press "Submit". NOTE: this will add the bot to your group.
#Now on https://dev.groupme.com/bots you will see your newly created bot and your group ID. Paste your group ID between the '' below. You can now delete your bot.
groupID = ''

#This url will now automatically incorporate your group ID and token.
url = 'https://api.groupme.com/v3/groups/' + groupID + '/messages?token=' + token + '&limit=100'

def get(response):
	return response.json()['response']

JSONresponse = get(requests.get(url))
group_msgs = JSONresponse['messages']
total_msg_count = JSONresponse['count']

def get_all_msgs():
        current_msg_count = len(group_msgs)
        while (current_msg_count < total_msg_count):
                last_msg_id = group_msgs[-1]['id']
                next_100_msgs = get(requests.get(url + '&before_id=' + last_msg_id))['messages']
                group_msgs.extend(next_100_msgs)
                last_msg_id = group_msgs[-1]['id']
                current_msg_count = len(group_msgs)

df = pd.DataFrame(group_msgs)

#Change the directory to the location you would like your output.csv to be posted to.
df.to_csv('C:\\Users\\##\\###\\output.csv', index=False, header=True) 
