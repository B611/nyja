from typing import List, Dict
import json as j
import os


def simple(cmd_out: List[str], export: str):
    if cmd_out:
        with open(export, 'a') as f:
            f.write('\n'.join(cmd_out) + '\n')
            f.close()
            print('Command output successfully exported to {}'.format(export))


def json(cmd_out: Dict, export: str):
    if cmd_out:
        if os.path.isfile(export):
            try:
                with open(export, 'r+') as json_file:
                    data = j.load(json_file)
                data.append(cmd_out)
                with open(export, 'w+') as json_file:
                    j.dump(data, json_file, indent=4, default=str)
                print('Command output successfully appended to {}'.format(export))
            except:
                with open(export, 'w+') as json_file:
                    j.dump([cmd_out], json_file, indent=4, default=str)
                print('Command output successfully exported to {}'.format(export))
        else:
            with open(export, 'w+') as json_file:
                j.dump([cmd_out], json_file, indent=4, default=str)
            print('Command output successfully exported to {}'.format(export))
    else:
        print('Command output was empty, export cancelled.')

