#!/usr/bin/env python3
"""Independent reuse probes of tb/verilator/nvm_split_target/run.py's main and extra mutants of accept/main
against the repository self-test. Usage: probe_reuse.py <checkout root>. Writes nothing in the checkout."""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / 'tb/verilator/nvm_split_target'))
import target_selftest as T  # noqa: E402

RUN = T.RUN
CPU, SYS = 62_500_000, 125_000_000
verdicts = []


def note(label, ok, detail=''):
    verdicts.append(ok)
    print(f"{'OK ' if ok else 'BAD'} {label}{': ' + detail if detail else ''}")


def run_main(build_root: Path, builds=None, graded_at=0, crash=None, argv_extra=()):
    """main on synthetic producers (own substitutions): status, sorted names left in results/, table text."""
    def built(r, key, point, reuse):
        return dict((builds or {}).get(key, dict(cpu_hz=CPU, sys_hz=SYS)), build_dir=str(r / key))

    def run_cases(selected, specs, point, out, jobs, clk):
        if crash:
            raise crash
        return T.graded_commit(graded_at or clk['cpu_hz'], clk['sys_hz'])
    status = None
    with contextlib.ExitStack() as st:
        st.enter_context(T.replaced(RUN, 'built', built))
        st.enter_context(T.replaced(RUN, 'run_cases', run_cases))
        st.enter_context(contextlib.redirect_stdout(io.StringIO()))
        st.enter_context(contextlib.redirect_stderr(io.StringIO()))
        try:
            status = RUN.main(['--point', '1x1', '--build-dir', str(build_root), '--cases', 'valid', *argv_extra])
        except SystemExit as e:
            status = f'SystemExit({e.code})'
        except Exception as e:  # noqa: BLE001
            status = f'raised {type(e).__name__}'
    out = build_root / 'results'
    left = sorted(p.name for p in out.iterdir()) if out.is_dir() else []
    text = (out / 'table.md').read_text() if (out / 'table.md').is_file() else ''
    return status, left, text


# 1. success then each refusal class, independent producers; then refusal then success.
classes = {
    'one arm without CPU clock': dict(builds={'fixture': dict(sys_hz=SYS)}),
    'all arms without CPU clock': dict(builds={'capture-all': dict(sys_hz=SYS), 'fixture': dict(sys_hz=SYS)}),
    'bus clock disagrees': dict(builds={'fixture': dict(cpu_hz=CPU, sys_hz=100_000_000)}),
    'misconverted': dict(graded_at=50_000_000),
}
for label, kw in classes.items():
    with tempfile.TemporaryDirectory() as tmp:
        a = run_main(Path(tmp))
        b = run_main(Path(tmp), **kw)
        ref = json.loads((Path(tmp) / 'results/refused.json').read_text()) if 'refused.json' in b[1] else {}
    note(f'success then {label}', a[0] == 0 and a[1] == ['results.json', 'table.md'] and b[0] == 2
         and b[1] == ['refused.json'] and set(ref) == {'refused', 'record'}, f'{a[:2]} -> {b[:2]} keys {sorted(ref)}')
with tempfile.TemporaryDirectory() as tmp:
    a = run_main(Path(tmp), graded_at=50_000_000)
    b = run_main(Path(tmp))
    rec = json.loads((Path(tmp) / 'results/results.json').read_text())
note('refusal then success', a[1] == ['refused.json'] and b[0] == 0 and b[1] == ['results.json', 'table.md']
     and (rec['cpu_hz'], rec['sys_hz']) == (CPU, SYS), f'{a[:2]} -> {b[:2]}')

# 2. Paths outside the documented refusal set (observations, not README claims).
with tempfile.TemporaryDirectory() as tmp:
    run_main(Path(tmp))
    c = run_main(Path(tmp), crash=KeyError('planted'))
note('success then an uncaught crash (KeyError): no earlier pair survives', 'table.md' not in c[1]
     and 'results.json' not in c[1], f'{c[:2]}')
with tempfile.TemporaryDirectory() as tmp:
    a = run_main(Path(tmp))
    before = (Path(tmp) / 'results/table.md').read_bytes()
    u = run_main(Path(tmp), argv_extra=('--cases', 'no-such-case'))
    after = (Path(tmp) / 'results/table.md').read_bytes()
print(f'OBS usage error after a success: status {u[0]}, left {u[1]}, earlier table unchanged {before == after}')
with tempfile.TemporaryDirectory() as tmp:
    run_main(Path(tmp))
    (Path(tmp) / 'results/table.md').unlink()
    (Path(tmp) / 'results/table.md').mkdir()
    d = run_main(Path(tmp), graded_at=50_000_000)
print(f'OBS table.md an undeletable directory, then a refusal: status {d[0]}, left {d[1]}')


# 3. Extra mutants: each run against the full repository check list; report which checks fail.
def accept_after_table_before_build_check(out, rec, specs):
    """write the pair once table() passes, then check the builds."""
    text = RUN.table(rec)
    (out / 'results.json').write_text(json.dumps(rec))
    (out / 'table.md').write_text(text)
    wrong = RUN.against_build(rec, specs)
    if wrong:
        raise RuntimeError('; '.join(wrong))
    return text


def accept_no_build_check(out, rec, specs):
    """the against_build check dropped."""
    text = RUN.table(rec)
    (out / 'results.json').write_text(json.dumps(rec))
    (out / 'table.md').write_text(text)
    return text


def refuse_silent(out, words, rec):
    """refuse that clears but leaves no refusal record."""
    RUN.clear(out)


def refuse_with_clocks(out, words, rec):
    """refused.json carrying the record's clocks at its top."""
    RUN.clear(out)
    (out / RUN.REFUSAL).write_text(json.dumps(dict(refused=words, record=rec, **({} if rec is None else
                                                   dict(cpu_hz=rec['cpu_hz'], sys_hz=rec['sys_hz'])))))


def clear_keeps_table(out):
    """clear that leaves table.md."""
    for name in ('results.json', RUN.REFUSAL):
        (out / name).unlink(missing_ok=True)


mutants = [('accept: pair written before against_build', 'accept', accept_after_table_before_build_check),
           ('accept: against_build dropped', 'accept', accept_no_build_check),
           ('refuse: no refusal record', 'refuse', refuse_silent),
           ('refuse: clocks at refused.json top', 'refuse', refuse_with_clocks),
           ('clear: table.md kept', 'clear', clear_keeps_table)]
for label, name, value in mutants:
    with T.replaced(RUN, name, value):
        failed = [n for n, ok, _ in T.checks() if not ok]
    print(f'MUTANT {label}: {len(failed)} repository checks fail' + ''.join(f'\n    - {n}' for n in failed))
print('PROBES', 'PASS' if all(verdicts) else 'FAIL')
sys.exit(0 if all(verdicts) else 1)
