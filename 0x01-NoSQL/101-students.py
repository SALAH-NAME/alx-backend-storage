#!/usr/bin/env python3
""" 101-students.py  """


def top_students(mongo_collection):
    """
    top_students function
    """
    top_student = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return top_student
