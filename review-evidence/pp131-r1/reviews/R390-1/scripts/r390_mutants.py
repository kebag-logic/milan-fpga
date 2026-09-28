#!/usr/bin/env python3
"""Reviewer mutants for PR #132 at the exact head. Each mutant is planted in
a fresh git-archive copy, the pp_top bench is built with the given Verilator
and the D3 section is run (--d3-only). KILLED = build ok and the run fails;
SURVIVED = build ok and every D3 check passes. Usage:
  r390_mutants.py <clone> <scratch> <verilator> [name ...]"""
import subprocess, sys, pathlib, shutil, concurrent.futures as cf

HEAD = "e1ae468f7e237f321ce5fee19e59ae157da4b83d"
W = "hdl/aecp/KL_aecp_nvm_writer.sv"
MUTANTS = {
    # contract 6.1: "BACKOFF holds neither the state bus nor the port"
    "backoff_holds_dispatch": (W,
        "assign own_o = !done_r || (ss_r == S_ACQ) || latch_w;",
        "assign own_o = !done_r || (ss_r == S_ACQ) || latch_w || (ss_r == S_BACKOFF);"),
    # contract 6.2/6.3: a record whole in ONE pass and not the other aborts;
    # this mutant only aborts whole-then-blank, never blank-then-whole
    "disagree_one_direction": (W,
        "&& (rd_whole_w != whole0_r[rec_r]);",
        "&& (!rd_whole_w && whole0_r[rec_r]);"),
    # contract 6.2: rb_rst held for two cycles at least
    "rollback_one_cycle": (W,
        "if (rb_min_r && !desc_debt_i) ws_r <= W_RELOC;",
        "if (!desc_debt_i) ws_r <= W_RELOC;"),
}

def run(name, clone, scratch, vl):
    path, old, new = MUTANTS[name]
    out = pathlib.Path(scratch) / name
    shutil.rmtree(out, ignore_errors=True); out.mkdir(parents=True)
    tar = subprocess.run(["git", "-C", clone, "archive", HEAD], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(out)], input=tar, check=True)
    f = out / path; s = f.read_text()
    assert s.count(old) == 1, f"{name}: anchor"
    f.write_text(s.replace(old, new))
    tb = out / "tb/pp_top"
    b = subprocess.run(["make", "gsi-build", f"VERILATOR={vl}"], cwd=tb, capture_output=True, text=True)
    if b.returncode != 0:
        return f"{name}: BUILD FAILED rc={b.returncode} (REFUSED)"
    (tb / "obj_dir").mkdir(exist_ok=True)
    r = subprocess.run(["./obj_dir/Vpp_top_sim", "--d3-only"], cwd=tb, capture_output=True, text=True)
    (out / "run.log").write_text(r.stdout + r.stderr)
    fails = [l for l in r.stdout.splitlines() if "FAIL" in l][:3]
    tally = [l for l in r.stdout.splitlines() if l.startswith("D3:")]
    verdict = "KILLED" if r.returncode != 0 else "SURVIVED"
    return f"{name}: {verdict} run rc={r.returncode} {tally} first fails: {fails}"

if __name__ == "__main__":
    clone, scratch, vl = sys.argv[1:4]
    names = sys.argv[4:] or list(MUTANTS)
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for line in ex.map(lambda n: run(n, clone, scratch, vl), names):
            print(line, flush=True)
