#!/usr/bin/env python3
"""Usage: flow_identity_probe.py <repo> <scratch-dir>

Probe the recipe's claim that a measurement prepared without
--single-thread-synthesis is not comparable with baseline F (exit 2).
Uses the resource gate's own self-test fixture: the recorded baseline carries
`set_param synth.maxThreads 1` first in its script, as baseline F does; the
candidate either carries it (control, wanted 0) or omits it (wanted 2), and a
third arm moves it after synthesis (wanted 2)."""
import shutil
import sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "syn/ooc"))
import pp_resource_gate as gate            # noqa: E402
import pp_resource_gate_selftest as st     # noqa: E402

CAP = "set_param synth.maxThreads 1\n"
shutil.rmtree(scratch, ignore_errors=True)
scratch.mkdir(parents=True)
failures = 0
for kind in ("route", "ooc"):
    root = scratch / kind
    folder = st.fixture(root / "arm", kind)
    script = folder / gate.SCRIPTS[kind]
    script.write_text(CAP + script.read_text())
    entry = st.POLICY if kind == "route" else st.OOC_POLICY
    entry = {**entry, "record": gate.record(folder, kind)}
    assert entry["record"]["identity"]["flow"][0] == CAP.strip(), entry["record"]["identity"]["flow"]
    (root / "arm").rename(root / "pristine")
    arms = (("flag kept (control)", lambda t: t, 0),
            ("flag dropped", lambda t: t.replace(CAP, "", 1), 2),
            ("cap moved after synthesis", lambda t: t.replace(CAP, "", 1) + CAP, 2))
    for label, change, wanted in arms:
        cand = st.fresh(root, kind)
        s = cand / gate.SCRIPTS[kind]
        s.write_text(change(s.read_text()))
        try:
            c = gate.record(cand, gate.kind_of(cand))
            status, lines = gate.judge(entry, c, gate.routing(cand, c["kind"]))
        except gate.Refusal as error:
            status, lines = 2, [str(error)]
        ok = status == wanted
        failures += not ok
        print(f"{kind}\t{label}\texit {status}\twanted {wanted}\t{'PASS' if ok else 'FAIL'}\t{ascii(lines[0] if lines else '')}")
print(f"flow identity probe: {'PASS' if not failures else f'FAIL ({failures})'}")
sys.exit(1 if failures else 0)
