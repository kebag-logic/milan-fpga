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
    pulse = "if (amap_edit_context_w && amap_edit_in_change_w) begin\n              input_loop_invalidate_r <= 1'b1;"
    plants = [("control1", 1, None, None), ("control8", 8, None, None),
              ("missing_edit_invalidation", 8, "dp", [(pulse, pulse.replace("1'b1", "1'b0"))]),
              ("disconnected_map", 8, "dp", [(".input_map_i (amap_in_store_r)", ".input_map_i ('0)")]),
              ("overwritten_capture_page", 1, "queue", [("cons_w[2:0]", "{1'b0, cons_w[1:0]}")])]
    results = []
    for name, shape, kind, replacements in plants:
        work = out / name
        work.mkdir(exist_ok=True)
        cmd = [sys.executable, str(HERE / "run.py"), "--shape", str(shape), "--work", str(work)]
        if kind:
            source = dp if kind == "dp" else queue
            for old, new in replacements:
                count = source.count(old)
                expected = 1 if kind == "dp" else 5
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
