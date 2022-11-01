import json 
import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt
import time
import requests 
from bs4 import BeautifulSoup as Soup 
import seaborn as sns 
import os 


def get_results(url): 
    request = requests.get(url,timeout=2)
    soup = Soup(request.content,features='lxml')
    parties = soup.findAll('parti')
    results = {}
    kreds = soup.find("sted")['id']
    finished = soup.find("status")['kode']
    for parti in parties: 
        results[parti['id']] = int(parti['stemmerantal'])
    return results,kreds,finished

def district_vote_quotient(parties,votes,district): 
    seats = vote_allocation_dict[district]
    votes_raw = votes
    quotient = [1] * len(parties)
    party_seats = [0] * len(parties)
 
    for i in range(int(seats)):
        winner = votes.index(max(votes))
        quotient[winner] += 1
        party_seats[winner] += 1
        votes[winner] = votes_raw[winner] / quotient[winner]
    results = {}
    for idx,party in enumerate(parties):
        results[party] = party_seats[idx]
    return results 

def votes_district(results,parties):
        red = 0 
        blue = 0
        if results == {}: 
            return 0,0,0
        for i in results:
            if i == "":
                continue 
            if parties[i]['Wing'] == "Red":
                red += int(results[i])
            else:
                blue += int(results[i])
        total = red + blue 
        return red, blue, total 

zero_time = time.time()
vote_allocation_dict = {
    "10": 15,
    "11": 11,
    "12": 10,
    "13": 2,
    "14": 21,
    "15": 12,
    "16": 18,
    "17": 17,
    "18": 14,
    "19": 15
}
stor_kreds_parties = ['5905','1487618','1962272','5897','5893','5891',"Ikke fordelt",'1962293','5903','5895','5907','5901','5899','1675319','1968075']

colors = [(194/255, 27/255, 62/255,1),(0, 1, 0,1),(242/255, 227/255, 208/255,1),(191/255, 4/255, 24/255,1),(212/255, 0/255, 127/255,1),(204/255, 17/255, 48/255,1),(220/255,220/255,220/255,1),(122/255, 40/255, 133/255,1),(0, 83/255, 146/255,1),(0, 62/255, 44/255,1),(255/255, 102/255, 0, 1), (240/255, 81/255, 35/255,1), (231/255, 208/255, 30/255,1),(0, 68/255, 80/255,1),(18/255, 114/255, 194/255,1)]

# stor_kreds_parties = ['5905','1487618','5897','5893','5891',"Ikke fordelt",'5903','5895','5907','5901','5899','1675319']

# colors = [(194/255, 27/255, 62/255,1),(0, 1, 0,1),(191/255, 4/255, 24/255,1),(212/255, 0/255, 127/255,1),(204/255, 17/255, 48/255,1),(220/255,220/255,220/255,1),(0, 83/255, 146/255,1),(0, 62/255, 44/255,1),(255/255, 102/255, 0, 1), (240/255, 81/255, 35/255,1), (231/255, 208/255, 30/255,1),(0, 68/255, 80/255,1)]
color_dict = {i:colors[idx] for idx,i in enumerate(stor_kreds_parties)}

with open("./data/parties.json","r") as infile:
    parties = json.load(infile)
with open("./data/xml_urls.json","r") as infile:
    kredse = json.load(infile)
with open("./data/stor_xml_urls.json","r") as infile:
    storkredse = json.load(infile)
start_time = time.time()  - zero_time
diff_time = 0 
while True: 
    #### 
    #### Valgkredse 
    ####
    results = {}
    for kreds in kredse:
        tmp_result, tmp_kreds, finished = get_results(kreds)
        results[tmp_kreds] = tmp_result

    #### 
    #### Storkredse  
    ####
    stor_kreds_results = [0] * len(stor_kreds_parties)
    for kreds in storkredse: 
        tmp_result,tmp_kreds,finished = get_results(kreds)
        if finished == "1":
            tmp_votes = []
            tmp_parties = []
            for i in tmp_result:
                if i in stor_kreds_parties:
                    tmp_votes.append(tmp_result[i])
                    tmp_parties.append(i)
            vote_tally = district_vote_quotient(tmp_parties,tmp_votes,tmp_kreds)
            for i in vote_tally:
                stor_kreds_results[stor_kreds_parties.index(i)] += vote_tally[i]

    tmp_total = sum(stor_kreds_results)
    ikke_fordelt_idx = stor_kreds_parties.index("Ikke fordelt")
    stor_kreds_results[ikke_fordelt_idx] = 135 - tmp_total 
    #print(stor_kreds_results)
    stor_kreds = {
        'Parties': [parties[i]['Party'] if i != "Ikke fordelt" else "Ikke fordelt" for i in stor_kreds_parties],
        'Votes': stor_kreds_results
        }
    # print(stor_kreds)
    plt.figure(figsize=(1890/96,300/96),dpi=96)
    sns.set(rc = {'figure.figsize':(1890/96,300/96),'axes.labelsize':18.0,'axes.titlesize': 25.0,'font.size': 25.0})
    ax = sns.barplot(stor_kreds,y="Parties",x="Votes",errorbar=None,palette=colors,label=stor_kreds['Votes'])
    
    #ax = sns.catplot(stor_kreds,kind="bar",y="Parties",x="Votes",errorbar=None,label=stor_kreds['Votes'],palette=colors)
    ax.set(title="Sikre mandater")
    
    # ax.figure.savefig(f"./data/charts/chart.{number}.png", format="png")
    ax.figure.savefig(f"./data/charts/chart.0.svg", format="svg",bbox_inches="tight")


    

    aggregated = {}
    for district in results:
        tmp = votes_district(results[district],parties)
        if (tmp[0],tmp[1],tmp[2]) == (0,0,0):
            aggregated[district] = {
            "Red": 0,
            "Blue": 0,
            "Color": (128/255,128/255,128/255,1)
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
            "Color": color
        }



    results = {
        "opstilling": [],
        "Color": [],
    }

    for i in aggregated: 
        results["opstilling"].append(int(i))
        results['Color'].append(aggregated[i]['Color'])



    result_df = pd.DataFrame(results)
    result_df['opstilling'] -= 19


    geo = gpd.read_file("./test_data/geo/opstillingskreds.shp")

    geo['opstilling'] = geo['opstilling'].astype(int)
    geo = pd.merge(geo,result_df,left_on="opstilling",right_on='opstilling')
    plt.close()
    plt.figure(figsize=(480/96,720/96),dpi=96)
    ax = geo.plot(color=geo['Color'],figsize=(480/96,720/96))

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.margins(x=0)
    # ax.figure.savefig(f"./data/maps/map.{number}.png", format="png")
    ax.figure.savefig(f"./data/maps/map.0.svg", format="svg",bbox_inches="tight")
    plt.close()
    sns.reset_defaults()
    end_time = time.time() - zero_time    
    #time.sleep(119-(end_time-start_time))
    start_time = time.time() - zero_time 
    
    

