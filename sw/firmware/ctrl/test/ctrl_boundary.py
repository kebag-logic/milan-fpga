#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_boundary.py - the TSN stack's boundary, held from both sides (#697).

THE STACK'S SIDE. Every source and public header of the tsn-c-stack submodule
(src/*.c, include/*.h) is preprocessed with this firmware's own include path
and flags, as the host arms compile it (ctrl_build.includes, C_FLAGS) and as
the RV32 build does (RV32_FLAGS and the freestanding headers of fw_rv32), and
its dependencies are read from the compiler (-M). Each must be one of the
stack's public headers or a header of the C library the compiler supplies. A
dependency anywhere else (the mailbox driver or its HAL, the generated
register-map contract, the MMIO platform, the app, the loop, the store, an
image) is refused by name; one that does not resolve is refused too. The
stack's own gate, its scripts/check_boundary.py (the same rule under its own
CMake build with gcc and clang, and its objects' symbols), runs as well.

THE FIRMWARE'S SIDE. Every firmware source and header under sw/firmware/ctrl
(not the host model or the tests) and the measured images' own sources reach
the stack through its public headers only. Each is preprocessed (-M -MG, a
generated header named, not read) with the firmware's include path and the
stack's other directories searched last, so a header only they hold resolves
there; a dependency inside the stack outside include/ is refused. No file
under sw/firmware may be named as one of the stack's sources or public
headers: a copy there would shadow, or stand in for, the stack's own.

Every gate that builds the stack first checks that the submodule is at its
gitlink with its sources, headers and tests unmodified (ctrl_build.stack_pin);
this one does too.

--selftest first plants defects in copies of the two trees, each of which must
be refused by name, and controls each of which must pass; then the pin
check's controls (a clone of the stack at its gitlink passes, the clone with
a source or a test edited, or at another revision, is refused); then runs the
stack gate's own self-test. --require-rv32 refuses, rather than skips, the RV32 arm
when no RV32 compiler is found.

Usage:
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest

Exit 0 = both sides hold; 1 = a finding or a control that misbehaved; 2 =
refused (no compiler, cmake or clang, or the stack's gate could not run).
"""

from __future__ import annotations

import argparse
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gtest"))

import fw_rv32  # noqa: E402
from ctrl_build import (C_FLAGS, CTRL, NVM_DIR, ROOT, RV32_FLAGS, STACK, STACK_INCLUDE, STACK_PARTS,  # noqa: E402
                        Refusal, Tree, includes, stack_gitlink, stack_pin)

#: The C library's headers (ISO C11, 7.1.2): what the stack may include beside its own.
C_HEADERS = ("assert complex ctype errno fenv float inttypes iso646 limits locale math stdalign stdarg stdatomic "
             "stdbool stddef stdint stdio stdlib stdnoreturn string tgmath uchar wchar wctype").split()
#: The stack's directories other than its public headers, searched last on the firmware's side.
STACK_PRIVATE = ("src", "tests", "examples")
#: The firmware's directories under sw/firmware/ctrl; host/ and test/ are test equipment.
FIRMWARE_DIRS = ("mbx", "port", "loop", "adp", "maap", "acmp", "app", "plat", "srp")
#: The measured images' own sources (ctrl_image.py, ctrl_srp_image.py).
IMAGE_SOURCES = ("test/rv32_image/image_main.c", "test/rv32_image/image_arith.c", "test/rv32_image/image_rt.c",
                 "test/ctrl_image.c")
#: What the firmware's sources need defined to preprocess at all: the window's address (plat/), a shape's
#: stream counts (the image), lwSRP's Milan profile and the SRP image (srp/, ctrl_image.c).
FIRMWARE_DEFINES = ("-DNDEBUG", "-DCTRL_MBX_BASE=0x80000000u", "-DIMAGE_SINKS=1u", "-DIMAGE_SOURCES=1u",
                    "-DLWSRP_MILAN=1", "-DCTRL_IMAGE_SRP")
LWSRP = ROOT / "third_party/lwSRP/src"
#: The entity the SRP adapter's generated shape is taken from, as the SRP arms take it by default.
SRP_ENTITY = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
#: The stack's own gate, from the submodule.
STACK_GATE = STACK / "scripts/check_boundary.py"


@dataclass(frozen=True)
class Trees:
    """The ctrl tree and the stack being judged: the checkout's, or planted copies."""

    ctrl: Path
    stack: Path


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """One tool, its output captured."""
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)


def dependencies(argv: list[str], source: Path) -> set[Path] | str:
    """The files the compiler reads for `source` under `argv` (-M), or its error."""
    res = run([*argv, "-M", "-MT", "boundary", str(source)])
    if res.returncode != 0:
        return res.stderr.strip().splitlines()[-1] if res.stderr.strip() else f"exit {res.returncode}"
    names = shlex.split(res.stdout.replace("\\\n", " ").split(":", 1)[1])
    return {Path(n) for n in names}


def c_library(argv: list[str], work: Path) -> set[Path]:
    """The C library headers the compiler supplies under `argv` without the firmware's paths: the closure of
    every standard header it has."""
    found: set[Path] = set()
    work.mkdir(parents=True, exist_ok=True)
    for header in C_HEADERS:
        probe = work / f"probe_{header}.c"
        probe.write_text(f"#include <{header}.h>\n", encoding="utf-8")
        deps = dependencies(argv, probe)
        if isinstance(deps, set):
            found |= {d.resolve() for d in deps if d.resolve() != probe.resolve()}
    if not found:
        raise Refusal(f"{argv[0]} supplies no C library header")
    return found


def stack_side(trees: Trees, argv: list[str], library: set[Path], label: str) -> list[str]:
    """The stack's sources and public headers, preprocessed under the firmware's flags `argv`: every
    dependency is the stack's public header or the C library's."""
    public = (trees.stack / STACK_INCLUDE).resolve()
    units = sorted((trees.stack / "src").glob("*.c")) + sorted((trees.stack / STACK_INCLUDE).glob("*.h"))
    findings = []
    for unit in units:
        lang = ["-x", "c"] if unit.suffix == ".h" else []
        deps = dependencies([*argv, *lang], unit)
        name = unit.relative_to(trees.stack).as_posix()
        if isinstance(deps, str):
            findings.append(f"{label}: the stack's {name} does not preprocess with the firmware's flags: {deps}")
            continue
        for dep in sorted(d.resolve() for d in deps):
            if dep != unit.resolve() and not dep.is_relative_to(public) and dep not in library:
                findings.append(f"{label}: the stack's {name} includes {where(dep, trees)}")
    return findings


def where(path: Path, trees: Trees) -> str:
    """A dependency, named by where it lives."""
    for root, label in ((trees.ctrl, "sw/firmware/ctrl/"), (trees.stack, "tsn-c-stack/"), (ROOT, "")):
        if path.is_relative_to(root.resolve()):
            return label + path.relative_to(root.resolve()).as_posix()
    return str(path)


def firmware_units(trees: Trees) -> list[Path]:
    """The firmware's sources and headers, and the measured images' own sources."""
    units = [p for d in FIRMWARE_DIRS for p in sorted((trees.ctrl / d).glob("*.[ch]"))]
    return units + [trees.ctrl / s for s in IMAGE_SOURCES]


def firmware_flags(trees: Trees, work: Path) -> list[str]:
    """The firmware's include path as its builds give it, with the stack's other directories last, and the
    SRP adapter's generated shape force-included as the SRP builds include it."""
    tree = Tree(trees.ctrl, trees.ctrl, trees.ctrl, stack=trees.stack)
    paths = [*includes(tree), f"-I{trees.ctrl / 'srp'}", f"-I{NVM_DIR / 'plat'}", f"-I{NVM_DIR / 'test/rv32'}",
             f"-I{LWSRP / 'include'}", f"-I{LWSRP}"]
    last = [f"-idirafter{trees.stack / d}" for d in STACK_PRIVATE]
    shape = work / "srp_entity_gen.h"
    work.mkdir(parents=True, exist_ok=True)
    res = run([sys.executable, "-B", str(CTRL / "srp/srp_entity.py"), str(SRP_ENTITY), "-o", str(shape)])
    if res.returncode != 0:
        raise Refusal(f"srp_entity.py refused {SRP_ENTITY.name}: {res.stderr.strip()}")
    return ["gcc", "-std=c11", *FIRMWARE_DEFINES, *paths, *last, "-include", str(shape), "-MG"]


def firmware_side(trees: Trees, work: Path) -> list[str]:
    """Every firmware unit reaches the stack through its public headers only."""
    argv = firmware_flags(trees, work)
    public = (trees.stack / STACK_INCLUDE).resolve()
    stack = trees.stack.resolve()
    findings = []
    for unit in firmware_units(trees):
        lang = ["-x", "c"] if unit.suffix == ".h" else []
        deps = dependencies([*argv, *lang], unit)
        name = unit.relative_to(trees.ctrl).as_posix()
        if isinstance(deps, str):
            findings.append(f"firmware: {name} does not preprocess: {deps}")
            continue
        for dep in sorted(d.resolve() for d in deps if d.is_absolute() or d.exists()):
            if dep.is_relative_to(stack) and not dep.is_relative_to(public):
                findings.append(f"firmware: {name} includes {where(dep, trees)}, not one of the stack's public "
                                "headers")
    return findings


def shadows(trees: Trees, firmware: Path) -> list[str]:
    """No file under sw/firmware is named as a source or public header of the stack."""
    names = {p.name for part in STACK_PARTS for p in (trees.stack / part).iterdir() if p.is_file()}
    roots = [trees.ctrl] + [p for p in firmware.iterdir() if p.is_dir() and p.resolve() != CTRL.resolve()]
    return [f"firmware: {p.relative_to(root.parent).as_posix()} has the name of the stack's {p.name}"
            for root in roots for p in sorted(root.rglob("*")) if p.is_file() and p.name in names]


def judge(trees: Trees, rv32: str | None, work: Path) -> list[str]:
    """Every finding on both sides of the boundary for these trees."""
    host = ["gcc", *C_FLAGS]
    findings = stack_side(trees, [*host, *includes(Tree(trees.ctrl, work, work, stack=trees.stack))],
                          c_library(host, work / "host-library"), "host")
    if rv32 is not None:
        cross = [rv32, *RV32_FLAGS, *fw_rv32.includes(rv32)]
        findings += stack_side(trees, [*cross, *includes(Tree(trees.ctrl, work, work, stack=trees.stack))],
                               c_library(cross, work / "rv32-library"), "rv32")
    findings += firmware_side(trees, work / "firmware")
    findings += shadows(trees, ROOT / "sw/firmware")
    return findings


def stack_gate(selftest: bool, work: Path) -> list[str]:
    """The stack's own boundary gate (and its self-test), from the submodule; its refusal is a finding."""
    for tool in ("cmake", "clang", "gcc", "nm"):
        if shutil.which(tool) is None:
            raise Refusal(f"the stack's gate needs {tool}")
    argv = [sys.executable, "-I", str(STACK_GATE), "--work", str(work), "--jobs", "4"]
    res = run([*argv, "--selftest"] if selftest else argv, cwd=work)
    lines = (res.stdout + res.stderr).strip().splitlines()
    for line in lines:
        print(f"    {line}")
    return [] if res.returncode == 0 else [f"the stack's own gate {STACK_GATE.relative_to(ROOT)} refused: exit "
                                           f"{res.returncode}"]


# ---- the planted controls -------------------------------------------------------------------

#: (name, the tree it is planted in, the file, its anchor, the replacement, a fragment of the finding or ""
#: for a control that must pass). Stack plants are written into the stack's copy, firmware plants into the
#: ctrl tree's copy, side by side, so a relative path from one reaches the other; a "+" file is written whole
#: as a new file.
PLANTS = (
    ("stack source includes the mailbox HAL", "stack", "src/adp.c", "#include <assert.h>\n",
     "#include <assert.h>\n#include \"mbx_hal.h\"\n", "the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    ("stack source includes the register-map contract", "stack", "src/acmp.c", "#include \"acmp.h\"\n",
     "#include \"acmp.h\"\n#include \"mbx_contract.h\"\n", "includes sw/firmware/ctrl/mbx/mbx_contract.h"),
    ("stack source includes the composition", "stack", "src/maap.c", "#include \"maap.h\"\n",
     "#include \"maap.h\"\n#include \"ctrl_app.h\"\n", "includes sw/firmware/ctrl/app/ctrl_app.h"),
    ("stack source includes the store's port", "stack", "src/maap.c", "#include \"maap.h\"\n",
     "#include \"maap.h\"\n#include \"nvm_state.h\"\n", "includes sw/firmware/ctrl_nvm/nvm_state.h"),
    ("stack source includes the loop through a macro", "stack", "src/adp.c", "#include <assert.h>\n",
     "#include <assert.h>\n#define TSN_LOOP \"ctrl_loop.h\"\n#include TSN_LOOP\n",
     "includes sw/firmware/ctrl/loop/ctrl_loop.h"),
    ("stack public header includes the platform's header", "stack", "include/wire.h", "#include <stdint.h>\n",
     "#include <stdint.h>\n#include \"ctrl_debug.h\"\n", "the stack's include/wire.h includes"),
    ("stack source includes a header nobody supplies", "stack", "src/adp.c", "#include <assert.h>\n",
     "#include <assert.h>\n#include \"image_layout.h\"\n", "does not preprocess with the firmware's flags"),
    ("stack source includes an OS header", "stack", "src/adp.c", "#include <assert.h>\n",
     "#include <assert.h>\n#include <unistd.h>\n", "includes "),
    ("firmware reaches a stack example's header", "ctrl", "adp/adp_mbx.c", "#include \"adp_mbx.h\"\n",
     "#include \"adp_mbx.h\"\n#include \"adp_port.h\"\n",
     "adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers"),
    ("firmware header reaches a stack source by a relative path", "ctrl", "maap/maap_mbx.h", "#include \"maap.h\"\n",
     "#include \"maap.h\"\n#include \"../../tsn-c-stack/src/maap.c\"\n",
     "includes tsn-c-stack/src/maap.c, not one of the stack's public headers"),
    ("image source reaches a stack test's header", "ctrl", "test/rv32_image/image_main.c", "#include \"ctrl_app.h\"\n",
     "#include \"ctrl_app.h\"\n#include \"../../../tsn-c-stack/tests/acmp_fake.hpp\"\n",
     "test/rv32_image/image_main.c includes tsn-c-stack/tests/acmp_fake.hpp"),
    ("a copy of the stack's wire.h in the firmware", "ctrl", "+mbx/wire.h", "", "#include <stdint.h>\n",
     "mbx/wire.h has the name of the stack's wire.h"),
    ("a copy of the stack's adp.c in the firmware", "ctrl", "+adp/adp.c", "", "int adp_copy;\n",
     "adp/adp.c has the name of the stack's adp.c"),
    ("pass: the firmware includes a public header", "ctrl", "port/ctrl_debug.c", "#include \"ctrl_debug.h\"\n",
     "#include \"ctrl_debug.h\"\n#include \"wire.h\"\n", ""),
    ("pass: the stack includes only its own header and the C library", "stack", "src/maap.c", "#include \"maap.h\"\n",
     "#include \"maap.h\"\n#include \"wire.h\"\n#include <stdint.h>\n", ""),
)


def planted(plant: tuple[str, str, str, str, str, str], work: Path) -> Trees:
    """Copies of the trees with one plant written into them."""
    name, side, rel, old, new, _ = plant
    trees = Trees(work / "ctrl", work / "tsn-c-stack")
    for path in trees.ctrl, trees.stack:
        if path.exists():
            shutil.rmtree(path)
    shutil.copytree(CTRL, trees.ctrl, ignore=shutil.ignore_patterns("__pycache__"))
    for part in dict.fromkeys((*STACK_PARTS, *STACK_PRIVATE)):
        shutil.copytree(STACK / part, trees.stack / part)
    root = trees.stack if side == "stack" else trees.ctrl
    if rel.startswith("+"):
        target = root / rel[1:]
        if target.exists():
            raise Refusal(f"control {name!r}: {rel[1:]} exists already")
        target.write_text(new, encoding="utf-8")
        return trees
    target = root / rel
    text = target.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise Refusal(f"control {name!r}: its anchor occurs {text.count(old)} times in {rel}")
    target.write_text(text.replace(old, new), encoding="utf-8")
    return trees


def controls(rv32: str | None, work: Path) -> int:
    """Every plant refused by the finding it names, every pass control passing; the misbehaving count."""
    bad = 0
    for plant in PLANTS:
        name, needle = plant[0], plant[5]
        trees = planted(plant, work / "plants")
        findings = judge(trees, rv32, work / "plants-build")
        ok = (not findings) if not needle else any(needle in f for f in findings)
        print(f"[{'ok' if ok else 'ESCAPED'}] boundary control {name}: "
              f"{'passes' if not findings else findings[0]}")
        bad += not ok
    shutil.rmtree(work / "plants", ignore_errors=True)
    return bad


def pin_controls(work: Path) -> int:
    """The pin check (ctrl_build.stack_pin, which every gate runs first) passes a clone of the stack at its
    gitlink and refuses, by name, the same clone with a source or a test edited, and at another revision.
    Returns the misbehaving count."""
    clone = work / "pin-clone"
    pin = stack_gitlink()
    if run(["git", "clone", "--quiet", "--no-hardlinks", str(STACK), str(clone)]).returncode or \
            run(["git", "-C", str(clone), "checkout", "--quiet", pin]).returncode:
        raise Refusal(f"cannot clone {STACK.relative_to(ROOT)} at {pin} for the pin controls")
    source, test = clone / "src/adp.c", clone / "tests/test_adp.cpp"
    pristine = {path: path.read_text(encoding="utf-8") for path in (source, test)}
    arms = (("the pinned clone, unmodified", lambda: None, ""),
            ("a core source edited", lambda: source.write_text(pristine[source] + "/* local */\n"),
             "differs from the pinned"),
            ("a core test edited", lambda: test.write_text(pristine[test] + "// local\n"), "differs from the pinned"),
            ("another revision checked out",
             lambda: run(["git", "-C", str(clone), "checkout", "--quiet", "HEAD~1"]), "is not the pinned"))
    bad = 0
    for what, spoil, needle in arms:
        for path, text in pristine.items():
            path.write_text(text, encoding="utf-8")
        spoil()
        try:
            stack_pin(clone, pin)
            ok, detail = not needle, "accepted"
        except Refusal as exc:
            ok, detail = bool(needle) and needle in str(exc), str(exc)
        print(f"[{'ok' if ok else 'ESCAPED'}] tsn-c-stack pin control, {what}: {detail}")
        bad += not ok
    shutil.rmtree(clone)
    return bad


def main(argv: list[str] | None = None) -> int:
    """Hold both sides, then the stack's own gate; with --selftest, the controls first."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--selftest", action="store_true", help="also plant every control and require its verdict")
    ap.add_argument("--require-rv32", action="store_true", help="refuse, not skip, without an RV32 compiler")
    args = ap.parse_args(argv)
    rv32 = fw_rv32.compiler()
    if rv32 is None and args.require_rv32:
        print("REFUSED: no RV32 compiler (the pinned SDK's riscv32-linux-gcc or MILAN_RV32_CC)")
        return 2
    if rv32 is None:
        print("  SKIPPED: the RV32 arm, no RV32 compiler; --require-rv32 refuses instead")
    try:
        with tempfile.TemporaryDirectory(prefix="ctrl-boundary-") as tmp:
            work = Path(tmp)
            print(f"tsn-c-stack at {stack_pin()}")
            bad = controls(rv32, work) + pin_controls(work) if args.selftest else 0
            findings = judge(Trees(CTRL, STACK), rv32, work / "checkout")
            findings += stack_gate(args.selftest, work)
    except Refusal as exc:
        print(f"REFUSED: {exc}")
        return 2
    for finding in findings:
        print(f"  [FAIL] {finding}")
    units = len(firmware_units(Trees(CTRL, STACK)))
    print(f"ctrl_boundary: {units} firmware units and the stack's sources and headers, host"
          f"{' and RV32' if rv32 else ''}; {len(findings)} finding(s)"
          f"{f', {len(PLANTS)} boundary and 4 pin controls, {bad} misbehaved' if args.selftest else ''}")
    print(f"ctrl_boundary: {'FAIL' if findings or bad else 'PASS'}")
    return 1 if findings or bad else 0


if __name__ == "__main__":
    sys.exit(main())
