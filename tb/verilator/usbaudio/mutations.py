#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Plant one protocol-leaf defect at a time; require its named runtime check.

The output directory must be new. No cleanup is performed. Optional temporary
filenames are recorded in the supplied ledger before the build starts.
Compilation failures and unrelated runtime failures never count as detections.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import resource
import shutil
import subprocess

# name, leaf, original, replacement, required runtime assertion
PLANTS = (
    ("magic", "record", "data_i == 16'h554f", "data_i != 16'h0000", "BAD_RECORD_DRAIN"),
    ("digest", "record", "data_i == DIGEST_P", "data_i != 16'h0000", "BAD_RECORD_DRAIN"),
    ("length_limit", "record", "data_i <= 224", "data_i <= 256", "BAD_RECORD_DRAIN"),
    ("whole_frames", "record", "data_i[4:0] == 0", "data_i[0] == 0", "BAD_RECORD_DRAIN"),
    ("reserved_flags", "record", "data_i[15:3] == 0", "data_i[15:4] == 0", "BAD_RECORD_DRAIN"),
    ("payload_active", "record", "data_i[1:0] == 2'b11", "data_i[1:0] != 0", "BAD_RECORD_DRAIN"),
    ("inactive_state", "record", "length_bytes_r == 0 || data_i[1:0]",
     "length_bytes_r == 0 && data_i[0] || data_i[1:0]", "COMPLETE_RECORD"),
    ("channel_bits", "record", "<= data_i;\n        payload_word_r",
     "<= {data_i[15:8], 8'b0};\n        payload_word_r", "PCM_ALL_BITS_ORDER"),
    ("capture_epoch", "record", "capture_epoch_o[31:16] <= data_i",
     "capture_epoch_o[31:16] <= 16'b0", "INDEPENDENT_EPOCHS"),
    ("playback_epoch", "record", "playback_epoch_o[15:0] <= data_i",
     "playback_epoch_o[15:0] <= 16'b0", "INDEPENDENT_EPOCHS"),
    ("frame_count", "record", "3'(data_i >> 5)", "3'(data_i >> 6)", "FRAME_COUNT"),
    ("early_record", "record", "if (length_bytes_r != 0) state_r <= PAYLOAD_S",
     "if (length_bytes_r != 0) state_r <= COMPLETE_S", "PARTIAL_NOT_VISIBLE"),
    ("record_stall", "record", "state_r == COMPLETE_S && record_ready_i",
     "state_r == COMPLETE_S", "RECORD_BACKPRESSURE"),
    ("status_magic", "status", "16'h5541", "16'h5540", "STATUS_BYTES"),
    ("status_digest", "status", "capture_epoch_i, DIGEST_P,", "capture_epoch_i, DIGEST_P ^ 16'h0001,", "STATUS_BYTES"),
    ("status_epoch", "status", "{capture_epoch_i, DIGEST_P",
     "{capture_epoch_i ^ 32'h00010000, DIGEST_P", "STATUS_BYTES"),
    ("status_sequence", "status", "sequence_r + 1'b1", "sequence_r + 16'd2", "STATUS_BYTES"),
    ("status_end", "status", "word_r == 9", "word_r == 8", "STATUS_LENGTH"),
    ("status_stall", "status", "valid_o && ready_i", "valid_o", "STATUS_BYTES"),
    ("status_snapshot", "status", "snapshot_valid_i && snapshot_ready_o", "snapshot_valid_i", "STATUS_BYTES"),
    ("feedback_scale", "feedback", "16 - WINDOW_LOG2_P", "15 - WINDOW_LOG2_P", "FEEDBACK_VALUE"),
    ("feedback_window", "feedback", "if (&intervals_r)", "if (intervals_r == 8190)", "FEEDBACK_WINDOW_LENGTH"),
    ("feedback_reference", "feedback", "else if (interval_i)", "else if (locked_i)", "FEEDBACK_WINDOW_LENGTH"),
    ("feedback_unlock", "feedback", "locked_i ? feedback_r : 32'd0",
     "locked_i ? feedback_r : 32'h00060000", "FEEDBACK_UNLOCKED"),
)


def main() -> int:
    """Build independent source defects and require their named checks."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--cleanup-ledger", type=Path)
    parser.add_argument("--temporary-file", action="append", default=[])
    parser.add_argument("--only", action="append", default=[])
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("jobs must be positive")
    if args.temporary_file and not args.cleanup_ledger:
        parser.error("temporary filenames require a cleanup ledger")
    args.out.mkdir(parents=True, exist_ok=False)
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    here = Path(__file__).resolve().parent
    rtl = here.parents[2] / "hdl" / "milan" / "usbaudio"
    originals = {p.name: p.read_text() for p in sorted(rtl.glob("*.sv"))}
    results = []
    selected = [p for p in PLANTS if not args.only or p[0] in args.only]
    if not selected:
        parser.error("no selected plants")
    for name, leaf, old, new, expected in selected:
        # Preserve the free-space floor before every build; never clean another tree.
        if shutil.disk_usage(args.out).free < 19 * 1024**3:
            raise RuntimeError("free-space guard: build deferred")
        case = args.out / name
        case.mkdir()
        sources = []
        for filename, original in originals.items():
            content = original
            if filename == f"KL_usbaudio_{leaf}.sv":
                if original.count(old) != 1:
                    raise RuntimeError(f"{name}: plant must match exactly once")
                content = original.replace(old, new)
            source = case / filename
            source.write_text(content)
            sources.append(str(source))
        obj = case / "build"
        if args.cleanup_ledger:
            with args.cleanup_ledger.open("a") as ledger:
                for filename in args.temporary_file:
                    target = obj / filename
                    if target.parent != obj or not filename:
                        raise ValueError("temporary filename must be a basename")
                    ledger.write(f"Planned generated temporary removal: {target.resolve()}\n")
        command = [args.engine, "--binary", "--timing", "--top-module", "protocol_tb",
                   "-Wall", "-Wno-TIMESCALEMOD", "-Wno-fatal", "--build-jobs", str(args.jobs),
                   "--Mdir", str(obj), *sources, str(here / "protocol_tb.sv")]
        with (case / "compile.log").open("w") as log:
            compiled = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
        if compiled.returncode:
            results.append({"plant": name, "result": "BUILD_FAILED"})
        else:
            run = subprocess.run([str(obj / "Vprotocol_tb"), f"+case={leaf}"],
                                 text=True, capture_output=True, timeout=180, check=False)
            (case / "run.log").write_text(run.stdout + run.stderr)
            caught = run.returncode != 0 and f"CHECK {expected}" in run.stdout + run.stderr
            results.append({"plant": name, "check": expected,
                            "result": "CAUGHT" if caught else "NOT_CAUGHT"})
        (args.out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        print(json.dumps(results[-1]), flush=True)
    return 0 if all(row["result"] == "CAUGHT" for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
