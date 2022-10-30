import requests 
from bs4 import BeautifulSoup as Soup 
import json 
import time 
import pandas as pd 


def get_results(url): 
    request = requests.get(url)
    soup = Soup(request.content,features='lxml')
    parties = soup.findAll('parti')
    results = {}
    kreds = soup.find("sted")['id']
    for parti in parties: 
        results[parti['id']] = parti['stemmerantal']
    return results,kreds 

with open("./test_data/xml_urls.json","r") as infile:
    kredse = json.load(infile)
results = {}
for kreds in kredse:
    tmp_result, tmp_kreds = get_results(kreds)
    results[tmp_kreds] = tmp_result
with open("./test_data/resultater.json", "w") as outfile:
    json.dump(results,outfile,indent=4)

with open("./test_data/parties.json","r") as infile:
    parties = json.load(infile)

with open("./test_data/resultater.json", "r") as infile: 
    results = json.load(infile)

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def votes_district(results):
    red = 0 
    blue = 0
    for i in results:
        if i == "":
            continue 
        if parties[i] == "Red":
            red += int(results[i])
        else:
            blue += int(results[i])
    total = red + blue 
    return red, blue, total 

aggregated = {}
for district in results:
    tmp = votes_district(results[district])
    aggregated[district] = {
        "Red": tmp[0]/tmp[2],
        "Blue": tmp[1]/tmp[2],
        "Color": (255*tmp[0]/tmp[2],0,255*tmp[1]/tmp[2]),
        "Hex_color": rgb_to_hex((int(255*tmp[0]/tmp[2]),0,int(255*tmp[1]/tmp[2])))
    }



