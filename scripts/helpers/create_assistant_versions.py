import argparse, csv

from .base_helper import BaseHelper
from models.assistant import Assistant
from models.intent import Intent
import time
from models.publishing import PublishingObj, PublishingPayload


class CreateAssistantVersions(BaseHelper):
    def create_assistant_versions(self, assistant_id=None, targets=['stage'], assistant_secret=None):
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
            a_intent_api = self.get_assistant_enabled_api('intents', a, target)
            a_pub_api = self.get_assistant_enabled_api('publishing', a, target)
            self.ensure_global_segment_is_published(a, [target])
            for x in range(self.n):
                intent = Intent()
                res = a_intent_api.post(intent)
                rev = a_intent_api.get_latest_revision(intent.get_id()).get('revision_id')
                pay = PublishingPayload(PublishingObj('intent', intent.get_id(), rev).get_json())

                pub = a_pub_api.post_documents(target, pay)
                print(pub.json())
                print(f'Created revision id on target {target}')
                time.sleep(10)
            print(f'Successfully created {self.n} assistant versions')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int)
    parser.add_argument('--autopublish_to')
    parser.add_argument('--assistant_id')
    parser.add_argument('--assistant_secret')

    args = parser.parse_args()
    n = args.n
    targets = ['stage']
    assistant_id = None
    assistant_secret = None
    if args.assistant_id:
        assistant_id = args.assistant_id

    if args.autopublish_to:
        targets = args.autopublish_to.split(',')
        n = n - 1

    if args.assistant_secret:
        assistant_secret = args.assistant_secret

    a = CreateAssistantVersions(n)
    a.create_default_assistant()
    a.create_assistant_versions(assistant_id, targets=targets, assistant_secret=assistant_secret)
