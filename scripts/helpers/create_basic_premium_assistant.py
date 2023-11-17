import argparse, csv, os, time

from .base_helper import BaseHelper
from models.assistant import Assistant
from models.publishing import PublishingObj, PublishingPayload


class CreateBasicPremiumAssistant(BaseHelper):
    def __init__(self, n):
        super().__init__(n)
        
    def create_basic_and_premium_assistants(self, targets, n_basic, n_premium):
        package_dir = os.chdir('package')
        packages = [i for i in os.listdir(package_dir) if 'package_for_premium' in i]
        if not packages and n_premium:
            print('No premium packages found, exiting...')
            exit(1)

        for i in range(self.n):
            print(f'Creating assistants for batch: {i+1}')
            for j in range(n_basic):
                a = Assistant()
                basic_assistant = self.assistant_api.post_with_autopublish(a, targets)
                print(basic_assistant, f'Autopublishing basic assistant: {a.name}')

            for k in range(n_premium):
                a = Assistant()
                self.assistant_api.post(a)
                a_pack_api = self.get_assistant_enabled_api('packaging', a)
                print(f'Exporting {packages[k % len(packages)]}')
                replace = a_pack_api.replace(packages[k % len(packages)])
                autopub = self.assistant_api.post_with_autopublish(a, targets)
                print(autopub, f'Autopublishing premium assistant: {a.name}')
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=int) # Number of batches of assistants to be created (7 basic, 3 premium)
    parser.add_argument('--autopublish_to') # Targets to autopublish
    parser.add_argument('--basic', type=int) # Number of basic assistants to create
    parser.add_argument('--premium', type=int) # Number of premium assistants to create

    parser.set_defaults(feature=False)

    args = parser.parse_args()
    n_batch = args.batch if args.batch else 1
    n_basic = args.basic if args.basic else 7
    n_premium = args.premium if args.premium else 3

    helper = CreateBasicPremiumAssistant(n_batch)
    assistant_ids = []

    targets = args.autopublish_to.split(',')
    helper.create_basic_and_premium_assistants(targets, n_basic, n_premium)

    # Sample usage: python -m helpers.create_basic_premium_assistant --autopublish_to=stage,prod --batch=2 --basic=7 --premium=0


