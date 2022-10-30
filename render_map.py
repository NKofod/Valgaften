import drawSvg as draw 
import json 
import pandas as pd 
import geopandas as gpd 
from palettable.colorbrewer.diverging import RdBu_4
import matplotlib

gpd.read_file("./test_data/geo/opstillingskreds.shp")



with open("./test_data/geo/opstilling_modified.json","r") as infile: 
    tmp_geo = json.load(infile)

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
        #"Color": (int(255*tmp[0]/tmp[2]),0,int(255*tmp[1]/tmp[2])),
        "Result": tmp[1] - tmp[0], 
        "Hex_color": "#" + str(rgb_to_hex((int(255*tmp[0]/tmp[2]),0,int(255*tmp[1]/tmp[2]))))
    }



with open("tmp.json","w") as outfile:
    json.dump(aggregated,outfile,indent=4)
results = {
    "opstilling": [],
    "Color": [],
    "Result": []
}

for i in aggregated: 
    results["opstilling"].append(int(i))
    results['Color'].append(aggregated[i]['Hex_color'])
    results['Result'].append(aggregated[i]['Result'])



with open("tmp.json","w") as outfile:
    json.dump(aggregated,outfile,indent=4)
result_df = pd.DataFrame(results)
result_df['opstilling'] -= 19
geo = gpd.read_file("./test_data/geo/opstillingskreds.shp")

geo['opstilling'] = geo['opstilling'].astype(int)
geo = geo.join(result_df,on="opstilling",rsuffix='out')
geo_out = pd.DataFrame()
geo_out['opstilling'] = geo['opstilling']
geo_out['Color'] = geo['Color']
geo_out.to_csv("tmp.csv")

ax = geo.plot(column='Result',cmap=RdBu_4.mpl_colormap)
# ax = geo.plot(color=geo['Color'])

ax.get_xaxis().set_visible(False)

#hide y-axis 
ax.get_yaxis().set_visible(False)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

ax.figure.savefig("tmp.svg", format="svg")