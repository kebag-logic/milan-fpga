#!/usr/bin/env python3
"""R328-2 mutants of the round-2 parent-side map pulse (milan_datapath.sv).

Usage: r328_2_dp_mutants.py <repo-root> <scratch-dir> [mutant ...]

Each mutant is an exact-anchor textual edit of a COPY of
hdl/milan/milan_datapath.sv (or, for S*, of hdl/milan/KL_pp_shadow.sv),
substituted into the milan_dp source list. Two harness legs run, exactly as
reviewer_mutants.py runs them:
  static  = make run-base SIM_ARGS=--pending-only
  dynamic = make run-pending
A build failure is BUILD-FAIL, never a kill. Shipping sources are hashed
before and after; any change aborts.

Pulse mutants (P*) move amap_edit_live_wr_p away from the write condition.
Equivalence controls (E*) are edits the author's claims say are behaviour-
preserving; they are expected to SURVIVE, and a kill would refute the claim.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

DP = "hdl/milan/milan_datapath.sv"
SH = "hdl/milan/KL_pp_shadow.sv"

LIVE = ("  assign amap_edit_live_wr_p = axis_resetn && amap_edit_beat_w\n"
        "      && (pp_amap_edit_phase_w == 3'd5) && amap_edit_context_w\n"
        "      && (amap_edit_in_change_w || amap_edit_out_change_w);")
ELSEIF = "            end else if (amap_edit_context_w && amap_edit_out_change_w) begin"
SH_LIVE = ("  assign aecp_live_wr_w = aecp_name_wr_w\n"
           "                        | amap_live_wr_i;")


def live(expr):
    return (DP, LIVE, f"  assign amap_edit_live_wr_p = {expr};")


MUTANTS = {
    # pulse diverges from the write
    "P1_in_only": live("axis_resetn && amap_edit_beat_w && (pp_amap_edit_phase_w == 3'd5)"
                       " && amap_edit_context_w && amap_edit_in_change_w"),
    "P2_out_only": live("axis_resetn && amap_edit_beat_w && (pp_amap_edit_phase_w == 3'd5)"
                        " && amap_edit_context_w && amap_edit_out_change_w"),
    "P3_unqualified": live("axis_resetn && amap_edit_beat_w && (pp_amap_edit_phase_w == 3'd5)"
                           " && amap_edit_context_w"),
    "P4_no_phase5": live("axis_resetn && amap_edit_beat_w && amap_edit_context_w"
                         " && (amap_edit_in_change_w || amap_edit_out_change_w)"),
    "P5_no_context": live("axis_resetn && amap_edit_beat_w && (pp_amap_edit_phase_w == 3'd5)"
                          " && (amap_edit_in_change_w || amap_edit_out_change_w)"),
    "P6_tied_low": live("1'b0"),
    # behaviour-preserving per the author's claims (expected to survive)
    "E1_no_beat": live("axis_resetn && (pp_amap_edit_phase_w == 3'd5) && amap_edit_context_w"
                       " && (amap_edit_in_change_w || amap_edit_out_change_w)"),
    "E2_priority_dropped": (DP, ELSEIF,
                            "            end\n"
                            "            if (amap_edit_context_w && amap_edit_out_change_w) begin"),
    # shadow ignores the new input: map group drops out entirely
    "S1_shadow_ignores_input": (SH, SH_LIVE,
                                "  assign aecp_live_wr_w = aecp_name_wr_w\n"
                                "                        | 1'b0;"),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verdict(rc, text):
    if "RESULT: PASS" in text and rc == 0:
        return "SURVIVED"
    if "RESULT: FAIL" in text:
        return "KILLED"
    return "BUILD-FAIL"


def main():
    root = Path(sys.argv[1]).resolve()
    scratch = Path(sys.argv[2]).resolve()
    names = sys.argv[3:] or list(MUTANTS)
    here = root / "tb/verilator/pp_shadow"
    files = {rel: root / rel for rel in (DP, SH)}
    before = {rel: sha(p) for rel, p in files.items()}
    text = {rel: p.read_text() for rel, p in files.items()}
    listing = subprocess.run(["make", "-s", "-C", "../milan_dp", "print-srcs"], cwd=here,
                             check=True, capture_output=True, text=True).stdout.split()
    sources = [(here / p).resolve() for p in listing]
    for rel, p in files.items():
        assert sources.count(p) == 1, f"expected exactly one {rel}"
        print(f"shipping {rel} sha256 {before[rel]}")
    for name in names:
        rel, old, new = MUTANTS[name]
        if text[rel].count(old) != 1:
            print(f"{name}: REFUSED anchor count {text[rel].count(old)}")
            continue
        mdir = scratch / "mut" / name
        mutant = mdir / rel
        mutant.parent.mkdir(parents=True, exist_ok=True)
        mutant.write_text(text[rel].replace(old, new))
        srcs = " ".join(str(mutant if p == files[rel] else p) for p in sources)
        results = []
        for leg, cmd in (
            ("static", ["make", "run-base", f"BUILD_DIR={mdir}/obj_static",
                        "SIM_ARGS=--pending-only", f"DP_SRCS={srcs}"]),
            ("dynamic", ["make", "run-pending", f"PENDING_BUILD_DIR={mdir}/obj_dyn",
                         f"DP_SRCS={srcs}"]),
        ):
            log = mdir / f"{leg}.log"
            with log.open("w") as fh:
                rc = subprocess.run(cmd, cwd=here, stdout=fh,
                                    stderr=subprocess.STDOUT).returncode
            out = log.read_text(errors="replace")
            fails = sorted({l.split("got=")[0].strip() for l in out.splitlines() if "[FAIL]" in l})
            results.append(f"{leg}={verdict(rc, out)}({len(fails)} fails)")
            (scratch / "mut" / f"{name}.{leg}.fails.txt").write_text("\n".join(fails) + "\n")
        print(f"{name}: " + " ".join(results), flush=True)
        for rel, p in files.items():
            if sha(p) != before[rel]:
                sys.exit(f"ABORT: shipping {rel} changed")
    for rel, p in files.items():
        print(f"shipping {rel} sha256 after {sha(p)}")


if __name__ == "__main__":
    main()
