from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# DATABASE
db = client['health_insurance']

# COLLECTION
collection = db['health_facilities']

# query = ctrl + f
query = {"FacilityName": "Adimposo CHPS"}

for doc in collection.find(query):
    print(doc)