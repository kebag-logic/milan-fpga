#!/usr/bin/env python3
"""The windows check 13 does not generate, run at this head (#671 round 4).

Usage: complement_windows.py <tree> <work> <jobs> <cfg-stem>

Check 13 starts a window at every read a clean boot opens. This builds every
window that starts at a later read, up to the bound (13 reads on a cold boot,
12 on a restart), one to four reads long, for every group, manner, orientation
and path, and checks that (1) the reference model gives each the clean boot's
read count and no unread slot, and (2) graded at this head with check 13's own
grade_fault_case, each gives no finding: the boot it meets has ended where a
clean one does, since the reads before the window are clean.
"""
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

tree, work, jobs, stem = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
sys.path.insert(0, str(tree / "sw/firmware/nvm_hosttest"))
import read_fault_cases as RF  # noqa: E402
import test_nvm_firmware as T  # noqa: E402

work.mkdir(parents=True, exist_ok=False)
bench = T.make_bench(tree / "configs" / f"{stem}.yaml", work / "bench", T.FIRMWARE.read_text())
body = T.KLJ2_HDR + (bench.img_len - T.KLJ2_HDR - T.KLJ2_TRAILER) // 2
cases, model_bad = [], 0
for restart in (True, False):
    for older, faulted, manners, seqs in RF.GROUPS:
        for valid in "ab":
            slot = valid if faulted == "valid" else ("b" if valid == "a" else "a")
            clean = RF.expect(RF.FaultCase(valid, older, seqs[0], ("--read-fault", f"{slot}:0:0:0"), 0, 0, restart))
            bound = RF.BOOT_READ_BOUND - (1 if restart else 0)
            for skip in range(clean.reads, bound):
                for count in range(1, RF.READ_TRIES + 2):
                    for i, manner in enumerate(manners):
                        c = RF.FaultCase(valid, older, seqs[(skip + count + i) % len(seqs)],
                                         RF.fault(manner, slot, skip, count, body), skip, count, restart)
                        e = RF.expect(c)
                        model_bad += (e.reads, e.unread, e.within) != (clean.reads, "", True)
                        cases.append(c)
print(f"{stem}: {len(cases)} windows starting after the clean boot's last read; "
      f"the model departs from the clean boot on {model_bad}")
fr = T.fault_run(bench)
seen, lock, out = {}, threading.Lock(), []


def walk(k: int) -> None:
    w = work / f"w{k}"
    w.mkdir()
    for c in cases[k::jobs]:
        got = T.grade_fault_case(bench, fr, c, w, seen)
        with lock:
            out.extend(got)


t0 = time.time()
with ThreadPoolExecutor(max_workers=jobs) as pool:
    list(pool.map(walk, range(jobs)))
print(f"{stem}: graded at this head in {time.time() - t0:.0f}s: {len(out)} findings")
for f in out[:5]:
    print("   ", f[:300])
