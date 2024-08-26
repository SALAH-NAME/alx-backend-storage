#!/usr/bin/env python3
""" 11-schools_by_topic.py """


def schools_by_topic(mongo_collection, topic):
    """
    schools_by_topic function
    """
    return list(mongo_collection.find({"topics": topic}))
