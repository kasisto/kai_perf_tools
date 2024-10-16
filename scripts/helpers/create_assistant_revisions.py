import argparse, csv

from .base_helper import BaseHelper
from models.assistant import Assistant
from models.intent import Intent
import time
from models.publishing import PublishingObj, PublishingPayload


class CreateAssistantRevision(BaseHelper):
    def create_assistant_revisions(self):
        mt_enabled = False
        if mt_enabled:
            a = Assistant(self.default_assistant_name)
        else:
            a = self.get_default_assistant()
        a_intent_api = self.get_assistant_enabled_api('intents', a, 'stage')
        a_pub_api = self.get_assistant_enabled_api('publishing', a, 'stage')
        self.ensure_global_segment_is_published()

        intent = Intent('Test_intent')
        for x in range(self.n):
            intent.set_display_sentence(f"This is a display sentence {x}")
            intent_res = a_intent_api.post(intent)
            print(intent_res)
            rev = a_intent_api.get_latest_revision(intent.get_id()).get('revision_id')
            pay = PublishingPayload(PublishingObj('intent', intent.get_id(), rev).get_json())

            pub = a_pub_api.post_documents('stage', pay)
            print(pub.json())
            print(f'Created revision id')
            time.sleep(10)
        print(f'Successfully created {self.n} assistant versions')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int)
    args = parser.parse_args()
    a = CreateAssistantRevision(args.n)
    a.create_default_assistant()
    a.create_assistant_revisions()
