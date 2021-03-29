import os
import sys
from typing import Dict

with open('/opt/sftpy/conf/folders.conf') as file:
    folders = [p.strip() for p in file.read().split("\n") if p.strip() != '' and '#' not in p]

with open('/etc/group') as file:
    groups = [p.strip() for p in file.read().split("\n") if p.strip() != '' and '#' not in p]

gids: Dict = dict()
for folder in folders:
    group = folder.split(":")[0]
    param = folder.split(":")[1]

    if '/data' in param:
        name = param.split("/")[len(param.split("/")) - 1]
        if [n for n in groups if name in n] == 1:
            print(f"Group [{name}] already exists")
            sys.exit(os.EX_CONFIG)

        gids[group] = name
        print(f"Setting up [{param}]")
        os.system(f"mkdir -p {param}")
        os.system(f"chmod g+s {param}")
        os.system(f"chmod 770 {param}")
        os.system(f"addgroup -g {group} {name}")
        os.system(f"chgrp {group} {param}")
    else:
        for user in param.split(","):
            print(f"Adding user [{user}] to group [{gids[group]}]")
            os.system(f"addgroup {user} {gids[group]}")
            os.system(f"mkdir -p /home/{user}/{gids[group]}")
            os.system(f"mount --bind /data/{gids[group]} /home/{user}/{gids[group]}")
