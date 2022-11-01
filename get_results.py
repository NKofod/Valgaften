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



