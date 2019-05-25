import getPropertyImages
import requests
import dbHandler as db
import shutil
import os.path



valid_websites = ["OnTheMarket.com"]
listing_type = "rent" # rent/buy
place_name = "Cardiff"
listings_per_page = 50
page = 1


def assignID(properties):
    counter = 0
    newProperties = list()
    for prop in properties:
        listener_url = prop["lister_url"]
        prop["_id"] = int(listener_url.split('/')[4])
        if not db.propertyExists(prop["_id"]):
            newProperties.append(prop)
            counter += 1
    print("Adding {0} new properties to the database...".format(counter))
    return(newProperties)


def downloadImages(property_dict):

    property_dict["image_locs"] = list()

    if not os.path.exists("Pictures/{0}".format(property_dict["_id"])):
        os.makedirs("Pictures/{0}".format(property_dict["_id"]))
    for link in property_dict["image_links"]:
        location = "Pictures/{0}/{1}".format(property_dict["_id"], link.split('/')[-1])

        r = requests.get(link, stream=True)
        if r.status_code == 200:
            with open(location, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                property_dict["image_locs"].append(location)

    return(property_dict)





url = "https://api.nestoria.co.uk/api?encoding=json&pretty=1&action=search_listings&country=uk&" \
                "listing_type={0}&place_name={1}&number_of_results={2}&page={3}".format(listing_type, place_name,
                                                                                        listings_per_page, page)

r = requests.get(url)

number_of_pages = r.json()['response']['total_pages']

returnedProperties = r.json()['response']['listings']


for i in range(2, number_of_pages):
    url = "https://api.nestoria.co.uk/api?encoding=json&pretty=1&action=search_listings&country=uk&" \
          "listing_type={0}&place_name={1}&number_of_results={2}&page={3}".format(listing_type, place_name,
                                                                                  listings_per_page, i)
    r = requests.get(url)
    returnedProperties.extend(r.json()['response']['listings'])
    print("Added page {0} of number_of_pages".format(i))

allProperties = list()

# Remove all results from websites which cannot be processed
for i in returnedProperties:
    if i['datasource_name'] in valid_websites:
        allProperties.append(i)
    else:
        print("Removed entry from source: {0}".format(i['datasource_name']))


allProperties = assignID(allProperties)
keysToRemove = ('construction_year', 'commission', 'datasource_name', 'img_height', 'img_url', 'img_width',
                'lister_url', 'location_accuracy', 'price_formatted', 'size', 'size_type', 'thumb_height',
                'thumb_url', 'thumb_width', 'title', 'updated_in_days', 'updated_in_days_formatted',
                'car_spaces', 'summary')


for n, prop in enumerate(allProperties):
    # Get image links
    prop["image_links"] = getPropertyImages.getImageLinks(prop['lister_url'])

    # Remove unwanted fields
    for k in keysToRemove:
        prop.pop(k, None)

    # Split up keywords into list & reassign keyword list
    prop["keywords"] = prop["keywords"].split(',')
    keywords = list()
    for i in prop["keywords"]:
        keywords.append(i.lstrip())
    prop["keywords"] = keywords

    print("Downloading images for property {0} - {1}/{2}".format(prop["_id"], n, len(allProperties)))
    prop = downloadImages(prop)
    db.insertOneEntry(prop)








