import requests
import json

api_endpoint1 = 'https://api.zigbang.com/v2/items'
lat_south = 37.47728517173178
lat_north = 37.480090431877294
lng_west = 126.95566533252335
lng_east = 126.96495717452899
room = [1, 2, 3, 4, 5]
deposit_e = 8000
rent_e = 30
params = {
    'lat_south': 37.47728517173178,
    'lat_north': 37.480090431877294,
    'lng_west': 126.95566533252335,
    'lng_east': 126.96495717452899,
    'room': ', '.join('{:0>2}'.format(x) for x in [1, 2, 3, 4, 5]),
    'deposit_e': 8000,
    'rent_e': 30
}

response = requests.get(api_endpoint1, params=params)
response_json = response.json()
item_ids = [str(item['simple_item']['item_id']) for item in response_json['list_items']]
print(item_ids)

api_endpoint2 = 'https://api.zigbang.com/v1/items?detail=true'
for i in item_ids:
    api_endpoint2 = '{}&item_ids={}'.format(api_endpoint2, i)

response = requests.get(api_endpoint2)
response_json = response.json()
items = response_json['items']
for item in items:
    item = item['item']
    print(item['title'])
    print(item['description'])
    print('보증금 : {}'.format(item['deposit']))
    print('월세 : {}'.format(item['rent']))
    print('{}({}평)'.format(item['size_m2'], int(item['size'])))
    print('https://www.zigbang.com/items1/{}'.format(item['id']))
    print(item['images'][0]['url'])
    print('')
