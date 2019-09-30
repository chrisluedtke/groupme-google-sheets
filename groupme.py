#! python3
import os

import requests


GROUPME_TOKEN = os.environ['GROUPME_TOKEN']
GROUPME_GROUP_NAME = os.environ['GROUPME_GROUP_NAME']


def get_all_msgs(group_name=GROUPME_GROUP_NAME):
    group_id = get_group_id(group_name)

    all_group_msgs = []
    last_msg_id = None

    while True:
        next_100_msgs = get_recent_messages(
            group_id=group_id,
            before_msg_id=last_msg_id
        )

        if next_100_msgs:
            all_group_msgs.extend(next_100_msgs)
            last_msg_id = next_100_msgs[-1]['id']
        else:
            return all_group_msgs


def get_recent_messages(group_id, before_msg_id=None):
    url = f'https://api.groupme.com/v3/groups/{group_id}/messages'
    params={'token': GROUPME_TOKEN, 'limit': 100, 'before_id': before_msg_id}

    response = requests.get(url, params)

    if response.status_code == 304:
        print('Error 304: No previous messages found.')
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
