#!/usr/bin/env python3
"""R463-2 section AQ probe matrix for processor PR #155 (milan-fpga #639).

usage: aq_matrix.py --trees DIR --r462 R462_SCRIPTS --work DIR --out DIR [--jobs N]

DIR (--trees) holds `git archive` exports named head, r1_9e86991, main_c050d971,
main_07b1469d and base_5c71928a. R462_SCRIPTS is the R462-1 review's published
scripts/ directory (aq_probe.sh and lockstep_armq/gen.py are used unchanged:
aq_probe.sh is executed as published, gen.py's MUTANTS table is imported as
published and each edit is planted once, exact-match, in protocol_processor_top.sv).
`verilator` on PATH must be the pinned 5.050. Each job copies hdl/, tb/common and
tb/pp_top into its own work directory, builds `make gsi-build` and runs
`./obj_dir/Vpp_top_sim --arm-queue-only`; its log and rc go to --out.
"""
import argparse
import concurrent.futures
import importlib.util
import json
import re
import shutil
import subprocess
from pathlib import Path

TOP = "hdl/top/protocol_processor_top.sv"


def load_gen(r462: Path):
    spec = importlib.util.spec_from_file_location("gen", r462 / "lockstep_armq" / "gen.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.MUTANTS


def stage(work: Path, hdl_tree: Path, tb_tree: Path) -> None:
    shutil.rmtree(work, ignore_errors=True)
    (work / "tb").mkdir(parents=True)
    shutil.copytree(hdl_tree / "hdl", work / "hdl")
    shutil.copytree(tb_tree / "tb" / "common", work / "tb" / "common")
    shutil.copytree(tb_tree / "tb" / "pp_top", work / "tb" / "pp_top")


def plant(work: Path, old: str, new: str) -> None:
    p = work / TOP
    s = p.read_text()
    assert s.count(old) == 1, f"planted text occurs {s.count(old)} times"
    p.write_text(s.replace(old, new, 1))


def run_job(job: dict, args) -> dict:
    log = args.out / f"{job['name']}.log"
    work = args.work / job["name"]
    with log.open("w") as stream:
        if job["kind"] == "aq_probe":
            shutil.rmtree(work, ignore_errors=True)
            rc = subprocess.run(["bash", str(args.r462 / "aq_probe.sh"), str(args.trees / "head"),
                                 str(work), job["probe"]], stdout=stream,
                                stderr=subprocess.STDOUT, check=False).returncode
        else:
            stage(work, args.trees / job["hdl"], args.trees / job["tb"])
            if job.get("edit"):
                plant(work, *job["edit"])
            cwd = work / "tb" / "pp_top"
            rc = subprocess.run(["make", "gsi-build"], cwd=cwd, stdout=stream,
                                stderr=subprocess.STDOUT, check=False).returncode
            if rc == 0:
                rc = subprocess.run(["./obj_dir/Vpp_top_sim", "--arm-queue-only"], cwd=cwd,
                                    stdout=stream, stderr=subprocess.STDOUT,
                                    check=False).returncode
            else:
                rc = 1000 + rc
    text = log.read_text(errors="replace")
    keep = [l for l in text.splitlines()
            if l.startswith("AQ") or re.match(r"FAIL: AQ", l) or l.startswith("[build")]
    shutil.rmtree(work, ignore_errors=True)
    return {"name": job["name"], "rc": rc, "expect": job["expect"], "aq_lines": keep}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trees", type=Path, required=True)
    ap.add_argument("--r462", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    args.work.mkdir(parents=True, exist_ok=True)
    gen = load_gen(args.r462)
    jobs = [{"name": "head_clean", "kind": "plant", "hdl": "head", "tb": "head", "expect": "pass"}]
    for p in ("write_refused", "wr_wrap_hi"):
        jobs.append({"name": f"aqprobe_{p}", "kind": "aq_probe", "probe": p, "expect": "fail"})
    for m, edit in gen.items():
        jobs.append({"name": f"gen_{m}", "kind": "plant", "hdl": "head", "tb": "head",
                     "edit": edit, "expect": "pass" if m == "hd_not_reset" else "fail"})
    for ref in ("main_c050d971", "main_07b1469d", "base_5c71928a"):
        jobs.append({"name": f"rtl_{ref}", "kind": "plant", "hdl": ref, "tb": "head",
                     "expect": "pass"})
    for m in ("write_refused", "wr_wrap_hi", "full_pop_refuses", "drop_skip_sat"):
        jobs.append({"name": f"r1bench_{m}", "kind": "plant", "hdl": "r1_9e86991",
                     "tb": "r1_9e86991", "edit": gen[m], "expect": "pass"})
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        results = list(pool.map(lambda j: run_job(j, args), jobs))
    ok = True
    for r in results:
        got = "pass" if r["rc"] == 0 else "fail"
        r["as_expected"] = got == r["expect"]
        ok &= r["as_expected"]
        print(f"{r['name']:<28} rc={r['rc']:<5} expect={r['expect']:<4} "
              f"{'OK' if r['as_expected'] else 'UNEXPECTED'}")
    (args.out / "results.json").write_text(json.dumps(results, indent=1) + "\n")
    print("ALL AS EXPECTED" if ok else "SOME UNEXPECTED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
