#!/usr/bin/env python3
"""Summarise a probe group's observation log: every work pass over the 200,000-cycle share, the longest passes
with their modules, and each store/flash-reading pass.

usage: probe_passes.py <checkout> <log>..."""
import sys, re
root, logs = sys.argv[1], sys.argv[2:]
sys.path.insert(0, root + '/tb/verilator/ctrl_service_budget')
sys.path.insert(0, root + '/sw/mailbox')
import grade
for path in logs:
    text = open(path, errors='replace').read()
    text = text[:text.rfind('\n') + 1]
    if text.count('\n') and not text.rstrip().rsplit('\n', 1)[-1].startswith('RESULT'):
        text = text.rstrip().rsplit('\n', 1)[0] + '\n'  # a run still writing: its last whole line may be cut
    log = grade.parse(text, 100_000_000, 100_000_000)
    marks = dict((n, c) for c, n in log.marks)
    over = [p for p in log.passes if p.cycles > 200000]
    top = sorted(log.passes, key=lambda p: -p.cycles)[:4]
    print(path.rsplit('/', 1)[-1], 'passes', len(log.passes), 'over-share', len(over))
    for p in top:
        m = sorted(p.modules.items(), key=lambda kv: -kv[1])[:7]
        print(f'   {p.cycles:7d} cyc start {p.start_sys} (+{(p.start_sys - marks.get("composed", 0)) / 1e5:.2f} ms from composed) {m}')
    flash = [p for p in log.passes if p.modules.get('nvm_flash_litespi', 0) > 1000]
    print('   passes with store flash work', len(flash), 'largest', max([p.cycles for p in flash], default=0))
