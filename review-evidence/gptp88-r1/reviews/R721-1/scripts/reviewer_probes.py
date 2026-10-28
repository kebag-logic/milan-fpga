"""Reviewer-owned disposable mutants for FPGA-gPTP #87/#88, outside the shipped arms.

usage: python3 reviewer_probes.py <tree> <outdir> <jobs>
Each probe is planted alone into a temporary copy (the engine arm's own
stage/build/generate_image/run_harness) and the engine suite (shipping pass +
priority1 255 pass) is run; the parser probes are also run against the parser
suite. Records rc, tally and every FAIL line per probe. Nothing in <tree> is
written.
"""
import importlib.util, subprocess, sys, tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

tree, outdir, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), int(sys.argv[3])
def load(name, rel):
    s = importlib.util.spec_from_file_location(name, tree / rel)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
E = load("engine_mutants", "tb/verilator/engine/mutants.py")
PM = load("parser_mutants", "tb/verilator/parser/mutants.py")
WORK = Path(tempfile.mkdtemp(prefix="rprobe-"))
ENG, PAR = "top/KL_gptp_engine.sv", "wire/KL_gptp_rx_parser.sv"
PROBES = [
 ("R1 count written without a TLV (entries kept)", ENG,
  [("                if (ann_pub_present_r) begin\n"
    "                  pub_path_count_r <= path_trace_count_w;\n",
    "                pub_path_count_r <= path_trace_count_w;\n"
    "                if (ann_pub_present_r) begin\n")]),
 ("R2 address-6 self path rewrites entry 0 only (stale entries 1..7)", ENG,
  [("                  pub_path_count_r <= 4'd1;\n"
    "                  pub_path_r       <= self_path_w;\n",
    "                  pub_path_count_r <= 4'd1;\n"
    "                  pub_path_r[63:0] <= rom_clock_id_w;\n")]),
 ("R3 parser presence at bit 62 (engine reads 63)", PAR,
  [("{pt_seen_r, 54'd0, pt_self_r, pt_cnt_r}",
    "{1'b0, pt_seen_r, 53'd0, pt_self_r, pt_cnt_r}")]),
 ("R4 parser reports an empty TLV as absent", PAR,
  [("{pt_seen_r, 54'd0, pt_self_r, pt_cnt_r}",
    "{pt_seen_r && (pt_cnt_r != 8'd0), 54'd0, pt_self_r, pt_cnt_r}")]),
 ("R5 keep-previous only while the grandmaster is unchanged", ENG,
  [("                if (ann_pub_present_r) begin\n",
    "                if (!ann_pub_present_r && (ann_ctx_r[9] != pub_gm_r)) begin\n"
    "                  pub_path_count_r <= 4'd1;\n"
    "                  pub_path_r       <= self_path_w;\n"
    "                end else if (ann_pub_present_r) begin\n")]),
 ("R6 entry 0 captured from w17 (head dropped, path shifted)", ENG,
  [("          if ((bank_addr_w >= 5'd16) && (bank_addr_w <= 5'd23))\n"
    "            ann_pub_path_r[64*(bank_addr_w-5'd16) +: 64] <= bank_wdata_w;\n",
    "          if ((bank_addr_w >= 5'd17) && (bank_addr_w <= 5'd23))\n"
    "            ann_pub_path_r[64*(bank_addr_w-5'd17) +: 64] <= bank_wdata_w;\n")]),
]

def run_parser(edits, tag):
    src = PM.stage(WORK, "p" + tag, edits)
    exe = PM.build(src, WORK, "p" + tag)
    if exe is None: return "no-build", ""
    rc, out = PM.run_harness(exe)
    return PM.verdict(rc, out), out

def one(a):
    i, (name, fname, edits) = a
    text = (E.HDL / fname).read_text(encoding="utf-8")
    if any(text.count(p) != 1 for p, _ in edits):
        return i, name, "stale-pattern", "", "n/a", ""
    tag = f"r{i}"
    srcdir = E.stage(WORK, tag, (fname, edits))
    rundir = WORK / f"run_{tag}"
    E.generate_image(srcdir, rundir)
    exe = E.build(srcdir, WORK, tag)
    if exe is None:
        return i, name, "no-build", "", "n/a", ""
    rc, out = E.run_harness(exe, rundir)
    ans = E.verdict(rc, out)
    fails = [l for l in out.splitlines() if l.startswith("FAIL ")]
    tally = next((l for l in out.splitlines() if " checks: " in l), "")
    pans, pout = ("n/a", "")
    if fname == PAR:
        pans, pout = run_parser(edits, tag)
    pfails = [l for l in pout.splitlines() if l.startswith("FAIL ")]
    (outdir / f"{name.split()[0]}.log").write_text(
        f"probe: {name}\nengine verdict: {ans}\n{tally}\n" + "\n".join(fails) +
        f"\nparser verdict: {pans}\n" + "\n".join(pfails) + "\n")
    return i, name, ans, tally, pans, len(fails)

if __name__ == "__main__":
    outdir.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=jobs) as ex:
        rows = list(ex.map(one, enumerate(PROBES)))
    with open(outdir / "summary.tsv", "w") as f:
        f.write("probe\tengine_verdict\tengine_tally\tparser_verdict\tengine_fail_lines\n")
        for r in rows:
            f.write(f"{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[5]}\n"); print(r, flush=True)
