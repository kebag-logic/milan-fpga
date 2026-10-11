# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_runs.py - the builder runs the boundary gate makes under the capture itself (#697).

OWNED, on every run, beside the stack's own gate's build (ctrl_boundary.
stack_gate, under the same capture): the image builders, which need only the
RV32 compiler. ctrl_image.py links its own shapes (ctrl_image.SHAPES, the
shipping one and the largest); ctrl_image_selftest.py runs its controls;
ctrl_srp_image.py compiles those shapes at one and two interfaces, without
SRP, with it, and with AECP: every source both images compile, the saved-state
store's among them, as they compile it. ctrl_srp_image.py links against the
bare-metal runtime archives, which
ctrl_image_runtime.py builds from sources outside the checkout: it is given
archives that do not exist, so it compiles every object and then stops at its
link, and it must stop there and nowhere else. The images themselves are
never this gate's: the capture needs the invocations only.

STANDALONE, when the gate is given no capture (the hosted firmware-boundary
and firmware-verilator jobs): every other builder of ctrl_configs.BUILDERS,
by its own build commands (a suite builder's --build-only: its builds, not
its suites), from the checkout's root, but the ones the run leaves out
(ctrl_configs.Scope). Each must exit 0: a builder that fails may have
compiled less than it does.

THE STACK'S GATE (stack_gate) and THE CONTROLS' BUILDERS (planted_run,
replayed, control_capture): the stack's own gate's CMake build runs under the
capture too. A control's planted builder compiles a copy of the checkout's
firmware tree and stack (ctrl_boundary.mirror) through a capture of its own,
given the copy, the arms' include path for it, and the gate's directory to
import a builder's own compile functions from (the image builder's, the
arms'); a replay runs a compile of the run's capture again, its own
arguments with the firmware's tree and the stack in them the copy's. What it
compiled is judged, joined to the run's capture for what a capture must hold.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path

import ctrl_capture
import ctrl_image
from ctrl_build import CTRL, HERE, NVM_DIR, ROOT, STACK, Refusal, Tree, includes
from ctrl_capture import Capture
from ctrl_configs import BUILDERS, CONFIGS, Scope, run
from ctrl_pin import named_compilers
from ctrl_plants import Plant

#: The image builders the gate runs on every run, and the archive a runtime-less link names.
ABSENT = "absent-runtime"
#: Image builder runs at once.
JOBS = 4


def image_runs(work: Path) -> list[tuple[str, list[str]]]:
    """Every image builder run: a label and its command."""
    py = sys.executable
    shapes = ctrl_image.SHAPES
    runs = [(f"ctrl_image.py, {' and '.join(shapes)}",
             [py, "-B", str(HERE / "ctrl_image.py"), "--out", str(work / "ctrl-image")]),
            ("ctrl_image_selftest.py", [py, "-B", str(HERE / "ctrl_image_selftest.py"), "--require-rv32",
                                        "--out", str(work / "ctrl-image-selftest")])]
    absent = work / ABSENT
    for shape in shapes:
        for interfaces in ("1", "2"):
            for composition in ("--without-srp", "", "--with-aecp"):
                out = work / "srp-image" / f"{shape}-if{interfaces}{composition or '-srp'}"
                label = f"ctrl_srp_image.py {shape}, {interfaces} interface(s) {composition or '--with-srp'}"
                runs.append((label,
                             [py, "-B", str(HERE / "ctrl_srp_image.py"), "--config", str(CONFIGS / f"{shape}.yaml"),
                              "--interfaces", interfaces, "--output", str(out), "--libc", str(absent / "libc.a"),
                              "--compiler-runtime", str(absent / "libcompiler_rt.a"),
                              *([composition] if composition else [])]))
    return runs


def stopped_at_link(argv: list[str], res: subprocess.CompletedProcess) -> bool:
    """Whether an image builder run stopped where a runtime-less one must: ctrl_srp_image.py at its link, on the
    archives that do not exist; every other one passing."""
    if Path(argv[2]).name != "ctrl_srp_image.py":
        return res.returncode == 0
    said = res.stdout + res.stderr
    return res.returncode == 2 and f"{ABSENT}/libc.a" in said and "No such file" in said


def owned(capture: Path, work: Path) -> list[str]:
    """The image builders run under the capture; what each did, one line each. A run that ended anywhere else
    than it must refuses the gate."""
    if ctrl_image.fw_rv32.compiler() is None:
        raise Refusal("the image builders need the RV32 compiler")
    runs = image_runs(work)
    lines, bad = [], []

    def one(label: str, argv: list[str]) -> tuple[str, list[str], object, float]:
        """One image builder run, timed."""
        start = time.monotonic()
        res = ctrl_capture.run(capture, argv, cwd=ROOT, capture_output=True, text=True)
        return label, argv, res, time.monotonic() - start

    with ThreadPoolExecutor(max_workers=JOBS, thread_name_prefix="ctrl-boundary-image") as pool:
        for label, argv, res, took in pool.map(lambda r: one(*r), runs):
            ok = stopped_at_link(argv, res)
            lines.append(f"    {label}: exit {res.returncode}{', stopped at its link' if res.returncode else ''} "
                         f"({took:.0f} s)")
            if not ok:
                bad.append(f"{label} exited {res.returncode}: {(res.stdout + res.stderr).strip()[-400:]}")
    if bad:
        raise Refusal("an image builder did not run as the capture needs: " + "; ".join(bad))
    return lines


def standalone(capture: Path, work: Path, scope: Scope, verilator: str | None) -> list[str]:
    """Every builder of BUILDERS with commands, but those the run leaves out, run under the capture; one line
    each. A builder that does not exit 0 refuses the gate."""
    out = {b.path for b in scope.left_out()}
    lines = []
    for b in BUILDERS:
        if b.path in out or not b.runs:
            continue
        if b.needs == "verilator" and verilator is None:
            raise Refusal(f"{b.path} needs Verilator (VERILATOR, or on PATH); --without verilator leaves it out")
        for words in b.runs:
            argv = [w.format(python=sys.executable, work=work, verilator=verilator) for w in words]
            log = work / f"{Path(b.path).name}-{len(lines)}.log"
            work.mkdir(parents=True, exist_ok=True)
            start = time.monotonic()
            with log.open("w", encoding="utf-8") as sink:
                res = ctrl_capture.run(capture, argv, cwd=ROOT, stdout=sink, stderr=sink,
                                       env_extra={"VERILATOR": verilator} if verilator else None)
            lines.append(f"    {' '.join(words[1:3] if words[0] == '{python}' else words[:3])}: exit "
                         f"{res.returncode} ({time.monotonic() - start:.0f} s)")
            print(lines[-1], flush=True)
            if res.returncode:
                tail = log.read_text(encoding="utf-8", errors="replace").strip()[-600:]
                raise Refusal(f"{b.path} exited {res.returncode} under the capture, so it may have compiled less "
                              f"than it does: {tail}")
    return lines


def captures(given: list[Path] | None, work: Path, scope: Scope) -> list[ctrl_capture.Capture]:
    """The captures the gate judges beside its own: the ones given, each of whose builder runs exited 0 in this
    checkout, or one it makes by running every known builder the run judges under it."""
    if not given:
        mine = work / "standalone"
        print("no capture given: running every known builder the run judges under one", flush=True)
        standalone(mine, work / "builders", scope, verilator_of())
        return [ctrl_capture.load(mine)]
    loaded = [ctrl_capture.load(path.resolve()) for path in given]
    failed = [f"{' '.join(c['argv'])} exited {c['rc']}" for capture in loaded for c in capture.commands if c["rc"]]
    if failed:
        raise Refusal("a builder run of the capture failed, so it may have compiled less than it does: " +
                      "; ".join(failed))
    # what a compile read is judged where it lives: another checkout's files are none of this one's
    elsewhere = [f"{' '.join(c['argv'])} ran in {c['cwd']}" for capture in loaded for c in capture.commands
                 if not Path(c["cwd"]).resolve().is_relative_to(ROOT.resolve())]
    if elsewhere:
        raise Refusal("a builder run of the capture ran outside this checkout, whose files are none of this one's: " +
                      "; ".join(elsewhere))
    return loaded


def verilator_of() -> str | None:
    """The Verilator a standalone run gives the builders that need it: VERILATOR, else the one on PATH."""
    given = os.environ.get("VERILATOR")
    return given if given else next((str(p / "verilator") for p in map(Path, os.environ.get("PATH", "").split(":"))
                                     if (p / "verilator").is_file()), None)


def stack_gate(selftest: bool, work: Path, capture: Path | None) -> tuple[list[str], list[str]]:
    """The stack's own boundary gate (and its self-test), from the submodule, its CMake builds under the capture
    where one is given: what it said, and its refusal as a finding."""
    gate = STACK / "scripts/check_boundary.py"
    for tool in ("cmake", "clang", "gcc", "nm"):
        if shutil.which(tool) is None:
            raise Refusal(f"the stack's gate needs {tool}")
    work.mkdir(parents=True, exist_ok=True)
    argv = [sys.executable, "-I", str(gate), "--work", str(work), "--jobs", "4"]
    argv = [*argv, "--selftest"] if selftest else argv
    res = run(argv, cwd=work) if capture is None else \
        ctrl_capture.run(capture, argv, cwd=work, capture_output=True, text=True, env_extra={"LC_ALL": "C"})
    lines = [f"    {line}" for line in (res.stdout + res.stderr).strip().splitlines()]
    return lines, [] if res.returncode == 0 else [f"the stack's own gate {gate.relative_to(ROOT)} refused: "
                                                  f"exit {res.returncode}"]


def planted_env(root: Path, where: Path) -> dict[str, str]:
    """What a planted builder is given: the copy (its root, its ctrl tree, its stack and its store), its own
    directory, the real gcc, the gate's directory (to import a builder's own functions from) and the arms' include
    path for the copy (ctrl_build.includes)."""
    ctrl, stack = root / CTRL.relative_to(ROOT), root / STACK.relative_to(ROOT)
    arms = includes(Tree(ctrl, where / "out", where / "reuse", stack=stack))
    return {"PLANT_ROOT": str(root), "PLANT_CTRL": str(ctrl), "PLANT_STACK": str(stack),
            "PLANT_NVM": str(root / NVM_DIR.relative_to(ROOT)), "PLANT_WORK": str(where),
            "PLANT_GCC": shutil.which("gcc") or "gcc", "PLANT_TESTS": str(HERE), "PLANT_INCLUDES": " ".join(arms)}


def planted_run(plant: Plant, root: Path, work: Path, capture: Path) -> list[dict]:
    """A plant's builder, run through `capture` in a directory of its own beside the copy of the checkout at
    `root`, its files beside it there before the capture began (a tick of the file clock earlier); a planted
    Makefile's compilers named by a path, as bypass records (ctrl_pin.named_compilers)."""
    where = (work / "builder").resolve()
    shutil.rmtree(where, ignore_errors=True)
    where.mkdir(parents=True)
    (where / "planted.c").write_text("", encoding="utf-8")
    for name, text in plant.beside:
        (where / name).parent.mkdir(parents=True, exist_ok=True)
        (where / name).write_text(text, encoding="utf-8")
    if plant.beside:
        time.sleep(0.05)
    builder = where / ("planted.mk" if plant.make else "planted_builder.py")
    builder.write_text(plant.run, encoding="utf-8")
    argv = ["make", "-f", str(builder), "planted"] if plant.make else [sys.executable, str(builder)]
    given = planted_env(root, where)
    ctrl_capture.run(capture, argv, cwd=where, capture_output=True, text=True, env_extra=given)
    return named_compilers(builder, {**ctrl_capture.install(capture), **given}) if plant.make else []


def replayed(plant: Plant, root: Path, base: Capture, work: Path, capture: Path) -> None:
    """A plant's replay: every compile of the run's capture whose source is named `plant.replay`, run again through
    `capture` with its own arguments, in its own directory, the firmware's tree and the stack in them the copy's,
    and its output its own (a wire comparison the gate's run built, with a mode only that builder gives)."""
    moves = {str(tree): str(root / tree.relative_to(ROOT)) for tree in (CTRL, NVM_DIR, STACK)}
    moved = re.compile("|".join(rf"{re.escape(tree)}(?=/|$)" for tree in moves))
    done: set[tuple[str, ...]] = set()
    for inv in base.invocations:
        # a compile whose inputs are gone (a builder's temporary files) cannot run again
        sources = [s for s in inv.sources if Path(s.path).name == plant.replay and s.deps is not None and
                   all(Path(f).exists() for f in s.deps.files)]
        if not sources or inv.args in done:
            continue
        done.add(inv.args)
        args = [moved.sub(lambda m: moves[m[0]], arg) for arg in inv.args]
        args = [str(work / f"replayed-{len(done)}") if at and args[at - 1] == "-o" else arg
                for at, arg in enumerate(args)]
        ctrl_capture.run(capture, [inv.tool, *args], cwd=Path(inv.cwd), capture_output=True, text=True)


def control_capture(plant: Plant, root: Path, base: Capture, work: Path) -> tuple[Capture, Capture]:
    """The capture a control is judged against, and the part of it its own compiles are: the base the controls
    share, altered as the plant says, with nothing of its own; or the base and what its planted builder (or its
    replay) compiled from the copy of the checkout at `root`, run through a capture of its own."""
    nothing = Capture((), (), (), ())
    if plant.alter == "missing":
        return ctrl_capture.load(work / "no-capture"), nothing
    if plant.alter == "empty":
        (work / "empty").mkdir(parents=True, exist_ok=True)
        for name in ("records.jsonl", "manifest.jsonl"):
            (work / "empty" / name).write_text("", encoding="utf-8")
        return ctrl_capture.load(work / "empty"), nothing
    if plant.alter.startswith("drop "):
        lost = plant.alter.removeprefix("drop ")
        return replace(base, invocations=tuple(inv for inv in base.invocations if lost not in inv.builders),
                       parts=()), nothing
    if not plant.run and not plant.replay:
        return base, nothing
    capture = (work / "capture").resolve()
    shutil.rmtree(capture, ignore_errors=True)
    if plant.replay:
        replayed(plant, root, base, work, capture)
        named: list[dict] = []
    else:
        named = planted_run(plant, root, work, capture)
    own = ctrl_capture.load(capture, required=False) + Capture((), (), (), tuple(named))
    return base + own, own
