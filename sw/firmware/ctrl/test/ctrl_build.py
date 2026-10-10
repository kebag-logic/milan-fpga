# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_build.py - the build helpers of the control-plane firmware's host test.

The firmware is compiled from a Tree: the checkout, or a copy a planted defect
was written into (ctrl_mutants.py), with every object and executable under the
tree's own output directory, never in the checkout. The tests are GoogleTest
(sw/firmware/gtest/README.md): always compiled from the checkout's test
sources against the tree's headers, so a defect planted in a .c file reuses
every test object and one planted in a header rebuilds the tests that see it.

The ADP, ACMP and MAAP cores and the wire layer are the TSN stack's, from the
pinned tsn-c-stack submodule (#697): a tree names them, and the stack's own
core tests, with STACK_PREFIX, and builds them from its stack (the submodule,
or a copy a defect was planted in). The firmware includes only the stack's
public headers (its include/), and nothing of the stack includes the firmware
(ctrl_boundary.py).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
CTRL = HERE.parent
ROOT = CTRL.parents[2]
HARNESS = ROOT / "sw/firmware/gtest"
sys.path.insert(0, str(HARNESS))

import fw_gtest  # noqa: E402

PP = ROOT / "protocol-processor"
PP_ADP_SIM = "tb/adp_engine/sim_main.cpp"
PP_ADP_PKG = PP / "hdl/adp/pp_adp_pkg.sv"
TB_MBX = ROOT / "tb/verilator/mbx"
TB_COMMON = ROOT / "tb/common"

#: The TSN stack: the tsn-c-stack submodule at its gitlink (#697).
STACK = ROOT / "third_party/tsn-c-stack"
#: A source or test named with this prefix is the stack's, the rest of the name
#: inside it; every other name is the ctrl tree's.
STACK_PREFIX = "tsn-c-stack/"
#: The stack's parts a tree builds from: its sources and its public headers. Its
#: tests are always the checkout's, as the ctrl tree's are.
STACK_PARTS = ("src", "include")
#: The stack's public headers, the only part of it the firmware includes.
STACK_INCLUDE = "include"
#: The stack's core tests and their fakes (acmp_fake.hpp), in the checkout.
STACK_TESTS = STACK / "tests"

#: The firmware every target links: the driver, the loop, the port layer, ADP, ACMP, the app.
#: The order is the link order of the measured images (ctrl_image.py, ctrl_srp_image.py).
PORTABLE = ("mbx/mbx.c", "loop/ctrl_loop.c", "port/ctrl_pool.c", "port/ctrl_debug.c", "port/shlan_port.c",
            "tsn-c-stack/src/adp.c", "adp/adp_mbx.c", "tsn-c-stack/src/maap.c", "maap/maap_mbx.c",
            "maap/maap_csr.c", "tsn-c-stack/src/acmp.c", "acmp/acmp_mbx.c", "acmp/acmp_nvm.c", "app/ctrl_app.c")
#: The host side: the model and mbx_hal.h on it. Test equipment, never measured.
HOST = ("host/mbx_model.c", "host/mbx_plat_host.c")
INCLUDE_DIRS = ("mbx", "host", "port", "loop", "adp", "maap", "acmp", "app", "test")
#: The saved-state store's state port (nvm_state.h), which acmp_nvm.c serves.
NVM_DIR = ROOT / "sw/firmware/ctrl_nvm"
C_FLAGS = ("-std=c11", "-O2", "-DNDEBUG", "-Wall", "-Wextra", "-Werror", "-pedantic")

RV32_FLAGS = ("-march=rv32i", "-mabi=ilp32", "-ffreestanding", "-fno-stack-protector", "-Os", "-DNDEBUG",
              "-std=c11", "-Wall",
              "-Wextra", "-Werror", "-pedantic", "-fstack-usage", "-DCTRL_MBX_BASE=0x80000000u")
#: Runtime interfaces an object-only check may leave undefined, including the
#: assertion handler when a debug build enables a protocol's re-entry guard.
RV32_LIBC = frozenset({"memset", "memcpy", "vsnprintf", "__assert_fail"})


class Refusal(Exception):
    """The gate cannot run as asked; exit 2, never a pass."""


@dataclass(frozen=True)
class Tree:
    """Where the firmware sources come from and where its builds go."""

    src: Path
    out: Path
    reuse: Path
    build: fw_gtest.Build = field(default_factory=lambda: fw_gtest.Build(jobs=4))
    #: the stack's root: its src/ and include/ (the submodule, or a planted copy)
    stack: Path = STACK


@dataclass(frozen=True)
class Outcome:
    """One arm's verdict and its output."""

    arm: str
    rc: int
    log: str


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """One subprocess, its output captured."""
    return fw_gtest.run(argv, cwd=cwd)


def includes(tree: Tree) -> list[str]:
    """The firmware's include path, from the tree being built and its stack's public headers, then the harness."""
    return ([f"-I{tree.src / d}" for d in INCLUDE_DIRS] + [f"-I{tree.stack / STACK_INCLUDE}"] +
            [f"-I{NVM_DIR}", f"-I{HARNESS}"])


def compile_c(tree: Tree, sources: list[Path], tag: str, extra: tuple[str, ...] = (),
              measured: bool = True) -> list[Path]:
    """Compile C sources to objects under out/<tag>; a compile error refuses the arm."""
    try:
        return fw_gtest.compile_c(tree.build, C_FLAGS, [*includes(tree), *extra], sources, tree.out / tag, measured)
    except fw_gtest.BuildError as exc:
        raise Refusal(str(exc)) from exc


def firmware(tree: Tree, names: tuple[str, ...], tag: str) -> list[Path]:
    """The firmware sources `names` (measured) and the host model (not) as objects."""
    return (compile_c(tree, sources(tree, names), tag) +
            compile_c(tree, sources(tree, HOST), f"{tag}/host", measured=False))


def test_source(name: str) -> Path:
    """A test source of the checkout: the stack's tests/ for a STACK_PREFIX name, else this test/."""
    return STACK / name.removeprefix(STACK_PREFIX) if name.startswith(STACK_PREFIX) else HERE / name


def compile_tests(tree: Tree, names: tuple[str, ...], tag: str, extra: tuple[str, ...] = ()) -> list[Path]:
    """The GoogleTest sources `names` (from the checkout's test/, or the stack's tests/) against the
    tree's headers; the stack's test fakes (acmp_fake.hpp) are the checkout's too."""
    try:
        return fw_gtest.compile_tests(tree.build, [*includes(tree), f"-I{STACK_TESTS}", *extra],
                                      [test_source(n) for n in names], tree.out / tag)
    except fw_gtest.BuildError as exc:
        raise Refusal(str(exc)) from exc


def label(tree: Tree, text: str) -> Path:
    """The tally label of a binary whose test files name none: the stack's tests carry no FW_TALLY_LABEL."""
    try:
        return fw_gtest.label_object(tree.build, text, tree.out / "labels")
    except fw_gtest.BuildError as exc:
        raise Refusal(str(exc)) from exc


def link(tree: Tree, name: str, objects: list[Path]) -> Path:
    """Link objects with the harness's main into out/<name>."""
    try:
        main = fw_gtest.main_object(tree.build, tree.out / "harness")
        return fw_gtest.link(tree.build, [*objects, main], tree.out / name)
    except fw_gtest.BuildError as exc:
        raise Refusal(str(exc)) from exc


def execute(arm: str, exe: Path) -> Outcome:
    """Run one test binary and grade it as the sweep grades a suite log."""
    ok, log = fw_gtest.run_binary(exe)
    return Outcome(arm, 0 if ok else 1, log)


def source(src: Path, stack: Path, name: str) -> Path:
    """One firmware source: the stack's for a STACK_PREFIX name, else the ctrl tree's."""
    return stack / name.removeprefix(STACK_PREFIX) if name.startswith(STACK_PREFIX) else src / name


def sources(tree: Tree, names: tuple[str, ...]) -> list[Path]:
    """Paths of firmware sources inside the tree and its stack."""
    return [source(tree.src, tree.stack, n) for n in names]


def stack_gitlink(root: Path = ROOT) -> str:
    """The tsn-c-stack revision the repository at `root` records: one stage-0 gitlink, or a Refusal."""
    rel = STACK.relative_to(ROOT).as_posix()
    entry = run(["git", "-C", str(root), "ls-files", "--stage", "--", rel]).stdout.split()
    if len(entry) != 4 or entry[0] != "160000" or entry[2] != "0":
        raise Refusal(f"{rel} is not one stage-0 gitlink")
    return entry[1]


#: What the pin check proves file by file: everything of the stack a gate builds, runs or searches (its
#: sources, public headers, tests, examples, scripts and CMake files).
STACK_PROVEN = ("src", "include", "tests", "examples", "scripts", "cmake", "CMakeLists.txt")


def blob_id(path: Path, algorithm: str) -> str:
    """The object id git gives `path`'s content as a blob (a symbolic link's is its target), read from the
    file itself and never from an index."""
    data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
    return hashlib.new(algorithm, b"blob %d\0" % len(data) + data).hexdigest()


def worktree_files(stack: Path) -> set[str]:
    """Every file and symbolic link on disk under STACK_PROVEN, relative to the stack."""
    found = set()
    for part in STACK_PROVEN:
        top = stack / part
        if top.is_symlink() or top.is_file():
            found.add(part)
        for here, dirs, files in os.walk(top):
            found |= {(Path(here) / n).relative_to(stack).as_posix() for n in files}
            found |= {(Path(here) / n).relative_to(stack).as_posix() for n in dirs if (Path(here) / n).is_symlink()}
    return found


def stack_pin(stack: Path = STACK, pin: str | None = None) -> str:
    """Refuse a stack checkout that is not at the recorded gitlink, or whose content under STACK_PROVEN is not
    the gitlink's tree: every file is hashed as git hashes a blob and compared with that tree, and a file the
    tree does not hold is refused too. The index is never consulted, so an edit hidden from `git status`
    (assume-unchanged, skip-worktree) is refused like any other: every gate builds the pinned stack or none."""
    pin = pin or stack_gitlink()
    top = run(["git", "-C", str(stack), "rev-parse", "--show-toplevel"])
    if top.returncode or Path(top.stdout.strip()).resolve() != stack.resolve():
        raise Refusal(f"{stack} is not its own checkout: initialise the tsn-c-stack submodule")
    head = run(["git", "-C", str(stack), "rev-parse", "HEAD"]).stdout.strip()
    if head != pin:
        raise Refusal(f"tsn-c-stack at {head or 'no HEAD'} is not the pinned {pin}")
    algorithm = run(["git", "-C", str(stack), "rev-parse", "--show-object-format"]).stdout.strip()
    tree = run(["git", "-C", str(stack), "ls-tree", "-r", "-z", "--full-tree", pin, "--", *STACK_PROVEN])
    if tree.returncode or algorithm not in hashlib.algorithms_available:
        raise Refusal(f"cannot read the pinned tree {pin[:8]} of {stack}: {tree.stderr.strip()}")
    want = {}
    for entry in filter(None, tree.stdout.split("\0")):
        meta, name = entry.split("\t", 1)
        mode, kind, oid = meta.split()
        want[name] = (mode, kind, oid)
    differ = []
    for name in sorted(want.keys() | worktree_files(stack)):
        path, (mode, kind, oid) = stack / name, want.get(name, ("", "", ""))
        if kind != "blob" or path.is_symlink() != (mode == "120000") or not (path.is_symlink() or path.is_file()) \
                or blob_id(path, algorithm) != oid:
            differ.append(name)
    if differ:
        raise Refusal(f"tsn-c-stack differs from the pinned {pin[:8]}: {', '.join(differ)}")
    return head


#: Where each stack file lived in sw/firmware/ctrl before #697 moved the cores
#: into the submodule (the file map of the stack's import record). A tree of an
#: older revision (ctrl_image.py --base, ctrl_srp_image.py --ctrl-source) still
#: holds them there.
LEGACY = {"src/adp.c": "adp/adp.c", "src/acmp.c": "acmp/acmp.c", "src/maap.c": "maap/maap.c",
          "include/adp.h": "adp/adp.h", "include/acmp.h": "acmp/acmp.h", "include/maap.h": "maap/maap.h",
          "include/wire.h": "wire/wire.h"}


def legacy_stack(ctrl: Path, into: Path) -> Path | None:
    """For a ctrl tree from before #697, which holds its own cores, a copy of them in the stack's layout
    under `into`; None for a tree that holds none. An older tree holds fewer (no ACMP before lane F3), and
    a source the copy lacks is one its tree lacks."""
    held = {new: old for new, old in LEGACY.items() if (ctrl / old).is_file()}
    if not held:
        return None
    for new, old in held.items():
        (into / new).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ctrl / old, into / new)
    return into


def main(argv: list[str] | None = None) -> int:
    """The pin check from a command line, for the gates that are not Python (the mailbox bench's Makefile):
    exit 0 with the pinned revision, or 2 with the refusal."""
    ap = argparse.ArgumentParser(description="Refuse a tsn-c-stack checkout off its gitlink or differing from it.")
    ap.add_argument("--stack-pin", type=Path, nargs="?", const=STACK, required=True, metavar="DIR",
                    help="the stack checkout a gate builds (default: the submodule)")
    args = ap.parse_args(argv)
    try:
        print(f"tsn-c-stack at {stack_pin(args.stack_pin.resolve())}")
    except Refusal as exc:
        print(f"REFUSED: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
