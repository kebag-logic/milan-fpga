#!/usr/bin/env python3
"""R603-3's re-stage scenario on this head (#671 round 4): slot A blank, slot B
valid at 0x5A5A5, A's one judgement read answered with B's container
(--read-other a:1:1), so A is picked on the tie and every re-stage read of A
is refused. Runs the head and the two re-stage controls and prints each boot.

Usage: restage_hang.py <tree> <work> <cfg-stem>
"""
import subprocess
import sys
from pathlib import Path

tree, work, stem = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(tree / "sw/firmware/nvm_hosttest"))
import read_fault_cases as RF  # noqa: E402
import test_nvm_firmware as T  # noqa: E402

work.mkdir(parents=True, exist_ok=False)
text = T.FIRMWARE.read_text()
bench = T.make_bench(tree / "configs" / f"{stem}.yaml", work / "head", text)
a, b = work / "a.bin", work / "b.bin"
a.write_bytes(b"\xff" * T.SLOT)
b.write_bytes(bench.assemble(bench.frames, 0x5A5A5))
case = RF.FaultCase("b", False, 0x5A5A5, ("--read-other", "a:1:1"), 1, 1)
e = RF.expect(case)
print(f"model: reads={e.reads} unread={e.unread!r} unstaged={e.unstaged!r} within={e.within}")
for label in ("head", "p_restage_unbounded", "r_restage_four_tries"):
    planted = text
    for old, new in RF.READ_FAULT_MUTATIONS.get(label, ((),))[0] if label != "head" else ():
        planted = planted.replace(old, new)
    pb = bench if label == "head" else T.replant(bench, work / label, planted)
    for extra in ((), ("--read-other", "a:1:1")):
        r = subprocess.run([str(pb.binary), "--slot-a", str(a), "--slot-b", str(b), *extra,
                            "--boot", "--idle-ms", "100"], capture_output=True, text=True, timeout=600)
        s = T.host_state(r.stdout)
        print(f"== {label} {'fault ' + ' '.join(extra) if extra else 'clean'}: rc={r.returncode} "
              f"boot_reads={s.get('boot_reads')} reads={s.get('reads')} walks={s.get('walks')} "
              f"storm={'HOST read storm' in r.stdout}")
        for line in r.stdout.splitlines():
            if line.startswith("Milan NVM:") or line.startswith("HOST read storm"):
                print("   ", line[:260])
