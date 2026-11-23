#!/usr/bin/env python3
"""dt5-plant.py REPOSITORY SCRATCH: prove DT5 detects a data delay frozen on bubbles.

Run under the pinned simulation environment in a separate memory-limited unit.
Builds and binaries stay in SCRATCH; no repository file is modified.
"""
from pathlib import Path
import difflib
import hashlib
import subprocess
import sys

repo, work = map(lambda p: Path(p).resolve(), sys.argv[1:])
work.mkdir(parents=True, exist_ok=True)
suite = repo / "tb/verilator/avtp_rxmon"
source = repo / "hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv"
text = source.read_text()
start = "  always_ff @(posedge clk_i) begin : tap_delay_data\n"
end = "  end : tap_delay_data\n"
assert text.count(start) == text.count(end) == 1
mutated = text.replace(start, start + "    if (tap_acc_w) begin\n").replace(end, "    end\n" + end)
plant = work / source.name
plant.write_text(mutated)
(work / "dt5-plant.diff").write_text("".join(difflib.unified_diff(
    text.splitlines(True), mutated.splitlines(True), fromfile=str(source.relative_to(repo)),
    tofile="plant/KL_aaf_rx_depacketizer.sv")))
head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
print(f"Head: {head}", flush=True)
print("Plant: tap-delay data stages shift only on an accepted input beat; valid still shifts every cycle.", flush=True)
word = "[DT5] cases whose every output frame is whole, in order, under its index"
for name, src in (("control", source), ("plant", plant)):
    mdir = work / f"obj_{name}"
    cmd = ["make", "-j16", "-s", "-C", str(suite), "depkt-build", "DT_LEAD=0",
           f"DT_MDIR={mdir}", f"DEPKT_SRC={src}"]
    with (work / f"{name}-build.log").open("w") as log:
        build = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=420)
    print(f"{name} build rc={build.returncode}", flush=True)
    assert build.returncode == 0
    exe = mdir / "Vdepkt"
    b = exe.read_bytes()
    print(f"{name} executable: {len(b)} bytes sha256 {hashlib.sha256(b).hexdigest()}", flush=True)
    run = subprocess.run([str(exe)], cwd=suite, capture_output=True, text=True, timeout=60)
    output = run.stdout + run.stderr
    (work / f"{name}-run.log").write_text(output)
    hits = [line for line in output.splitlines() if word in line]
    print(f"{name} run rc={run.returncode}", flush=True)
    print("\n".join(hits), flush=True)
    assert hits
    if name == "control":
        assert run.returncode == 0 and all("[FAIL]" not in line for line in hits)
    else:
        assert run.returncode != 0 and any("[FAIL]" in line for line in hits)
print("DT5 planted data-delay defect: caught by name; control passes.", flush=True)
