#!/usr/bin/env python3
"""Lane B21 PR round 2: planted output-latency controls for b21_restart_bound.py (offline).

usage: b21_restart_controls.py <bound_py> <cycles.jsonl> <peer_link_pcap> <cap_lr_raw> <cap_ts_bin> <work_dir> <out_json>

A planted latency of D seconds is a copy of the external capture's sample record with round(D * 48000)
zero frames in front and as many frames cut from its end. The read-time record is unchanged, so every
sample reaches the reader D later: a constant extra output latency, the reviewer's counterexample.
Each control runs the published bound tool on the planted copy in its own process; it passes when the
tool's verdict and its set of failing cycles equal the expected ones. The expected failing cycles
follow from the as-measured upper bounds: a cycle fails when its upper bound plus D reaches 1 s.
"""
import json
import subprocess
import sys
from pathlib import Path

bound, cycles, pcap, cap_lr, cap_ts, work, out = sys.argv[1:8]
work = Path(work)
work.mkdir(parents=True, exist_ok=True)
FS = 48000


def run(lr, tag):
    o = work / f"bound-{tag}.json"
    r = subprocess.run([sys.executable, "-I", "-B", bound, cycles, pcap, str(lr), cap_ts, str(o)],
                       capture_output=True, text=True, timeout=900)
    (work / f"bound-{tag}.txt").write_text(r.stdout + r.stderr)
    g = json.load(open(o))
    return r.returncode, g


rc0, base = run(cap_lr, "as-measured")
ups = {c["cycle"]: c["upper_s"] for c in base["cycles"]}
res = dict(as_measured=dict(rc=rc0, verdict=base["verdict"], upper_max_s=base["upper_s"]["max"]), controls=[])
raw = Path(cap_lr).read_bytes()
ok_all = rc0 == 0 and base["verdict"] == "PASS"
for d in (0.5, 0.903, 1.0):
    n = round(d * FS)
    lr = work / f"cap-lr-plant-{n}.raw"
    lr.write_bytes(bytes(6 * n) + raw[:len(raw) - 6 * n])
    rc, g = run(lr, f"plant-{n}")
    fails = sorted(c["cycle"] for c in g["cycles"] if not c["pass_"])
    # a read quantum (at most 1,092 frames, 22.75 ms) separates the planted from the as-measured read
    exp_fail = sorted(c for c, u in ups.items() if u + d >= 1.0)
    exp_verdict = "FAIL" if exp_fail else "PASS"
    ok = g["verdict"] == exp_verdict and fails == exp_fail and rc == (1 if exp_fail else 0)
    ok_all &= ok
    res["controls"].append(dict(planted_s=d, planted_frames=n, verdict=g["verdict"], rc=rc, failing_cycles=fails,
                                expected_verdict=exp_verdict, expected_failing_cycles=exp_fail,
                                upper_max_s=g["upper_s"]["max"] if g.get("upper_s") else None, control_pass=ok))
    print(f"planted {d} s ({n} frames): verdict {g['verdict']} rc {rc}, failing cycles {fails}; expected {exp_verdict} {exp_fail}: "
          f"{'PASS' if ok else 'FAIL'}")
    lr.unlink()
res["all_controls_pass"] = ok_all
json.dump(res, open(out, "w"), indent=1)
print("as measured:", base["verdict"], "; all controls pass:", ok_all)
sys.exit(0 if ok_all else 1)
