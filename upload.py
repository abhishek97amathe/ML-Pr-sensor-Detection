# Description: This script is used to upload the data from the csv file to the MongoDB database.
from pymongo.mongo_client import MongoClient 
import pandas as pd
import json

uri = 'mongodb+srv://abhishekamathe:GxLpMfwsvwFTYSM9@cluster0.klw8d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(uri)

df = pd.read_csv('C:/Users/SAI/Documents/DA/Project One/notebook/wafer_23012020_041211.csv')
df = df.drop('Unnamed: 0',axis= 1)

Database_Name = 'My_db'
Collection_Name='wafer'

json_record = list(json.loads(df.T.to_json()).values())

client[Database_Name][Collection_Name].insert_many(json_record)