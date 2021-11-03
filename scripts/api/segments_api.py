import os
from .crud_base_api import CrudBaseApi


class SegmentsApi(CrudBaseApi):
    def __init__(self, header_overrides={}):
        base_url = os.environ.get('URL')
        if header_overrides:
            headers = header_overrides
        else:
            headers = {
                'secret': os.environ.get('ASSISTANT_SECRET'),
                'assistant_name': os.environ.get('ASSISTANT_NAME')
            }

        super().__init__(
            f'{base_url}/kai/api/v1/content/segments', 
            os.environ.get('APPLICATION_SECRET'),
            headers
        )


    def get(self, id=None, status_code=200,is_query=False):
        res = super().get(id, status_code,is_query)

        return res