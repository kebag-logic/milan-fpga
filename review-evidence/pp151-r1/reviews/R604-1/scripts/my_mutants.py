#!/usr/bin/env python3
"""Reviewer-owned mutants of the head's guards, each in its own scratch copy.

Each mutant is graded twice: by the head's own bench (guards.py --only <guard>)
and directly by the tools (Verilator lint with scripts/lint_hdl.sh's flags, and
sv2v + Yosys with the syn/yosys/run.sh elaboration), so the kill does not rest
on the bench's own reading. Usage: my_mutants.py <head-tree> <workdir> <bin12> <bin13>
"""
import os, re, shutil, subprocess, sys
from pathlib import Path

HEAD, WORK, B12, B13 = (Path(a).resolve() for a in sys.argv[1:5])
LINT = ["--lint-only", "-Wall", "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL", "-Wno-UNUSEDPARAM"]

MUTANTS = [
    # name, file, old, new, guard, top, params
    ("R1-encoder-error", "hdl/srp/KL_srp_encoder.sv",
     '    $fatal(1, "DEPTH_P drain', '    $error("DEPTH_P drain',
     "KL_srp_encoder.g_depth_check", "KL_srp_encoder", [("DEPTH_P", 13)]),
    ("R2-ucpu-warning", "hdl/aecp/KL_aecp_ucpu.sv",
     '    $fatal(1, "RESP_D8_CAP_BYTES_P', '    $warning("RESP_D8_CAP_BYTES_P',
     "KL_aecp_ucpu.gen_g_d8_cap", "KL_aecp_ucpu", [("RESP_D8_CAP_BYTES_P", 1025)]),
    ("R3-merge-initial-block", "hdl/packet_engine/KL_pp_release_merge.sv",
     '  if (N_SLOTS_P < 1) begin : g_slot_count_check\n    $fatal(1, "KL_pp_release_merge: N_SLOTS_P must be positive");\n  end',
     '  initial begin : g_slot_count_check\n    if (N_SLOTS_P < 1)\n      $fatal(1, "KL_pp_release_merge: N_SLOTS_P must be positive");\n  end',
     "KL_pp_release_merge.g_slot_count_check", "KL_pp_release_merge", [("N_SLOTS_P", 0)]),
    ("R4-writer-info", "hdl/aecp/KL_aecp_nvm_writer.sv",
     '    $fatal(1, "KL_aecp_nvm_writer: RS_AGG_CYC_P', '    $info("KL_aecp_nvm_writer: RS_AGG_CYC_P',
     "KL_aecp_nvm_writer.g_rs_agg_check", "KL_aecp_nvm_writer", [("RS_AGG_CYC_P", 0)]),
    ("R5-top-owner-error", "hdl/top/protocol_processor_top.sv",
     '    $fatal(1, "F08.4: owner tags OVERLAP', '    $error("F08.4: owner tags OVERLAP',
     "protocol_processor_top.gen_g_owner_overlap", "protocol_processor_top",
     [("N_STREAM_IN_P", 16), ("N_STREAM_OUT_P", 17)]),
]


def run(cmd, cwd, path):
    env = dict(os.environ, PATH=f"{path}:{os.environ['PATH']}")
    r = subprocess.run(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, errors="replace")
    return r.returncode, r.stdout


def first(out, pat):
    for line in out.splitlines():
        if re.search(pat, line):
            return line.strip()[:200]
    return "-"


def sources(tree):
    pk = sorted(str(p.relative_to(tree)) for p in (tree / "hdl").rglob("*_pkg.sv"))
    rest = sorted(str(p.relative_to(tree)) for p in (tree / "hdl").rglob("*.sv") if not p.name.endswith("_pkg.sv"))
    return pk + rest


def main():
    WORK.mkdir(parents=True, exist_ok=False)
    for name, f, old, new, guard, top, params in MUTANTS:
        tree = WORK / name
        shutil.copytree(HEAD, tree, ignore=shutil.ignore_patterns(".git"))
        text = (tree / f).read_text()
        assert text.count(old) == 1, (name, "plant not unique")
        (tree / f).write_text(text.replace(old, new))
        print(f"=== {name}: {f} planted ({guard})")
        g = f"-G" 
        rc, out = run(["verilator", *LINT, "--top-module", top, *(f"-G{k}={v}" for k, v in params),
                       *sources(tree)], tree, B12)
        print(f"  direct verilator lint rc={rc}: {first(out, r'^%')}")
        for tag, b in (("0.0.12", B12), ("0.0.13", B13)):
            w = tree / f"yosys-{tag}"; w.mkdir()
            with open(w / "all.v", "w") as fh:
                subprocess.run(["sv2v", *sources(tree)], cwd=tree, stdout=fh, check=True,
                               env=dict(os.environ, PATH=f"{b}:{os.environ['PATH']}"))
            subprocess.run([sys.executable, "gen_ucode.py", "-o", str(w / "ucode.hex")], cwd=tree / "hdl/aecp/ucode", stdout=subprocess.DEVNULL, check=True)
            subprocess.run([sys.executable, "gen_ltn_rom.py", "-o", str(w / "ltn_rom.hex")], cwd=tree / "hdl/acmp/rom", stdout=subprocess.DEVNULL, check=True)
            sets = " ".join(f"-set {k} {v}" for k, v in params)
            rc, out = run(["yosys", "-q", "-p", f"read_verilog -defer all.v; chparam {sets} {top}; hierarchy -check -top {top}; proc; opt_clean"], w, b)
            print(f"  direct sv2v {tag} + yosys rc={rc} ({'ELABORATES' if rc == 0 else 'refused'}): {first(out, r'ERROR|Warning')}")
        for tag, b in (("0.0.12", B12), ("0.0.13", B13)):
            rc, out = run([sys.executable, "-B", str(tree / "tb/elab_guards/guards.py"), "--root", str(tree),
                           "--verilator", "verilator", "--only", guard, "--jobs", "2"], tree / "tb/elab_guards", b)
            fails = [l for l in out.splitlines() if l.startswith("FAIL:")]
            named = [l for l in fails if guard in l]
            verdict = "KILLED" if rc != 0 and named else "SURVIVED"
            print(f"  bench (sv2v {tag}) rc={rc} {verdict}; tally: {first(out, 'elab guards:')}")
            for l in named:
                print(f"    {l[:220]}")
        shutil.rmtree(tree / "yosys-0.0.12"); shutil.rmtree(tree / "yosys-0.0.13")


main()
