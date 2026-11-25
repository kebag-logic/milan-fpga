"""fbphases.py LOG...: one hosted firmware-boundary log each -> its step's phases (s): builders by name, the
phase after the builders up to the capture summary (images), and the judgement after it (controls, pins, stack
self-test), and the step's and job's windows."""
import re, sys
from datetime import datetime
def ts(line):
    m = re.search(r"\t(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+)Z ", line)
    return datetime.fromisoformat(m.group(1)[:26]) if m else None
print("run\tjob\tstep\trv32\tctrl_fw\tnvm\tcoverage\tmemory\tf5\tbuilders\timages\tjudge")
for path in sys.argv[1:]:
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    stamps = [ts(l) for l in lines if ts(l)]
    start = next(ts(l) for l in lines if "ctrl_boundary.py --require-rv32" in l and "##[group]Run" in l)
    last_builder = summary = end = None; b = {}
    for l in lines:
        m = re.search(r"    (\S+) (--[\w-]+).*: exit 0 \((\d+) s\)", l)
        if m and "ctrl_image" not in l and "ctrl_srp" not in l and "ctrl_plat" not in l:
            key = m.group(1).split("/")[-1]
            b[key] = b.get(key, 0) + int(m.group(3)); last_builder = ts(l)
        if "capture: " in l and "compiler invocations" in l: summary = ts(l)
        if "ctrl_boundary: PASS" in l: end = ts(l)
    job = (stamps[-1] - stamps[0]).total_seconds()
    name = path.split("/")[-1].split(".")[0]
    row = [name, f"{job:.0f}", f"{(end-start).total_seconds():.0f}",
           *(str(b.get(k, "")) for k in ("fw_rv32_selftest.py", "test_ctrl_firmware.py", "test_ctrl_nvm.py",
                                          "fw_coverage.py", "test_ctrl_memory.py", "stream_counter_f5.py")),
           f"{(last_builder-start).total_seconds():.0f}", f"{(summary-last_builder).total_seconds():.0f}",
           f"{(end-summary).total_seconds():.0f}"]
    print("\t".join(row))
