import json

class JSONCustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, object):
            return obj.to_dict()
        
        return super().default(obj)