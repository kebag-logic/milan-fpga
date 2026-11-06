#!/usr/bin/env python3
"""Own source-level probes of the round 3 rules, in memory, one forked child per mutant.

usage: source_probe.py TREE   (TREE is a full export of the head under review; nothing in it is written)
Each mutant replaces one exact text of run.py or hooks.py; a text that does not match exactly once is an error.
A child reports what makes the self-test exit nonzero: each failing check, and each of its mutants that escapes.
"""
import json, os, sys, types
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
H = tree / 'tb/verilator/ctrl_service_hooks'
HP = "family='notify', ms=held['ms'], cpu_cycles=cycles, wait_ms=held['wait_ms'],"
HPB = "bound_ms=bound, within=held['ms'] <= bound, unbounded=False, loaded=False,"
HPL = "row='GET_COUNTERS push, held until 1 s after the last departure, from its eligibility (H-COUNTERS)',"
HPI = "interface=0, family='notify', ms=held['ms']"
HM = "'(H-COUNTERS)', interface=0, family='notify', ms=0.0, cpu_cycles=0, wait_ms=0.0,"
HMB = "bound_ms=hooks.bound_ms('notify'), within=False, unbounded=True, loaded=False,"
HMN = "normative_ms=hooks.COUNTERS_NORMATIVE_MS, margin_ms=0.0, ahead=0, missing=True)"
HMH = "return dict(hook='H-COUNTERS', group='hooks-counters', probe=held['probe'], path='counters.held',\n                    row='GET_COUNTERS push, held '"
NAR = "narrow = sum(r['within'] and r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES for r in mine)"
SUP = "(x['group'], x['path'], x['interface']) == (by, *r['path'])"
ROW = "bound_ms=bound, within=not unbounded and row['ms'] <= bound, unbounded=unbounded,"
M = [
 # the six named by the ruling, in this reviewer's own spelling
 ('hp-row-ms-zero', 'run', HP, HP.replace("ms=held['ms']", 'ms=0.0')),
 ('hp-ms', 'run', HP, HP.replace("ms=held['ms']", "ms=held['ms'] + 1")),
 ('s-narrow-le', 'run', NAR, NAR.replace(' < ', ' <= ')),
 ('hm-cycles', 'run', HM, HM.replace('cpu_cycles=0', 'cpu_cycles=1')),
 ('hm-wait', 'run', HM, HM.replace('wait_ms=0.0', 'wait_ms=1.0')),
 ('hm-margin', 'run', HMN, HMN.replace('margin_ms=0.0', 'margin_ms=1.0')),
 # the narrow boundary on the other side
 ('s-narrow-minus1', 'run', NAR, NAR.replace('hooks.LAYOUT_SWING_CYCLES', 'hooks.LAYOUT_SWING_CYCLES - 1')),
 ('s-narrow-plus2', 'run', NAR, NAR.replace('hooks.LAYOUT_SWING_CYCLES', 'hooks.LAYOUT_SWING_CYCLES + 2')),
 ('s-narrow-no-within', 'run', NAR, NAR.replace("r['within'] and ", '')),
 ('g-narrow-le', 'run', "elif r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES:", "elif r['slack_cycles'] <= hooks.LAYOUT_SWING_CYCLES:"),
 # the measured held row, field by field
 ('hp-within-lt', 'run', HPB, HPB.replace("held['ms'] <= bound", "held['ms'] < bound")),
 ('hp-within-true', 'run', HPB, HPB.replace("within=held['ms'] <= bound", 'within=True')),
 ('hp-unbounded', 'run', HPB, HPB.replace('unbounded=False', 'unbounded=True')),
 ('hp-loaded', 'run', HPB, HPB.replace('loaded=False', 'loaded=True')),
 ('hp-bound', 'run', HPB, HPB.replace('bound_ms=bound', "bound_ms=bound + held['wait_ms']")),
 ('hp-interface', 'run', "interface=0, family='notify', ms=held['ms']", "interface=1, family='notify', ms=held['ms']"),
 ('hp-family', 'run', HP, HP.replace("family='notify'", "family='aecp'")),
 ('hp-wait', 'run', HP, HP.replace("wait_ms=held['wait_ms']", 'wait_ms=0.0')),
 ('hp-rowlabel', 'run', HPL, "row='x',"),
 ('hp-ahead', 'run', "margin_ms=round(hooks.COUNTERS_NORMATIVE_MS - held['wait_ms'] - held['ms'], 5), ahead=0)", "margin_ms=round(hooks.COUNTERS_NORMATIVE_MS - held['wait_ms'] - held['ms'], 5), ahead=1)"),
 ('hp-margin-round0', 'run', "held['ms'], 5), ahead=0)", "held['ms'], 0), ahead=0)"),
 ('hp-margin-round4', 'run', "held['ms'], 5), ahead=0)", "held['ms'], 4), ahead=0)"),
 ('hp-margin-noround', 'run', "margin_ms=round(hooks.COUNTERS_NORMATIVE_MS - held['wait_ms'] - held['ms'], 5), ahead=0)", "margin_ms=hooks.COUNTERS_NORMATIVE_MS - held['wait_ms'] - held['ms'], ahead=0)"),
 # the missing held row, field by field
 ('hm-ms', 'run', HM, HM.replace('ms=0.0, cpu', 'ms=1.0, cpu')),
 ('hm-interface', 'run', HM, HM.replace('interface=0', 'interface=1')),
 ('hm-family', 'run', HM, HM.replace("family='notify'", "family='aecp'")),
 ('hm-within', 'run', HMB, HMB.replace('within=False', 'within=True')),
 ('hm-unbounded', 'run', HMB, HMB.replace('unbounded=True', 'unbounded=False')),
 ('hm-loaded', 'run', HMB, HMB.replace('loaded=False', 'loaded=True')),
 ('hm-bound', 'run', HMB, HMB.replace("hooks.bound_ms('notify')", '1000.0')),
 ('hm-normative', 'run', HMN, HMN.replace('hooks.COUNTERS_NORMATIVE_MS', "hooks.NORMATIVE_MS['notify']")),
 ('hm-ahead', 'run', HMN, HMN.replace('ahead=0', 'ahead=1')),
 ('hm-not-missing', 'run', HMN, HMN.replace(', missing=True', '')),
 ('hm-hook', 'run', HMH, HMH.replace("hook='H-COUNTERS'", "hook='H-NOTIFY'")),
 ('hm-group', 'run', HMH, HMH.replace("group='hooks-counters'", "group='x'")),
 ('hm-probe', 'run', HMH, HMH.replace("probe=held['probe']", "probe='x'")),
 ('hm-path', 'run', HMH, HMH.replace("path='counters.held'", "path='x'")),
 ('hm-rowlabel', 'run', "row='GET_COUNTERS push, held '\n                    '(H-COUNTERS)',", "row='x',"),
 # the supersede rule at its source
 ('sup-no-interface', 'run', SUP, "(x['group'], x['path']) == (by, r['path'][0])"),
 ('sup-no-path', 'run', SUP, "(x['group'], x['interface']) == (by, r['path'][1])"),
 ('sup-no-group', 'run', SUP, "(x['path'], x['interface']) == tuple(r['path'])"),
 ('sup-any-row', 'run', SUP, 'True'),
 ('sup-table-empty', 'hooks', "SUPERSEDED = {'acmp.tmr_no_adp': 'hooks-disc-aging'}", 'SUPERSEDED = {}'),
 ('sup-second-entry', 'hooks', "SUPERSEDED = {'acmp.tmr_no_adp': 'hooks-disc-aging'}", "SUPERSEDED = {'acmp.tmr_no_adp': 'hooks-disc-aging', 'acmp.bind_rx': 'hooks-disc-aging'}"),
 # the amended column reaching what it must not
 ('am-verdict-1if', 'run', ROW, "bound_ms=bound, within=not unbounded and row['ms'] <= bound + (hooks.AMENDED_SRP_MS - bound + row['wait_ms'] if hook == 'H-SRP' else 0), unbounded=unbounded,"),
 ('am-verdict-queued-60', 'run', ROW, "bound_ms=bound, within=not unbounded and row['ms'] <= (60.0 if row['path'][0].startswith(hooks.QUEUED_PATH) else bound), unbounded=unbounded,"),
 ('am-bound-field-srp', 'run', "bound = hooks.bound_ms(row['family']) + row['wait_ms']\n    unbounded", "bound = (hooks.AMENDED_SRP_MS if row['family'] == 'srp' else hooks.bound_ms(row['family'])) + row['wait_ms']\n    unbounded"),
 ('am-slack-reads-column', 'run', "return round(r['bound_ms'] * cpu_hz / 1000) - r['cpu_cycles']", "return round(hooks.amended_ms(r, 2) * cpu_hz / 1000) - r['cpu_cycles']"),
 ('am-misses-read-column', 'run', "misses=sum(not r['within'] for r in mine)", "misses=sum(r['unbounded'] or r['ms'] > hooks.amended_ms(r, 2) for r in mine)"),
 ('am-table-verdict-reads-column', 'run', "f\"{'yes' if r['within'] else 'NO'} | \"", "f\"{'yes' if r['ms'] <= hooks.amended_ms(r, interfaces) else 'NO'} | \""),
 ('am-cell-reads-column', 'run', "verdict = '' if r['within'] else ' **over its bound**'", "verdict = '' if r['ms'] <= hooks.amended_ms(r, 2) else ' **over its bound**'"),
]
def apply(src, old, new):
    if src.count(old) != 1:
        raise SystemExit(f'text matches {src.count(old)} times: {old!r}')
    return src.replace(old, new)
def child(which, old, new):
    sys.path.insert(0, str(H))
    sys.dont_write_bytecode = True
    path = H / f'{which}.py'
    src = apply(path.read_text(), old, new) if old else path.read_text()
    if which == 'hooks':
        m = types.ModuleType('hooks'); m.__file__ = str(path); sys.modules['hooks'] = m
        import dataclasses  # noqa
        exec(compile(src, str(path), 'exec'), m.__dict__)
    else:
        import hooks  # noqa
        m = types.ModuleType('run'); m.__file__ = str(path); sys.modules['run'] = m
        exec(compile(src, str(path), 'exec'), m.__dict__)
    import hooks_selftest as st
    from contextlib import ExitStack
    out = {k: v for k, v in st.run_checks().items() if v}
    for name, make, named in st.MUTANTS:
        with ExitStack() as stack:
            stack.enter_context(make())
            got = st.run_checks()
        if got[named] is None:
            out[f'MUTANT ESCAPED: {name}'] = named
    return out
def fork(which, old, new):
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(r)
        try:
            out = child(which, old, new)
        except BaseException as e:  # noqa
            out = {'__crash__': f'{type(e).__name__}: {e}'}
        os.write(w, json.dumps(out).encode()[:60000]); os._exit(0)
    os.close(w); data = b''
    while True:
        b = os.read(r, 65536)
        if not b: break
        data += b
    os.waitpid(pid, 0)
    return json.loads(data)
base = fork('run', '', '')
print('unmutated failing checks:', list(base))
killed = 0; survivors = []
for name, which, old, new in M:
    got = fork(which, old, new)
    if got:
        killed += 1
    else:
        survivors.append(name)
    first = next(iter(got.items()), ('-', ''))
    print(f"{'KILLED  ' if got else 'SURVIVED'} {name} | {len(got)} failure(s) | {first[0]} | {str(first[1])[:90]}")
print(f'{killed} of {len(M)} killed; survivors {survivors}')
