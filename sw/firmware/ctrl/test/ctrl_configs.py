# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_configs.py - the firmware's builders, and what a capture of their compiles must hold (#697).

The boundary gate (ctrl_boundary.py) judges the compiles a capture of the
builders' compiler invocations holds (ctrl_capture.py); this module says which
builders those are and refuses a capture that does not hold them whole.

THE BUILDERS. BUILDERS is the known set: every builder of the firmware that
compiles, each with the commands that run it when the gate makes the capture
itself: its builds, not its suites (a suite builder's --build-only builds
every binary and image its suites build, and runs and plants nothing). A
capture judged must hold an invocation of each from a run of its own (a
compile one builder makes under another's run, as the coverage gate runs the
control and store gates, holds only the one whose run it is), unless the run
leaves it out (Scope): it has none of what that builder needs (--without
verilator), or it judges only the builders that need it (--only verilator,
which leaves out the firmware builders, judged by the run that holds
them); each one left out is named on every run. The builders are found by
text as well, as a cross-check that cannot pass on its own: every Python
module and Makefile of the checkout, tracked or new and not ignored, that
names the firmware's tree (sw/firmware/ctrl, or its shared builder
ctrl_build), the gate's own modules excepted, must be one of BUILDERS, be
listed in PART_OF with the builder it runs under (and have compiled in the
capture, unless the run leaves that one out), or, when it is no program (a
Makefile, or a Python module with a __main__ block, is one), have compiled
in the capture; or it must be listed in OUTSIDE with the reason its compiles, if any, are
none of the firmware's, or be listed in SUITES with what it compiles only in
a suite, which a build-only run does not run (a planted-defect campaign
compiles planted copies, and the checkout's tests against them, and the
builds compile every source of the checkout it does). Any other refuses the
gate by name, and so does a compiler a builder runs by a path that is no
wrapper. So a builder dropped from BUILDERS refuses by name even where
another builder still runs it.
A run that judges only the builders that need Verilator leaves that
cross-check to the run that holds the firmware builders, whose capture holds
the builders found by text.

WHAT A CAPTURE MUST HOLD, each refused by name (held): a dependency list of
every source a recorded invocation compiles (ctrl_shim, THE DEPENDENCY PASS),
unless the compile itself failed and so compiled nothing (the RV32 self-test
compiles planted header defects that must fail; each such compile is named
on the run, failed), and the compiler's own expansion of every invocation
that names an input (ctrl_expand, THE EXPANSION), which is one
(ctrl_expand.refusal). A precompiled header an invocation reads first must
be one a compile the capture holds made.

THE FILES READ FIRST: every file the expansion read before its source
(-include, -imacros, in any spelling, and what those include), by kind: the
implementation's (a file the baseline reads, or one in a directory it
searches), an installed tool's (read_first), or the builders' own. A file of
the stack that is not one of its public headers refuses the gate by name, and
so does a file of the checkout outside the stack read first into a compile of
the stack's own sources. A file a builder writes outside the checkout (the
SRP builds' shape header, the two-interface builds' mailbox contract, both
force-included into every unit they compile) is the builder's: it is judged
by what it reads, as every file a compile reads is (ctrl_boundary).
"""

from __future__ import annotations

import os
import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from ctrl_build import HERE, ROOT, STACK, STACK_INCLUDE, Refusal
from ctrl_capture import Capture, Expansion, Invocation

#: The boundary gate's own modules: never a builder.
GATE = frozenset(HERE / name for name in ("ctrl_boundary.py", "ctrl_capture.py", "ctrl_configs.py", "ctrl_pin.py",
                                          "ctrl_pin_env.py", "ctrl_pin_store.py", "ctrl_pin_lifecycle.py",
                                          "ctrl_pin_bench.py", "ctrl_plants.py",
                                          "ctrl_shim.py", "ctrl_expand.py", "ctrl_runs.py"))
#: The shipped configs: each a shape the image builders take (ctrl_image.py --shape, ctrl_srp_image.py --config).
CONFIGS = ROOT / "configs"
#: What a builder of the firmware names: its tree, or the shared builder the arms, campaigns and fixtures
#: are written on.
BUILDER_NAMES = ("sw/firmware/ctrl", "ctrl_build")
#: What a file an expansion read first is (read_first).
IMPLEMENTATION, TOOL, OWN = "the compiler's own", "an installed tool's", "the builders'"
#: The languages a compiler compiles a source in, each of which the recorder lists the reads of.
COMPILED = ("c", "c++", "assembler")


@dataclass(frozen=True)
class Builder:
    """One builder of the firmware that compiles: its file (a script, or a Makefile), from the checkout's root;
    the commands that make its compiles when the gate makes the capture itself, its builds and not its suites,
    from the root ({python} the interpreter, {work} a directory of the run's own, {verilator} the Verilator); and
    what it needs that a run may have none of ("verilator")."""

    path: str
    runs: tuple[tuple[str, ...], ...]
    needs: str = ""


#: The known set: every builder of the firmware that compiles. The hosted firmware-boundary job runs the first
#: six through the gate's own capture (--without verilator, rtl-fast.yml), the suite builders by their
#: --build-only: every arm's binaries and RV32 build, every shape's store binaries and RV32 build, and both
#: gates' coverage builds, none run and no defect planted (the RV32 self-test compiles its planted header,
#: ABI and runtime cases and runs no binary); the gate runs the stack's gate and the image builders itself on
#: every run (ctrl_runs.owned); the last three need Verilator, and the hosted firmware-verilator job runs them
#: through the gate's own capture (--only verilator). Each runs every configuration its own list holds: the
#: bench's default target, the differential with its self-test, the wire comparison at every reference it pins
#: (--every); the differential and the comparison keep what they build in the run's directory, where a control
#: replays it.
BUILDERS = (
    Builder("sw/firmware/gtest/fw_rv32_selftest.py",
            (("{python}", "sw/firmware/gtest/fw_rv32_selftest.py", "--require-rv32"),)),
    Builder("sw/firmware/ctrl/test/test_ctrl_firmware.py",
            (("{python}", "sw/firmware/ctrl/test/test_ctrl_firmware.py", "--require-rv32", "--build-only", "--jobs",
              "4"),)),
    Builder("sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py",
            (("{python}", "sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py", "--require-rv32", "--build-only", "--jobs",
              "4"),)),
    Builder("sw/firmware/gtest/fw_coverage.py",
            (("{python}", "sw/firmware/gtest/fw_coverage.py", "--build-only", "--jobs", "4"),)),
    Builder("sw/litex/test_ctrl_memory.py", (("{python}", "sw/litex/test_ctrl_memory.py", "--build-only"),)),
    Builder("tb/verilator/milan_dp/stream_counter_f5.py",
            tuple(("{python}", "tb/verilator/milan_dp/stream_counter_f5.py", "--build-only", "--shape", shape,
                   "--work", "{work}/f5-" + shape) for shape in ("1", "8"))),
    Builder("third_party/tsn-c-stack/scripts/check_boundary.py", ()),
    Builder("sw/firmware/ctrl/test/ctrl_image.py", ()),
    Builder("sw/firmware/ctrl/test/ctrl_srp_image.py", ()),
    Builder("sw/firmware/ctrl/test/ctrl_plat_image.py", ()),
    Builder("sw/firmware/ctrl/test/ctrl_image_selftest.py", ()),
    Builder("tb/verilator/mbx/Makefile",
            (("make", "-C", "tb/verilator/mbx", "VERILATOR={verilator}", "VBUILD_JOBS=4"),), "verilator"),
    Builder("sw/firmware/ctrl/test/maap_differential.py",
            (("{python}", "sw/firmware/ctrl/test/maap_differential.py", "--self-test", "--keep",
              "{work}/maap-differential"),), "verilator"),
    Builder("sw/firmware/ctrl/test/aecp_wire.py",
            (("{python}", "sw/firmware/ctrl/test/aecp_wire.py", "--every", "--output", "{work}/aecp-wire",
              "--verilator", "{verilator}"),), "verilator"),
)
#: What a run may say it has none of: each builder that needs it is left out of the capture, and named.
NEEDS = {"verilator": "Verilator"}
#: The programs found by text that run, in the builds, only under another builder (as its module, or a program
#: it runs): left out where that one is, and otherwise held as any builder found by text is.
PART_OF = {
    "sw/litex/ctrl_memory_probe.py": "sw/litex/test_ctrl_memory.py",
    "tb/verilator/mbx/mutants.py": "tb/verilator/mbx/Makefile",
    # the AECP arms, which the control gate builds; its own command, a developer's, builds a selection of them
    "sw/firmware/ctrl/test/aecp_arms.py": "sw/firmware/ctrl/test/test_ctrl_firmware.py",
    # the split platform's arms (#665), which the control gate builds
    "sw/firmware/ctrl/test/plat_arms.py": "sw/firmware/ctrl/test/test_ctrl_firmware.py",
    # the shared builder: its program is the stack's pin check (--stack-pin), which the bench's Makefile runs and
    # which compiles nothing; it compiles as the module of every builder of the firmware
    "sw/firmware/ctrl/test/ctrl_build.py": "tb/verilator/mbx/Makefile",
}
#: The builders found by text whose compiles, if any, are none of the firmware's, each with the reason.
OUTSIDE = {
    "tb/verilator/milan_dp/Makefile": "delegates firmware builds to the separately captured F5 program; "
                                     "its own compiler recipes build RTL harnesses",
    "sw/litex/ctrl_memory.py": "reads linked ELF bytes and plans memory banks; it compiles nothing",
    "sw/litex/milan_soc.py": "loads a prelinked control image; its optional BIOS and milan_baremetal builds "
                            "compile no control-stack source",
    "docs/diagrams/submodule_boundaries.gen.py": "draws the submodule diagram; it compiles nothing",
    "scripts/ci_events.py": "models the CI workflows; it compiles nothing",
    "scripts/ci_scope.py": "selects the CI scope from the paths a change touches; it compiles nothing",
    "sw/firmware/ctrl/adp/adp_entity.py": "writes the ADP shape header; it compiles nothing",
    "sw/firmware/ctrl/test/ctrl_mutant.py": "the campaign tables' record of one defect; it compiles nothing",
    "sw/firmware/ctrl/test/plat_mutants.py": "the split platform's planted defects (#665 S3), which the control "
                                             "campaign plants; it compiles nothing",
    "sw/firmware/ctrl/plat/ctrl_plat_gen.py": "writes the split platform's policy and bus map headers (#665 S3); it "
                                              "compiles nothing",
    "tb/verilator/ctrl_split_boot/run.py": "the split boot simulation (#665 S3), which no hosted job can run (the "
                                           "CPU budget harness's prerequisites): it delegates every compile of the "
                                           "firmware to ctrl_plat_image.py, unchanged or given a planted copy of the "
                                           "firmware's tree outside the checkout, and the runtime to runtime_ssp.py; "
                                           "its own compiles build the boot SoC's Verilator model",
    "sw/firmware/ctrl_nvm/test/nvm_mutants.py": "the saved-state store campaign's planted defects, which "
                                                "test_ctrl_nvm.py compiles; it compiles nothing",
    "sw/firmware/ctrl/test/ctrl_reuse.py": "cuts the processor's sources into fragments the arms compile; it "
                                           "compiles nothing",
    "sw/firmware/ctrl/test/srp_reuse.py": "cuts the processor's SRP sources into fragments the SRP arms compile; it "
                                          "compiles nothing",
    "sw/firmware/ctrl/test/ctrl_image_runtime.py": "compiles the bare-metal runtime from picolibc's and "
                                                   "compiler-rt's sources outside the checkout, no firmware or stack "
                                                   "source",
    "sw/firmware/ctrl/test/test_ctrl_firmware_shards.py": "proves the control gate's four-job dispatch (#716) with "
                                                          "every arm and campaign a stand-in; it compiles nothing",
    "sw/mailbox/gen_mailbox.py": "writes the mailbox contract; it compiles nothing",
    "sw/mailbox/mailbox_emit.py": "writes the mailbox contract's text; it compiles nothing",
    "sw/mailbox/publication_census.py": "counts the datapath's reads of the mailbox's publication block in the "
                                        "netlists sv2v and Yosys elaborate (#665 F-INT); it compiles no C",
    "sw/mailbox/census_ports.py": "classifies every port of the processor wrapper in the census's netlists, naming "
                                  "the firmware that writes each face (#665 S1); it compiles nothing",
    # the CPU budget harness (#665): no hosted job can run its build, which needs picolibc's and compiler-rt's
    # packages, the patched LiteX tree and Verilator together, so none of it is a known builder
    "tb/verilator/ctrl_service_budget/build.py": "delegates every compile of the firmware: its image to "
                                                 "ctrl_srp_image.py, run unchanged at the shapes, interface counts and "
                                                 "AECP composition the gate runs it at (ctrl_runs.image_runs; the "
                                                 "split layout's reset entry is test_ctrl_memory.py's, and the runtime "
                                                 "archives change only the link), a control's planted copy of the "
                                                 "firmware's tree outside the checkout to the same builder, a variant "
                                                 "arm's image to fixture_variant.py and its runtime to runtime_ssp.py, "
                                                 "and the hybrid-XIP arm's relink of the image's objects to "
                                                 "ctrl_srp_image.link, which compiles the split layout's reset entry "
                                                 "from an unchanged copy and changes only the linker script; its own "
                                                 "compiles build the test SoC's Verilator model",
    "tb/verilator/ctrl_service_budget/runtime_ssp.py": "runs ctrl_image_runtime.py with -fno-stack-protector on its "
                                                       "compiles (#723): the bare-metal runtime from picolibc's and "
                                                       "compiler-rt's sources outside the checkout, no firmware or "
                                                       "stack source",
    "tb/verilator/ctrl_service_budget/scenario.py": "writes the harness's stimulus and reads AECP_REGISTRATIONS from "
                                                    "aecp.h; it compiles nothing",
    "tb/verilator/ctrl_service_budget/selftest.py": "the harness's grader self-test; it reads AECP_REGISTRATIONS from "
                                                    "aecp.h and compiles nothing",
    "tb/verilator/ctrl_service_budget/split_soc.py": "exports the test SoC with LiteX, its software and gateware "
                                                     "compiles off, and reads the image's placeholder addresses from "
                                                     "ctrl_build.RV32_FLAGS and the store's generated headers; it "
                                                     "compiles no firmware or stack source",
}
#: The builders found by text that compile only in a suite, which a suite builder's build-only run does not run,
#: each with what it compiles there. The builds compile every source of the checkout these compile, against the
#: checkout's own trees.
SUITES = {
    "sw/firmware/ctrl/test/ctrl_mutants.py": "the control campaign (test_ctrl_firmware.py --self-test): copies of "
                                             "the firmware's tree and the stack's src/ and include/ with a defect "
                                             "planted, and the checkout's tests and the stack's tests against them",
    "sw/firmware/ctrl/test/aecp_mutants.py": "the AECP campaign (test_ctrl_firmware.py --self-test): copies of the "
                                             "firmware's tree with a defect planted, and the checkout's tests "
                                             "against them",
    "sw/firmware/ctrl/test/srp_mutants.py": "the SRP campaign (test_ctrl_firmware.py --self-test): copies of the "
                                            "firmware's tree with a defect planted, and the checkout's tests "
                                            "against them",
    "sw/firmware/gtest/fw_coverage_selftest.py": "the coverage reader's planted cases (fw_coverage.py --selftest): "
                                                 "programs it writes outside the checkout",
    "sw/firmware/ctrl/test/plat_trace.py": "the split platform's CSR trace arm (#665 S3, test_ctrl_firmware.py's "
                                           "plattrace): ctrl_plat_csr.c, or a planted copy of it outside the "
                                           "checkout, and milan_baremetal.c as builder gate 35 compiles it, on the "
                                           "host",
    "tb/verilator/ctrl_service_budget/fixture_variant.py": "the CPU budget harness's labelled variant arms (#665, "
                                                           "run.py --variant): ctrl_srp_image.py's compiles, the size "
                                                           "fixture read from build.py's edited copy outside the "
                                                           "checkout",
}


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """One tool, its output captured, its messages in English."""
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False,
                          env={**os.environ, "LC_ALL": "C"})


def rel(path: Path) -> str:
    """A path of the checkout, named from its root."""
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


# ---- the builders ---------------------------------------------------------------------------


@lru_cache(maxsize=None)
def candidates() -> list[Path]:
    """Every Python module and Makefile of the checkout, tracked or new (and not ignored), listed once per run."""
    res = run(["git", "-C", str(ROOT), "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--",
               "*.py", "*Makefile", "*.mk"])
    if res.returncode:
        raise Refusal(f"cannot list the checkout's files: {res.stderr.strip()}")
    return sorted({ROOT / name for name in res.stdout.split("\0") if name and (ROOT / name).is_file()})


def builder(path: Path, text: str) -> bool:
    """Whether a file is one of the firmware's builders: it names the firmware's tree, and it is not one of the
    boundary gate's own modules (its controls' builders are not the checkout's)."""
    return path.resolve() not in GATE and any(n in text for n in BUILDER_NAMES)


@lru_cache(maxsize=None)
def checkout_builders() -> tuple[tuple[Path, str], ...]:
    """Every builder the checkout holds, with its text: read once per run, as the gate writes nothing there."""
    texts = ((path, path.read_text(encoding="utf-8", errors="replace")) for path in candidates())
    return tuple((path, text) for path, text in texts if builder(path, text))


def builder_texts(planted: dict[Path, str] | None = None) -> dict[Path, str]:
    """The text of every builder the checkout holds, with `planted` replacing a file's text, or adding a new
    file, for the self-test."""
    texts = dict(checkout_builders())
    for path, text in (planted or {}).items():
        texts.pop(path, None)
        if builder(path, text):
            texts[path] = text
    return dict(sorted(texts.items()))


def program(path: Path, text: str) -> bool:
    """Whether a builder found by text is a program: a Makefile, or a Python module with a __main__ block."""
    return path.suffix != ".py" or re.search(r"^if __name__ == ['\"]__main__['\"]:", text, re.M) is not None


def makefiles() -> list[Path]:
    """The Makefiles among the builders."""
    return [path for path in builder_texts() if path.suffix != ".py"]


@dataclass(frozen=True)
class Scope:
    """Which known builders a run judges: every one but those needing what it has none of (`without`), or, with
    `only`, those that need it alone (the gate's own runs beside them, which need nothing)."""

    without: frozenset[str] = frozenset()
    only: str = ""

    def left_out(self) -> list[Builder]:
        """The known builders the run leaves out."""
        return [b for b in BUILDERS if (b.needs and b.needs in self.without) or
                (self.only and b.runs and b.needs != self.only)]

    def judges(self, needs: str) -> bool:
        """Whether a control that needs this ("" for nothing) is the run's: its plant needs a builder the run
        holds."""
        return needs == self.only if self.only else needs not in self.without


def held(capture: Capture, scope: Scope, planted: dict[Path, str] | None = None,
         trees: tuple[Path, ...] = (ROOT,), own: Capture | None = None, known: tuple[Builder, ...] = BUILDERS) -> None:
    """Refuse, by name, a known builder (`known`: BUILDERS, but for a control) the capture holds no invocation of
    from a run of its own, a builder found by text that is a program and none of `known`, PART_OF, OUTSIDE or
    SUITES, one that is no program and compiled nothing in it and is none of those, a compiler a builder ran by a
    path that is no wrapper, a compiled source the recorder holds no dependency list of, and an invocation whose
    expansion is none or reads a file first that the stack's side does not admit (expanded; `trees` are the
    checkout roots judged, the checkout's and a control's copy of it, which only the control's `own` capture
    compiles)."""
    out = {b.path for b in scope.left_out()}
    names = {b.path for b in known}
    reasons = [f"the capture holds no invocation of {b.path} from a run of its own, a builder of the firmware that "
               "compiles (its compiles under another builder's run are that one's)"
               for b in known if b.path not in out and b.path not in capture.ran]
    for path, text in builder_texts(planted).items() if not scope.only else ():
        name = rel(path)
        if name in names or name in OUTSIDE or name in SUITES or PART_OF.get(name) in out:
            continue
        if program(path, text) and name not in PART_OF:
            reasons.append(f"{name} names the firmware's tree and is a program, and is neither a known builder "
                           "(ctrl_configs.BUILDERS) nor listed as one that runs under another (PART_OF), compiles "
                           "none of the firmware's (OUTSIDE) or compiles only in a suite (SUITES)")
        elif name not in capture.builders:
            reasons.append(f"{name} names the firmware's tree, compiled nothing in the capture, and is neither a known "
                           "builder (ctrl_configs.BUILDERS), one whose compiles are none of the firmware's (OUTSIDE), "
                           "nor one that compiles only in a suite (SUITES)")
    for bypass in capture.bypassed:
        reasons.append(f"{', '.join(bypass['from']) or 'a builder'} ran {bypass['bypass']}, a compiler the capture "
                       "does not wrap, so it records none of that compiler's invocations")
    reasons += [reason for leaf in capture.leaves for reason in once("unlisted", leaf, unlisted)]
    mine = [] if own is None else [id(leaf) for leaf in own.leaves]
    for leaf in capture.leaves:
        where = places(trees if id(leaf) in mine else (ROOT,))
        reasons += once(f"expanded {where}", leaf, lambda c, at=where: expanded(c, at))
    if reasons:
        raise Refusal("; ".join(dict.fromkeys(reasons)))


def unlisted(capture: Capture) -> list[str]:
    """Each source a compile that passed compiled whose dependency pass gave no list (ctrl_shim, THE DEPENDENCY
    PASS): it failed, was incomplete, or read standard input. A compile that failed compiled nothing (failed)."""
    reasons = []
    for inv in capture.invocations:
        for source in inv.sources:
            if source.lang in COMPILED and source.deps is None and inv.rc == 0:
                why = source.error or "the recorder holds no dependency list of it"
                reasons.append(f"{command(inv)}, whose dependency output for {source.path} is none: {why}")
    return reasons


def failed(capture: Capture) -> list[Invocation]:
    """Each compile that failed, a source of which its dependency pass gave no list either: it compiled nothing (the
    RV32 self-test's planted header defects), so nothing it read is in an object."""
    return [inv for inv in capture.invocations
            if inv.rc and any(s.lang in COMPILED and s.deps is None for s in inv.sources)]


#: What is read from each capture, once per capture: a control's capture is joined from the run's and its own.
READ: dict[tuple[str, int], tuple[Capture, object]] = {}


def once(kind: str, capture: Capture, read: Callable[[Capture], object]) -> object:
    """What `read` gives for a capture, read once (by kind and identity)."""
    known = READ.get((kind, id(capture)))
    if known is None or known[0] is not capture:
        READ[(kind, id(capture))] = known = (capture, read(capture))
    return known[1]


def command(inv: Invocation) -> str:
    """An invocation, named: who ran it and how (its arguments cut short)."""
    words = " ".join([inv.tool, *inv.args])
    return f"{', '.join(sorted(inv.builders)) or 'a builder'} ran {words[:200]}{' ...' if len(words) > 200 else ''}"


def expansions(inv: Invocation) -> list[Expansion]:
    """An invocation's expansion, then those of the compiles that made each precompiled header it read first."""
    return [inv.expansion, *inv.first] if inv.expansion is not None else []


def read_first(inv: Invocation) -> list[tuple[str, str]]:
    """Every file an invocation read before its source, resolved, with what it is: the implementation's (its
    baseline read it, or it lies in a directory its baseline searches), an installed tool's (as the expansion
    judges one: outside the checkout, the temporary directory and the compile's, there before the capture began),
    or the builders' own. A precompiled header's header and what it read are read first by every compile that
    reads the precompiled header."""
    return once_read_first(tuple(expansions(inv)))


@lru_cache(maxsize=None)
def once_read_first(made: tuple[Expansion, ...]) -> list[tuple[str, str]]:
    """read_first of a tuple of expansions, made once."""
    own = frozenset().union(*(b.own for e in made for _, b in e.baseline))
    found: dict[str, str] = {}
    for exp in made:
        for _, where, _, tool in (*exp.entered, *(exp.mains if exp is not made[0] else ())):
            if where in own or any(where.startswith(d.rstrip("/") + "/") for d in own):
                found[where] = IMPLEMENTATION
            else:
                found[where] = TOOL if tool else OWN
    return list(found.items())


def places(trees: tuple[Path, ...]) -> tuple[tuple[Path, ...], tuple[Path, ...]]:
    """The checkout roots judged (the checkout's, and a control's copy of it), and the stack of each."""
    roots = tuple(dict.fromkeys(t.resolve() for t in trees))
    return roots, tuple(root / STACK.relative_to(ROOT) for root in roots)


def kind_of(where: str, places_of: tuple[tuple[Path, ...], tuple[Path, ...]]) -> str:
    """Where a file read first lies: "public" (a stack's public header), "stack" (another file of a stack),
    "checkout" (another file of a root judged: tracked in the checkout, or in a control's copy), or "outside" (a
    build's own)."""
    path, (roots, stacks) = Path(where), places_of
    for stack in stacks:
        if path.is_relative_to(stack):
            return "public" if path.is_relative_to(stack / STACK_INCLUDE) else "stack"
    return "checkout" if any(path.is_relative_to(root) for root in roots) and tracked(path) else "outside"


def expanded(capture: Capture, where_of: tuple[tuple[Path, ...], tuple[Path, ...]]) -> list[str]:
    """Each invocation the capture could not have expanded, whose expansion is none, or whose expansion read a file
    first that is a stack's but not one of its public headers, or a file of the checkout outside the stack read
    into a compile of the stack's own sources."""
    stacks = where_of[1]
    reasons = []
    for inv in capture.invocations:
        made = inv.expansion
        if inv.failed or made is not None and made.error:
            reasons.append(f"{command(inv)}, which the compiler could not expand: {inv.failed or made.error}")
            continue
        if made is None:
            continue
        # an installed tool's file is no file of a root judged: a copy's file is judged by where it lives
        ours = [(where, kind_of(where, where_of)) for where, what in read_first(inv) if what != IMPLEMENTATION]
        stack_own = any(Path(s.path).is_relative_to(stack) for s in inv.sources if s.path != "-" for stack in stacks)
        for where, kind in ours:
            if kind == "stack":
                reasons.append(f"{command(inv)}, which reads {where} first, a file of the stack that is not one of "
                               "its public headers")
            elif kind == "checkout" and stack_own:
                reasons.append(f"{command(inv)}, which reads {where} first into a compile of the stack's own "
                               "sources: a file of the checkout outside the stack")
    return reasons


def tracked(path: Path) -> bool:
    """Whether a file is one the checkout tracks, or one of a control's copy of the checkout (outside it): a
    build's own file under the checkout (a generated header in an object directory) is not."""
    if not path.is_relative_to(ROOT.resolve()):
        return path.is_file()
    return path.relative_to(ROOT.resolve()).as_posix() in tracked_files()


@lru_cache(maxsize=None)
def tracked_files() -> frozenset[str]:
    """Every file the checkout tracks, its submodules' included, listed once per run."""
    res = run(["git", "-C", str(ROOT), "ls-files", "-z", "--recurse-submodules"])
    if res.returncode:
        raise Refusal(f"cannot list the checkout's files: {res.stderr.strip()}")
    return frozenset(name for name in res.stdout.split("\0") if name)
