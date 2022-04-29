import argparse, csv, time
from lib2to3.pytree import Base

from .base_helper import BaseHelper
from models.assistant import Assistant


class CreateCSV(BaseHelper):
    def get_assistants_and_create_csv(self, targets=['stage']):
        assistants = self.assistant_api.get()
        for assistant in assistants:
            for target in targets:
                assistant_json = self.assistant_api.get(assistant["name"])
                self.assistants.append([
                    assistant_json["name"],
                    target,
                    f'{assistant_json["name"]}_{target}'
                ])
        self.generate_csv()  

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--targets')
    args = parser.parse_args()
    targets = ['stage']
    if args.targets:
        targets = args.targets.split(',')
    csv_helper = CreateCSV(1).get_assistants_and_create_csv(targets)