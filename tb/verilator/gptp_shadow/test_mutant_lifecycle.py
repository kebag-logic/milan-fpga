#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise the production mutation driver at observable lifecycle boundaries."""

import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from owned_process import OwnedProcesses  # noqa: E402
from process_test_support import (  # noqa: E402
    Probe, assert_reaped, commit, git, install, snapshot, write,
)
from mutants import MUTATIONS, NOT_SEPARATELY_OBSERVABLE  # noqa: E402

DRIVER = "tb/verilator/gptp_shadow/mutants.py"
SOURCE = "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"

MAKE = r'''#!/usr/bin/env python3
import hashlib, json, os, subprocess, sys
from pathlib import Path
control = Path(os.environ["PROBE_CONTROL"])
root = Path.cwd().parents[2]
(control / "workspace").write_text(str(root))
catalog = json.loads((control / "mutation.json").read_text())
matches = [row for row in catalog
           if hashlib.sha256((root / row["path"]).read_bytes()).hexdigest() == row["hash"]]
assert len(matches) == 1, matches
row = matches[0]
with (control / "seen").open("a") as seen:
    seen.write(row["name"] + "\n")
mode = os.environ.get("PROBE_MODE", "detect")
if mode == "hold":
    raise SystemExit(subprocess.call([sys.executable, str(control / "worker.py")]))
if mode == "build":
    print("synthetic compilation failed")
    raise SystemExit(2)
if mode == "survive":
    print("1 checks: 1 PASS, 0 FAIL")
    raise SystemExit(0)
print("FAIL " + row["expect"] + " got 0 exp 1")
print("1 checks: 0 PASS, 1 FAIL")
raise SystemExit(1)
'''


def fixture(parent: Path, label: str) -> tuple[Path, Probe]:
    """Create tracked inputs and two real pinned disposable dependency repos."""
    root = parent / (label + " input [523]")
    root.mkdir()
    for relative in (DRIVER, "tb/verilator/gptp_shadow/private_inputs.py",
                     "scripts/owned_process.py", "tb/verilator/gptp_shadow/Makefile",
                     "tb/verilator/gptp_shadow/sim_main.cpp", "tb/common/verilator_harness.hpp"):
        install(root, relative)
    for path in {row[1] for row in MUTATIONS + NOT_SEPARATELY_OBSERVABLE}:
        install(root, str(path.relative_to(ROOT)))
    git(root, "init", "-q")
    for name in ("gptp-processor", "third_party/verilog-axis"):
        write(root / name / "probe.txt", "pinned dependency\n")
        git(root / name, "init", "-q")
        commit(root / name)
    commit(root)
    probe = Probe(root, label)
    catalog = []
    for name, path, old, new, expect in MUTATIONS:
        original = path.read_text()
        catalog.append(dict(name=name, path=str(path.relative_to(ROOT)), new=new, expect=expect,
                            hash=hashlib.sha256(original.replace(old, new, 1).encode()).hexdigest()))
    write(probe.control / "mutation.json", json.dumps(catalog))
    write(probe.control / "bin/make", MAKE, executable=True)
    probe.env["PATH"] = str(probe.control / "bin") + os.pathsep + os.environ["PATH"]
    return root, probe


def normal(parent: Path, mode: str, repeat: bool = False) -> None:
    """Check exact populations, verdict distinctions and repeated cleanup."""
    root, probe = fixture(parent, mode)
    probe.env["PROBE_MODE"] = mode
    before = snapshot(root)
    for iteration in range(2 if repeat else 1):
        probe.start([sys.executable, str(root / DRIVER)])
        status, output = probe.finish()
        assert status == (0 if mode == "detect" else 1), output
        assert snapshot(root) == before, "caller inputs changed"
        assert not Path((probe.control / "workspace").read_text()).exists(), "scratch survived"
        seen = (probe.control / "seen").read_text().splitlines()
        assert seen == [row[0] for row in MUTATIONS] * (iteration + 1), seen
        assert output.count("[note]") == len(NOT_SEPARATELY_OBSERVABLE), output
        if mode == "detect":
            for name, _path, _old, _new, expect in MUTATIONS:
                assert f'{name}: caught by "{expect}"' in output, output
            assert "controls: 9   failures: 0\nRESULT: PASS" in output, output
        else:
            assert "RESULT: PASS" not in output and "controls: 9   failures: 9" in output, output
            assert ("no completed suite tally" if mode == "build" else "stayed green") in output, output
        probe.save(dict(exit=status, iteration=iteration, mutations=seen,
                        source_unchanged=True, scratch_removed=True))


def interrupted(parent: Path, signum: int, unsafe: bool = False) -> None:
    """Signal only after private mutation and stubborn-child readiness."""
    label = ("unsafe-" if unsafe else "isolated-") + signal.Signals(signum).name
    root, probe = fixture(parent, label)
    if unsafe:
        path = root / DRIVER
        text = path.read_text()
        assert "private = Path(scratch)" in text
        # Restore the original defect: caller input is the mutation/build tree,
        # and restoration remains after the command, unreachable on interruption.
        path.write_text(text.replace("private = Path(scratch)", "private = REPO")
                        .replace("copy_inputs(REPO, private, owner)", "owner.checkpoint()"))
        commit(root)
    before = snapshot(root)
    probe.env["PROBE_MODE"] = "hold"
    probe.start([sys.executable, str(root / DRIVER)])
    data = probe.ready()
    assert "abort_counts_as_completion" in data["mutations"], data
    private = Path(data["private"])
    if not unsafe:
        assert private != root and snapshot(root) == before
        for relative in (SOURCE, "gptp-processor/probe.txt", "third_party/verilog-axis/probe.txt"):
            assert not (root / relative).samefile(private / relative)
    probe.signal(signum)
    status, output = probe.finish()
    changed = snapshot(root) != before
    assert changed == unsafe, (label, "isolation oracle", changed)
    assert "RESULT: PASS" not in output and "controls:" not in output, output
    if signum == signal.SIGKILL:
        assert status == -signal.SIGKILL, output
    else:
        assert status == 128 + signum, output
        assert_reaped(data)
        if not unsafe:
            assert not private.exists(), private
    probe.save(dict(exit=status, signal=signal.Signals(signum).name, handshake=data,
                    caller_changed=changed, unsafe_control_detected=unsafe,
                    cleanup_required=signum != signal.SIGKILL))


def refusal(parent: Path, kind: str) -> None:
    """Dirty, index-hidden and linked input must fail before starting make."""
    root, probe = fixture(parent, kind)
    path = root / SOURCE
    if kind in ("dirty", "staged", "assume", "skip", "mode"):
        if kind in ("assume", "skip"):
            git(root, "update-index", "--assume-unchanged" if kind == "assume" else "--skip-worktree", SOURCE)
        if kind == "mode":
            path.chmod(0o755)
            git(root, "config", "core.filemode", "false")
        else:
            path.write_bytes(path.read_bytes() + b"\n// caller work\n")
        if kind == "staged":
            git(root, "add", SOURCE)
    elif kind == "untracked":
        git(root, "rm", "--cached", SOURCE)
    elif kind == "extra":
        write(root / "hdl/untracked.sv", "unknown input\n")
    elif kind == "symlink":
        saved = root / "saved.sv"
        path.rename(saved)
        path.symlink_to(saved)
    elif kind == "parent-link":
        directory = root / "hdl/ieee8021as"
        saved = root / "saved-hdl"
        directory.rename(saved)
        directory.symlink_to(saved, target_is_directory=True)
    elif kind == "dependency":
        dependency = root / "gptp-processor"
        git(dependency, "update-index", "--skip-worktree", "probe.txt")
        write(dependency / "probe.txt", "caller dependency work\n")
    elif kind == "off-pin":
        dependency = root / "gptp-processor"
        write(dependency / "probe.txt", "different revision\n")
        commit(dependency)
    elif kind == "pin-index":
        git(root, "update-index", "--force-remove", "gptp-processor")
    elif kind == "dependency-link":
        dependency = root / "gptp-processor"
        saved = root / "saved-dependency"
        dependency.rename(saved)
        dependency.symlink_to(saved, target_is_directory=True)
    elif kind == "git-env":
        probe.env["GIT_INDEX_FILE"] = str(root / ".git/index")
    before = snapshot(root)
    probe.start([sys.executable, str(root / DRIVER)])
    status, output = probe.finish()
    assert status == 2 and "REFUSED:" in output, output
    assert snapshot(root) == before and not (probe.control / "seen").exists(), output
    assert not list(probe.control.glob("gptp-shadow-mutants-*")), "refusal left scratch"
    probe.save(dict(exit=status, refusal=kind, input_unchanged=True, make_started=False))


def ownership(parent: Path) -> None:
    """The normal Makefile owns lifecycle tests and propagates their failure."""
    root, probe = fixture(parent, "make-owner")
    write(root / "gptp-processor/hdl/ucode/gen_gptp_ucode.py", "# dry-run prerequisite\n")
    directory = root / "tb/verilator/gptp_shadow"
    status = subprocess.run(["make", "-n", "-C", str(directory)], capture_output=True, text=True, check=False)
    assert status.returncode == 0 and "python3 test_mutant_lifecycle.py" in status.stdout, status
    write(directory / "test_mutant_lifecycle.py", "raise SystemExit(1)\n")
    # Use real make and Python, not the synthetic mutation command shim.
    probe.env["PATH"] = os.environ["PATH"]
    probe.start(["make", "-C", str(directory), "lifecycle"])
    code, output = probe.finish()
    assert code != 0 and "test_mutant_lifecycle.py" in output, output
    probe.save(dict(exit=code, normal_make_owns_lifecycle=True, failure_propagated=True))


def outer_cancellation(parent: Path, signum: int) -> None:
    """Cancel the real sweep containing the real mutation driver and child owner."""
    from test_suite_cancellation import fixture as sweep_fixture
    label = "nested-" + signal.Signals(signum).name
    original, mutation_probe = fixture(parent, label + "-inputs")
    root, probe = sweep_fixture(parent, label)
    for relative in ("hdl", "tb/common", "tb/verilator/gptp_shadow", "gptp-processor",
                     "third_party/verilog-axis"):
        shutil.copytree(original / relative, root / relative, dirs_exist_ok=True)
    git(root, "init", "-q")
    commit(root)
    shutil.copy2(mutation_probe.control / "mutation.json", probe.control / "mutation.json")
    shim = MAKE.replace('control = Path(os.environ["PROBE_CONTROL"])', '''control = Path(os.environ["PROBE_CONTROL"])
if "-C" in sys.argv:
    suite = Path(sys.argv[sys.argv.index("-C") + 1])
    if suite.name == "omega":
        (control / "next-suite").write_text("unexpected later suite")
        raise SystemExit(1)
    driver = suite.parents[2] / "tb/verilator/gptp_shadow/mutants.py"
    raise SystemExit(subprocess.call([sys.executable, str(driver)]))''')
    write(probe.control / "bin/make", shim, executable=True)
    probe.env["PROBE_MODE"] = "hold"
    before = snapshot(root)
    probe.start(["bash", str(root / "scripts/run_all_suites.sh"), str(root / "logs")])
    data = probe.ready()
    private = Path(data["private"])
    assert private != root and snapshot(root) == before
    probe.signal(signum)
    status, output = probe.finish()
    assert status == 128 + signum and "\nsuites:" not in output, output
    assert not (probe.control / "next-suite").exists(), output
    assert_reaped(data)
    assert snapshot(root) == before and not private.exists(), "nested cancellation left private work"
    probe.save(dict(exit=status, handshake=data, nested_driver=True,
                    source_unchanged=True, scratch_removed=True, next_suite=False))


def main() -> int:
    """Run the normal, refusal and deterministic interruption controls."""
    with tempfile.TemporaryDirectory(prefix="mutant-lifecycle-") as scratch:
        parent = Path(scratch)
        # This outer owner is test containment only. Successful graceful cases
        # must prove identities gone BEFORE it can reap any leaked descendant.
        with OwnedProcesses():
            normal(parent, "detect", repeat=True)
            normal(parent, "survive")
            normal(parent, "build")
            ownership(parent)
            for kind in ("dirty", "staged", "assume", "skip", "mode", "untracked", "extra",
                         "symlink", "parent-link", "dependency", "off-pin", "pin-index",
                         "dependency-link", "git-env"):
                refusal(parent, kind)
            for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGKILL):
                # KILL may leave private children. Reap these fixture-owned
                # survivors before deleting the disposable fixture directory.
                with OwnedProcesses():
                    interrupted(parent, signum)
            with OwnedProcesses():
                interrupted(parent, signal.SIGTERM, unsafe=True)
            with OwnedProcesses():
                interrupted(parent, signal.SIGKILL, unsafe=True)
            for signum in (signal.SIGINT, signal.SIGTERM):
                outer_cancellation(parent, signum)
    print("mutant lifecycle: PASS (normal/repeat, nine named defects, survivor, build, "
          "input refusals, INT/TERM/KILL, unsafe negative controls)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
