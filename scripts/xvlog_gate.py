#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Parse every hdl/ module with Vivado's xvlog, so a construct Vivado's
front-end REJECTS but Verilator/sv2v ACCEPT is caught by a cheap local check.

WHY THIS EXISTS (issue #132). The whole verification bar shares one front-end
family: the 52-suite Verilator sweep, `scripts/lint_rtl.py`, and the
`syn/yosys/run.sh` portability gate all lower SystemVerilog through
Verilator or sv2v. Any construct where Vivado's front-end is STRICTER than
that family is invisible to the entire bar. Use-before-declaration is the
first one found: `KL_gptp_shadow.sv` used a signal above its declaration,
Verilator accepted it, every local gate was green, and Vivado answered

    ERROR: [VRFC 10-3380] identifier 'full_w' is used before its declaration
    ERROR: [VRFC 10-8530] module 'KL_gptp_shadow' is ignored ...

`synth_design` only WARNS (Synth 8-6901) and still builds, so even a bitstream
run would not have failed; and the file becomes ineligible for the xsim benches
under tb/utests and tb/itests. There will be other such constructs. This gate
is a second front-end opinion, run before Vivado's, on a bench box.

WHAT IT DOES. `xvlog -sv` ANALYSES (it does not elaborate or synthesise), so it
needs no project, no submodule instances, and a few seconds per file. Packages
are compiled first into one work library - detected by reading each file for a
`package` declaration, the same way scripts/pp_srcs.py does, never by filename -
then every other module is compiled INDEPENDENTLY against that library. Compiling
independently is load-bearing: xvlog stops analysing a compilation unit at the
first module error, so a single bad file in a shared compile masks every file
after it. One module per invocation enumerates them all, which a ratchet needs.

WHAT IT ANALYSES, exactly (widened by #224 and #236 - read the next paragraph
before narrowing it again): every TRACKED `.sv` AND `.v` under hdl/, and every
tracked design source under protocol-processor/hdl and gptp-processor/hdl. Those
two are not third-party leaf IP - they are the control plane milan_datapath
elaborates on every build, and the same sources scripts/pp_srcs.py hands the
Verilator sweep, the Yosys portability gate and both Vivado OOC flows, so #132's
argument applies to them exactly as it applies to hdl/. third_party/ and
external/ are NOT analysed: leaf IP this repository neither owns nor edits, which
scripts/lint_rtl.py already treats as resolution-only, never linted. The census
prints that scope in full every run, because the defect both issues reported was
a census claiming more than the measurement covered - "every hdl/ module" over a
set that excluded one tracked `.v` and every processor source.

THE #186 INVARIANT IS KEPT BY REFUSING, NOT BY NARROWING. This banner used to say
the gate reads only hdl/, so that an uninitialised submodule cannot make the tree
look cleaner than it is. That reason stands and is not weakened here; the
conclusion drawn from it does not, because its price was that the very class this
gate exists to catch had live occurrences in the pinned processors with no gate
at all (#236 measured 37 at the pin on dev, 51 at the pin PR #227 proposes). So
the scope widens and the invariant is enforced directly instead: with a processor
tree absent, empty, or not a checked-out submodule, the gate REFUSES - exit 2,
naming the tree and the init command - rather than reporting a smaller clean set.
That is scripts/lint_rtl.py's shape, which #186 forced on the lint ratchet for
this same reason.

ONE FINDING PER MODULE, NOT ONE PER OCCURRENCE. xvlog stops at the first error in
a compilation unit and prints only the 10-8530 cascade after it, so a module with
many use-before-declaration occurrences yields ONE finding, naming the first
identifier. Measured 2026-08-24 on the processor top that `synth_design` reports
with 35 `Synth 8-6901` warnings: xvlog prints exactly one 10-3380 plus the
cascade, and `xvlog --help` in 2026.1 offers no continue-on-error switch. Fixing
that first occurrence banks one key and raises the next, so --check fails in both
directions at once and the new front is re-banked deliberately. That is the
ratchet working, not churn: the finding set changed, and it said so.

WHAT IT STILL CANNOT SEE: elaboration. Splitting a declaration-with-initialiser
(`reg [7:0] r = 8'd0;`) into a declaration plus a continuous `assign` is NOT
equivalent - an initialiser runs once at time zero, a continuous assign drives
forever - and xvlog, Verilator 5.050 under -Wall, sv2v and Yosys all accept the
broken form silently (#224). Only `xelab` rejects it, with VRFC 10-9171, and
`xelab` appears nowhere in this repository: the required `elaborate` context is
the LiteX/Verilator elaboration in sw/builder/test_builder.py. #224 leaves that
arm deliberately open; a lane doing declaration-order work has no gate for it.

TOOL ABSENCE IS A SKIP, NEVER A FALSE GREEN. With no xvlog on the box (CI has
none) the gate prints a visible SKIP marker and exits 0, the tsn-gen precedent.
The skip is decided BEFORE the missing-tree refusal, on purpose: with no tool
nothing can be measured at all, so refusing there would turn a gate CONTRIBUTING
section 3 calls inert in CI into a red one, and a skip already reads as not a
pass.

THE RATCHET keys on the finding IDENTITY `path|CODE|identifier`, not on a count.
A count ratchet cannot see a compensating swap - one finding fixed while another
appears in the same commit nets to zero (the lesson of #150). An identity set
fails on any NEW finding AND on any grandfathered finding that has silently
vanished (bank the improvement deliberately), so neither direction is silent.
Today's backlog is grandfathered in scripts/xvlog.budget and printed in full;
the underlying defects are their own ticket, not this gate's to fix.

THE BUDGET HAS TWO SECTIONS, hdl/ and the pinned processors, and a key cannot
move between them: a finding's section is DERIVED from its own path and a budget
filing a key under the other section is rejected as malformed. Donor debt can
therefore never be traded against hdl/ debt, and the empty hdl/ section #193
reached stays visibly empty instead of being absorbed into a joint total.

A PROCESSOR KEY IS SPELLED `<submodule>:<path>`, never `<submodule>/<path>`.
scripts/pp_srcs.py --check - a required `rtl-fast` context - fails any tracked
file outside its PROSE_OK table that names a submodule source literally, and this
ratchet is a tracked file whose whole job is to name them. Measured 2026-08-24
against pp_srcs.check(): the `/` spelling fails it, the `:` spelling does not.
Widening PROSE_OK instead would put a hand-maintained list of submodule sources
back in the tree, which is the defect pp_srcs.py exists to prevent. The colon
also carries the population inside the key, which is what the two sections above
are checked against.

    scripts/xvlog_gate.py            # analyse, print the census, LOWER the ratchet
    scripts/xvlog_gate.py --check    # gate: fail on a NEW or a vanished finding
    scripts/xvlog_gate.py --selftest # prove the gate reddens on a planted fault

Exit 0 = at the ratchet (or skipped), 1 = regression / vanished finding / a
package that will not analyse, 2 = usage or setup error, including a processor
tree that is not checked out and a malformed budget.
"""

import argparse
import hashlib
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

#: Repository root, from this file's location.
ROOT = pathlib.Path(__file__).resolve().parent.parent
HDL = ROOT / "hdl"
BUDGET = ROOT / "scripts" / "xvlog.budget"

#: Include search path and defines, the same set syn/yosys/run.sh hands the
#: portability sweep, so the two front-ends see the same preprocessor world.
INCLUDE_DIRS = [
    "hdl/common",
    "hdl/common/csr",
    "hdl/ieee8021q/ts",
    "hdl/common/eth_event_counter",
    "hdl/ieee17221/adp",
    "hdl/ieee8021as/ptp_timestamp",
]
DEFINES = ["SYNTHESIS"]

#: The pinned processor trees analysed alongside hdl/, each with the reason its
#: sources belong in a gate about THIS repository's front-end risk, printed by
#: the refusal when it is not checked out. Nothing here is resolved or
#: elaborated - xvlog analyses one file at a time - so unlike lint_rtl.py's
#: REQUIRED_TREES this list deliberately omits third_party/verilog-axis (leaf IP,
#: resolution only) and external/ (SSH-only; CONTRIBUTING 2.2 keeps it out of the
#: documented local-bar init, so requiring it would refuse on every lane).
SUBMODULE_TREES = [
    ("protocol-processor", "protocol-processor/hdl",
     "the ATDECC/SRP control plane milan_datapath elaborates via KL_pp_shadow"),
    ("gptp-processor", "gptp-processor/hdl",
     "the 802.1AS engine milan_datapath elaborates via KL_gptp_shadow"),
]

#: Budget/census sections, in print order, with the words the census uses for
#: each. A finding belongs to exactly one, derived from its path.
SECTIONS = ["hdl", "submodules"]
SECTION_LABEL = {"hdl": "hdl/", "submodules": "pinned processors"}

#: Where a bench install puts Vivado (docs/reference: 2026.1). $XVLOG wins, then
#: these, then PATH. Read, not restated in three places.
XVLOG_CANDIDATES = [
    "/home/alex/Xilinx/2026.1/Vivado/bin/xvlog",
    "/home/alex/Xilinx2/2026.1/Vivado/bin/xvlog",
]

#: The cascade line xvlog prints AFTER a real error ("module X is ignored due to
#: previous errors"). It is a consequence, not a finding, and naming it as one
#: would double-count every defect.
_CASCADE = "VRFC 10-8530"

_PACKAGE_RE = re.compile(r"^\s*package\s+\w+\s*;", re.M)
_CODE_RE = re.compile(r"\[(VRFC \d+-\d+)\]")
_IDENT_RE = re.compile(r"identifier '([^']+)'")
_LOC_RE = re.compile(r"\[([^\]\s]+):(\d+)\]\s*$")


def display_path(rel):
    """The path a finding is KEYED on: `<submodule>:<path>` inside a processor.

    A processor source is spelled with a colon rather than a slash because
    scripts/pp_srcs.py --check fails any tracked file outside its PROSE_OK table
    that names a submodule source literally, and scripts/xvlog.budget is a
    tracked file that must name exactly those sources (see the module docstring
    for the measurement). Everything else is unchanged, so an hdl/ key reads
    today as it read before, and an absolute path - the self-test's planted
    temp file - passes straight through.
    """
    for label, _tree, _why in SUBMODULE_TREES:
        if rel.startswith(label + "/"):
            return label + ":" + rel[len(label) + 1:]
    return rel


def section_of(key_or_path):
    """Which budget section a finding key (or its path) belongs to.

    Derived from the path, never stored alongside it: a section a writer could
    choose independently of the finding is a section a hand edit can move a key
    into, which is exactly the trade between donor and hdl/ debt the two
    sections exist to prevent.
    """
    head = key_or_path.split("|", 1)[0]
    for label, _tree, _why in SUBMODULE_TREES:
        if head.startswith(label + ":"):
            return "submodules"
    return "hdl"


class Finding:
    """One xvlog defect, keyed on identity, carrying every line it occurs on.

    The key is path + code + identifier and deliberately omits the line: a
    line number drifts as the file is edited, and one identifier used before
    its declaration in several places is ONE defect (the fix, moving the
    declaration up, addresses them together). The lines are kept as detail.
    """

    def __init__(self, path, code, identifier, line, message):
        self.path = path            # hdl-relative path of the module compiled
        self.code = code            # e.g. "VRFC 10-3380", or "" if none parsed
        self.identifier = identifier or ""
        self.lines = [line] if line else []
        self.message = message

    def merge(self, other):
        for ln in other.lines:
            if ln not in self.lines:
                self.lines.append(ln)

    @property
    def key(self):
        # Most VRFC errors name an identifier, and that is the stable key. Some
        # (a syntax error, an unopenable include) carry none, and keying two
        # DISTINCT such defects in one file as `path|code|` would collapse them:
        # once one is grandfathered, a different one of the same code hides
        # behind the banked key. So an identifier-less finding is discriminated
        # by a short hash of its message - stable across line moves, unlike the
        # line number, and distinct per defect ([R1] on PR #194).
        # The discriminator is prefixed `~`, NOT `#`: the budget's trailing
        # `# line(s) N` comment is stripped at the first `#`, so a `#`-keyed
        # finding wrote one key and read back a different, truncated one --
        # it could never be banked, only re-reported forever ([R0] on
        # PR #222 proved it end to end). `~` cannot appear in a path, a
        # VRFC code or an identifier.
        # An ESCAPED SystemVerilog identifier is terminated by whitespace,
        # which is a delimiter and not part of the name. It must not reach
        # the key: the budget is line-based, so a trailing space would be
        # invisible, would make `git diff --check` refuse the generated
        # file, and would not survive the reader's strip.
        ident = (self.identifier or "").strip() or (
            "~" + hashlib.sha1(self.message.encode("utf-8",
                                                   "replace")).hexdigest()[:8])
        return f"{self.path}|{self.code}|{ident}"

    def detail(self):
        loc = f":{','.join(self.lines)}" if self.lines else ""
        ident = f" '{self.identifier}'" if self.identifier else ""
        return f"{self.path}{loc}  [{self.code}]{ident}  {self.message}"


def find_xvlog():
    """An xvlog executable, or None."""
    env = os.environ.get("XVLOG")
    if env and os.path.exists(env):
        return env
    for cand in XVLOG_CANDIDATES:
        if os.path.exists(cand):
            return cand
    return shutil.which("xvlog")


def _split_packages(files):
    """(packages, modules) - a package is a file that DECLARES one, read.

    Keying on a `_pkg.sv` suffix is a naming convention; a package in a file
    named otherwise would sort after its importers and fail to analyse. Same
    rule, same reason, as scripts/pp_srcs.py.
    """
    pkgs = [f for f in files if _PACKAGE_RE.search((ROOT / f).read_text())]
    rest = [f for f in files if f not in set(pkgs)]
    return pkgs, rest


def hdl_sources():
    """Tracked hdl/ design sources, packages first then the rest, both sorted.

    Tracked only (git ls-files): analysing an untracked stray source is a build
    no other checkout can reproduce - the same rule pp_srcs.py keeps.

    BOTH `.sv` AND `.v`. The glob was `*.sv` alone and silently excluded
    hdl/milan/milan_dma_wrapper.v, the one tracked Verilog-2001 module under
    hdl/, while the census claimed every hdl/ module (#224). It is a real
    module - bd/build.tcl ships it and scripts/lint_rtl.py carries a named
    LINT_EXCLUDE waiver for it - and being outside the fabric build is a reason
    not to LINT it, not a reason to leave it out of a parse census that says
    "every". `.svh` is not matched: an include header is analysed through the
    file that includes it, and compiling one alone is not a compilation unit.
    """
    out = subprocess.run(["git", "ls-files",
                          "hdl/**/*.sv", "hdl/*.sv", "hdl/**/*.v", "hdl/*.v"],
                         cwd=ROOT, capture_output=True, text=True)
    if out.returncode:
        raise SystemExit(f"git ls-files failed: {out.stderr.strip()}")
    files = sorted(set(out.stdout.split()))
    if not files:
        raise SystemExit("no tracked hdl/ .sv or .v files found")
    return _split_packages(files)


def submodule_sources(label, tree):
    """Tracked design sources under one processor tree, or None if unusable.

    None means REFUSE, and it covers three states that all look like a smaller
    clean finding set: the tree is missing, the tree is present but holds no
    tracked source, and the directory exists without being a checked-out
    submodule.

    The third is why this resolves the repository boundary before listing
    anything. `git -C <dir>` WALKS UP when <dir> is not a repository, so an
    empty submodule directory - what an aborted `submodule update` leaves
    behind - would answer with the SUPERPROJECT's file list, and the gate would
    happily analyse hdl/ twice and call the processors covered. Requiring the
    submodule's own top-level to BE the submodule directory rules that out.
    """
    root = ROOT / tree
    if not root.is_dir():
        return None
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         cwd=ROOT / label, capture_output=True, text=True)
    if top.returncode:
        return None
    if pathlib.Path(top.stdout.strip()).resolve() != (ROOT / label).resolve():
        return None
    out = subprocess.run(["git", "ls-files", "*.sv", "*.v"], cwd=root,
                         capture_output=True, text=True)
    if out.returncode:
        return None
    files = sorted(set(out.stdout.split()))
    if not files:
        return None
    return [f"{tree}/{f}" for f in files]


def missing_submodule_trees(sources=None):
    """(label, why) for every processor tree the gate cannot analyse.

    `sources` overrides the lookup so the self-test can drive both arms on any
    box, with no submodule present or absent - lint_rtl.py's shape.
    """
    sources = sources or submodule_sources
    return [(label, why) for label, tree, why in SUBMODULE_TREES
            if not sources(label, tree)]


def source_plan():
    """(packages, modules, {section: tracked file count}) for the whole scope.

    Every package in the scope is analysed into the one work library before any
    module, hdl/ first and then each processor tree in SUBMODULE_TREES order.
    Within a tree the order is the sorted one pp_srcs.py emits, which is what
    the Yosys and Verilator consumers already build with; a cross-package
    dependency the order got wrong would surface as a package error, and the
    gate refuses to grade any module when a package will not analyse.

    Callers must have cleared missing_submodule_trees() first: this function
    silently omits a tree it cannot read, which is precisely the under-report
    the refusal exists to prevent.
    """
    pkgs, mods = hdl_sources()
    counts = {"hdl": len(pkgs) + len(mods), "submodules": 0}
    for label, tree, _why in SUBMODULE_TREES:
        files = submodule_sources(label, tree)
        if not files:
            continue
        sub_pkgs, sub_mods = _split_packages(files)
        pkgs += sub_pkgs
        mods += sub_mods
        counts["submodules"] += len(sub_pkgs) + len(sub_mods)
    return pkgs, mods, counts


def _xvlog_cmd(xvlog, path):
    cmd = [xvlog, "-sv", "--work", "work"]
    for d in DEFINES:
        cmd += ["-d", d]
    for inc in INCLUDE_DIRS:
        cmd += ["-i", str(ROOT / inc)]
    cmd.append(str(ROOT / path))
    return cmd


def _parse(path, text):
    """Every real ERROR in one xvlog run, attributed to `path`."""
    findings = []
    for line in text.splitlines():
        if not line.startswith("ERROR"):
            continue
        if _CASCADE in line:
            continue
        code = _CODE_RE.search(line)
        ident = _IDENT_RE.search(line)
        loc = _LOC_RE.search(line)
        # The human message is the text after the [CODE] tag with the trailing
        # [file:line] bracket removed - that location is parsed out separately
        # and its absolute path has no place in a committed finding.
        msg = line.split("]", 1)[-1].strip() if "]" in line else line
        msg = _LOC_RE.sub("", msg).strip()
        findings.append(Finding(
            path=path,
            code=code.group(1) if code else "",
            identifier=ident.group(1) if ident else "",
            line=loc.group(2) if loc else "",
            message=msg,
        ))
    return findings


def _dedup(findings):
    """Collapse findings sharing a key, merging their line lists."""
    by_key = {}
    for f in findings:
        if f.key in by_key:
            by_key[f.key].merge(f)
        else:
            by_key[f.key] = f
    return sorted(by_key.values(), key=lambda x: x.key)


def analyse(xvlog, extra_modules=None, workdir=None):
    """Compile packages then every module; return (findings, package_errors).

    `extra_modules` replaces the module list (the self-test passes a planted
    file); `workdir` overrides the scratch dir. Packages always come from the
    tree, because a planted module may import one - including the processor
    packages, so a planted PROCESSOR file analyses in the same library the real
    ones do and the self-test cannot pass on a world the gate never builds.
    """
    pkgs, rest, _counts = source_plan()
    modules = rest if extra_modules is None else extra_modules
    findings, pkg_errors = [], []
    made = workdir is None
    workdir = workdir or tempfile.mkdtemp(prefix="xvlog-gate-")
    try:
        for p in pkgs:
            r = subprocess.run(_xvlog_cmd(xvlog, p), cwd=workdir,
                               capture_output=True, text=True)
            if r.returncode:
                pkg_errors += _parse(display_path(p), r.stdout + r.stderr)
        if pkg_errors:
            return findings, pkg_errors
        for m in modules:
            r = subprocess.run(_xvlog_cmd(xvlog, m), cwd=workdir,
                               capture_output=True, text=True)
            if r.returncode:
                findings += _parse(display_path(m), r.stdout + r.stderr)
    finally:
        if made:
            shutil.rmtree(workdir, ignore_errors=True)
    return _dedup(findings), pkg_errors


_BUDGET_HEADER = [
    "# GENERATED by scripts/xvlog_gate.py - the Vivado front-end ratchet: the",
    "# set of xvlog findings (path|CODE|identifier) this tree is grandfathered",
    "# to carry. A normal run REWRITES this to the current set; --check FAILS on",
    "# any finding not listed (a regression) and on any listed finding that no",
    "# longer occurs (bank the fix). Keyed on identity, not a count, so a",
    "# compensating swap cannot hide (issue #150's lesson).",
    "#",
    "# An entry is a construct Vivado's front-end REJECTS that the",
    "# Verilator/sv2v bar cannot see - use-before-declaration is the first",
    "# such class found (#132). Fixing one means changing the source, not",
    "# this file; banking the fix is a normal commit:",
    "#     scripts/xvlog_gate.py && git add scripts/xvlog.budget",
    "# An EMPTY list is the goal state, reached for the whole hdl/ tree by",
    "# #193: the gate then fails on the first NEW finding rather than on a",
    "# count, and no entry can be traded away against a fix.",
    "#",
    "# TWO SECTIONS, and a key cannot move between them (#236). The `hdl`",
    "# section is this repository's own RTL; `submodules` is the pinned",
    "# processor control plane, whose keys are spelled `<submodule>:<path>`",
    "# so that scripts/pp_srcs.py --check does not read this generated file",
    "# as a hand-written copy of the submodule source list. A section is",
    "# DERIVED from each key's path when this file is read, so grandfathering",
    "# donor debt cannot bank an hdl/ finding and vice versa, and the empty",
    "# hdl section #193 reached stays visible as its own zero.",
    "#",
    "# xvlog stops at the FIRST error in a module, so one entry can stand for",
    "# many occurrences of the same class in that file. Fixing the first one",
    "# raises the next: --check then reports one vanished and one new key, and",
    "# both are re-banked in the same deliberate commit.",
]


_LOC_COMMENT_RE = re.compile(r"\s+# line\(s\) [\d,]+\s*$")
_SECTION_RE = re.compile(r"^#\s*---\s*section (\w+):")


class BudgetError(Exception):
    """The budget file cannot be read as written - a setup error, not a finding."""


def read_budget(path=None):
    """{section: {key}} for the grandfathered findings, or None if absent.

    The trailing `  # line(s) N` note is stripped by its OWN shape, not by
    cutting at the first `#`: a key may legitimately contain that character
    (an escaped SystemVerilog identifier such as ``\\hash#in~side``), and a
    reader that cuts at it returns a key the writer never wrote, so the
    finding can be reported forever and never banked ([R0] on PR #222 found
    the `#`-prefixed discriminator case; this is the same defect's general
    form). A whole-line `#` comment is still a comment - except the section
    marker, which is a comment the reader parses.

    A key filed under a section its own path does not derive raises
    BudgetError rather than being silently re-filed. Silently re-filing is
    the trade the sections exist to stop, and accepting it would make the
    file's own section headers decorative.
    """
    path = path or BUDGET
    if not path.exists():
        return None
    sections = {name: set() for name in SECTIONS}
    # Keys before the first marker belong to `hdl`: that is the shape of every
    # budget written before #236 added sections, and those keys are hdl/ paths.
    current = SECTIONS[0]
    for line in path.read_text().splitlines():
        marker = _SECTION_RE.match(line)
        if marker:
            current = marker.group(1)
            if current not in sections:
                raise BudgetError(f"unknown section {current!r} in {path}")
            continue
        if line.lstrip().startswith("#"):
            continue
        line = _LOC_COMMENT_RE.sub("", line).strip()
        if not line:
            continue
        derived = section_of(line)
        if derived != current:
            raise BudgetError(
                f"{path}: key {line!r} is filed under section {current!r} but "
                f"its path derives {derived!r}. A key does not move between "
                "sections; fix the file rather than the finding.")
        sections[current].add(line)
    return sections


def write_budget(findings, path=None):
    """Rewrite the ratchet: one block per section, in SECTIONS order.

    No blank lines anywhere, deliberately. The previous format carried a blank
    separator that had to be suppressed for an empty list, because a trailing
    blank line at EOF is what `git diff --check` refuses and the merge bar runs
    that check; with a section per population the same conditional would have
    to be right in four combinations instead of two. A comment line before each
    block reads the same and cannot end the file wrong.
    """
    by_section = {name: [] for name in SECTIONS}
    for f in findings:
        by_section[section_of(f.key)].append(f)
    lines = list(_BUDGET_HEADER)
    for name in SECTIONS:
        entries = sorted(by_section[name], key=lambda x: x.key)
        lines.append("#")
        lines.append(f"# --- section {name}: {len(entries)} finding(s) "
                     f"({SECTION_LABEL[name]}) ---")
        for f in entries:
            loc = f"  # line(s) {','.join(f.lines)}" if f.lines else ""
            lines.append(f"{f.key}{loc}")
    (path or BUDGET).write_text("\n".join(lines) + "\n")


def _scope_lines(counts):
    """The census's coverage claim, printed EVERY run, findings or not.

    The claim and the measurement are the same sentence on purpose. Both #224
    and #236 are the same defect - a census line reading "every hdl/ module"
    over a set that excluded one tracked `.v` and every processor source - so
    the counts here are computed from the list actually analysed, and what is
    NOT analysed is named rather than left to be inferred from a green line.
    """
    trees = ", ".join(tree for _label, tree, _why in SUBMODULE_TREES)
    return [
        f"  analysed: {counts['hdl']} tracked .sv/.v file(s) under hdl/ and "
        f"{counts['submodules']} under the pinned processors ({trees})",
        "  NOT analysed: third_party/ and external/ (leaf IP this repo neither "
        "owns nor edits), and",
        "                any defect only ELABORATION rejects - xvlog analyses; "
        "the split-initialiser",
        "                class needs xelab, which nothing in this repo runs "
        "(#224)",
    ]


def _print_census(findings, counts):
    total = len(findings)
    print(f"xvlog gate: {total} finding(s) across "
          f"{len({f.path for f in findings})} module(s)")
    for line in _scope_lines(counts):
        print(line)
    for name in SECTIONS:
        here = sorted((f for f in findings if section_of(f.key) == name),
                      key=lambda x: x.key)
        print(f"  {SECTION_LABEL[name]}: {len(here)} finding(s)")
        for f in here:
            print(f"    {f.detail()}")


def cmd_selftest(xvlog):
    """Plant a use-before-declaration into a clean module; require it to show.

    Detection cannot be proved without the tool, so this SKIPS (not passes)
    when xvlog is absent - the same honesty the gate keeps everywhere else.
    """
    problems = _selftest_logic()
    if xvlog is None:
        for p in problems:
            print(f"  SELFTEST FAILED: {p}")
        if problems:
            return 1
        print("xvlog gate selftest: parser/dedup/ratchet arms PASS; live "
              "detection arm SKIPPED (no xvlog on this box)")
        return 0
    _pkgs, rest = hdl_sources()
    donor = "hdl/ieee8021q/ts/credit_based_shaper.sv"
    if donor not in rest:
        donor = rest[0]
    # Each analyse() call builds a FRESH work library holding only the packages
    # plus the one file passed, so the donor never clashes with the real module
    # of the same name and needs no rename.
    with tempfile.TemporaryDirectory(prefix="xvlog-selftest-") as tmp:
        src = (ROOT / donor).read_text().splitlines()
        # Reference a net one line above its declaration, just before endmodule.
        idx = max(i for i, l in enumerate(src) if "endmodule" in l)
        planted = src[:idx] + [
            "  logic kl_selftest_use_w;",
            "  assign kl_selftest_use_w = kl_selftest_late_w;  // planted fault",
            "  logic kl_selftest_late_w;",
        ] + src[idx:]
        clean = pathlib.Path(tmp) / "clean.sv"
        faulted = pathlib.Path(tmp) / "faulted.sv"
        clean.write_text("\n".join(src) + "\n")
        faulted.write_text("\n".join(planted) + "\n")

        clean_f, perr = analyse(xvlog, extra_modules=[str(clean)])
        if perr:
            return _fail_setup(perr)
        if clean_f:
            problems.append(f"the unplanted donor produced findings: "
                            f"{[f.detail() for f in clean_f]}")
        bad_f, perr = analyse(xvlog, extra_modules=[str(faulted)])
        if perr:
            return _fail_setup(perr)
        hit = [f for f in bad_f
               if f.code == "VRFC 10-3380"
               and f.identifier == "kl_selftest_late_w"]
        if not hit:
            problems.append("the planted use-before-declaration produced no "
                            f"matching finding; got {[f.detail() for f in bad_f]}")

    for p in problems:
        print(f"  SELFTEST FAILED: {p}")
    if problems:
        return 1
    print("xvlog gate selftest: PASS (a planted use-before-declaration reddens "
          "the gate and names the identifier; the clean donor does not)")
    return 0


def _diff(keys, budget):
    """(new findings, vanished grandfathered findings)."""
    return sorted(keys - budget), sorted(budget - keys)


def _refuse_missing(missing):
    """Print the missing-tree refusal and return its exit code.

    Exit 2, a setup refusal, deliberately NOT the exit-1 regression path: a
    finding set measured over an incomplete scope proves nothing, must not read
    as a pass, and must not invite anyone to bank a smaller ratchet from it.
    Same shape and same reasoning as scripts/lint_rtl.py's LINT SETUP refusal.
    """
    print("XVLOG SETUP: REFUSED - a source tree this gate analyses is not "
          "checked out, so the finding set would be under-reported:",
          file=sys.stderr)
    for label, why in missing:
        print(f"  missing: {label:<22} ({why})", file=sys.stderr)
    print("  A fresh clone or `git worktree add` inherits no submodules. "
          "Initialise them:", file=sys.stderr)
    print("    git submodule update --init "
          + " ".join(label for label, _ in missing), file=sys.stderr)
    print("  Refused rather than counted: with a processor tree absent the "
          "gate would print a SMALLER clean set than the tree really carries, "
          "which is the #186 trap the hdl/-only scope used to avoid by "
          "narrowing.", file=sys.stderr)
    return 2


def _selftest_logic():
    """Arms that need no xvlog: the parser, the dedup, the ratchet diff.

    These are the parts that rot silently when xvlog output or the budget
    format changes, so they run on every box, CI included, where the live
    detection arm can only skip.
    """
    problems = []
    real = ("INFO: [VRFC 10-311] analyzing module milan_csr\n"
            "ERROR: [VRFC 10-3380] identifier 'lctx_wr_p_r' is used before its "
            "declaration [/abs/hdl/common/csr/milan_csr.sv:900]\n"
            "ERROR: [VRFC 10-8530] module 'milan_csr' is ignored due to "
            "previous errors [/abs/hdl/common/csr/milan_csr.sv:85]")
    got = _parse("hdl/common/csr/milan_csr.sv", real)
    if len(got) != 1:
        problems.append(f"parse: expected 1 finding (the 10-8530 cascade "
                        f"dropped), got {len(got)}")
    else:
        f = got[0]
        if f.code != "VRFC 10-3380" or f.identifier != "lctx_wr_p_r" \
                or f.lines != ["900"]:
            problems.append(f"parse: wrong fields {f.detail()!r}")
        if "/abs/" in f.detail():
            problems.append(f"parse: absolute path leaked into the finding "
                            f"{f.detail()!r}")

    merged = _dedup([Finding("m.sv", "VRFC 10-3380", "x", "10", "m"),
                     Finding("m.sv", "VRFC 10-3380", "x", "20", "m")])
    if len(merged) != 1 or merged[0].lines != ["10", "20"]:
        problems.append(f"dedup: same key not merged with both lines: "
                        f"{[f.detail() for f in merged]}")

    new, gone = _diff({"a", "c"}, {"a", "b"})
    if new != ["c"] or gone != ["b"]:
        problems.append(f"diff: expected new=['c'] gone=['b'], "
                        f"got new={new} gone={gone}")

    # Identifier-less findings must not collapse: two DISTINCT ones in a file
    # get distinct keys (by message hash), two identical ones share a key.
    a = Finding("m.sv", "VRFC 10-2989", "", "1", "cannot resolve ALPHA")
    b = Finding("m.sv", "VRFC 10-2989", "", "2", "cannot resolve BETA")
    c = Finding("m.sv", "VRFC 10-2989", "", "9", "cannot resolve ALPHA")
    if a.key == b.key:
        problems.append("empty-identifier: distinct messages collapsed to one "
                        f"key {a.key}")
    if a.key != c.key:
        problems.append("empty-identifier: identical messages got different "
                        f"keys {a.key} vs {c.key}")
    if "#" in a.key:
        problems.append(f"empty-identifier: key {a.key} contains the budget's "
                        "comment character, so read_budget would truncate it")

    # ...and the budget must SERIALIZE and ROUND-TRIP in both its goal state
    # (empty) and populated states. A populated list has one blank separator
    # before its entries; an empty list ends at the total instead, because a
    # trailing blank line fails `git diff --check`. A key the writer emits and
    # the reader cannot parse makes the finding unbankable, which is the only
    # escape hatch --check offers once the ratchet is empty (#193).
    # The tracked ratchet is NEVER touched by this: the round-trip runs
    # against a scratch file. run_all_suites.sh runs --selftest at the start
    # of every sweep, so an arm that wrote scripts/xvlog.budget in place
    # would leave synthetic entries in a tracked file if the process were
    # killed mid-call, and SIGTERM/SIGKILL cannot be caught ([R0] on #222).
    sub_label = SUBMODULE_TREES[0][0]
    sub = Finding(f"{sub_label}:hdl/top/t.sv", "VRFC 10-3380", "late_w", "5", "m")
    scratch = pathlib.Path(tempfile.mkdtemp(prefix="xvlog-budget-")) / "b"
    try:
        for case in ([], [a], [a, b], [sub], [a, sub],
                     [a, Finding("m.sv", "VRFC 10-3380", "x", "3", "m"), sub]):
            write_budget(case, scratch)
            rendered = scratch.read_text()
            for name in SECTIONS:
                n = len([f for f in case if section_of(f.key) == name])
                if f"# --- section {name}: {n} finding(s)" not in rendered:
                    problems.append(f"budget serialization: no section header "
                                    f"for {name} with {n} finding(s)")
            if "\n\n" in rendered:
                problems.append("budget serialization: blank line in the file "
                                "- `git diff --check` refuses one at EOF and "
                                "the merge bar runs it")
            back = read_budget(scratch)
            want = {name: {f.key for f in case if section_of(f.key) == name}
                    for name in SECTIONS}
            if back != want:
                problems.append(f"budget round-trip: wrote {want}, read back "
                                f"{back}")
            for name in SECTIONS:
                new_k, gone_k = _diff(want[name], (back or {}).get(name, set()))
                if new_k or gone_k:
                    problems.append(f"budget round-trip [{name}]: --check would "
                                    f"report new={new_k} gone={gone_k} against "
                                    "its own freshly written budget")
        # a key carrying the comment character must survive too: the reader
        # strips the location note by shape, not by cutting at the first `#`
        esc = Finding("m.sv", "VRFC 10-3380", "\\hash#in~side ", "7", "m")
        if esc.key.endswith(" ") or "\n" in esc.key:
            problems.append(f"key {esc.key!r} carries trailing whitespace, "
                            "which the budget format cannot represent")
        write_budget([esc], scratch)
        if read_budget(scratch) != {"hdl": {esc.key}, "submodules": set()}:
            problems.append("budget round-trip: a key containing '#' (an "
                            "escaped identifier) did not survive the reader")
        # A key filed under the wrong section must be REFUSED, not re-filed:
        # silently re-filing it is the donor-against-hdl/ trade the sections
        # exist to stop, and would make the headers decorative.
        scratch.write_text("# --- section hdl: 1 finding(s) ---\n"
                           f"{sub.key}\n")
        try:
            read_budget(scratch)
            problems.append("budget sections: a submodule key filed under "
                            "`hdl` was accepted; a hand edit can then trade "
                            "donor debt against hdl/ debt")
        except BudgetError:
            pass
    finally:
        shutil.rmtree(scratch.parent, ignore_errors=True)

    # ---- scope arms (#224, #236) -------------------------------------------
    # These need no xvlog, so they run in CI too, where the live detection arm
    # can only skip. They are what re-narrowing the scope would break.
    if display_path(f"{sub_label}/hdl/top/t.sv") != f"{sub_label}:hdl/top/t.sv":
        problems.append("display_path: a processor source is not keyed with "
                        "its `<submodule>:` prefix, so scripts/pp_srcs.py "
                        "--check would read the budget as a hand-written copy "
                        "of the submodule source list")
    if display_path("hdl/common/x.sv") != "hdl/common/x.sv":
        problems.append("display_path: an hdl/ key changed spelling, which "
                        "would orphan every banked hdl/ entry")
    if (section_of(f"{sub_label}:hdl/top/t.sv|C|i") != "submodules"
            or section_of("hdl/common/x.sv|C|i") != "hdl"):
        problems.append("section_of: a finding lands in the wrong budget "
                        "section")

    absent = {label for label, _why in
              missing_submodule_trees(sources=lambda label, tree: None)}
    if absent != {label for label, _tree, _why in SUBMODULE_TREES}:
        problems.append(f"tree refusal: not every absent processor tree is "
                        f"flagged, got {sorted(absent)}")
    if missing_submodule_trees(sources=lambda label, tree: ["x.sv"]):
        problems.append("tree refusal: a present processor tree was flagged "
                        "absent, so the gate would refuse on every lane")

    # #224: the one tracked `.v` under hdl/ is in the analysed set. Asserted
    # against git, not against a hardcoded name, so the arm still bites when
    # another `.v` is added.
    out = subprocess.run(["git", "ls-files", "hdl/**/*.v", "hdl/*.v"],
                         cwd=ROOT, capture_output=True, text=True)
    tracked_v = set(out.stdout.split()) if out.returncode == 0 else set()
    pkgs, mods = hdl_sources()
    analysed = set(pkgs) | set(mods)
    if tracked_v - analysed:
        problems.append(f"hdl scope: tracked Verilog file(s) "
                        f"{sorted(tracked_v - analysed)} are not analysed, so "
                        "the census claims more modules than it measures")
    if any(f.endswith(".svh") for f in analysed):
        problems.append("hdl scope: an include header reached the module list; "
                        "it is analysed through its includer, not alone")

    # #236: a checked-out processor tree really does contribute sources. When
    # it is absent the gate refuses, so there is nothing to assert.
    _p, plan_mods, counts = source_plan()
    for label, tree, _why in SUBMODULE_TREES:
        if submodule_sources(label, tree) is None:
            continue
        if not any(m.startswith(tree + "/") for m in _p + plan_mods):
            problems.append(f"submodule scope: {tree} is checked out but "
                            "contributes no analysed source")
    if counts["hdl"] != len(analysed):
        problems.append(f"census: the printed hdl/ count {counts['hdl']} is "
                        f"not the number of files analysed ({len(analysed)})")
    return problems


def _fail_setup(pkg_errors):
    print("xvlog gate: a package will not analyse, so no module can be graded:",
          file=sys.stderr)
    for f in pkg_errors:
        print(f"  {f.detail()}", file=sys.stderr)
    return 1


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="fail on a new or a vanished finding; write nothing")
    ap.add_argument("--selftest", action="store_true",
                    help="prove the gate reddens on a planted fault")
    args = ap.parse_args(argv[1:])

    xvlog = find_xvlog()

    if args.selftest:
        return cmd_selftest(xvlog)

    # Order matters, and the docstring says why: with no tool nothing can be
    # measured, so the skip is decided BEFORE the missing-tree refusal.
    if xvlog is None:
        print("xvlog gate: SKIPPED (no Vivado xvlog found; set $XVLOG or install "
              "to /home/alex/Xilinx/2026.1). A skip is not a pass.")
        return 0

    missing = missing_submodule_trees()
    if missing:
        return _refuse_missing(missing)

    _pkgs, _mods, counts = source_plan()
    findings, pkg_errors = analyse(xvlog)
    if pkg_errors:
        return _fail_setup(pkg_errors)
    _print_census(findings, counts)

    keys = {f.key for f in findings}
    try:
        budget = read_budget()
    except BudgetError as exc:
        print(f"xvlog gate: {exc}", file=sys.stderr)
        return 2

    if args.check:
        if budget is None:
            print("xvlog gate: no scripts/xvlog.budget to check against; run "
                  "scripts/xvlog_gate.py once to create it", file=sys.stderr)
            return 1
        rc = 0
        for name in SECTIONS:
            here = {k for k in keys if section_of(k) == name}
            new, gone = _diff(here, budget[name])
            for k in new:
                print(f"  REGRESSION [{name}]: {k} is not grandfathered in "
                      f"scripts/xvlog.budget - fix it or add it with a reason",
                      file=sys.stderr)
            for k in gone:
                print(f"  BANK IT [{name}]: {k} no longer occurs - run "
                      f"scripts/xvlog_gate.py to lower the ratchet",
                      file=sys.stderr)
            if new or gone:
                rc = 1
        if rc:
            return rc
        per = ", ".join(f"{len(budget[n])} {SECTION_LABEL[n]}" for n in SECTIONS)
        print(f"xvlog gate: PASS ({len(keys)} finding(s) == ratchet; {per})")
        return 0

    write_budget(findings)
    print(f"wrote {BUDGET.relative_to(ROOT)}: {len(findings)} grandfathered "
          f"finding(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
