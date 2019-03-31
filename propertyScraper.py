import json
import requests


valid_websites = ["OnTheMarket.com"]


listing_type = "buy"
place_name = "Cardiff"
listings_per_page = 50
page = 1


url = "https://api.nestoria.co.uk/api?encoding=json&pretty=1&action=search_listings&country=uk&" \
                "listing_type={0}&place_name={1}&number_of_results={2}&page={3}".format(listing_type, place_name,
                                                                                        listings_per_page, page)

r = requests.get(url)

number_of_pages = r.json()['response']['total_pages']

returnedProperties = r.json()['response']['listings']

for i in range(2, 2):
    url = "https://api.nestoria.co.uk/api?encoding=json&pretty=1&action=search_listings&country=uk&" \
          "listing_type={0}&place_name={1}&number_of_results={2}&page={3}".format(listing_type, place_name,
                                                                                  listings_per_page, i)
    r = requests.get(url)
    returnedProperties.extend(r.json()['response']['listings'])
    print("Added page {0}".format(i))

allProperties = list()

# Remove all results from websites which cannot be processed
for i in returnedProperties:
    if i['datasource_name'] in valid_websites:
        allProperties.append(i)
    else:
        print("Removed entry from source: {0}".format(i['datasource_name']))
