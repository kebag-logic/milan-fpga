#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Require runtime sample failures for broken parent connections and retention."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    dp = (ROOT / "hdl/milan/milan_datapath.sv").read_text()
    queue = (ROOT / "hdl/ieee1722/aaf/KL_render_queue.sv").read_text()
    pulse = "else invalidate_r <= edit_change_w || direct_change_w || restore_change_w;"
    plants = [("control1", 1, None, None), ("control8", 8, None, None),
              ("missing_edit_invalidation", 8, "dp", [(pulse, pulse.replace("edit_change_w", "1'b0"))]),
              ("disconnected_map", 8, "dp", [("{(INPUT_LOOPBACK_P != 0){amap_in_store_r,", "{(INPUT_LOOPBACK_P != 0){(AMAP_IN_KEYS_C*8)'(0),")]),
              ("overwritten_capture_page", 1, "queue", [
                  ("cons_w[2:0]", "{1'b0, cons_w[1:0]}"),
                  ("page_frame_r[read_page_w][2:0]", "{1'b0, read_page_w}")]),
              ("truncated_claim_page", 1, "queue", [
                  ("page_frame_r[read_page_w][2:0]", "{1'b0, read_page_w}")])]
    results = []
    for name, shape, kind, replacements in plants:
        work = out / name
        work.mkdir(exist_ok=True)
        cmd = [sys.executable, str(HERE / "run.py"), "--shape", str(shape), "--work", str(work)]
        if kind:
            source = dp if kind == "dp" else queue
            for old, new in replacements:
                count = source.count(old)
                expected = 1
                if count != expected:
                    raise RuntimeError((name, "anchor count", count, expected))
                source = source.replace(old, new)
            target = work / ("milan_datapath.sv" if kind == "dp" else "KL_render_queue.sv")
            target.write_text(source)
            cmd += ["--dp-source" if kind == "dp" else "--queue-source", str(target)]
        log = out / (name + ".log")
        with log.open("w") as sink:
            result = subprocess.run(cmd, stdout=sink, stderr=subprocess.STDOUT, timeout=7200)
        text = log.read_text()
        built = (work / "obj/parent_loopback").is_file()
        passed = (result.returncode == 0 and "RESULT: PASS" in text) if not kind else (
            built and result.returncode != 0 and "[FAIL] PARENT_SAMPLE" in text and "RESULT: FAIL" in text)
        results.append(dict(name=name, command=cmd, exit=result.returncode, built=built, passed=passed,
                            log_sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
        (out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        print(name, "PASS" if passed else "FAIL", flush=True)
        if not passed:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
