import json, requests


class CmsDoc:
    def __init__(self, name):
        self.name=name
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
            'description': self.description
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


class Assistant(CmsDoc):
    
    def __init__(self, name=None):
        
        _id = name if name else utils.get_uid(25)
        super().__init__(_id)

        self.display_name = _id
        self.locale = 'en_US'
        self.default = {
            'endpoints': {
                'iapi': {'secret': _id},
                'capi': {'secret': _id},
                'eapi': {'secret': _id}
            }
        }
        self.targets = [
            {
                'name':'prod',
                'display_name': 'production',
                'primary': True,
                'endpoints':{
                    'capi': {'secret': f'{_id}_prod'},
                    'eapi': {'secret': f'{_id}_prod'}
                }
            },
            {
                'name':'stage',
                'display_name': 'staging',
                'primary': False,
                'endpoints':{
                    'capi': {'secret': f'{_id}_stage'},
                    'eapi': {'secret': f'{_id}_stage'}
                }
            }
        ]
    
    
    def __repr__(self):
        res = json.loads(super().__repr__())
        
        res.update({
            'display_name': self.display_name,
            'locale': self.locale,
            'default': self.default,
            'targets': self.targets  
        })
        
        return str(res)
    
    def get_json(self):
        res = json.loads(super().__repr__())
        
        res.update({
            'display_name': self.display_name,
            'locale': self.locale,
            'default': self.default,
            'targets': self.targets  
        })
        
        return str(json.dumps(res))