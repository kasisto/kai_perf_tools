import argparse, json, os, requests
from models.cms_doc import Assistant, CmsDoc
from models.publishing import PublishingObj, PublishingPayload

class PerformanceHelpers:
    def __init__(self):
        self.url = os.environ.get('URL')
        self.headers = {
            'secret': os.environ.get('ASSISTANT_SECRET'),
            'assistant_name': os.environ.get('ASSISTANT_NAME')
        }
        self.application_headers = {
            'secret': os.environ.get('APPLICATION_SECRET')
        }

    def post(self, path, data, headers, auth):
        full_path = self.url + path
        return requests.post(full_path, headers=headers, data=data, auth=auth)

    def get_latest_revision(self, _id, headers, auth):
        full_path = url + f'/kai/api/v1/content/segments/{_id}/revisions/latest'
        print(requests.get(full_path, headers=headers, auth=auth).json())
        return requests.get(full_path, headers=headers, auth=auth).json()

    def publish(self, data, headers, auth): 
        full_path = self.url + '/kai/api/v1/publishing/stage/documents'
        return requests.post(full_path, headers=headers, data=data, auth=auth)
    
    def ensure_global_segment_is_published(self, assistant=None, target='stage'):
        """
        Ensure that the global segment is published to the target
        """
        path = '/kai/api/v1/content/segments'

        res = self.post(path, CmsDoc(f'global').get_json(), self.headers, ('automated_crud_test', 'pw'))
        rev = self.get_latest_revision(f'global', self.headers, ('automated_crud_test', 'pw'))['revision_id']
        pay = PublishingPayload(PublishingObj('segment', f'global', rev).get_json()).get_json()

        pub = self.publish(pay, self.headers, ('automated_crud_test', 'pw'))


    def create_assistant_versions(self, n):
        path = self.url + '/kai/api/v1/content/segments'
        publishing_path = self.url + '/kai/api/v1/publishing/stage/documents'

        for x in range(n):
            path = '/kai/api/v1/content/segments'
            res = self.post(path, CmsDoc(f'test_{x}').get_json(), self.headers, ('automated_crud_test', 'pw'))
            rev = self.get_latest_revision(f'test_{x}', self.headers, ('automated_crud_test', 'pw'))['revision_id']
            pay = PublishingPayload(PublishingObj('segment', f'test_x', rev).get_json()).get_json()

            pub = self.publish(pay, self.headers, ('automated_crud_test', 'pw'))
            print(pub.json())


    def create_assistants(self, n):
        path = '/kai/api/v1/content/assistants'

        for x in range(n):
            assistant = Assistant(f'test_{x}').get_json()
            res = self.post(path, assistant, self.application_headers, ('automated_crud_test', 'pw'))
            print(res.json())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--assistant')
    parser.add_argument('--n', type=int)
    args = parser.parse_args()
    url = 'https://ncr-mt-en-us-qa.kitsys.net:8090'
    perf_helper = PerformanceHelpers()
    perf_helper.ensure_global_segment_is_published()

    if args.assistant == 'True':
        perf_helper.create_assistants(args.n)
    else:
        perf_helper.create_assistant_versions(args.n)

