#!/usr/bin/env python3
"""Two scratch-only bench edits, never applied to the clone.
A: PV20 with a producer that drops its offer on the clock it is taken, as the row's
   comment says, run on the head and on the busy-not-in-alloc reviewer arm.
B: an unknown AttributeType offered on a full table and to a draining application,
   printing whether it is taken on its first clock (PV19's comment says never held)."""
import shutil, subprocess, sys
from pathlib import Path
head, work, rec = map(Path, sys.argv[1:4])
def tree(name):
    t = work / name
    shutil.rmtree(t, ignore_errors=True); t.mkdir(parents=True)
    shutil.copytree(head / "hdl", t / "hdl"); (t / "tb").mkdir()
    for s in ("common", "srp_encoder"):
        shutil.copytree(head / "tb" / s, t / "tb" / s, ignore=shutil.ignore_patterns("obj_*"))
    return t
def sub(p, old, new):
    s = p.read_text(); assert s.count(old) == 1, old; p.write_text(s.replace(old, new))
def producer(t):
    c = t / "tb/srp_encoder/sim_main.cpp"
    sub(c, "    d->clk_i = 1; d->eval();\n  }\n  void run(int n)",
        "    d->clk_i = 1; d->eval();\n    if (drop_on_accept && last_enc_ready) d->enc_ev_valid_i = 0;\n  }\n  void run(int n)")
    sub(c, "  bool last_prepare_done = false;\n", "  bool last_prepare_done = false;\n  bool drop_on_accept = false;\n")
    sub(c, "  d->enc_ev_valid_i = !taken;\n  const bool frame = h.wait_and_drain(got);\n",
        "  d->enc_ev_valid_i = !taken;\n  h.drop_on_accept = true;\n  const bool frame = h.wait_and_drain(got);\n  h.run(40);\n  h.drop_on_accept = false;\n")
def busy(t):
    sub(t / "hdl/srp/KL_srp_encoder.sv", "assign busy_app_w  = (st_r != E_IDLE) && (st_r != E_COLLECT)\n",
        "assign busy_app_w  = (st_r != E_IDLE) && (st_r != E_COLLECT) && (st_r != E_ALLOC)\n")
def unknown(t):
    sub(t / "tb/srp_encoder/sim_main.cpp",
        "  CHECK(h.capture_pdu(1, got), \"PV19 MVRP frame captured\");\n  check_pdu(\"PV19 the MVRP frame carries the pending value\", got,\n            model_pdu({vd}, false, OWN_MAC));\n",
        "  CHECK(h.capture_pdu(1, got), \"PV19 MVRP frame captured\");\n  check_pdu(\"PV19 the MVRP frame carries the pending value\", got,\n            model_pdu({vd}, false, OWN_MAC));\n"
        "  bring_out_of_reset();\n  for (int i = 0; i < 12; ++i) h.push_enc(mk_ev(0, 3, 1, 0, {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x00, uint8_t(0x20 + 2 * i)}));\n"
        "  printf(\"PROBE pending=%u\\n\", unsigned(d->enc_dbg_cnt_msrp_o));\n"
        "  printf(\"PROBE unknown type on a full table taken on its first clock=%d\\n\", int(h.push_enc(mk_ev(0, 9, 0, 0, {0x01}), 1)));\n"
        "  bring_out_of_reset();\n  h.push_enc(dm);\n  d->enc_join_tick_i = 1; h.tick(); d->enc_join_tick_i = 0; h.run(2);\n"
        "  printf(\"PROBE unknown type beside its own drain taken on its first clock=%d\\n\", int(h.push_enc(mk_ev(0, 9, 0, 0, {0x01}), 1)));\n"
        "  bring_out_of_reset();\n")
plans = {"pv20-producer-head": [producer], "pv20-producer-busy-arm": [producer, busy], "pv19-unknown-held": [unknown]}
procs = []
for name, edits in plans.items():
    t = tree(name)
    for e in edits: e(t)
    f = (rec / f"{name}.log").open("w")
    procs.append((name, subprocess.Popen(["make", "-C", str(t / "tb/srp_encoder"), "run"], stdout=f, stderr=subprocess.STDOUT)))
for name, p in procs:
    rc = p.wait(); txt = (rec / f"{name}.log").read_text(errors="replace").splitlines()
    print(name, "rc", rc, [l for l in txt if " checks: " in l][-1:])
    for l in txt:
        if l.startswith(("FAIL:", "PROBE")): print("   ", l[:150])
