from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db = client.testing


def getQuizResult(user_id, quiz_id):
    """ Retrieves results for a quiz in user results collection
    """
    pipeline = [
        {
            "$match": {
                "user_id": user_id, 
            }
        },
        { "$project": {
            "_id": 0,
            "match": {
                "$filter": {
                    "input": "$results",
                    "as": "result",
                    "cond": {"$eq": ["$$result.quiz_id", quiz_id]}
                    }
                }
            }
        }
    ]
    match = list(db.results.aggregate(pipeline))
    if match and match[0]["match"]:
        return match[0]["match"][0]
    else:
        return None


def check(user_id):
    """ Checks if user with user_id has a results document
    return true if it does
    """
    return db.results.find_one({"user_id": user_id}, {"_id": 1}) is not None


def getByUserID(user_id):
    return db.results.find_one({"user_id": user_id})

def update(user_id, quiz_id, results):

    query = db.results.update_one(
            {"user_id": user_id},
            { "$push": {
                "results": {
                    "$each": [results],
                    "$position": 0
                    }
                }}
    )
    if query.matched_count != 1 or query.modified_count != 1:
        raise Exception("User does not have results collection")


result = {
    "user_id": "233444",
    "result_id": "223344",
    "results": [
        {
            "quiz_id": "322334434343",
            "Score": 70,
            "Attempts": 4,
            "Best score": 100,
            "timestamp": "2025-01-02T12:34:56Z"
        },
        {
            "quiz_id": "234334434243",
            "Score": 50,
            "Attempts": 5,
            "Best score": 90,
            "timestamp": "2025-01-02T12:34:56Z"
        },
        {
            "quiz_id": "123444434343",
            "Score": 70,
            "Attempts": 4,
            "Best score": 100,
            "timestamp": "2025-01-02T12:34:56Z"
        },
    ]
}

data = {
    "Score": '100',
    "Attempts": '4',
    "Best score": '100',
    "timestamp": "2025-01-02T12:34:56Z"
}

user_id = "233444"
quiz_id = "123444434343"

db.results.insert_one(result)

pprint(db.results.find_one({"user_id": user_id}))

pprint(check(user_id))
update(user_id, quiz_id, data)

pprint(db.results.find_one({"user_id": user_id}))

db.results.delete_one({"user_id": "233444"})
