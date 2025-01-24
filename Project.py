import pandas as pd
import json
from pymongo import MongoClient

uri = "your_mongodb_uri_here"
client = MongoClient(uri)

df = pd.read_csv(r'C:\Users\SAI\Documents\DA\Project One\notebook\wafer_23012020_041211.csv')
df = df.drop('Unnamed: 0', axis=1)

json_record = list(json.loads(df.T.to_json()).values())