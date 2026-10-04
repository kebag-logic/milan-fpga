#!/usr/bin/env python3
"""R462-3 disposable mutation probes. Each probe copies the exact-head tree
(scratch/head, a `git archive` of c725be1), replaces ONE exact source line,
builds and runs one suite, and records the rc and tally lines.

Usage: probe.py PACKET VERILATOR JOBS [NAME ...]
"""
import concurrent.futures, json, shutil, subprocess, sys
from pathlib import Path

TOP = "hdl/top/protocol_processor_top.sv"
LSN = "hdl/acmp/KL_pp_acmp_listener.sv"
AQ = ("tb/pp_top", "make gsi-build VERILATOR={v} && ./obj_dir/Vpp_top_sim --arm-queue-only")
LS = ("tb/acmp_listener", "make run VERILATOR={v}")
RING_STORE = "      if (armq_push_ok_w[g]) mem_r[wr_ix_w] <= armq_in_w[g];\n"
RING_READ = "    assign armq_hd_w[g] = mem_r[armq_hd_r[g]];\n"
HD_RESET = "      armq_hd_r  <= '0;\n"
DROP_IF = "        if (armq_in_vld_w[i] && !armq_push_ok_w[i]) begin\n"
SWEEP = "  assign recwr_en_w   = ((xs_r == X_INIT) && (init_cnt_r < (SINK_W_C+1)'(N_SINKS_P)))\n"
REC_READ = "  assign rec_rd_w     = acmp_rec_t'(rec_ram_r[sink_r]);\n"

# name: (suite, file, old, new, expectation)
PROBES = {
  # kill expected: a push lost whenever its own face pops in the same clock
  "ring_pop_blocks_write": (AQ, TOP, RING_STORE,
      "      if (armq_push_ok_w[g] && !armq_pop_w[g]) mem_r[wr_ix_w] <= armq_in_w[g];\n", "KILL"),
  # kill expected: a full face reads one entry past its head
  "ring_full_reads_next": (AQ, TOP, RING_READ,
      "    assign armq_hd_w[g] = mem_r[armq_hd_r[g] + 2'(armq_cnt_r[g] == 3'd4)];\n", "KILL"),
  # kill expected: the stored arm is the next face's
  "ring_stores_neighbour": (AQ, TOP, RING_STORE,
      "      if (armq_push_ok_w[g]) mem_r[wr_ix_w] <= armq_in_w[(g + 1) % ARM_N_C];\n", "KILL"),
  # kill expected: drops on the notify monitor face are not counted
  "drop_ignores_face7": (AQ, TOP, DROP_IF,
      "        if (armq_in_vld_w[i] && !armq_push_ok_w[i] && (i != 7)) begin\n", "KILL"),
  # equivalent expected: the ring is head-relative and cnt resets, so the
  # head index's reset value is unobservable
  "ring_hd_not_reset": (AQ, TOP, HD_RESET, "      // armq_hd_r not reset (probe)\n", "PASS"),
  # equivalent expected: outside X_INIT the write address is sink_r
  "rec_read_at_write_addr": (LS, LSN, REC_READ,
      "  assign rec_rd_w     = acmp_rec_t'(rec_ram_r[recwr_addr_w]);\n", "PASS"),
  # kill wanted: the X_INIT sweep skips the last sink (RS's own claim)
  "sweep_skips_last_sink": (LS, LSN, SWEEP,
      "  assign recwr_en_w   = ((xs_r == X_INIT) && (init_cnt_r < (SINK_W_C+1)'(N_SINKS_P - 1)))\n",
      "KILL"),
  # kill wanted: the X_INIT sweep skips sink 0
  "sweep_skips_sink0": (LS, LSN, SWEEP,
      "  assign recwr_en_w   = ((xs_r == X_INIT) && (init_cnt_r < (SINK_W_C+1)'(N_SINKS_P)) && (init_cnt_r != 0))\n",
      "KILL"),
}

def run(name, pkt, v):
    (sdir, cmd), f, old, new, want = PROBES[name]
    src = Path(pkt, "scratch/head"); dst = Path(pkt, "scratch/probes", name)
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("obj_*"))
    p = dst / f; text = p.read_text()
    assert text.count(old) == 1, (name, "anchor not unique")
    p.write_text(text.replace(old, new))
    log = Path(pkt, "receipts/probes", name + ".log"); log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "w") as fh:
        fh.write(f"# probe {name}: {f}\n# - {old}# + {new}")
        fh.flush()
        rc = subprocess.run(cmd.format(v=v), shell=True, cwd=dst / sdir, stdout=fh,
                            stderr=subprocess.STDOUT).returncode
    out = log.read_text()
    tally = [l for l in out.splitlines() if "checks" in l and ("PASS" in l or "failures" in l)][-3:]
    fails = [l for l in out.splitlines() if l.startswith("FAIL")][:5]
    got = "PASS" if rc == 0 else "KILL"
    shutil.rmtree(dst)
    return {"probe": name, "file": f, "rc": rc, "verdict": got, "expected": want,
            "as_expected": got == want, "tally": tally, "first_fails": fails}

if __name__ == "__main__":
    pkt, v, jobs = sys.argv[1], sys.argv[2], int(sys.argv[3])
    names = sys.argv[4:] or list(PROBES)
    with concurrent.futures.ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda n: run(n, pkt, v), names))
    Path(pkt, "receipts/probes.json").write_text(json.dumps(res, indent=1) + "\n")
    for r in res: print(json.dumps(r))
    sys.exit(0 if all(r["as_expected"] for r in res) else 1)
