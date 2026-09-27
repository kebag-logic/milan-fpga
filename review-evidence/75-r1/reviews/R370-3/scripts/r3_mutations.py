"""Show that r3_probe.py fails for each defect class it claims to detect.

Usage: python3 -B r3_mutations.py EVIDENCE_DIR PAGE INDEX SCRATCH
Copies the evidence, page and index into SCRATCH, applies one mutation at a
time, runs r3_probe.py on the copy and records the exit status. Inputs are
never modified. Exits 1 unless the unmutated copy passes and every mutant fails.
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sub(path, old, new):
    text = path.read_text()
    if old not in text:
        raise SystemExit(f'mutation anchor missing in {path.name}: {old!r}')
    path.write_text(text.replace(old, new, 1))


MUTANTS = [
    ('page census says 100/100', 'page', lambda e, p, i: sub(p, 'in 99/100 holds', 'in 100/100 holds')),
    ('cycle 1 hold event relabelled as declaration', 'ev',
     lambda e, p, i: sub(e / 'author-r3/hold-events.csv', '1,2835636498,0.120687323,Lv,False',
                         '1,2835636498,0.120687323,JoinMt,True')),
    ('summary census pinned to 100', 'ev',
     lambda e, p, i: sub(e / 'author-r3/declarations-summary.json', '"holds_with_dut_declaration": 99',
                         '"holds_with_dut_declaration": 100')),
    ('census counted with a literal', 'ev',
     lambda e, p, i: sub(e / 'author-r3/declarations.py',
                         "holds_with_dut_declaration=sum(r['declaration_count'] > 0 for r in holds)",
                         'holds_with_dut_declaration=99')),
    ('old universal claim restored on page', 'page',
     lambda e, p, i: sub(p, 'That shared absence alone cannot explain the initial-bind delay.',
                         'The initial bind therefore differs in DUT-side state too.')),
    ('cycle 1 Lv offset wrong on page', 'page', lambda e, p, i: sub(p, '+0.120687323 seconds', '+0.120687324 seconds')),
    ('non-stop Lv time wrong on page', 'page', lambda e, p, i: sub(p, '| 24 | 0.010356881 |', '| 24 | 0.010356882 |')),
    ('non-stop event row dropped from page', 'page', lambda e, p, i: sub(p, '| 75 | New | +2.122542224 | +0.113522106 |\n', '')),
    ('listener-events.csv loses a row', 'ev',
     lambda e, p, i: sub(e / 'author-r3/listener-events.csv',
                         '13,5167050381,New,2,2.182730731,0.173347014,5166069251,5168069280,0.002000029\n', '')),
    ('#608 link removed from index row', 'index',
     lambda e, p, i: sub(i, 'three non-restarts tracked by [#608](https://github.com/kebag-logic/milan-fpga/issues/608)',
                         'three non-restarts open')),
    ('#608 link removed from acceptance row', 'page',
     lambda e, p, i: sub(p, 'three talker non-restarts excluded, tracked by [#608]', 'three talker non-restarts excluded [#608]')),
    ('replay classifies by catching AssertionError', 'ev',
     lambda e, p, i: sub(e / 'author-r3/recompute.py',
                         "            verdict = classify_stop(settled_count, post_settle['ns'], ack)\n",
                         "            try:\n                assert settled_count == 0\n                verdict = 'RESTART'\n"
                         "            except AssertionError:\n                verdict = 'NOT_RESTART'\n")),
    ('optimisation guard removed', 'ev',
     lambda e, p, i: sub(e / 'author-r3/recompute.py',
                         'if sys.flags.optimize:\n    raise SystemExit("REFUSED: optimized execution disables evidence checks")\n', '')),
    ('outcome pinned to 197', 'ev',
     lambda e, p, i: sub(e / 'author-r3/recompute.py', 'f"Stop checks: {passed} PASS;', 'f"Stop checks: 197 PASS;')),
    ('classify_stop ignores the settled count', 'ev',
     lambda e, p, i: sub(e / 'author-r3/recompute.py', "    if count != 0:\n        return 'NOT_RESTART'\n", '')),
    ('published record byte changed', 'ev',
     lambda e, p, i: sub(e / 'author-r3/talker-024/action.log', 'a', 'b')),
]


def run(ev, page, index):
    p = subprocess.run([sys.executable, '-B', str(HERE / 'r3_probe.py'), str(ev), str(page), str(index)],
                       capture_output=True, text=True, timeout=900)
    firstfail = next((l for l in p.stdout.splitlines() if l.startswith('FAIL')), p.stderr.strip().splitlines()[-1:] or [''])
    return p.returncode, firstfail if isinstance(firstfail, str) else firstfail[0] if firstfail else ''


def main():
    ev, page, index, scratch = map(Path, sys.argv[1:])
    bad = 0
    for label, _, mutate in [('unmutated copy', None, lambda e, p, i: None)] + MUTANTS:
        work = scratch / 'mutant'
        if work.exists():
            shutil.rmtree(work)
        work.mkdir(parents=True)
        e = work / 'ev'
        shutil.copytree(ev, e)
        p, i = work / 'page.md', work / 'README.md'
        shutil.copyfile(page, p)
        shutil.copyfile(index, i)
        mutate(e, p, i)
        rc, why = run(e, p, i)
        ok = (rc == 0) if label == 'unmutated copy' else (rc != 0)
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {label}: probe rc {rc}; {why}")
        shutil.rmtree(work)
    print('RESULT ' + ('PASS' if not bad else f'FAIL ({bad})'))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
