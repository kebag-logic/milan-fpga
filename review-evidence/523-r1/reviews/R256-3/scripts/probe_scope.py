#!/usr/bin/env python3
"""Reviewer probe: refusal scope on the real tree, private population, and
missing-facility refusals at both production entry points.

Usage: probe_scope.py SOURCE_CLONE WORKDIR RECEIPT.json
The disposable copy commits a fast `run` stand-in (as in probe_gitenv.py);
all campaign inputs are still verified and copied by the real driver.
"""
import json, os, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_campaign import integrity  # noqa: E402

SOURCE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
RECEIPT = Path(sys.argv[3]).resolve()
CLEAN = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
DRIVER = "tb/verilator/gptp_shadow/mutants.py"

# Removes one facility before the entry point runs (independent of the lane's helper).
SITE = r'''
import os, signal, ctypes
m = os.environ.get("RFACILITY")
if m == "no-pidfd-open" and hasattr(os, "pidfd_open"):
    del os.pidfd_open
elif m == "no-pidfd-send" and hasattr(signal, "pidfd_send_signal"):
    del signal.pidfd_send_signal
elif m == "no-prctl":
    real = ctypes.CDLL
    class NoPrctl:
        def __init__(self, *a, **k):
            pass
    ctypes.CDLL = NoPrctl
'''


def fresh(label):
    base = WORK / label
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    repo = base / "repo"
    shutil.copytree(SOURCE, repo, symlinks=True)
    mk = repo / "tb/verilator/gptp_shadow/Makefile"
    t = mk.read_text()
    old = "run: gptp_ucode.hex\n\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vgptp_shadow_sim\n\t./obj_dir/Vgptp_shadow_sim\n"
    assert old in t
    # The stand-in also records the private population it was built from.
    mk.write_text(t.replace(old, "run:\n\t@cd ../../.. && find . -type f -o -type l | sort > \"$(RPOP)\"\n"
                                 "\t@echo 'FAIL stand-in got 0 exp 1'\n\t@echo '1 checks: 0 PASS, 1 FAIL'\n\t@exit 1\n"))
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=Reviewer probe", "-c", "user.email=probe@example.invalid",
                    "commit", "-qam", "reviewer fast run stand-in"], env=CLEAN, check=True)
    (base / "tmp").mkdir()
    return base, repo


def drive(base, repo, argv, extra=None):
    env = dict(CLEAN, TMPDIR=str(base / "tmp"), PYTHONDONTWRITEBYTECODE="1", RPOP=str(base / "population.txt"))
    env.update(extra or {})
    done = subprocess.run(argv, cwd=repo, env=env, capture_output=True, text=True, timeout=300)
    out = done.stdout + done.stderr
    return done.returncode, out


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    results = []
    # 1. unrelated state proceeds (the R256-2 F3 shapes), on the real tree
    base, repo = fresh("unrelated")
    tr = repo / "hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md"
    tr.write_text(tr.read_text().replace("20", "21", 1))
    aaf = repo / "hdl/ieee1722/aaf/doc/TEST_RESULTS.md"
    aaf.write_text(aaf.read_text() + "\nlocal note\n")
    (repo / "hdl/common/reviewer_untracked.sv").write_text("// untracked\n")
    readme = repo / "tb/verilator/gptp_shadow/README.md"
    readme.write_text(readme.read_text() + "\nstaged local edit\n")
    subprocess.run(["git", "-C", str(repo), "add", "tb/verilator/gptp_shadow/README.md"], env=CLEAN, check=True)
    before = integrity(repo, base / "before.json")
    code, out = drive(base, repo, [sys.executable, DRIVER])
    after = integrity(repo, base / "after.json")
    population = (base / "population.txt").read_text().split() if (base / "population.txt").exists() else []
    declared = subprocess.run(["make", "-s", "--no-print-directory", "print-inputs"], cwd=repo / "tb/verilator/gptp_shadow",
                              capture_output=True, text=True, env=CLEAN).stdout.split()
    declared = sorted({str((repo / "tb/verilator/gptp_shadow" / w).resolve().relative_to(repo)) for w in declared})
    copied = sorted(p[2:] for p in population if not p.startswith("./tb/verilator/gptp_shadow/obj_dir")
                    and not p.endswith("gptp_ucode.hex"))
    results.append(dict(arm="unrelated-state-proceeds", exit=code, controls_line=[l for l in out.splitlines() if l.startswith("controls:")],
                        refused=[l for l in out.splitlines() if l.startswith("REFUSED")], caller_unchanged=before == after,
                        declared_count=len(declared), copied_count=len(copied),
                        copied_minus_declared=sorted(set(copied) - set(declared)),
                        declared_minus_copied=sorted(set(declared) - set(copied)),
                        unrelated_copied=[n for n in copied if n.endswith(("TEST_RESULTS.md", "README.md", "reviewer_untracked.sv"))]))
    # 2. a dirty build input still refuses
    for rel in ("hdl/common/cdc_pulse.sv", "tb/verilator/gptp_shadow/sim_main.cpp", "gptp-processor/hdl/ucpu/KL_gptp_ucpu.sv"):
        base, repo = fresh("dirty-" + Path(rel).name)
        f = repo / rel
        f.write_text(f.read_text() + "\n// local edit\n")
        code, out = drive(base, repo, [sys.executable, DRIVER])
        results.append(dict(arm="dirty-input-refuses:" + rel, exit=code,
                            refused=[l for l in out.splitlines() if l.startswith("REFUSED")],
                            ran=bool([l for l in out.splitlines() if l.startswith("controls:")]),
                            tmp_left=sorted(x.name for x in (base / "tmp").iterdir())))
    # 3. copied (not initialised) dependency, per the old CONTRIBUTING layout
    base, repo = fresh("copied-axis")
    axis = repo / "third_party/verilog-axis"
    (axis / ".git").unlink()
    code, out = drive(base, repo, [sys.executable, DRIVER])
    results.append(dict(arm="copied-dependency-refuses", exit=code, refused=[l for l in out.splitlines() if l.startswith("REFUSED")]))
    # 4. missing facilities at both entry points (a full sweep invocation; it must refuse before any log or command)
    base, repo = fresh("facility")
    site = base / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text(SITE)
    for mode in ("no-prctl", "no-pidfd-open", "no-pidfd-send"):
        for entry, argv in (("campaign", [sys.executable, DRIVER]),
                            ("sweep", ["bash", "scripts/run_all_suites.sh", str(base / ("logs-" + mode))])):
            code, out = drive(base, repo, argv, dict(PYTHONPATH=str(site), RFACILITY=mode))
            results.append(dict(arm=f"facility:{entry}:{mode}", exit=code, traceback="Traceback" in out,
                                refused=[l for l in out.splitlines() if "REFUSED" in l][:1],
                                started=(base / ("logs-" + mode)).exists() if entry == "sweep" else "controls:" in out))
    RECEIPT.write_text(json.dumps(results, indent=1) + "\n")
    for r in results:
        print(json.dumps(r)[:400], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
