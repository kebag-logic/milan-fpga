#!/usr/bin/env python3
"""Compile the exact added parser, then exercise normal and overflowing inputs."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root, out = (Path(p).resolve() for p in sys.argv[1:3])
work = out/'scratch/env-probe'
work.mkdir(parents=True,exist_ok=True)
source=(root/'tb/verilator/input_loopback/sim_main.cpp').read_text()
function=re.search(r'int env_int\(const char\* name\) \{.*?\n\}',source,re.S)[0]
(work/'parser.cpp').write_text('#include <cstdio>\n#include <cstdlib>\n'+function+'\nint main() { std::printf("%d\\n", env_int("STAMP_PPM")); }\n')
subprocess.run(['c++','-std=c++17',str(work/'parser.cpp'),'-o',str(work/'parser')],check=True)
results=[]
for value in [None,'1000','abc','1000x','2147483648','4294967296','-4294967296','99999999999999999999999999999']:
    env=dict(os.environ)
    env.pop('STAMP_PPM',None)
    if value is not None: env['STAMP_PPM']=value
    p=subprocess.run([str(work/'parser')],env=env,text=True,capture_output=True)
    results.append(dict(input=value,exit=p.returncode,stdout=p.stdout,stderr=p.stderr))
(out/'env-parser.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
