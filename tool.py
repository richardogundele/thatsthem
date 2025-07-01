#all this does is to scrap information from a website

import pprint

import requests
from bs4 import BeautifulSoup as bs

def get_text(element):
	if element:
		return (text := element[-1].text) if text else '-'
	else:
		return '-'

def find_skiper_data(record):
	dds = record.select('dd')
	dts = record.select('dt')
	dictionary = {dt.text.strip(): dd.text.strip() for dt, dd in zip(dts, dds)}

	name = get_text(record.select('span[itemprop="name"]'))
	dictionary['Name'] = name

	# fish out the address
	address = get_text(record.select('span[itemprop="streetAddress"]')) 
	locality = get_text(record.select('span[itemprop="addressLocality"]')) 
	region = get_text(record.select('span[itemprop="addressRegion"]'))
	postal__code = get_text(record.select('span[itemprop="postalCode"]'))
	address = ' '.join([address, locality, region, postal__code])
	dictionary['Address'] = address

	# # skipers age
	age = get_text(record.select('.ThatsThem-record-age .active'))
	dictionary['Age'] = age
	pprint.pprint(dictionary)
	return dictionary

def make_request(name):
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1ua.ff'}
	name = name.replace(' ', '-')
	res = requests.get("https://thatsthem.com/name/" + name, headers=headers)
	if res.ok:
		soup = bs(res.text, features="html.parser")
		records = soup.select(".ThatsThem-record")
		# for record in records:
		record = records[0]
		response = find_skiper_data(record)
		return response
	else:
		print(res.reason)
		
fields = ['Phone Number', 'Alternate Phones', 'Email Address', 'Length of Residence', 
'Household Size', 'IP Address', 'Estimated Net Worth', 'Estimated Income', 'Education',
'Occupation', 'Language', 'Wealth Score', 'Green Score', 'Donor Score', 'Travel Score',
'Tech Score', 'Shopping Score', 'Name', 'Address', 'Age']

r = make_request('jean doe')
with open('thatsthem.csv', 'w') as fp:
	headings = ','.join(fields)
	fp.write(headings)

	values = ','.join([ r.get(field) for field in fields])
	fp.write(values)
