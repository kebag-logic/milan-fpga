#!/usr/bin/env python3
"""Isolate the startup delta from inherited dev changes in the epoch leg.

Usage: python3 scripts/check_dev_epoch.py CHECKOUT SIMULATOR
Requires check_epoch.py's exact-head scratch checkout. Its render harness,
build recipes, configuration, other HDL and gitlinks equal live dev. Supply
the live-dev packetizer as the single substituted input to a separate build.
"""
import hashlib
import json
import os
import subprocess
import run_focused as f

dev = 'bd884631684ccf5060339efa92263d5c3e5c262c'
rtl = 'hdl/ieee1722/aaf/KL_aaf_packetizer.sv'
source = f.SCRATCH / 'epoch-head'
suite = source / 'tb/verilator/milan_dp_render'
env = os.environ.copy()
env.update(VERILATOR=f.SIM, VERILATOR_JOBS='8', TMPDIR=str(f.SCRATCH))
dev_rtl = f.SCRATCH / 'dev-packetizer.sv'
dev_rtl.write_bytes(subprocess.check_output(['git','show',dev+':'+rtl],cwd=f.REPO))
# The source list and harness are verified against dev independently of the
# startup receipts. Generated inputs use the same unchanged generators/config.
relevant = ['hdl', 'protocol-processor', 'gptp-processor', 'third_party/verilog-axis',
            'configs', 'sw/builder', 'avdecc', 'tb/verilator/milan_dp',
            'tb/verilator/milan_dp_render', 'tb/common']
changed = subprocess.check_output(['git','diff','--name-only',dev+'..'+f.HEAD,'--',
                                   *relevant],cwd=f.REPO).decode().splitlines()
assert changed == [rtl], changed
sources = subprocess.check_output(['make','--no-print-directory','-s','-C','../milan_dp',
                                   'print-srcs'],cwd=suite,env=env).decode().split()
needle = '../../../'+rtl
assert sources.count(needle)==1
sources[sources.index(needle)] = str(dev_rtl)
obj = f.SCRATCH / 'dev-epoch-obj'
f.run('epoch-dev-build',['make','-j16','--no-print-directory','tdm8render-build',
      'VERILATOR_JOBS=8','TDM8R_MDIR='+str(obj),'SRCS='+' '.join(sources)],suite,env)
f.run('epoch-dev-run',[str(obj/'Vmilan_dp_tdm8r'),'--epoch-only'],suite,env,1)
base = (f.RECEIPTS/'epoch-dev-run.log').read_bytes()
head = (f.RECEIPTS/'epoch-head-run.log').read_bytes()
result = {'comparison_base':dev,'head':f.HEAD,'render_source_closure_delta':changed,
          'head_byte_equal_to_dev':base==head,
          'dev_sha256':hashlib.sha256(base).hexdigest(),
          'head_sha256':hashlib.sha256(head).hexdigest(),
          'bytes':len(base)}
(f.RECEIPTS/'epoch-dev-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
assert base==head
