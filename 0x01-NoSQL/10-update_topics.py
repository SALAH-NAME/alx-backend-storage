#!/usr/bin/env python3
""" 10-update_topics.py """


def update_topics(mongo_collection, name, topics):
    """
    update_topics function
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
