import requests
import json
import pprint


def search_by_location(location='lisbon'):
	headers = {"User-agent": "curl/7.43.0","Accept": "application/json", "user_key":'3def892746d3f3960a77cff75345f69e'}

	r=requests.get("https://developers.zomato.com/api/v2.1/search?q="+location, headers=headers)
	response = json.loads(r.content)
	pprint.pprint(response['restaurants'][1]['restaurant']['name'])
	return response['restaurants'][1]['restaurant']['name']

if __name__ == '__main__':
	search_by_location()