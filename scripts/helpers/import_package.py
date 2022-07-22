import argparse, csv, time

from .base_helper import BaseHelper
from models.assistant import Assistant
from models.publishing import PublishingObj, PublishingPayload


class ImportPackage(BaseHelper):
    def __init__(self, n=10):
        super().__init__(n)

    def import_package(self, targets=[], assistant_ids=[]):
        if assistant_ids:
            for assistant_id in assistant_ids:
                assistant = self.get_assistant(assistant_id)
                if assistant:
                    autopublish = self.assistant_api.post_with_autopublish(assistant, targets)
                    print(autopublish)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--package')
    parser.add_argument('--autopublish_to')
    parser.add_argument('--assistant_ids')
    parser.set_defaults(feature=False)

    args = parser.parse_args()
    helper = ImportPackage()
    assistant_ids = []
    if args.package:
        replace = helper.pack_api.replace(args.package)
        print(replace)
    if args.autopublish_to:
        targets = args.autopublish_to.split(',')
        if args.assistant_ids:
            assistant_ids = args.assistant_ids.split(',')
            print(assistant_ids, "TEST")
        helper.import_package(targets=targets, assistant_ids=assistant_ids)


