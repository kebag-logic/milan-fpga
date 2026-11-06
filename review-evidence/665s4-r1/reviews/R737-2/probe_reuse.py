#!/usr/bin/env python3
"""Reviewer probes of the target harness's reused-output contract (run.py main/clear/accept/refuse).

Every probe patches functions in memory; no file of the checkout is written. Run with -I:
    python3 -I probe_reuse.py CHECKOUT OLD_MAIN_SOURCE
OLD_MAIN_SOURCE is the previously reviewed head's run.py (git show ac45db8f:tb/verilator/nvm_split_target/run.py).
"""
import contextlib
import inspect
import io
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

checkout, old_source = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).read_text()
sys.path.insert(0, str(checkout / 'tb/verilator/nvm_split_target'))
import target_selftest as ST  # noqa: E402

RUN = ST.RUN
REUSE = [n for n, _, _ in ST.reused_checks()]
CLOCK_MAIN = [n for n, _, _ in ST.clock_checks() if n.startswith('run.py ')]
failures = 0


def compile_main(src: str):
    """A main defined from src, its globals run.py's own, so the self-test's patches reach it."""
    ns: dict = {}
    exec(src, RUN.__dict__, ns)
    return ns['main']


def main_source_of(text: str) -> str:
    start = text.index('def main(')
    return text[start:text.index("\nif __name__ == '__main__':")]


def failing(**patches) -> list[str]:
    with contextlib.ExitStack() as stack:
        for name, value in patches.items():
            stack.enter_context(patch.object(RUN, name, value))
        return [n for n, ok, _ in ST.checks() if not ok]


def expect(label: str, got: list[str], must_fail: list[str]) -> None:
    global failures
    missing = [n for n in must_fail if n not in got]
    ok = not missing
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'}: {label}")
    for n in got:
        print(f'    fails: {n}')
    for n in missing:
        print(f'    NOT FAILED (expected): {n}')


head = failing()
print(f'head: {len(ST.checks())} ordinary checks, failing {head}')
failures += bool(head)

# P1: the previously reviewed main (results.json written before validation, nothing cleared, no refusal record).
old = compile_main(main_source_of(old_source))
expect('P1 round-3 main restored: every success-then-refusal check fails', failing(main=old),
       [n for n in REUSE if n.startswith('a success, then ')])

current = inspect.getsource(RUN.main)
# P2: only main's own clear before the run removed (refuse still clears on refusal).
assert current.count('        clear(out)\n') == 1
expect("P2 main's initial clear removed: refusal-then-success fails",
       failing(main=compile_main(current.replace('        clear(out)\n', '', 1))),
       ["a refusal, then a success in the same directory: the success's pair alone, no refusal left"])
# P3: main never calls refuse.
assert current.count('        refuse(out, str(error), rec)\n') == 1
expect('P3 refuse() not called by main: every success-then-refusal check fails',
       failing(main=compile_main(current.replace('        refuse(out, str(error), rec)\n', '', 1))),
       [n for n in REUSE if n.startswith('a success, then ')])
# P4: accept skips the comparison with the builds' clocks.
acc = inspect.getsource(RUN.accept)
assert acc.count('    wrong = against_build(rec, specs)\n') == 1
ns: dict = {}
exec(acc.replace('    wrong = against_build(rec, specs)\n', '    wrong = []\n'), RUN.__dict__, ns)
expect("P4 accept without against_build: the not-its-builds' checks fail", failing(accept=ns['accept']),
       ["a success, then clocks that are not its builds' in the same directory: the refusal alone, no table or "
        "results left", "run.py refuses a run whose clocks are not its builds', writing no table"])
# P5: accept writes the table text it has not validated (table() bypassed for rendering only after writing).
ns = {}
exec(acc.replace('    text = table(rec)\n    (out / \'results.json\')',
                 '    (out / \'table.md\').write_text(\'stale\')\n    text = table(rec)\n    (out / \'results.json\')'),
     RUN.__dict__, ns)
expect('P5 accept writes table.md before validating: the direct accept check fails', failing(accept=ns['accept']),
       ['accept writes nothing for a record it refuses'])


# P6: a success, then a crash outside the refused exception classes: nothing of the earlier pair is left.
def boom(*a, **k):
    raise KeyError('planted crash')


with tempfile.TemporaryDirectory() as tmp:
    first = ST.main_run(ST.OTHER_CPU_HZ, ST.OTHER_SYS_HZ, root=Path(tmp))
    with patch.object(RUN, 'record', boom):
        again = ST.main_run(ST.OTHER_CPU_HZ, ST.OTHER_SYS_HZ, root=Path(tmp))
    left = sorted(p.name for p in (Path(tmp) / 'results').iterdir() if p.name in ('results.json', 'table.md',
                                                                                    'refused.json'))
ok = first[0] == 0 and again[0] == -1 and left == []
failures += not ok
print(f"{'PASS' if ok else 'FAIL'}: P6 success then an uncaught crash: no pair or refusal left {first[0]} {again[0]} "
      f'{left}')

# P7 (informational): a success, then a usage error (unknown case) in the same directory.
with tempfile.TemporaryDirectory() as tmp:
    first = ST.main_run(ST.OTHER_CPU_HZ, ST.OTHER_SYS_HZ, root=Path(tmp))
    err = io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
        try:
            RUN.main(['--point', '1x1', '--build-dir', tmp, '--cases', 'no-such-case'])
            code = 0
        except SystemExit as exit_:
            code = exit_.code
    left = sorted(p.name for p in (Path(tmp) / 'results').iterdir() if p.name in ('results.json', 'table.md',
                                                                                    'refused.json'))
print(f'INFO: P7 success then a usage error: exit {code}, left {left} (the earlier accepted pair, untouched)')

# P8: the refusal record is not an accepted record and carries the refused record nested.
with tempfile.TemporaryDirectory() as tmp:
    ST.main_run(ST.OTHER_CPU_HZ, ST.OTHER_SYS_HZ, root=Path(tmp))
    run = ST.main_run(ST.OTHER_CPU_HZ, ST.OTHER_SYS_HZ, root=Path(tmp), graded_at=ST.CPU_HZ)
ref = run[3]
ok = sorted(ref) == ['record', 'refused'] and ref['record']['cpu_hz'] == ST.OTHER_CPU_HZ and \
    'is not 40,000 CPU cycles' in ref['refused'] and run[0] == 2
failures += not ok
print(f"{'PASS' if ok else 'FAIL'}: P8 refused.json top keys {sorted(ref)}, nested record CPU "
      f"{ref.get('record', {}).get('cpu_hz')}, words {ref.get('refused', '')[:90]!r}")

print(f'probes failing: {failures}')
sys.exit(1 if failures else 0)
