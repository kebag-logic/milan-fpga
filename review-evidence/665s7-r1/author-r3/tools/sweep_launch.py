"""sweep_launch.py SECONDS: launch each of the FULL sweep's 4 shards not yet launched (no sweep/shard-k), each the
moment cpu_ranges.py pick returns a free 8-CPU range, pick and launch back to back (sweep-shard.py); shard 2, which
holds capture_coherence, on the range's first 4 CPUs. Returns after SECONDS or when all four are launched."""
import subprocess
import sys
import time
from pathlib import Path

S = Path("/data-2/milan/tmp/665s7-a757c")
T = Path(__file__).resolve().parent
PICK = "$MANAGEMENT/2026-09-23/cpu_ranges.py"
end = time.time() + float(sys.argv[1])
while time.time() < end:
    pending = [k for k in (2, 0, 1, 3) if not (S / "sweep" / f"shard-{k}").exists()]
    if not pending:
        print("all four shards launched")
        break
    cpus = subprocess.run([sys.executable, PICK, "pick"], capture_output=True, text=True).stdout.strip()
    if cpus:
        k = pending[0]
        lo, hi = (int(x) for x in cpus.split("-"))
        mine = f"{lo}-{lo + 3}" if k == 2 else cpus
        out = subprocess.run([sys.executable, str(T / "sweep-shard.py"), str(k), mine], capture_output=True, text=True)
        print(time.strftime("%T"), f"shard {k} on {mine} (picked {cpus}): rc {out.returncode} {out.stdout.strip()[-200:]}"
              f"{out.stderr.strip()[-300:]}", flush=True)
        continue
    time.sleep(20)
print(time.strftime("%T"), "pending:", [k for k in (2, 0, 1, 3) if not (S / "sweep" / f"shard-{k}").exists()])
