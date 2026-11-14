"""Phase B's restatement of 8x8/1if's provisional figures from its measurement (#894's round 2 ruling, items (b)(ii) and
(b)(iii)): over every given leg's grades, each poll kind's heaviest (passes.polls.heaviest) and the heaviest SRP record
handler (srp_mbx:receive spans in the logs, the record CTRL_LOOP_SRP_UNIT_US states, as 8x8/2if's 365 us was), each
plus 5 % and rounded up to 5 us at the CPU's 100 MHz, against the figure the tree states (poll_grade.EIGHT_ONE and
ctrl_loop.h's (1, 9, 9) block). Read only.
usage: python3 -I restate.py TREE LEG_DIR..."""
import json
import math
import re
import sys
from pathlib import Path

tree, legs = Path(sys.argv[1]), [Path(a) for a in sys.argv[2:]]
CPU_MHZ = 100
#: poll_grade's kinds and the grade JSON's names for them (the same names, but the SRP record's apply, 'record',
#: which poll_grade holds to the retained item's cost).
KINDS = ('base', 'withdraw', 'rebuild', 'walk', 'reclaim', 'acmp', 'acmp_declined', 'aecp', 'aecp_long', 'record',
         'acmp_kept')
heaviest: dict[str, tuple[int, str]] = {}
receive = (0, '')
for leg in legs:
    for js in sorted((leg / 'results').glob('*.json')):
        if js.name == 'results.json':
            continue
        d = json.loads(js.read_text())
        for k, v in d.get('passes', {}).get('polls', {}).get('heaviest', {}).items():
            if v > heaviest.get(k, (0, ''))[0]:
                heaviest[k] = (v, f'{leg.name}/{js.stem}')
        log = js.with_suffix('.log')
        if log.exists():
            with log.open() as fh:
                for line in fh:
                    if line.startswith('SPAN ') and line.rstrip().endswith('srp_mbx:receive'):
                        f = line.split()
                        if f[5] == 'srp_mbx:receive' and int(f[3]) > receive[0]:
                            receive = (int(f[3]), f'{leg.name}/{js.stem}')


def stated(cycles: int) -> int:
    """Cycles plus 5 %, in us at the CPU clock, rounded up to 5 us."""
    return 5 * math.ceil(cycles * 1.05 / CPU_MHZ / 5 - 1e-9)


text = (tree / 'tb/verilator/ctrl_service_budget/poll_grade.py').read_text()
body = re.search(r'EIGHT_ONE = dict\((.*?)\)\n', text, re.S)[1]
now = {k: int(v) for k, v in re.findall(r'(\w+)=(\d+)', body)}
loop = (tree / 'sw/firmware/ctrl/loop/ctrl_loop.h').read_text()
unit = int(re.search(r'CTRL_LOOP_SHAPE\(1u, 9u, 9u\).*?#define CTRL_LOOP_SRP_UNIT_US (\d+)u', loop, re.S)[1])
print(f'# legs: {" ".join(l.name for l in legs)}; at 100 MHz, the most measured plus 5 %, rounded up to 5 us')
print('| Figure | Heaviest, CPU cycles | Where | Plus 5 %, us | Stated now, us | Restated, us |')
print('|---|---:|---|---:|---:|---:|')
c, where = receive
print(f'| CTRL_LOOP_SRP_UNIT_US (srp_mbx:receive), and EIGHT_ONE retained | {c:,} | {where} | {c * 1.05 / CPU_MHZ:.1f} | '
      f'{unit} (retained {now.get("retained")}) | {stated(c)} |')
for k in KINDS:
    if k not in heaviest:
        print(f'| {k} | not measured | | | {now.get(k, "")} | |')
        continue
    c, where = heaviest[k]
    target = {'record': 'held to retained', 'acmp_kept': "held to record.acmp (load_grade)"}.get(k)
    print(f'| {k} | {c:,} | {where} | {c * 1.05 / CPU_MHZ:.1f} | {now.get(k, target or "")} | '
          f'{stated(c) if target is None else "(" + str(stated(c)) + ")"} |')
others = sorted(set(heaviest) - set(KINDS))
if others:
    print('\nOther measured kinds: ' + ', '.join(f'{k} {heaviest[k][0]:,} ({heaviest[k][1]})' for k in others))
