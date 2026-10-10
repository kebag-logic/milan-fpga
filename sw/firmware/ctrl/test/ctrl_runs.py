# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_runs.py - the builder runs the boundary gate makes under the capture itself (#697).

OWNED, on every run, beside the stack's own gate's build (ctrl_boundary.
stack_gate, under the same capture): the image builders, which need only the
RV32 compiler. ctrl_image.py links its own shapes (ctrl_image.SHAPES, the
shipping one and the largest); ctrl_image_selftest.py runs its controls;
ctrl_srp_image.py compiles those shapes at one and two interfaces, without
SRP, with it, and with AECP. Their -D and -U flags are the same at every
shape: a shape is the generated headers they search, which the boundary takes
for every shipped config from the same generators (ctrl_configs.shape_dim).
ctrl_srp_image.py links against the bare-metal runtime archives, which
ctrl_image_runtime.py builds from sources outside the checkout: it is given
archives that do not exist, so it compiles every object and then stops at its
link, and it must stop there and nowhere else. The images themselves are
never this gate's: the capture needs the invocations only.

STANDALONE, when the gate is given no capture: every other builder of
ctrl_configs.BUILDERS, by its own commands, from the checkout's root, but the
ones needing what the run says it has none of. Each must exit 0: a builder
that fails may have compiled less than it does.
"""

from __future__ import annotations

import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import ctrl_capture
import ctrl_image
from ctrl_build import HERE, ROOT, Refusal
from ctrl_configs import BUILDERS, CONFIGS, left_out

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


def stopped_at_link(argv: list[str], res) -> bool:
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


def standalone(capture: Path, work: Path, without: frozenset[str], verilator: str | None) -> list[str]:
    """Every builder of BUILDERS with commands, but those the run leaves out, run under the capture; one line
    each. A builder that does not exit 0 refuses the gate."""
    out = {b.path for b in left_out(without)}
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


def captures(given: list[Path] | None, work: Path, without: frozenset[str]) -> list[ctrl_capture.Capture]:
    """The captures the gate judges beside its own: the ones given, each of whose builder runs exited 0, or one
    it makes by running every known builder under it."""
    if not given:
        mine = work / "standalone"
        print("no capture given: running every known builder under one", flush=True)
        standalone(mine, work / "builders", without, verilator_of())
        return [ctrl_capture.load(mine)]
    loaded = [ctrl_capture.load(path.resolve()) for path in given]
    failed = [f"{' '.join(c['argv'])} exited {c['rc']}" for capture in loaded for c in capture.commands if c["rc"]]
    if failed:
        raise Refusal("a builder run of the capture failed, so it may have compiled less than it does: " +
                      "; ".join(failed))
    return loaded


def verilator_of() -> str | None:
    """The Verilator a standalone run gives the builders that need it: VERILATOR, else the one on PATH."""
    given = os.environ.get("VERILATOR")
    return given if given else next((str(p / "verilator") for p in map(Path, os.environ.get("PATH", "").split(":"))
                                     if (p / "verilator").is_file()), None)
