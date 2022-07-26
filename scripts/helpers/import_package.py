import argparse, copy, csv, time

from .base_helper import BaseHelper
from models.assistant import Assistant
from models.publishing import PublishingObj, PublishingPayload
from api.packaging_api import PackagingApi


class ImportPackage(BaseHelper):
    def __init__(self, n=10):
        super().__init__(n)

    def get_assistant_secret(self, assistant, ep='iapi'):
        if assistant:
            if 'default' in assistant and 'endpoints' in assistant['default']:
                if ep in assistant['default']['endpoints'] and 'secret' in assistant['default']['endpoints'][ep]:
                    return assistant['default']['endpoints'][ep]['secret']
        return None

    def import_package(self, package, targets=[], assistant_ids=[]):
        if assistant_ids:
            for assistant_id in assistant_ids:
                assistant = self.get_assistant(assistant_id)
                if assistant:
                    assistant = copy.deepcopy(assistant)
                    secret = self.get_assistant_secret(assistant)
                    headers = {
                        'secret': secret,
                        'assistant_name': assistant.get('name')
                    }
                    print('Importing package to assistant')
                    replace = PackagingApi(header_overrides=headers).replace(package, type='DATA')
                    print(replace)
                    autopublish = self.assistant_api.post_with_autopublish(assistant, targets)
                    print(autopublish)

    def import_package_with_application(self, targets=[], assistant_ids=[]):
        if assistant_ids:
            for assistant_id in assistant_ids:
                assistant = self.get_assistant(assistant_id)
                if assistant:
                    autopublish = self.assistant_api.post_with_autopublish(assistant, targets)
                    print(autopublish)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--package')
    parser.add_argument('--import_to')
    parser.add_argument('--autopublish_to')
    parser.add_argument('--assistant_ids')
    parser.set_defaults(feature=False)

    args = parser.parse_args()
    helper = ImportPackage()
    assistant_ids = []
    if args.package:
        if args.import_to:
            if args.import_to == 'application':
                replace = helper.pack_api.replace(args.package)
                print(replace)
                if args.autopublish_to and args.assistant_ids:  
                    targets = args.autopublish_to.split(',')
                    assistant_ids = args.assistant_ids.split(',')
                    helper.import_package_with_application(targets=targets, assistant_ids=assistant_ids)
            elif args.import_to == 'assistant':
                if args.autopublish_to and args.assistant_ids:
                    targets = args.autopublish_to.split(',')
                    assistant_ids = args.assistant_ids.split(',')
                    helper.import_package(args.package, targets=targets, assistant_ids=assistant_ids)
            else:
                print('Please set --import_to to either application or assistant')
        else:
            print('Please set --import_to to either application or assistant')
    else:
        print('No package name was supplied')


