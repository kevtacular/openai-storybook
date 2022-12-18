"""
Utility functions.

Functions:

    to_json(object) -> str
"""
import json


def to_json(an_object: object) -> str:
    """
    Convert object to JSON string.
    """
    return json.dumps(an_object.__dict__, default=lambda o: o.__dict__, indent=True)
