import argparse, csv

from .base_helper import BaseHelper
from models.assistant import Assistant
from models.publishing import PublishingObj, PublishingPayload


class CreateAssistant(BaseHelper):
    def __init__(self, n):
        self.assistants = []
        super().__init__(n)


    def generate_csv(self):
        headers = ['assistant_name', 'assistant_target', 'secret']

        with open('assistants.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(self.assistants)
    
    def create_assistants(self, autopublish=False, targets=['stage']):
        for x in range(self.n):
            assistant = Assistant()
            if autopublish:
                self.assistant_api.post_with_autopublish(assistant, targets)
            else:
                self.assistant_api.post(assistant)
            rev = self.assistant_api.get_latest_revision(assistant.get_id())['revision_id']
            pay = PublishingPayload(PublishingObj('assistant', assistant.get_id(), rev).get_json()).get_json()

            self.ensure_global_segment_is_published(assistant=assistant)
            pub = self.publishing_api.post_documents('stage', pay)
            self.assistants.append([assistant.get_id(), 'stage', f'{assistant.get_id()}_stage'])
        print(f'Successfully created {self.n} assistants')
        self.generate_csv()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int)
    parser.add_argument('--package')
    parser.add_argument('--autopublish_to')
    parser.set_defaults(feature=False)

    args = parser.parse_args()
    helper = CreateAssistant(args.n)
    if args.package:
        helper.pack_api.replace(args.package)
    if args.autopublish_to:
        targets = args.autopublish_to.split(',')
        print(targets)
        helper.create_assistants(autopublish=True, targets=targets)
    else:
        helper.create_assistants()


