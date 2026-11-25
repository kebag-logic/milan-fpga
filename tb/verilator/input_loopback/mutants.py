#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Each planted media defect must fail the unmodified wire scoreboard."""
from pathlib import Path
import argparse
import json
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
QUEUE = ROOT / "hdl/ieee1722/aaf/KL_render_queue.sv"
PLANTS = (
    ("ignored_mapping", "assign copy_stream_w = {1'b0, entry_w[5:3]};",
     "assign copy_stream_w = 4'd0;", "COPY_SAMPLE"),
    ("wrong_bank", "return_bank_r <= copy_channel_w[0] ^ cons_w[0];",
     "return_bank_r <= !(copy_channel_w[0] ^ cons_w[0]);", "COPY_SAMPLE"),
    ("skipped_copy", "copy_active_r <= 1'b1;",
     "copy_active_r <= 1'b0;", "COPY_SAMPLE"),
    ("ignored_invalidation", "wire invalidate_w = input_invalidate_i || (|flush_i)",
     "wire invalidate_w = 1'b0 || (|flush_i)", "COPY_SAMPLE"),
    ("retained_word", "if (return_r)\n        samples_r",
     "if (return_r && return_valid_r && returned_w[24])\n        samples_r", "COPY_SAMPLE"),
    ("missing_clock_flush", "assign input_clock_flush_w = (32'(idle_cyc_r) == IDLE_CYC_C);",
     "assign input_clock_flush_w = 1'b0;", "COPY_SAMPLE"),
    ("wrong_latency", "64'(KMIN_C + 1) * PS3_L", "64'(KMIN_C + 2) * PS3_L", "COPY_SAMPLE"),
)


def main() -> None:
    """Require a clean run and a named sample failure for every planted defect."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    text = QUEUE.read_text()
    results = []
    for name, old, new, assertion in (("control", "", "", ""), *PLANTS):
        with tempfile.TemporaryDirectory(dir=args.output, prefix=name+"-") as temp:
            where = Path(temp)
            source = where / QUEUE.name
            if old:
                assert text.count(old) == 1, name
            source.write_text(text.replace(old, new, 1) if old else text)
            command = ["make", "-s", "-C", str(ROOT / "tb/verilator/input_loopback"), "run",
                       "VERILATOR_JOBS=4", "MDIR="+str(where / "obj"), "QUEUE_SRC="+str(source)]
            log = args.output / (name+".log")
            with log.open("w") as sink:
                result = subprocess.run(command, stdout=sink, stderr=subprocess.STDOUT)
            output = log.read_text()
            passed = ((result.returncode == 0 and "PASS input-loopback" in output) if not old else
                      (result.returncode != 0 and "FAIL "+assertion in output
                       and "FAIL input-loopback" in output))
            results.append(dict(plant=name, command=command, exit=result.returncode, passed=passed))
            print(name, "PASS" if passed else "FAIL", flush=True)
            (args.output / "results.json").write_text(json.dumps(results, indent=2)+"\n")
            if not passed:
                raise SystemExit(1)


if __name__ == "__main__":
    main()
