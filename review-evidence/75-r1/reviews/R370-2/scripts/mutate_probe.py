"""Fault injection for stop_check_probe.py: every mutant must be rejected.

Usage: python3 mutate_probe.py EVIDENCE_DIR PAGE WORK_DIR
Copies the evidence and page under WORK_DIR, applies one defect per mutant,
reruns the probe, and prints KILLED (non-zero exit) or SURVIVED per mutant.
Inputs are never modified.
"""
import csv
import io
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def csv_mutant(rows, direction, cycle, **changes):
    out = [dict(r) for r in rows]
    for r in out:
        if r['direction'] == direction and r['cycle'] == str(cycle):
            r.update({k: str(v) for k, v in changes.items()})
    return out


def main():
    ev, page, work = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    rows = list(csv.DictReader((ev / 'author-r2' / 'stop-checks.csv').open()))
    t13 = next(r for r in rows if r['direction'] == 'talker' and r['cycle'] == '13')
    text = page.read_text()
    mutants = {
        'talker 13 hold made silent, label kept': ('csv', csv_mutant(rows, 'talker', 13, settled_to_response_pdus=0, settled_to_command_pdus=0,
                                                                        command_to_response_pdus=0, last_half_second_pdus=0,
                                                                        first_after_settle_ns=t13['first_post_response_ns'])),
        'talker 14 one PDU in settled hold': ('csv', csv_mutant(rows, 'talker', 14, settled_to_response_pdus=1, settled_to_command_pdus=1)),
        'listener 7 one PDU between command and response': ('csv', csv_mutant(rows, 'listener', 7, settled_to_response_pdus=1, command_to_response_pdus=1)),
        'talker 50 counter delta 0/0': ('csv', csv_mutant(rows, 'talker', 50, active_start_delta=0, active_stop_delta=0)),
        'talker 24 relabelled RESTART': ('csv', csv_mutant(rows, 'talker', 24, classification='RESTART', stop_check='PASS')),
        'hold shortened to 1.9 s': ('csv', csv_mutant(rows, 'listener', 3, connect_command_ns=int(rows[2]['disconnect_response_ns']) + 1_900_000_000)),
        'page talker median reverts to round-1 value': ('page', text.replace('| 97 | 97 | 0.017427 | 0.019175 |', '| 97 | 97 | 0.017427 | 0.019165 |')),
        'page talker 24 stop check PASS': ('page', text.replace('| DUT talker | 24 | 754 | 4 | 0 / 0 | 0 / 0 | FAIL |', '| DUT talker | 24 | 754 | 4 | 0 / 0 | 0 / 0 | PASS |')),
        'page talker interval upper bound +1e-9': ('page', text.replace('+0.000093851]', '+0.000093852]')),
        'page talker 75 row result PASS': ('page', text.replace('| DUT talker | 75 | 0.001864 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | NOT RESTART |',
                                                                 '| DUT talker | 75 | 0.001864 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |')),
    }
    survived = 0
    for i, (name, (kind, data)) in enumerate(mutants.items()):
        d = work / f'm{i:02d}'
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(ev, d / 'ev')
        mpage = d / 'page.md'
        mpage.write_text(text)
        if kind == 'csv':
            buf = io.StringIO()
            w = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator='\n')
            w.writeheader(); w.writerows(data)
            (d / 'ev' / 'author-r2' / 'stop-checks.csv').write_text(buf.getvalue())
        else:
            assert data != text, f'mutation did not apply: {name}'
            mpage.write_text(data)
        rc = subprocess.run([sys.executable, '-B', str(HERE / 'stop_check_probe.py'), str(d / 'ev'), str(mpage)],
                            capture_output=True, text=True, timeout=600).returncode
        verdict = 'KILLED' if rc != 0 else 'SURVIVED'
        survived += rc == 0
        print(f'{verdict} rc={rc} {name}')
    print('RESULT', 'PASS all mutants killed' if not survived else f'FAIL {survived} survived')
    return 1 if survived else 0


if __name__ == '__main__':
    sys.exit(main())
