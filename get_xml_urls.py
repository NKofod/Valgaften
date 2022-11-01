import requests 
from bs4 import BeautifulSoup as Soup 
import json 

base_url = "https://www.dst.dk/valg/Valg1968094/xml/valgdag.xml"

base_request = requests.get(base_url)

base_soup = Soup(base_request.content,features='lxml')
kredse = base_soup.findAll("opstillingskreds")
links = []
for kreds in kredse: 
    links.append(kreds['filnavn'])
with open("./data/xml_urls.json", "w") as outfile:
    json.dump(links,outfile,indent=4)
    