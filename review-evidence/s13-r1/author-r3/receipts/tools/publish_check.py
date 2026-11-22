#!/usr/bin/env python3
"""publish_check.py PACKET COPY WORK: the packet as the evidence archive will publish it, then its replay and plants.

The archive's rule, as the manager states it for round 3: a file the privacy scrub (privacy.scrub_redact) would
alter is not published as is: a binary is refused and left out (BINARY-MASK-REFUSED), a text file is published
scrubbed. COPY receives every file under that rule; each refusal or alteration is listed. Then tools/replay.py and
tools/rmutants.py run over COPY. Exit 0 only when nothing is refused or altered, the replay holds and every plant
is caught."""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "<home>/milan-fpga-management/2026-09-23")
import privacy  # noqa: E402

PACKET, COPY, WORK = (Path(a).resolve() for a in sys.argv[1:4])
if COPY.exists():
    shutil.rmtree(COPY)
refused, altered, n = [], [], 0
for path in sorted(p for p in PACKET.rglob("*") if p.is_file()):
    rel = path.relative_to(PACKET)
    data = path.read_bytes()
    scrubbed = privacy.scrub_redact(data)
    if scrubbed != data and b"\0" in data[:8000]:
        refused.append(str(rel))
        continue
    if scrubbed != data:
        altered.append(str(rel))
    (COPY / rel).parent.mkdir(parents=True, exist_ok=True)
    (COPY / rel).write_bytes(scrubbed)
    n += 1
print(f"# the packet copied under the publication rule: {n} files written, {len(refused)} binaries refused "
      f"{refused}, {len(altered)} text files altered {altered}")
replay = subprocess.run([sys.executable, "-I", str(COPY / "tools/replay.py"), str(COPY)], capture_output=True,
                        text=True)
print(f"# python3 -I tools/replay.py . over that copy: exit {replay.returncode}")
print(replay.stdout + replay.stderr)
WORK.mkdir(parents=True, exist_ok=True)
plants = subprocess.run([sys.executable, "-I", str(COPY / "tools/rmutants.py"), str(COPY), str(WORK)],
                        capture_output=True, text=True)
print(f"# python3 -I tools/rmutants.py <copy> <work> over that copy: exit {plants.returncode}")
print(plants.stdout + plants.stderr)
ok = not refused and not altered and replay.returncode == 0 and plants.returncode == 0
print(f"== PUBLICATION CHECK: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
