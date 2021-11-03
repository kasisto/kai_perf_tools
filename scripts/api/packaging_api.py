import os, requests
from .base_api import BaseApi


class PackagingApi(BaseApi):
    def __init__(self, header_overrides={}):
        base_url = os.environ.get('URL')
        if header_overrides:
            self.headers = header_overrides
        else:
            self.headers = {
                'secret': os.environ.get('PACKAGING_SECRET')
            }

        super().__init__(
            f'{base_url}/kai/api/v1/package', 
            self.headers
        )

    def replace(self, package_name, mode='APPLY', type='ALL'):
        url = self.get_url('replace')
        if mode:
            url += f'?mode={mode}'
        if type:
            url += f'&type={type}'

        package_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'package'))
        file = {
            'package': open(f'{package_folder}/{package_name}', 'rb')
        }
        res = requests.post(url, headers=self.headers, files=file)
        return res.json()