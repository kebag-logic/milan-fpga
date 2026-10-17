"""Plant a realtime step in a copy of the capture read-time record and run the published bound tool.
usage: probe_rt_step.py <bound_py> <cycles.jsonl> <peer_pcap> <cap_lr_raw> <cap_ts_bin> <work_dir> <step_s>"""
import subprocess, sys
from pathlib import Path
import numpy as np
bound, cyc, pcap, lr, tsf, work, step = sys.argv[1:8]
work = Path(work); work.mkdir(parents=True, exist_ok=True)
ts = np.fromfile(tsf, dtype=[("f", "<i8"), ("rt", "<f8"), ("mono", "<i8")])
ts["rt"][len(ts) // 2:] += float(step)
out = work / f"cap-ts-step-{step}.bin"; ts.tofile(out)
r = subprocess.run([sys.executable, "-I", "-B", bound, cyc, pcap, lr, str(out), str(work / f"bound-step-{step}.json")],
                   capture_output=True, text=True)
print(f"planted realtime step {step} s at read {len(ts)//2}: rc {r.returncode}; stderr tail: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ''}")
out.unlink(missing_ok=True)
