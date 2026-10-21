#!/usr/bin/env python3
"""Reproduce both-parent composition and preservation checks without editing source."""
import hashlib
import pathlib
import re
import subprocess
import sys
repo = pathlib.Path(sys.argv[1]).resolve()
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
head = '4ff3642e8fe9a0bd48d28374350390cde553bc32'
prior = '1e914414557874648ac5041aff88b96908e0e053'
merge = git('rev-parse', 'd26fca65').decode().strip()
dev = git('rev-parse', '78ca9bdf').decode().strip()
base = git('merge-base', prior, dev).decode().strip()
assert git('rev-parse', 'HEAD').decode().strip() == head
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == '62626aefcfd7c4ff0b53f3a5413f700477bb9611'
assert git('rev-list', '--parents', '-n', '1', merge).decode().split() == [merge, prior, dev]
def edits(a, b, path):
    lines = git('diff', '--no-ext-diff', '--no-textconv', '-U0', a, b, '--', path).splitlines()
    return b'\n'.join(l for l in lines if l[:1] in (b'+', b'-') and not l.startswith((b'+++', b'---')))
rtl = 'hdl/milan/milan_datapath.sv'
for a,b,c,d,label in [(prior,merge,base,dev,'merge minus prior = dev change'),(dev,merge,base,prior,'merge minus dev = map change')]:
    x,y = edits(a,b,rtl),edits(c,d,rtl)
    assert x == y, label
    print('PASS', label, 'exact ordered added/removed lines SHA256', hashlib.sha256(x).hexdigest())
assert git('diff', '--name-only', merge, head).decode().splitlines() == ['tb/verilator/milan_dp/README.md']
print('PASS merge to head changes README only')
cpp = 'tb/verilator/milan_dp/sim_nxn.cpp'
def blob(rev, path): return git('show', rev + ':' + path).decode()
old,cur,other = (blob(r,cpp) for r in (prior,head,dev))
start='    #if defined(DYNMAP_DEFAULT_TB) || defined(MAPREC_MP_TB)'
end='    // ----'
# Entire map implementation, including all lone-record checks, precedes next feature block.
map_begin=old.index(start, old.index('void dynmap_power_on_and_adaptation_section'))
map_end=old.index('    #endif', old.index('void maprec_multiport_section',map_begin))+len('    #endif')
map_bytes=old[map_begin:map_end]
assert map_bytes in cur
print('PASS complete prior map helper block retained', len(map_bytes), 'characters')
for name in ['stopped_input_law_on_the_shipping_geometry','prove_a_stopped_stream_input_counts_no_interruption']:
    begin=other.index('    void '+name+'()')
    finish=other.index('\n    }',begin)+len('\n    }')
    assert other[begin:finish] in cur
    print('PASS imported function unchanged',name)
probes='tb/verilator/milan_dp/dynmap_probes.vlt'
opens=lambda rev:set(l for l in blob(rev,probes).splitlines() if l.startswith('public_flat'))
assert opens(head) == opens(prior)|opens(dev)
print('PASS probe declarations equal parent union',len(opens(head)))
tail=cur[cur.index('        dynmap_power_on_and_adaptation_section();'):]
assert tail.index('stopped_input_law_on_the_shipping_geometry();') < tail.index('dynmap_map_records_section();') < tail.index('return true;')
assert 'bring_the_datapath_out_of_reset();' in cur[cur.index('    void stopped_input_law_on_the_shipping_geometry()'):cur.index(start,cur.index('    void stopped_input_law_on_the_shipping_geometry()'))]
assert 'load_the_saved_state_window(AEMI_CFG_C, {}, &why)' in cur
print('PASS call ordering, reset and erased-window setup')
assert not git('diff', '--raw', prior, head, '--', 'protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack')
print('PASS required gitlinks unchanged')
live='59740e3c9d0420e2e7fef185978954710448dc4a'
candidate=git('merge-tree','--write-tree',live,head).decode().strip()
assert re.fullmatch('[0-9a-f]{40}',candidate)
print('PASS clean test merge',live,head,'tree',candidate)
print('No candidate execution or manager source bank is inferred.')
