#!/usr/bin/env python3
"""Reviewer fault probes for tb/adp_engine at the reviewed head (disposable).

Each probe copies hdl/ and tb/{common,adp_engine} of the checkout given by
--root into a scratch directory of its own, applies one exact string
replacement (which must match exactly once), runs `make -C tb/adp_engine run`
and records rc, the tally and every FAIL line. A control with no edit runs
first. Nothing is written to the checkout.

usage: probes.py --root CHECKOUT --scratch DIR --out RECEIPT_DIR [--jobs N]
       (VERILATOR in the environment names the simulator)
"""
import argparse
import concurrent.futures
import pathlib
import shutil
import subprocess

SV = "hdl/adp/KL_adp_engine.sv"
TB = "tb/adp_engine/sim_main.cpp"

FRESH_ANCHOR = "  int ac[4] = {};\n"
FRESH_CHECK = """  {  // reviewer probe: arc 4 notes the fresh index (Milan 5.6.4.5.2 step 3)
    const unsigned s = 0;
    const uint64_t tk = walk_talker(s);
    set_bound(s, tk, false); idle(6); set_bound(s, tk, true); idle(4);
    load_remote(0, tk, 700, d->gm_id_i, DOM0, 0, 10, MSG_AVAIL);
    CHECK(send_txn(adp_txn(MSG_AVAIL, tk, 10, 0, now)), "PROBE discovery consumed");
    idle(20);
    load_remote(0, tk, 701, d->gm_id_i, DOM0, 0, 10, MSG_AVAIL);
    CHECK(send_txn(adp_txn(MSG_AVAIL, tk, 10, 0, now)), "PROBE fresh consumed");
    idle(20);
    const size_t e1 = evts.size();
    load_remote(0, tk, 701, d->gm_id_i, DOM0, 0, 10, MSG_AVAIL);
    CHECK(send_txn(adp_txn(MSG_AVAIL, tk, 10, 0, now)), "PROBE repeat consumed");
    idle(20);
    CHECK(evts.size() - e1 == 2 && evts[e1].departed && !evts[e1 + 1].departed,
          "PROBE arc 4 noted the fresh index: a repeat of it is the restart pair, got %zu events",
          evts.size() - e1);
    set_bound(s, tk, false); idle(8);
  }
"""

# name: ([(file, old, new), ...], what it breaks, which check must go red)
# (a single-edit probe is written (file, old, new, what, expected))
PROBES = {
    "control": None,
    # ---- RTL: the five cells #85 named, at properties no checked-in arm plants
    "r1-shutdown-keeps-timer": (
        SV,
        "          adv_st_r[i] <= ADP_ADV_DOWN;        // pend_dep set below\n"
        "          tpend_r[i]  <= TPEND_CANCEL;\n",
        "          adv_st_r[i] <= ADP_ADV_DOWN;        // pend_dep set below\n",
        "SHUTDOWN leaves the running T-ADP-ADV / T-ADP-DELAY armed",
        "SHUTDOWN x WAITING / DELAY(timer armed): the running timer is stopped"),
    "r2-delay-linkdown-departs": (
        SV,
        "        if (enable_fall_w && (adv_st_r[i] != ADP_ADV_DOWN)) begin\n"
        "          pend_dep_r[i]   <= 1'b1;\n",
        "        if ((enable_fall_w || (link_fall_w[i] && (adv_st_r[i] == ADP_ADV_DELAY)))\n"
        "            && (adv_st_r[i] != ADP_ADV_DOWN)) begin\n"
        "          pend_dep_r[i]   <= 1'b1;\n",
        "LINK_DOWN in DELAY queues an ENTITY_DEPARTING (Milan 5.6.3.5.10 says none)",
        "LINK_DOWN x DELAY: 0 frames"),
    "r3-delay-gm-change-redraws": (
        SV,
        "        if (gm_change_i[i] && (adv_st_r[i] == ADP_ADV_WAITING)) begin\n",
        "        if (gm_change_i[i] && (adv_st_r[i] != ADP_ADV_DOWN)) begin\n",
        "GM_CHANGE in DELAY restarts the delay (Table 5.51 '-')",
        "GM_CHANGE x DELAY cells"),
    "r4-departing-increments": (
        SV,
        "      if (bld_done_dep_w) begin\n"
        "        aidx_r[bld_done_if_w] <= 32'd0;\n",
        "      if (bld_done_dep_w) begin\n"
        "        aidx_r[bld_done_if_w] <= aidx_r[bld_done_if_w] + 32'd1;\n",
        "the reference platform's former rule: ENTITY_DEPARTING increments, no reset",
        "SHUTDOWN x WAITING / both DELAY phases: available_index 0"),
    # ---- RTL: F04.3 arcs at actions the arc- arms do not plant
    "r5-noadp-expiry-keeps-state": (
        SV,
        "      if (noadp_exp_w) begin\n"
        "        disc_st_r[noadp_exp_sink_w] <= 1'b0;\n"
        "      end\n",
        "      if (noadp_exp_w) begin\n"
        "      end\n",
        "a T-ADP-NOADP expiry raises DEPARTED but leaves the sink TK_DISCOVERED",
        "arc DISCOVERED -> NOT (T-ADP-NOADP expiry)"),
    "r6-fresh-no-store": (
        SV,
        "            rec_wr_en_w = 1'b1;               // fresh cycle: store + re-arm\n",
        "            // fresh cycle: re-arm only (probe: the index is not noted)\n",
        "a fresh index in TK_DISCOVERED is not noted (F04.8 arc 4 'note the index')",
        "any check: does the walk or a directed phase grade the noted index?"),
    "r7-restart-no-store": (
        SV,
        "            ev_dep_w    = 1'b1;\n"
        "            ev_disc_w   = 1'b1;\n"
        "            rec_wr_en_w = 1'b1;\n",
        "            ev_dep_w    = 1'b1;\n"
        "            ev_disc_w   = 1'b1;\n",
        "the restart pair does not note the new index (F04.8 arc 5 'note the index')",
        "any check: does the walk or a directed phase grade the noted index?"),
    "r8-discover-no-store": (
        SV,
        "            ev_disc_w   = 1'b1;\n"
        "            st_set_w    = 1'b1;\n"
        "            rec_wr_en_w = 1'b1;\n",
        "            ev_disc_w   = 1'b1;\n"
        "            st_set_w    = 1'b1;\n",
        "TK_NOT_DISCOVERED to TK_DISCOVERED saves neither interface_index nor index",
        "arc NOT -> DISCOVERED or a later cell"),
    # ---- testbench: the walk is driven by its table and ends with counts
    "t1-table-expects-departing": (
        TB,
        "   {'N', ST_DOWN, 0, 0, true, true, 0, \"5.6.3.5.10\", I_LINK}},         // LINK_DOWN\n",
        "   {'N', ST_DOWN, 0, 0, true, true, 2, \"5.6.3.5.10\", I_LINK}},         // LINK_DOWN\n",
        "the table (not the RTL) is changed: DELAY(armed) x LINK_DOWN expects a DEPARTING",
        "LINK_DOWN x DELAY(timer armed): 1 frames"),
    "t2-walk-skips-a-cell": (
        TB,
        "      walk_advertise_cell(row, col);\n      ++adv_cells;\n",
        "      if (row == R_SHUT && col == A_DLY) continue;\n"
        "      walk_advertise_cell(row, col);\n      ++adv_cells;\n",
        "the walk loop skips DELAY(armed) x SHUTDOWN",
        "P13 MTXW walked 44 F04.2 cells (want 45"),
    "t3-cell-loses-ieee-citation": (
        TB,
        "constexpr const char* I_LINK = \"6.2.7.2 LINK STATE CHANGE, no needsAdvertise\";\n",
        "constexpr const char* I_LINK = \"\";\n",
        "three LINK_DOWN cells lose their IEEE citation",
        "P13 F04.2 cells citing ... 42 of 45"),
    # ---- the r6 survivor: a check that grades arc 4's noted index
    "x1-fresh-noted-check": (
        [(TB, FRESH_ANCHOR, FRESH_CHECK + FRESH_ANCHOR)],
        "nothing in the RTL: the walk gains one check that arc 4 noted the fresh index",
        "nothing: the head RTL must pass it"),
    "x2-fresh-noted-check-vs-r6": (
        [(TB, FRESH_ANCHOR, FRESH_CHECK + FRESH_ANCHOR),
         (SV, "            rec_wr_en_w = 1'b1;               // fresh cycle: store + re-arm\n",
          "            // fresh cycle: re-arm only (probe: the index is not noted)\n")],
        "r6's RTL fault under x1's added check",
        "PROBE arc 4 noted the fresh index"),
}


def edits_of(spec):
    if spec is None:
        return []
    if isinstance(spec[0], list):
        return spec[0]
    return [(spec[0], spec[1], spec[2])]


def what_of(spec):
    return spec[1:] if isinstance(spec[0], list) else spec[3:]


def run_probe(name, spec, root, scratch, out):
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(root / "hdl", tree / "hdl")
    for sub in ("common", "adp_engine"):
        shutil.copytree(root / "tb" / sub, tree / "tb" / sub,
                        ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
    for rel, old, new in edits_of(spec):
        path = tree / rel
        text = path.read_text()
        assert text.count(old) == 1, f"{name}: anchor matches {text.count(old)} times"
        path.write_text(text.replace(old, new))
    log = out / f"probe-{name}.log"
    with log.open("w") as stream:
        rc = subprocess.run(["make", "-C", str(tree / "tb" / "adp_engine"), "run"],
                            stdout=stream, stderr=subprocess.STDOUT, check=False).returncode
    text = log.read_text()
    tally = [l for l in text.splitlines() if l.endswith(" FAIL") and "checks:" in l]
    fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
    return name, rc, (tally[-1] if tally else "NO TALLY"), fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=pathlib.Path, required=True)
    ap.add_argument("--scratch", type=pathlib.Path, required=True)
    ap.add_argument("--out", type=pathlib.Path, required=True)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    a.scratch.mkdir(parents=True, exist_ok=True)
    a.out.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        futs = [pool.submit(run_probe, n, s, a.root, a.scratch, a.out) for n, s in PROBES.items()]
        results = [f.result() for f in futs]
    with (a.out / "probes-summary.txt").open("w") as summary:
        for name, rc, tally, fails in results:
            spec = PROBES[name]
            head = f"{name}: rc={rc} {tally} failures={len(fails)}"
            if spec:
                what, expected = what_of(spec)
                head += f"\n  breaks: {what}\n  expected red: {expected}"
            print(head, file=summary)
            for line in fails:
                print(f"    {line}", file=summary)
    print((a.out / "probes-summary.txt").read_text())


if __name__ == "__main__":
    main()
