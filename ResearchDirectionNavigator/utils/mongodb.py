import os
import re
from pymongo.errors import PyMongoError
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

_ROOT=Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env")

# create a function to get the mongodb configure from environment variables, with default values
def get_mongodb_config():
    # return dictionary with keys uri, database and collection
    mongo_server_address=os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
    mongo_database_name=os.getenv("MONGO_DATABASE", "academicworld")
    mongo_collection_publications="publications"
    return {
        "uri": mongo_server_address,
        "database": mongo_database_name,
        "collection": mongo_collection_publications,
    }

# create a function to check if the mongodb connection is successful
def check_mongodb_connection():
    mongodb_config = get_mongodb_config()

    mongodb_client = MongoClient(
        mongodb_config["uri"],
        serverSelectionTimeoutMS=3000
    )

    mongodb_client.admin.command("ping")
    mongodb_client.close()

    return True

# w05-create a function to count publications by year for papers based on searching keywords in MongoDB
def w05_get_research_trends_based_on_publication_numbers_with_year(keywords: str, limit: int=100):
    # first, check if the mongodb connection is successful
    if not check_mongodb_connection():
        raise ConnectionError("we cannot connect to MongoDB. please check.")
    # after the connection is successful, we can execute the query to search for papers based on keywords
    # check if the keywords is empty, if it is empty, return an empty list
    input_text=(keywords or "").strip()
    if not input_text:
        return []
    # if the input text is not empty, we can split the keywords by comma and strip the whitespace
    keyword_list=[keyword.strip() for keyword in input_text.split(",") if keyword.strip()]
    # if the list is still empty after split, return []
    if not keyword_list:
        return []
    # use only the first token; case-insensitive substring match on keywords.name (aligned with MySQL LIKE %keyword%)
    first_keyword=keyword_list[0]
    pattern=re.escape(first_keyword)
    # load the same configuration from get_mongodb_config()
    mongodb_config=get_mongodb_config()

    # create the mongo client, with time limit 
    mongo_client=MongoClient(mongodb_config["uri"], serverSelectionTimeoutMS=8000)
    # choose the database via name
    db=mongo_client[mongodb_config["database"]]
    # choose the collection 
    publications=db[mongodb_config["collection"]]
    # pipeline: match, group, sort
    match_action={
        "$match": {
            "keywords": {"$elemMatch": {"name": {"$regex": pattern, "$options": "i"}}}
        }
    }
    group_action_by_year={"$group": {"_id": "$year", "pub_count": {"$sum": 1}}}
    sort_action_by_year={"$sort": {"_id": 1}}
    pipeline=[match_action, group_action_by_year, sort_action_by_year]
    
    # loop the cursor and construct the list of dicts
    rows=[]
    for ele in publications.aggregate(pipeline):
        rows.append({"year": ele["_id"], "pub_count": ele["pub_count"]})
    mongo_client.close()

    return rows[:limit]

# W5: yearly publication counts for papers whose keywords intersect name set K from Neo4j
def w05_get_research_trends_by_keyword_name_set(keyword_names, limit=100):
    """Aggregate publications by year where keyword names are in set K from Neo4j (demo-oriented, not production-hardened)."""
    if not keyword_names:
        return []
    if not check_mongodb_connection():
        raise ConnectionError("we cannot connect to MongoDB. please check.")
    mongodb_config=get_mongodb_config()
    mongo_client=MongoClient(mongodb_config["uri"], serverSelectionTimeoutMS=8000)
    db=mongo_client[mongodb_config["database"]]
    publications=db[mongodb_config["collection"]]
    match_action={
        "$match": {"keywords": {"$elemMatch": {"name": {"$in": keyword_names}}}},
    }
    pipeline=[
        match_action,
        {"$group": {"_id": "$year", "pub_count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    rows=[]
    for ele in publications.aggregate(pipeline):
        rows.append({"year": ele["_id"], "pub_count": ele["pub_count"]})
    mongo_client.close()
    return rows[:limit]