import json

"""
Convert object to JSON string.
"""
def to_json(an_object: object):
    return json.dumps(an_object.__dict__, default=lambda o: o.__dict__, indent=True)
