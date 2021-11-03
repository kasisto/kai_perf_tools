from .base_api import BaseApi


class CrudBaseApi(BaseApi):
    def __init__(self, url, secret, header_overrides):

        super(CrudBaseApi, self).__init__(
            url,
            self.merge_dicts([{'secret': secret}, header_overrides])
        )
    
    def get(self, _id=None, status_code=200, is_query=False):
        """
        Executes a GET command to the endpoint
        """
        res = super().get(self.get_url(_id, is_query))

        return res
    
    def post(self, data,  auth='automated_crud_test'):
        res = super().post(
            self.get_url(), 
            self.normalize_payload(data), 
            (auth, 'pw')
        )
        return res.json()
    
    def merge_dicts(self, dict_list):
        """
        Merges a list of dictionaries
        """
        mega = {}
        for d in dict_list:
            if d:
                mega.update(d)
        return mega

    def get_revisions(self, _id, rev_id=None, status_code=200):
        ep = f'{_id}/revisions'
        if rev_id:
            ep += f'/{rev_id}'
        res = self.get(ep, status_code)

        return res

    def get_latest_revision(self, _id):
        return self.get_revisions(_id, 'latest')
    