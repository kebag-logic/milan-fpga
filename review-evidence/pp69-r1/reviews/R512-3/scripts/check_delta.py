#!/usr/bin/env python3
"""Check exact-head merge preservation and the counter-stamp storage contract."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import types

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--output', type=Path, required=True)
args = ap.parse_args()
HEAD = '669ded57b1fabc2bbf274b8ad05493c7593e0a0a'
ROUND2 = '75c4eee4589e9317aca3d07b91f94a38b4cc86af'
MAIN = '2ad2f845dd583f8310075fa2380cb60a04fd091a'


def git(*argv):
    return subprocess.check_output(['git', *argv], cwd=args.repo, text=True)


def content(ref, path):
    return git('show', ref + ':' + path)


def catalog(ref):
    path = 'tb/pp_top/notify_mutants.py'
    name = 'catalog_' + ref[:8]
    module = types.ModuleType(name)
    module.__file__ = str(args.repo / path)
    sys.modules[name] = module
    exec(compile(content(ref, path), module.__file__, 'exec'), module.__dict__)
    return {m.name: dict(m._asdict(), suite=m.suite._asdict()) for m in module.MUTANTS}


rows = []


def check(name, passed, evidence):
    rows.append({'check': name, 'pass': bool(passed), 'evidence': evidence})


check('exact head', git('rev-parse', 'HEAD').strip() == HEAD, git('rev-parse', 'HEAD').strip())
check('exact tree', git('rev-parse', 'HEAD^{tree}').strip() == '4bce83358cf24f551909ab46aeb19c5f93787106', git('rev-parse', 'HEAD^{tree}').strip())
for path in ['hdl', 'syn']:
    hashes = {ref: git('rev-parse', ref + ':' + path).strip() for ref in [ROUND2, HEAD]}
    check(path + ' unchanged since round 2', len(set(hashes.values())) == 1, hashes)
    baseline_hashes = {ref: git('rev-parse', ref + ':' + path).strip()
                       for ref in ['86a7b0c57831c15e9cd8b42d64cc4a9843f4e726', MAIN]}
    check(path + ' baseline main unchanged by issue 42', len(set(baseline_hashes.values())) == 1,
          baseline_hashes)
parents = git('show', '-s', '--format=%P', '600ef131c54f9f389b955eb90009f777b06d0ced').strip().split()
check('non-fast-forward merge parents', parents == [ROUND2, MAIN], parents)
old, main, now = catalog(ROUND2), catalog(MAIN), catalog(HEAD)
check('campaign union', set(now) == set(old) | set(main) and len(now) == 86,
      {'round2': len(old), 'main': len(main), 'head': len(now)})
for label, source in [('round2', old), ('main', main)]:
    moved = [name for name, m in source.items() if now.get(name) != m]
    if label == 'main':
        name = 'dereg_lost_at_round_end'
        normalized = json.loads(json.dumps(source[name]).replace('N_CTRL_P - 1', 'N_ROW_C - 1'))
        expected = json.loads(json.dumps(now[name]))
        check('main mutation definitions preserved with existing row-depth anchor refresh',
              moved == [name] and normalized == expected,
              {'unchanged': len(source) - len(moved), 'refreshed': moved,
               'only_difference': 'N_CTRL_P - 1 becomes N_ROW_C - 1; identical at count 1'})
    else:
        check(label + ' exact mutation definitions preserved', not moved, moved)
for path in ['tb/pp_top/interface_phases.hpp', 'tb/aecp_notify/port_tuple.hpp',
             'tb/pp_top/if_guards.py', 'tb/adp_engine/sim_if2.cpp', 'tb/pp_top/pp_top_wrap.sv',
             'tb/aecp_notify/sim_main.cpp', 'tb/pp_top/Makefile', 'tb/aecp_notify/Makefile']:
    check(path + ' preserved from round2', content(ROUND2, path) == content(HEAD, path),
          git('rev-parse', HEAD + ':' + path).strip())
path = 'tb/pp_top/notify_phases.hpp'
check('DN implementation identical to main', content(MAIN, path) == content(HEAD, path), git('rev-parse', HEAD + ':' + path).strip())
text = content(HEAD, 'tb/pp_top/sim_main.cpp')
main_function = text[text.index('int main(int argc, char** argv) {'):]
check('main length at most 100 lines', len(main_function.splitlines()) <= 100, len(main_function.splitlines()))
check('both test dispatches retained', 'run_domain_notify(h);' in text and 'run_interfaces(h);' in text,
      ['run_domain_notify(h);', 'run_interfaces(h);'])
rtl = content(HEAD, 'hdl/aecp/KL_aecp_notify.sv')
doc = content(HEAD, 'docs/architecture/06_aecp_engine.md')
check('storage formula matches RTL',
      'N_CTR_DESC_C = N_STREAM_IN_P + N_STREAM_OUT_P + 1 + N_IF_P;' in rtl and
      '(streams in + out + 1 + P-N-AVB-INTERFACES) × 32 bits' in doc and
      re.search(r'logic\s+\[31:0\]\s+ctr_last_r\s*\[0:N_CTR_DESC_C-1\]', rtl),
      {'small_shape': {'1 interface': {'stamps': 4, 'bits': 128}, '2 interfaces': {'stamps': 5, 'bits': 160}},
       'default_8x8': {'1 interface': {'stamps': 18, 'bits': 576}, '2 interfaces': {'stamps': 19, 'bits': 608}}})
check('all 86 exact-text mutation anchors match once',
      all(content(HEAD, path).count(old_text) == 1 for m in now.values() for path, old_text, _ in m['edits']),
      {'mutants': len(now), 'edits': sum(len(m['edits']) for m in now.values())})
gitlinks = [line for line in git('ls-tree', '-r', HEAD).splitlines() if line.startswith('160000 ')]
check('processor repository gitlinks', not gitlinks, {'gitlinks': gitlinks, 'note': 'No nested submodule gitlinks in this repository.'})
args.output.write_text(json.dumps({'head': HEAD, 'checks': rows}, indent=2) + '\n')
for row in rows:
    print(('PASS' if row['pass'] else 'FAIL') + ': ' + row['check'] + ': ' + json.dumps(row['evidence']))
raise SystemExit(any(not row['pass'] for row in rows))
