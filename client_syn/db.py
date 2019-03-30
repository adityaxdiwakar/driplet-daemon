import json
import pymongo
import copy
from bson import json_util

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["driplet"]
services = db["services"]

def encoder(input):
    return copy.copy(json.loads(json_util.dumps(input)))

def last_50(serviceid):
    logs = services.find({'id': serviceid})
    logs = encoder(logs)[0]
    logs = logs["logs"]
    return logs