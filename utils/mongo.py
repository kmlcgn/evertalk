from pymongo import MongoClient
from utils.config import MONGO_DB

# Mongo Database
mongo_db = MongoClient(MONGO_DB)
maindb = mongo_db["main"]
filtersdb = maindb["filters"]
groupsdb = mongo_db["groups"]


# This will add all messages to database
def add_msg(chatid, msg_id, text=None, photo_id=None, video_id=None, document_id=None, sticker_id=None):
    mycol = groupsdb[str(chatid)]
    data = {
        "msg_id" : msg_id,
        "text" : text,
        "photo_id" :photo_id,
        "video_id" :video_id,
        "document_id" : document_id,
        "sticker_id" : sticker_id
        }
    try:
        mycol.update_one({"msg_id": msg_id},  {"$set": data}, upsert=True)
    except:
        print('Couldnt save, check your db')

def add_filter(keyword, filter_id):
    data = {"keyword" : keyword,
            "filter_id" : str(filter_id)} # Filter id will make easier to delete filters.
    filtersdb.update_one({"keyword": keyword},  {"$set": data}, upsert=True)

def get_filters():
    query = filtersdb.find()
    return query

def del_filter(filter_id):
    checkfiltr = filtersdb.find_one({"filter_id" : str(filter_id)})
    if checkfiltr : filtersdb.delete_one({"filter_id" : str(filter_id)})

def del_all_filters():
    if str("filters") not in maindb.list_collection_names():
        return
    mycol = filtersdb
    try:
        mycol.drop()
    except:
        return