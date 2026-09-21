import importlib.util
import json
from pathlib import Path
import shutil
import sys

ev = Path('/data/milan/reviews/r217-scratch/evidence/design-evidence/500-materialization/proposal-evidence')
spec = importlib.util.spec_from_file_location('d3probe', ev / 'run.py')
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)
scratch = Path('/data/milan/reviews/r217-scratch')
h = scratch / 'probe-harness'
shutil.copytree(r.HARNESS, h, dirs_exist_ok=True)
r.HARNESS = h
r.STUBS = h / 'stubs'
# Keep the writer, arbiter, stores, port, backend and firmware unchanged.
# Only vary the fault stimulus, using the public harness's cycle callback.
f = h / 'd3_cases.cpp'
s = f.read_text()
old = '    read_fault(0x80, 8 + 16, -1);\n    boot();'
new = '''    if (variant == "second-pass") {
      // Two device reads (header and payload) finish the first 0x80 visit.
      // Arm only then: the second restore pass encounters the read error.
      on_cycle([] {
        unsigned reads = 0;
        for (const auto &op : evlog.ops)
          if (op.rid == 0x80 && op.op == 0 && op.res == "done") ++reads;
        if (reads < 2) return false;
        read_fault(0x80, 8 + 16, -1);
        std::printf("REVIEW second-pass read error armed at %llu\\n", (unsigned long long)cyc);
        return true;
      });
    } else {
      read_fault(0x80, 8 + 16, -1);
    }
    boot();'''
assert s.count(old) == 1
s = s.replace(old, new)
# A separate case uses a delayed backend memory response. It returns just
# after the public firmware timeout, demonstrating late writes after enable.
anchor = '  cases["V10_blank_first_boot"] = [] {'
addition = '''  cases["R217_restore_timeout"] = [] {
    boot();
    snap("after_timeout");
    idle(600);
    snap("after_late_restore");
  };
'''
assert s.count(anchor) == 1
f.write_text(s.replace(anchor, addition + anchor))
# Fault mode 2 is selected by the new case through a private environment
# switch; affect the first D3 record request, after the binding walk only.
b = h / 'd3_bridge.cpp'
s = b.read_text()
old = '  if (rtake) rd = Rd{true, 2, dut->mem_req_addr_o};'
new = '''  if (rtake) {
    rd = Rd{true, 2, dut->mem_req_addr_o};
    static bool delayed = false;
    if (std::getenv("R217_DELAY_RESTORE") && !delayed && dut->own_o) {
      delayed = true;
      rd.delay = 3500000;
      std::printf("REVIEW delayed D3 read at %llu\\n", (unsigned long long)cyc);
    }
  }'''
assert s.count(old) == 1
b.write_text(s.replace(old, new))
shapes = {n: r.prep_shape(n) for n in ['1x1']}
shape = shapes['1x1']
build = r.Build('reviewer-probes', '1x1')
r.do_build(build, shape, 8)
case = 'V11_torn_read_restores_nothing'
slots, over = r.crafted_for(shape, case)
for variant in ['', 'second-pass']:
    result = r.run_case(build, shape, case, variant, slots)
    grade = r.grade_run(result, shape, {'crafted': over})
    print('PROBE', variant or 'first-pass', 'exit', result.rc, 'completed', result.done, flush=True)
    print(json.dumps(grade.checks, indent=2), flush=True)
    print('OBS', json.dumps(result.obs.get('restored')), flush=True)
import os
os.environ['R217_DELAY_RESTORE'] = '1'
result = r.run_case(build, shape, 'R217_restore_timeout', '', slots)
print('TIMEOUT PROBE', 'exit', result.rc, 'completed', result.done, flush=True)
print(json.dumps(result.obs, indent=2), flush=True)
print('BOOT', [e for e in result.evts if e['k'] == 'boot'], flush=True)
print('FIRMWARE', result.fw, flush=True)
