import json 
import pandas as pd 
import geopandas as gpd 
import matplotlib
import time
import requests 
from bs4 import BeautifulSoup as Soup 

def get_results(url): 
    request = requests.get(url)
    soup = Soup(request.content,features='lxml')
    parties = soup.findAll('parti')
    results = {}
    kreds = soup.find("sted")['id']
    finished = soup.find("status")['kode']
    for parti in parties: 
        results[parti['id']] = parti['stemmerantal']
    return results,kreds,finished


zero_time = time.time()
number = 0 

while True: 
    print(time.time() - zero_time)
    start_time = time.time()  - zero_time
    

    with open("./data/xml_urls.json","r") as infile:
        kredse = json.load(infile)
    results = {}
    for kreds in kredse:
        tmp_result, tmp_kreds, finished = get_results(kreds)
        
        results[tmp_kreds] = tmp_result
    with open(f"./data/resultater_{number}.json", "w") as outfile:
        json.dump(results,outfile,indent=4) 

    with open("./data/parties.json","r") as infile:
        parties = json.load(infile)
    # with open(f"./data/resultater.json", "r") as infile:
    #     results = json.load(infile)

    def rgb_to_hex(rgb):
        return '%02x%02x%02x' % rgb


    def votes_district(results):
        red = 0 
        blue = 0
        if results == {}: 
            return 0,0,0
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
        if (tmp[0],tmp[1],tmp[2]) == (0,0,0):
            aggregated[district] = {
            "Red": 0,
            "Blue": 0,
            "Color": (128/255,128/255,128/255,1),
        }
            continue 
        if tmp[0] > tmp[1]: 
            color = (1-(tmp[0]/tmp[2]),0,0,1)
        elif tmp[1] > tmp[0]: 
            color = (0,0,1-(tmp[1]/tmp[2]),1)
        else: 
            color = (tmp[0]/tmp[2],0,tmp[1]/tmp[2],0.5)
        aggregated[district] = {
            "Red": tmp[0]/tmp[2],
            "Blue": tmp[1]/tmp[2],
            "Color": color,
        }



    with open("tmp.json","w") as outfile:
        json.dump(aggregated,outfile,indent=4)
    results = {
        "opstilling": [],
        "Color": [],
    }

    for i in aggregated: 
        results["opstilling"].append(int(i))
        results['Color'].append(aggregated[i]['Color'])



    with open("tmp.json","w") as outfile:
        json.dump(results,outfile,indent=4)
    result_df = pd.DataFrame(results)
    result_df['opstilling'] -= 19
    geo = gpd.read_file("./test_data/geo/opstillingskreds.shp")

    geo['opstilling'] = geo['opstilling'].astype(int)
    geo = pd.merge(geo,result_df,left_on="opstilling",right_on='opstilling')


    geo_out = pd.DataFrame()
    geo_out['opstilling'] = geo['opstilling']
    geo_out['Color'] = geo['Color']
    geo_out.to_csv("tmp.csv")

    #ax = geo.plot(column='Result',cmap=RdBu_4.mpl_colormap)
    ax = geo.plot(color=geo['Color'],figsize=(19,10))

    ax.get_xaxis().set_visible(False)

    #hide y-axis 
    ax.get_yaxis().set_visible(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.margins(x=0)
    ax.figure.savefig(f"map.{number}.png", format="png")
    ax.figure.savefig(f"map.{number}.svg", format="svg")

    number += 1 
    end_time = time.time() - zero_time
    print(time.time() - zero_time)
    # time.sleep(120-(end_time-start_time))
