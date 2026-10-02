#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# [R432] CLASSIFIED_CONSUMERS at each revision given. Usage: run inside a clone: classified_set.py <rev>...
import subprocess, sys, ast
for rev in sys.argv[1:]:
    src = subprocess.run(['git','show',f'{rev}:scripts/shape_consumer_inventory.py'],capture_output=True,text=True,check=True).stdout
    tree = ast.parse(src)
    for node in tree.body:
        t = getattr(node,'targets',None) or ([node.target] if isinstance(node,ast.AnnAssign) else [])
        if any(getattr(x,'id',None)=='CLASSIFIED_CONSUMERS' for x in t):
            d = ast.literal_eval(node.value)
            print(f'== {rev}: {len(d)} entries')
            for k,v in sorted(d.items()): print('  ',k,'=>',v)
