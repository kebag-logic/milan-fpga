"""Probe the builder's simulation-shape keys at their boundaries, in scratch configs.
usage: python3 -I probe_boundaries.py TREE SCRATCH"""
import copy, sys, yaml
from pathlib import Path
tree, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb
base = yaml.safe_load((tree / "configs/endstation_ax7101_32x32.yaml").read_text())
def variant(name, edit):
    d = copy.deepcopy(base); edit(d); p = scratch / f"endstation_probe_{name}.yaml"; p.write_text(yaml.safe_dump(d)); return p
def more(d, n):
    for k in ("listeners", "talkers"):
        lst = d["streams"][k]
        while len(lst) < n: lst.append(dict(lst[-1], name=f"{lst[-1]['name'].rsplit(' ',1)[0]} {len(lst)}"))
        del lst[n:]
cases = [
    ("33 streams a direction, no saved state", lambda d: more(d, 33), "streams (max 32 per direction)"),
    ("17 streams with saved state on a simulation shape", lambda d: (more(d, 17), d.pop("saved_state")), "streams (max 16 per direction)"),
    ("simulation_only as a string", lambda d: d.__setitem__("simulation_only", "yes"), "is not true or false"),
    ("saved_state none without simulation_only", lambda d: d.pop("simulation_only"), "simulation shape's option"),
]
fails = 0
for label, edit, words in cases:
    try:
        eb.load_config(str(variant(label.split()[0] + str(len(label)), edit))); print(f"[FAIL] {label}: accepted"); fails += 1
    except eb.ConfigError as e:
        ok = words in str(e); fails += not ok; print(f"[{'ok' if ok else 'FAIL'}] {label}: refused: {str(e)[:160]}")
cfg = eb.load_config(str(variant("rtl_table", lambda d: d["srp"].__setitem__("rtl_table", True))))
try:
    eb.build(str(scratch / "endstation_probe_rtl_table.yaml"), str(scratch / "out"))
    print("[FAIL] srp.rtl_table on the simulation shape: built"); fails += 1
except eb.ConfigError as e:
    ok = "srp.rtl_table" in str(e); fails += not ok; print(f"[{'ok' if ok else 'FAIL'}] srp.rtl_table on the simulation shape: refused: {str(e)[:200]}")
print(f"boundary probe: {fails} failure(s)")
