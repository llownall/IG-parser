import logging

import requests

from settings import *


def get_token(code):
    try:
        token_response = requests.get(VK_TOKEN_URL, params={
            'client_id': APP_ID,
            'client_secret': APP_SECRET,
            'redirect_uri': f'{BASE_URL}/vk',
            'code': code,
        })
        print(token_response.json())
        return token_response.json().get('access_token')
    except Exception as exp:
        print(exp)
        return exp


def get_group_data(access_token, group_id):
    try:
        token_response = requests.get(VK_API_URL + 'groups.getMembers', params={
            'access_token': access_token,
            'group_id': group_id,
            'fields': 'connections',
            'v': '5.126',
        })

        people = token_response.json()['response']['items']

        result = []
        for human in people:
            if 'instagram' in human:
                result.append({
                    'first_name': human.get('first_name', '...'),
                    'last_name': human.get('last_name', '...'),
                    'vk_id': human['id'],
                    'ig_name': human['instagram'],
                })
        return result, True
    except Exception as exp:
        print(exp)
        return exp, False
