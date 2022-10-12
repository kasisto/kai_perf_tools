import json, uuid
from .cms_doc import CmsDoc

import json, uuid


class Response(CmsDoc):
    def __init__(self, name=None):
        super().__init__(name)
        self.default_response = {
            'message_contents': [{'type': 'TEXT', 'payload': 'testing'}],
            'quick_replies': None
        }
    
    def get_json(self):
        doc = json.loads(super().get_json())
        doc['default_response'] = self.default_response
        return str(doc)
    
    def get_id(self):
        return self.name
