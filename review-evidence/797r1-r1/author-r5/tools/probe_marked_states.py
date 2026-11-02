#!/usr/bin/env python3
"""The reviewer's probe of the SRP-served clause (#797), its sequences
unchanged, judged against the new rows: for each state it prints the clause
"the SRP table's latest answer to the window was a poll, after the last
STRM_SEL/STRMW_CTRL write, with no other master using the table since" from the
head harness's own record (tick()), the value the new row predicts
(0x00004444 / 0x66666666 when it holds, else 0), and whether the read agrees.
The old clause ("answered a poll since the last write") is printed beside it.

Builds milan_csr with Verilator at the page's build parameters with two
listeners and two talkers (the sweep's 2x2 build), selects talker index 1, and
drives two engine-side sequences the block's port contract allows:

  A. a continuously granting engine around a provisioning STRMW_CTRL write:
     the grant window is shifted cycle by cycle; for each offset the probe
     records whether a POLL was answered after the write fired, then reads
     STRMW_SRP (0x85C) and STRMW_SID_LO (0x814) once the engine is idle;
  B. a poll answer, then one i_srp_ctx_stolen beat (another master used the
     table), then reads.

A read of 0 in a state where a poll was answered after the last STRM_SEL and
STRMW_CTRL write disagrees with the printed clause, whose row says
{16'd0, i_srp_ctx_rd_stat} / i_srp_ctx_rd_sid.

Usage: python3 -I probe_srp_poll_clause.py REPO WORKDIR   (verilator on PATH)
"""
import subprocess
import sys
from pathlib import Path

repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.dont_write_bytecode = True  # leave the reviewed clone untouched
sys.path.insert(0, str(repo / "scripts"))
import register_read_sweep as sweep  # noqa: E402  (the reviewed head's own helpers)

page = (repo / sweep.PAGE).read_text(encoding="utf-8").splitlines()
params = {**sweep.build_parameters(page), **sweep.WIDE}
text = (repo / sweep.RTL).read_text(encoding="utf-8")
base = sweep.harness(text, [0x85C], params, sweep.rtl_constants(text))
head = base[:base.index("static const uint32_t WORDS")]
init = base[base.index("  t->s_axi_awvalid = 0;"):base.index("  for (int i = 0; i < (int)(sizeof(t->i_acmp_tbl_ctx)")]

main = r'''
static int bad = 0;
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv); t = new Vmilan_csr; auto* r = t->rootp;
''' + init + r'''
  t->i_srp_ctx_rd_stat = 0x4444; t->i_srp_ctx_rd_sid = 0x5555555566666666ULL;
  t->aresetn = 0; ticks(8); t->aresetn = 1; ticks(530);
  // A: grant window [off, off+len) in ticks from the start of the CTRL write
  for (int len = 1; len <= 3; len++)
  for (int off = 0; off < 8; off++) {
    wr(0x800, 0x101); ticks(4);
    answer_srp();
    int fired = 0, poll_after = 0, write_ans = 0, hs = 0;
    t->s_axi_awaddr = 0x810; t->s_axi_wdata = 1; t->s_axi_wstrb = 0xF; t->s_axi_bready = 1;
    for (int k = 0; k < 14; k++) {
      t->s_axi_awvalid = !hs; t->s_axi_wvalid = !hs;
      t->i_srp_ctx_gnt = (k >= off && k < off + len);
      t->eval();
      int ready = t->s_axi_awready, waswr = r->milan_csr__DOT__srp_cmd_was_wr_r;
      int pend0 = r->milan_csr__DOT__srp_wr_pend_r;
      if (t->i_srp_ctx_gnt && !waswr && fired) poll_after = 1;
      if (t->i_srp_ctx_gnt && waswr) write_ans = 1;
      tick();
      if (ready && !hs) hs = 1;
      if (!pend0 && r->milan_csr__DOT__srp_wr_pend_r) fired = 1;
    }
    t->s_axi_awvalid = 0; t->s_axi_wvalid = 0; t->i_srp_ctx_gnt = 0; t->eval(); ticks(6);
    uint32_t srp = rd(0x85C), sid = rd(0x814);
    int now = ans_poll && at_ans > at_selwr && !(at_steal > at_ans), was = at_poll > at_selwr;
    int ok = srp == (now ? 0x4444u : 0u) && sid == (now ? 0x66666666u : 0u);
    printf("A len=%d off=%d poll_answered_after_write=%d write_answered=%d STRMW_SRP=%08x STRMW_SID_LO=%08x"
           " new_clause=%d new_agrees=%d old_clause=%d%s\n", len, off, poll_after, write_ans, srp, sid, now, ok, was,
           (poll_after && write_ans && srp == 0 && sid == 0 && (len == 2 && off == 1 || len == 3 && off <= 1))
           ? "  <-- marked" : "");
    bad += !ok;
  }
  // B: poll answer, then a stolen beat
  wr(0x800, 0x101); ticks(4);
  answer_srp();
  uint32_t before = rd(0x85C);
  t->i_srp_ctx_stolen = 1; tick(); t->i_srp_ctx_stolen = 0; t->eval(); ticks(2);
  uint32_t after = rd(0x85C), sid = rd(0x814);
  int now = ans_poll && at_ans > at_selwr && !(at_steal > at_ans), was = at_poll > at_selwr;
  int ok = after == (now ? 0x4444u : 0u) && sid == (now ? 0x66666666u : 0u);
  printf("B before the stolen beat STRMW_SRP=%08x; after it STRMW_SRP=%08x STRMW_SID_LO=%08x"
         " new_clause=%d new_agrees=%d old_clause=%d  <-- marked\n", before, after, sid, now, ok, was);
  bad += !ok;
  printf("states disagreeing with the new rows: %d\n", bad);
  delete t; return bad ? 1 : 0;
}
'''
work.mkdir(parents=True, exist_ok=True)
(work / "probe.cpp").write_text(head + main, encoding="utf-8")
cmd = ["verilator", "--cc", "--exe", "--build", "-j", "8", "-O2", "-Wno-fatal", "-Wno-lint", "-Wno-style",
       "--public-flat-rw", "--top-module", "milan_csr", f"+incdir+{repo / sweep.CSR_INCLUDE}",
       f"+incdir+{repo / sweep.SHAPE_INCLUDE['2x2']}", "--Mdir", str(work / "obj"), "-o", "Vprobe",
       *[f"-G{n}={v}" for n, v in params.items()], str(repo / sweep.RTL), str(work / "probe.cpp")]
built = subprocess.run(cmd, capture_output=True, text=True, check=False)
if built.returncode:
    print(built.stdout[-3000:], built.stderr[-3000:])
    sys.exit(2)
ran = subprocess.run([str(work / "obj" / "Vprobe")], capture_output=True, text=True, check=False)
print(ran.stdout, end="")
sys.exit(ran.returncode)
