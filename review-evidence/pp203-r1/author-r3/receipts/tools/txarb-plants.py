#!/usr/bin/env python3
"""txarb-plants.py TREE OUT: plant each tx_arbiter suite mutation (README M1..M7) in its own copy
of TREE's hdl/ and tb/{common,tx_arbiter}, build and run the suite, and record the tally and the
failing checks. Each plant is an exact single-occurrence substitution in KL_pp_tx_arbiter.sv."""
import pathlib, shutil, subprocess, sys, concurrent.futures as cf
TREE, OUT = (pathlib.Path(a).resolve() for a in sys.argv[1:3])
ARB = "hdl/packet_engine/KL_pp_tx_arbiter.sv"
PLANTS = {
    "control": [],
    "M1-aging-never-promotes": [("key_w[i] = {~aged_w[i], PRIO_MAP_P[2*i +: 2]};",
                                 "key_w[i] = {1'b1, PRIO_MAP_P[2*i +: 2]};")],
    "M2-pacing-dropped": [("elig_w = (pace_nonsol_r && sol_pend_w) ?", "elig_w = (1'b0) ?")],
    "M3-priority-inverted": [("(key_w[j] <= key_w[i])) win_w[i] = 1'b0;", "(key_w[j] >= key_w[i])) win_w[i] = 1'b0;"),
                             ("(key_w[j] < key_w[i]))  win_w[i] = 1'b0;", "(key_w[j] > key_w[i]))  win_w[i] = 1'b0;")],
    "M4-atomicity-broken": [("assign eof_w     = consume_w && ser_last_i;", "assign eof_w     = consume_w;")],
    "M5-abort-ignored": [("  assign accept_w  = (arb_st_r == A_START) && !start_sent_r\n                     && !start_abort_i;",
                          "  assign accept_w  = (arb_st_r == A_START) && !start_sent_r;"),
                         ("  assign abort_w   = (arb_st_r == A_START) && !start_sent_r\n                     && start_abort_i;",
                          "  assign abort_w   = 1'b0;"),
                         ("  assign ser_req_o   = (arb_st_r == A_START)\n                       && (start_sent_r || !start_abort_i);",
                          "  assign ser_req_o   = (arb_st_r == A_START);")],
    "M6-busy-from-the-stream": [("assign busy_o      = (arb_st_r != A_IDLE);", "assign busy_o      = (arb_st_r == A_STREAM);")],
    "M7-busy-ends-at-last-byte-offered": [("assign busy_o      = (arb_st_r != A_IDLE);",
                                           "assign busy_o      = (arb_st_r != A_IDLE) && !(ser_valid_i && ser_last_i);")],
}
OUT.mkdir(parents=True, exist_ok=True)

def one(name):
    d = OUT / "scratch" / name
    if d.exists():
        shutil.rmtree(d)
    for sub in ("hdl", "tb/common", "tb/tx_arbiter"):
        shutil.copytree(TREE / sub, d / sub, ignore=shutil.ignore_patterns("obj_dir"))
    f = d / ARB
    t = f.read_text()
    for old, new in PLANTS[name]:
        if t.count(old) != 1:
            return name, f"PLANT TEXT occurs {t.count(old)} times: {old[:50]!r}"
        t = t.replace(old, new)
    f.write_text(t)
    log = OUT / f"{name}.log"
    with log.open("w") as fh:
        r = subprocess.run(["make", "VERILATOR=/usr/bin/verilator"], cwd=d / "tb/tx_arbiter",
                           stdout=fh, stderr=subprocess.STDOUT)
    text = log.read_text()
    tally = [l for l in text.splitlines() if " checks: " in l and "PASS" in l]
    fails = [l for l in text.splitlines() if l.startswith("FAIL")]
    shutil.rmtree(d)
    return name, f"rc={r.returncode} {tally[-1] if tally else 'NO TALLY'}; failing: " + " | ".join(fails[:40])

with cf.ThreadPoolExecutor(4) as ex:
    res = list(ex.map(one, PLANTS))
with (OUT / "SUMMARY.txt").open("w") as fh:
    for name, s in res:
        print(f"{name}: {s}", file=fh)
        print(f"{name}: {s}"[:400])
shutil.rmtree(OUT / "scratch", ignore_errors=True)
