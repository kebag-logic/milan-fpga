#!/usr/bin/env python3
"""R358-1 probe: does the packet's own tools/summarize.py fail when the library's
verdict or the enumeration is not clean?  Each mutant is a disposable copy of the
published author/ directory with one change; the unmutated copy must pass.

usage: probe_summarize_mutations.py <packet_author_dir> <scratch_dir>
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

src, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()


def edit_json(name, fn):
    def apply(d):
        p = d / name
        j = json.loads(p.read_text())
        fn(j)
        p.write_text(json.dumps(j, indent=4))
    return apply


def edit_text(name, old, new):
    def apply(d):
        p = d / name
        t = p.read_text()
        assert old in t, (name, old)
        p.write_text(t.replace(old, new, 1))
    return apply


def drop_cluster(j):
    sp = j["entity_model"]["entity_descriptor"]["configuration_descriptors"][0]
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "audio_cluster_descriptors" and isinstance(v, list) and v:
                    v.pop()
                    return True
                if walk(v):
                    return True
        elif isinstance(o, list):
            return any(walk(v) for v in o)
        return False
    assert walk(sp)


def static_change(j):
    e = j["entity_model"]["entity_descriptor"]["configuration_descriptors"][0]
    e["static"]["localized_description"] = {"index": 9, "offset": 9}


MUTANTS = {
    "baseline (no change)": None,
    "run-2 library drops MILAN": edit_json("run-2.entity.json", lambda j: j.__setitem__("compatibility_flags", ["IEEE17221"])),
    "run-3 library adds MILAN_WARNING": edit_json("run-3.entity.json", lambda j: j.__setitem__("compatibility_flags", ["IEEE17221", "MILAN", "MILAN_WARNING"])),
    "run-1 library flags MISBEHAVING": edit_json("run-1.entity.json", lambda j: j.__setitem__("compatibility_flags", ["IEEE17221", "MILAN", "MISBEHAVING"])),
    "all runs library drops MILAN": lambda d: [edit_json(f"run-{n}.entity.json", lambda j: j.__setitem__("compatibility_flags", ["IEEE17221"]))(d) for n in (1, 2, 3)],
    "run-1 compatibility event recorded": edit_json("run-1.entity.json", lambda j: j.__setitem__("compatibility_events", [{"x": 1}])),
    "run-2 one AUDIO_CLUSTER missing": edit_json("run-2.entity.json", drop_cluster),
    "run-3 static field differs": edit_json("run-3.entity.json", static_change),
    "run-1 log complaints=1": edit_text("run-1.log", "complaints=0", "complaints=1"),
    "run-2 log query-errors 1": edit_text("run-2.log", "query-errors 0", "query-errors 1"),
    "run-3 log rc=5": edit_text("run-3.log", "rc=0", "rc=5"),
    "run-1 wrong entity": edit_json("run-1.entity.json", lambda j: j["adp_information"]["common"].__setitem__("entity_id", "0x020000FFFE000002")),
}

bad = 0
for name, mut in MUTANTS.items():
    d = scratch / ("mut-" + "".join(c if c.isalnum() else "_" for c in name))
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(src, d)
    if mut:
        mut(d)
    r = subprocess.run([sys.executable, str(d / "tools" / "summarize.py")], capture_output=True, text=True, timeout=120)
    want_pass = mut is None
    ok = (r.returncode == 0) == want_pass
    bad += not ok
    tail = (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or [""])[-1][:110]
    print(f"{'OK  ' if ok else 'BAD '} {name}: rc={r.returncode} expected={'pass' if want_pass else 'fail'} | {tail}")
    shutil.rmtree(d)
print("RESULT", "PASS" if bad == 0 else "FAIL", bad)
sys.exit(1 if bad else 0)
