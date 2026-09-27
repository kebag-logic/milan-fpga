#!/usr/bin/env python3
"""Compile the reviewer probe binary from an existing fw_service_budget build.

usage: compile_probe.py <repo> <build_dir> <out_mdir>
Same Verilator arguments as fw_service_budget/build.py compile_sim(), plus a
public_flat_rd configuration for three KL_nvm_backend state registers.
"""
import json, re, subprocess, sys
from pathlib import Path
here = Path(__file__).resolve().parent
repo, build, mdir = (Path(a).resolve() for a in sys.argv[1:4])
spec = json.loads((build / 'service_spec.json').read_text())
inc = mdir.parent / (mdir.name + '-inc'); inc.mkdir(parents=True, exist_ok=True)
(inc / 'probe_config.hpp').write_text((build / 'probe_config.hpp').read_text())
for n in ('probe_flash.hpp',):
    (inc / n).write_text((here / n).read_text())
(inc / 'probe_names.hpp').write_text('#pragma once\n#define ALIVE(d) 0u\n#define BACKED(d) 0u\n#define STALE(d) 0u\n')
argv = ['verilator', '--cc', '--exe', '-j', '8', '-Wno-fatal', '-Werror-USERERROR',
        '-Wno-BLKANDNBLK', '-Wno-WIDTH', '-Wno-COMBDLY', '-Wno-CASEINCOMPLETE',
        '--top-module', 'sim', '--Mdir', str(mdir), '-O3',
        '--output-split', '5000', '--output-split-cfuncs', '500',
        '-CFLAGS', f'-O3 -std=c++17 -Wall -Wextra -I{repo}/tb/common -I{inc}',
        *['-I' + str(i) for i in spec['includes']], str(here / 'probe_public.vlt'), *spec['sources'],
        str(here / 'probe_sim_main.cpp')]
subprocess.run(argv, cwd=build / 'gateware', check=True)
hdr = (mdir / 'Vsim_sim.h').read_text()
names = {}
for var in ('alive_r', 'backed_r', 'stale_r'):
    found = sorted(set(re.findall(r'\b(milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__' + var + r');', hdr)))
    print(var, found)
    assert len(found) == 1, found
    names[var] = found[0]
(inc / 'probe_names.hpp').write_text('#pragma once\n' + ''.join(
    f'#define {m}(d) static_cast<unsigned>((d).rootp->sim->{names[v]})\n'
    for m, v in (('ALIVE', 'alive_r'), ('BACKED', 'backed_r'), ('STALE', 'stale_r'))))
subprocess.run(['make', '-C', str(mdir), '-f', 'Vsim.mk', '-j', '8'], check=True)
print('built', mdir / 'Vsim')
