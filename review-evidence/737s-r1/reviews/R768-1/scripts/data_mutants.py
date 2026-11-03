#!/usr/bin/env python3
"""Receipt-level plants on real passing LiteX leg receipts; each judged by the union CLI and
the elaborate aggregate verifier CLI.
usage: data_mutants.py <clone> <base-e2e-dir> <outdir>"""
import copy, json, os, shutil, subprocess, sys
from pathlib import Path
clone, base, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
H = Path(__file__).resolve().parent
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=clone, text=True).strip()
tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=clone, text=True).strip()
good = {i: json.loads((base / "legs" / f"litex-leg-{i}.json").read_text()) for i in range(3)}
def row(leg, name): return next(r for r in good[leg]["results"] if r["simulation"] == name)
PLANTS = []
def plant(label, fn): PLANTS.append((label, fn))
def edit(fn):
    def apply():
        g = copy.deepcopy(good); fn(g); return g
    return apply
plant("D1 row removed from leg 1 (PR's quoted example)", edit(lambda g: g[1]["results"].remove(row(1, "test_pp_boot_bus_freeze"))))
plant("D2 row moved from leg 1 to leg 2", edit(lambda g: (g[1]["results"].remove(row(1, "test_pp_mem_bridge")), g[2]["results"].append(row(1, "test_pp_mem_bridge")))))
plant("D3 row copied into a second leg", edit(lambda g: g[2]["results"].append(row(0, "test_soc_timing_cuts"))))
plant("D4 leg 2 receipt lost", edit(lambda g: g.pop(2)))
plant("D5 leg 0 receipt duplicated (as leg 0 twice)", edit(lambda g: g.__setitem__(3, copy.deepcopy(g[0]))))
plant("D6 receipt from another head", edit(lambda g: g[0].update(head="0" * 40)))
plant("D7 selection and rows both narrowed in leg 2", edit(lambda g: (g[2]["selected"].remove("test_ctrl_memory"), g[2]["results"].remove(row(2, "test_ctrl_memory")))))
plant("D8 exit given as false (bool)", edit(lambda g: g[0].update(exit=False)))
plant("D9 verdict lower-case pass", edit(lambda g: g[0]["results"][0].update(verdict="pass")))
results = []
for label, fn in PLANTS:
    key = label.split()[0]; d = out / key; shutil.rmtree(d, ignore_errors=True); (d / "legs").mkdir(parents=True)
    for i, receipt in fn().items():
        (d / "legs" / f"litex-leg-{i}.json").write_text(json.dumps(receipt) + "\n")
    files = sorted(str(p) for p in (d / "legs").glob("*.json"))
    u = subprocess.run(["python3", "scripts/ci_litex_legs.py", "union", "--head", head, "--tree", tree, *files],
                       cwd=clone, capture_output=True, text=True)
    # aggregate root: leg i -> worker 2+i, a fourth receipt goes beside worker 3's
    lit = d / "lit"; lit.mkdir()
    needs = subprocess.run(["python3", str(H / "mk_gate_root.py"), str(clone), str(lit), str(d / "root")],
                           capture_output=True, text=True).stdout
    for f in files:
        i = int(Path(f).stem.rsplit("-", 1)[1]); w = 2 + (i if i < 3 else 1)
        name = f"litex-leg-{i if i < 3 else 0}.json"; target = d / "root" / f"gate-elaborate-{w}" / ("x" if i == 3 else "")
        target.mkdir(parents=True, exist_ok=True); shutil.copy(f, target / name)
    v = subprocess.run(["python3", "scripts/ci_gate_receipts.py", "verify", "--workflow", "elaborate", "--root",
                        str(d / "root"), "--head", head], cwd=clone, capture_output=True, text=True,
                       env=dict(os.environ, CI_GATE_NEEDS=needs))
    r = {"plant": label, "union_rc": u.returncode, "union": (u.stderr + u.stdout).strip().splitlines()[0][:200],
         "verify_rc": v.returncode, "verify": (v.stderr + v.stdout).strip().splitlines()[0][:200]}
    results.append(r); print(json.dumps(r))
(out / "data-mutants.json").write_text(json.dumps(results, indent=1) + "\n")
