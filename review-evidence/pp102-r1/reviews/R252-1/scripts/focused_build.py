#!/usr/bin/env python3
"""Execute only complete pp_top with installed pinned Verilator, max 8 jobs."""
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
from collect import CHECKOUT, OUT, capture
from integrity import verify

verify('prebuild')
selector = Path(os.environ.get('R252_VERILATOR','$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator'))
selector_bytes = selector.read_bytes()
(OUT/'raw/installed-selector.txt').write_bytes(selector_bytes)
line = next(l for l in selector_bytes.decode().splitlines() if l.startswith('exec '))
args = shlex.split(line)
assert args[:2] == ['exec','env'] and args[-1] == '$@'
root = Path(args[2].split('=',1)[1]); driver = Path(args[3]); forwarder = root/'bin/verilator_bin'
assert args[2].startswith('VERILATOR_ROOT=')
forwarding = forwarder.read_text()
assert 'my $relpath = "../../../bin";' in forwarding
assert 'exec { "$RealBin/$relpath/$RealScript" } @ARGV;' in forwarding
binary = (forwarder.parent/'../../../bin/verilator_bin').resolve()
files = [selector,driver,forwarder,binary]
records=[]
for file in files:
    b=file.read_bytes()
    records.append({'path':str(file),'resolved':str(file.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'elf':b.startswith(b'\x7fELF')})
assert records[-1]['elf']
version=capture('raw/selector-version.txt',[str(selector),'--version'])
real_version=capture('raw/real-binary-version.txt',['env','VERILATOR_ROOT='+str(root),str(binary),'--version'])
assert b'Verilator 5.050' in version and version == real_version
actual_root=capture('raw/selector-root.txt',[str(selector),'--getenv','VERILATOR_ROOT']).decode().strip()
assert actual_root == str(root)
capture('raw/verilator-file.txt',['file',*[str(p) for p in files]])
capture('raw/compiler-version.txt',['g++','--version'])
(OUT/'raw/tool-identity.json').write_text(json.dumps(records,indent=2)+'\n')
makefile=(CHECKOUT/'tb/pp_top/Makefile').read_text()
vflags=re.search(r'^VFLAGS = (.*?)(?=\n\n)',makefile,re.M|re.S).group(1).replace('\\\n',' ')
assert vflags.count('-j 0') == 1
bounded=vflags.replace('-j 0','-j 8')
argv=['make','-C',str(CHECKOUT/'tb/pp_top'),'run','VERILATOR='+str(selector),'VFLAGS='+bounded]
capture('raw/pp-top-dry-run.log',argv[:1]+['-n']+argv[1:])
print('Running complete pp_top default + fixture, jobs 8',flush=True)
capture('raw/pp-top-full.stdout.log',argv)
tally=(CHECKOUT/'tb/pp_top/obj_dir/build_tally.txt').read_bytes()
(OUT/'raw/build-tally.txt').write_bytes(tally)
assert tally.decode().splitlines() == ['1391 0','20 0'],tally
artifacts=[]
for sub,name in [('obj_dir','Vpp_top_sim'),('obj_vid','Vpp_top_vid')]:
    exe=CHECKOUT/'tb/pp_top'/sub/name
    b=exe.read_bytes()
    artifacts.append({'path':str(exe),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'elf':b.startswith(b'\x7fELF')})
    for generated in ('Vpp_top_wrap.mk','Vpp_top_wrap_classes.mk'):
        p=exe.parent/generated
        (OUT/'raw'/(sub+'-'+generated)).write_bytes(p.read_bytes())
(OUT/'raw/build-artifacts.json').write_text(json.dumps(artifacts,indent=2)+'\n')
verify('postbuild')
print('pp_top complete: 1391 default + 20 fixture = 1411 checks, 0 failing.',flush=True)
