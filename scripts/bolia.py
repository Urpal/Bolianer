import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Content-Type": "application/json"
    # 'referer': my_referer
}

# PARAMS
# condition = perfect, packingok, productok
# retailType = storepickup, hubpickup, delivery
# locationName = bgo-214b, bgo-b, boo-229b, 
# size = 1000 # probably the maximum.

# locationNameDict = {
#     "Bergen - Vaskerelven" : "bgo-214b",
#     "Bergen - LMT" : "bgo-b",
#     "Bodø - City Nord" : "boo-229b",
# }


#What is actually done behind the curtains
# https://www.bolia.com/api/search/outlet?
# condition=perfect&
# includerangelimits=true&
# language=nb-no&
# lastfacet=locationName&
# locationName=osl-217b&
# mode=category&
# pageLink=5471&
# v=2023.5923.0320.1-122




params = {
    "condition": "perfect",
    "locationName":"osl-217b",
    "includerangelimits":"true",
    "lastfacet":"locationName",
    # "pageLink":"5471",
    # "v":"2023.5923.0320.1-122",
    "language":"nb-no",
    # "mode":"category"
}



# url = "https://www.bolia.com/nb-no/mot-oss/butikker/online-outlet/"
url = "https://www.bolia.com/api/search/outlet?"
response = requests.get(url,params=params, headers=headers)
# response = requests.get("https://www.bolia.com/api/search/outlet?condition=perfect&includerangelimits=true&language=nb-no&lastfacet=locationName&locationName=osl-217b&mode=category&pageLink=5471&v=2023.5923.0320.1-122")
content = response.text
page_json = json.loads(content) #To use the json loads, we would need to use the API directly and not just the get from the website itself.
nr_of_results = page_json["products"]["total"]
for product in page_json["products"]["results"][0]["results"]:
    print(json.dumps(product,indent=2))

# print(json.dumps(page_json, indent = 3))







# soup = BeautifulSoup(content, 'html.parser')
# products = []

# for product in soup.find_all('div', class_='product'):
#     print(product)

# json_data = json.dumps(products)
# print(json_data)
