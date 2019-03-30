import json
import pymongo
import copy
from bson import json_util

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["driplet"]
services = db["services"]

def encoder(input):
    return copy.copy(json.loads(json_util.dumps(input)))

def update_log(serviceid, item):
    x = services.find({'id': serviceid})
    if services.count == 0:
        return
    x = encoder(x)[0]
    if item not in x["logs"]:
        services.find_one_and_update({'id': serviceid}, {'$push': {'logs': item}})
    if len(x["logs"]) > 50:
        content = x["logs"][0]
        services.find_one_and_update({'id': serviceid}, {'$pull': {'logs': content}})