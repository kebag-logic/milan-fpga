"""Every backlog group's script (owed_group, the delta's one changed script, among them) at the 1x1/1if and 8x8/2if points, from one tree's ctrl_service_budget scenario.py,
as JSON {point: {group: sha256}}, with the Point built directly (fixed identity values). usage: TREE"""
import dataclasses, hashlib, json, sys
from pathlib import Path
tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import scenario
out = {}
for label, shape, n_if, src, snk in (('1x1', 'endstation_ax7101_1x1_tdm8', 1, 2, 2), ('8x8', 'endstation_ax7101_8x8', 2, 9, 9)):
    build = {'shape': shape, 'interfaces': n_if}
    names = [f.name for f in dataclasses.fields(scenario.Point)]
    vals = dict(label=label, shape=shape, interfaces=n_if, entity_id=0x0102030405060708, mac=0x020304050607,
                sources=src, sinks=snk, layout=scenario.CONTRACT)
    p = scenario.Point(*[vals[n] for n in names])
    out[label] = {g.name: hashlib.sha256(g.script().encode()).hexdigest() for g in scenario.scaled(scenario.backlog_groups(p), p)}
print(json.dumps(out, sort_keys=True))
