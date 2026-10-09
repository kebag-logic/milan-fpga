#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove the startup checks reject stale timestamps and invalid first PDUs.

Each arm builds a disposable packetizer through the suite's own recipe.
Only rc 1 with the named assertion is a caught defect. Compile failures,
crashes and missing assertions fail this campaign. All loops in the leg
are bounded by sample counts, independently of DUT progress.
"""

import argparse
import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv"
# name, unique source text, replacement, required failed assertion
MUTATIONS = (
    ("stale admission restored",
     "                   (started_r[pown_t_w] || pown_o_w == '0) &&\n", "",
     "startup step equals steady"),
    ("disable keeps the previous start",
     "          started_r[t] <= 1'b0;", "          started_r[t] <= started_r[t];",
     "startup step equals steady"),
    ("reset keeps the previous start",
     "        started_r[t] <= 1'b0;", "        started_r[t] <= started_r[t];",
     "startup step equals steady"),
    ("offset omitted", "+ transit_ns_i[32*(32'(pown_t_w)) +: 32];", "+ 32'd0;",
     "sample plus offset"),
    ("normal timestamp marked invalid",
     "fb[19]={1'b1, 3'b000, emr_r, 2'b00, 1'b1};",
     "fb[19]={1'b1, 3'b000, emr_r, 2'b00, 1'b0};", "valid normal timestamp"),
    ("sequence held", "{24'd0, eseq_r + 8'd1}", "{24'd0, eseq_r}",
     "consecutive sequence"),
    ("bank never published", "pend_r[pown_t_w]  <= 1'b1;", "pend_r[pown_t_w]  <= 1'b0;",
     "bounded first ten"),
    ("left samples corrupt", "assign stg_wdata_w = {pair_l_i, pair_r_i};",
     "assign stg_wdata_w = {pair_l_i ^ 24'd1, pair_r_i};", "complete sample rows"),
)


def run_arm(arm: tuple[str, str, str, str], parent: Path) -> bool:
    """Build and grade one mutation without changing tracked sources."""
    name, old, new, assertion = arm
    source = RTL.read_text()
    # Compare whole lines for reset/disable: their indentation distinguishes
    # two sites. A substring count would mistake the longer indentation.
    if "started_r[t]" in old:
        old = "\n" + old + "\n"
        new = "\n" + new + "\n"
    if source.count(old) != 1:
        print(f"[FAIL] {name}: expected one planting site", flush=True)
        return False
    work = parent / name.replace(" ", "_")
    work.mkdir()
    mutated = work / RTL.name
    mutated.write_text(source.replace(old, new))
    obj = work / "obj"
    command = ["make", "-j16", "--no-print-directory", "-C", str(HERE),
               "startup-build", f"START_RTL={mutated}", f"START_MDIR={obj}"]
    with (work / "build.log").open("w") as log:
        build = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
    if build.returncode != 0:
        print(f"[FAIL] {name}: build rc={build.returncode}", flush=True)
        print((work / "build.log").read_text()[-4000:])
        return False
    run = subprocess.run([str(obj / "VKL_aaf_packetizer")], capture_output=True,
                         text=True, check=False)
    caught = run.returncode == 1 and any(
        "[FAIL]" in line and assertion in line for line in run.stdout.splitlines())
    print(f"[{'PASS' if caught else 'FAIL'}] {name}: {assertion}; rc={run.returncode}",
          flush=True)
    if not caught:
        print((run.stdout + run.stderr)[-4000:])
    return caught


def main() -> int:
    """Run every declared arm and refuse any missed defect."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    # TMPDIR selects physical scratch storage for the entire campaign.
    with tempfile.TemporaryDirectory(prefix="aaf-start-", dir=os.environ.get("TMPDIR")) as temp:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(lambda arm: run_arm(arm, Path(temp)), MUTATIONS))
    print(f"startup mutants: {sum(results)}/{len(results)} caught")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
