# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R217's round-three probe, ADAPTED to run against the revision-d evidence.

The original is review-evidence/503-round3/reviews/R217/REVIEW-evidence/
probe_preload.py at commit 3d790bc1 (sha256
6605c56913fcea079040d00a94bc286792800ecd3118e8618ad9f4ed0a1c7cbc). It copied
the harness and PATCHED d3_top.sv to connect the unchanged pinned
KL_pp_acmp_listener, driving its talker-event face with the pinned acmp_nvm
suite's evt_block_i lever: a droppable event (sink 0xffff) held as a level,
from reset until R217_PRELOAD_RELEASE (never, for "held"; cycle 100000 for
"finite"). Revision d instantiates that same pinned listener in d3_top.sv
itself, behind the proposed admission gate (seam S4), so the patch's anchor
no longer exists. The adaptations, and the only ones:

1. PATH CONSTANTS come from the environment: PROBE_OUT (a scratch directory,
   required) and EVIDENCE (the proposal-evidence directory, default this
   file's sibling).
2. THE LEVER is the harness's own talker-event producer, held as the same
   level (lt_tk_drop: sink 0xffff, re-presented after every acknowledgement)
   from reset, for ever or to the same release cycle, instead of a patched
   port and an environment variable.
3. BOTH BUILDS: the probe runs its ten scenarios on the evidence's base
   wiring (the gate) AND on the mutant LG01_admission_deleted (the gate's
   masks deleted: the pinned wiring), so the counterexample is shown to come
   back exactly where the admission is removed.

Every case body, variant, seed slot (V1a's) and descriptor delay is the
reviewer's. It writes adjacent-probes-gate.json and
adjacent-probes-gate-deleted.json under PROBE_OUT/r217r3, in the reviewer's
row format; r217_r3_check.py grades them, and the reviewer's own
assert_review_observations.py (the same archive, sha256
fa0d6df89875828055666838397365781d539ac3d9a6a9ad65c30bceb370bba3) can be run
on each.
"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys

scratch = Path(os.environ["PROBE_OUT"]) / "r217r3"
ev = Path(os.environ.get("EVIDENCE", Path(__file__).resolve().parents[1] / "proposal-evidence"))
os.environ["D3_OUT"] = str(scratch / "d3")
spec = importlib.util.spec_from_file_location("r217_r3_d3", ev / "run.py")
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)
h = scratch / "probe-harness"
shutil.copytree(r.HARNESS, h, dirs_exist_ok=True)
r.HARNESS, r.STUBS = h, h / "stubs"
f = h / "d3_cases.cpp"
s = f.read_text()
needle = '  cases["V10_blank_first_boot"] = [] {'
assert s.count(needle) == 1
addition = '''  cases["R217_preload"] = [] {
    // ADAPTATION 2: the reviewer's evt_block_i level, as the harness's own
    // talker-event producer; the case body is the reviewer's
    if (variant == "held") lt_tkq.push_back(lt_tk_drop(0, 0));
    if (variant == "finite") lt_tkq.push_back(lt_tk_drop(0, 100000));
    boot(); idle(200); snap("terminal");
    read_row(SEL_PTOF, 0, "post.ptof0");
    idle(2000); snap("observed");
  };
  cases["R217_descriptor_boundary"] = [] {
    desc_delay_after_apply = std::stoll(variant);
    boot(); idle(200); snap("terminal");
    command_after_recovery(); snap("recovered");
  };
'''
f.write_text(s.replace(needle, addition + needle))
shape = r.prep_shape("1x1")
builds = {"gate": r.do_build(r.Build("r217-r3-gate", "1x1"), shape, 8),
          "gate-deleted": r.do_build(r.Build("r217-r3-gate-deleted", "1x1", mut="LG01_admission_deleted"), shape, 8)}
for key, b in builds.items():
    seed = r.run_case(b, shape, r.V1A)
    assert seed.rc == 0 and seed.done
    slots = (seed.out / "cut-slotA.bin", seed.out / "cut-slotB.bin")
    results = []
    for name in ("control", "held", "finite"):
        result = r.run_case(b, shape, "R217_preload", name, slots)
        d = {"variant": name, "rc": result.rc, "done": result.done, "obs": result.obs, "events": result.evts}
        results.append(d)
        print(key, json.dumps({"variant": name, "rc": result.rc, "done": result.done,
                               "terminal": result.obs.get("terminal", {}).get("restore_done")}), flush=True)
    for delay in (4094, 4095, 4096, 4097, 24090, 24098, 24100):
        result = r.run_case(b, shape, "R217_descriptor_boundary", str(delay), slots)
        d = {"variant": str(delay), "rc": result.rc, "done": result.done, "obs": result.obs, "events": result.evts}
        results.append(d)
        print(key, json.dumps({"variant": delay, "rc": result.rc, "done": result.done}), flush=True)
    (scratch / f"adjacent-probes-{key}.json").write_text(json.dumps(results, indent=2))
