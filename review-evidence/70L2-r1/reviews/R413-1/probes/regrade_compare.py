#!/usr/bin/env python3
"""Grade service traces with the base grader (dev 79c36963) and the head
grader (18199bac rule) and compare service findings and per-row bounds.
Traces: the three recorded oracle traces (old boot order) and the public
18199bac native receipts (AEM-first order). argv: base_run.py head_run.py
oracle.json receipt.json..."""
import copy, importlib.util, json, sys
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
base, head = load(sys.argv[1], "run_base"), load(sys.argv[2], "run_head")
traces = [(f"oracle[{i}] {r['shape']} {r['media'].get('plan')}", r) for i, r in enumerate(json.load(open(sys.argv[3])))]
traces += [(p.split('/')[-1], json.load(open(p))) for p in sys.argv[4:]]
fail = 0
for label, rec in traces:
    raw, media = rec['raw_log'], rec['media']
    out = {}
    # the only quantity 18199bac changes is the stretch bound; compare it on
    # every row the rule reads, whether or not service_findings() applies
    res = head.grade(raw, media)
    rows = [r for r in res['rows'] if r['duty'] not in ('boot_to_entity_enabled', 'maximum_heartbeat_gap')]
    changed = [(r['duty'], r['period_bound_ms'], b) for r in rows
               for b in [head.armed_bound(copy.deepcopy(r), res['events'])] if b != r['period_bound_ms']]
    print(f"{label}: rows read by the rule={len(rows)}; rows whose bound the rule changes={changed}")
    for tag, mod in (("base", base), ("head", head)):
        res = mod.grade(raw, media)
        try:
            f = mod.service_findings(res, raw)
        except RuntimeError as exc:
            f = 'N/A: ' + str(exc)
        out[tag] = (f, [(r['duty'], r.get('phy_publication_bound_ms'), r.get('armed_period_bound_ms')) for r in res['rows']])
    same_f = out['base'][0] == out['head'][0]
    same_b = [(d, p) for d, p, _ in out['base'][1]] == [(d, p) for d, p, _ in out['head'][1]]
    armed = [(d, round(a, 5)) for d, _, a in out['head'][1] if a is not None]
    print(f"{label}: base findings={out['base'][0]} head findings={out['head'][0]} "
          f"findings_equal={same_f} phy_bounds_equal={same_b} head_armed_rows={armed}")
    if 'oracle' in label and (changed or not (same_f and same_b)): fail += 1
print("OLD-ORDER TRACES REGRADE UNCHANGED" if not fail else f"{fail} OLD-ORDER TRACE(S) CHANGED")
