#!/usr/bin/env python3
# R603-3 disposable probe: drive one boot whose judgement read of a BLANK slot A
# is answered with slot B's valid container (an address fault, inside the
# documented fault model), so A is picked on the tie and every re-stage read of
# A is refused. Runs the same scenario on harness binaries already built by
# probe_plants.py (the unplanted head and a plant), and prints each boot's line,
# the reads it opened and whether the boot completed.
#
# usage: probe_restage_hang.py ROOT CONFIG WORK BIN_LABEL=BINARY...
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root, cfg, work = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
    import test_nvm_firmware as t  # noqa: E402

    work.mkdir(parents=True, exist_ok=False)
    bench = t.make_bench(cfg, work / "bench", (root / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text())
    a = work / "slot_a.bin"
    b = work / "slot_b.bin"
    a.write_bytes(b"\xff" * t.SLOT)
    b.write_bytes(bench.assemble(bench.frames, 0x5A5A5))
    rc = 0
    for spec in sys.argv[4:]:
        label, binary = spec.split("=", 1)
        r = subprocess.run([binary, "--slot-a", str(a), "--slot-b", str(b), "--read-other", "a:1:1",
                            "--boot", "--idle-ms", "100"], capture_output=True, text=True, timeout=900)
        out = r.stdout
        boot = t.BOOT_RE.search(out)
        state = t.host_state(out)
        storm = "HOST read storm" in out
        print(f"== {label}: rc={r.returncode} boot_line={'yes' if boot else 'NO'} "
              f"read_storm={'YES' if storm else 'no'} reads={state.get('reads')} "
              f"boot_reads={state.get('boot_reads')} walks={state.get('walks')}")
        for line in out.splitlines():
            if line.startswith("Milan NVM:") or line.startswith("HOST read storm"):
                print("   ", line[:300])
        rc |= r.returncode
    return rc


if __name__ == "__main__":
    sys.exit(main())
