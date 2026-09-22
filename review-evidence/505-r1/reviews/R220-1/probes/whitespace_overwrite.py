"""Rebuild _selftest_whitespace's world at base and head and report which carrier
bodies still carry a backslash-newline continuation when check(world) runs."""
import sys, pathlib, importlib.util, copy, inspect, re
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
for tag in ("base", "head"):
    ce = load(f"/tmp/r220-pristine/{tag}/scripts/ci_events.py", f"ce_{tag}")
    P = ce.parse_world(ce.read_tree(pathlib.Path(f"/tmp/r220-pristine/{tag}")))
    captured = {}
    orig_check = ce.check
    def spy(world, _orig=orig_check):
        captured["w"] = copy.deepcopy(world)
        return _orig(world)
    ce.check = spy
    try:
        problems, n = ce._selftest_whitespace(P)
    finally:
        ce.check = orig_check
    w = captured["w"]
    cont = []
    for path in (ce.DOCS, ce.ELABORATE):
        for jid in ce.PUBLIC_NAMES[path]:
            for i, s in enumerate(ce._job_steps(w, path, jid)):
                if isinstance(s.get("run"), str) and "\\\n" in s["run"]:
                    cont.append(f"{jid} step {i+1} ({s['name']})")
    gate = [s.get("name") for s in ce.steps(ce.jobs(w[ce.RTL_FULL])[ce.GATE_JOB]) if isinstance(s.get("run"), str) and "\\\n" in s["run"]]
    print(f"{tag}: whitespace control problems={problems}; carrier bodies with a continuation at check time: {cont or 'none'}; gate-job steps with one: {gate}")
