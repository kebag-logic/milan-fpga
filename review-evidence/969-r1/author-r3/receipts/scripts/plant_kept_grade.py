#!/usr/bin/env python3
"""plant_kept_grade.py CHECKOUT: each held condition of tb/verilator/ctrl_service_budget/kept_grade.py removed in
memory, one at a time, and kept_grade's own --selftest run on the planted module: a plant is CAUGHT when a self-test
check fails or the self-test cannot complete, ESCAPED when every check still passes. No file is modified.
Exit 0 = every plant caught and the unplanted self-test green."""
import contextlib, io, sys
from pathlib import Path
target = Path(sys.argv[1]).resolve() / 'tb/verilator/ctrl_service_budget/kept_grade.py'
text = target.read_text()
PLANTS = [
    ('log-refusal-removed', 'grade.refuse_run(log, scenario.Group(name))', 'pass'),
    ('never-marked-unfound', 'for probe in want[name] if probe not in marked]', 'for probe in want[name] if False]'),
    ('foreign-probe-unfound', 'if probe.startswith(prefix) and probe not in want[name]]', 'if False]'),
    ('no-record-unfound', "findings.append(f'{probe}: no SRP record follows its mark')", 'pass'),
    ('unit-never-owed', 'if us > unit:', 'if False:'),
    ('mate-missing-skipped', "findings.append(f'{probe}: no {mate or \"srp-bound\"} record", "pass; (f'{probe}: no {mate or \"srp-bound\"} record"),
    ('kept-over-bound-unfound', 'if cycles > recs[kept_window.BOUND][mate]:', 'if False:'),
    ('share-not-read-from-log', "over = grade.pass_share(log)['over_passes']", 'over = []'),
    ('kept-share-unfound', 'for at, cycles in k_work]', 'for at, cycles in []]'),
    ('bound-share-not-owed', 'for at, cycles in b_work]', 'for at, cycles in []]'),
    ('idle-run-unfound', 'for run, cycles in idle]', 'for run, cycles in []]'),
    ('idle-read-as-work', "for o in over if 'start_sys' in o]", 'for o in over]'),
    ('build-over-cost-unfound', "for o in builds['over'] if o['kind'] != 'step']", "for o in builds['over'] if False]"),
    ('pair-not-required', 'if len(self.ran) < len(OWED_KINDS):', 'if False:'),
    ('disposition-ignores-findings', '_, self.owed, self.findings = held(', '_, self.owed, _ = held('),
    ('owed-despite-findings', 'return not self.findings and any(', 'return any('),
    ('absent-log-unfound', "if not (results / f'{name}.log').is_file()]", 'if False]'),
    ('share-owed-despite-findings', 'return [line for line in lines if self.findings or not', 'return [line for line in lines if not'),
    ('record-taken-by-the-next-mark', 'k = bisect_left(starts, sys_start + 1) - 1', 'k = min(bisect_left(starts, sys_start + 1), len(starts) - 1)'),
    ('unparsed-log-unfound', "return [], [], [f'{name}: its log does not parse: {error}']", 'continue'),
]
def run(source):
    ns = dict(__file__=str(target), __name__='planted_kept_grade')
    exec(compile(source, str(target), 'exec'), ns)
    with contextlib.redirect_stdout(io.StringIO()):
        checks = ns['selftest']()
    return checks
base = run(text)
print(f'unplanted: {sum(ok for _, ok, _ in base)}/{len(base)} self-test checks pass')
escaped = 0
for name, old, new in PLANTS:
    assert text.count(old) == 1, f'{name}: anchor found {text.count(old)} times'
    try:
        checks = run(text.replace(old, new))
        failed = [what for what, ok, _ in checks if not ok]
        verdict = f'CAUGHT by {len(failed)} check(s): {failed[0]}' if failed else 'ESCAPED'
        escaped += not failed
    except Exception as error:  # the planted self-test cannot complete: caught, by the exception
        verdict = f'CAUGHT: the self-test raises {type(error).__name__}: {str(error)[:90]}'
    print(f'{name}: {verdict}')
print(f'plants: {len(PLANTS)}, caught {len(PLANTS) - escaped}, escaped {escaped}')
sys.exit(1 if escaped or not all(ok for _, ok, _ in base) else 0)
