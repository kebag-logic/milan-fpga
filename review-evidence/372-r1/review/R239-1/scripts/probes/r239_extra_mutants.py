#!/usr/bin/env python3
"""R239: extra scratch mutants of the REAL mux, beyond sva_campaign.py's rows.

Each targets a claimed property on the branch, port or width the campaign did
not use, is built through the suite's own `make mux-sva-build` recipe (via the
campaign's own build()), run on the real harness with the campaign's error
limit, and judged by the campaign's own detection() rule. The last row is an
expected NON-detection: a TKEEP forwarding defect the 8-bit stimulus cannot
see, recorded to measure the w8 shape's TKEEP reach, not claimed as a defect.

Scratch only: mutant sources and logs go under the probes directory.
"""
import sys
from pathlib import Path

SRC = Path("$VALIDATION_STORAGE/r239-372-r1-work/src")
OUT = Path("$VALIDATION_STORAGE/r239-372-r1-work/probes/extra_mutants")
VERILATOR = "$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator"
sys.path.insert(0, str(SRC / "tb/verilator/ptp_ts"))
import sva_campaign as camp  # noqa: E402  (read-only reuse of the campaign's rules)

MUTANTS = (
    # name, width, pattern, replacement, scenario, expected property ('' = expect NOT detected)
    ("grant_without_request_other_branch", 64,
     "end else begin\n          if (s0_tvalid)", "end else begin\n          if (1'b1)",
     "single_beats", "ap_grant_only_to_requester"),
    ("released_while_tlast_stalled_s1", 8,
     "if (s1_tvalid && s1_tlast && m_tready)", "if (s1_tvalid && s1_tlast)",
     "backpressure_last_beat", "u_m_dut.ap_tvalid_held_until_handshake"),
    ("tvalid_waits_for_tready_s1", 64,
     "m_tvalid = s1_tvalid;", "m_tvalid = s1_tvalid && m_tready;",
     "backpressure_mid_packet", "forwarding_laws.ai_tvalid_forwarded"),
    ("tdata_from_other_source_s0", 8,
     "m_tdata  = s0_tdata;", "m_tdata  = s1_tdata;",
     "multi_beats", "forwarding_laws.ai_payload_forwarded_on_transfer"),
    ("both_sources_ready_s1_owner", 64,
     "assign s0_tready = (state == STREAM_0) && m_tready;", "assign s0_tready = (state != IDLE) && m_tready;",
     "single_beats", "forwarding_laws.ai_grants_mutually_exclusive"),
    ("reset_to_owner", 8,
     "if (!rst_n)\n      state <= IDLE;", "if (!rst_n)\n      state <= STREAM_0;",
     "single_beats", "ap_reset_releases_owner"),
    ("tlast_hidden_while_stalled_s0_w64", 64,
     "m_tlast  = s0_tlast;", "m_tlast  = s0_tlast && m_tready;",
     "backpressure_last_beat", "u_m_dut.ap_tlast_stable_until_handshake"),
    ("tkeep_stuck_all_ones_s0_w8", 8,
     "m_tkeep  = s0_tkeep;", "m_tkeep  = '1;",
     "", ""),
)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    pristine = camp.DUT.read_text()
    rc = 0
    for name, width, pattern, replacement, scenario, expect in MUTANTS:
        row = OUT / name
        row.mkdir(parents=True, exist_ok=True)
        if pristine.count(pattern) != 1:
            print(f"[R239-FAIL] {name}: pattern occurs {pristine.count(pattern)} times")
            rc = 1
            continue
        scratch = row / camp.DUT.name
        scratch.write_text(pristine.replace(pattern, replacement))
        binary = camp.build(row, camp.Shape(width, scratch, camp.BIND, "--assert"), VERILATOR)
        if binary is None:
            print(f"[R239-FAIL] {name}-w{width}: did not build")
            rc = 1
            continue
        plus = [camp.ERROR_LIMIT] + ([f"+scenario={scenario}"] if scenario else [])
        status, text = camp.run_harness(binary, row / "run.log", plus)
        if expect:
            verdict = camp.detection(status, text, expect)
            tag = "R239-DETECTED" if verdict.ok else "R239-MISSED"
            rc |= 0 if verdict.ok else 1
            print(f"[{tag}] {name}-w{width} ({scenario}): {verdict.text}")
        else:
            fails = camp.fail_lines(text)
            print(f"[R239-INFO] {name}-w{width} (all scenarios): exit {status}; "
                  f"properties fired: {camp.fired(text) or 'none'}; harness failures: {len(fails)}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
