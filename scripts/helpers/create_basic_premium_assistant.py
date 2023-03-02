import argparse, csv, os, time

from .base_helper import BaseHelper
from models.assistant import Assistant
from models.publishing import PublishingObj, PublishingPayload


class CreateBasicPremiumAssistant(BaseHelper):
    def __init__(self, n):
        super().__init__(n)
        
    def create_basic_and_premium_assistants(self, targets):
        package_dir = os.chdir('package')
        packages = [i for i in os.listdir(package_dir) if 'package' in i]
        for i in range(self.n):
            print(f'Creating assistants for batch: {i}')
            for j in range(7):
                a = Assistant()
                basic_assistant = self.assistant_api.post_with_autopublish(a)
                print(basic_assistant, ' Autopublishing basic assistant')

            for k in range(3):
                a = Assistant()
                self.assistant_api.post(a)
                a_pack_api = self.get_assistant_enabled_api('packaging', a)
                replace = a_pack_api.replace(packages[k % 2]) # We have 2 packages so the logic here is check if i is odd or even
                autopub = self.assistant_api.post_with_autopublish(a, targets)
                print(autopub, ' Autopublishing premium assistant')
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=int) # Number of batches of assistants to be created(7 basic, 3 premium)
    parser.add_argument('--autopublish_to') # Targets to autopublish
    parser.set_defaults(feature=False)

    args = parser.parse_args()
    n_batch = args.batch if args.batch else 1
    helper = CreateBasicPremiumAssistant(n_batch)
    assistant_ids = []

    targets = args.autopublish_to.split(',')
    helper.create_basic_and_premium_assistants(targets)


