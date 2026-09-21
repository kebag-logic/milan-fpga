# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R217's round-two probe, ADAPTED to run against the revision-c evidence.

The original is review-evidence/503-round2/R217/probes.py at commit 7d9da877
(sha256 94de822b7cf87a44c9cef93a9c771af463b7bebe40c1c5469bbb39a230eb452b).
Every stimulus and variant is the reviewer's. Two adaptations, and only two:

1. PATH CONSTANTS come from the environment: PROBE_OUT (a scratch directory,
   required) and EVIDENCE (the proposal-evidence directory, default this
   file's sibling).
2. THE ONE SEAM THAT MOVED: the reviewer patched d3_bridge.cpp to delay the
   first descriptor request accepted once the writer's applied count reads
   non-zero by 5,000 cycles. The revision-c bridge models the descriptor
   memory as a queue and carries that exact trigger as a knob,
   desc_delay_after_apply, so the variant arms the knob instead.

It writes probe-results.json under PROBE_OUT/r217; r217_check.py grades it
against the behaviour the reviewer demanded.
"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys

scratch = Path(os.environ["PROBE_OUT"]) / 'r217'
ev = Path(os.environ.get("EVIDENCE", Path(__file__).resolve().parents[1] / "proposal-evidence"))
os.environ["D3_OUT"] = str(scratch / "d3")
spec = importlib.util.spec_from_file_location('r217_d3', ev / 'run.py')
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)
h = scratch / 'probe-harness'
shutil.copytree(r.HARNESS, h, dirs_exist_ok=True)
r.HARNESS, r.STUBS = h, h / 'stubs'
f = h / 'd3_cases.cpp'
s = f.read_text()
old = '    read_fault(0x80, 8 + 16, -1);\n    boot();'
new = '''    if (variant == "original-second-pass") {
      on_cycle([] {
        unsigned reads = 0;
        for (const auto &op : evlog.ops)
          if (op.rid == 0x80 && op.op == 0 && op.res == "done") ++reads;
        if (reads < 2) return false;
        read_fault(0x80, 8 + 16, -1);
        return true;
      });
    } else { read_fault(0x80, 8 + 16, -1); }
    boot();'''
assert s.count(old) == 1
s = s.replace(old, new)
anchor = '  cases["V10_blank_first_boot"] = [] {'
addition = '''  cases["R217_transport_probes"] = [] {
    if (variant == "descriptor-initial-error") desc_mem_fail = true;
    if (variant == "header-repeat") read_fault(0x50, 0, -1);
    if (variant == "header-balanced") {
      read_fault(0x30, 0, -1, 0);
      read_fault(0x50, 0, -1, 1);
    }
    if (variant == "header-pass0") read_fault(0x50, 0, -1, 0);
    if (variant == "descriptor-error") {
      on_cycle([] {
        if (!levels().rs_app) return false;
        desc_mem_fail = true;
        return true;
      });
    }
    // ADAPTATION 2: the reviewer's bridge seam, as the evidence's own knob
    if (variant == "descriptor-timeout") desc_delay_after_apply = 5000;
    boot();
    idle(200);
    snap("terminal");
    read_row(SEL_CFG, 0, "post.cfg");
    read_row(SEL_CLKS, 0, "post.clks");
    read_row(SEL_FMTI, 0, "post.fmti0");
    read_row(SEL_PTOF, 0, "post.ptof0");
    read_name(0, "post.name0");
    settle();
    snap("observed");
  };
'''
assert s.count(anchor) == 1
f.write_text(s.replace(anchor, addition + anchor))
shape = r.prep_shape('1x1')
build = r.do_build(r.Build('reviewer-probes', '1x1'), shape, 8)
summaries = []
case = 'V11_torn_read_restores_nothing'
slots, over = r.crafted_for(shape, case)
for v in ['', 'original-second-pass']:
    result = r.run_case(build, shape, case, v, slots)
    grade = r.grade_run(result, shape, {'crafted': over})
    summary = {'case': case, 'variant': v, 'rc': result.rc, 'completed': result.done,
               'checks': grade.checks, 'obs': result.obs, 'snaps': result.snaps}
    summaries.append(summary)
    print('ORIGINAL', v or 'first-pass', json.dumps(grade.checks), flush=True)
seed = r.run_case(build, shape, r.V1A)
assert seed.rc == 0 and seed.done
slots = (seed.out / 'cut-slotA.bin', seed.out / 'cut-slotB.bin')
for variant in ['control', 'header-repeat', 'header-balanced', 'header-pass0', 'descriptor-error', 'descriptor-timeout', 'descriptor-initial-error']:
    result = r.run_case(build, shape, 'R217_transport_probes', variant, slots)
    summary = {'case': result.case, 'variant': variant, 'rc': result.rc, 'completed': result.done,
               'obs': result.obs, 'snaps': result.snaps, 'events': result.evts, 'fw': result.fw}
    summaries.append(summary)
    print('PROBE', variant, 'rc', result.rc, 'completed', result.done, flush=True)
    print(json.dumps(result.obs.get('observed', {})), flush=True)
    print('BOOT', json.dumps([e for e in result.evts if e['k'] == 'boot']), flush=True)
(scratch / 'probe-results.json').write_text(json.dumps(summaries, indent=2))
