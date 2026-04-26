import os
import re
from pymongo.errors import PyMongoError
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
from bson import ObjectId
from datetime import datetime, timezone

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


def normalize_publication_document(publication_document):
    if not publication_document:
        return None
    raw_publication_id=publication_document.get("id")
    if raw_publication_id is None:
        raw_publication_id=publication_document.get("_id")
    publication_id=str(raw_publication_id)
    title=publication_document.get("title") or "(no title)"
    venue=publication_document.get("venue") or publication_document.get("booktitle") or ""
    citation_count=publication_document.get("num_citations")
    if citation_count is None:
        citation_count=publication_document.get("numCitations")
    keywords=[]
    for keyword_document in publication_document.get("keywords") or []:
        if isinstance(keyword_document, dict):
            keyword_name=keyword_document.get("name")
        else:
            keyword_name=str(keyword_document)
        if keyword_name:
            keywords.append(str(keyword_name))
    return {
        "publication_id": publication_id,
        "title": title,
        "year": publication_document.get("year"),
        "venue": venue,
        "num_citations": citation_count or 0,
        "keywords": keywords[:8],
    }


def w08_search_publications(query_text: str, limit: int=10):
    if not check_mongodb_connection():
        raise ConnectionError("we cannot connect to MongoDB. please check.")
    cleaned_query=(query_text or "").strip()
    if not cleaned_query:
        return []
    escaped_query=re.escape(cleaned_query)
    mongodb_config=get_mongodb_config()
    mongo_client=MongoClient(mongodb_config["uri"], serverSelectionTimeoutMS=8000)
    db=mongo_client[mongodb_config["database"]]
    publications=db[mongodb_config["collection"]]
    cursor=publications.find(
        {
            "$or": [
                {"title": {"$regex": escaped_query, "$options": "i"}},
                {"keywords.name": {"$regex": escaped_query, "$options": "i"}},
            ]
        },
        {
            "_id": 1,
            "id": 1,
            "title": 1,
            "year": 1,
            "venue": 1,
            "booktitle": 1,
            "num_citations": 1,
            "numCitations": 1,
            "keywords.name": 1,
        },
    ).sort([("num_citations", -1), ("numCitations", -1), ("year", -1)]).limit(int(limit))
    rows=[]
    for publication_document in cursor:
        normalized=normalize_publication_document(publication_document)
        if normalized:
            rows.append(normalized)
    mongo_client.close()
    return rows


def w08_list_favorite_publications():
    if not check_mongodb_connection():
        raise ConnectionError("we cannot connect to MongoDB. please check.")
    mongodb_config=get_mongodb_config()
    mongo_client=MongoClient(mongodb_config["uri"], serverSelectionTimeoutMS=8000)
    db=mongo_client[mongodb_config["database"]]
    favorites=db["favorite_publications"]
    rows=[]
    for favorite_document in favorites.find({}, {"_id": 0}).sort([("updated_at", -1), ("created_at", -1)]):
        rows.append(favorite_document)
    mongo_client.close()
    return rows


def w08_add_favorite_publication(publication_row):
    if not check_mongodb_connection():
        raise ConnectionError("we cannot connect to MongoDB. please check.")
    normalized=normalize_publication_document(publication_row)
    if not normalized:
        return None
    now=datetime.now(timezone.utc)
    mongodb_config=get_mongodb_config()
    mongo_client=MongoClient(mongodb_config["uri"], serverSelectionTimeoutMS=8000)
    db=mongo_client[mongodb_config["database"]]
    favorites=db["favorite_publications"]
    favorites.update_one(
        {"publication_id": normalized["publication_id"]},
        {
            "$setOnInsert": {
                "publication_id": normalized["publication_id"],
                "title": normalized["title"],
                "year": normalized.get("year"),
                "venue": normalized.get("venue") or "",
                "num_citations": normalized.get("num_citations") or 0,
                "keywords": normalized.get("keywords") or [],
                "note": "",
                "status": "To Read",
                "created_at": now,
            },
            "$set": {
                "updated_at": now,
            },
        },
        upsert=True,
    )
    mongo_client.close()
    return normalized


def w08_add_favorite_publication_by_id(publication_id):
    if not check_mongodb_connection():
        raise ConnectionError("we cannot connect to MongoDB. please check.")
    publication_id=str(publication_id)
    mongodb_config=get_mongodb_config()
    mongo_client=MongoClient(mongodb_config["uri"], serverSelectionTimeoutMS=8000)
    db=mongo_client[mongodb_config["database"]]
    publications=db[mongodb_config["collection"]]
    publication_document=publications.find_one(
        {"$or": [{"id": publication_id}, {"id": int(publication_id)}]} if publication_id.isdigit() else {"id": publication_id}
    )
    if publication_document is None:
        publication_document=publications.find_one({"_id": publication_id})
    if publication_document is None and ObjectId.is_valid(publication_id):
        publication_document=publications.find_one({"_id": ObjectId(publication_id)})
    mongo_client.close()
    return w08_add_favorite_publication(publication_document)


def w08_remove_favorite_publication(publication_id):
    if not check_mongodb_connection():
        raise ConnectionError("we cannot connect to MongoDB. please check.")
    mongodb_config=get_mongodb_config()
    mongo_client=MongoClient(mongodb_config["uri"], serverSelectionTimeoutMS=8000)
    db=mongo_client[mongodb_config["database"]]
    favorites=db["favorite_publications"]
    result=favorites.delete_one({"publication_id": str(publication_id)})
    mongo_client.close()
    return result.deleted_count


def w08_update_favorite_publication(publication_id, status, note):
    if not check_mongodb_connection():
        raise ConnectionError("we cannot connect to MongoDB. please check.")
    allowed_statuses={"To Read", "Reading", "Read", "Important"}
    cleaned_status=(status or "To Read").strip()
    if cleaned_status not in allowed_statuses:
        cleaned_status="To Read"
    cleaned_note=(note or "").strip()
    mongodb_config=get_mongodb_config()
    mongo_client=MongoClient(mongodb_config["uri"], serverSelectionTimeoutMS=8000)
    db=mongo_client[mongodb_config["database"]]
    favorites=db["favorite_publications"]
    result=favorites.update_one(
        {"publication_id": str(publication_id)},
        {
            "$set": {
                "status": cleaned_status,
                "note": cleaned_note,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )
    mongo_client.close()
    return result.modified_count