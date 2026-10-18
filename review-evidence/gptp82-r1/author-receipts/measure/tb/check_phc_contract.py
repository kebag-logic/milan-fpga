# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Pin the engine PHC boundary and the egress result face.

The PHC half records the removal of the unused ns input. The result half
records FPGA-gPTP #31: the egress return is a valid/ready face carrying an
outcome and a generation beside the timestamp, and the transmit admission
credit is an engine input. A caller that drops one of those ports, or an
engine that goes back to taking a result without an accepted beat, is named
here by file and token instead of being found later by a wrong exchange.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN = {
    "hdl/top/KL_gptp_engine.sv": ("phc_ns_i", "disp_ts1_r", ".disp_ts1_i"),
    "hdl/ucpu/KL_gptp_ucpu.sv": ("disp_ts1_i", "S_PRE0"),
    "hdl/ucode/gen_gptp_ucode.py": ("RTS1",),
    "bench/arty/bench_arty_top.sv": (".phc_ns_i",),
    "tb/verilator/engine/sim_main.cpp": ("phc_ns_i",),
    "tb/verilator/ucpu/sim_main.cpp": ("disp_ts1_i",),
}

REQUIRED = {
    "hdl/top/KL_gptp_engine.sv": (
        "rx_ts_i",
        "txts_ns_i",
        "phc_addend_we_o",
        "phc_step_we_o",
        "phc_slew_active_o",
        "gx_data_r <= {32'd0, ms_now_w};",
        # the accepted-beat result face and the admission credit (#31)
        "txts_ready_o",
        "txts_ok_i",
        "txts_gen_i",
        "tx_credit_i",
        "txts_accept_w = txts_valid_i && txts_ready_o",
        "if (txts_accept_w) begin",
    ),
    "bench/arty/bench_arty_top.sv": (
        "rxts_r <= phc_ns_w;",
        "txts_r <= phc_ns_w;",
        ".rx_ts_i",
        ".txts_ns_i",
        ".phc_addend_we_o",
        ".phc_step_we_o",
        ".phc_slew_active_o",
        ".txts_ready_o",
        ".txts_ok_i",
        ".txts_gen_i",
        ".tx_credit_i",
    ),
    "hdl/ucode/gen_gptp_ucode.py": (
        # the lost arm, the retained pair and the three gated legs
        "TXT_OK_C",
        "S_T1V",
        "S_PDWAIT",
        "e_credit_gate(p, \"skip\")",
        "e_credit_gate(p, \"beat_off\")",
    ),
}


def main() -> int:
    """The gate: 0 when no removed token has come back and every surviving
    path is still wired, 1 with the file and the token named."""
    failures = []
    for relpath, needles in FORBIDDEN.items():
        text = (ROOT / relpath).read_text(encoding="utf-8")
        failures.extend(
            f"{relpath}: removed token is present: {needle}"
            for needle in needles
            if needle in text
        )

    for relpath, needles in REQUIRED.items():
        text = (ROOT / relpath).read_text(encoding="utf-8")
        failures.extend(
            f"{relpath}: required surviving path is missing: {needle}"
            for needle in needles
            if needle not in text
        )

    if failures:
        print("PHC interface contract: FAIL")
        for failure in failures:
            print(f"  {failure}")
        return 1

    print("PHC interface contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
