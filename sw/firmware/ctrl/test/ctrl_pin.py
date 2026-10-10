# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_pin.py - the TSN stack's pin, held at every gate that builds the stack (#697).

The pin check itself is ctrl_build.stack_pin: the submodule at its gitlink,
every file of its sources, headers, tests, examples, scripts and CMake files
hashing to the gitlink's tree. Every Python gate that builds the stack calls it
first. This module holds the rest, for the boundary gate (ctrl_boundary.py).

THE MAKEFILES. A Makefile among the firmware's builders is read with make's
own database (make -p) and dry run (make -n -B --trace), never restated here,
with the stack it builds named through STACK_DIR. A target whose own recipe
names that stack (its include path, its sources) must have a target that runs
the pin check (ctrl_build.py --stack-pin) as a prerequisite, so no target
reaches the stack unpinned, whichever target is run alone; a recipe that names
the checkout's stack rather than STACK_DIR's is refused too, since no stack
could be checked in its place.

THE CONTROLS (pin_controls, under ctrl_boundary.py --selftest). The pin check
passes a clone of the stack at its gitlink and refuses, by name, the clone with
a source, a test, a script or a CMake file edited, with an edit hidden from
git status, with a file the tree does not hold, and at another revision. The
MAAP differential (both its modes) and the AECP lane's arms, campaign and wire
comparison refuse an edited clone before building it. Then every target of
every Makefile builder whose dry run reaches the stack is run for real, in a
scratch copy of its directory (the rest of the checkout linked, so its paths
reach what they reach in the checkout), with the system's compilers and a
simulator that builds nothing, against a clone whose wire.h is poisoned: each
must refuse on the pin check and never compile the poisoned header. A planted
copy of the mailbox bench's Makefile whose run-if2 lacks the pin prerequisite
must be refused by name.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from ctrl_build import HERE, PP, ROOT, STACK, Refusal, stack_gitlink, stack_pin
from ctrl_capture import COMPILER

#: A target make's database does not hold: asked for so make prints the database and runs nothing.
NO_GOAL = "ctrl-pin-no-such-goal"
#: make --trace's line before each target's commands, the target in group 1.
TRACE = re.compile(r"^\S+:\d+: (?:update )?target '(.+?)'")
#: What a recipe line that runs the pin check holds.
PIN_RUN = "--stack-pin"
#: The checkout's stack, however a recipe names it (relative or absolute).
CHECKOUT_STACK = STACK.relative_to(ROOT).as_posix()
#: The line the poisoned clone's wire.h ends with; a build that reads it fails naming it.
POISON = "#error PIN-POISON: the poisoned tsn-c-stack was compiled"
#: A simulator that builds nothing: it writes, where Verilator would build it, an executable that passes.
NO_SIMULATOR = '''import sys
from pathlib import Path
args = sys.argv[1:]
if "--Mdir" in args and "-o" in args:
    exe = Path(args[args.index("--Mdir") + 1]) / args[args.index("-o") + 1]
    exe.parent.mkdir(parents=True, exist_ok=True)
    exe.write_text("#!/bin/sh\\nexit 0\\n", encoding="utf-8")
    exe.chmod(0o755)
'''
#: The planted Makefile control: the mailbox bench's run-if2 without the pin check as its prerequisite.
UNPINNED = (ROOT / "tb/verilator/mbx/Makefile", "run-if2: if2-gen | stack-pin\n", "run-if2: if2-gen\n", "run-if2")
#: How long one bench target may run against the poisoned clone before it is a failure.
BENCH_TIMEOUT_S = 900


def run(argv: list[str], cwd: Path | None = None, env: dict[str, str] | None = None,
        timeout: int | None = None) -> tuple[int, str]:
    """One tool, its output and errors interleaved, its messages in English."""
    try:
        res = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                             check=False, env={**os.environ, "LC_ALL": "C", **(env or {})}, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout} s"
    return res.returncode, res.stdout


def make(makefile: Path, *args: str, timeout: int | None = None, env: dict[str, str] | None = None) -> tuple[int, str]:
    """make on one Makefile, in its directory."""
    return run(["make", "--no-print-directory", "-C", str(makefile.parent), "-f", makefile.name, *args],
               env=env, timeout=timeout)


def targets(makefile: Path, overrides: list[str], env: dict[str, str] | None = None) -> dict[str, frozenset[str]]:
    """Every target the Makefile defines, special and pattern ones aside, with all its prerequisites (normal
    and order-only), from make's own database."""
    _, out = make(makefile, "-p", "-n", "-q", "-R", *overrides, NO_GOAL, env=env)
    files = out.partition("\n# Files\n")[2].partition("\n# files hash-table stats")[0]
    if not files:
        raise Refusal(f"make printed no database for {makefile.relative_to(ROOT)}")
    found = {}
    for entry in files.split("\n\n"):
        lines = [ln for ln in entry.splitlines() if ln]
        rule = next((ln for ln in lines if not ln.startswith(("#", "\t"))), None)
        if rule is None or any(ln.startswith("# Not a target") for ln in lines):
            continue
        name, sep, rest = rule.partition(":")
        if sep and not name.startswith(".") and "%" not in name:
            found[name.strip()] = frozenset(rest.lstrip(":").replace("|", " ").split())
    return found


def recipes(makefile: Path, target: str, overrides: list[str],
            env: dict[str, str] | None = None) -> dict[str, list[str]]:
    """Each target make's dry run of `target` would build (it and its prerequisites, every one remade), with the
    command lines of its own recipe."""
    _, out = make(makefile, "-n", "-B", "--trace", *overrides, target, env=env)
    own: dict[str, list[str]] = {}
    current = None
    for line in out.splitlines():
        if m := TRACE.match(line):
            current = m[1]
            own.setdefault(current, [])
        elif current is not None:
            own[current].append(line)
    return own


def stack_targets(makefile: Path, stack: Path) -> tuple[list[str], list[str], list[str]]:
    """The Makefile's targets whose build reaches `stack` (STACK_DIR), those that run the pin check, and the
    findings: each target whose own recipe names the stack without one that runs the pin check among its
    prerequisites, and each that names the checkout's stack instead."""
    overrides = [f"STACK_DIR={stack}"]
    defined = targets(makefile, overrides)
    built = {name: recipes(makefile, name, overrides) for name in defined}
    pins = {t for own in built.values() for t, lines in own.items() if any(PIN_RUN in ln for ln in lines)}
    where = makefile.relative_to(ROOT).as_posix() if makefile.is_relative_to(ROOT) else makefile.name
    reaching, findings = [], {}
    for name, own in built.items():
        if any(str(stack) in ln for lines in own.values() for ln in lines):
            reaching.append(name)
        for target, lines in own.items():
            if target in pins:
                continue
            if any(CHECKOUT_STACK in ln for ln in lines):
                findings[f"{where}: {target} builds the checkout's tsn-c-stack, not the STACK_DIR it is given"] = None
            elif any(str(stack) in ln for ln in lines) and not defined.get(target, frozenset()) & pins:
                findings[f"{where}: {target} builds against tsn-c-stack without the pin check "
                         f"({', '.join(sorted(pins)) or 'none'}) as a prerequisite"] = None
    return reaching, sorted(pins), list(findings)


def named_compilers(makefile: Path, env: dict[str, str]) -> list[dict]:
    """Each compiler a Makefile's recipes run by a path no capture wrapper stands on (`env`'s CTRL_CAPTURE_BIN),
    read from make's own dry run of every target under the capture's environment: a bypass record of each, as
    the capture's audit hook writes one for a Python builder."""
    wrappers = Path(env["CTRL_CAPTURE_BIN"]).resolve()
    where = makefile.relative_to(ROOT).as_posix() if makefile.is_relative_to(ROOT) else makefile.name
    found = {}
    for target in targets(makefile, [], env):
        for own, lines in recipes(makefile, target, [], env).items():
            for line in lines:
                for word in re.split(r"[\s;&|()`]+", line):
                    word = word.strip("'\"")
                    if "/" in word and COMPILER.match(word.rpartition("/")[2]) and \
                            (makefile.parent / word).resolve().parent != wrappers:
                        found[(word, line)] = {"bypass": word, "args": [line], "cwd": str(makefile.parent),
                                               "from": [f"{where} (target {own})"]}
    return list(found.values())


def makefile_findings(makefiles: list[Path], work: Path) -> list[str]:
    """Every Makefile builder's targets that build the stack take the pin check first: judged with STACK_DIR a
    link to the submodule, so a recipe naming the submodule itself is told apart."""
    link = work / "tsn-c-stack-link"
    work.mkdir(parents=True, exist_ok=True)
    if not link.is_symlink():
        link.symlink_to(STACK, target_is_directory=True)
    return [f for makefile in makefiles for f in stack_targets(makefile, link)[2]]


def mirror(directory: Path, into: Path) -> Path:
    """A scratch checkout for one directory of it: the directory's files copied (tracked, or new and not
    ignored), every other entry of the checkout linked, so its relative paths reach what they reach in the
    checkout and what it writes stays in the copy."""
    if into.exists():
        shutil.rmtree(into)
    here, there = ROOT, into
    for part in directory.relative_to(ROOT).parts:
        there.mkdir(parents=True, exist_ok=True)
        for entry in here.iterdir():
            if entry.name != part:
                (there / entry.name).symlink_to(entry)
        here, there = here / part, there / part
    rc, out = run(["git", "-C", str(directory), "ls-files", "-z", "--cached", "--others", "--exclude-standard", "."])
    if rc:
        raise Refusal(f"cannot list {directory.relative_to(ROOT)}: {out.strip()}")
    for name in filter(None, out.split("\0")):
        if (directory / name).is_file():
            (there / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(directory / name, there / name)
    return there


def bench_arms(makefiles: list[Path], clone: Path, work: Path, edited: str) -> list[tuple]:
    """For every target of every Makefile builder that reaches the stack in its dry run: run it in a scratch
    copy of its directory against the clone with wire.h poisoned, with no simulator; it must refuse on the pin
    check and never reach the poisoned header; each target that runs the pin check passes the clone
    unpoisoned. And the planted Makefile without the pin prerequisite."""
    simulator = work / "no_simulator.py"
    simulator.write_text(NO_SIMULATOR, encoding="utf-8")

    def poison() -> None:
        """The clone's wire.h, which every firmware build reads, ends in an #error."""
        wire = clone / "include/wire.h"
        wire.write_text(wire.read_text(encoding="utf-8") + f"\n{POISON}\n", encoding="utf-8")

    def bench(makefile: Path, target: str) -> tuple[bool, str]:
        """The target run for real in a fresh scratch copy: accepted, and its verdict on the stack."""
        copy = mirror(makefile.parent, work / "bench") / makefile.name
        rc, out = make(copy, f"STACK_DIR={clone}", f"VERILATOR={sys.executable} -I {simulator}", target,
                       timeout=BENCH_TIMEOUT_S)
        said = [ln for ln in out.splitlines() if "tsn-c-stack" in ln or "PIN-POISON" in ln]
        if "PIN-POISON" in out:
            return True, f"exit {rc}: compiled the poisoned header: {said[-1].strip()}"
        return rc == 0, f"exit {rc}: {said[-1].strip() if said else 'no pin verdict'}"

    def unpinned() -> tuple[bool, str]:
        """The planted Makefile, judged as the gate judges every Makefile builder."""
        makefile, old, new, _ = UNPINNED
        copy = mirror(makefile.parent, work / "bench") / makefile.name
        text = copy.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise Refusal(f"the planted Makefile control's anchor occurs {text.count(old)} times")
        copy.write_text(text.replace(old, new), encoding="utf-8")
        found = makefile_findings([copy], work / "unpinned")
        return not found, found[0] if found else "no finding"

    arms = []
    for makefile in makefiles:
        where = makefile.relative_to(ROOT).as_posix()
        reaching, pins, _ = stack_targets(makefile, clone)
        arms += [(f"{where} make {pin}, the pinned clone", lambda: None, lambda m=makefile, t=pin: bench(m, t), "")
                 for pin in pins]
        for target in reaching:
            arms.append((f"{where} make {target}, the stack's wire.h poisoned", poison,
                         lambda m=makefile, t=target: bench(m, t), edited + "include/wire.h"))
    arms.append((f"{UNPINNED[0].relative_to(ROOT).as_posix()} planted with {UNPINNED[3]} unpinned", lambda: None,
                 unpinned, f"{UNPINNED[3]} builds against tsn-c-stack without the pin check"))
    return arms


def pin_controls(work: Path, makefiles: list[Path]) -> tuple[int, int]:
    """The shared pin check passes a clone of the stack at its gitlink and refuses, by name, the clone with a
    source, a test, a script or a CMake file edited, with an edit hidden from git status, with a header the
    gitlink's tree does not hold, and at another revision; the MAAP differential (both modes) and the AECP
    lane's arms, campaign and wire comparison refuse an edited one before building it; every Makefile
    builder's target that reaches the stack refuses a poisoned one on the pin check. Returns the misbehaving
    count and the number of controls."""
    pin = stack_gitlink()
    clone = work / "pin-clone"
    edited = f"differs from the pinned {pin[:8]}: "

    def fresh() -> None:
        """A new clone of the stack at its gitlink, for the next control."""
        if clone.exists():
            shutil.rmtree(clone)
        if run(["git", "clone", "--quiet", "--no-hardlinks", str(STACK), str(clone)])[0] or \
                run(["git", "-C", str(clone), "-c", "advice.detachedHead=false", "checkout", "--quiet", pin])[0]:
            raise Refusal(f"cannot clone {STACK.relative_to(ROOT)} at {pin} for the pin controls")

    def append(rel: str) -> None:
        """One line added to a file of the clone."""
        (clone / rel).write_text((clone / rel).read_text(encoding="utf-8") + "\n", encoding="utf-8")

    def hidden() -> None:
        """A source edited and hidden from git status by the index's assume-unchanged flag."""
        append("src/adp.c")
        if run(["git", "-C", str(clone), "update-index", "--assume-unchanged", "src/adp.c"])[0]:
            raise Refusal("cannot hide the pin control's edit from git status")

    def direct() -> tuple[bool, str]:
        """The pin check itself on the clone: accepted, and what it said."""
        try:
            return True, f"accepted {stack_pin(clone, pin)}"
        except Refusal as exc:
            return False, str(exc)

    def tool(argv: list[str], env: dict[str, str] | None = None) -> tuple[bool, str]:
        """A gate run on the clone: accepted (exit 0), and its last line about the stack."""
        rc, out = run(argv, env=env)
        said = [ln for ln in out.splitlines() if "tsn-c-stack" in ln]
        return rc == 0, f"exit {rc}: {said[-1].strip() if said else 'no pin verdict'}"

    def differential(*extra: str) -> tuple[bool, str]:
        """The MAAP differential on the clone, with a simulator that always fails."""
        return tool([sys.executable, "-B", str(HERE / "maap_differential.py"), "--stack", str(clone), *extra],
                    {"VERILATOR": "false"})

    def aecp(script: str, *extra: str) -> tuple[bool, str]:
        """One of the AECP lane's tools on the clone, with a simulator that always fails."""
        return tool([sys.executable, "-B", str(HERE / script), "--stack", str(clone), "--output",
                     str(work / "aecp-out"), *extra], {"VERILATOR": "false"})

    arms = [("the pinned clone, unmodified", lambda: None, direct, ""),
            ("a core source edited", lambda: append("src/adp.c"), direct, edited + "src/adp.c"),
            ("a core test edited", lambda: append("tests/test_adp.cpp"), direct, edited + "tests/test_adp.cpp"),
            ("a stack script edited", lambda: append("scripts/check_boundary.py"), direct,
             edited + "scripts/check_boundary.py"),
            ("a CMake file edited", lambda: append("CMakeLists.txt"), direct, edited + "CMakeLists.txt"),
            ("an edit hidden from git status (assume-unchanged)", hidden, direct, edited + "src/adp.c"),
            ("a header the pinned tree does not hold", lambda: (clone / "include/stdint.h").write_text(""), direct,
             edited + "include/stdint.h"),
            ("another revision checked out",
             lambda: run(["git", "-C", str(clone), "checkout", "--quiet", "HEAD~1"]), direct, "is not the pinned"),
            ("the MAAP differential, a core source edited", lambda: append("src/maap.c"), differential,
             edited + "src/maap.c"),
            ("the MAAP differential's self-test, a core source edited", lambda: append("src/maap.c"),
             lambda: differential("--self-test"), edited + "src/maap.c"),
            ("the AECP arms, a core source edited", lambda: append("src/acmp.c"), lambda: aecp("aecp_arms.py", "--app"),
             edited + "src/acmp.c"),
            ("the AECP campaign, a core source edited", lambda: append("src/acmp.c"),
             lambda: aecp("aecp_mutants.py", "--shard", "0", "1000"), edited + "src/acmp.c"),
            ("the AECP wire comparison, the stack's wire layer edited", lambda: append("include/wire.h"),
             lambda: aecp("aecp_wire.py", "--reference", str(PP), "--verilator", "false"), edited + "include/wire.h")]
    fresh()
    arms += bench_arms(makefiles, clone, work, edited)
    bad = 0
    for what, spoil, check, needle in arms:
        fresh()
        spoil()
        accepted, detail = check()
        ok = accepted if not needle else (not accepted and needle in detail)
        print(f"[{'ok' if ok else 'ESCAPED'}] tsn-c-stack pin control, {what}: {detail}", flush=True)
        bad += not ok
    for scratch in (clone, work / "aecp-out", work / "bench", work / "unpinned"):
        shutil.rmtree(scratch, ignore_errors=True)
    return bad, len(arms)
