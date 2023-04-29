import requests
from bs4 import BeautifulSoup
import json
import pickle

######################################
#   Load data
######################################
try:
    with open("data/products.json", 'r') as f:
            products = json.load(f)
    f.close()
except:
    products = {}

# GET NEW DATA

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Content-Type": "application/json"
    # 'referer': my_referer
}

params = {
    # "condition": "perfect",
    # "locationName":"osl-217b",
    # "includerangelimits": "false",
    "lastfacet": "locationName",
    # "pageLink":"5471",
    # "v":"2023.5923.0320.1-122",
    "language": "nb-no",
    # "mode":"category"
}

url = "https://www.bolia.com/api/search/outlet?"
response = requests.get(url, params=params, headers=headers)
content = response.text
page_json = json.loads(content)
nr_of_results = page_json["products"]["total"]
# print(f"Number of results {nr_of_results}\n")

# Loop through all product categories, category wise since the maximum number of data than can be queries is 1k products... no pages or higher query can be made actually :P
categories = [cat["value"] for cat in page_json["facets"][5]["options"]]
# print(f"Category values: {categories}")

# print("Plassering:")
# print(json.dumps(page_json["facets"][2], indent = 3))

locations = {}
for location in page_json["facets"][2]["options"]:
    locations[location["title"]] = {
        "ID": location["value"],
        "count": location["count"],
    }
# print(locations)

for category in categories:
    params = {
        "lastfacet": "room",
        "language": "nb-no",
        "room": category,
        "size": 1000,  # 1000 is the maximum number of products in one query This also applies to their website catually!
    }
    time.sleep(1)
    response = requests.get(url, params=params, headers=headers)
    # response = requests.get("https://www.bolia.com/api/search/outlet?condition=perfect&includerangelimits=true&language=nb-no&lastfacet=locationName&locationName=osl-217b&mode=category&pageLink=5471&v=2023.5923.0320.1-122")
    content = response.text
    page_json = json.loads(content)

    for product in page_json["products"]["results"][0]["results"]:
        # Check if product is not already in json using the URL path which needs to be unique (at least for this product), if they reuse, then this needs to be reviewed and changed
        url_id = product["urlPath"]
        discount_percentage = product["discountPercentage"]["value"]

        update = False
        if url_id not in products:
            update = True
        else:
            # Check if discount has changed for the same URL, then update URL.
            if discount_percentage != products[url_id]["discount"]:
                update = True

        if update:
            # print(json.dumps(product,indent=2))

            # Check location if product is in one of the local stores
            loc = product.get("location", "no location")
            if loc != "no location":
                location_ID = product["location"]["inventoryLocationId"]
                hub = product["location"]["hub"]
                location_name = product["location"]["name"]
            else:
                # This susually has to do with the fact that they are shipping the product directly from producer!
                location_ID = "none"
                hub = "none"
                location_name = "none"

            url_full = (
                "https://www.bolia.com/nb-no/mot-oss/butikker/online-outlet/produkt/"
                + url_id
            )
            # print(f"\nURL of product: {url_full} \n")
            list_price = product["listPrice"]["raw"]["amount"]
            sales_price = product["salesPrice"]["raw"]["amount"]

            dets = product["details"]
            design_info = product["designInformation"]
            sales_type = product["type"]
            title = product["title"]

            recID = product[
                "recId"
            ]  # Maybe this is the "unique ID that should be used? "

            # Add to products
            products[url_id] = {
                "title": title,
                "sales_type": sales_type,
                "design_info": design_info,
                "sales_price": sales_price,
                "list_price": list_price,
                "discount": discount_percentage,
                "url": url_full,
                "location_name": location_name,
                "location_ID": location_ID,
                "hub": hub,
            }

print(f"Number of products scraped: {len(products)}")

# print(json.dumps(products, indent = 3))

# Temporary store the data
with open("data/products.json", 'w') as f:
    json.dump(products, f)
f.close()





# soup = BeautifulSoup(content, 'html.parser')
# products = []

# for product in soup.find_all('div', class_='product'):
#     print(product)

# json_data = json.dumps(products)
# print(json_data)
