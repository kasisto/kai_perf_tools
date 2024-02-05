import csv, os
from api.responses_api import ResponsesApi
from api.packaging_api import PackagingApi

from api.assistant_api import AssistantApi
from api.packaging_api import PackagingApi
from api.publishing_api import PublishingApi
from api.intents_api import IntentsApi
from api.segments_api import SegmentsApi
from models.assistant import Assistant
from models.cms_doc import CmsDoc
from models.publishing import PublishingObj, PublishingPayload


class BaseHelper:
    def __init__(self, n):
        self.n = n
        self.headers = {
            'secret': os.environ.get('APPLICATION_SECRET')
        }
        self.default_assistant_name = os.environ.get('ASSISTANT_NAME')
        self.default_assistant_secret = os.environ.get('ASSISTANT_SECRET')
        self.assistant_api = AssistantApi()
        self.segments_api = SegmentsApi()
        self.publishing_api = PublishingApi()
        self.pack_api = PackagingApi()
        self.assistants = []
    
    def ensure_global_segment_is_published(self, assistant=None, targets=['stage']):
        """
        Ensure that the global segment is published to the target
        """
        headers = self.headers

        if assistant:
            for target in targets:
                if isinstance(assistant, dict):
                    self.headers = {
                        'secret': assistant['default']['endpoints']['iapi']['secret'], 
                        'assistant_name': assistant['name'],
                        'target': target
                    }
                    res = SegmentsApi(self.headers).post(CmsDoc(f'global').get_json())
                    rev = self.segments_api.get_latest_revision('global').get('revision_id')
                    pay = PublishingPayload(PublishingObj('segment', f'global', rev))

                    pub = self.publishing_api.post_documents(target, pay)
                else:
                    res = SegmentsApi(self.headers).post(CmsDoc(f'global').get_json())
                    if assistant.get_id() == os.environ.get('ASSISTANT_NAME'):
                        a = self.get_default_assistant()
                    else:
                        a = Assistant(assistant.get_id()).get_json()

                    self.assistant_api.post_with_autopublish(a, [target])
    
    def create_default_assistant(self):
        res = AssistantApi().get(os.environ.get('ASSISTANT_NAME'))

        if 'code' in res:
            if res['code'] == '404':
                return AssistantApi().post(Assistant(os.environ.get('ASSISTANT_NAME')))
            else:
                print('Failed to create default assistant')
                return
        return
    
    def get_default_assistant(self):
        res = AssistantApi().get(os.environ.get('ASSISTANT_NAME'))

        if 'code' in res:
            if res['code'] == '404':
                return AssistantApi().post(Assistant(os.environ.get('ASSISTANT_NAME')))
        return res

    def get_assistant(self, id):
        res = AssistantApi().get(id)

        if 'code' in res:
            if res['code'] == '404':
                print('Assistant does not exists')
                return False
        return res

    
    def get_assistant_enabled_api(self, data, assistant, target='default'):
        if isinstance(assistant, dict):
            header_overrides = {
                'secret': assistant['default']['endpoints']['iapi']['secret'], 
                'assistant_name': assistant['name']
            }
        else:
            header_overrides = {
                'secret': assistant.get_secret('iapi', target), 
                'assistant_name': assistant.get_id()
            }

        if isinstance(data, str) and data.lower() == 'publishing':
            return PublishingApi(header_overrides=header_overrides)
        if isinstance(data, str) and data.lower() == 'intents':
            return IntentsApi(header_overrides=header_overrides)
        if isinstance(data, str) and data.lower() == 'responses':
            return ResponsesApi(header_overrides=header_overrides)
        if isinstance(data, str) and data.lower() == 'segments':
            return SegmentsApi(header_overrides=header_overrides)
        if isinstance(data, str) and data.lower() == 'packaging':
            return PackagingApi(header_overrides=header_overrides)

    def generate_csv(self):
        headers = ['assistant_name', 'assistant_target', 'secret']

        with open('assistants.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(self.assistants)
    
