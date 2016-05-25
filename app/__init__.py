# -*- coding: utf-8 -*-
import requests
from flask import Flask, request, render_template

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    deposit = request.args['deposit'] if 'deposit' in request.args else 500
    rent = request.args['rent'] if 'rent' in request.args else 40
    params = {
        'lat_south': 37.47728517173178,
        'lat_north': 37.480090431877294,
        'lng_west': 126.95566533252335,
        'lng_east': 126.96495717452899,
        'room': ', '.join([str(x) for x in [1, 2, 3, 4, 5]]),
        'deposit_e': deposit,
        'rent_e': rent
    }

    response = requests.get('https://api.zigbang.com/v2/items', params=params)
    response_json = response.json()
    item_ids = [str(item['simple_item']['item_id']) for item in response_json['list_items']]

    api_endpoint2 = 'https://api.zigbang.com/v1/items?detail=true'
    for i in item_ids:
        api_endpoint2 = '{}&item_ids={}'.format(api_endpoint2, i)

    response = requests.get(api_endpoint2)
    response_json = response.json()
    room_list = []
    for item in response_json['items']:
        item = item['item']
        data = {
            'title': item['title'],
            'description': item['description'],
            'building_type': item['building_type'],
            'room_type': item['room_type'],
            'floor': '{}/{}'.format(item['floor'], item['floor_all']),
            'updated_at': item['updated_at'],
            'options': item['options'],
            'deposit': item['deposit'],
            'rent': item['rent'],
            'manage': '{}({})'.format(item['manage_cost'], item['manage_cost_inc']),
            'size': '{}({}평)'.format(item['size_m2'], int(item['size'])),
            'link': 'https://www.zigbang.com/items1/{}'.format(item['id']),
            'thumbnail': '{}?w=400&h=300'.format(item['images'][0]['url'])
        }
        room_list.append(data)

    return render_template('index.html', room_list=room_list)
