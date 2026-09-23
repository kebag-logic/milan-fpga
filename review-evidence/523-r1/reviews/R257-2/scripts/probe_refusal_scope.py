#!/usr/bin/env python3
"""Independent reviewer probe: which caller states refuse the campaign's real
identity/copy step, on a disposable clone with real submodules.

Usage: probe_refusal_scope.py CLONE SCRATCH OUTPUT_JSON

Each arm builds a fresh disposable clone at the exact head (required
submodules initialised at their pins from the clone's local module repos),
plants one state, then runs `private_inputs.copy_inputs` exactly as
`mutants.main` drives it, in a fresh interpreter.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HEAD = "26353960ae2763cc09741d0f7bcc720621bd5148"
CHILD = r'''
import json, sys, tempfile
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
here = repo / "tb/verilator/gptp_shadow"
sys.path.insert(0, str(here)); sys.path.insert(0, str(repo / "scripts"))
import mutants
from owned_process import OwnedProcesses
from private_inputs import InputRefused, copy_inputs
try:
    with OwnedProcesses() as owner:
        with tempfile.TemporaryDirectory() as scratch:
            copy_inputs(repo, here, Path(scratch), owner,
                        {row[1] for row in mutants.MUTATIONS + mutants.NOT_SEPARATELY_OBSERVABLE})
            n = sum(1 for p in Path(scratch).rglob("*") if p.is_file())
    print(json.dumps({"verdict": "ACCEPTED", "files": n}))
except InputRefused as exc:
    print(json.dumps({"verdict": "REFUSED", "reason": str(exc)}))
'''


def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", str(root), *args], env=env, capture_output=True, check=True).stdout


def clone_at(clone, dest):
    git(dest.parent, "clone", "-q", "--no-local", "--no-checkout", str(clone), str(dest))
    git(dest, "checkout", "-q", "--detach", HEAD)
    for name in ("gptp-processor", "third_party/verilog-axis"):
        git(dest, "config", f"submodule.{name}.url", str(clone / ".git/modules" / name))
        git(dest, "-c", "protocol.file.allow=always", "submodule", "update", "-q", "--init", "--", name)


def append(path, text):
    path.write_bytes(path.read_bytes() + text.encode())


def plant(root, arm):
    if arm == "clean":
        return
    if arm == "rewritten-test-results":
        p = root / "hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md"
        p.write_bytes(p.read_bytes().replace(b"20", b"21", 1))
        q = root / "hdl/ieee1722/aaf/doc/TEST_RESULTS.md"
        append(q, "\nrewritten by another suite\n")
    elif arm == "untracked-unrelated-hdl":
        (root / "hdl/common/reviewer_untracked.sv").write_text("// untracked unrelated work\n")
    elif arm == "dirty-unrelated-tb-common":
        append(root / "tb/common/gptp_launch_observer.hpp", "\n// unrelated work\n")
    elif arm == "dirty-suite-readme":
        append(root / "tb/verilator/gptp_shadow/README.md", "\nlocal note\n")
    elif arm == "dirty-unrelated-axis":
        append(root / "third_party/verilog-axis/rtl/axis_adapter.v", "\n// unrelated\n")
    elif arm == "dirty-mutation-target":
        append(root / "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv", "\n// caller work\n")
    elif arm == "dirty-build-input":
        append(root / "hdl/common/cdc_pulse.sv", "\n// caller work\n")
    elif arm == "dirty-local-header":
        append(root / "tb/common/gptp_tx_flags.hpp", "\n// caller work\n")
    elif arm == "dirty-axis-input":
        append(root / "third_party/verilog-axis/rtl/axis_fifo.v", "\n// caller work\n")
    elif arm == "dirty-gptp-input":
        append(root / "gptp-processor/hdl/top/KL_gptp_engine.sv", "\n// caller work\n")
    elif arm == "dirty-ucode-generator":
        append(root / "gptp-processor/hdl/ucode/gen_gptp_ucode.py", "\n# caller work\n")
    elif arm == "dirty-suite-makefile":
        append(root / "tb/verilator/gptp_shadow/Makefile", "\n# caller work\n")
    elif arm == "copied-dependency-no-git":
        # CONTRIBUTING's retired lane layout: copy of the files without the submodule .git
        (root / "third_party/verilog-axis/.git").unlink()
    elif arm == "uninitialised-dependency":
        git(root, "submodule", "deinit", "-q", "-f", "--", "gptp-processor")
    elif arm == "off-pin-dependency":
        git(root / "third_party/verilog-axis", "checkout", "-q", "--detach", "HEAD~1")
    elif arm == "assume-unchanged-target":
        path = "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
        git(root, "update-index", "--assume-unchanged", path)
        append(root / path, "\n// hidden caller work\n")
    else:
        raise ValueError(arm)


ARMS = ["clean", "rewritten-test-results", "untracked-unrelated-hdl", "dirty-unrelated-tb-common",
        "dirty-suite-readme", "dirty-unrelated-axis", "dirty-mutation-target", "dirty-build-input",
        "dirty-local-header", "dirty-axis-input", "dirty-gptp-input", "dirty-ucode-generator",
        "dirty-suite-makefile", "copied-dependency-no-git", "uninitialised-dependency",
        "off-pin-dependency", "assume-unchanged-target"]


def main():
    clone, scratch, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    (scratch / "child.py").write_text(CHILD)
    base = scratch / "_base"
    clone_at(clone, base)
    results = {}
    for arm in ARMS:
        root = scratch / arm
        shutil.copytree(base, root, symlinks=True)
        plant(root, arm)
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update(TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1")
        done = subprocess.run([sys.executable, "-I", str(scratch / "child.py"), str(root)], env=env,
                              capture_output=True, text=True, timeout=300)
        try:
            res = json.loads(done.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            res = {"verdict": "ERROR", "reason": (done.stdout + done.stderr)[-600:]}
        res["exit"] = done.returncode
        results[arm] = res
        print(f"{arm:28s} {res['verdict']:8s} {res.get('files', '')} {res.get('reason', '')[:120]}", flush=True)
        shutil.rmtree(root)
    output.write_text(json.dumps(results, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
