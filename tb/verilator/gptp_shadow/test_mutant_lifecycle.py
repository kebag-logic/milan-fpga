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
    FACILITY_MODES, FACILITY_SITE, Probe, assert_reaped, commit, git, install, snapshot, write,
)
from mutants import MUTATIONS, NOT_SEPARATELY_OBSERVABLE  # noqa: E402

DRIVER = "tb/verilator/gptp_shadow/mutants.py"
SUITE = "tb/verilator/gptp_shadow"
SOURCE = "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
DEPENDENCIES = ("gptp-processor", "third_party/verilog-axis")
#: The local headers sim_main.cpp includes. Stated here, independently of the
#: driver's include walk, so a walk that loses one fails the population check.
HEADERS = ("tb/common/verilator_harness.hpp", "tb/common/gptp_tx_flags.hpp")
#: Tracked files the build never reads. Their state must never refuse.
UNRELATED = ("tb/verilator/gptp_shadow/README.md", "hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md",
             "hdl/ieee1722/aaf/doc/TEST_RESULTS.md", "tb/common/gptp_launch_observer.hpp")
UNRELATED_DEPENDENCY = "third_party/verilog-axis/rtl/axis_adapter.v"
#: Ordinary settings that cannot change what the identity commands read.
PRESENTATION = dict(GIT_EDITOR="true", GIT_SEQUENCE_EDITOR="true", GIT_PAGER="cat",
                    GIT_AUTHOR_NAME="Author", GIT_AUTHOR_EMAIL="author@example.invalid",
                    GIT_COMMITTER_NAME="Committer", GIT_COMMITTER_EMAIL="committer@example.invalid",
                    GIT_SSH_COMMAND="ssh -oBatchMode=yes", GIT_ASKPASS="true", GIT_TERMINAL_PROMPT="0",
                    GIT_TRACE="0", GIT_MERGE_AUTOEDIT="no", GIT_NAMESPACE="presentation")
#: Every variable that redirects the checkout Git reads must refuse by name.
#: Listed here, not imported, so dropping one from the driver turns its arm red.
REDIRECTS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
             "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_REPLACE_REF_BASE", "GIT_CONFIG_PARAMETERS",
             "GIT_CONFIG_COUNT", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM")

MAKE = r'''#!/usr/bin/env python3
import hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
if "print-inputs" in sys.argv:
    # The input declaration is the real Makefile, asked through real make.
    here = Path(__file__).resolve().parent
    real = shutil.which("make", path=os.pathsep.join(
        entry for entry in os.environ["PATH"].split(os.pathsep) if Path(entry).resolve() != here))
    os.execv(real, [real, *sys.argv[1:]])
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

#: Real Git, with one unreadable record ahead of every index listing.
GARBLED_GIT = r'''#!/usr/bin/env python3
import os, shutil, subprocess, sys
from pathlib import Path
here = Path(__file__).resolve().parent
real = shutil.which("git", path=os.pathsep.join(
    entry for entry in os.environ["PATH"].split(os.pathsep) if Path(entry).resolve() != here))
result = subprocess.run([real, *sys.argv[1:]], stdout=subprocess.PIPE, check=False)
if "--stage" in sys.argv:
    sys.stdout.buffer.write(b"not an identity record\0")
sys.stdout.buffer.write(result.stdout)
raise SystemExit(result.returncode)
'''


def declared() -> set[str]:
    """What the real suite Makefile says its build reads, plus the stated headers."""
    words = subprocess.run(["make", "-s", "--no-print-directory", "print-inputs"], cwd=ROOT / SUITE,
                           capture_output=True, text=True, check=True).stdout.split()
    return {str((ROOT / SUITE / word).resolve().relative_to(ROOT)) for word in words} | set(HEADERS)


def fixture(parent: Path, label: str) -> tuple[Path, Probe]:
    """Create tracked inputs and two real pinned disposable dependency repos."""
    root = parent / (label + " input [523]")
    root.mkdir()
    population = declared()
    first_party = {name for name in population if not name.startswith(DEPENDENCIES)}
    for relative in sorted(first_party | set(UNRELATED) | {
            DRIVER, "tb/verilator/gptp_shadow/private_inputs.py", "scripts/owned_process.py"}):
        install(root, relative)
    git(root, "init", "-q")
    for name in DEPENDENCIES:
        for relative in sorted(population - first_party) + [UNRELATED_DEPENDENCY]:
            if relative.startswith(name + "/"):
                write(root / relative, f"pinned dependency input {relative}\n")
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
    writes = [min(name for name in population if name.startswith(dependency + "/"))
              for dependency in DEPENDENCIES]
    write(probe.control / "private-writes.json", json.dumps(writes))
    write(probe.control / "population.json", json.dumps(sorted(population)))
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


def accepted(parent: Path, kind: str) -> None:
    """Files the build never reads and non-redirecting Git settings run every control."""
    root, probe = fixture(parent, "accept-" + kind)
    probe.env["PROBE_MODE"] = "detect"
    if kind == "unrelated":
        for relative in UNRELATED:
            path = root / relative
            path.write_bytes(path.read_bytes().replace(b"20", b"21", 1) + b"\nrewritten by another suite\n")
        git(root, "add", UNRELATED[0])
        write(root / "hdl/common/unrelated_work.sv", "// untracked caller work\n")
        write(root / UNRELATED_DEPENDENCY, "caller dependency work\n")
    elif kind == "presentation":
        probe.env.update(PRESENTATION)
    elif kind == "scrubbed":
        # Would make every literal-pathspec identity command fail if passed on.
        probe.env["GIT_GLOB_PATHSPECS"] = "1"
    elif kind == "git-stderr":
        # Git reports this deprecated setting on standard error.
        git(root, "config", "core.fsyncObjectFiles", "true")
    before = snapshot(root)
    probe.start([sys.executable, str(root / DRIVER)])
    status, output = probe.finish()
    assert status == 0 and "controls: 9   failures: 0\nRESULT: PASS" in output, output
    assert snapshot(root) == before, "caller inputs changed"
    assert not Path((probe.control / "workspace").read_text()).exists(), "scratch survived"
    probe.save(dict(exit=status, accepted=kind, controls=9, source_unchanged=True))


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
                        .replace("copy_inputs(REPO, HERE, private, owner, targets)", "owner.checkpoint()"))
        commit(root)
    before = snapshot(root)
    probe.env["PROBE_MODE"] = "hold"
    probe.start([sys.executable, str(root / DRIVER)])
    data = probe.ready()
    assert "abort_counts_as_completion" in data["mutations"], data
    private = Path(data["private"])
    if not unsafe:
        assert private != root and snapshot(root) == before
        # Exactly what the build reads is copied: nothing it never reads.
        expected = json.loads((probe.control / "population.json").read_text())
        copied = sorted(str(path.relative_to(private)) for path in private.rglob("*")
                        if path.is_file() or path.is_symlink())
        assert copied == expected, (copied, expected)
        for relative in [SOURCE, *json.loads((probe.control / "private-writes.json").read_text())]:
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


def prepare_refusal(root: Path, probe: Probe, kind: str) -> str:
    """Plant one refused input state; return the reason the refusal must name."""
    path = root / SOURCE
    dependency = root / "gptp-processor"
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
            return "index differs from HEAD"
        return "modified input bytes/mode"
    changed = {"dirty-input": "hdl/common/cdc_pulse.sv", "dirty-header": HEADERS[1],
               "dirty-anchor": "hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv"}
    if kind in changed:
        target = root / changed[kind]
        target.write_bytes(target.read_bytes() + b"\n// caller work\n")
        return "modified input bytes/mode: " + str(target)
    if kind == "untracked":
        git(root, "rm", "--cached", "-q", SOURCE)
        return "index differs from HEAD"
    if kind == "undeclared-target":
        makefile = root / SUITE / "Makefile"
        makefile.write_text(makefile.read_text().replace("$(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_txret.sv \\\n", ""))
        commit(root)
        return "mutation target or anchor is not a build input: " + SOURCE
    if kind == "symlink":
        saved = root / "saved.sv"
        path.rename(saved)
        path.symlink_to(saved)
        return "input is not a regular file"
    if kind in ("parent-link", "dependency-link"):
        directory = root / ("hdl/ieee8021as" if kind == "parent-link" else "gptp-processor")
        saved = root / ("saved-" + kind)
        directory.rename(saved)
        directory.symlink_to(saved, target_is_directory=True)
        return "input directory is missing or linked"
    if kind == "dependency":
        name = json.loads((probe.control / "private-writes.json").read_text())[0]
        inner = name[len("gptp-processor/"):]
        git(dependency, "update-index", "--skip-worktree", inner)
        write(root / name, "caller dependency work\n")
        return "modified input bytes/mode: " + str(root / name)
    if kind == "off-pin":
        name = json.loads((probe.control / "private-writes.json").read_text())[0]
        write(root / name, "different revision\n")
        commit(dependency)
        return "required dependency is not at its pin: gptp-processor"
    if kind == "pin-index":
        git(root, "update-index", "--force-remove", "gptp-processor")
        return "required dependency gitlinks differ from HEAD"
    if kind == "git-garbage":
        write(probe.control / "bin/git", GARBLED_GIT, executable=True)
        return "unreadable Git identity record"
    variable = kind[len("git-env-"):]
    assert variable in REDIRECTS, kind
    probe.env[variable] = str(root / ".git")
    return "Git environment redirects the checkout: " + variable


def refusal(parent: Path, kind: str) -> None:
    """Dirty, index-hidden, linked, redirected or unreadable input fails before make."""
    root, probe = fixture(parent, kind)
    reason = prepare_refusal(root, probe, kind)
    before = snapshot(root)
    probe.start([sys.executable, str(root / DRIVER)])
    status, output = probe.finish()
    assert status == 2 and "REFUSED:" in output and reason in output, (reason, output)
    assert "Traceback" not in output, output
    assert snapshot(root) == before and not (probe.control / "seen").exists(), output
    assert not list(probe.control.glob("gptp-shadow-mutants-*")), "refusal left scratch"
    probe.save(dict(exit=status, refusal=kind, reason=reason, input_unchanged=True, make_started=False))


def unsupported(parent: Path, mode: str) -> None:
    """A host lacking a process facility gets the documented refusal, not a traceback."""
    root, probe = fixture(parent, "facility-" + mode)
    write(probe.control / "site/sitecustomize.py", FACILITY_SITE)
    probe.env.update(PYTHONPATH=str(probe.control / "site"), PROBE_FACILITY=mode)
    before = snapshot(root)
    probe.start([sys.executable, str(root / DRIVER)])
    status, output = probe.finish()
    assert status == 2 and "REFUSED:" in output and "Traceback" not in output, output
    assert snapshot(root) == before and not (probe.control / "seen").exists(), output
    assert not list(probe.control.glob("gptp-shadow-mutants-*")), "refusal left scratch"
    probe.save(dict(exit=status, facility=mode, refused=True, make_started=False))


def ownership(parent: Path) -> None:
    """The normal Makefile owns lifecycle tests and propagates their failure."""
    root, probe = fixture(parent, "make-owner")
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
    for name in ("mutation.json", "private-writes.json"):
        shutil.copy2(mutation_probe.control / name, probe.control / name)
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


REFUSALS = ("dirty", "staged", "assume", "skip", "mode", "dirty-input", "dirty-header", "dirty-anchor",
            "untracked", "undeclared-target", "symlink", "parent-link", "dependency", "off-pin",
            "pin-index", "dependency-link", "git-garbage") + tuple("git-env-" + name for name in REDIRECTS)


def main() -> int:
    """Run the normal, refusal and deterministic interruption controls."""
    with tempfile.TemporaryDirectory(prefix="mutant-lifecycle-") as scratch:
        # Refusals name resolved caller paths; compare against the same form.
        parent = Path(scratch).resolve()
        # This outer owner is test containment only. Successful graceful cases
        # must prove identities gone BEFORE it can reap any leaked descendant.
        with OwnedProcesses():
            normal(parent, "detect", repeat=True)
            normal(parent, "survive")
            normal(parent, "build")
            for kind in ("unrelated", "presentation", "scrubbed", "git-stderr"):
                accepted(parent, kind)
            ownership(parent)
            for kind in REFUSALS:
                refusal(parent, kind)
            for mode in FACILITY_MODES:
                unsupported(parent, mode)
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
    print("mutant lifecycle: PASS (normal/repeat, nine named defects, survivor, build, unread-file and "
          "Git-setting acceptance, input/Git-redirect/record/facility refusals, INT/TERM/KILL, "
          "unsafe negative controls)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
