import json, uuid


class CmsDoc:
    def __init__(self, name=None):
        self.name = name if name else str(uuid.uuid4())[-25:]
        self.display_name = f'dummy_display_name_{name}'
        self.state = 'SAVED'
        self.categorization = {'tags': ['tags'], 'skill': 'skill'}
        self.notes = f'{name}_notes'
        self.description = f'{name} description from automated tests'
    
    def __repr__(self):
        return str(json.dumps({
            'name': self.name,
            'display_name': self.display_name,
            'state': self.state,
            'categorization': self.categorization,
            'notes': self.notes,
            'description': self.description,
        }))
    
    def get_json(self):
        return str(json.dumps({
            'name': self.name,
            'display_name': self.display_name,
            'state': self.state,
            'categorization': self.categorization,
            'notes': self.notes,
            'description': self.description
        }))
    
    def get_id(self):
        return self.name

