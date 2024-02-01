import jsons, os
from .base_api import BaseApi


class PublishingApi(BaseApi):
    def __init__(self, header_overrides={}):
        self.base_url = os.environ.get('URL')
        if header_overrides:
            headers = header_overrides
        else:
            headers = {
                'secret': os.environ.get('ASSISTANT_SECRET'),
                'assistant_name': os.environ.get('ASSISTANT_NAME')
            }

        super().__init__(
            f'{self.base_url}/kai/api/v1/publishing', 
            # os.environ.get('APPLICATION_SECRET'),
            headers
        )
    
    def post(self, target_name, pay, endpoint, pub_by, sc=200):        
        res = super().post(
            f'{self.url}/{target_name}/{endpoint}', 
            self.normalize_payload(pay),
            (pub_by, 'pw')
        )
        return res
    
    def post_documents(self, target_name, pay, pub_by='automated_tests', sc=200): 
        return self.post(target_name, jsons.dumps(pay), 'documents', pub_by,sc) 

    def get_versions(self, target_name):
        return self.get(f'{self.base_url}/kai/api/v1/publishing/versions/?target_name={target_name}')