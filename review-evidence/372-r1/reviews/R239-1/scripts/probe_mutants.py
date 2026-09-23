#!/usr/bin/env python3
"""Reviewer disposable probes for #372 (R239-1). Portable: paths come from arguments.

Two families, both run in a DISPOSABLE scratch copy of the exact head (never in a
review clone):

  dut     independent DUT mutants NOT in sva_campaign.py. Each is a scratch copy of
          hdl/common/axis_mux_rr_2in_1out.sv with one exactly-once span rewritten, built
          through the suite's own `make mux-sva-build` recipe, then run over ALL
          scenarios twice: at the default error limit (the suite's own mode) and with
          +verilator+error+limit+1000 (to list every property failing at the first
          failing edge). Pass = the default run exits non-zero; the fired list is recorded.

  weaken  checker-weakening probes. One property of the checker in the scratch tree is
          weakened in place, the clean binaries are rebuilt with `make mux-sva` (the
          positive leg), and the campaign rows written for that property are run with
          `sva_campaign.py --only`. The file is restored byte-for-byte afterwards.
          A full weakening (consequent -> 1'b1) must make its campaign row(s) FAIL;
          a partial weakening documents what the campaign can and cannot distinguish.

Usage: probe_mutants.py <scratch-tree> <verilator> <out-dir> [dut|weaken|all] [weaken-name-prefix]
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

FIRED = re.compile(r"Assertion failed in ([\w.$]+):")

DUT_MUTANTS = [
    # name, width, pattern, replacement, what a correct checker/scoreboard should say
    ("wrong_tlast_source_s0", 64, "m_tlast  = s0_tlast;", "m_tlast  = s1_tlast;",
     "STREAM_0 forwards s1's TLAST"),
    ("wrong_tdata_source_s1", 8, "m_tdata  = s1_tdata;", "m_tdata  = s0_tdata;",
     "STREAM_1 forwards s0's TDATA"),
    ("tvalid_from_other_source", 64, "m_tvalid = s1_tvalid;", "m_tvalid = s0_tvalid;",
     "STREAM_1 forwards s0's TVALID"),
    ("grant_s1_when_s0_offers", 8,
     "end else begin\n          if (s0_tvalid)\n            next_state = STREAM_0;",
     "end else begin\n          if (s0_tvalid)\n            next_state = STREAM_1;",
     "after s1 was served, an s0 offer grants s1"),
    ("s1_release_ignores_sink", 8, "if (s1_tvalid && s1_tlast && m_tready)", "if (s1_tvalid && s1_tlast)",
     "s1 gives up the output on a stalled TLAST beat (s1 twin of a campaign row)"),
    ("last_served_frozen", 64,
     "else if ((s0_tready && s0_tvalid && s0_tlast) || (s1_tready && s1_tvalid && s1_tlast))",
     "else if (1'b0)", "round-robin memory never updates (no property claims fairness)"),
    ("reset_to_stream0", 8, "if (!rst_n)\n      state <= IDLE;", "if (!rst_n)\n      state <= STREAM_0;",
     "reset makes s0 the owner"),
    ("s0_never_released", 64, "if (s0_tvalid && s0_tlast && m_tready)", "if (1'b0)",
     "s0 never gives the output back"),
    ("tdata_bit0_flip_s0", 64, "m_tdata  = s0_tdata;", "m_tdata  = s0_tdata ^ TDATA_WIDTH'(1);",
     "one TDATA bit corrupted on the s0 path"),
    ("s0_ready_in_idle", 8, "assign s0_tready = (state == STREAM_0) && m_tready;",
     "assign s0_tready = (state != STREAM_1) && m_tready;", "s0 sees TREADY while nobody owns the output"),
    ("s1_ready_waits_for_valid", 64, "assign s1_tready = (state == STREAM_1) && m_tready;",
     "assign s1_tready = (state == STREAM_1) && m_tready && s1_tvalid;",
     "AXI-legal (TREADY may depend on TVALID) but breaks the mux's own exact-ready law"),
    ("m_tvalid_in_idle", 8, "m_tvalid = 1'b0;", "m_tvalid = s0_tvalid;", "IDLE forwards s0's TVALID"),
    ("tkeep_zero_on_last_s1", 64, "m_tkeep  = s1_tkeep;", "m_tkeep  = s1_tlast ? '0 : s1_tkeep;",
     "s1's TLAST beat leaves with TKEEP zero"),
]

SRC = "tb/common/sva/axis_stream_source_sva.sv"
MUX = "tb/common/sva/axis_mux_rr_2in_1out_sva.sv"
WEAKEN = [
    # name, file, [(pattern, replacement)], campaign --only prefixes, expectation
    ("state_legal_true", MUX, [("$onehot({owner_none_i, owner_s0_i, owner_s1_i}))", "1'b1)")],
     ["mutant-illegal_state_reached"], "row-fails"),
    ("tdata_stable_true", SRC, [("stalled_w |=> $stable(tdata_i))", "stalled_w |=> 1'b1)")],
     ["stimulus-s0_flip_tdata-w8", "stimulus-s1_flip_tdata-w64", "mutant-tdata_hidden_while_stalled"], "row-fails"),
    ("tkeep_stable_true", SRC, [("stalled_w |=> $stable(tkeep_i))", "stalled_w |=> 1'b1)")],
     ["stimulus-s0_flip_tkeep-w64", "mutant-tkeep_hidden_while_stalled"], "row-fails"),
    ("tlast_stable_true", SRC, [("stalled_w |=> $stable(tlast_i))", "stalled_w |=> 1'b1)")],
     ["stimulus-s1_flip_tlast-w8", "mutant-tlast_hidden_while_stalled"], "row-fails"),
    ("tvalid_held_true", SRC, [("stalled_w |=> tvalid_i)", "stalled_w |=> 1'b1)")],
     ["stimulus-s1_drop_tvalid-w8", "mutant-released_while_tlast_stalled"], "row-fails"),
    ("reset_releases_true", MUX, [("!rst_n |=> owner_none_i)", "!rst_n |=> 1'b1)")],
     ["mutant-reset_ignored"], "row-fails"),
    ("released_after_tlast_true", MUX, [("owner_last_handshake_w |=> owner_none_i)", "owner_last_handshake_w |=> 1'b1)")],
     ["mutant-kept_after_tlast"], "row-fails"),
    ("owner_held_true", MUX, [("|=> $stable({owner_s0_i, owner_s1_i}))", "|=> 1'b1)")],
     ["mutant-released_before_tlast"], "row-fails"),
    ("grant_only_true", MUX,
     [("owner_none_i |=> (!owner_s0_i || $past(s0_tvalid_i)) && (!owner_s1_i || $past(s1_tvalid_i)))",
       "owner_none_i |=> 1'b1)")], ["mutant-granted_without_request"], "row-fails"),
    ("mutex_true", MUX, [("assert final (!(s0_tready_i && s1_tready_i))", "assert final (1'b1)")],
     ["mutant-both_sources_ready"], "row-fails"),
    ("ready_only_true", MUX,
     [("s0_tready_i == (owner_s0_i && m_tready_i) && s1_tready_i == (owner_s1_i && m_tready_i))", "1'b1)")],
     ["mutant-ready_ignores_sink"], "row-fails"),
    ("tvalid_forwarded_true", MUX,
     [("m_tvalid_i == ((owner_s0_i && s0_tvalid_i) || (owner_s1_i && s1_tvalid_i)))", "1'b1)")],
     ["mutant-tvalid_waits_for_tready"], "row-fails"),
    ("payload_no_tkeep", MUX,
     [("m_tdata_i == s0_tdata_i && m_tkeep_i == s0_tkeep_i && m_tlast_i == s0_tlast_i",
       "m_tdata_i == s0_tdata_i && m_tlast_i == s0_tlast_i"),
      ("m_tdata_i == s1_tdata_i && m_tkeep_i == s1_tkeep_i", "m_tdata_i == s1_tdata_i")],
     ["mutant-tkeep_from_other_source"], "row-fails"),
    # partial weakenings: the campaign is not claimed to prove completeness
    ("tdata_stable_bit0_only", SRC, [("stalled_w |=> $stable(tdata_i))", "stalled_w |=> $stable(tdata_i[0]))")],
     ["stimulus-s0_flip_tdata", "stimulus-s1_flip_tdata", "mutant-tdata_hidden_while_stalled"], "informative"),
    ("payload_no_tdata", MUX,
     [("m_tdata_i == s0_tdata_i && m_tkeep_i == s0_tkeep_i", "m_tkeep_i == s0_tkeep_i"),
      ("owner_s1_i && m_tdata_i == s1_tdata_i && m_tkeep_i", "owner_s1_i && m_tkeep_i")],
     ["mutant-tkeep_from_other_source"], "informative"),
    # v2: the first spelling of these four left the signal unused, so -Wall refused the
    # build (UNUSEDSIGNAL) before any detection ran; these tautologies keep it referenced.
    ("v2_tdata_stable_true", SRC, [("stalled_w |=> $stable(tdata_i))",
                                    "stalled_w |=> ($stable(tdata_i) || !$stable(tdata_i)))")],
     ["stimulus-s0_flip_tdata-w8", "stimulus-s1_flip_tdata-w64", "mutant-tdata_hidden_while_stalled"], "row-fails"),
    ("v2_tkeep_stable_true", SRC, [("stalled_w |=> $stable(tkeep_i))",
                                    "stalled_w |=> ($stable(tkeep_i) || !$stable(tkeep_i)))")],
     ["stimulus-s0_flip_tkeep-w64", "mutant-tkeep_hidden_while_stalled"], "row-fails"),
    ("v2_tlast_stable_true", SRC, [("stalled_w |=> $stable(tlast_i))",
                                    "stalled_w |=> ($stable(tlast_i) || !$stable(tlast_i)))")],
     ["stimulus-s1_flip_tlast-w8", "mutant-tlast_hidden_while_stalled"], "row-fails"),
    ("v2_tdata_stable_bit0_only", SRC, [("stalled_w |=> $stable(tdata_i))",
                                         "stalled_w |=> $stable(tdata_i & TDATA_WIDTH_P'(1)))")],
     ["stimulus-s0_flip_tdata", "stimulus-s1_flip_tdata", "mutant-tdata_hidden_while_stalled"], "informative"),
    ("grant_only_s1_half_dropped", MUX,
     [("owner_none_i |=> (!owner_s0_i || $past(s0_tvalid_i)) && (!owner_s1_i || $past(s1_tvalid_i)))",
       "owner_none_i |=> (!owner_s0_i || $past(s0_tvalid_i)))")],
     ["mutant-granted_without_request"], "informative"),
]


def sh(cmd, log, cwd=None):
    with open(log, "w") as handle:
        return subprocess.run(cmd, stdout=handle, stderr=subprocess.STDOUT, cwd=cwd, check=False).returncode


def fired(text):
    seen = []
    for match in FIRED.finditer(text):
        if match.group(1) not in seen:
            seen.append(match.group(1))
    return seen


def run_dut(tree, verilator, out):
    suite = tree / "tb/verilator/ptp_ts"
    pristine = (tree / "hdl/common/axis_mux_rr_2in_1out.sv").read_text()
    rows = []
    for name, width, pattern, replacement, why in DUT_MUTANTS:
        row = out / "dut" / name
        row.mkdir(parents=True, exist_ok=True)
        count = pristine.count(pattern)
        if count != 1:
            rows.append((name, "PATTERN", f"pattern occurs {count} times"))
            continue
        mutant = row / "axis_mux_rr_2in_1out.sv"
        mutant.write_text(pristine.replace(pattern, replacement))
        rc = sh(["make", "--no-print-directory", "-C", str(suite), "mux-sva-build", f"VERILATOR={verilator}",
                 f"MUX_SVA_WIDTH={width}", f"MUX_SVA_OBJ={row / 'obj'}", f"MUX_SVA_DUT={mutant}"],
                row / "build.log")
        if rc != 0:
            rows.append((name, "BUILD-FAIL", f"build exit {rc}"))
            continue
        binary = row / "obj" / "Vmux_sva"
        rc_default = sh([str(binary)], row / "run_default.log")
        rc_raised = sh([str(binary), "+verilator+error+limit+1000"], row / "run_raised.log")
        text = (row / "run_raised.log").read_text(errors="replace")
        fails = [line.strip() for line in text.splitlines() if line.lstrip().startswith("[FAIL]")
                 or line.startswith("FAIL")][:3]
        names = [p.split("u_sva.", 1)[-1] for p in fired(text)]
        verdict = "DETECTED" if rc_default != 0 else "SURVIVED"
        rows.append((name, verdict, f"w{width} default-exit={rc_default} raised-exit={rc_raised} "
                                    f"fired={names or 'none'} harness-fail={fails[:1] or 'none'} ({why})"))
    return rows


def run_weaken(tree, verilator, out):
    suite = tree / "tb/verilator/ptp_ts"
    rows = []
    only = sys.argv[5] if len(sys.argv) > 5 else ""
    for name, rel, rewrites, prefixes, expectation in WEAKEN:
        if not name.startswith(only):
            continue
        row = out / "weaken" / name
        row.mkdir(parents=True, exist_ok=True)
        path = tree / rel
        original = path.read_bytes()
        digest = hashlib.sha256(original).hexdigest()
        text = original.decode()
        bad = [p for p, _ in rewrites if text.count(p) != 1]
        if bad:
            rows.append((name, "PATTERN", f"not exactly once: {bad}"))
            continue
        for pattern, replacement in rewrites:
            text = text.replace(pattern, replacement)
        try:
            path.write_text(text)
            (row / Path(rel).name).write_text(text)
            rc_pos = sh(["make", "--no-print-directory", "-C", str(suite), "mux-sva", f"VERILATOR={verilator}"],
                        row / "positive.log")
            results = []
            for prefix in prefixes:
                safe = prefix.replace("/", "_")
                rc = sh([sys.executable, str(suite / "sva_campaign.py"), "--verilator", verilator, "--only", prefix],
                        row / f"campaign_{safe}.log")
                for raw in (suite / "obj_dir_sva_campaign").glob("*/*.log"):
                    keep = row / "raw" / safe / raw.parent.name
                    keep.mkdir(parents=True, exist_ok=True)
                    (keep / raw.name).write_bytes(raw.read_bytes())
                ctext = (row / f"campaign_{safe}.log").read_text(errors="replace")
                tally = re.search(r"checks: (\d+)\s+failures: (\d+)", ctext)
                results.append(f"{prefix}: exit {rc} ({tally.group(0) if tally else 'no tally'})")
            any_fail = any(" exit 1 " in r for r in results)
            all_fail = all(" exit 1 " in r for r in results)
            if expectation == "row-fails":
                verdict = "CAUGHT" if all_fail else ("PARTLY-CAUGHT" if any_fail else "NOT-CAUGHT")
            else:
                verdict = "INFO-caught" if any_fail else "INFO-survives"
            rows.append((name, verdict, f"positive mux-sva exit {rc_pos}; " + "; ".join(results)))
        finally:
            path.write_bytes(original)
            assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, f"restore failed for {rel}"
    return rows


def main():
    tree, verilator, out = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
    which = sys.argv[4] if len(sys.argv) > 4 else "all"
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    if which in ("dut", "all"):
        rows += [("dut",) + r for r in run_dut(tree, verilator, out)]
    if which in ("weaken", "all"):
        rows += [("weaken",) + r for r in run_weaken(tree, verilator, out)]
    with open(out / f"summary_{which}{("_" + sys.argv[5]) if len(sys.argv) > 5 else ""}.txt", "w") as handle:
        for family, name, verdict, detail in rows:
            line = f"{family:6} {verdict:14} {name}: {detail}"
            print(line)
            handle.write(line + "\n")


if __name__ == "__main__":
    main()
