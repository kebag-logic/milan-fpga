#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
lint_rtl.py - the whole-of-`hdl/` RTL lint gate (Verilator --lint-only).

WHY THIS EXISTS.  `scripts/run-verilator-lint.sh` linted the nine AECP modules
and nothing else, ran nowhere in CI and was documented nowhere, so nothing ran
it and nothing told a contributor to.  This replaces it with a sweep over every
module in `hdl/`, wired into the `rtl` workflow next to the suites.

WHY VERILATOR AND NOT VERIBLE/svlint - measured, not asserted.  The `rtl`
workflow already builds and caches a pinned Verilator 5.050 at /opt/verilator
for the suite sweep, so `--lint-only` costs one cache restore and ~10 s of
runner time: nothing extra to install, nothing extra to cache, and exactly the
version the harnesses are gated against, so a lint verdict and a suite verdict
can never disagree about what the source means.

Verible v0.0-4084 was then actually run over the same 89 files (2026-07-27):

    Verilator --lint-only     188 findings, 155 of them width (WIDTHTRUNC 74 +
                              WIDTHEXPAND 81) - the correctness meat
    Verible default rules    1004 findings, ZERO width. It has no elaborator,
                              so every one of those 155 is invisible to it

and of Verible's 1004, 916 are pure style - the largest single rule being 356
`parameter-name-style`, whose default pattern
`(([A-Z0-9]+[a-z0-9]*)+(_[0-9]+)?)` rejects essentially every parameter in the
tree because CONTRIBUTING.md §1 mandates the `_C`/`_P` suffix convention.
Adopting Verible's defaults would mean mass-renaming to its taste or waiving
its biggest rule on day one.  Turning off everything that fights the house
style leaves exactly THREE useful rules and FIFTEEN findings:
undersized-binary-literal 9, posix-eof 4, case-missing-default 2 (Verilator's
CASEINCOMPLETE already reports 1 of those 2).  Fifteen findings do not buy a
16.4 MB second toolchain, a second cache entry and a second version pin that
has to be kept in step with the suites.  Revisit if the tree adopts Verible's
naming conventions, or if a formatter (verible-verilog-format) is wanted -
that is a different job from this gate.

THE RULE THAT SHAPES THIS FILE.  A gate that only warns is worse than no gate:
`check_tied_inputs.sh` printed four warnings for months, three of them
expected, and the fourth - a tied-off `i_mac_events` that silently zeroed all
of RMON - survived precisely because a report whose warnings are mostly
expected is a report nobody reads.  So nothing here is advisory:

  * a malformed / unbalanced / unjustified `lint_off`, and a module that will
    not ELABORATE, are HARD failures, never ratcheted - see ELAB_BLOCKERS;
  * a violation COUNT above the committed per-directory ratchet
    (`scripts/lint.budget`) is a failure, and the offending violations are
    printed in full;
  * a waiver is a table entry naming the reason AND where the reason is
    recorded - the `check_tied_inputs.sh` shape - never a blanket `-Wno-`.

THE RATCHET.  Today's tree is not lint-clean and this round does not try to
make it so: rewriting RTL to please a linter is how deliberate truncations
become bugs.  `scripts/lint.budget` records the per-directory violation count
this tree is allowed to carry.  `--check` FAILS when a directory exceeds its
entry, so a NEW violation breaks the build from day one; a normal run only ever
LOWERS an entry, so paying the debt down is one commit with no argument.  The
outstanding count and its per-directory / per-code breakdown are printed on
every run: the size of the debt is never something you have to go and measure.

METHOD.  Every module declared under `hdl/` (excluding `**/doc/**`) is linted
as its own top, with the WHOLE source list on the command line each time.  The
obvious cheaper spelling - `-y hdl/...` library search - is wrong here and was
measured to be wrong: Verilator does not honour a compilation-unit-scope
`import <pkg>::*;` in a file it found through `-y`, so linting milan_datapath
that way produced 60+ bogus "Can't find definition of variable" errors out of
the then-current SRP registrar and friends, which put their import above the
module (house style; those files are deleted, the failure mode is not).
Passing the sources explicitly costs ~2 s per top and is correct.
Consequences worth knowing:

  * a module is elaborated at its DEFAULT parameters, which is why ALL 20
    SELRANGE used to be one bug: a 64-bit `s_axis.tdata` select against
    axi_stream_if's own `TDATA_WIDTH_P = 32` default (the then-current ADP
    parser 14, ptp_ts_core 5, KL_avtp_common_parser 1).  CLOSED 2026-07-27 by
    defaulting the interface to 64 - the width every one of its 53
    instantiations already passes explicitly, so no elaboration moved - which
    took the sweep from 188 to 150: SELRANGE 20 -> 0 plus 18 width findings
    that were themselves artifacts of the narrow elaboration.  It also retired
    two `lint_off SELRANGE` pragmas in the (since-deleted) AECP tree whose
    recorded justification ("the parameter default is 32") had been false since
    those modules moved to flat `input wire [63:0] s_axis_tdata` ports: they
    suppressed nothing, and removing them left the count at 150.  NOTE the hole
    that let a dead pragma sit there - this gate checks that a `lint_off` is
    well-formed, balanced and justified, but not that it still SUPPRESSES
    anything.
  * an %Error-rated code MASKS the findings behind it, so a count can go UP
    when a defect is fixed and that is not a regression.  Measured on the ADP
    parser of the day: with its uncast enum assignment in place Verilator stops
    after the ENUMVALUE error and reports 0 CASEINCOMPLETE for that file; with
    the cast it runs the later passes and reports 1 (`case (adp_state)`, no
    default).  The adp directory still fell 20 -> 6 because 15 findings went
    away, but a reviewer seeing a NEW code appear next to a fix should suspect
    unmasking before suspecting the fix.
  * a file that is `` `include ``-d by another (ethernet_packet_pkg.sv) is NOT
    also passed on the command line - that is a MODDUP, not a finding.
  * package/interface-only files declare no module, so they are linted as part
    of every run rather than as a top; `--check` FAILS if an interface file is
    instantiated by nothing (see `coverage_gaps`), so nothing escapes the sweep
    silently.
  * third_party/verilog-axis is on the `-y` path for RESOLUTION ONLY.  It is
    upstream code (alexforencich), we do not patch it, and diagnostics whose
    file lands under third_party/ are counted nowhere and waived nowhere - but
    they ARE printed, with their codes, so "excluded" never quietly becomes
    "unknown" (17 today: WIDTHTRUNC 10, WIDTHEXPAND 4, SELRANGE 3).

Run:
    scripts/lint_rtl.py                # sweep, print census, lower the ratchet
    scripts/lint_rtl.py --check        # CI gate: fail on regression, write nothing
    scripts/lint_rtl.py --pragmas      # just the `lint_off` well-formedness gate
    scripts/lint_rtl.py --self-test    # + prove a malformed pragma is rejected
    scripts/lint_rtl.py --verbose      # list every surviving violation

Exit 0 = at or under ratchet, 1 = regression / hard error, 2 = usage or setup.
"""

import argparse
import collections
import concurrent.futures
import dataclasses
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Callable, Iterable
from pathlib import Path

#: The waiver, exclusion and extra-warning TABLES - what this sweep asks
#: Verilator for, what it refuses to count, and the record behind every
#: entry - are `scripts/lint_rtl_policy.py`, which is pure policy with no
#: machinery in it. They are re-exported here because `from lint_rtl import
#: LINT_EXCLUDE` is how four other gates learn what this repository is
#: responsible for.
from lint_rtl_policy import (ELAB_BLOCKERS, EXTRA_WARNINGS, LINT_EXCLUDE,
                             PRAGMA_WAIVERS, RULE_WAIVERS)

#: TWO PATH TYPES, and which is which is a contract. An ANCHOR - this file, the
#: tree root, a walked directory - is a `Path`. Anything that NAMES A SOURCE is
#: a relative POSIX string: that is what Verilator is handed and prints back,
#: and what keys LINT_EXCLUDE, PRAGMA_WAIVERS and every line of lint.budget,
#: where a `Path` would compare unequal to the string the table holds.
#: `ROOT / rel` crosses one way, `_rel()` the other.
SELF = Path(__file__).resolve()
ROOT = SELF.parent.parent
HDL = ROOT / "hdl"
BUDGET = ROOT / "scripts" / "lint.budget"
THIRD_PARTY = "third_party/"


def _rel(path: Path, base: Path) -> str:
    """`path` as the tree names it: relative to `base`, or absolute when it is
    not under it (only the self-test, which roots a tree at a temp dir)."""
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def _read_text(path: Path) -> str:
    """The whole text of one file, the handle closed before it returns."""
    return path.read_text()


def _write_text(path: Path, text: str) -> None:
    """Write `text` to `path`, the handle closed before it returns."""
    path.write_text(text)


# ---- pragma well-formedness -------------------------------------------------
# The 2026 scar this gate must be able to catch: a trailing `//` comment after
# the waiver code
#
#     // verilator lint_off SELRANGE  // prose about why
#
# is TOLERATED by 5.050 and REJECTED by 5.020, and it made four suites
# unbuildable.  A lint gate that cannot catch a broken lint pragma has an
# obvious hole, so this is a HARD failure and never ratcheted: it breaks
# builds on other Verilator versions, which no violation count can express.
PRAGMA_RE = re.compile(r"verilator\s+lint_(off|on|save|restore)\b")
#: the ONLY accepted shapes.  Note `lint_on  UNUSED` (extra spaces) is fine;
#: anything after the code is not.
PRAGMA_OK_RE = re.compile(
    r"^\s*(?://|/\*)\s*verilator\s+lint_(?:off|on)\s+([A-Z][A-Z0-9_]*)\s*(?:\*/)?\s*$"
)
PRAGMA_BARE_RE = re.compile(r"^\s*(?://|/\*)\s*verilator\s+lint_(?:save|restore)\s*(?:\*/)?\s*$")


@dataclasses.dataclass(eq=False, repr=False)
class Violation:
    """One deduplicated Verilator diagnostic.

    A record, so the six fields ARE the constructor and the reader never has to
    check a hand-written positional order against the call site.  `pin` is not
    a field: it is read out of `msg` once, on construction, because the
    RULE_WAIVERS predicates ask for it by name and re-running the regex at
    every waiver test would be the same work in a worse place.  `eq=False`
    keeps identity comparison and hashability - the sweep dedupes on `key`,
    never on the object.
    """

    __slots__ = ("code", "path", "line", "col", "msg", "source", "pin")

    code: str
    path: str
    line: str
    col: str
    msg: str
    source: str

    def __post_init__(self):
        m = re.search(r"missing pin: '(\w+)'", self.msg)
        self.pin = m.group(1) if m else ""

    @property
    def key(self) -> tuple[str, str, str, str]:
        """Dedup identity: one finding arrives once per elaboration that saw it."""
        return (self.path, self.line, self.col, self.code)

    @property
    def bucket(self) -> str:
        """Ratchet bucket = the directory the offending file lives in - a
        STRING key of `scripts/lint.budget`, and "" (never `Path.parent`'s
        ".") at the root, or one directory would answer to two buckets."""
        parent = Path(self.path).parent
        return "" if parent == Path(".") else str(parent)

    def __str__(self):
        return "%s:%s:%s: %s  %s" % (self.path, self.line, self.col,
                                     self.code, self.msg)


def hdl_files(exts: tuple[str, ...] = (".sv",)) -> list[str]:
    """Every `hdl/` source of the given extensions, doc/ trees excluded."""
    out = []
    for base, dirs, files in os.walk(HDL):
        dirs[:] = [d for d in dirs if d != "doc"]
        for f in sorted(files):
            if f.endswith(exts):
                out.append(_rel(Path(base, f), ROOT))
    return sorted(out)


def submodule_sources() -> list[str]:
    """The RTL of the protocol-processor and gptp-processor submodules, as SOURCES only.

    `hdl/milan/KL_pp_shadow.sv` instantiates `protocol_processor_top` and
    `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv` instantiates
    `KL_gptp_engine`; both live in submodules and therefore are not in
    `hdl_files()`. Without them every sweep reported a hard MODMISSING for
    those tops - an %Error-rated code, so it also MASKED whatever findings
    sat behind it in those files.

    These are appended as sources and NEVER added to the lint task list: the
    submodule is linted by its own gate at its own ratchet, and re-linting it
    here would import another repository's debt into this one's budget.
    Packages first, for the same compilation-unit reason as above.
    """
    out = []
    for sub in ("protocol-processor", "gptp-processor"):
        root = ROOT / sub / "hdl"
        if not root.is_dir():
            continue                  # submodule not initialised: not our gate
        pkg, mod = [], []
        for base, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in ("doc", "rom", "ucode")]
            for f in sorted(files):
                if not f.endswith(".sv"):
                    continue
                rel = _rel(Path(base, f), ROOT)
                (pkg if f.endswith("_pkg.sv") else mod).append(rel)
        out += sorted(pkg) + sorted(mod)
    return out


def include_dirs() -> list[str]:
    """`-I` roots for `` `include ``: every hdl directory.

    The ENTITY SHAPE comes first. Lint elaborates every module at its DEFAULT
    parameters, and milan_datapath defaults to N_STREAMS = 1, so it must see
    the 1x1 entity definition - not whichever config was last written into
    hdl/common/gen/ by `endstation_builder.py --write-rtl`. Regenerating
    the tree for the 8x8 ship shape otherwise lints a 1-stream datapath
    against a 9-source entity, which milan_datapath's elaboration guard
    correctly rejects (and which, before that guard existed, showed up only
    as UNDRIVEN talker DMAC/VID bits). Same rule as the testbenches: name the
    shape you are elaborating, and put it ahead of hdl/common/csr.
    """
    dirs = ["configs/generated/endstation_arty_current"]
    for base, sub, _ in os.walk(HDL):
        sub[:] = [d for d in sub if d != "doc"]
        dirs.append(_rel(Path(base), ROOT))
    return dirs[:1] + sorted(dirs[1:])


def axis_lib() -> str | None:
    """verilog-axis `-y` root - RESOLUTION ONLY, never linted (see module doc)."""
    axis = ROOT / "third_party" / "verilog-axis" / "rtl"
    return _rel(axis, ROOT) if axis.is_dir() else None


#: The trees lint reads to RESOLVE the modules hdl/ instantiates, each with the
#: directory whose absence makes axis_lib()/submodule_sources() skip it. These
#: are exactly the paths those two functions test, kept in one place so the
#: refusal below cannot drift from what the sweep actually consumes.
REQUIRED_TREES = [
    ("third_party/verilog-axis", "third_party/verilog-axis/rtl",
     "the Forencich AXIS `-y` resolution root"),
    ("protocol-processor", "protocol-processor/hdl",
     "KL_pp_shadow's protocol_processor_top and its reset cone"),
    ("gptp-processor", "gptp-processor/hdl",
     "KL_gptp_shadow's KL_gptp_engine"),
]


def _tree_has_sources(rel):
    """True only if the tree exists AND holds source files lint would read.

    isdir alone is not enough: a submodule checked out to a pin with an empty
    `hdl/`, or a partial checkout, passes isdir yet contributes no sources, so
    the count still drops while the refusal below would not fire. So this walks
    for a `.sv`/`.v` under the tree (skipping the non-source `doc`/`rom`/`ucode`
    dirs, as submodule_sources does), and an empty tree is treated as absent
    ([R0] on PR #198).
    """
    root = ROOT / rel
    if not root.is_dir():
        return False
    for _base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ("doc", "rom", "ucode")]
        if any(f.endswith((".sv", ".v")) for f in files):
            return True
    return False


def missing_resolution_trees(present: Callable[[str], bool] | None = None) -> list[tuple[str, str]]:
    """(label, why) for every resolution tree lint needs that is absent or empty.

    The COUNT lint prints depends on every tree here: without its sources
    Verilator cannot bind the modules hdl/ instantiates, the reset/logic cone
    it needs to SEE a finding is incomplete, and the finding drops out of the
    count. Measured 2026-08-21: protocol-processor absent drops two hdl/milan
    SYNCASYNCNET findings, 99 -> 97. A fresh `git worktree add` has NO
    submodules, so a lane running the documented `scripts/lint_rtl.py` there
    reads a lower count AND is invited to tighten the ratchet to a number the
    real tree cannot meet (#186). Today an absent tree also raises a loud
    MODMISSING that the elaboration gate turns into an exit-1 (so no lowered
    budget is written), but that failure re-prints the misleading tighten hint
    and would not fire for a tree whose absence dropped findings WITHOUT a
    MODMISSING; refusing up front over an incomplete resolution set is the
    clean and future-proof answer, the pp_srcs.py shape.

    external/ is deliberately NOT here: it is an SSH-only submodule lint never
    reads. The full local-bar init set is in CONTRIBUTING 2.2. `present`
    overrides the presence test so the self-test drives every arm.
    """
    present = present or _tree_has_sources
    return [(label, why) for label, rel, why in REQUIRED_TREES
            if not present(rel)]


INCLUDE_RE = re.compile(r'^\s*`include\s+"([^"]+)"', re.M)


def included(files: Iterable[str]) -> set[str]:
    """Basenames pulled in by `` `include `` - passing them on the command line
    as well would define their modules twice (MODDUP)."""
    out = set()
    for rel in files:
        for inc in INCLUDE_RE.findall(_read_text(ROOT / rel)):
            out.add(Path(inc).name)
    return out


DECL_RE = re.compile(r"^\s*(module|package|interface)\s+([A-Za-z_]\w*)", re.M)


def declarations() -> dict[str, list[tuple[str, str]]]:
    """(file -> [(kind, name), ...]) for every linted `hdl/` source."""
    out = {}
    for rel in hdl_files((".sv",)):
        if rel in LINT_EXCLUDE:
            continue
        text = _read_text(ROOT / rel)
        # Strip comments before the declaration search.  A banner line that
        # happens to begin with the word "module" is prose, not a design unit,
        # and handing its next word to --top-module fails elaboration outright
        # ("module at all" in KL_chan_map_capture's queue banner did exactly
        # that).  docs/traceability/gen_module_matrix.py carries the same guard
        # for the same reason.
        scan = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        scan = re.sub(r"//.*", "", scan)
        out[rel] = DECL_RE.findall(scan)
    return out


def packages(decls: dict[str, list[tuple[str, str]]]) -> list[str]:
    """Package-only files.  Verilator's `-y` library search resolves MODULES
    and INTERFACES by filename but NOT `import <pkg>::*`, so every package is
    handed to every lint run explicitly - which also means the packages
    themselves are linted rather than merely parsed."""
    return sorted(rel for rel, ds in decls.items()
                  if ds and all(k == "package" for k, _ in ds))


def coverage_gaps(decls: dict[str, list[tuple[str, str]]]) -> list[tuple[str, str]]:
    """Files that no lint run would reach.  A module file is linted directly, a
    package file is preloaded into every run; an INTERFACE file is pulled in
    only by `-y` when something instantiates it, so prove something does.
    Without this, an unreferenced file could sit in the tree completely
    unlinted while the sweep still reported success - a silently capped scan."""
    bodies = {rel: _read_text(ROOT / rel) for rel in decls}
    pkgs = set(packages(decls))
    gaps = []
    for rel, ds in sorted(decls.items()):
        if any(k == "module" for k, _ in ds) or rel in pkgs:
            continue
        if not ds:
            gaps.append((rel, "declares no module, package or interface"))
            continue
        for kind, name in ds:
            users = [o for o, b in bodies.items()
                     if o != rel and re.search(r"\b%s\b" % re.escape(name), b)]
            if not users:
                gaps.append((rel, "%s %s is instantiated by nothing" % (kind, name)))
    return gaps


DIAG_RE = re.compile(r"^%(Warning|Error)-([A-Z][A-Z0-9_]*): (\S+?):(\d+):(\d+): (.*)$")
HARD_RE = re.compile(r"^%Error(?!: Exiting due to)")


def lint_one(mod: str, incdirs: list[str], sources: list[str],
             verilator: str) -> tuple[str, list[Violation], list[str]]:
    """Lint `mod` as a top; return (raw stdout, [Violation], [hard error])."""
    cmd = [verilator, "--lint-only", "--sv", "--top-module", mod]
    for w in EXTRA_WARNINGS:
        cmd.append("-Wwarn-" + w)
    for d in incdirs:
        cmd.append("-I" + d)
    axis = axis_lib()
    if axis:
        cmd += ["-y", axis]
    cmd += sources
    p = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, universal_newlines=True)
    lines = p.stdout.split("\n")
    vios, hard = [], []
    for i, ln in enumerate(lines):
        m = DIAG_RE.match(ln)
        if m:
            kind, code, path, line, col, msg = m.groups()
            # the offending SOURCE line, which Verilator echoes as `NNN | text`
            # a line or three below - MULTIDRIVEN and friends slip a
            # `... note: In instance` line in between. Waiver predicates read
            # this, so take the first real echo, not merely the next line.
            src = ""
            for ln2 in lines[i + 1:i + 5]:
                m2 = re.match(r"^\s*\d+\s*\|\s?(.*)$", ln2)
                if m2:
                    src = m2.group(1).strip()
                    break
            v = Violation(code, path, line, col, msg, src)
            # Findings inside a submodule are NOT this tree's debt: each is
            # linted by its own gate at its own ratchet, and counting it here
            # would move this budget every time that pin advances. Their
            # sources are on the command line only so our tops can find
            # `protocol_processor_top`/`KL_gptp_engine` (see
            # submodule_sources).
            if v.path.startswith(("protocol-processor/", "gptp-processor/")):
                continue
            if code in ELAB_BLOCKERS:
                hard.append("%s (linting %s)" % (v, mod))
            else:
                vios.append(v)
        elif HARD_RE.match(ln):
            hard.append("%s (linting %s)" % (ln.strip(), mod))
    return p.stdout, vios, hard


def sweep(verilator: str, jobs: int) -> tuple[
        dict[str, list[tuple[str, str]]], list[Violation], list[str], int]:
    """Lint every module as its own top, in parallel.

    Returns (declarations, deduped violations, hard errors, n_lints).  The
    dedup key is (file, line, col, code): a leaf module is elaborated both on
    its own and inside every parent, so the same finding arrives many times and
    must be counted once or the ratchet would move with the hierarchy."""
    decls = declarations()
    incdirs = include_dirs()
    inc = included(decls)
    pkgs = packages(decls)
    # packages first: a compilation-unit `import` must see them declared
    sources = ([p for p in pkgs if Path(p).name not in inc]
               + [r for r in sorted(decls)
                  if r not in pkgs and Path(r).name not in inc]
               + submodule_sources())
    tasks = [name for rel, ds in sorted(decls.items())
             for kind, name in ds if kind == "module"]
    vios, hard = {}, []
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = {ex.submit(lint_one, m, incdirs, sources, verilator): m
                for m in tasks}
        for f in concurrent.futures.as_completed(futs):
            _, vv, hh = f.result()
            hard += hh
            for v in vv:
                vios.setdefault(v.key, v)
    return decls, list(vios.values()), sorted(set(hard)), len(tasks)


def apply_waivers(vios: list[Violation]) -> tuple[list[Violation], list[Violation], list[Violation]]:
    """Split into (counted, waived, external) - external being third_party."""
    counted, waived, external = [], [], []
    for v in vios:
        if v.path.startswith(THIRD_PARTY) or "/third_party/" in v.path:
            external.append(v)            # upstream code, not ours to lint
            continue
        rule = RULE_WAIVERS.get(v.code)
        if rule is not None:
            pred = rule[0]
            if pred is None or pred(v):
                waived.append(v)
                continue
        counted.append(v)
    return counted, waived, external


# ---- pragma gate ------------------------------------------------------------

def known_codes(verilator: str, codes: Iterable[str]) -> list[str]:
    """Codes Verilator 5.050 actually knows (asked, never assumed)."""
    bad = []
    for c in sorted(codes):
        p = subprocess.run([verilator, "--lint-only", "-Wno-" + c, "--version"],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           universal_newlines=True)
        if "Unknown warning" in p.stdout:
            bad.append(c)
    return bad


def check_pragmas(verilator: str, files: list[str] | None = None,
                  root: Path | None = None) -> tuple[list[str], set[str]]:
    """Well-formedness + balance + justification of every in-tree lint pragma.

    `files` are relative POSIX strings under the `root` anchor, which is the
    tree root everywhere but the self-test.

    Returns (findings, seen) where `seen` is the set of `<path>|<CODE>` keys."""
    root = root or ROOT
    files = files if files is not None else hdl_files((".sv", ".svh", ".v"))
    findings, seen, codes = [], set(), set()
    for rel in files:
        depth = collections.Counter()
        with open(root / rel) as fh:
            lines = fh.readlines()
        for n, ln in enumerate(lines, 1):
            if not PRAGMA_RE.search(ln):
                continue
            if PRAGMA_BARE_RE.match(ln):
                continue
            m = PRAGMA_OK_RE.match(ln)
            if not m:
                findings.append(
                    "%s:%d: MALFORMED lint pragma - the waiver code must be the "
                    "LAST token on the line (5.050 tolerates trailing prose, "
                    "5.020 rejects it and the file stops building):\n"
                    "        %s" % (rel, n, ln.rstrip()))
                continue
            code = m.group(1)
            codes.add(code)
            if "lint_off" in ln:
                depth[code] += 1
                key = "%s|%s" % (rel, code)
                seen.add(key)
                if key not in PRAGMA_WAIVERS:
                    findings.append(
                        "%s:%d: UNJUSTIFIED `lint_off %s` - add a "
                        "PRAGMA_WAIVERS entry (why | where the reason is "
                        "recorded) in %s, or delete the pragma."
                        % (rel, n, code, _rel(SELF, root)))
            else:
                depth[code] -= 1
                if depth[code] < 0:
                    findings.append("%s:%d: `lint_on %s` with no open lint_off"
                                    % (rel, n, code))
        for code, d in sorted(depth.items()):
            if d > 0:
                findings.append(
                    "%s: `lint_off %s` never closed - it leaks to the end of "
                    "the file and silences code nobody looked at" % (rel, code))
    for key in sorted(PRAGMA_WAIVERS):
        if key not in seen:
            findings.append("STALE PRAGMA_WAIVERS entry '%s': that file no "
                            "longer carries that lint_off" % key)
    if codes:
        bad = known_codes(verilator, codes)
        for c in bad:
            findings.append("unknown warning code '%s' in a lint pragma - "
                            "Verilator does not know it, so the pragma "
                            "silences nothing" % c)
    return findings, seen


# ---- ratchet ----------------------------------------------------------------

BUDGET_HDR = [
    "# GENERATED by scripts/lint_rtl.py - the RTL lint ratchet: the largest",
    "# number of Verilator --lint-only violations each hdl/ directory may",
    "# carry. A normal run only ever LOWERS an entry; --check FAILS when a",
    "# directory exceeds it, so a NEW violation breaks the build even though",
    "# today's backlog is grandfathered. Lowering one is a normal commit:",
    "#     scripts/lint_rtl.py && git add scripts/lint.budget",
    "# Waived rules and the reasons are the tables in scripts/lint_rtl.py.",
]


def read_budget() -> dict[str, int] | None:
    """{directory: allowance}, or None when the file is missing."""
    if not BUDGET.exists():
        return None
    out = {}
    for line in _read_text(BUDGET).splitlines():
        s = line.split("#", 1)[0].strip()
        if not s:
            continue
        d, n = s.rsplit(None, 1)
        out[d] = int(n)
    return out


def write_budget(counts: dict[str, int], per_code: collections.Counter[str] | None = None) -> bool:
    """Rewrite scripts/lint.budget when its content moved, and say whether it did."""
    width = max([len(d) for d in counts] or [1])
    #: the debt is legible from the committed file alone - a reader should
    #: never have to run the sweep to find out how big the backlog is or what
    #: it is made of.
    tail = ["#", "# total %d across %d director(y/ies)"
            % (sum(counts.values()), len([1 for n in counts.values() if n]))]
    if per_code:
        tail.append("# by rule: " + ", ".join("%s %d" % (c, n)
                                              for c, n in ranked(per_code)))
    body = ["%-*s  %d" % (width, d, n) for d, n in sorted(counts.items())]
    content = "\n".join(BUDGET_HDR + tail + [""] + body) + "\n"
    cur = _read_text(BUDGET) if BUDGET.exists() else None
    if cur != content:
        _write_text(BUDGET, content)
    return cur != content


# ---- self-test --------------------------------------------------------------

SELF_TEST_CASES = [
    # (filename, body, must-be-rejected, what it proves)
    ("bad_trailing.sv",
     "// verilator lint_off SELRANGE  // prose Verilator 5.020 chokes on\n"
     "// verilator lint_on  SELRANGE\n",
     True, "the 5.020 trailing-prose scar"),
    ("bad_block.sv",
     "/* verilator lint_off UNUSED */ wire x;\n"
     "/* verilator lint_on  UNUSED */\n",
     True, "a block comment with code after the pragma"),
    ("bad_unclosed.sv",
     "// verilator lint_off WIDTHTRUNC\n",
     True, "a lint_off that leaks to end of file"),
    ("bad_unknown.sv",
     "// verilator lint_off NOTACODE\n"
     "// verilator lint_on  NOTACODE\n",
     True, "a waiver code Verilator does not know"),
    ("bad_orphan_on.sv",
     "// verilator lint_on  UNUSED\n",
     True, "a lint_on with no matching lint_off"),
    ("good.sv",
     "// verilator lint_off UNUSED\n"
     "wire unused = 1'b0;\n"
     "// verilator lint_on  UNUSED\n",
     False, "the well-formed shape the tree already uses"),
]


def self_test(verilator: str) -> int:
    """Mutation-prove the pragma gate: malformed pragmas MUST be rejected."""
    import tempfile
    rc = 0
    with tempfile.TemporaryDirectory() as td:
        tree = Path(td)
        for name, body, must_fail, what in SELF_TEST_CASES:
            _write_text(tree / name, body)
            saved = dict(PRAGMA_WAIVERS)
            # the good case needs its justification, exactly like the tree does
            PRAGMA_WAIVERS["good.sv|UNUSED"] = ("self-test fixture", "this file")
            try:
                found, _ = check_pragmas(verilator, files=[name], root=tree)
            finally:
                PRAGMA_WAIVERS.clear()
                PRAGMA_WAIVERS.update(saved)
            found = [f for f in found if not f.startswith("STALE")]
            ok = bool(found) == must_fail
            print("  [self-test] %-16s %-8s %s (%s)"
                  % (name, "REJECT" if must_fail else "ACCEPT",
                     "OK" if ok else "FAILED", what))
            if not ok:
                rc = 1
                for f in found:
                    print("        unexpected: %s" % f.replace("\n", " "))
    # #186: the resolution-tree refusal, proven on its pure predicate so it runs
    # on any box. End to end it is the negative control in the PR: remove a tree
    # and the gate exits 2, not the ratchet-tighten 1.
    all_absent = {label for label, _ in
                  missing_resolution_trees(present=lambda rel: False)}
    if all_absent != {label for label, _, _ in REQUIRED_TREES}:
        print("  [self-test] resolution-refusal REFUSE   FAILED "
              "(absent trees not all flagged: %s)" % sorted(all_absent))
        rc = 1
    elif missing_resolution_trees(present=lambda rel: True):
        print("  [self-test] resolution-refusal REFUSE   FAILED "
              "(a present tree was flagged absent)")
        rc = 1
    else:
        print("  [self-test] resolution-refusal REFUSE   OK (every absent "
              "resolution tree refuses; none flagged when present)")
    # A present-but-EMPTY tree must read as absent: isdir True is not enough,
    # or a submodule pinned to an empty hdl/ under-counts without refusing
    # ([R0] on PR #198). Proven on real temp dirs, no submodule needed.
    with tempfile.TemporaryDirectory() as td:
        tree = Path(td)
        (tree / "empty").mkdir()
        (tree / "sourced").mkdir()
        _write_text(tree / "sourced" / "m.sv", "module m; endmodule\n")
        saved = ROOT
        try:
            globals()["ROOT"] = tree
            bad = _tree_has_sources("empty") or not _tree_has_sources("sourced")
        finally:
            globals()["ROOT"] = saved
        if bad:
            print("  [self-test] empty-tree-is-absent      FAILED "
                  "(empty dir passed, or a sourced dir failed)")
            rc = 1
        else:
            print("  [self-test] empty-tree-is-absent      OK (a present but "
                  "source-empty tree reads as absent)")
    return rc


# ---- reporting --------------------------------------------------------------

def ranked(counter: collections.Counter[str]) -> list[tuple[str, int]]:
    """Counter -> [(key, n)] sorted by count then key.  `most_common()` keeps
    INSERTION order for ties, and the sweep is threaded, so using it would make
    the `by rule` line in the committed budget file reorder itself at random -
    a spurious diff on a generated artifact."""
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))


def census(vios: list[Violation]) -> tuple[collections.Counter[str], collections.Counter[str]]:
    """(per-directory, per-code) violation counts - the two views the ratchet uses."""
    per_dir = collections.Counter(v.bucket for v in vios)
    per_code = collections.Counter(v.code for v in vios)
    return per_dir, per_code


def print_census(counted: list[Violation], waived: list[Violation],
                 external: list[Violation], budget: dict[str, int],
                 n_lints: int) -> None:
    """The whole census: counted per directory against its ratchet, then the
    by-rule line, then what was waived and what was resolved but never ours."""
    per_dir, per_code = census(counted)
    print("== hdl/ Verilator lint census (%d module elaborations) ==" % n_lints)
    width = max([len(d) for d in per_dir] or [24])
    for d, n in sorted(per_dir.items()):
        b = budget.get(d) if budget else None
        tag = "" if b is None else ("  <= ratchet %d" % b if n <= b
                                    else "  > RATCHET %d" % b)
        print("  %-*s %4d%s" % (width, d, n, tag))
    clean = sorted(set(budget or {}) - set(per_dir))
    for d in clean:
        print("  %-*s %4d  (was %d)" % (width, d, 0, budget[d]))
    print("  %-*s %4d" % (width, "TOTAL", len(counted)))
    print("  by rule: " + ", ".join("%s %d" % (c, n)
                                    for c, n in ranked(per_code)))
    if waived:
        wd = collections.Counter(v.code for v in waived)
        print("  waived (RULE_WAIVERS, reasons in %s): %s"
              % (_rel(SELF, ROOT),
                 ", ".join("%s %d" % (c, n) for c, n in ranked(wd))))
    if external:
        ed = collections.Counter(v.code for v in external)
        print("  third_party (upstream verilog-axis - resolved, never linted, "
              "not ours to fix): %s"
              % ", ".join("%s %d" % (c, n) for c, n in ranked(ed)))


def _parse_args():
    """The command line: which of the four modes this run is."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="CI gate: fail on regression, never write the budget")
    ap.add_argument("--pragmas", action="store_true",
                    help="only the lint_off well-formedness / justification gate")
    ap.add_argument("--self-test", action="store_true",
                    help="prove the pragma gate rejects a malformed pragma")
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="list every surviving violation")
    ap.add_argument("--jobs", "-j", type=int, default=os.cpu_count() or 4)
    ap.add_argument("--verilator", default=os.environ.get("VERILATOR", "verilator"))
    return ap.parse_args()


def _pragma_gate(verilator):
    """Run and report the pragma gate; (rc, the `<path>|<CODE>` keys seen)."""
    print("== lint pragma gate (well-formed · balanced · justified) ==")
    findings, seen = check_pragmas(verilator)
    for f in findings:
        print("  [FAIL] " + f)
    if findings:
        print("PRAGMA GATE: FAIL - %d finding(s). Never ratcheted: a malformed "
              "pragma stops OTHER Verilator versions building the file (which "
              "no violation count can express), and an unexplained lint_off is "
              "the same defect class as an unexplained tied-off input."
              % len(findings))
        return 1, seen
    print("PRAGMA GATE: PASS (%d justified lint_off, %d excluded file(s))"
          % (len(seen), len(LINT_EXCLUDE)))
    return 0, seen


def _refuse_incomplete_resolution():
    """True (having said which tree and how to get it) if nothing may be
    measured: a source tree lint resolves hdl/ against is absent or empty.

    The sweep and the budget-lowering path would otherwise run over a tree
    missing the sources hdl/ instantiates and under-count, inviting a ratchet
    tighten (--check). Today an absent tree also raises a MODMISSING the
    elaboration gate turns into an exit-1 before any budget is written, so the
    danger is the misleading tighten hint rather than a silent lower-write -
    but that backstop does not cover a present-but-empty tree, nor a future
    resolution tree whose absence drops findings without a MODMISSING. A clean
    up-front refusal covers all of them (#186). This is exit 2, a setup
    refusal, deliberately NOT the exit-1 tighten path.
    """
    missing = missing_resolution_trees()
    if not missing:
        return False
    print("LINT SETUP: REFUSED - a source tree lint reads to resolve hdl/ "
          "is not checked out, so the violation count would be "
          "under-reported:")
    for label, why in missing:
        print("  missing: %-26s (%s)" % (label, why))
    print("  A fresh `git worktree add` inherits no submodules. Initialise "
          "them (no network needed for these three):")
    print("    git submodule update --init %s"
          % " ".join(label for label, _ in missing))
    print("  Refused rather than counted: a violation count over an "
          "incomplete resolution set proves nothing and must not read as a "
          "pass, nor invite a ratchet tighten - the pp_srcs.py rule.")
    return True


def _lower_ratchet(per_dir, per_code, budget, counted):
    """Write back a budget that only ever went DOWN; the exit status.

    A directory over its allowance is reported and left alone: raising the
    ratchet is not something a tool gets to do quietly, and --check will fail
    on it until someone deals with it.
    """
    new, tightened, over = dict(budget), [], []
    for d in sorted(set(budget) | set(per_dir)):
        n, cur = per_dir.get(d, 0), budget.get(d, 0)
        if n < cur:
            tightened.append("%s %d -> %d" % (d, cur, n))
        elif n > cur:
            over.append("%s %d > %d" % (d, n, cur))
        new[d] = min(n, cur) if d in budget else 0
    for o in over:
        print("WARNING: %s violation(s) exceeds the ratchet - --check will FAIL" % o)
    if over:
        return 1
    # always rewrite when the CONTENT moved: the by-rule line in the header is
    # part of what makes the debt readable from the committed file alone, so it
    # must not go stale just because no directory count happened to change.
    rewrote = write_budget(new, per_code)
    if tightened:
        print("lint ratchet tightened: " + "; ".join(tightened))
    elif rewrote:
        print("lint ratchet unchanged (%d violation(s) <= %d); budget header "
              "refreshed" % (len(counted), sum(budget.values())))
    else:
        print("lint ratchet unchanged (%d violation(s) <= %d)"
              % (len(counted), sum(budget.values())))
    return 0


def main() -> int:
    """The gate, in the order it refuses: pragmas, resolution trees, coverage,
    elaboration, then the per-directory ratchet."""
    a = _parse_args()

    verilator = shutil.which(a.verilator) or a.verilator
    if not shutil.which(a.verilator):
        print("lint_rtl: no verilator on PATH (VERILATOR=<path> overrides)",
              file=sys.stderr)
        return 2

    rc = 0
    if a.self_test:
        rc |= self_test(verilator)

    pragma_rc, seen = _pragma_gate(verilator)
    rc |= pragma_rc
    # --self-test composes with --check (that is how CI runs it); on its own it
    # is the fast pragma-only mode.
    if a.pragmas or (a.self_test and not a.check):
        return rc

    # REFUSE before measuring anything if a resolution tree is absent or empty.
    if _refuse_incomplete_resolution():
        return 2

    decls = declarations()
    gaps = coverage_gaps(decls)
    for rel, why in gaps:
        print("  [FAIL] %s: %s - it would be linted by nobody" % (rel, why))
    if gaps:
        print("LINT COVERAGE: FAIL - %d file(s) reachable by no lint run." % len(gaps))
        rc = 1

    decls, vios, hard, n_lints = sweep(verilator, a.jobs)
    counted, waived, external = apply_waivers(vios)
    for h in hard:
        print("  [ERROR] " + h)
    if hard:
        print("ELABORATION: FAIL - %d Verilator error(s). Never ratcheted: a "
              "module that will not elaborate is a broken build, not a lint "
              "finding." % len(hard))
        rc = 1

    budget = read_budget()
    print_census(counted, waived, external, budget or {}, n_lints)
    per_dir, _ = census(counted)

    # The backlog is printed IN FULL on every gated run. A ratchet that hides
    # what it is grandfathering is a silent cap, and a reader of this log must
    # be able to see the whole debt without going and running the sweep.
    if counted and (a.verbose or a.check):
        over = {d for d, n in per_dir.items() if n > (budget or {}).get(d, 0)}
        print("-- outstanding backlog: %d violation(s) --" % len(counted))
        for v in sorted(counted, key=lambda v: (v.path, int(v.line))):
            print("  %s%s" % ("NEW " if v.bucket in over else "", v))

    if a.check:
        if budget is None:
            print("LINT GATE: FAIL - %s is missing; run scripts/lint_rtl.py "
                  "once to record the baseline." % _rel(BUDGET, ROOT))
            return 1
        bad = sorted(d for d, n in per_dir.items() if n > budget.get(d, 0))
        if bad:
            for d in bad:
                print("LINT REGRESSION: %s has %d violation(s), ratchet allows %d"
                      % (d, per_dir[d], budget.get(d, 0)))
            print("  Fix it, or - if the finding is structurally impossible to")
            print("  be a defect - add a RULE_WAIVERS entry naming the reason")
            print("  AND where the reason is recorded. Raising the ratchet is")
            print("  not an option: it only ever goes down.")
            return 1
        low = sorted(d for d in budget if per_dir.get(d, 0) < budget[d])
        tot = sum(budget.values())
        print("LINT GATE: PASS (%d violation(s) <= ratchet %d; %d waived, "
              "%d justified lint_off)" % (len(counted), tot, len(waived), len(seen)))
        if low:
            print("  ratchet can be tightened in: %s  (run scripts/lint_rtl.py)"
                  % ", ".join(sorted(set(low))))
        return rc

    _, per_code = census(counted)
    if rc:
        return rc
    if budget is None:
        write_budget(per_dir, per_code)
        print("lint ratchet recorded: %d violation(s) across %d director(y/ies)"
              % (len(counted), len(per_dir)))
        return 0
    # A normal run only ever LOWERS an entry.
    return _lower_ratchet(per_dir, per_code, budget, counted)


if __name__ == "__main__":
    sys.exit(main())
