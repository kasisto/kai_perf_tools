import argparse, csv, time
from lib2to3.pytree import Base

from .base_helper import BaseHelper
from models.assistant import Assistant

from models.response import Response
from models.publishing import PublishingObj, PublishingPayload


class AddAssistantVersionToAssistant(BaseHelper):
    def get_assistants_and_add_versions(self, targets=['stage']):
        assistants = self.assistant_api.get()
        for assistant in assistants:
            self.add_assistant_versions_to_assistant(assistant['name'], targets=targets)

    def add_assistant_versions_to_assistant(self, assistant_id=None, targets=['stage'], assistant_secret=None):
        mt_enabled = False
        if assistant_id:
            a = Assistant(assistant_id)
            if assistant_secret:
                a.set_secret(assistant_secret)
            elif self.default_assistant_name == assistant_id:
                a.set_secret(self.default_assistant_secret)
        elif mt_enabled:
            a = Assistant(self.default_assistant_name)
        else:
            a = self.get_default_assistant()

        for target in targets:
            a_responses_api = self.get_assistant_enabled_api('responses', a, target)
            a_pub_api = self.get_assistant_enabled_api('publishing', a, target)
            self.ensure_global_segment_is_published(a, [target])
            for x in range(self.n):
                response = Response()
                res = a_responses_api.post(response)
                rev = a_responses_api.get_latest_revision(response.get_id()).get('revision_id')
                pay = PublishingPayload(PublishingObj('response', response.get_id(), rev).get_json())

                pub = a_pub_api.post_documents(target, pay)
                print(pub.json())
                print(f'Created revision id on target {target}')
                time.sleep(10)
            print(f'Successfully created {self.n} assistant versions') 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--targets')
    parser.add_argument('--n', type=int)

    args = parser.parse_args()
    n = args.n
    targets = ['stage']
    if args.targets:
        targets = args.targets.split(',')
    csv_helper = AddAssistantVersionToAssistant(n).get_assistants_and_add_versions(targets)