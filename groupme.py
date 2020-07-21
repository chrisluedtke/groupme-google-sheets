#! python3
import os

import requests

import pandas as pd
import pygsheets
from dotenv import load_dotenv

load_dotenv()


def msg_getter_generator(group_name):
    group_id = get_group_id(group_name)

    last_msg_id = None
    next_100_msgs = True

    while next_100_msgs:
        next_100_msgs = get_recent_messages(
            group_id=group_id,
            before_msg_id=last_msg_id
        )

        if next_100_msgs:
            last_msg_id = next_100_msgs[-1]['id']
            for msg in next_100_msgs:
                yield msg


def get_recent_messages(group_id, before_msg_id=None):
    url = f'https://api.groupme.com/v3/groups/{group_id}/messages'
    params = {
        'token': os.environ['GROUPME_TOKEN'],
        'limit': 100,
        'before_id': before_msg_id
    }

    response = requests.get(url, params)

    if response.status_code == 304:
        # No previous messages found
        return []
    elif response.status_code != 200:
        response.raise_for_status()
    else:
        response = response.json()
        return response['response']['messages']


def get_group_id(group_name):
    url = 'https://api.groupme.com/v3/groups'
    params = {'token': os.environ['GROUPME_TOKEN'], 'per_page': 100}

    response = requests.get(url, params)

    groups = response.json()['response']

    for group in groups:
        if group['name'].lower() == group_name.lower():
            return group['id']

    raise ValueError('No group found with name:', group_name)


if __name__ == "__main__":
    print('Downloading messages from group')
    data = msg_getter_generator(os.environ['GROUPME_GROUP_NAME'])
    df = pd.DataFrame(data)
    df['created_at'] = (pd.to_datetime(df['created_at'], unit='s', utc=True)
                          .dt.tz_convert('US/Central'))

    col_order = [
        'attachments',
        'avatar_url',
        'created_at',
        'event',
        'favorited_by',
        'group_id',
        'id',
        'name',
        'platform',
        'sender_id',
        'sender_type',
        'source_guid',
        'system',
        'text',
        'user_id'
    ]
    df = df[col_order]

    print('Creating calculated columns')
    df['likes'] = df.loc[:,'favorited_by'].str.len()
    df['words'] = df.loc[:,'text'].str.findall(r'(\w+)').str.len().fillna(0)

    print('Writing messages to Google sheet')
    client = pygsheets.authorize(service_file='credentials.json')
    sheet = client.open(os.environ['GOOGLE_SHEET'])
    wks = sheet.sheet1
    wks.set_dataframe(df=df, start=(1, 1), copy_index=False, extend=True, nan='')

    print('Success!')
