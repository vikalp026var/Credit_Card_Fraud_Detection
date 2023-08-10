import pymongo 
import pandas as pd 
import json 
uri="mongodb+srv://vikalp026varshney:Vikalp026var@cluster0.r31hq0n.mongodb.net/?retryWrites=true&w=majority"
client=pymongo.MongoClient(uri)
DATABASE_NAME="Credit_Card"
COLLECTION_NAME="collection"
df=pd.read_csv(r"D:\Credit_Card_Fraud_Detection\artifacts\creditCardFraud_28011964_120214.csv")
json_record=list(json.loads(df.T.to_json()).values())
client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
print("Succesfully insert into Mongodb")