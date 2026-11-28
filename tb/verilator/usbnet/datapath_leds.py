#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run real datapath LED sources and plants at one and four stream inputs.

The wrapper drives the split image's stored-index port and forces media producers.
The production decoder, monitor export, six LED assignments and truth module
all execute unchanged. This does not measure media acquisition or command MMIO.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DP = ROOT / "hdl/milan/milan_datapath.sv"
MONITOR = ROOT / "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
# Each substitution must be unique and fail the named executable assertion.
PLANTS = (
    ("internal_decode", DP, "int_clk_selected_r <= int_sel_w;", "int_clk_selected_r <= aaf_sel_w;",
     "LD3 internal source decode"),
    ("stream_decode", DP, "aaf_sel_w ||\n", "1'b0 ||\n", "LD3 stream source decode"),
    ("source_index", DP, "avtprx_locked_all_w[aaf_follow_idx_r]", "avtprx_locked_all_w[0]",
     "LD3 selected input lock index"),
    ("source_crf", DP, ": crf_locked_w;", ": 1'b0;", "LD3 selected input lock index"),
    ("input_aaf", DP, "(|avtprx_locked_all_w) | crf_locked_w", "crf_locked_w",
     "LD2 input reduction includes AAF and CRF"),
    ("input_crf", DP, "(|avtprx_locked_all_w) | crf_locked_w", "(|avtprx_locked_all_w)",
     "LD2 input reduction includes AAF and CRF"),
    ("output_gate", DP, "o_led_output_open = |tkd_streaming_w", "o_led_output_open = tkd_streaming_w[0]",
     "LD2 output reduction includes every transmit gate"),
    ("internal_level", DP, "o_led_clock_internal = int_clk_selected_r", "o_led_clock_internal = follow_sel_r",
     "LD3 internal source decode"),
    ("stream_level", DP, "o_led_clock_stream = follow_sel_r", "o_led_clock_stream = int_clk_selected_r",
     "LD3 stream source decode"),
    ("clock_level", DP, "o_led_clock_locked = ctr_mclk_lock_w", "o_led_clock_locked = 1'b1",
     "LD3 clock-domain lock predicate"),
    ("clock_servo", DP, "(~follow_sel_r | mcsrv_locked_w)", "1'b1",
     "LD3 clock-domain lock predicate"),
    ("monitor_export", MONITOR, "media_locked_all_o = locked_sh_r", "media_locked_all_o = '0",
     "monitor exports every input lock"),
    ("monitor_wiring", DP, ".media_locked_all_o (avtprx_locked_all_w)", ".media_locked_all_o ()",
     "LD2 input reduction includes AAF and CRF"),
)


def build(directory: Path, streams: int, replacement: tuple[Path, Path] | None = None) -> Path:
    """Use the datapath source inventory, substituting one disposable plant."""
    directory.mkdir(parents=True, exist_ok=True)
    sources = subprocess.check_output(["make", "-s", "-C", str(HERE.parent / "milan_dp"),
                                       "print-srcs"], text=True).split()
    paths = [(HERE / source).resolve() for source in sources]
    if replacement:
        old, new = replacement
        if paths.count(old) != 1:
            raise ValueError("plant source absent or repeated in datapath inventory")
        paths = [new if path == old else path for path in paths]
    shape = "endstation_arty_split" if streams == 1 else "endstation_arty_4x4"
    header = (ROOT / "configs/generated" / shape / "gen/adp_shape_defaults.svh").read_text()
    outputs = int(re.search(r"ADP_TALKER_SRC_C\s*=\s*([0-9]+)", header)[1])
    includes = [ROOT / "configs/generated" / shape, ROOT / "hdl/common", ROOT / "hdl/common/csr",
                ROOT / "hdl/common/eth_event_counter", ROOT / "hdl/ieee17221/adp",
                ROOT / "hdl/ieee8021q/ts", ROOT / "hdl/ieee8021as/ptp_timestamp",
                ROOT / "third_party/verilog-axis/rtl"]
    command = [os.environ.get("VERILATOR", "verilator"), "--cc", "--exe", "--build", "-j", "4",
               "--public-ignore", "-Wno-fatal", "-Wno-PINMISSING", "--top-module", "led_datapath",
               f"-GN_STREAMS_P={streams}", "--Mdir", str(directory),
               "-CFLAGS", f"-std=c++17 -O2 -DSTREAMS_TB={streams} -DOUTPUTS_TB={outputs}",
               *["+incdir+" + str(path) for path in includes], *map(str, paths),
               str(ROOT / "hdl/usbnet/KL_status_led_truth.sv"), str(HERE / "led_datapath.sv"),
               str(HERE / "sim_datapath.cpp"), "-o", "Vled_datapath"]
    (directory / "command.json").write_text(json.dumps(command, indent=2) + "\n")
    with (directory / "build.log").open("w") as log:
        subprocess.run(command, cwd=HERE, stdout=log, stderr=subprocess.STDOUT, check=True)
    return directory / "Vled_datapath"


def run(directory: Path, streams: int, replacement: tuple[Path, Path] | None = None) -> subprocess.CompletedProcess:
    """Retain the executable's complete output separately from the build."""
    result = subprocess.run([str(build(directory, streams, replacement))], capture_output=True, text=True)
    (directory / "run.log").write_text(result.stdout + result.stderr)
    return result


def plants(directory: Path) -> bool:
    """Every mutation must reach its named assertion, not just fail to build."""
    passed = True
    for name, source, old, new, assertion in PLANTS:
        text = source.read_text()
        if text.count(old) != 1:
            raise ValueError("plant anchor absent or repeated: " + name)
        work = directory / name
        work.mkdir(parents=True, exist_ok=False)
        planted = work / source.name
        planted.write_text(text.replace(old, new))
        result = run(work / "native", 4, (source, planted))
        caught = result.returncode != 0 and any(
            line.startswith("FAIL ") and assertion in line for line in result.stdout.splitlines())
        print(("CAUGHT " if caught else "MISSED ") + name + ": " + assertion, flush=True)
        passed &= caught
    return passed


def main() -> int:
    """Run both supported geometries or the explicit mutation campaign."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--plants", action="store_true")
    args = parser.parse_args()
    directory = args.directory.resolve()
    if args.plants:
        return int(not plants(directory))
    for streams in (1, 4):
        result = run(directory / str(streams), streams)
        print(result.stdout, end="", flush=True)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
