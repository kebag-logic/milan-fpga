#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
shape_consumer_inventory.py - what a shape-header reference RESOLVES TO.

Arm I of scripts/check_entity_shape.py asks one question of every tracked
file in the tree: does each reference to gen/adp_shape_defaults.svh name a
file that is actually there?  Answering it is a subject of its own - make
variable expansion, `+=`, `include`, `$(shell ...)`, immediate `:=` freezing
and the rule lines make expands at parse time - and it is the part that has
been got wrong twice.  It lives here, apart from the arms that judge entity
shapes, so that "how a build expression becomes a repository path" can be
read and reviewed on its own.

WHAT THIS MODULE PRODUCES.  `dangling_consumers(name, text, tracked)` is the
finding list for ONE file: the references it spells that resolve to nothing
tracked, resolve outside the repository, or cannot be settled at all.  It is
FAIL CLOSED - "could not tell" is a finding, never a pass - and the only way
past it is a CLASSIFIED_CONSUMERS entry naming the reason.

For a makefile the resolution is done by MAKE ITSELF, twice: the reference
expanded in the consumer's own directory (final variable state, includes and
functions applied), cross-checked against the frozen value of every variable
assigned from it, and then the prerequisites make froze into its post-parse
database.  A hand-rolled model of make was tried and mis-read `+=`, a later
`:=` and an `include` override, banking confidently wrong resolutions as
clean; make is the only reader that agrees with the build by construction.

GATE_SOURCES lists the files whose own text is FIXTURE rather than
consumption - this module (it carries the matching pattern), the gate, and
the self-test that plants deliberately stale paths.
"""

import os
import re
import subprocess
from pathlib import Path, PurePosixPath

#: The repository root, spelled with pathlib so this module needs no import
#: back into check_entity_shape.py, which computes the same directory.
ROOT = Path(__file__).resolve().parent.parent

#: Any literal that names the shape header, with or without a build variable
#: in front of it ($(RTL_DIR)/..., ../../hdl/..., configs/generated/...).
CONSUMER_RE = re.compile(r"[\w$(){}./\\-]*gen/adp_shape_defaults\.svh")


ASSIGN_RE = re.compile(r"^\s*(\w+)\s*[:?]?=\s*(\S+)\s*$", re.MULTILINE)
VARIABLE_RE = re.compile(r"\$[({]?(\w+)[)}]?")
SHAPE_BASENAME = "adp_shape_defaults.svh"

#: References to the shape header that no static expansion can settle, each
#: classified with the reason it is not a tracked-header consumer. This set
#: is the ONLY way past the inventory: an unresolvable reference that is not
#: listed here is a finding, because "could not tell" must not read as "fine".
CLASSIFIED_CONSUMERS = {
    ("sw/litex/sweep.sh", "$CFG_GEN/gen/adp_shape_defaults.svh"):
        "a per-config copy chosen at build time under configs/generated/",
    ("tb/verilator/milan_dp/Makefile",
     "gen_divergent/gen/adp_shape_defaults.svh"):
        "written by gen_divergent_shape.py during the suite, never tracked",
    ("tb/verilator/milan_dp/gen_divergent_shape.py",
     "gen_divergent/gen/adp_shape_defaults.svh"):
        "the same generated file, named by the script that writes it",
}

#: Repo-root-anchored prefixes: a reference starting with one of these is
#: relative to the repository, not to the file quoting it.
ROOT_PREFIXES = ("hdl/", "configs/", "scripts/", "sw/", "syn/", "tb/",
                 "docs/", "bd/", "avdecc/")


def _normalized(text: str | PurePosixPath) -> str:
    """A path with its `.` and `..` segments collapsed, LEXICALLY.

    The verdicts this module reaches are about the text a build spells, not
    about what the filesystem happens to hold, so the collapse must never
    follow a symlink the way `Path.resolve()` would: `a/../b` is `b` here
    even when `a` is a link somewhere else entirely, which is how make and
    the compiler read it too. A `..` that walks off the front of a relative
    path SURVIVES - that residue is exactly what marks a reference as
    reaching above the repository, and arm I refuses it by name.
    """
    pure = PurePosixPath(text)
    anchor = pure.anchor
    parts: list[str] = []
    for part in pure.parts:
        if part == "..":
            if parts and parts[-1] not in ("..", anchor):
                parts.pop()
                continue
            if anchor and parts == [anchor]:
                continue          # `/..` is `/`; there is nothing above it
        parts.append(part)
    return str(PurePosixPath(*parts)) if parts else "."


def _repo_relative(absolute: str) -> str:
    """Where an absolute path make printed sits relative to the repository.

    A path outside the tree keeps its leading `..` segments rather than
    raising, because "reaches outside the tracked tree" is a verdict arm I
    reports, not an error it may die on.
    """
    return str(PurePosixPath(_normalized(absolute))
               .relative_to(ROOT, walk_up=True))


def resolve_reference(reference: str, name: str, text: str) -> str | None:
    """Static expansion for script and prose consumers: the repo-relative
    path a reference names, or None when substituting the same-file
    assignments does not settle it. Makefile references never come here --
    make's own engine expands those (resolve_make_reference), because only
    make applies +=, includes and $(shell ...) the way the build does.
    None is NOT a pass -- see the classification below."""
    assignments = dict(ASSIGN_RE.findall(text))
    resolved = reference.lstrip("(")
    for _ in range(4):
        expanded = VARIABLE_RE.sub(
            lambda m: assignments.get(m.group(1), m.group(0)), resolved)
        if expanded == resolved:
            break
        resolved = expanded
    if "$" in resolved:
        return None
    if resolved.startswith(ROOT_PREFIXES):
        return _normalized(resolved)
    return _normalized(PurePosixPath(name).parent / resolved)


MAKE_PROBE_TARGET = "__shape_probe__"

#: An assignment line, however it is spelled: optional `export`/`override`
#: prefixes, any of make's assignment operators. The frozen-value cross
#: check below keys on the VARIABLE being assigned, so a spelling the
#: pattern missed would only ever ADD a probe, never remove one.
ASSIGN_LINE_RE = re.compile(
    r"^[ \t]*(?:export[ \t]+|override[ \t]+)*"
    r"(?P<var>\w+)[ \t]*[:+?]{0,2}=(?P<rhs>.*)$", re.MULTILINE)


def probe_make(directory: Path, makefile: str, expression: str) -> str | None:
    """One expression expanded by make itself in the consumer's own
    directory: final variable state, includes read, `+=`, `$(shell ...)`
    and every assignment applied exactly as a build applies them. Returns
    make's expansion, or None when make errors out."""
    probe = "%s: ; @printf '%%s' \"%s\"" % (MAKE_PROBE_TARGET, expression)
    env = dict(os.environ, MAKEFLAGS="", MFLAGS="")
    try:
        run = subprocess.run(
            ["make", "-s", "--no-print-directory", "-f", makefile,
             "--eval", probe, MAKE_PROBE_TARGET],
            cwd=directory, env=env, capture_output=True, text=True,
            timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if run.returncode != 0 or not run.stdout.strip():
        return None
    return run.stdout.strip()


def shape_prereqs_from_database(directory: Path,
                                makefile: str) -> tuple[bool, list[str]]:
    """Every prerequisite naming the shape header, exactly as make FROZE
    it at parse time. Rule prerequisites are immediate-expansion contexts
    -- a variable defined after the rule line never reaches them however
    the final state reads -- and make's post-parse database records them
    frozen, so it is their ground truth. Returns (ok, tokens); not-ok
    means the database could not be read and nothing is verified."""
    env = dict(os.environ, MAKEFLAGS="", MFLAGS="")
    try:
        run = subprocess.run(["make", "-pqrR", "-f", makefile],
                             cwd=directory, env=env, capture_output=True,
                             text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return False, []
    if "# Files" not in run.stdout:
        return False, []
    tokens = set()
    for line in run.stdout.splitlines():
        if not line or line.startswith(("#", "\t", " ")):
            continue
        idx = line.find(":")
        if idx <= 0 or line[idx + 1:idx + 2] == "=":
            continue
        for token in line[idx + 1:].lstrip(":").split():
            if "$" not in token and token.endswith("/" + SHAPE_BASENAME) \
                    and token.endswith("gen/" + SHAPE_BASENAME):
                tokens.add(token)
    return True, sorted(tokens)


def resolve_make_reference(reference: str, name: str,
                           text: str) -> str | None:
    """The reference expanded by make itself, cross-checked against every
    variable whose assignment carries it. The text probe alone reads the
    FINAL variable state, which an immediate `:=` does not honor -- make
    froze that value at its line, whatever `include`, `export` or a later
    definition did afterwards -- so for each assignment line containing
    the reference, the frozen variable is probed too and the text result
    must appear among its words. Any disagreement, any expansion make
    cannot settle to one word, any make error: None, and None is NOT a
    pass."""
    raw = reference.lstrip("(")
    directory = ROOT / PurePosixPath(name).parent
    makefile = PurePosixPath(name).name
    text_out = probe_make(directory, makefile, "$(abspath %s)" % raw)
    if text_out is None or any(c.isspace() for c in text_out):
        return None
    for m in ASSIGN_LINE_RE.finditer(text):
        if reference not in m.group("rhs"):
            continue
        var_out = probe_make(directory, makefile,
                             "$(abspath $(%s))" % m.group("var"))
        if var_out is None or text_out not in var_out.split():
            return None
    return _repo_relative(text_out)


#: The gate's OWN three sources, skipped by the consumer inventory: between
#: them they carry the CONSUMER_RE pattern itself, its classified entries and
#: every deliberately stale path the self-test plants. None of the three is a
#: consumer of the tracked header; a reference spelled inside them is fixture.
GATE_SOURCES = ("scripts/check_entity_shape.py",
                "scripts/entity_shape_selftest.py",
                "scripts/shape_consumer_inventory.py")


def _judge_consumer(name, reference, target, tracked, seen_targets):
    """One resolved reference's verdict: the finding it earns, or None.

    `seen_targets` is this file's set of already-reported targets, so one
    resolved defect is reported once however many references reach it.
    """
    if target is None:
        return (f"{name}: {reference} cannot be resolved and is not "
                f"classified in CLASSIFIED_CONSUMERS")
    if target.startswith("configs/generated/"):
        return None               # per-config copies are arm D's
    if target in seen_targets:
        return None               # one report per resolved defect
    if not target.startswith("hdl/"):
        seen_targets.add(target)
        return (f"{name}: {reference} -> {target} is outside the "
                f"tracked tree and is not classified")
    if target not in tracked:
        seen_targets.add(target)
        return f"{name}: {reference} -> {target}"
    return None


def _frozen_prereq_findings(name, tracked, seen_targets):
    """Findings from the prerequisites make FROZE at parse time.

    The makefile's second source: an immediate-expansion RULE line that no
    per-reference probe can see ([R8-4]). An unreadable database is itself
    a finding -- nothing about those prerequisites is then verified.
    """
    dangling = []
    directory = ROOT / PurePosixPath(name).parent
    ok, prereqs = shape_prereqs_from_database(
        directory, PurePosixPath(name).name)
    if not ok:
        dangling.append(
            f"{name}: make database unreadable; frozen shape "
            f"prerequisites cannot be verified")
    for token in prereqs:
        if token.lstrip("(") == "gen/" + SHAPE_BASENAME:
            continue
        if (name, token) in CLASSIFIED_CONSUMERS:
            continue
        if PurePosixPath(token).is_absolute():
            target = _repo_relative(token)
        else:
            target = _normalized(PurePosixPath(name).parent / token)
        note = _judge_consumer(name, token, target, tracked, seen_targets)
        if note is not None:
            dangling.append(note)
    return dangling


def dangling_consumers(name: str, text: str, tracked: set) -> list:
    """Every dead or unresolvable shape-header reference in ONE file.

    Two sources, in this order: the references the file's own text spells
    -- expanded by make itself when the file is a makefile -- and then, for
    a makefile, the frozen prerequisites of make's post-parse database.
    """
    dangling = []
    seen_targets = set()
    is_make = name.endswith("Makefile") or name.endswith(".mk")
    references = sorted(set(CONSUMER_RE.findall(text)))
    for reference in references:
        # A bare `gen/...` is an `include directive: the compiler
        # resolves it through the search path, not against the file's
        # own directory. Whether it can bind two ways is arm H's
        # subject. A build prerequisite always carries a prefix.
        if reference.lstrip("(") == "gen/" + SHAPE_BASENAME:
            continue
        if (name, reference) in CLASSIFIED_CONSUMERS:
            continue              # the ONLY way past the inventory
        if is_make:
            target = resolve_make_reference(reference, name, text)
        else:
            target = resolve_reference(reference, name, text)
        note = _judge_consumer(name, reference, target, tracked, seen_targets)
        if note is not None:
            dangling.append(note)
    if is_make and references:
        dangling.extend(_frozen_prereq_findings(name, tracked, seen_targets))
    return dangling
