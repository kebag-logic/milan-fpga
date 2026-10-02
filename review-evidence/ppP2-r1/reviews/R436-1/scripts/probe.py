#!/usr/bin/env python3
"""Reviewer-owned planted-defect campaign for KL_pp_nvm_port (and two
tb/acmp_nvm probes). Each probe: a fresh `git archive` copy of the exact head,
exact-anchor edits (each anchor must occur exactly once), one build+run of the
named suite, tally and failing check names recorded. The source clone is never
touched.  Usage: probe.py REPO HEAD OUTDIR WORKDIR JOBS [ID...]"""
import concurrent.futures as cf, os, re, shutil, subprocess, sys, json
from pathlib import Path

RTL = "hdl/packet_engine/KL_pp_nvm_port.sv"
SIM = "tb/nvm_port/sim_main.cpp"
MK = "tb/nvm_port/Makefile"
SHADOW = "hdl/acmp/KL_acmp_nvm_shadow.sv"
M = {  # handshake/array model toggles in the harness (README model table)
    "pristine": [],
    "silent": [(SIM, "  bool silent_model = false;", "  bool silent_model = true;")],
    "short": [(SIM, "  bool short_model = false;", "  bool short_model = true;")],
    "unsol": [(SIM, "  bool unsol_model = false;", "  bool unsol_model = true;")],
    "coinc": [(SIM, "  bool done_on_last_byte = false;", "  bool done_on_last_byte = true;")],
}
RT_ANCHOR = "  every_operation_got_what_it_was_owed();\n\n  printf"
def tmo(n):
    return [(SIM, "constexpr int TMO       = 100;", f"constexpr int TMO       = {n};"),
            (MK, "-GMEM_TIMEOUT_CYC_P=100", f"-GMEM_TIMEOUT_CYC_P={n}")]

P = {}  # id -> (suite, description, edits)
def p(i, desc, edits, suite="nvm_port"): P[i] = (suite, desc, edits)

p("W1", "verdict one cycle early (tmo_hit at TMO-1)",
  [(RTL, "(tmo_r == TMO_W_C'(MEM_TIMEOUT_CYC_P));", "(tmo_r == TMO_W_C'(MEM_TIMEOUT_CYC_P - 1));")])
p("W2", "verdict one cycle late (tmo_hit at TMO+1)",
  [(RTL, "(tmo_r == TMO_W_C'(MEM_TIMEOUT_CYC_P));", "(tmo_r == TMO_W_C'(MEM_TIMEOUT_CYC_P + 1));")])
p("W3", "an unowned done counts as progress",
  [(RTL, "|| (dev_done_i && (dev_cmd_owned_w || owed_r))", "|| dev_done_i")])
p("W4", "manager write stall charged to the device (S_WDPUMP owed without wvalid)",
  [(RTL, "|| ((state_r == S_WDPUMP) && nvm_wvalid_i)", "|| (state_r == S_WDPUMP)")])
p("W4b", "manager write stall charged to the device (S_WDPUMP owed without wvalid)",
  [(RTL, "|| ((state_r == S_WDPUMP) && nvm_wvalid_i)\n                  || ((state_r == S_RPPUMP) && nvm_rready_i);",
         "|| (state_r == S_WDPUMP)\n                  || ((state_r == S_RPPUMP) && nvm_rready_i);")])
p("X1", "#19.1 low magic byte check removed", [(RTL, "(hdr_r[1] == MAGIC_LO_C)", "1'b1")])
p("X2", "#19.2 payload bound weakened to <", [(RTL, "(hdr_plen_w <= MAXP_C)", "(hdr_plen_w < MAXP_C)")])
p("X3", "#19.3/#21 latch deleted", [(RTL, "      if (dev_done_i && dev_cmd_owned_w) done_seen_r <= 1'b1;\n", "")])
p("X4", "#14/#21 latch armed in every state", [(RTL, "      if (dev_done_i && dev_cmd_owned_w) done_seen_r <= 1'b1;", "      if (dev_done_i) done_seen_r <= 1'b1;")])
p("X5", "#19.4/#21 header short-read defence off", [(RTL, "            if (done_seen_r || (dev_done_i && !(dev_rvalid_i && (hidx_r == 3'd7)))) begin", "            if (1'b0) begin")])
p("H0", "no defect (head RTL)", [])
p("W5", "manager read stall charged to the device (S_RPPUMP owed without rready)",
  [(RTL, "|| ((state_r == S_RPPUMP) && nvm_rready_i);", "|| (state_r == S_RPPUMP);")])
p("W6", "count held (not cleared) across unowed cycles: accumulates, not 'in a row'",
  [(RTL, "else if (!owe_w || prog_w) tmo_r <= '0;",
         "else if (prog_w || (state_r == S_IDLE)) tmo_r <= '0;\n    else if (!owe_w) tmo_r <= tmo_r;")])
p("W7", "deadline in an owned state leaves nothing owed",
  [(RTL, "end else if (dl_w && dev_cmd_owned_w) begin\n        owed_r <= 1'b1;\n      ", "")])
p("W8", "late registered grant after a deadline not owed",
  [(RTL, "end else if (lg_r && dev_gnt_i && !dev_done_i && !dev_err_i) begin", "end else if (1'b0) begin")])
p("W9", "late grant owed even when its terminal rides it",
  [(RTL, "lg_r && dev_gnt_i && !dev_done_i && !dev_err_i", "lg_r && dev_gnt_i")])
p("W10", "quarantine released by time: a later deadline clears the owed command",
  [(RTL, "if (dev_done_i || dev_err_i) owed_r <= 1'b0;", "if (dev_done_i || dev_err_i || dl_w) owed_r <= 1'b0;")])
p("W11", "owed command ended only by done, never by err",
  [(RTL, "if (dev_done_i || dev_err_i) owed_r <= 1'b0;", "if (dev_done_i) owed_r <= 1'b0;")])
p("W12", "owed READ never drained",
  [(RTL, "|| (owed_r && owed_rd_r);", ";")])
p("W13", "owed kind overwritten by a later deadline (drain stops)",
  [(RTL, "if (dl_w && !owed_r) owed_rd_r <= rd_st_w;", "if (dl_w) owed_rd_r <= rd_st_w;")])
p("W14", "device request not gated by the owed command",
  [(RTL, "assign dev_req_o    = req_st_w && !owed_r;", "assign dev_req_o    = req_st_w;")])
p("W15", "S_RHREQ not gated by owed: the owed command's err credited to the new restore",
  [(RTL, "S_RHREQ: if (!owed_r) begin", "S_RHREQ: begin")])
p("W15b", "S_WEREQ not gated by owed: the owed command's err credited to the new commit",
  [(RTL, "S_WEREQ: if (!owed_r) begin", "S_WEREQ: begin")])
p("W16", "drained owed-READ bytes are not progress",
  [(RTL, "|| (dev_rvalid_i && dev_rready_o);", "|| (dev_rvalid_i && dev_rready_o && !owed_r);")])
p("W17", "verdict never ends S_RPWAIT",
  [(RTL, "if (dl_w) begin\n        err_r   <= 1'b1;", "if (dl_w && (state_r != S_RPWAIT)) begin\n        err_r   <= 1'b1;")])
p("W18", "S_RHWAIT not owed (no deadline on a missing header-read terminal)",
  [(RTL, "|| (state_r == S_RHWAIT) || (state_r == S_RPWAIT)\n                  || (state_r == S_WHPUMP)",
         "|| (state_r == S_RPWAIT)\n                  || (state_r == S_WHPUMP)")])
p("W19", "DEADLINE reported as cause DEVICE",
  [(RTL, "cause_r <= CAUSE_DEADLINE_C;", "cause_r <= CAUSE_DEVICE_C;")])
p("W20", "busy held while a command is owed",
  [(RTL, "assign nvm_busy_o   = (state_r != S_IDLE) && (state_r != S_FIN);",
         "assign nvm_busy_o   = ((state_r != S_IDLE) && (state_r != S_FIN)) || owed_r;")])
p("W21", "refusal (d) off in S_WDPUMP",
  [(RTL, "end else if (done_seen_r || (dev_done_i\n                       && !(nvm_wvalid_i && dev_wready_i && (bcnt_r == (plen_r - 16'd1)))))",
         "end else if (1'b0)")])
p("W22", "refusal (d) off in S_RPPUMP",
  [(RTL, "end else if (done_seen_r || (dev_done_i\n                       && !(dev_rvalid_i && nvm_rready_i && (bcnt_r == (plen_r - 16'd1)))))",
         "end else if (1'b0)")])
p("W23", "refusal (d) off in S_WHPUMP",
  [(RTL, "end else if (done_seen_r || (dev_done_i\n                       && !(dev_wready_i && (hidx_r == 3'd7) && (plen_r == 16'd0)))) begin",
         "end else if (1'b0) begin")])
p("W24", "S_RPWAIT dropped from the ownership window (deadline there leaves nothing owed)",
  [(RTL, "|| (state_r == S_RPPUMP) || (state_r == S_RPWAIT);\n\n  // ---- the deadline", "|| (state_r == S_RPPUMP);\n\n  // ---- the deadline")])
p("W25", "verdict ignores an event in the verdict cycle",
  [(RTL, "assign dl_w = owe_w && !prog_w && tmo_hit_w;", "assign dl_w = owe_w && tmo_hit_w;")])
p("W26", "deadline never fires (watchdog removed)",
  [(RTL, "assign dl_w = owe_w && !prog_w && tmo_hit_w;", "assign dl_w = 1'b0;")])
p("W27", "owed command's terminal released while a new request is in the REQ state only (owed cleared on dl only in REQ)",
  [(RTL, "if (dev_done_i || dev_err_i) owed_r <= 1'b0;", "if (dev_done_i || dev_err_i || (dl_w && req_st_w)) owed_r <= 1'b0;")])
# parametric variants, no defect
p("V37", "harness and port at MEM_TIMEOUT_CYC_P=37 (no defect)", tmo(37))
p("V1000", "harness and port at MEM_TIMEOUT_CYC_P=1000 (no defect)", tmo(1000))
# acmp_nvm probes
p("A1", "binding manager reads a zero-byte DEADLINE as blank",
  [(SHADOW, "&& (nvm_err_cause_i != CAUSE_UNFRAMED_C);", "&& (nvm_err_cause_i == 2'd1);"),
   (SHADOW, "                         && (nvm_err_cause_i == CAUSE_UNFRAMED_C))", "                         && (nvm_err_cause_i != 2'd1))")], suite="acmp_nvm")
p("A2", "binding manager's crc16 term forced true (torn record accepted)",
  [(SHADOW, "&& (rcrc_acc_r == rcrc_rx_r);", "&& 1'b1;")], suite="acmp_nvm")
p("A3", "port deadline removed (acmp_nvm both builds)",
  [(RTL, "assign dl_w = owe_w && !prog_w && tmo_hit_w;", "assign dl_w = 1'b0;")], suite="acmp_nvm")
p("A4", "port deadline leaves nothing owed (acmp_nvm)",
  [(RTL, "end else if (dl_w && dev_cmd_owned_w) begin\n        owed_r <= 1'b1;\n      ", "")], suite="acmp_nvm")


RTEST_CODE = r"""  { // [R436] reviewer-owned directed checks on the owed command (not part of the PR)
    // (a) the owed READ ended by the device's ERR while a later restore waits
    fresh_reset();
    h.deadline_ok = true;
    const std::vector<uint8_t> rr = frame(2, pattern(40, 0x31));
    CHECK(h.commit(2, rr) == 0, "R436a setup: region 2 committed");
    int rc = silenced(false, rr, SIL_BYTE, 1, -1, 10);
    CHECK(rc == 1 && h.last_cause == 3 && h.d_busy, "R436a setup: payload READ abandoned, owed");
    h.clear_capture(); h.ops.clear(); h.m_mode = 2; h.m_stall = 0; h.start(false, 2);
    for (int i = 0; i < 20; ++i) h.tick();
    h.end_command_now(true);
    rc = h.run_op();
    CHECK(rc == 0 && h.err_pulses == 0 && h.rbytes == rr && h.ops.size() == 2,
          "R436a owed READ ended by err while a restore waits in S_RHREQ: credited to no operation, the restore is served (rc %d cause %d ops %zu)",
          rc, h.last_cause, h.ops.size());
    // (b) the owed ERASE ended by the device's ERR while a later commit waits
    rc = silenced(true, rr, SIL_DONE, 0, -1);
    CHECK(rc == 1 && h.last_cause == 3 && h.d_busy, "R436b setup: ERASE abandoned, owed");
    h.clear_capture(); h.ops.clear(); h.m_mode = 1; h.m_wbytes = rr; h.m_widx = 0; h.m_stall = 0; h.start(true, 2);
    for (int i = 0; i < 30; ++i) h.tick();
    h.end_command_now(true);
    rc = h.run_op();
    CHECK(rc == 0 && h.err_pulses == 0 && h.sent == rr && h.ops.size() == 2,
          "R436b owed ERASE ended by err while a commit waits in S_WEREQ: credited to no operation, the commit is served (rc %d cause %d ops %zu)",
          rc, h.last_cause, h.ops.size());
    // (c) an owed READ that keeps dribbling bytes (one per TMO/2) holds a waiting restore's deadline off
    h.rstall = TMO / 2;
    rc = silenced(false, rr, SIL_BYTE, 1, TMO + 1, 10);
    CHECK(rc == 1 && h.last_cause == 3 && h.d_busy, "R436c setup: slow payload READ abandoned at byte 10, owed");
    const long t0 = h.cycles;
    h.ops.clear();
    rc = h.restore(2);
    const long took = h.cycles - t0;
    h.rstall = 0;
    CHECK(rc == 0 && h.rbytes == rr && took > 4 * TMO,
          "R436c a waiting restore is never refused while the owed READ's drained bytes keep moving: served after %ld cycles (rc %d cause %d)",
          took, rc, h.last_cause);
    h.deadline_ok = false;
  }
"""

M["rtest"] = [(SIM, RT_ANCHOR, RTEST_CODE + RT_ANCHOR)]

def combos():
    out = []
    for i, (suite, desc, ed) in P.items():
        models = ["pristine"] if suite == "acmp_nvm" else ["pristine"]
        if i.startswith("V"): models = ["pristine", "silent", "short", "unsol", "coinc"]
        if i in ("W3",): models += ["unsol"]
        if i in ("W12", "W13", "W16", "W14", "W7", "W10", "W26"): models += ["silent"]
        if i in ("W21", "W22", "W23"): models += ["short", "coinc"]
        if i == "X3": models = ["pristine", "coinc"]
        if i == "X4": models = ["pristine", "unsol"]
        if i == "X5": models = ["pristine", "short"]
        if i in ("H0", "W15", "W15b", "W16", "W6", "W11", "W12", "W14", "W10"): models = ["rtest"]
        for m in models: out.append((i, m))
    return out

def run(repo, head, outdir, work, pid, model):
    suite, desc, edits = P[pid]
    tag = f"{pid}__{model}"
    d = Path(work) / tag
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    subprocess.run(f"git -C {repo} archive {head} | tar -x -C {d}", shell=True, check=True)
    log = Path(outdir) / f"{tag}.log"
    applied = []
    for f, old, new in edits + M[model]:
        fp = d / f; t = fp.read_text(); n = t.count(old)
        if n != 1:
            log.write_text(f"ANCHOR {f} occurs {n} times: {old!r}\n"); return tag, "ANCHOR", None
        fp.write_text(t.replace(old, new, 1)); applied.append(f)
    env = dict(os.environ, PATH="$VALIDATION_TOOLS/pinned-verilator-5.050:" + os.environ["PATH"])
    tgt = "run"
    pr = subprocess.run(["make", "-s", "-C", str(d / "tb" / suite), tgt], env=env,
                        capture_output=True, text=True, timeout=1800)
    txt = pr.stdout + pr.stderr
    tallies = re.findall(r"(\d+) checks: (\d+) PASS, (\d+) FAIL", txt)
    fails = [l for l in txt.splitlines() if l.startswith("FAIL") or "FAIL:" in l[:12]]
    elab = [l for l in txt.splitlines() if l.startswith(("ELAB", "GUARD"))]
    log.write_text(f"# probe {pid} model {model}: {desc}\n# rc {pr.returncode}\n"
                   + "\n".join(f"# tally {a} {b} {c}" for a, b, c in tallies) + "\n"
                   + "\n".join(elab) + "\n" + "\n".join(fails) + "\n# ---- tail\n" + txt[-3000:])
    last = tallies[-1] if tallies else None
    shutil.rmtree(d, ignore_errors=True)
    return tag, pr.returncode, last

if __name__ == "__main__":
    repo, head, outdir, work, jobs = sys.argv[1:6]
    want = set(sys.argv[6:])
    todo = [c for c in combos() if not want or c[0] in want]
    res = {}
    with cf.ThreadPoolExecutor(int(jobs)) as ex:
        futs = {ex.submit(run, repo, head, outdir, work, i, m): (i, m) for i, m in todo}
        for f in cf.as_completed(futs):
            tag, rc, last = f.result(); res[tag] = (rc, last)
            print(tag, rc, last, flush=True)
    summ = Path(outdir) / "SUMMARY.tsv"
    with summ.open("a") as fh:
        for tag in sorted(res):
            rc, last = res[tag]; i = tag.split("__")[0]
            fh.write(f"{tag}\t{rc}\t{' '.join(last) if last else '-'}\t{P[i][1]}\n")
