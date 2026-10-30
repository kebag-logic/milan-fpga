#!/usr/bin/env python3
"""Reviewer probe: a non-ADP frame held MID-FRAME by the MAC when a REBOOT's
notification round ends, in the non-advertising and the advertising path.

Applies to a private copy of a tree, optionally plants one RTL patch first,
runs only the probe scenarios of tb/pp_top section RBT, and writes the log.

usage: probe_mid.py TREE SCRATCH_DIR LOG VERILATOR [RTL_PATCH]
"""
import shutil, subprocess, sys
from pathlib import Path

SIM = "tb/pp_top/sim_main.cpp"

FIELDS_ANCHOR = "  bool stall_rbt_ntf_at_eof = false;\n"
FIELDS = """  //! reviewer probe: hold tx_ready_i low at byte stall_mid_byte of the first
  //! frame whose first byte the MAC took after clock stall_mid_after_t
  long stall_mid_after_t = -1;
  size_t stall_mid_byte = 30;
  bool mid_stalled = false;
  long mid_frame_sof_t = -1;
"""

HOOK_ANCHOR = "    if (d->rst_n && d->tx_valid_o) tx_offer_t = long(t);\n"
HOOK = """    if (stall_mid_after_t >= 0 && d->tx_valid_o && in_frame && !d->tx_eof_o
        && long(cur_sof_t) > stall_mid_after_t && cur.size() == stall_mid_byte) {
      mac_tx_ready = false;
      mid_stalled = true;
      mid_frame_sof_t = long(cur_sof_t);
    }
"""

RUN_ANCHOR = "  void run() {\n    refusals();\n"
PROBE = r"""  //! reviewer probe: the requester's lock expires while the MAC holds the
  //! REBOOT notification's last byte 1 s; released, the next frame (the
  //! automatic unlock's notification, not ADP's) is held by the MAC at its
  //! 30th byte for 500 ms, mid-frame, then its last byte is taken
  void probe_mid(bool advertise, const char* tag) {
    boot(advertise, tag);
    register_ctlr(C2_MAC, CTLR2_EID, tag);
    lock(CTLR_MAC, CTLR_EID, true, tag);
    io.run_ms(20);
    io.tx_log.clear();
    io.stall_rbt_ntf_at_eof = true;
    send(CTLR_MAC, CTLR_EID, AEM_REBOOT, ti(DT_ENTITY, 0));
    for (long c = 0; c < 2000L * MS_CYC && !io.tx_eof_stalled; ++c) io.step();
    CHECK(io.tx_eof_stalled, "%s the MAC holds the REBOOT notification's last byte", tag);
    io.run_ms(1000);
    io.stall_rbt_ntf_at_eof = false;
    io.tx_eof_stalled = false;
    io.mid_stalled = false;
    io.stall_mid_after_t = long(io.t);
    io.mac_tx_ready = true;
    for (long c = 0; c < 50L * MS_CYC && !io.mid_stalled; ++c) io.step();
    CHECK(io.mid_stalled, "%s the MAC holds the next frame mid-frame", tag);
    const auto part = io.cur;
    const bool non_adp = part.size() > 14 && part[14] != 0xFA;
    printf("  %s held mid-frame: %zu bytes taken, subtype %02x, sof at %ld\n", tag,
           part.size(), part.size() > 14 ? part[14] : 0, io.mid_frame_sof_t);
    CHECK(non_adp, "%s the frame held mid-frame is not ADP's", tag);
    io.run_ms(500);
    CHECK(io.reboot_rise_t < 0,
          "%s reboot_req_o stays 0 while the MAC holds another lane's frame mid-frame "
          "(rise %ld)", tag, io.reboot_rise_t);
    io.stall_mid_after_t = -1;
    io.mac_tx_ready = true;
    for (long c = 0; c < 3000L * MS_CYC && io.reboot_rise_t < 0; ++c) io.step();
    io.run_ms(2000);
    long t_rsp = -1, t_ntf = -1, t_held = -1, t_dep = -1;
    int deps = 0, after = 0;
    for (const auto& e : io.tx_log) {
      const auto& f = e.second;
      const long te = long(e.first);
      printf("  %s frame: last byte at %ld, %zu bytes, subtype %02x, to %012llx\n", tag, te,
             f.size(), f.size() > 14 ? f[14] : 0, static_cast<unsigned long long>(dst(f)));
      if (aecp(f) && ct(f) == AEM_REBOOT && !(f[36] & 0x80) && st(f) == AECP_SUCCESS)
        t_rsp = te;
      if (aecp(f) && ct(f) == AEM_REBOOT && (f[36] & 0x80) && dst(f) == C2_MAC) t_ntf = te;
      if (t_held < 0 && f.size() >= part.size()
          && std::equal(part.begin(), part.end(), f.begin()) && te > t_ntf && t_ntf >= 0)
        t_held = te;
      if (departing(f)) { ++deps; t_dep = te; }
      if (io.reboot_rise_t >= 0 && te >= io.reboot_rise_t) ++after;
    }
    printf("  %s rsp %ld ntf %ld held %ld dep %ld (%d) rise %ld last offered %ld torn %d\n",
           tag, t_rsp, t_ntf, t_held, t_dep, deps, io.reboot_rise_t, io.tx_offer_t,
           io.tx_torn);
    CHECK(t_rsp >= 0 && t_ntf > t_rsp && t_held > t_ntf,
          "%s SUCCESS, then the notification, then the held frame whole", tag);
    if (advertise) {
      CHECK(deps == 1 && t_dep > t_ntf,
            "%s one ENTITY_DEPARTING, after the notification (%d at %ld)", tag, deps, t_dep);
    } else {
      CHECK(deps == 0, "%s no ENTITY_DEPARTING (%d)", tag, deps);
    }
    const long t_last = std::max(t_held, t_dep);
    CHECK(io.reboot_rise_t > t_last && after == 0 && io.tx_offer_t < io.reboot_rise_t,
          "%s reboot_req_o rises after every frame's last byte and no byte is offered "
          "from the rise (rise %ld, last %ld, offered %ld, %d after)", tag,
          io.reboot_rise_t, t_last, io.tx_offer_t, after);
    CHECK(io.tx_torn == 0, "%s every byte the MAC took belongs to a whole frame", tag);
    CHECK(io.d->reboot_req_o, "%s reboot_req_o is held", tag);
  }

"""
RUN_HOOK = """    probe_mid(false, "PRM-NA");
    probe_mid(true, "PRM-ADV");
    return;
"""


def plant(text, anchor, new, before=True):
    assert text.count(anchor) == 1, f"anchor matches {text.count(anchor)} times: {anchor!r}"
    return text.replace(anchor, (new + anchor) if before else (anchor + new))


def main():
    tree_in, scratch, log, ver = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
    rtl = Path(sys.argv[5]).resolve() if len(sys.argv) > 5 else None
    tree = scratch / ("prm_" + log.stem)
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(tree_in, tree, symlinks=True)
    shutil.rmtree(tree / "tb/pp_top/obj_dir", ignore_errors=True)
    out = ""
    if rtl:
        r = subprocess.run(["patch", "-p1", "-i", str(rtl)], cwd=tree, capture_output=True, text=True)
        out += f"### planted {rtl.name}: rc={r.returncode}\n{r.stdout}{r.stderr}"
        assert r.returncode == 0
    src = tree / SIM
    t = src.read_text()
    t = plant(t, FIELDS_ANCHOR, FIELDS, before=False)
    t = plant(t, HOOK_ANCHOR, HOOK)
    t = plant(t, RUN_ANCHOR, PROBE)
    t = t.replace(RUN_ANCHOR, RUN_ANCHOR.replace("    refusals();\n", RUN_HOOK + "    refusals();\n"))
    src.write_text(t)
    r = subprocess.run(["make", "-C", str(tree / "tb/pp_top"), "reboot", "VERILATOR=" + ver],
                       capture_output=True, text=True)
    out += f"### make reboot: rc={r.returncode}\n" + r.stdout + r.stderr
    log.write_text(out)
    tally = [l for l in out.splitlines() if l.startswith("RBT:")]
    fails = [l for l in out.splitlines() if l.startswith("FAIL")]
    print(f"{log.stem}: rc={r.returncode} {tally} {len(fails)} FAIL lines")
    for l in fails[:8]:
        print("    " + l)
    shutil.rmtree(tree, ignore_errors=True)


if __name__ == "__main__":
    main()
