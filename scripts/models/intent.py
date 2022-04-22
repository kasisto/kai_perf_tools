import json, uuid
from .cms_doc import CmsDoc

import json, uuid


class Intent(CmsDoc):
    def __init__(self, name=None):
        super().__init__(name)
        self.display_sentence = "This is a display sentence"
    
    def get_json(self):
        doc = json.loads(super().get_json())
        doc['display_sentence'] = self.display_sentence
        return str(doc)
    
    def get_id(self):
        return self.name

    def set_display_sentence(self, sentence):
        self.display_sentence = sentence
