#!/usr/bin/env python3
"""Scratch-only rows for the prepared round's start clock, and the two arms the
author left open. Usage: 04_collect_and_rv.py <exported-head> <work-dir> <receipt-dir>
C1: a value pending, an own LeaveAll round prepared, an offer whose search ends on the
    clock the join tick starts the prepared drain (st_r == E_COLLECT, go0_w).
C2: the same offer ending on the clock la_prepare_i leaves E_IDLE.
The producer drops its offer on the clock it is taken."""
import shutil, subprocess, sys
from pathlib import Path
head, work, rec = map(Path, sys.argv[1:4])
RTL = "hdl/srp/KL_srp_encoder.sv"
ROW = r'''
void SrpSuite::probe_prepared_start_clocks() {
  const Ev dm = mk_ev(0, 4, 1, 0, {0x06, 0x03, 0x00, 0x02});
  const Ev ot = mk_ev(0, 4, 1, 0, {0x06, 0x03, 0x00, 0x07});
  bring_out_of_reset();
  h.push_enc(dm);
  d->enc_la_prepare_i = 1;
  for (int i = 0; i < 50; ++i) { h.tick(); if (h.last_prepare_done) break; }
  d->enc_la_prepare_i = 0;
  h.offer(ot);
  h.tick();
  d->enc_join_tick_i = 1;
  h.tick();
  d->enc_join_tick_i = 0;
  const bool taken = h.last_enc_ready;
  d->enc_ev_valid_i = !taken;
  h.drop_on_accept = true;
  const bool first = h.wait_and_drain(got);
  const size_t first_len = got.size();
  h.run(40);
  h.drop_on_accept = false;
  const unsigned left = unsigned(d->enc_dbg_cnt_msrp_o);
  const bool second = h.capture_pdu(0, got);
  printf("PROBE C1 taken_on_go_clock=%d first_frame=%d first_len=%zu pending_after=%u second_frame=%d second_len=%zu\n",
         int(taken), int(first), first_len, left, int(second), second ? got.size() : size_t(0));
  bring_out_of_reset();
  h.push_enc(dm);
  h.offer(ot);
  h.tick();
  d->enc_la_prepare_i = 1;
  h.tick();
  const bool taken2 = h.last_enc_ready;
  d->enc_ev_valid_i = !taken2;
  h.drop_on_accept = true;
  for (int i = 0; i < 50; ++i) { h.tick(); if (h.last_prepare_done) break; }
  d->enc_la_prepare_i = 0;
  h.run(40);
  h.drop_on_accept = false;
  const unsigned held = unsigned(d->enc_dbg_cnt_msrp_o);
  const bool frame = h.capture_pdu(0, got);
  printf("PROBE C2 taken_on_prepare_clock=%d pending=%u frame=%d len=%zu\n",
         int(taken2), held, int(frame), got.size());
  bring_out_of_reset();
}
'''
def sub(p, old, new):
    s = p.read_text(); assert s.count(old) == 1, old; p.write_text(s.replace(old, new))
def tree(name, rtl=None, row=True):
    t = work / name
    shutil.rmtree(t, ignore_errors=True); t.mkdir(parents=True)
    shutil.copytree(head / "hdl", t / "hdl"); (t / "tb").mkdir()
    for s in ("common", "srp_encoder"):
        shutil.copytree(head / "tb" / s, t / "tb" / s, ignore=shutil.ignore_patterns("obj_*"))
    if rtl: sub(t / RTL, *rtl)
    if row:
        c = t / "tb/srp_encoder/sim_main.cpp"
        sub(c, "    d->clk_i = 1; d->eval();\n  }\n  void run(int n)",
            "    d->clk_i = 1; d->eval();\n    if (drop_on_accept && last_enc_ready) d->enc_ev_valid_i = 0;\n  }\n  void run(int n)")
        sub(c, "  bool last_prepare_done = false;\n", "  bool last_prepare_done = false;\n  bool drop_on_accept = false;\n")
        sub(c, "  void hold_a_push_off_its_drain_start();\n", "  void hold_a_push_off_its_drain_start();\n  void probe_prepared_start_clocks();\n")
        sub(c, "int SrpSuite::run() {\n", ROW + "\nint SrpSuite::run() {\n")
        sub(c, "  hold_a_push_off_its_drain_start();\n\n  printf(", "  hold_a_push_off_its_drain_start();\n  probe_prepared_start_clocks();\n\n  printf(")
    return t
START = "                     ? (start0_w || ((st_r == E_COLLECT) && go0_w)\n                        || ((st_r == E_IDLE) && la_prepare_i)) : start1_w;"
plans = {
 "c-head": None,
 "c-collect-term-dropped": (START, "                     ? (start0_w || ((st_r == E_IDLE) && la_prepare_i)) : start1_w;"),
 "c-laprepare-term-dropped": (START, "                     ? (start0_w || ((st_r == E_COLLECT) && go0_w)) : start1_w;"),
 "c-rv-search-ignores-start": ("assign sr_engage_w = ev_valid_i && valid_type_w && base_ok_w && (tgt_cnt_w != '0);",
                               "assign sr_engage_w = ev_valid_i && valid_type_w && !tgt_full_w && !busy_app_w && (tgt_cnt_w != '0);"),
}
procs = []
for name, rtl in plans.items():
    t = tree(name, rtl)
    f = (rec / f"{name}.log").open("w")
    procs.append((name, subprocess.Popen(["make", "-C", str(t / "tb/srp_encoder"), "run"], stdout=f, stderr=subprocess.STDOUT)))
t = tree("rv-empty-table-searches", ("&& (!valid_type_w || (tgt_cnt_w == '0) || sr_hit_w || sr_last_w);", "&& (!valid_type_w || sr_hit_w || sr_last_w);"), row=False)
f = (rec / "rv-empty-table-searches.log").open("w")
mk = t / "tb/srp_encoder/Makefile"
sub(mk, "\t./obj_dir/Vsrp_sim\n", "\tstdbuf -o0 ./obj_dir/Vsrp_sim\n")
procs.append(("rv-empty-table-searches", subprocess.Popen(["make", "-C", str(t / "tb/srp_encoder"), "run"], stdout=f, stderr=subprocess.STDOUT)))
for name, p in procs:
    rc = p.wait(); txt = (rec / f"{name}.log").read_text(errors="replace").splitlines()
    print(name, "rc", rc, [l for l in txt if " checks: " in l][-1:])
    for l in txt:
        if l.startswith("PROBE"): print("   ", l[:150])
    if name.startswith("rv-"):
        fl = [l for l in txt if l.startswith("FAIL:")]
        print("    named FAIL lines before the stop:", len(fl))
        for l in fl[:5]: print("     ", l[:120])
        print("    tail:", [l[:110] for l in txt[-4:]])
