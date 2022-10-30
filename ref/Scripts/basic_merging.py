import pandas as pd 
from statistics import mean
import numpy as np
import statsmodels.api as sm 
import json 
import folium 



def merge_data(attr_file): 
    with open(attr_file, "r") as infile:
        attributes = json.load(infile)
    weather_data = pd.read_csv(f'{attributes["Files"]["Base_path"]}{attributes["Files"]["Weather"]}', sep=",")
    if weather_data.isnull().values.any(): 
        return "Missing data"
    weather_data[["country","region"]]= weather_data["iso3166-2"].str.split("-",expand=True)
    weather_data = weather_data[weather_data["country"] == attributes["Country"]]
    corona_data = pd.read_csv(f'{attributes["Files"]["Base_path"]}{attributes["Files"]["Corona"]}', sep="\t")
    with open(f'{attributes["Files"]["Base_path"]}{attributes["Files"]["Metadata"]}') as f:
        country_metadata = json.load(f)
    with open(f'{attributes["Files"]["Base_path"]}{attributes["Files"]["Shapefile"]}') as f: 
        geojson = json.load(f)
    covid_region_map = {int(country_metadata["country_metadata"][i]["covid_region_code"]): country_metadata["country_metadata"][i]["iso3166-2_code"] for i in range(len(country_metadata["country_metadata"]))}
    corona_data["iso3166-2"] = corona_data["region_code"].map(covid_region_map)
    for i in attributes["Replacements"]:
        corona_data["region_name"] = corona_data["region_name"].str.replace(i,attributes["Replacements"][i])
    # print(corona_data.describe)
    merged = weather_data.merge(corona_data, on = attributes["Merge"])
    # print(merged.describe)
    for column in merged.columns: 
        try: 
            merged[column] = merged[column].astype("float")
        except ValueError:
            try: 
                merged[column] = pd.to_datetime(merged[column])
            except ValueError:
                pass 
    merged.replace([np.inf,-np.inf],np.nan,inplace=True)
    merged.dropna(inplace=True)
    
merge_data("attributes.json")
