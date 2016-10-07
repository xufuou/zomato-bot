import requests
import json
import os
import pprint
from random import randint
from dotenv import load_dotenv
load_dotenv(".env")


headers = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key":os.environ.get("ZOMATO_USER_KEY")}


def get_random_restaurant(location='lisbon',category=None):

    city_id = get_city_id(location)
    if not city_id:
		return 'City not found'
    if category:
        category = int(category)
        if category > 0 and category <= 14:
            print 'Got into category'
            r = requests.get('https://developers.zomato.com/api/v2.1/search?entity_id=' + str(city_id) + '&entity_type=city&category='+str(category)+'&sort=rating&order=desc', headers=headers)
        else:
            return 'Category not found'
    else:
        r = requests.get('https://developers.zomato.com/api/v2.1/search?entity_id=' + str(city_id) + '&entity_type=city&sort=rating&order=desc', headers=headers)

    response = json.loads(r.content)
    if response['results_found'] > 0:
        index = randint(0,len(response['restaurants'])-1)
        return '*'+response['restaurants'][index]['restaurant']['name'].upper()+'*' + ' \n' + response['restaurants'][index]['restaurant']['url']

    return 'Well probably it is time you try something different'


def get_city_id(city='lisbon'):
    r = requests.get("https://developers.zomato.com/api/v2.1/cities?q="+city, headers=headers)
    response = json.loads(r.content)
    #only gets the first result
    if response['location_suggestions']:
    	return response['location_suggestions'][0]['id']
    return ''


def get_categories():
    r = requests.get("https://developers.zomato.com/api/v2.1/categories", headers=headers)
    response = json.loads(r.content)
    categories = ''

    for category in response['categories']:
        categories += '*(' + str(category['categories']['id']) + ')* ' + category['categories']['name'] + ' \n'

    return categories


def get_restaurant_by_category(category):
    r = requests.get("https://developers.zomato.com/api/v2.1/categories", headers=headers)
    response = json.loads(r.content)
    ids = []

    for category in response['categories']:
        ids.append(category['categories']['id'])
    return ids[randint(0,len(ids)-1)]


if __name__ == '__main__':
    get_categories()
