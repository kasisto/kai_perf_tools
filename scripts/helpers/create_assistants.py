import argparse, csv, time

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
                print(self.assistant_api.post_with_autopublish(assistant, targets))
            else:
                self.assistant_api.post(assistant)
            self.assistants.append([assistant.get_id(), 'stage', f'{assistant.get_id()}_stage'])
            print(f'Assistant {assistant.get_id()} created')
            time.sleep(10)
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
        replace = helper.pack_api.replace(args.package)
        print(replace)
    if args.autopublish_to:
        targets = args.autopublish_to.split(',')
        helper.create_assistants(autopublish=True, targets=targets)
    else:
        helper.create_assistants()


