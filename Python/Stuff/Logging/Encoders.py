import json

class ClassJsonEncoder(json.JSONEncoder) :
    def default(self, o) :
        return o.__dict__