import argparse, csv, time

from .base_helper import BaseHelper
from models.assistant import Assistant
from models.publishing import PublishingObj, PublishingPayload


class CreateAssistant(BaseHelper):
    def __init__(self, n):
        super().__init__(n)

    
    def create_assistants(self, autopublish=False, targets=['stage'], assistant_ids=[]):
        if assistant_ids:
            for assistant_id in assistant_ids:
                assistant = Assistant(assistant_id)
                if autopublish:
                    autopublish = self.assistant_api.post_with_autopublish(assistant, targets)
                    print(autopublish)
        else:
            for x in range(self.n):
                assistant = Assistant()
                if autopublish:
                    self.assistant_api.post_with_autopublish(assistant, targets)
                else:
                    self.assistant_api.post(assistant)
                for target in targets:
                    self.assistants.append([assistant.get_id(), target, f'{assistant.get_id()}_{target}'])
                print(f'Assistant {assistant.get_id()} created')
                time.sleep(10)
            print(f'Successfully created {self.n} assistants')
            self.generate_csv()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int)
    parser.add_argument('--package')
    parser.add_argument('--autopublish_to')
    parser.add_argument('--assistant_ids')
    parser.set_defaults(feature=False)

    args = parser.parse_args()
    helper = CreateAssistant(args.n)
    assistant_ids = []
    if args.package:
        replace = helper.pack_api.replace(args.package)
        print(replace)
    if args.autopublish_to:
        targets = args.autopublish_to.split(',')
        if args.assistant_ids:
            assistant_ids = args.assistant_ids.split(',')
            print(assistant_ids, "TEST")
        helper.create_assistants(autopublish=True, targets=targets, assistant_ids=assistant_ids)
    else:
        helper.create_assistants()


