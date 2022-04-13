import argparse, csv

from .base_helper import BaseHelper
from models.assistant import Assistant
from models.cms_doc import CmsDoc
import time
from models.publishing import PublishingObj, PublishingPayload


class CreateAssistantVersions(BaseHelper):
    def create_assistant_versions(self):
        mt_enabled = False
        if mt_enabled:
            a = Assistant(self.default_assistant_name)
        else:
            a = self.get_default_assistant()
        a_seg_api = self.get_assistant_enabled_api('segments', a, 'stage')
        a_pub_api = self.get_assistant_enabled_api('publishing', a, 'stage')
        self.ensure_global_segment_is_published(a)
        for x in range(self.n):
            segment = CmsDoc()
            a_seg_api.post(segment.get_json())
            rev = a_seg_api.get_latest_revision(segment.get_id()).get('revision_id')
            pay = PublishingPayload(PublishingObj('segment', segment.get_id(), rev).get_json())

            pub = a_pub_api.post_documents('stage', pay)
            print(pub.json())
            print(f'Created revision id')
            time.sleep(10)
        print(f'Successfully created {self.n} assistant versions')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int)
    args = parser.parse_args()
    a = CreateAssistantVersions(args.n)
    a.create_default_assistant()
    a.create_assistant_versions()
