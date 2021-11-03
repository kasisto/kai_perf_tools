import jsons, os, requests, time


class BaseApi(object):

    def __init__(self, url, headers):
        self.url = url
        self.headers = headers


    def get_url(self, ep=None, is_query=False):
        url = self.url

        if is_query and ep:
            url += f'?{ep}'
        
        if not is_query and ep:
            url += f'/{ep}'

        return url
    

    def normalize_payload(self, data):
        if isinstance(data, str):
            data = data
        elif isinstance(data, dict) or isinstance(data, list):
            data = jsons.dumps(data)
        elif data: # Want to test how APIs handle null/none payloads
            data = jsons.dumps(data.__dict__)
            
        return data
    

    def post(self, full_path, data, auth=('performance_test', 'pw')):
        return requests.post(full_path, headers=self.headers, data=data, auth=auth)
    

    def post_with_override(self, full_path, data, headers, auth=('performance_test', 'pw')):
        return requests.post(full_path, headers=headers, data=data, auth=auth)


    def put(self, full_path, data, auth=('performance_test', 'pw')):
        return requests.put(full_path, headers=self.headers, data=data, auth=auth)
    

    def get(self, full_path):
        return requests.get(full_path, headers=self.headers).json()
    

    def delete(self, full_path):
        return requests.delete(full_path, headers=self.headers)