#! python3
import os

import requests
from dotenv import load_dotenv

load_dotenv()

GROUPME_TOKEN = os.environ['GROUPME_TOKEN']

def msg_getter_generator(group_name=os.getenv('GROUPME_GROUP_NAME')):
    if not group_name:
        group_name = input('Enter group name: ')

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
    params={'token': GROUPME_TOKEN, 'limit': 100, 'before_id': before_msg_id}

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
    url = f'https://api.groupme.com/v3/groups'
    params={'token': GROUPME_TOKEN, 'per_page': 100}

    response = requests.get(url, params)

    groups = response.json()['response']

    for group in groups:
        if group['name'].lower() == group_name.lower():
            return group['id']

    raise ValueError('No group found with name:', group_name)


if __name__ == "__main__":
    import pandas as pd

    data = msg_getter_generator()
    df = pd.DataFrame(data)
    df['created_at'] = (pd.to_datetime(df['created_at'], unit='s', utc=True)
                          .dt.tz_convert('US/Central'))
    df.to_csv('output.csv', index=False)
