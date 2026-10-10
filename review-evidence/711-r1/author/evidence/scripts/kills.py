"""Count each planted-defect campaign's verdicts in a test_ctrl_firmware.py --self-test log (scratch).

Usage: python3 kills.py CHECKOUT LOG
Campaigns are told apart by their own tables, imported from the checkout that produced the log.
"""
import re
import sys
from pathlib import Path

checkout, log = Path(sys.argv[1]), Path(sys.argv[2])
sys.path[:0] = [str(checkout / 'sw/firmware/ctrl/test'), str(checkout / 'sw/firmware/gtest')]
import aecp_mutants  # noqa: E402
import ctrl_mutants  # noqa: E402
import srp_mutants  # noqa: E402

text = log.read_text(errors='replace').splitlines()
verdicts = [(m.group(1), m.group(2)) for line in text
            if (m := re.match(r'\[(ok|ESCAPED)\] (.+?)(?::| \(|$)', line))]
ctrl_names = {f'mutant {m.name}' for m in ctrl_mutants.MUTANTS}
srp_names = {d.name for d in srp_mutants.DEFECTS}
aecp_names = {d.name for d in aecp_mutants.DEFECTS}
pin = {name for _, name in verdicts if name.startswith('lwSRP pin')}
rows = {'ctrl': ctrl_names, 'aecp': aecp_names, 'srp': srp_names, 'pin': pin}
# A name in more than one table belongs to the campaign of the verdict before it (campaigns run in sequence).
counts = {key: [0, 0] for key in rows}
previous = None
for verdict, name in verdicts:
    owners = [key for key, names in rows.items() if name in names]
    if not owners:
        continue
    owner = owners[0] if len(owners) == 1 else (previous if previous in owners else owners[0])
    counts[owner][0 if verdict == 'ok' else 1] += 1
    previous = owner
counts = {key: (ok, esc, len(rows[key]), ok + esc) for key, (ok, esc) in counts.items()}
summary = [line for line in text if re.match(r'mutants: \d+ of \d+ caught', line)]
srp_first = [n for v, n in verdicts if n in srp_names]
print('table sizes: ctrl', len(ctrl_names), 'aecp', len(aecp_names), 'srp', len(srp_names))
for key, (ok, esc, size, lines) in counts.items():
    print(f'{key}: {ok} caught, {esc} escaped, {lines} verdict lines, table {size}')
print('ctrl summary lines:', summary)
print('srp verdict lines (two-interface table, then the one-interface subset):', len(srp_first))
print('final:', [line for line in text if line.startswith('test_ctrl_firmware:')])
