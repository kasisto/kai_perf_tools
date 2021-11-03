import os, requests
from .crud_base_api import CrudBaseApi

class AssistantApi(CrudBaseApi):
    
    def __init__(self, header_overrides={}):
        base_url = os.environ.get('URL')

        super().__init__(
            f'{base_url}/kai/api/v1/content/assistants', 
            os.environ.get('APPLICATION_SECRET'),
            header_overrides
        )
    
    def get(self, _id=None, status_code=200, is_query=False):
        res = super().get(_id, status_code, is_query)

        return res
    
    def post_with_autopublish(self, data, targets=['stage'], auth='automated_crud_test'):
        url = self.get_url()
        url += f'?mode=APPLY'
        if targets:
            url += f'&autopublish_to='
            for target in targets:
                url += f'{target},'
    
        res = requests.post(url, self.normalize_payload(data), headers=self.headers)
        return res.json()
