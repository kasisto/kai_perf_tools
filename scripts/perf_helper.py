import argparse, json, requests
from models.cms_doc import Assistant, CmsDoc
from models.publishing import PublishingObj, PublishingPayload

class PerformanceHelpers:
    def __init__(self, path):
        self.url = url

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
        headers = {
            'secret': 'kaidemo-en-us-2',
            'assistant_name': 'kaidemo-en-us'
        }

        res = self.post(path, CmsDoc(f'global').get_json(), headers, ('automated_crud_test', 'pw'))
        rev = self.get_latest_revision(f'global', headers, ('automated_crud_test', 'pw'))['revision_id']
        pay = PublishingPayload(PublishingObj('segment', f'global', rev).get_json()).get_json()

        pub = self.publish(pay, headers, ('automated_crud_test', 'pw'))


    def create_assistant_versions(self, n):
        path = 'https://kaidemo-en-us-qa.kitsys.net:8090/kai/api/v1/content/segments'
        publishing_path = 'https://kaidemo-en-us-qa.kitsys.net:8090/kai/api/v1/publishing/stage/documents'
        headers = {
            'secret': 'kaidemo-en-us-2',
            'assistant_name': 'kaidemo-en-us'
        }

        for x in range(n):
            path = '/kai/api/v1/content/segments'
            res = self.post(path, CmsDoc(f'test_{x}').get_json(), headers, ('automated_crud_test', 'pw'))
            rev = self.get_latest_revision(f'test_{x}', headers, ('automated_crud_test', 'pw'))['revision_id']
            pay = PublishingPayload(PublishingObj('segment', f'test_x', rev).get_json()).get_json()

            pub = self.publish(pay, headers, ('automated_crud_test', 'pw'))
            print(pub.json())


    def create_assistants(self, n):
        path = '/kai/api/v1/content/assistants'
        headers = {
            'secret': 'ef576554-637f-11e8-adc0-fa7ae01bbebc'
        }
        for x in range(n):
            assistant = Assistant(f'test_{x}').get_json()
            res = self.post(path, assistant, headers, ('automated_crud_test', 'pw'))
            print(res.json())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--assistant')
    parser.add_argument('--n', type=int)
    args = parser.parse_args()
    url = 'https://kaidemo-en-us-qa.kitsys.net:8090'
    perf_helper = PerformanceHelpers(url)
    perf_helper.ensure_global_segment_is_published()

    if args.assistant == 'True':
        perf_helper.create_assistants(args.n)
    else:
        perf_helper.create_assistant_versions(args.n)

