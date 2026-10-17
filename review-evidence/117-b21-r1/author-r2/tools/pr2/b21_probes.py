#!/usr/bin/env python3
"""Lane B21 PR round 2: fault controls for the Direction B McASP grade (offline).

usage: b21_probes.py <noise_samples> <as_run_grade_py> <corrected_grade_py> <work_dir> <out_json>

<noise_samples> is a received-frame record of 4-slot noise (uint32 per slot, b21_aaf.py extract).
Every control takes N frames of it at a fixed wire offset as the "capture", plants one fault, writes
<work_dir>/<control>.pcm and runs both graders through their published command line
(mcasp <dir> <name> <wire_samples> 4 <prefix>), each in its own process. A control passes when the
corrected grader's counts equal the expected ones; the as-run grader's result is recorded beside it,
including a crash. The noise statistics the page quotes (frames equal to the one before, all-zero
frames, the slot values) are printed from the same record.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

noise, as_run, corrected, work, out = sys.argv[1:6]
work = Path(work)
work.mkdir(parents=True, exist_ok=True)
W = np.fromfile(noise, dtype="<u4").reshape(-1, 4)
OFF, N, K = 1000, 12000, 6000
wire = work / "wire.samples"
W.tofile(wire)


def nonzero_run(k, before=3, after=3):
    """first frame index >= k whose neighbours are all non-zero frames (so a planted zero is not
    equal to the wire frames it lands among)"""
    nz = ~np.all(W == 0, axis=1)
    while not nz[OFF + k - before:OFF + k + after].all():
        k += 1
    return k


def base():
    return W[OFF:OFF + N].copy()


controls = {}
controls["clean"] = (base(), dict(clean=True, matched=N, offset_changes=0, foreign_frames=0))
k = K
controls["skip_6"] = (np.concatenate([W[OFF:OFF + k], W[OFF + k + 6:OFF + N + 6]]),
                      dict(clean=False, skips=1, skipped_wire_frames=6, repeats_or_inserts=0, foreign_frames=0))
controls["repeat_1"] = (np.concatenate([W[OFF:OFF + k + 1], W[OFF + k:OFF + k + 1], W[OFF + k + 1:OFF + N]]),
                        dict(clean=False, skips=0, repeats_or_inserts=1, inserted_frames=1, foreign_frames=0))
k3 = nonzero_run(K)
controls["insert_3_zero_leading"] = (np.concatenate([W[OFF:OFF + k3], np.zeros((3, 4), np.uint32), W[OFF + k3:OFF + N]]),
                                     dict(clean=False, foreign_frames=3, foreign_zero=3, offset_changes=1,
                                          repeats_or_inserts=1, inserted_frames=3, skips=0))
m = base()
kb = nonzero_run(K)
m[kb, 1] ^= np.uint32(1 << 8)
controls["bit_flip"] = (m, dict(clean=False, foreign_frames=1, foreign_zero=0, offset_changes=0))
m = base()
m[kb] = 0
controls["zero_for_nonzero"] = (m, dict(clean=False, foreign_frames=1, foreign_zero=1, offset_changes=0))
# unequal words with the same 64-bit frame key: [0, 0, 0, 0] -> [0, 0, 256, 256000768]
# (key = ((0 * P ^ 0) * P ^ 256) * P ^ 256000768 with P = 1000003 is 0 for both)
m = base()
z = np.flatnonzero(np.all(m == 0, axis=1))
kc = int(z[np.searchsorted(z, K)])
m[kc] = np.array([0, 0, 256, 256000768], dtype=np.uint32)
controls["unequal_words_same_key"] = (m, dict(clean=False, foreign_frames=1, offset_changes=0))


def run(tool, name, tag):
    pre = work / f"{name}-{tag}"
    r = subprocess.run([sys.executable, "-I", "-B", tool, "mcasp", str(work), name, str(wire), "4", str(pre)],
                       capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        return dict(rc=r.returncode, error=r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "")
    g = json.load(open(str(pre) + "-mcasp.json"))
    g.pop("events", None)
    g["rc"] = 0
    if "clean" not in g:
        # the as-run version prints no verdict; "fully matched" is what its counts would have reported
        g["fully_matched"] = bool(g["matched"] == g["mcasp_frames"] and g["offset_changes"] == 0 and g["foreign_frames"] == 0)
    return g


res = dict(noise=dict(file=Path(noise).name, frames=int(len(W)), wire_offset=OFF, capture_frames=N,
                      planted_at=dict(skip_repeat=K, insert=k3, flip_zero=kb, collision=kc)))
eq = np.all(W[1:] == W[:-1], axis=1)
zr = np.all(W == 0, axis=1)
vals, cnt = np.unique(W, return_counts=True)
res["noise_stats"] = dict(frames_equal_to_previous=int(eq.sum()), fraction_equal_to_previous=round(float(eq.mean()), 4),
                          all_zero_frames=int(zr.sum()), fraction_all_zero=round(float(zr.mean()), 4),
                          slot_words={hex(int(v)): int(c) for v, c in zip(vals, cnt)})
ok_all = True
for name, (m, exp) in controls.items():
    m.astype("<u4").tofile(work / f"{name}.pcm")
    c = run(corrected, name, "corrected")
    a = run(as_run, name, "asrun")
    ok = c.get("rc") == 0 and all(c.get(k) == v for k, v in exp.items())
    ok_all &= ok
    res[name] = dict(expected=exp, corrected=c, control_pass=ok, as_run=a)
    print(f"{name}: corrected {'PASS' if ok else 'FAIL'} "
          f"{ {k: c.get(k) for k in list(exp) + ['matched']} }; as-run "
          f"{ {k: a.get(k) for k in ('rc', 'error', 'fully_matched', 'matched', 'foreign_frames', 'offset_changes') if k in a} }")
res["all_controls_pass"] = ok_all
print("noise:", json.dumps(res["noise_stats"]))
print("all controls pass:", ok_all)
json.dump(res, open(out, "w"), indent=1)
sys.exit(0 if ok_all else 1)
