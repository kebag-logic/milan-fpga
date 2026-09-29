#!/usr/bin/env python3
"""Disposable probe (R399-2): hunt the latency-independent LeaveAll stale-expiry
guard for a stale-forever case. Builds scratch copies of tb/srp_top from a
pristine tree (never the review clone) and adds one probe group, 'guardprobe':

  cycle   Peer MVRP and MSRP LeaveAlls 3 s before each own deadline, then two
          restarted cycles: each application's first own LeaveAll must come
          10-15 s after its peer (plus the join-tick ride), the second 10-15 s
          after the first. Run at arm delays 0 and 16 (ARM env), and with the
          timer service's ms timebase starting just before the 32-bit wrap
          (NOW0 env), so a superseded and a restarted deadline straddle it.
  drop    (DROP=1) The MSRP LeaveAll slot's restarted arm is dropped on its way
          to the timer service, as the processor top's per-face arm queue does
          on overrun (counted). Reports how many own MSRP LeaveAlls follow in
          the next 40 s.

Optional RTL mutants of the guard are applied with MUT (see MUTANTS below).
Usage: probe_guard.py <pristine tree> <work dir> <variant name>
Env: NOW0 (int, timer-service reset value of now_ms), ARM (0..16), DROP (0/1),
     MUT (mutant name or empty), GROUP (default 'guardprobe').
"""
import os, pathlib, re, shutil, subprocess, sys

src, work, name = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
NOW0 = int(os.environ.get("NOW0", "0")) & 0xFFFFFFFF
ARM = int(os.environ.get("ARM", "0"))
DROP = int(os.environ.get("DROP", "0"))
MUT = os.environ.get("MUT", "")
GROUP = os.environ.get("GROUP", "guardprobe")

OLD0 = ("  assign la_rearm_w[0] = need_draw_r[0] || (dr_inflight_r && !dr_app_r)\n"
        "                      || la_msrp_age_w[31];\n")
OLD1 = ("  assign la_rearm_w[1] = need_draw_r[1] || (dr_inflight_r && dr_app_r)\n"
        "                      || la_mvrp_age_w[31];\n")
MUTANTS = {
    # non-wrap-safe compare: stale while now < deadline, unsigned
    "unsigned-compare": [(OLD0, OLD0.replace("la_msrp_age_w[31]", "(now_ms_i < cad_dl_r[CAD_LA_MSRP_C])")),
                         (OLD1, OLD1.replace("la_mvrp_age_w[31]", "(now_ms_i < cad_dl_r[CAD_LA_MVRP_C])"))],
    # off by one: stale also at the deadline itself
    "age-le-zero": [(OLD0, OLD0.replace("la_msrp_age_w[31]", "(la_msrp_age_w[31] || la_msrp_age_w == 32'd0)")),
                    (OLD1, OLD1.replace("la_mvrp_age_w[31]", "(la_mvrp_age_w[31] || la_mvrp_age_w == 32'd0)"))],
    # the two applications' deadlines cross-wired
    "cross-deadline": [(OLD0, OLD0.replace("la_msrp_age_w[31]", "la_mvrp_age_w[31]")),
                       (OLD1, OLD1.replace("la_mvrp_age_w[31]", "la_msrp_age_w[31]"))],
    # the deadline term removed from the MVRP application only
    "mvrp-no-deadline": [(OLD1, OLD1.replace("\n                      || la_mvrp_age_w[31];", ";"))],
    # the issue-time guard of round 1 (as tb/srp_top/mutations/rearm-at-issue.patch)
    "rearm-at-issue": [(OLD0, OLD0.replace("la_msrp_age_w[31]", "cad_pend_r[CAD_LA_MSRP_C]")),
                       (OLD1, OLD1.replace("la_mvrp_age_w[31]", "cad_pend_r[CAD_LA_MVRP_C]"))],
}

PROBE = r'''
  // R399-2 probe helpers: wrap-safe time compare and own-LeaveAll times
  static bool before(uint32_t a, uint32_t b) { return static_cast<int32_t>(a - b) < 0; }
  void until_mod(uint32_t ms) { while (before(d->now_ms_o, ms)) h.cycle(); }
  static std::vector<uint32_t> own_la_ms(const H& bfm, size_t first, bool msrp) {
    std::vector<uint32_t> v;
    for (size_t i = first; i < bfm.archive.size(); i++) {
      auto p = parse_frame(bfm.archive[i]);
      bool la = false;
      for (const auto& x : p.vecs) la |= x.la;
      if (p.ok && la && p.msrp == msrp) v.push_back(bfm.archive_ms[i]);
    }
    return v;
  }
  void probe_guard() {
    d->arm_delay_i = GP_ARM;
    leaveall_setup(DECL_READY);
    const uint32_t now0 = d->now_ms_o;
    const uint32_t dm = d->dbg_la_deadline_o, dv = d->dbg_la_mvrp_deadline_o;
    printf("GUARD setup now0=%u msrp_dl=+%d mvrp_dl=+%d\n", now0,
           static_cast<int32_t>(dm - now0), static_cast<int32_t>(dv - now0));
    const size_t base = h.archive.size();
    const bool mvrp_first = before(dv, dm);
    uint32_t pm = 0, pv = 0;
    for (int k = 0; k < 2; k++) {
      const bool mv = (k == 0) == mvrp_first;
      const uint32_t at = (mv ? dv : dm) - 3000;
      until_mod(at);
      if (mv) { h.feed(peer_mvrp_leaveall(2), false); pv = d->now_ms_o; }
      else {
        if (GP_DROP) d->drop_la_arm_i = 1;
        h.feed(mrpdu_body(true, {la_only(4, 4, false)}), true); pm = d->now_ms_o;
        h.run_ms(50);
        d->drop_la_arm_i = 0;
      }
    }
    const uint32_t end = (before(pm, pv) ? pv : pm) + 40000;
    until_mod(end);
    auto om = own_la_ms(h, base, true), ov = own_la_ms(h, base, false);
    auto rel = [](const std::vector<uint32_t>& v, uint32_t from) {
      std::string s;
      for (auto x : v) s += std::to_string(static_cast<int32_t>(x - from)) + " ";
      return s;
    };
    printf("GUARD peer_msrp=+%d peer_mvrp=+%d wrap_at=+%d\n", static_cast<int32_t>(pm - now0),
           static_cast<int32_t>(pv - now0), static_cast<int32_t>(0u - now0));
    printf("GUARD own_msrp_ms_after_peer: %s\n", rel(om, pm).c_str());
    printf("GUARD own_mvrp_ms_after_peer: %s\n", rel(ov, pv).c_str());
    printf("GUARD msrp_expiries=%zu mvrp_expiries=%zu\n", h.expiry_cycles.size(), h.mvrp_expiry_cycles.size());
    if (GP_DROP) {
      printf("GUARD drop own_msrp_in_40s=%zu\n", om.size());
      CHECK(true, "GUARD drop scenario recorded");
    } else {
      auto in = [](int32_t x, int32_t lo, int32_t hi) { return x >= lo && x <= hi; };
      const bool okm = om.size() >= 2 && in(static_cast<int32_t>(om[0] - pm), 10000, 15400)
                       && in(static_cast<int32_t>(om[1] - om[0]), 10000, 15400);
      const bool okv = ov.size() >= 2 && in(static_cast<int32_t>(ov[0] - pv), 10000, 15400)
                       && in(static_cast<int32_t>(ov[1] - ov[0]), 10000, 15400);
      CHECK(okm, "GUARD: MSRP restarted cycle fires 10-15 s after the peer, then 10-15 s later");
      CHECK(okv, "GUARD: MVRP restarted cycle fires 10-15 s after the peer, then 10-15 s later");
    }
    d->arm_delay_i = 0;
  }
'''


def build(t):
    if t.exists():
        shutil.rmtree(t)
    (t / "tb").mkdir(parents=True)
    shutil.copytree(src / "hdl", t / "hdl")
    shutil.copytree(src / "tb" / "common", t / "tb" / "common")
    shutil.copytree(src / "tb" / "srp_top", t / "tb" / "srp_top", ignore=shutil.ignore_patterns("obj_*"))
    # C++: the probe group
    cpp = t / "tb/srp_top/sim_main.cpp"
    s = cpp.read_text()
    p = PROBE.replace("GP_ARM", str(ARM)).replace("GP_DROP", str(DROP))
    s = s.replace("  // P: issue #108.", p + "\n  // P: issue #108.", 1)
    s = s.replace('if (!*group || !strcmp(group,"join")) check_mvrp_join_before_the_stream();',
                  'if (!*group || !strcmp(group,"join")) check_mvrp_join_before_the_stream();\n'
                  '    if (!strcmp(group,"guardprobe")) probe_guard();', 1)
    s = s.replace('if (*group && strcmp(group,"armdelay")',
                  'if (*group && strcmp(group,"guardprobe") && strcmp(group,"armdelay")', 1)
    assert "probe_guard();" in s and '"guardprobe") && strcmp(group,"armdelay")' in s
    cpp.write_text(s)
    # wrapper: an input that drops arms to the MSRP LeaveAll slot (3 here)
    w = t / "tb/srp_top/srp_top_wrap.sv"
    v = w.read_text()
    v = v.replace("    input wire   [4:0]  arm_delay_i,",
                  "    input wire   [4:0]  arm_delay_i,\n    input wire          drop_la_arm_i,", 1)
    v = v.replace("      .arm_valid_i       (tmr_arm_valid_w),",
                  "      .arm_valid_i       (tmr_arm_valid_w && !(drop_la_arm_i && !tmr_arm_cancel_w"
                  " && tmr_arm_slot_w == TB_SLOT_AW_C'(3))),", 1)
    assert "drop_la_arm_i," in v and "(drop_la_arm_i &&" in v
    w.write_text(v)
    # timer service: the ms timebase's reset value
    ts = t / "hdl/common/KL_pp_timer_service.sv"
    x = ts.read_text()
    assert "      now_ms_r <= 32'd0;" in x
    x2 = x.replace("      now_ms_r <= 32'd0;", "      now_ms_r <= 32'd%d;" % NOW0, 1)
    ts.write_text(x2)
    # optional guard mutant
    if MUT:
        top = t / "hdl/srp/KL_srp_top.sv"
        y = top.read_text()
        for old, new in MUTANTS[MUT]:
            assert old in y, MUT
            y = y.replace(old, new, 1)
        top.write_text(y)


t = work / name
build(t)
log = work / f"{name}.log"
with log.open("w") as f:
    rc = subprocess.run(["make", "-C", str(t / "tb/srp_top"), "RUN_ARGS=" + GROUP],
                        stdout=f, stderr=subprocess.STDOUT).returncode
print(name, "rc", rc)
