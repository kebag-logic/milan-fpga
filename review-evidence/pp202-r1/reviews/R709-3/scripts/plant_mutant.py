"""Plant one reviewer-owned mutant in a probe tree; every old text must occur exactly once.

usage: python3 -I plant_mutant.py <tree> <name>
"""
import sys
from pathlib import Path

TALKER = "hdl/acmp/KL_acmp_talker.sv"
SRP = "hdl/srp/KL_srp_talker_fsm.sv"

MUTANTS = {
    # a blocked search leaves sid_none_r set for every later grant
    "none_sticky": (TALKER,
        "        sid_cand_r <= sid_cur_r;\n        sid_none_r <= 1'b0;\n",
        "        sid_cand_r <= sid_cur_r;\n"),
    # the record holds the ID the source moves onto, not the one it leaves
    "record_holds_new_id": (TALKER,
        "sid_rec_r[ev_src_r]     <= sid_ovr_v_r[ev_src_r] ? sid_ovr_r[ev_src_r]\n"
        "                                                           : mv_cfg_w[15:0];",
        "sid_rec_r[ev_src_r]     <= sid_cand_r;"),
    # the quarantine epoch never ends: records never expire, the guard never releases
    "epoch_never_ticks": (TALKER,
        "assign sidq_tick_w = (now_ms_i - sidq_t0_r) >= SIDQ_MS_C;",
        "assign sidq_tick_w = 1'b0;"),
    # a txLA! walk of a parked source sends the new value's FirstValue
    "parked_txla_sends_new_value": (SRP,
        "    if (lvp_r[wsrc_r]) begin\n      wval_w[271:72]",
        "    if (lvp_r[wsrc_r] && !wtxla_r) begin\n      wval_w[271:72]"),
    # the re-open's Join! never follows the parked Leave
    "join_never_follows_leave": (SRP,
        "      end else if (lvj_r[s] && !lvp_r[s]) begin",
        "      end else if (1'b0) begin"),
}

def main() -> int:
    tree, name = Path(sys.argv[1]), sys.argv[2]
    path, old, new = MUTANTS[name]
    f = tree / path
    text = f.read_text()
    n = text.count(old)
    if n != 1:
        print(f"REFUSED {name}: old text occurs {n} times in {path}")
        return 2
    f.write_text(text.replace(old, new))
    print(f"PLANTED {name} in {path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
