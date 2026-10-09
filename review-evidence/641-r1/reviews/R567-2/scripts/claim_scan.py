#!/usr/bin/env python3
"""Inventory current and historical elaboration-enforcement statements."""
import re, subprocess, sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
names=subprocess.check_output(['git','-C',str(root),'ls-files','-z']).decode().split('\0')
scan=re.compile(r'does not enforce|not enforced on|where that contract is and is not enforced|(?:yosys|sv2v).{0,140}(?:guard|\$error|elaboration)|(?:guard|elaboration).{0,100}(?:ignore|not enforce)',re.I)
count=0;patches=0;mutants=0
for name in names:
 if not name:continue
 path=root/name
 if not path.is_file():continue
 try:lines=path.read_text().splitlines()
 except (UnicodeError,OSError):continue
 count+=1
 for i,line in enumerate(lines,1):
  if scan.search(line):print(f'{name}:{i}: {line}')
 if name.startswith('tb/') and (name.endswith('.patch') or name.endswith('.py')):
  if name.endswith('.patch'):patches+=1
  if 'mutant' in name:mutants+=1
  assert not any('It is NOT enforced on the sv2v' in x or 'sv2v lowers a module-scope $error' in x for x in lines),name
print(f'first-party tracked text files scanned={count}; tb patches={patches}; mutant tables={mutants}')
print('No tb patch/table retains the changed enforcement comment as an exact anchor.')
