import argparse, csv, os
from .create_assistants import CreateAssistant
from .create_assistant_versions import CreateAssistantVersions


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_assistants', type=int)
    parser.add_argument('--n_versions', type=int)
    parser.add_argument('--package')
    parser.add_argument('--autopublish_to')
    parser.set_defaults(feature=False)

    args = parser.parse_args()
    assistant_helper = CreateAssistant(args.n_assistants)
    n_versions = args.n_versions
    if args.package:
        replace = assistant_helper.pack_api.replace(args.package)
    if args.autopublish_to:
        targets = args.autopublish_to.split(',')
        assistant_helper.create_assistants(autopublish=True, targets=targets)
        n_versions = n_versions - 1 # Reduce number of assistant version since autopublishing will create an assistant version
    else:
        assistant_helper.create_assistants()

    assistant_versions_helper = CreateAssistantVersions(n_versions)

    full_path = os.path.dirname(__file__) + '/../assistants.csv'
    with open(full_path, 'r', encoding='UTF8', newline='') as f:
        csv_reader = csv.reader(f, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                print(row[0], row[1], row[2])
                assistant_versions_helper.create_assistant_versions(assistant_id=row[0], targets=[row[1]])
                line_count += 1