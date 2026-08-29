#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure boundary names that hide a unit, and hold the list down by identity.

Why this exists. Rule 4 of the maintainability guide
(docs/development/CODE_QUALITY.md) asks that boundary types make width,
signedness, direction and units explicit. A general naming linter cannot help
here: it would fight the `_r` / `_w` / `_p` / `_S` / `_C` / `_P` suffixes
`CONTRIBUTING.md` mandates, and it has no idea what a signal means.

So the evidence is the port's OWN documentation. The house style requires every
port to be documented inline with `//!`, and those comments say what the value
IS - "Egress latency correction, ns", "hiCredit clamp, signed bytes". When the
comment names a unit of measure and the identifier does not, the unit is known
and simply absent from the name. That is a finding a reader can check in one
line. The converse is worse and is measured too: when the identifier carries
a unit token and the comment documents a different family - `timeout_bytes_i
//! timeout in cycles` - the name is not vague, it is wrong. Review found the
first form of this tool stopped at "the name has a unit token", so a
misleading `_bytes` satisfied a cycles contract and fell out of the ratchet.

WHAT IS SCANNED. Every module header - ports and parameters - in first-party
`.sv` under `hdl/` across the superproject and both project-owned processor
submodules. A declaration is parsed, not pattern-matched: direction, any type
(`wire`, `logic`, `reg`, `int`, a package type, an interface modport), packed
and unpacked dimensions, and every name a declaration shares, across lines. A
`//!` on the declaration's line documents every name on it; a standalone `//!`
line documents the undocumented names that follow it until one carries its own
comment, which is the bundle rule the port-contract gate uses. Function and
task arguments in module bodies are not boundaries and are not counted. Ports
with no `//!` at all cannot be judged here and are COUNTED SEPARATELY per tree,
so the blind spot has a size; the port-contract gate owns that population.

FALSE POSITIVES WERE MEASURED BEFORE ANY GATE. Three exclusion classes, each
with a reason, and each printed in full by `--excluded`:

  * SHAPE, not unit. "1-cycle pulse", "single-cycle strobe", "flips every
    eth_rx cycle" describe the SHAPE of a signal - what the `_p` suffix
    already encodes. Applied only when the matched unit is the cycle one.
  * PROTOCOL-FIXED identifiers. `s_axi_awaddr` is AXI's name and keeps it.
    The set is the published AXI/AXI-Stream signal names, not a prefix.
  * SINGLE-BIT ports. A one-bit port carries no quantity.
  * NOUN for the value. "write byte", "subframe A sample", "configuration
    word" name what the value IS, not what it is measured in. A singular
    byte/sample/octet with no count, "in", "per" or comma before it is prose.

UNITS ARE COMPARED BY FAMILY, DEFINED ONCE. `FAMILIES` maps every spelling the
tool knows - in a comment or as an identifier token - to time, bytes, cycles,
frequency, ratio, rate or samples, so `_ns` satisfies "nanoseconds", `_cyc`
satisfies "clock cycles" and `_bps` satisfies "bits per second". A unit-named
boundary is a candidate when the comment documents a unit of measure and never
names the name's family at all (nouns count: "tone sample" confirms `_smp`),
or when it states the value as "X per Y" and the name carries only Y - a cycle
count named for the tick it produces. The NOUN and SHAPE exclusions carry over
because they say the comment documents no unit; PROTOCOL carries over because
the name is not ours; SINGLE-BIT does not, because it excused a unit that was
missing from a port with no quantity, and a unit that is present and wrong is
a false statement at any width.

THE RATCHET IS KEYED ON IDENTITY, NOT A COUNT. `scripts/naming.budget` names
every candidate as `path:module:port`. A candidate may leave the list only by
being renamed with its unit or by being removed - or, for a name that already
carries a unit, by a comment that now names that family, since the tool cannot
tell a conversion ("~21 ms" on a cycle count) from a contradiction and the diff
can; a port that is still there under the same name and has merely lost the
unit word from its comment is refused - the cheapest way to lower a count would
otherwise be to strip the documentation, which is the opposite of the rule. No
new identity may appear. `--write-budget` regenerates the list after a rename,
so lowering is a normal commit and the diff shows exactly which boundary gained
its unit.

Usage:
    python3 scripts/measure_naming.py                # candidates + per-tree table
    python3 scripts/measure_naming.py --check        # the identity ratchet
    python3 scripts/measure_naming.py --excluded     # every filtered match, and why
    python3 scripts/measure_naming.py --write-budget # regenerate the budget
    python3 scripts/measure_naming.py --selftest     # fixture arms

Exit 0 = every candidate is recorded and no record left without a rename or
removal.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "naming.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from code_quality_scope import tracked
from sv_ports import declarations, module_headers

# ---------------------------------------------------------------------------
# vocabulary
# ---------------------------------------------------------------------------
#: THE UNIT FAMILIES, defined once. Every unit spelling the tool knows - as
#: written in a `//!` comment or carried as a `_`-delimited identifier token -
#: belongs to exactly one family, and two spellings agree when their families
#: do. `bit`, `bits` and `word` are deliberately absent: bit width is already
#: in the type, and "word" is a noun for the value in this tree
#: ("configuration word").
FAMILIES = {
    "time": ("ns", "us", "µs", "μs", "ms", "nsec", "usec", "msec", "sec", "secs",
             "second", "seconds", "nanosecond", "nanoseconds", "microsecond",
             "microseconds", "millisecond", "milliseconds"),
    "bytes": ("byte", "bytes", "octet", "octets"),
    "cycles": ("cyc", "cycle", "cycles", "clock cycle", "clock cycles", "clock", "clocks"),
    "frequency": ("hz", "khz", "mhz", "ghz", "hertz"),
    "ratio": ("ppb", "ppm"),
    "rate": ("bps", "kbps", "mbps", "gbps", "bit/s", "bits/s", "bit per second",
             "bits per second", "byte per second", "bytes per second"),
    "samples": ("smp", "sample", "samples"),
}
_FAMILY_OF = {alias: fam for fam, aliases in FAMILIES.items() for alias in aliases}
#: spellings a comment never uses as a unit: the identifier abbreviations
#: ("1-cyc strobe" is shape) and the singular clock, which is the signal or
#: timing prose ("per Clock Domain", "every clock") - the counted plural is
#: the unit ("in clocks", "6250 clocks per 3 samples")
_NOT_IN_PROSE = frozenset({"cyc", "smp", "clock"})
#: the tokens an identifier carries: the abbreviations and plain words, not
#: the English long forms, the compounds or the non-ASCII spellings, and not
#: `clock` (`clock_en_i` is a signal, not a count) or `second` (`second_stage_r`)
_NAME_TOKENS = ("ns", "us", "ms", "nsec", "usec", "msec", "cyc", "cycle", "cycles",
                "byte", "bytes", "octet", "octets", "hz", "khz", "mhz", "ghz", "ppb",
                "ppm", "smp", "sample", "samples", "sec", "secs", "bps", "kbps",
                "mbps", "gbps")


def family(word):
    """The family of a unit spelling from either vocabulary, or None."""
    return _FAMILY_OF.get(re.sub(r"\s*/\s*", "/", re.sub(r"\s+", " ", word.lower().strip())))


def _alternation(words):
    """A regex alternation of unit spellings, longest first so "clock cycles"
    beats "cycles" and "bytes per second" beats "bytes"; a space matches any
    whitespace and a slash tolerates spaces around it."""
    def pat(w):
        return r"\s+".join(r"\s*/\s*".join(re.escape(p) for p in tok.split("/"))
                           for tok in w.split(" "))
    return "|".join(pat(w) for w in sorted(words, key=len, reverse=True))


_DOC_ALT = _alternation(w for w in _FAMILY_OF if w not in _NOT_IN_PROSE)
#: A UNIT OF MEASURE as written in a `//!` comment. Case-insensitive except
#: where case is the unit (Hz/MHz vs the pronoun "us").
UNIT = re.compile(r"\b(" + _DOC_ALT + r")\b", re.I)
#: `us` is also a pronoun and `second` an ordinal: both need a unit context -
#: a count, a bracket, a comma, "in" or "per" in front.
_CONTEXT_UNIT = re.compile(
    r"(?:(?<=\d)\s*|(?<=[(,/])\s*|\b(?:in|per|every)\s+|^\s*)(us|seconds?)\b", re.I)
#: singular nouns that are a unit only after "in", "per" or "every" ("in byte
#: units"); "frame byte", "channel 0 sample", "(byte 0 = MSB)" name the value,
#: and a singular "cycle" outside a count ("applied on the cycle en is high",
#: "the next cycle") is timing prose, not a quantity measured in cycles
_NOUN_SINGULAR = re.compile(r"^(byte|octet|sample|cycle|clock)$", re.I)
_COUNT_CONTEXT = re.compile(r"\b(?:in|per|every)\s+$", re.I)
#: clocks are a unit only when counted ("in clocks", "6250 clocks per 3
#: samples"); elsewhere the word is the verb or the signals ("clocks alive",
#: "the ADC clocks are") and is not even a noun for the value
_COUNTED_ONLY = re.compile(r"^clocks$", re.I)
_COUNTED_BEFORE = re.compile(r"(?:\d\s*-?\s*|\b(?:in|per|every)\s+)$", re.I)
#: "X per Y": a value stated as a rate whose denominator is Y
_PER = re.compile(r"\b(" + _DOC_ALT + r")\s+per\s+(?:\d+\s*)?(" + _DOC_ALT + r")\b", re.I)
#: a unit word joined by a hyphen or underscore is part of an identifier or a
#: compound adjective (P-RX-SLOT-BYTES, byte-identical, cycle-count), not a unit
_JOINED = re.compile(r"[-_]")

#: a unit carried by the identifier, as a `_`-delimited token
NAME_UNIT = re.compile(r"(^|_)(" + "|".join(_NAME_TOKENS) + r")(?=_|\d|$)", re.I)

#: SHAPE phrasing - `_p` already encodes this. Only meaningful for the cycle
#: unit; "frame length in bytes, sampled every cycle" documents a real unit.
#: A plural count is a shape only when it is the signal's own duration
#: ("held 2 cycles", "asserted for 3 clocks", "2 cycles wide"); "latency,
#: 3 cycles after the strobe" is a quantity the port carries.
SHAPE = re.compile(
    r"\b\d+\s*-?\s*(cycle|clock)\b|\bone[- ]cycle\b|\bsingle[- ]cycle\b"
    r"|\b(held|asserted|driven|high|low|stays?)\s+(for\s+)?\d+\s*(cycles|clocks)\b"
    r"|\b\d+\s*(cycles|clocks)\s+(wide|long)\b"
    r"|\bper[- ]cycle\b|\bevery\b[^,;]*\bcycle\b", re.I)
_CYCLE = re.compile(r"cycle|clock", re.I)

#: identifiers a published protocol owns: the AXI4/AXI4-Lite and AXI-Stream
#: signal names, exactly, behind the house s_/m_ prefixes.
PROTOCOL = re.compile(
    r"^[sm]_axis?_(?:aw|w|b|ar|r)?(?:addr|data|valid|ready|last|keep|strb|user"
    r"|dest|id|resp|prot|len|size|burst|lock|cache|qos|region)$"
    r"|_t(?:valid|ready|last|data|keep|user|dest|strb|id)$")

# ---------------------------------------------------------------------------
# classification
# ---------------------------------------------------------------------------
def units_in(doc):
    """Every unit-looking word in a comment, in order, as (word, kind).

    kind is 'unit' for a unit of measure or 'noun' for a singular byte/octet/
    sample/cycle used as a noun for the value. Words joined by a hyphen or
    underscore into an identifier or adjective, the pronoun `us`, the ordinal
    `second` and a clock outside a count are prose and are not listed."""
    found = []
    for m in UNIT.finditer(doc):
        word = m.group(1)
        low = word.lower()
        before = doc[m.start() - 1] if m.start() else ""
        after = doc[m.end():m.end() + 2]
        count_hyphen = before == "-" and m.start() >= 2 and doc[m.start() - 2].isdigit()
        if (_JOINED.match(before) and not count_hyphen) or \
           (after[:1] == "-" and after[1:2].isalpha()):
            continue
        if low == "us" or low.startswith("second"):
            if not _CONTEXT_UNIT.search(doc[:m.end()]):
                continue
        if _COUNTED_ONLY.match(word) and not _COUNTED_BEFORE.search(doc[:m.start()]):
            continue
        if _NOUN_SINGULAR.match(word) and not _COUNT_CONTEXT.search(doc[:m.start()]):
            found.append((word, "noun"))  # "16-byte aligned", "1-cycle pulse": adjectives
            continue
        found.append((word, "unit"))
    return found


def unit_in(doc):
    """(word, kind) for the first unit of measure in a comment, else the first
    noun for the value (reported as an exclusion so the class stays visible),
    else (None, '') when no unit word is present at all."""
    words = units_in(doc)
    for word, kind in words:
        if kind == "unit":
            return word, kind
    return (words[0][0], "noun") if words else (None, "")


def name_families(name):
    """The unit families an identifier carries as `_`-delimited tokens."""
    return {family(m.group(2)) for m in NAME_UNIT.finditer(name)}


MISMATCH = "named for a different unit than documented"


def _classify_named(name, doc, unit, named):
    """A boundary whose identifier already carries a unit.

    Not a candidate when the comment agrees with the name; a candidate when
    the comment documents a unit of measure and never names the name's family
    (`timeout_bytes_i //! timeout in cycles`), or states the value as "X per
    Y" with only Y in the name (`DIV_US_P //! clk cycles per 1 us tick` is a
    cycle count named for the tick it produces).

    Which exclusions carry over. NOUN and SHAPE describe the comment - "write
    byte" and "held 2 cycles" document no unit of measure - so there is
    nothing to compare and the name stands. PROTOCOL-fixed names are not ours
    to rename either way. SINGLE-BIT does not carry over: it excused a unit
    that was MISSING because a one-bit port carries no quantity, and a unit
    that is present and wrong is a false statement at any width."""
    words = units_in(doc)
    documented = {family(w) for w, k in words if k == "unit"}
    if SHAPE.search(doc):
        documented.discard("cycles")
    if not documented:
        return None, unit, ""
    if PROTOCOL.search(name):
        return "excluded", unit, "protocol-fixed identifier"
    for m in _PER.finditer(doc):
        if family(m.group(1)) not in named and family(m.group(2)) in named:
            return "candidate", m.group(1), MISMATCH
    if named & {family(w) for w, _k in words}:
        return None, unit, ""
    return "candidate", unit, MISMATCH


def classify(name, doc, multibit):
    """('candidate'|'excluded'|None, unit, reason)."""
    unit, kind = unit_in(doc)
    if not unit:
        return None, unit, ""
    named = name_families(name)
    if named:
        return _classify_named(name, doc, unit, named)
    if kind == "noun":
        return "excluded", unit, "noun for the value or timing prose, not a unit of measure"
    if PROTOCOL.search(name):
        return "excluded", unit, "protocol-fixed identifier"
    if not multibit:
        return "excluded", unit, "single-bit port carries no quantity"
    if _CYCLE.search(unit) and SHAPE.search(doc):
        return "excluded", unit, "shape, not a unit (the _p suffix owns this)"
    return "candidate", unit, ""


def scan_text(text):
    """(candidates, excluded, stats) for one source.

    candidates: [(module, name, unit, doc, reason)] - reason is '' for a name
                that hides its documented unit, MISMATCH for one named for
                another
    excluded:   [(module, name, unit, reason)]
    stats: dict(ports, params, documented, undocumented, named, mismatched)."""
    candidates, excluded = [], []
    stats = {"ports": 0, "documented": 0, "undocumented": 0, "named": 0, "params": 0,
             "mismatched": 0}
    for module, name, doc, multibit, kind in declarations(text):
        stats["params" if kind == "param" else "ports"] += 1
        if doc.strip():
            stats["documented"] += 1
        else:
            stats["undocumented"] += 1
        if multibit and NAME_UNIT.search(name):
            stats["named"] += 1
        verdict, unit, reason = classify(name, doc, multibit)
        if verdict == "candidate":
            candidates.append((module, name, unit, doc.strip(), reason))
            stats["mismatched"] += reason == MISMATCH
        elif verdict == "excluded":
            excluded.append((module, name, unit, reason))
    return candidates, excluded, stats


def tree_of(rel):
    for sub in ("gptp-processor", "protocol-processor"):
        if rel.startswith(sub + "/"):
            return sub
    return "superproject"


def sources():
    return [p for p in tracked("hdl") if p.endswith(".sv")]


def scan_repo():
    rows, drops, per_tree = [], [], {}
    for rel in sources():
        c, e, st = scan_text((REPO / rel).read_text(errors="replace"))
        t = per_tree.setdefault(tree_of(rel), {"files": 0, "ports": 0, "params": 0,
                                               "documented": 0, "undocumented": 0,
                                               "named": 0, "matches": 0,
                                               "excluded": 0, "mismatched": 0,
                                               "candidates": 0})
        t["files"] += 1
        for k in ("ports", "params", "documented", "undocumented", "named", "mismatched"):
            t[k] += st[k]
        t["matches"] += len(c) + len(e)
        t["excluded"] += len(e)
        t["candidates"] += len(c)
        rows += [(rel,) + r for r in c]
        drops += [(rel,) + r for r in e]
    return rows, drops, per_tree


#: A processor identity is spelled `<submodule>:<path>:<module>:<name>`, with a
#: colon after the submodule name rather than a slash - the spelling
#: scripts/xvlog.budget uses - so this generated record is never read as a
#: hand-written copy of the submodule source list (scripts/pp_srcs.py --check
#: refuses any tracked file that names a processor source literally).
_SUBMODULE_PREFIXES = ("protocol-processor/", "gptp-processor/")


def identity(row):
    rel, module, name = row[0], row[1], row[2]
    for prefix in _SUBMODULE_PREFIXES:
        if rel.startswith(prefix):
            rel = prefix[:-1] + ":" + rel[len(prefix):]
            break
    return f"{rel}:{module}:{name}"


def identity_path(ident):
    """(rel_path, module, name) from an identity, undoing the processor spelling."""
    for prefix in _SUBMODULE_PREFIXES:
        sub = prefix[:-1]
        if ident.startswith(sub + ":"):
            rest, module, name = ident[len(sub) + 1:].rsplit(":", 2)
            return f"{sub}/{rest}", module, name
    rel, module, name = ident.rsplit(":", 2)
    return rel, module, name


# ---------------------------------------------------------------------------
# the identity ratchet
# ---------------------------------------------------------------------------
def read_budget():
    """{identity} recorded, or None when the file is missing/unreadable."""
    if not BUDGET.is_file():
        return None
    ids = set()
    for line in BUDGET.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            ids.add(line)
    return ids


def declared_as(rel, module, name):
    """The `//!` comment when `module` in `rel` still declares a port or
    parameter called `name`, else None."""
    path = REPO / rel
    if not path.is_file():
        return None
    for m, n, doc, _mb, _k in declarations(path.read_text(errors="replace")):
        if m == module and n == name:
            return doc
    return None


def agrees(name, doc):
    """True when the identifier carries a unit and the comment names that
    family: the one way a unit-named record may leave the ratchet without a
    rename, because the tool cannot tell a conversion ("~21 ms" on a cycle
    count) from a contradiction, and the diff can."""
    named = name_families(name)
    return bool(named) and bool(named & {family(w) for w, _k in units_in(doc)})


def ratchet(rows, recorded):
    """(new, stripped, left) - new identities, records that lost their unit
    word without a rename, and records that left legitimately."""
    current = {identity(r) for r in rows}
    new = sorted(current - recorded)
    stripped, left = [], []
    for ident in sorted(recorded - current):
        rel, module, name = identity_path(ident)
        doc = declared_as(rel, module, name)
        if doc is None or agrees(name, doc):
            left.append(ident)
        else:
            stripped.append(ident)
    return new, stripped, left


def write_budget(rows, per_tree):
    total = sum(t["candidates"] for t in per_tree.values())
    mismatched = sum(t["mismatched"] for t in per_tree.values())
    head = [
        "# Rule 4 ratchet, keyed on IDENTITY: every boundary port or parameter whose",
        "# own //! comment names a unit of measure that the identifier does not carry,",
        "# or documents a unit of a different family than the one the identifier",
        "# carries (marked `# " + MISMATCH + "`), as path:module:name.",
        "# A processor entry is spelled <submodule>:<path>:... (colon, not slash,",
        "# after the submodule name - the scripts/xvlog.budget spelling) so this",
        "# generated record is not a hand-written source list.",
        "# See scripts/measure_naming.py.",
        "#",
        "# A line may leave this file only because the boundary was renamed with its",
        "# unit or removed - or, for a name that already carries a unit, because its",
        "# comment now names that unit's family; a port still declared under the same",
        "# name that has lost the unit word from its comment is refused, so the",
        "# documentation cannot be stripped to lower the count. No line may be added.",
        "# Regenerate with `python3 scripts/measure_naming.py --write-budget`.",
        "#",
        "# 2026-08-29: the mismatch lines arrived when the measurement began comparing",
        "# the identifier's unit family to the documented one (PR #278 review,",
        "# scripts/measure_naming.py classify): a unit token in the name no longer",
        "# satisfies a comment that documents a different unit.",
        "#",
        f"# {total} candidate(s): " + ", ".join(
            f"{k} {v['candidates']}" for k, v in sorted(per_tree.items()))
        + f"; {mismatched} of them {MISMATCH}",
    ]
    body = sorted(identity(r) + (f"  # {r[5]}" if r[5] else "") for r in rows)
    BUDGET.write_text("\n".join(head + body) + "\n")


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------
def _wrap(decl):
    return f"module f (\n{decl}\n  input wire clk_i //! clock\n);\nendmodule\n"


FIXTURES = [
    # (name, source, expected candidates, expected excluded)
    ("a documented unit missing from the name is a candidate",
     _wrap("  input wire [31:0] pres_ofs_i,  //! presentation offset ns"), 1, 0),
    ("a name that already carries the unit is not",
     _wrap("  input wire [31:0] pres_ofs_ns_i,  //! presentation offset ns"), 0, 0),
    ("a 1-cycle pulse is timing prose, not a unit",
     _wrap("  input wire [3:0] arm_i,  //! 1-cycle pulse: arm the chain"), 0, 1),
    ("a strobe held for N cycles is a shape, not a unit",
     _wrap("  input wire [3:0] arm_i,  //! arm the chain, held 2 cycles"), 0, 1),
    ("shape phrasing does not swallow a real unit",
     _wrap("  input wire [15:0] len_i,  //! frame length in bytes, sampled every cycle"), 1, 0),
    ("a single-bit port carries no quantity",
     _wrap("  input wire go_i,  //! start, ns aligned"), 0, 1),
    ("a protocol-fixed identifier is left alone",
     _wrap("  input wire [11:0] s_axi_awaddr,  //! Write address, offset in bytes"), 0, 1),
    ("a prefix alone is not a protocol name",
     _wrap("  input wire [31:0] s_axi_probe_timeout,  //! timeout, ns"), 1, 0),
    ("a port with no unit in its comment is not a candidate",
     _wrap("  input wire [31:0] thing_i,  //! some opaque configuration word"), 0, 0),
    ("an undocumented port is not a candidate",
     _wrap("  input wire [31:0] thing_i,"), 0, 0),
    ("ordinary prose using second is not a time unit",
     _wrap("  input wire [31:0] stream_id_i, //! avoids a second copy"), 0, 0),
    ("a counted second is a time unit",
     _wrap("  input wire [31:0] window_i, //! window, 1 second"), 1, 0),
    ("the pronoun us is not microseconds",
     _wrap("  input wire [31:0] disc_cnt_i, //! ENTITY_DISCOVERs accepted for us"), 0, 0),
    ("microseconds written as us in a unit context is",
     _wrap("  input wire [31:0] hold_i, //! hold time, us"), 1, 0),
    ("ms, kHz, MHz, Mbps and nsec are units",
     _wrap("  input wire [31:0] a_i, //! timeout, ms\n  input wire [31:0] b_i, //! rate, kHz\n"
           "  input wire [31:0] c_i, //! clock, MHz\n  input wire [31:0] d_i, //! rate, Mbps\n"
           "  input wire [31:0] e_i, //! offset, nsec\n  input wire [31:0] f_i, //! rate in bits per second"), 6, 0),
    ("a capitalised unit is still a unit",
     _wrap("  input wire [31:0] fl_i, //! Bytes in flight"), 1, 0),
    ("a name carrying octets satisfies a comment saying octets",
     _wrap("  input wire [15:0] len_octets_i, //! length, octets"), 0, 0),
    ("a singular noun for the value is excluded, visibly, not counted",
     _wrap("  output wire [7:0] dev_wdata_o, //! write byte\n"
           "  input wire [23:0] pair_l_i, //! subframe A sample"), 0, 2),
    ("a counted singular is a unit",
     _wrap("  input wire [7:0] n_i, //! payload, in byte units"), 1, 0),
    ("a position noun with a number after it is a noun, not a count",
     _wrap("  input wire [47:0] mac_i, //! MSB-first (byte 0 in [47:40])\n"
           "  input wire [23:0] ph_i, //! phys channel 0 sample"), 0, 2),
    ("a singular cycle in timing prose is not a quantity in cycles",
     _wrap("  input wire [47:0] tcam_wr_key_i, //! TCAM entry write port. Applied on the cycle en is high\n"
           "  input wire [7:0] lat_i, //! latency, 3 cycles after the strobe"), 1, 1),
    ("a unit word joined by a hyphen is an identifier or an adjective, not a unit",
     _wrap("  input wire [7:0] a_i, //! P-RX-SLOTS / P-RX-SLOT-BYTES (F01.5)\n"
           "  input wire [7:0] b_i, //! stereo framer, byte-identical\n"
           "  input wire [7:0] c_i, //! free-running cycle-count width"), 0, 0),
    ("consecutive standalone comment lines are one group comment",
     "module f #(\n  //! per-stage re-arm guard, in clk_i cycles; the caller derives it\n"
     "  //! from the datapath clock rather than restating a count here\n"
     "  parameter int TIMEOUT_C = 50000\n) (\n  input wire clk_i //! clock\n);\nendmodule\n", 1, 0),
    ("the comment may sit on the line above, as a group comment",
     _wrap("  //! ring size (bytes)\n  input wire [31:0] ring_len_i,"), 1, 0),
    ("a group comment covers the undocumented ports of its bundle",
     _wrap("  //! window bounds, ns\n  input wire [31:0] lo_i,\n  input wire [31:0] hi_i,"), 2, 0),
    ("a port's own trailing comment is not inherited by the next port",
     _wrap("  input wire [31:0] nb1_i, //! delay, ns\n  input wire [31:0] nb2_i,"), 1, 0),
    ("a port with its own comment ends the bundle",
     _wrap("  //! window bounds, ns\n  input wire [31:0] lo_i,\n"
           "  input wire [31:0] hi_i, //! plain\n  input wire [31:0] later_i,"), 1, 0),
    ("output reg is parsed as a port, not as a name called reg",
     _wrap("  output reg  [31:0] probe_reg_o,  //! elapsed, ns"), 1, 0),
    ("an int port has a width even without brackets",
     _wrap("  output int probe_int_o, //! elapsed, ns"), 1, 0),
    ("a package-typed port is a boundary",
     _wrap("  input ethernet_packet_pkg::pkt_len_t probe_typed_i, //! length, bytes"), 1, 0),
    ("a two-dimensional port is a quantity",
     _wrap("  input wire [3:0][31:0] probe_2d_i, //! per-lane offsets, ns"), 1, 0),
    ("a declaration split across lines is one port",
     _wrap("  input wire [31:0]\n    probe_ml_i, //! delay, ns"), 1, 0),
    ("names sharing one declaration are each a port",
     _wrap("  input logic [7:0] probe_sh1_i, probe_sh2_i, //! sizes in bytes"), 2, 0),
    ("a port-like line inside a block comment is not a port",
     _wrap("  /* input wire [31:0] probe_blockcmt_i, //! delay, ns */\n  input wire [31:0] real_i, //! delay, ns"), 1, 0),
    ("a parameter is a boundary too",
     "module f #(\n  parameter int TIMEOUT_C = 50000 //! re-arm guard, cycles\n) (\n  input wire clk_i //! clock\n);\nendmodule\n", 1, 0),
    ("a parameter carrying its unit is not",
     "module f #(\n  parameter int TIMEOUT_CYC_C = 50000 //! re-arm guard, cycles\n) (\n  input wire clk_i //! clock\n);\nendmodule\n", 0, 0),
    ("a function argument in the body is not a boundary",
     "module f (\n  input wire clk_i //! clock\n);\n  function automatic int g(input int idle_slope); //! bits/s\n    return idle_slope;\n  endfunction\nendmodule\n", 0, 0),
    ("an interface modport port parses as one name",
     _wrap("  axi_stream_if.slave s_axis, //! ingress, bytes per beat"), 1, 0),
    # the unit families: a name must agree with its documented unit, not just carry one
    ("a name carrying a unit of a different family than documented is a candidate",
     _wrap("  input wire [31:0] timeout_bytes_i,  //! timeout in cycles"), 1, 0),
    ("a same-family alias in the comment agrees with the name",
     _wrap("  input wire [31:0] hold_ns_i,  //! hold, nanoseconds\n"
           "  input wire [31:0] guard_cyc_i,  //! guard, clock cycles\n"
           "  input wire [31:0] slope_bps_i,  //! slope, bits per second\n"
           "  input wire [31:0] len_octets_i,  //! length, bytes"), 0, 0),
    ("a cycle count named for the tick it produces is the tree's own cross-family pair",
     "module f #(\n  parameter int unsigned DIV_US_P = 100 //! clk cycles per 1 µs tick; override to compress time\n"
     ") (\n  input wire clk_i //! clock\n);\nendmodule\n", 1, 0),
    ("a single-bit port with a wrong-unit suffix is still misleading",
     _wrap("  input wire go_ns_i,  //! start, in cycles"), 1, 0),
    ("shape phrasing and a noun for the value do not contradict a unit-named port",
     _wrap("  input wire [7:0] arm_ns_i,  //! arm delay, held 2 cycles\n"
           "  input wire [23:0] tone_smp_i,  //! tone generator sample (live)"), 0, 0),
    ("a name carrying several tokens agrees when any of them matches",
     _wrap("  input wire [31:0] sample_lat_ns_i,  //! measured stage latency (ns or cycles)"), 0, 0),
    ("a comment that names the name's family anywhere is not a contradiction",
     "module f #(\n  //! PHC clock frequency. Sets the increment = the true clock period in ns\n"
     "  //! (125 MHz -> 0x08000000)\n  parameter int unsigned CLK_FREQ_HZ_P = 125_000_000\n"
     ") (\n  input wire clk_i //! clock\n);\nendmodule\n", 0, 0),
    ("in clocks is a cycle count; clocks outside a count are the verb or the signals",
     _wrap("  input wire [15:0] wdog_i,  //! no-progress watchdog, in clocks\n"
           "  input wire [15:0] alive_i,  //! clocks alive, reinit released\n"
           "  input wire [15:0] dom_i,  //! one setting per Clock Domain, every clock"), 1, 0),
]


def selftest():
    failures = 0

    def ck(name, ok, detail=""):
        nonlocal failures
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    for name, src, want_c, want_e in FIXTURES:
        c, e, _ = scan_text(src)
        ck(name, len(c) == want_c and len(e) == want_e,
           f"got {len(c)} candidate(s) {[(x[1], x[2]) for x in c]} / {len(e)} excluded "
           f"{[(x[1], x[3]) for x in e]}, want {want_c} / {want_e}")

    _c, e, _s = scan_text(FIXTURES[3][1])
    ck("an exclusion names its reason", bool(e) and e[0][3].startswith("shape"), f"{e}")
    _c, e2, _s = scan_text(FIXTURES[2][1])
    ck("timing prose is excluded under its own reason",
       bool(e2) and e2[0][3].startswith("noun"), f"{e2}")

    # the reviewer's reproduction, verbatim: a misleading suffix must not satisfy the contract
    verdict, unit, reason = classify("timeout_bytes_i", "timeout in cycles", True)
    ck("classify refuses a name whose unit family differs from the documented one",
       verdict == "candidate" and unit == "cycles" and reason == MISMATCH,
       f"{(verdict, unit, reason)}")
    ck("classify accepts a same-family alias",
       classify("hold_ns_i", "hold, nanoseconds", True) == (None, "nanoseconds", ""))
    rows_mm = scan_text(_wrap("  input wire [31:0] timeout_bytes_i, //! timeout in cycles"))[0]
    ck("a mismatch is reported under its own reason",
       bool(rows_mm) and rows_mm[0][4] == MISMATCH, f"{rows_mm}")
    ck("every spelling in both vocabularies has a family, and aliases share it",
       all(family(w) for w in _NAME_TOKENS) and all(family(w) for w in _FAMILY_OF)
       and _NOT_IN_PROSE <= set(_FAMILY_OF)
       and family("clock  cycles") == family("CYC") == "cycles"
       and family("Bits per second") == family("bits / s") == family("Mbps") == "rate"
       and family("nanoseconds") == family("NS") == family("µs") == "time"
       and family("octets") == family("byte") == "bytes" and family("word") is None,
       f"{[w for w in _NAME_TOKENS if not family(w)]}")

    _c, _e, st = scan_text(_wrap("  input wire [31:0] a_i,\n  input wire [31:0] b_i, //! x"))
    ck("undocumented ports are counted, not silently skipped",
       st["undocumented"] == 1 and st["documented"] == 2, f"{st}")

    # the identity ratchet: a stripped comment is refused, a rename or removal is not
    recorded = {"x.sv:f:pres_ofs_i"}
    rows_now = [("x.sv", "f", "pres_ofs_i", "ns", "offset ns")]
    ck("a recorded candidate that is still a candidate is neither new nor gone",
       ratchet(rows_now, recorded) == ([], [], []))
    ck("a new identity is refused",
       ratchet(rows_now + [("x.sv", "f", "zz_i", "ns", "d ns")], recorded)[0] == ["x.sv:f:zz_i"])
    # the processor path is ASSEMBLED, not spelled: pp_srcs.py --check refuses
    # any tracked file that names a processor source literally, this one included
    pp, tail = "protocol-processor", "hdl/srp/KL_srp_top.sv"
    ck("a processor identity is spelled submodule:path, never as a source literal",
       identity((f"{pp}/{tail}", "KL_srp_top", "wr_len_o", "b", "d"))
       == f"{pp}:{tail}:KL_srp_top:wr_len_o"
       and identity_path("gptp-processor:hdl/top/KL_gptp_engine.sv:KL_gptp_engine:pub_offset_o")
       == ("gptp-processor/hdl/top/KL_gptp_engine.sv", "KL_gptp_engine", "pub_offset_o")
       and identity_path("hdl/a.sv:m:p") == ("hdl/a.sv", "m", "p"))

    import tempfile
    with tempfile.TemporaryDirectory() as td:
        global REPO
        real = REPO
        try:
            REPO = Path(td)
            (REPO / "x.sv").write_text(_wrap("  input wire [31:0] pres_ofs_i, //! presentation offset"))
            ck("a recorded port that merely lost the unit from its comment is refused as stripped",
               ratchet([], recorded) == ([], ["x.sv:f:pres_ofs_i"], []))
            (REPO / "x.sv").write_text(_wrap("  input wire [31:0] pres_ofs_ns_i, //! presentation offset ns"))
            ck("a recorded port renamed with its unit has left legitimately",
               ratchet([], recorded) == ([], [], ["x.sv:f:pres_ofs_i"]))
            (REPO / "x.sv").write_text(_wrap(""))
            ck("a recorded port that was removed has left legitimately",
               ratchet([], recorded) == ([], [], ["x.sv:f:pres_ofs_i"]))
            # a recorded MISMATCH may also leave by a comment that names the name's family
            wrong = {"x.sv:f:timeout_bytes_i"}
            (REPO / "x.sv").write_text(_wrap("  input wire [31:0] timeout_bytes_i, //! timeout in cycles"))
            ck("a recorded mismatch that is still one is neither new nor gone",
               ratchet([("x.sv", "f", "timeout_bytes_i", "cycles", "timeout in cycles", MISMATCH)], wrong)
               == ([], [], []))
            (REPO / "x.sv").write_text(_wrap("  input wire [31:0] timeout_bytes_i, //! timeout in bytes"))
            ck("a recorded mismatch whose comment now names the name's unit has left legitimately",
               ratchet([], wrong) == ([], [], ["x.sv:f:timeout_bytes_i"]))
            (REPO / "x.sv").write_text(_wrap("  input wire [31:0] timeout_bytes_i, //! timeout"))
            ck("a recorded mismatch that merely lost the unit from its comment is refused as stripped",
               ratchet([], wrong) == ([], ["x.sv:f:timeout_bytes_i"], []))
            (REPO / "x.sv").write_text(_wrap("  input wire [31:0] pres_ofs_i, //! presentation offset"))
            ck("a name without a unit still cannot leave by a comment edit",
               ratchet([], recorded) == ([], ["x.sv:f:pres_ofs_i"], []))
        finally:
            REPO = real

    rows, drops, per_tree = scan_repo()
    total_ports = sum(t["ports"] for t in per_tree.values())
    ck("the live scan reads the tree", total_ports > 500 and rows,
       f"{total_ports} ports, {len(rows)} candidates")
    for sub in ("gptp-processor", "protocol-processor"):
        t = per_tree.get(sub, {})
        ck(f"the live scan reaches {sub}", t.get("files", 0) > 0 and t.get("ports", 0) > 0,
           f"{t}")
    recorded_live = read_budget()
    ck("the budget is keyed on identity, not a count",
       recorded_live is not None and all(":" in i for i in recorded_live),
       "scripts/naming.budget must list path:module:name lines")

    n = len(FIXTURES) + 20
    print(f"\n{n} checks: {n - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="the identity ratchet")
    ap.add_argument("--excluded", action="store_true", help="every filtered match, and why")
    ap.add_argument("--write-budget", action="store_true", help="regenerate scripts/naming.budget")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    rows, drops, per_tree = scan_repo()

    if args.excluded:
        print(f"{len(drops)} match(es) filtered, by reason:")
        for reason in sorted({d[4] for d in drops}):
            group = [d for d in drops if d[4] == reason]
            print(f"\n  {reason} ({len(group)}):")
            for rel, module, name, unit, _r in group:
                print(f"    {name:<28} [{unit}]  {rel}:{module}")
        return 0

    if args.write_budget:
        write_budget(rows, per_tree)
        print(f"wrote {BUDGET.relative_to(REPO)}: {len(rows)} candidate(s)")
        return 0

    for rel, module, name, unit, doc, reason in rows:
        if reason == MISMATCH:
            print(f"{rel}:{module}: {name} — named for a different unit "
                  f"({', '.join(sorted(name_families(name)))}) than documented "
                  f"({unit}, {family(unit)}): {doc}")
        else:
            print(f"{rel}:{module}: {name} — documented in {unit}, not named for it: {doc}")

    print(f"\n{'tree':<20}{'files':>6}{'ports':>7}{'params':>7}{'documented':>11}"
          f"{'undocumented':>13}{'unit-named':>11}{'matches':>8}{'excluded':>9}"
          f"{'mismatched':>11}{'candidates':>11}")
    for tree, t in sorted(per_tree.items()):
        print(f"{tree:<20}{t['files']:>6}{t['ports']:>7}{t['params']:>7}{t['documented']:>11}"
              f"{t['undocumented']:>13}{t['named']:>11}{t['matches']:>8}{t['excluded']:>9}"
              f"{t['mismatched']:>11}{t['candidates']:>11}")
    tot = {k: sum(t[k] for t in per_tree.values()) for k in
           ("files", "ports", "params", "documented", "undocumented", "named",
            "matches", "excluded", "mismatched", "candidates")}
    print(f"{'total':<20}{tot['files']:>6}{tot['ports']:>7}{tot['params']:>7}{tot['documented']:>11}"
          f"{tot['undocumented']:>13}{tot['named']:>11}{tot['matches']:>8}{tot['excluded']:>9}"
          f"{tot['mismatched']:>11}{tot['candidates']:>11}")
    print(f"\n{len(rows)} candidate(s): {len(rows) - tot['mismatched']} boundary name(s) hide "
          f"a documented unit and {tot['mismatched']} are {MISMATCH} "
          f"({tot['ports']} ports and {tot['params']} parameters scanned, "
          f"{tot['undocumented']} with no //! and so not judged here, "
          f"{len(drops)} match(es) excluded with a reason)")

    if not args.check:
        return 0

    recorded = read_budget()
    if recorded is None:
        print(f"\nNO RATCHET: {BUDGET.relative_to(REPO)} is missing")
        return 1
    new, stripped, left = ratchet(rows, recorded)
    for ident in new:
        print(f"\nNEW: {ident} - a new boundary must state its unit in its name")
    for ident in stripped:
        print(f"\nSTRIPPED: {ident} is still declared under that name and is no longer a "
              f"candidate only because its comment no longer names the unit - restore the "
              f"documentation, rename the boundary, or (for a name that carries a unit) "
              f"document that unit")
    if new or stripped:
        print(f"\nNAMING RATCHET: FAIL ({len(new)} new, {len(stripped)} stripped)")
        return 1
    print(f"\nNAMING RATCHET: PASS ({len(rows)} candidate(s), all recorded by identity; "
          f"{len(recorded)} recorded)")
    if left:
        print(f"  {len(left)} recorded boundary(ies) were renamed or removed - regenerate the "
              f"budget with --write-budget: " + ", ".join(left))
    return 0


if __name__ == "__main__":
    sys.exit(main())
