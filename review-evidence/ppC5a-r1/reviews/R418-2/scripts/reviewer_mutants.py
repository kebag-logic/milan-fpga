#!/usr/bin/env python3
"""Reviewer-designed arms on the round-2 RTL and harness, applied to a SCRATCH tree only.

Each arm is a literal text replacement (asserted to match exactly once) in a copy of
the exact-head export. A control of each section runs first and must pass. An arm is
KILLED when its section completed (a tally was printed), exited non-zero and printed
at least one FAIL line starting with one of the expected prefixes.
Usage: reviewer_mutants.py <pristine export> <scratch tree> <out dir> [arm,arm,...]
"""
import shutil
import subprocess
import sys
from pathlib import Path

ENG = "hdl/aecp/KL_aecp_engine.sv"
TOP = "hdl/top/protocol_processor_top.sv"
WRAP = "tb/pp_top/pp_top_wrap.sv"

ALLOC_ECHO = """            //! Milan v1.2 §5.4.3.3 Table 5.19: an MVU status is SUCCESS or
            //! NOT_IMPLEMENTED, so a voided MVU answer, like that of every
            //! other message type but AEM's, is its refusal form, the
            //! command echoed, as the deadline's is (A_RUN, `st_echo_w`)
            if (st_echo_w) begin
              status_r    <= ST_NOT_IMPLEMENTED_C;
              echo_r      <= 1'b1;
              pld_r       <= pld_cmd_r;
              frame_len_r <= echo_len_w;
            end
"""
WR_ECHO = """            //! the command echoed, as at A_ALLOC; its slot was sized for the
            //! echo (txs_oversize_o)
            if (st_echo_w) begin
              status_r    <= ST_NOT_IMPLEMENTED_C;
              echo_r      <= 1'b1;
              pld_r       <= pld_cmd_r;
              frame_len_r <= echo_len_w;
            end
"""

# arm: (section, [(file, old, new, count)], [expected FAIL prefixes], what it breaks)
ARMS = {
    "r-fault-echo-alloc-removed": ("deadline", [(ENG, ALLOC_ECHO, "", 1)],
        ["DL8"], "the A_ALLOC fault rebuild loses the non-AEM echo (A_WR keeps it)"),
    "r-fault-echo-wr-removed": ("deadline", [(ENG, WR_ECHO, "", 1)],
        ["DL8"], "the A_WR fault rebuild loses the non-AEM echo (A_ALLOC keeps it)"),
    "r-fault-echo-len-60": ("deadline",
        [(ENG, "              pld_r       <= pld_cmd_r;\n              frame_len_r <= echo_len_w;\n",
          "              pld_r       <= pld_cmd_r;\n", 2)],
        ["DL8 a read error under a 540-byte command"],
        "both fault rebuilds keep the 60-byte header length, truncating a long echo"),
    "r-st-echo-bucket-only": ("deadline",
        [(ENG, "assign st_echo_w = !((cmd_r.protocol == PP_PROTO_AEM)\n                       && (cmd_r.msg_type == 4'd0));",
          "assign st_echo_w = (cmd_r.protocol != PP_PROTO_AEM);", 1)],
        ["DL9 AVC past its deadline", "DL9 HDCP_APM past its deadline",
         "DL9 EXTENDED past its deadline"],
        "the echo guard reads the validator bucket only, so AVC/HDCP/EXTENDED in the AEM bucket get status 10"),
    "r-registry-and-lock-preempted": ("deadline",
        [(ENG, "&& !regun_r && !lockc_r && !amap_edit_r;", "&& !amap_edit_r;", 1)],
        ["DL10"], "both registry-face exemptions removed together"),
    "r-kill-not-gated-by-owner": ("deadline",
        [(TOP, "assign aecp_dl_kill_w = aecp_sb_active_r && !aecp_sb_done_pending_r\n                        && !aecp_dl_past_w[31];",
          "assign aecp_dl_kill_w = !aecp_sb_done_pending_r\n                        && !aecp_dl_past_w[31];", 1)],
        ["DL"], "the kill stays raised after the AECP hold has ended (stale id and deadline)"),
    "r-hz-key-index-dropped": ("hazards",
        [(TOP, "    return {ty[5:0], ix[9:0]};", "    return {ty[5:0], 10'h000};", 1)],
        ["HZ9b", "HZ9e", "HZ10d", "HZ12"], "every key loses its index, so streams alias"),
    "r-acmp-key-uid-dropped": ("hazards",
        [(TOP, "hz_key(HZ_DT_STREAM_OUT_C, hdr_operands_r[15:0])", "hz_key(HZ_DT_STREAM_OUT_C, 16'd0)", 1),
         (TOP, "hz_key(HZ_DT_STREAM_IN_C, hdr_operands_r[15:0])", "hz_key(HZ_DT_STREAM_IN_C, 16'd0)", 1)],
        ["HZ9b", "HZ9e", "HZ10d"], "ACMP keys lose the unique_id, so every source/sink aliases stream 0"),
    "r-name-keyed-as-output": ("hazards",
        [(TOP, "hz_class_w = 4'(PP_HZ_NAME_WR);\n          hz_key_w   = hz_dkey_w;",
          "hz_class_w = 4'(PP_HZ_NAME_WR);\n          hz_key_w   = hz_key(HZ_DT_STREAM_OUT_C, hdr_operands_r[47:32]);", 1)],
        ["HZ9a", "HZ9f"], "SET_NAME keyed as STREAM_OUTPUT of its index whatever it names"),
    "r-wrap-refused-tap-zero": ("hazards",
        [(WRAP, "assign dbg_sb_ref_aecp_o    = u_dut.sb_pick_aecp_w && !u_dut.sb_gnt_w;",
          "assign dbg_sb_ref_aecp_o    = 1'b0;", 1),
         (WRAP, "assign dbg_sb_ref_acmp_o    = u_dut.sb_pick_acmp_w && !u_dut.sb_gnt_w;",
          "assign dbg_sb_ref_acmp_o    = 1'b0;", 1)],
        ["HZ4", "HZ5", "HZ9a", "HZ9d", "HZ10", "HZ11", "HZ12"],
        "harness: the new refused taps blinded, so every 'waits' check loses its refusal evidence"),
}


def sh(cmd, cwd, log):
    with open(log, "w") as f:
        return subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT).returncode


def restore(src: Path, tree: Path):
    for rel in ("hdl", "tb/pp_top/pp_top_wrap.sv"):
        s, d = src / rel, tree / rel
        if s.is_dir():
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)


def section(tree: Path, sec: str, log: Path):
    rc = sh(["make", "-C", "tb/pp_top", "gsi-build"], tree, log.with_suffix(".build.log"))
    if rc != 0:
        return rc, "", False
    rc = sh(["./obj_dir/Vpp_top_sim", f"--{sec}-only"], tree / "tb/pp_top", log)
    text = log.read_text()
    return rc, text, ("checks" in text)


def main():
    src, tree, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    sel = sys.argv[4].split(",") if len(sys.argv) > 4 else list(ARMS)
    out.mkdir(parents=True, exist_ok=True)
    if not tree.exists():
        shutil.copytree(src, tree)
    ok_all = True
    for sec in sorted({ARMS[a][0] for a in sel}):
        restore(src, tree)
        rc, text, done = section(tree, sec, out / f"control-{sec}.log")
        fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
        good = rc == 0 and done and not fails
        ok_all &= good
        print(f"control {sec}: rc={rc} failures={len(fails)} {'PASS' if good else 'FAIL'}", flush=True)
    for arm in sel:
        sec, edits, expect, what = ARMS[arm]
        restore(src, tree)
        for rel, old, new, n in edits:
            p = tree / rel
            s = p.read_text()
            assert s.count(old) == n, (arm, rel, s.count(old))
            p.write_text(s.replace(old, new))
        rc, text, done = section(tree, sec, out / f"{arm}.log")
        fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
        named = [l for l in fails if any(l[5:].strip().startswith(e) for e in expect)]
        killed = rc != 0 and done and bool(named)
        ok_all &= killed
        print(f"{arm} [{sec}] ({what}): rc={rc} failures={len(fails)} named={len(named)} "
              f"{'KILLED' if killed else 'SURVIVED' if done else 'NO-TALLY'}", flush=True)
        for l in fails[:12]:
            print(f"    {l[:200]}", flush=True)
        if len(fails) > 12:
            print(f"    ... {len(fails) - 12} more", flush=True)
    restore(src, tree)
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
