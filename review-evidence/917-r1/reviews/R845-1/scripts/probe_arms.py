#!/usr/bin/env python3
"""Reviewer probe arms for #917 (KL_mbx_rx held frame): each plants one defect in a scratch copy
through the repository's own mutants.py machinery and reports every failing check, or ESCAPED.
Usage: python3 -I probe_arms.py <clone> <scratch-root> [arm-name ...]"""
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
root = Path(sys.argv[2]).resolve()
only = set(sys.argv[3:])
sys.path.insert(0, str(clone / "tb/verilator/mbx"))
import mutants as M  # noqa: E402

PROBES = (
    # documented: a frame held when its channel closes is still committed
    M.Arm("probe-release-gated-on-open", "KL_mbx_rx.sv",
          "      rel_w[c]    = refill_w[c] && held_r[c];",
          "      rel_w[c]    = refill_w[c] && held_r[c] && open_i[c];", 0, "?"),
    # a filter-refused frame behind a held one counted in RATE_DROP
    M.Arm("probe-refused-behind-held-counted", "KL_mbx_rx.sv",
          "vd_rate_r <= hit_r && rule_pass_w && !bad_w && (tokens_r[ch_r] == 8'd0) && held_r[ch_r];",
          "vd_rate_r <= hit_r && !bad_w && (tokens_r[ch_r] == 8'd0) && held_r[ch_r];", 0, "?"),
    # the held record's commit spends no token
    M.Arm("probe-release-spends-no-token", "KL_mbx_rx.sv",
          "if ((commit_w && ch_r == MBX_CH_W_C'(c)) || rel_w[c]) tokens = tokens - 9'd1;",
          "if (commit_w && ch_r == MBX_CH_W_C'(c)) tokens = tokens - 9'd1;", 0, "?"),
    # the held record's commit is not counted in RX_PASS
    M.Arm("probe-release-not-counted", "KL_mbx_rx.sv",
          "          head_r[c] <= wr_head_r[c];\n          pass_r[c] <= pass_r[c] + 16'd1;",
          "          head_r[c] <= wr_head_r[c];", 0, "?"),
    # held flag never cleared by the release
    M.Arm("probe-held-never-cleared", "KL_mbx_rx.sv",
          "        else if (rel_w[c]) held_r[c] <= 1'b0;", "", 0, "?"),
    # the held record does not move the write head
    M.Arm("probe-hold-leaves-write-head", "KL_mbx_rx.sv",
          "if ((commit_w || hold_w) && ch_r == MBX_CH_W_C'(c)) wr_head_r[c]",
          "if (commit_w && ch_r == MBX_CH_W_C'(c)) wr_head_r[c]", 0, "?"),
    # header words of a held record written at RX_HEAD, not the write head
    M.Arm("probe-header-at-head", "KL_mbx_rx.sv",
          "waddr_w = MBX_RING_AW_C'((wr_head_r[ch_r] + 16'd1) & (ring_words_w - 16'd1));",
          "waddr_w = MBX_RING_AW_C'((head_r[ch_r] + 16'd1) & (ring_words_w - 16'd1));", 0, "?"),
    # the verdict ignores the refill: a frame stored on an empty bucket with a refill at HDR1 held anyway (AXI)
    M.Arm("probe-refill-missed-axil", "KL_mbx_rx.sv",
          "assign tok_now_w   = (tokens_r[ch_r] != 8'd0) || refill_w[ch_r];",
          "assign tok_now_w   = (tokens_r[ch_r] != 8'd0) || (refill_w[ch_r] && st_r != HDR1_S);", 1, "?"),
    # free-space guard reads the committed head only (the pre-#917 space)
    M.Arm("probe-space-from-committed-head", "KL_mbx_rx.sv",
          "    used_w       = wr_head_r[ch_r] - tail_w;", "    used_w       = head_r[ch_r] - tail_w;", 0, "?"),
)

def main():
    root.mkdir(parents=True, exist_ok=True)
    for arm in PROBES:
        if only and arm.name not in only:
            continue
        rc, log = M.build_and_run(M.plant(arm, root), root / arm.name, arm.host, arm.ifs)
        fails = [ln.strip() for ln in log.splitlines() if "[FAIL]" in ln]
        tally = [ln for ln in log.splitlines() if "checks:" in ln]
        state = "CAUGHT" if rc == 1 and fails else ("ESCAPED" if rc == 0 else f"rc={rc}")
        print(f"[{state}] {arm.name} host={arm.host}: {len(fails)} failing; {tally[-1] if tally else ''}")
        for ln in fails[:8]:
            print("    " + ln)
        sys.stdout.flush()

main()
