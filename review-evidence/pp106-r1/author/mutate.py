#!/usr/bin/env python3
"""Plant one mutation at a time in KL_srp_encoder.sv, run the srp_encoder
suite, record the tally and the failing checks, restore, verify the restore.

M0 is the base encoder (main fbc1f715) run against the new suite."""
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

LANE = Path("$LANES/pp106-leaveall-scope")
RTL = LANE / "hdl/srp/KL_srp_encoder.sv"
TB = LANE / "tb/srp_encoder"
OUT = Path("$REVIEWS/pp106-a206-packet/mutations")
ENV = dict(os.environ,
           PATH="$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin:" + os.environ["PATH"])

MUTATIONS = {
    "M5": ("P1 every registered type flagged on its first vector: "
           "LeaveAllEvent back on the PDU's first vector only",
           [("  assign la3_w      = (la_act_r && ((la_types_w & la_bit_w & ~la_seen_r) != '0))",
             "  assign la3_w      = (la_act_r && (la_seen_r == 4'b0000))")]),
    "M6": ("P2 a LeaveAll-only vector for each type not declared: no append",
           [("  assign la_need_w  = la_act_r ? (la_types_w & ~la_seen_r) : 4'b0000;",
             "  assign la_need_w  = 4'b0000;")]),
    "M7": ("P3 the LeaveAll-only vector is NumberOfValues 0: written as 1",
           [("  assign nov_w    = 13'(run_len_r);",
             "  assign nov_w    = (run_len_r == '0) ? 13'd1 : 13'(run_len_r);")]),
    "M7b": ("P3 the LeaveAll-only FirstValue is zero: written all-ones",
            [("              run_first_r <= '0;\n              run_last_r  <= '0;",
              "              run_first_r <= '1;\n              run_last_r  <= '0;")]),
    "M8": ("P4 nothing added when every type is declared: declared types "
           "are never marked seen (always-append encoder)",
           [("            la_seen_r <= la_seen_r | la_bit_w;",
             "            if (run_len_r == '0) la_seen_r <= la_seen_r | la_bit_w;")]),
    "M9": ("P5 MVRP LeaveAll unchanged: MVRP type set emptied",
           [("  localparam logic [3:0]  LA_TYPES_MVRP_C    = 4'b0001;",
             "  localparam logic [3:0]  LA_TYPES_MVRP_C    = 4'b0000;")]),
    "M10": ("P6 a LeaveAll requested mid-drain goes whole to the next MRPDU: "
            "consumed at commit again (the base encoder's point)",
            [("            if (start0_w) la_pend_r[0] <= 1'b0;\n"
              "            else          la_pend_r[1] <= 1'b0;\n", ""),
             ("          else                         cnt_mvrp_r <= '0;\n"
              "          st_r <= E_TXREQ;",
              "          else                         cnt_mvrp_r <= '0;\n"
              "          la_pend_r[cur_app_r] <= 1'b0;\n"
              "          st_r <= E_TXREQ;")]),
    "M11": ("P7 a start-cycle LeaveAll is taken once: latch no longer gated",
            [("      if (leaveall_i[0] && !start0_w) la_pend_r[0] <= 1'b1;",
              "      if (leaveall_i[0]) la_pend_r[0] <= 1'b1;")]),
    "M12": ("P7 a start-cycle LeaveAll is taken by that drain: snapshot "
            "ignores the same-cycle request",
            [("            la_act_r <= start0_w ? (la_pend_r[0] || leaveall_i[0])",
              "            la_act_r <= start0_w ? (la_pend_r[0])")]),
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_suite(tag: str) -> str:
    log = OUT / f"{tag}.log"
    with log.open("w") as fh:
        subprocess.run(["make", "clean"], cwd=TB, env=ENV, stdout=subprocess.DEVNULL)
        try:
            rc = subprocess.run(["timeout", "600", "make"], cwd=TB, env=ENV,
                                stdout=fh, stderr=subprocess.STDOUT).returncode
        except Exception as exc:  # noqa: BLE001
            rc = f"exception {exc}"
    text = log.read_text(errors="replace")
    tally = re.findall(r"\d+ checks: \d+ PASS, \d+ FAIL", text)
    fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
    return (f"rc={rc} tally={tally[-1] if tally else 'NONE'} "
            f"fail_lines={len(fails)}\n" + "\n".join("    " + l for l in fails[:14]))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    orig = RTL.read_bytes()
    orig_sha = sha(RTL)
    summary = [f"restored-file sha256 must equal {orig_sha}"]
    only = sys.argv[1:]
    try:
        if not only or "M0" in only:
            base = subprocess.run(["git", "show", "fbc1f71:hdl/srp/KL_srp_encoder.sv"],
                                  cwd=LANE, capture_output=True, check=True).stdout
            RTL.write_bytes(base)
            summary.append("== M0 base encoder (main fbc1f715) against the new suite\n"
                           + run_suite("M0"))
            RTL.write_bytes(orig)
        for tag, (what, reps) in MUTATIONS.items():
            if only and tag not in only:
                continue
            s = orig.decode()
            for a, b in reps:
                assert s.count(a) == 1, (tag, a)
                s = s.replace(a, b)
            RTL.write_text(s)
            summary.append(f"== {tag} {what}\n" + run_suite(tag))
            RTL.write_bytes(orig)
    finally:
        RTL.write_bytes(orig)
    summary.append(f"restored sha256 {sha(RTL)} "
                   f"{'OK' if sha(RTL) == orig_sha else 'MISMATCH'}")
    text = "\n".join(summary)
    (OUT / "SUMMARY.txt").write_text(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
