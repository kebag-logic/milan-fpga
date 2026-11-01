#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Page and diagram rendering for the register reference generator (#797).

Renders the model `scripts/gen_register_reference.py` assembles into the
register reference page, in the layout of a technical reference manual: the
memory map, one summary table per module, one section per register with its
WaveDrom `reg` bit-field diagram and field table, and the access legend. Notes
render as paragraphs the concise-prose gate reads, never as a one-column table.
Everything rendered comes from the model; this module adds no register fact.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from register_decode import SymbolicScope
from register_fields import ACCESS_LEGEND, RESET_LEGEND, Effect, Field, Register, conj
from register_rtl import RTL, RtlFacts
from register_sv import WORD_BITS, Node, Refusal, evaluate, parse_expression, unparse

PAGE = "docs/reference/REGISTER_MAP.md"
DIAGRAM_DIR = "docs/diagrams/regmap"
MEMORY_MAP_SVG = "docs/diagrams/memory_map.svg"
RECORD = "docs/design/CSR_REGISTER_NOTES.md"
GENERATOR = "scripts/gen_register_reference.py"
DESCRIPTIONS = "scripts/register_descriptions.json"
SOC = "scripts/register_map_soc.json"


@dataclass
class Module:
    """A contiguous offset range of the Milan CSR block with one heading."""
    key: str
    heading: str
    start: int
    end: int
    purpose: str
    notes: list = field(default_factory=list)
    registers: list[Register] = field(default_factory=list)
    record: str = ""


@dataclass
class Model:
    """Everything the page and the diagrams are rendered from."""
    registers: list[Register]
    modules: list[Module]
    soc: dict
    parameters: list[tuple[str, str, int]]
    version: int
    descriptions: dict
    features: list[tuple[str, str, str]]
    guards: dict[str, str]
    root: Path = Path(".")
    wording: "Wording | None" = None
    mechanisms: list = field(default_factory=list)


# ---------------------------------------------------------------- conditions --
def signal_names(regs: list[Register], desc: dict) -> dict[str, str]:
    """`sig[k]` and whole `sig` -> the register field software reads it at."""
    names: dict[str, str] = {}
    for reg in regs:
        if reg.count > 1:
            continue
        shown = acronym(reg, desc)
        by_signal: dict[str, dict[int, int]] = {}
        for n, src in sorted(reg.sources.items()):
            names.setdefault(src, f"`{shown}[{n}]`")
            sig, _, idx = src.partition("[")
            by_signal.setdefault(sig, {})[int(idx[:-1]) if idx[:-1].isdigit() else n] = n
        for sig, placed in by_signal.items():
            bits = sorted(placed.values())
            if bits == list(range(bits[0], bits[-1] + 1)):
                span = f"{bits[-1]}:{bits[0]}" if len(bits) > 1 else str(bits[0])
                names.setdefault(sig, f"`{shown}[{span}]`" if len(bits) < WORD_BITS else f"`{shown}`")
    return names


class Wording:
    """Conditions from the RTL as plain words: a stored bit by the register
    field software reads it at, anything else by the descriptions file's
    wording. A condition with no wording is refused, so RTL fragments and
    pseudo-code never reach a table cell."""

    def __init__(self, facts: RtlFacts, regs: list[Register], desc: dict) -> None:
        self.facts = facts
        self.names = signal_names(regs, desc)
        self.phrases = desc.get("condition_words", {})
        self.constants = SymbolicScope(facts, {})
        for name in self.phrases:
            if name not in facts.signals and name not in facts.wires:
                raise Refusal(f"{DESCRIPTIONS} words the condition {name}, which {RTL} lacks")

    def value(self, node: Node) -> str:
        """A compared value: a named constant or a number."""
        if node[0] == "id" and self.facts.sym.has(node[1]):
            return f"`{node[1]}`"
        if node[0] == "cast":
            return self.value(node[2])
        if node[0] in ("num", "vec") and node[1].known:
            return f"{node[1].value}"
        raise Refusal(f"{RTL}: the compared value {unparse(node)} has no plain wording")

    def signal(self, node: Node) -> str:
        """A signal or an expression over it, as its field name or wording."""
        base = node[1] if node[0] in ("index", "range", "ipart") else node
        name = base[1] if base[0] == "id" else ""
        phrase = self.phrases.get(name)
        if isinstance(phrase, str):
            return phrase
        key = unparse(node)
        if key in self.names:
            return self.names[key]
        if node[0] == "cast":
            return self.signal(node[2])
        raise Refusal(f"{RTL}: the condition on {key} has no wording; add it to {DESCRIPTIONS} condition_words")

    def boolean(self, node: Node, polarity: bool) -> str:
        """A one-bit signal: its phrase pair, or its field and value."""
        base = node[1] if node[0] == "index" else node
        phrase = self.phrases.get(base[1] if base[0] == "id" else "")
        if isinstance(phrase, list):
            return phrase[0 if polarity else 1]
        return f"{self.signal(node)} is {1 if polarity else 0}"

    def condition(self, node: Node, polarity: bool = True) -> str:
        """Any condition, with `polarity` False meaning its negation."""
        if node[0] == "un" and node[1] == "!":
            return self.condition(node[2], not polarity)
        if node[0] == "bin" and node[1] in ("&&", "||"):
            joiner = " and " if (node[1] == "&&") == polarity else " or "
            return self.condition(node[2], polarity) + joiner + self.condition(node[3], polarity)
        if node[0] == "bin" and node[1] in ("==", "!="):
            same = (node[1] == "==") == polarity
            return f"{self.signal(node[2])} is {'' if same else 'not '}{self.value(node[3])}"
        if node[0] == "bin" and node[1] in ("<", ">=", ">", "<="):
            word = {"<": "below", ">=": "at least", ">": "above", "<=": "at most"}[node[1]]
            lead = "" if polarity else "not "
            return f"{self.signal(node[2])} is {lead}{word} {self.value(node[3])}"
        return self.boolean(node, polarity)

    def conditions(self, conds: tuple) -> str:
        """(node, polarity) pairs joined with `and`."""
        return " and ".join(self.condition(node, polarity) for node, polarity in conds)

    def rtl(self, text: str) -> str:
        """A condition spelled as RTL text."""
        return self.condition(parse_expression(text))


# ------------------------------------------------------------------ helpers --
def strip_md(text: str) -> str:
    """Heading text as a reader sees it, as `scripts/gen_toc.py` reads it."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "")
    text = re.sub(r"\*\*([^*]*)\*\*", r"\1", text)
    return text.strip()


def anchor(text: str, seen: dict[str, int]) -> str:
    """GitHub's heading-anchor algorithm, the one `scripts/gen_toc.py` uses."""
    a = strip_md(text).lower()
    a = re.sub(r"[^\w\- ]", "", a, flags=re.UNICODE)
    a = a.replace(" ", "-")
    n = seen.get(a, 0)
    seen[a] = n + 1
    return a if n == 0 else f"{a}-{n}"


#: Repository directories a description's link may start from.
REPO_ROOTS = ("hdl/", "sw/", "docs/", "scripts/", "configs/", "tb/", "syn/", "tests/", "avdecc/", "tools/",
              "ci/", ".github/")
LINK_TARGET_RE = re.compile(r"\]\((?!https?:|#|/)([^)\s]+)\)")


def page_links(text: str) -> str:
    """Descriptions spell link targets from the repository root; the page
    needs them relative to itself."""
    def _fix(m: re.Match) -> str:
        target = m.group(1)
        root_relative = (target.split("/", 1)[0] + "/") in REPO_ROOTS or target in (
            "README.md", "CONTRIBUTING.md", "REQUIREMENTS.md", "AGENTS.md")
        return f"]({relative(target)})" if root_relative else m.group(0)
    return LINK_TARGET_RE.sub(_fix, text)


def cell(text: str) -> str:
    """Text safe inside one table cell, its links made page-relative."""
    return re.sub(r"(?<!\\)\|", r"\\|", page_links(" ".join(str(text).split())))


def human_size(n: int) -> str:
    """A byte count in decimal, with its binary multiple when exact."""
    for unit, shift in (("GiB", 30), ("MiB", 20), ("KiB", 10)):
        if n >= 1 << shift and n % (1 << shift) == 0:
            return f"{n:,} ({n >> shift} {unit})"
    return f"{n:,}"


def acronym(reg: Register, desc: dict) -> str:
    """The register's documented name: the descriptions file's acronym for
    the RTL label, the label itself otherwise; `n` marks an array."""
    name = desc.get("registers", {}).get(reg.label, {}).get("acronym", reg.label)
    return name + ("n" if reg.count > 1 else "")


def heading(reg: Register, desc: dict) -> str:
    """`ACRONYM register (offset 0xNNN) [reset = 0xNNNNNNNN]`."""
    if reg.count > 1:
        last = reg.offset + reg.stride * (reg.count - 1)
        where = f"offset 0x{reg.offset:03X} to 0x{last:03X}, stride 0x{reg.stride:X}"
        return f"{acronym(reg, desc)} registers ({where}) [reset = {reg.reset}]"
    return f"{acronym(reg, desc)} register (offset 0x{reg.offset:03X}) [reset = {reg.reset}]"


def svg_path(module: Module, reg: Register, desc: dict) -> str:
    """Where a register's bit-field diagram is committed."""
    return f"{DIAGRAM_DIR}/{module.key}/{acronym(reg, desc)}.svg"


def relative(target: str, page: str = PAGE) -> str:
    """A repository path as a link relative to the page's directory, the
    shortest spelling (lexical; no filesystem access)."""
    path, anchor_part = (target.split("#", 1) + [""])[:2]
    here = PurePosixPath(page).parent.parts
    there = PurePosixPath(path).parts
    common = 0
    while common < min(len(here), len(there)) and here[common] == there[common]:
        common += 1
    rel = "/".join([".."] * (len(here) - common) + list(there[common:]))
    return rel + ("#" + anchor_part if anchor_part else "")


# ----------------------------------------------------------- field details --
def field_text(reg: Register, fl: Field, model: Model) -> str:
    """The description cell: the descriptions file's text, then what the
    RTL says about the field's side effects, generated."""
    regd = model.descriptions.get("registers", {}).get(reg.label, {})
    parts = []
    text = regd.get("fields", {}).get(fl.name, "")
    if text:
        parts.append(text)
    elif fl.name == "RESERVED":
        parts.append("Reserved." if fl.access == "R" else "Reserved; stored and read back, drives nothing.")
    else:
        parts.append(source_text(reg, fl, model))
    if fl.span:
        parts.append(f"Bits {fl.span} of the RTL value.")
    parts += store_conditions(fl, model)
    for note in fl.notes:
        if not note.startswith("cond:"):
            parts.append(note_text(note, fl, model))
    parts += side_effect_text(reg, fl, model)
    return " ".join(sentence(p) for p in parts if p)


def sentence(text: str) -> str:
    """A cell part ends with punctuation, so the next part reads as its own."""
    return text if text.rstrip("*`)").endswith((".", ":", "?", "!")) or text.endswith((".", ")")) else text + "."


def store_conditions(fl: Field, model: Model) -> list[str]:
    """When a write reaches this field: every path that stores it, in one
    sentence, so a window word does not repeat itself once per path."""
    paths = [model.wording.rtl(note.partition(":")[2].strip()) for note in fl.notes if note.startswith("cond:")]
    if not paths:
        return []
    terms = [set(path.split(" and ")) for path in paths]
    kept = [path for path, own in zip(paths, terms) if not any(other < own for other in terms)]
    return ["A write takes effect only when " + ", or when ".join(kept) + "."]


def source_text(reg: Register, fl: Field, model: Model) -> str:
    """A field without prose still says what it is, from the RTL: the input it
    reads, the output it drives, or the storage that holds it."""
    facts = model.wording.facts
    signals = facts.signals
    lower = fl.name.lower()
    if "W" in fl.access and f"o_{lower}" in signals:
        return f"Drives `o_{lower}`."
    src = reg.sources.get(fl.lo, "")
    sig = src.partition("[")[0]
    if reg.views and "W" in fl.access:
        return ""
    if sig.startswith("i_"):
        return f"Reads input `{sig}`."
    if sig.startswith("o_") or f"o_{lower}" in signals:
        return f"Reads back `o_{lower}`."
    if sig:
        return f"Held in `{sig}`."
    if any(n.startswith("expr:") for n in fl.notes):
        return ""
    return "Constant." if fl.access == "R" else ""


def side_effect_text(reg: Register, fl: Field, model: Model) -> list[str]:
    """Generated sentences for a key-compared write, for a guard bit and for
    what else a write does, in the row of the field the write lands on."""
    out = []
    for effect in reg.side_effects:
        kind, _, rest = effect.partition(":")
        if kind == "magic" and fl.name != "RESERVED" and "W" in fl.access:
            key, storage = rest.split(":", 1)
            value = int(key, 16)
            text = value.to_bytes(4, "big").decode("ascii", "replace")
            spelled = f" (ASCII `{text}`)" if text.isprintable() and text.isalnum() else ""
            out.append(f"Writing exactly `0x{value:08X}`{spelled} clears it; any other written value sets it.")
            guarded = model.guards.get("guarded:" + storage)
            if guarded:
                out.append(guarded)
    groups: dict[tuple, list[Effect]] = {}
    for effect in reg.effects:
        if effect_row(reg, effect) is fl:
            groups.setdefault((conj(effect.conds), effect.trigger), []).append(effect)
    for (_, trigger), effects in groups.items():
        out.append(effect_sentence(effects, trigger, model))
    return out


def effect_row(reg: Register, effect: Effect) -> Field | None:
    """The field a write's further action is stated in: the written bit that
    fires it, otherwise the word's first writable field."""
    if effect.trigger is not None:
        return next((f for f in reg.fields if f.lo <= effect.trigger <= f.hi), None)
    writable = next((f for f in reg.fields if "W" in f.access), None)
    return writable or (reg.fields[0] if reg.fields else None)


EFFECT_VERBS = (("sets", "sets"), ("clears", "clears"), ("counts", "counts in"), ("loads", "loads"))


def effect_sentence(effects: list[Effect], trigger: int | None, model: Model) -> str:
    """`When <condition>, a write also sets `a` and clears `b`.`"""
    actions = []
    for action, verb in EFFECT_VERBS:
        targets = sorted({f"`{e.target}`" for e in effects if e.action == action})
        if targets:
            actions.append(f"{verb} {', '.join(targets)}")
    lead = "writing 1 also " if trigger is not None else "a write also "
    conds = effects[0].conds
    if conds:
        return f"When {model.wording.conditions(conds)}, {lead}{' and '.join(actions)}."
    return f"{lead.capitalize()}{' and '.join(actions)}."


def note_text(note: str, fl: Field, model: Model) -> str:
    """One generated side-effect sentence for a field note."""
    kind, _, arg = note.partition(":")
    arg = arg.strip()
    if kind == "masked":
        return f"A write stores 0 here while {model.wording.rtl(arg)}."
    if kind == "reads":
        return f"A read returns `{arg}`."
    if kind == "writes":
        return f"A write sets `{arg}`; a read returns this field."
    if kind == "or":
        return f"A read returns the OR with `{arg}`."
    if kind == "key":
        return "A write compares the whole word with the unlock key."
    if kind == "expr":
        return f"Reads `{arg}`."
    if kind == "strobe":
        reads_other = any(n.startswith("reads:") for n in fl.notes)
        status = "" if fl.access == "W1S" or reads_other else " A read returns this bit's status."
        return f"Writing 1 fires `{arg}` for one cycle.{status}"
    if kind == "w1c":
        return "Writing 1 clears this latched bit; writing 0 leaves it."
    if kind == "any":
        span, _, name = arg.partition(" ")
        return f"Writing any set bit in `[{span}]` fires `{name}` once."
    raise Refusal(f"no wording for the field note {note!r}")


DIAGRAM_LANES = 4


def diagram(reg: Register) -> dict:
    """The WaveDrom `reg` source of one register, LSB first. A field crossing
    a lane is split at the lane boundary, so every lane shows its bit numbers
    and no row of the diagram is left blank."""
    lane_bits = WORD_BITS // DIAGRAM_LANES
    fields = []
    for fl in sorted(reg.fields, key=lambda f: f.lo):
        lo = fl.lo
        while lo <= fl.hi:
            hi = min(fl.hi, (lo // lane_bits + 1) * lane_bits - 1)
            entry = {"bits": hi - lo + 1, "name": fl.name, "attr": f"{fl.access}-{fl.reset}"}
            if fl.name == "RESERVED":
                entry["type"] = 1
            fields.append(entry)
            lo = hi + 1
    return {"reg": fields, "config": {"bits": WORD_BITS, "lanes": DIAGRAM_LANES, "hspace": 1000, "fontsize": 11}}


# ---------------------------------------------------------------- sections --
def contents(model: Model) -> list[str]:
    """The page's Contents block, one entry per `##` section."""
    rows = [[f"[{strip_md(title)}](#{anchor(title, {})})", purpose] for title, purpose in top_sections(model)]
    return ["## Contents", ""] + table(["Section", "What it holds"], rows)


def top_sections(model: Model) -> list[tuple[str, str]]:
    """(heading, one-line purpose) of every `##` section, in page order."""
    page = model.descriptions.get("page", {})
    rows = [("Reading this page", page.get("reading_purpose", "How the verdicts and codes read.")),
            ("Memory map", "Regions and windows of the shipping SoC."),
            ("Access types", "The access and reset codes the tables use."),
            ("Build parameters", "The parameters the shipping build elaborates.")]
    rows += [(m.heading, m.purpose) for m in model.modules]
    rows += [("SoC CSR banks", "The LiteX CSR banks beside the Milan block."),
             ("Feature status", "Machine-checked status rows for this page.")]
    return rows


def header(model: Model) -> list[str]:
    """Title, provenance and the regeneration commands."""
    soc = model.soc
    return [
        "# Milan CSR register reference",
        "",
        f"**GENERATED** by `{GENERATOR}` from `{RTL}` and a builder export.",
        "Do not hand-edit.",
        "",
        "Regenerate after any CSR change, then run the gate.",
        "",
        "```sh",
        f"python3 {GENERATOR} --write",
        f"python3 {GENERATOR} --check",
        "```",
        "",
        f"The SoC facts come from the `{soc['shape']}` export, recorded in `{SOC}`.",
        "",
        "Production classes are in [REGISTER_MAP_CLASSES.md](REGISTER_MAP_CLASSES.md).",
        "",
        f"Rationale and version history are in the [design notes]({relative(RECORD)}).",
        "",
    ]


def reading(model: Model) -> list[str]:
    """The page-level notes the descriptions file carries."""
    page = model.descriptions.get("page", {})
    out = ["## Reading this page", ""]
    for para in page.get("intro", []):
        out += [para, ""]
    out += mechanism_blocks(model, "reading")
    out += notes_block(page.get("notes", []), "###", model.soc)
    return out + record_link(page, "Design record")


def mechanism_blocks(model: Model, module: str) -> list[str]:
    """The diagrams of the mechanisms a section explains, each after its text."""
    out: list[str] = []
    for mech in model.mechanisms:
        if mech.module == module:
            out += [f"### {mech.title}", ""]
            for para in mech.text:
                out += [para, ""]
            out += ["```mermaid"] + mech.lines + ["```", ""]
    return out


def record_link(entry: dict, label: str) -> list[str]:
    """The link to an entry's rationale and history on the design-notes page."""
    if "record" not in entry:
        return []
    return [f"{label}: [design notes]({relative(RECORD)}#{entry['record']}).", ""]


def notes_block(notes: list, level: str, soc: dict | None = None) -> list[str]:
    """Notes in their written order, as prose the concise-prose gate reads. A
    statement is a paragraph, a [topic, text] pair a paragraph led by its
    topic, a carried table a table, a headed group its own heading one level
    down, and a code block is ["Code", text]. A {"when", "text"} note states
    what a build parameter of the export makes true, only while it does."""
    out: list[str] = []
    for item in notes:
        if isinstance(item, dict):
            if "when" in item:
                params = (soc or {}).get("datapath_parameters", {})
                if all(params.get(name) == value for name, value in item["when"].items()):
                    out += [page_links(item["text"]), ""]
            elif "heading" in item:
                out += [f"{level} {page_links(item['heading'])}", ""]
                for para in item.get("intro", []):
                    out += [page_links(para), ""]
                out += notes_block(item.get("rows", []), level + "#" if len(level) < 4 else level, soc)
            elif "table" in item:
                out += table(item["table"][0], item["table"][1:])
        elif isinstance(item, list) and item and item[0] == "Code":
            out += ["```text", item[1], "```", ""]
        elif isinstance(item, list):
            out += [f"**{item[0]}:** {page_links(' '.join(item[1:]))}", ""]
        else:
            out += [page_links(item), ""]
    return out


def table(head: list[str], rows: list[list]) -> list[str]:
    """A Markdown table. A one-column table is a paragraph in disguise that the
    concise-prose gate cannot read, so it is refused."""
    if len(head) < 2:
        raise Refusal(f"the one-column table {head} hides prose from the concise-prose gate")
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(cell(c) for c in row) + " |" for row in rows]
    return out + [""]


def memory_map(model: Model) -> list[str]:
    """The SoC memory map: regions, the windows inside them, the Milan
    modules inside the Milan CSR window."""
    soc, desc = model.soc, model.descriptions
    out = ["## Memory map", "", f"![Memory map of the shipping SoC]({relative(MEMORY_MAP_SVG)})", ""]
    rows = []
    for region, start, size, text in soc_windows(soc, desc):
        rows.append([region, f"`0x{start:08X}`", f"`0x{start + size - 1:08X}`", human_size(size), text])
    out += table(["Region", "Start address", "End address", "Size", "Description"], rows)
    out += ["### Milan CSR modules", ""]
    base = next(r["origin"] for r in soc["memory_regions"] if r["name"] == "milan_csr")
    seen: dict[str, int] = {}
    anchors = {}
    for title, _ in top_sections(model):
        anchors[title] = anchor(title, seen)
    rows = []
    for m in model.modules:
        rows.append([f"[{strip_md(m.heading)}](#{anchors[m.heading]})", f"`0x{base + m.start:08X}`",
                     f"`0x{base + m.end:08X}`", human_size(m.end - m.start + 1), m.purpose])
    out += table(["Module", "Start address", "End address", "Size", "Description"], rows)
    return out


def soc_windows(soc: dict, desc: dict) -> list[tuple[str, int, int, str]]:
    """(name, start, size, description) of every region and window, by
    start address, windows after the region that holds them."""
    regions = desc.get("regions", {})
    rows = []
    for r in soc["memory_regions"]:
        rows.append((f"`{r['name']}`", r["origin"], r["size"], regions.get(r["name"], "")))
    flash = next(r for r in soc["memory_regions"] if r["name"] == "spiflash")
    c = soc["constants"]
    for key, name in (("milan_flashboot_aem", "AEM image slot"), ("milan_flash_journal", "saved-state journal"),
                      ("milan_flash_user", "user range")):
        off = c.get(f"{key}_offset")
        size = c.get(f"{key}_size")
        if off is not None and size is not None:
            rows.append((f"`spiflash` {name}", flash["origin"] + off, size, regions.get(key, "")))
    w = soc["pp_windows"]
    stage = w["nvm_stage_base"]
    rows += [("`main_ram` processor window", w["desc_base"], w["window_bytes"], regions.get("pp_window", "")),
             ("`main_ram` descriptor image", w["desc_base"], stage - w["desc_base"], regions.get("pp_desc", "")),
             ("`main_ram` saved-state stage", stage, w["nvm_base"] - stage, regions.get("pp_stage", "")),
             ("`main_ram` saved-state live window", w["nvm_base"], w["resp_base"] - w["nvm_base"],
              regions.get("pp_live", "")),
             ("`main_ram` AECP response buffer", w["resp_base"], w["desc_base"] + w["window_bytes"] - w["resp_base"],
              regions.get("pp_resp", ""))]
    return sorted(rows, key=lambda r: (r[1], -r[2]))


def legend() -> list[str]:
    """The access-type legend."""
    out = ["## Access types", "", "A field's code reads as access, then reset value.", ""]
    out += table(["Code", "Meaning"], [[f"`{c}`", m] for c, m in ACCESS_LEGEND])
    out += table(["Reset code", "Meaning"],
                 [[f"`{c}`", m] for c, m in RESET_LEGEND]
                 + [["`0`, `5h`", "The reset value in hexadecimal; `h` marks hex digits."],
                    ["`see table`", "The reset differs per element; the table under the fields lists it."]])
    out += ["Reserved read-only fields read as `R-0`.", "",
            "A reserved `R/W` field stores bits that drive nothing.", ""]
    return out


def parameters(model: Model) -> list[str]:
    """The milan_csr parameters the shipping build elaborates."""
    rows = [[f"`{name}`", f"`{expr}`", f"{value:,}" if value > 9 else str(value)]
            for name, expr, value in model.parameters]
    return ["## Build parameters", "",
            "Some reset values depend on these parameters.", "",
            "`milan_datapath` sets them; the export supplies its values.", ""] + \
        table(["Parameter", "Set from", "Value"], rows)


def module_section(model: Model, module: Module, seen: dict[str, int]) -> list[str]:
    """One module: purpose, summary table and one section per register."""
    desc = model.descriptions
    out = [f"## {page_links(module.heading)}", "", module.purpose, ""]
    anchor(module.heading, seen)
    for mech in model.mechanisms:
        if mech.module == module.key:
            anchor(mech.title, seen)
    heads = [heading(r, desc) for r in module.registers]
    local = dict(seen)
    links = [anchor(h, local) for h in heads]
    rows = []
    for reg, link in zip(module.registers, links):
        name = desc.get("registers", {}).get(reg.label, {}).get("name", "")
        rows.append([f"`0x{reg.offset:03X}`", f"`{acronym(reg, desc)}`", name, f"`{reg.reset}`",
                     f"[section](#{link})"])
    out += table(["Offset", "Acronym", "Register name", "Reset", "Section"], rows)
    out += cbs_table(model, module)
    out += notes_block(module.notes, "###", model.soc)
    out += mechanism_blocks(model, module.key)
    out += record_link({"record": module.record} if module.record else {}, "Rationale and history")
    for reg, head in zip(module.registers, heads):
        anchor(head, seen)
        out += register_section(model, module, reg, head)
    return out


def cbs_table(model: Model, module: Module) -> list[str]:
    """The CBS reset image per queue, from the RTL's CBS_*_RST tables, when
    the module holds the queue window."""
    regs = {r.label: r for r in module.registers}
    if not {"CBS_IDLE", "CBS_HI", "CBS_LO", "CBS_EN"} <= set(regs):
        return []
    classes = model.descriptions.get("cbs_classes", [])
    idle, hi, lo, en = (regs[k].array_resets for k in ("CBS_IDLE", "CBS_HI", "CBS_LO", "CBS_EN"))
    if len(classes) != len(idle):
        raise ValueError(f"{DESCRIPTIONS}: cbs_classes names {len(classes)} queues, the RTL has {len(idle)}")
    rows = []
    for q in range(len(idle) - 1, -1, -1):
        signed = lo[q] - (1 << WORD_BITS) if lo[q] >> (WORD_BITS - 1) else lo[q]
        rows.append([str(q), classes[q], f"{idle[q] // 1_000_000} Mb/s", f"{idle[q] / 1e7:g} %",
                     str(hi[q]), str(signed), str(en[q])])
    return ["Reset image per queue, from `CBS_IDLE_RST`, `CBS_HI_RST`, `CBS_LO_RST` and `CBS_EN_RST`.", ""] + \
        table(["q", "class", "idleSlope", "% of 1 Gb/s", "hiCredit", "loCredit", "shaped"], rows)


def register_section(model: Model, module: Module, reg: Register, head: str) -> list[str]:
    """`### ACRONYM register ...`, purpose, diagram, field table, notes."""
    desc = model.descriptions
    regd = desc.get("registers", {}).get(reg.label, {})
    out = [f"### {head}", "", regd.get("purpose", ""), ""]
    if reg.label == "VERSION":
        hi, lo = model.version >> 16, model.version & 0xFFFF
        out += [f"This build's VERSION is `0x{hi:04X}_{lo:04X}`.", ""]
    out += [f"RTL name: `{reg.rtl_name}`.", ""]
    out += [f"![{acronym(reg, desc)} bit fields]({relative(svg_path(module, reg, desc))})", ""]
    rows = [[fl.bits, f"`{fl.name}`", fl.access, fl.reset, field_text(reg, fl, model)] for fl in reg.fields]
    out += table(["Bit", "Field", "Type", "Reset", "Description"], rows)
    out += read_value_table(reg, model)
    if reg.count > 1 and reg.array_resets is not None and len(set(reg.array_resets)) > 1:
        out += table(["n", "Offset", "Reset"],
                     [[str(n), f"`0x{reg.offset + n * reg.stride:03X}`", f"`0x{v:08X}`"]
                      for n, v in enumerate(reg.array_resets)])
    out += notes_block(regd.get("notes", []), "####", model.soc)
    out += record_link(regd, "Rationale and history")
    return out


def read_value_table(reg: Register, model: Model) -> list[str]:
    """What a read returns, per condition, for a word several values can reach."""
    if not reg.views:
        return []
    rows = []
    live = [leaf for _, leaf in reg.views if not leaf_constant(leaf, model)]
    for conds, leaf in reg.views:
        rows.append([model.wording.conditions(conds), leaf_text(leaf, len(live) == 1, model)])
    return table(["When", "A read returns"], rows)


def leaf_constant(leaf: Node, model: Model) -> bool:
    """Whether a read value is fixed whatever the state."""
    try:
        return evaluate(leaf, model.wording.constants).known
    except Refusal:
        return False


def leaf_text(leaf: Node, single_live: bool, model: Model) -> str:
    """One read value: a number, the fields above, or its RTL source."""
    if leaf_constant(leaf, model):
        return f"`0x{evaluate(leaf, model.wording.constants).resized(WORD_BITS).value:08X}`"
    return "the fields above" if single_live else f"`{unparse(leaf)}`"


def soc_banks(model: Model) -> list[str]:
    """The LiteX CSR banks, and the registers of the banks this page owns."""
    soc, desc = model.soc, model.descriptions
    banks = sorted(soc["csr_banks"], key=lambda b: b["origin"])
    origins = [b["origin"] for b in banks]
    page = min(b - a for a, b in zip(origins, origins[1:]))
    out = ["## SoC CSR banks", "", "LiteX assigns these banks; each spans one CSR page.", ""]
    bank_text = desc.get("csr_banks", {})
    out += table(["Bank", "Start address", "End address", "Size", "Description"],
                 [[f"`{b['name']}`", f"`0x{b['origin']:08X}`", f"`0x{b['origin'] + page - 1:08X}`",
                   human_size(page), bank_text.get(b["name"], "")] for b in banks])
    owned = desc.get("soc_registers", {})
    rows = [[f"`0x{r['address']:08X}`", f"`{r['name']}`", str(r["words"]), r["mode"].upper(), owned[r["name"]]]
            for r in sorted(soc["csr_registers"], key=lambda r: r["address"]) if r["name"] in owned]
    out += ["### Milan registers in the LiteX banks", ""]
    out += table(["Address", "Register", "Words", "Mode", "Description"], rows)
    out += notes_block(desc.get("soc_notes", []), "###", soc)
    out += record_link({"record": desc["soc_record"]} if "soc_record" in desc else {}, "Rationale and history")
    return out


def feature_block(model: Model) -> list[str]:
    """The ledger rows that name this page, rendered from the ledger."""
    out = ["## Feature status", "", "These rows come from the feature status ledger.", "",
           "<!-- milan-feature-status:start -->", "| Feature ID | Status | Canonical value |", "|---|---|---|"]
    for ident, status, value in model.features:
        shown = "-" if value == "-" else f"`{value}`"
        out.append(f"| `{ident}` | `{status}` | {shown} |")
    return out + ["<!-- milan-feature-status:end -->", ""]


def render_page(model: Model) -> str:
    """The whole register reference page."""
    out = header(model) + contents(model) + reading(model) + memory_map(model) + legend() + parameters(model)
    seen: dict[str, int] = {}
    for title in ("Reading this page", "Memory map", "Access types", "Build parameters"):
        anchor(title, seen)
    for mech in model.mechanisms:
        if mech.module == "reading":
            anchor(mech.title, seen)
    for module in model.modules:
        out += module_section(model, module, seen)
    out += soc_banks(model) + feature_block(model)
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out) + "\n"


def module_sources(model: Model) -> dict[str, str]:
    """One generated WaveDrom source per module: every register's `reg`
    description, with the SVG each one renders to."""
    out = {}
    for module in model.modules:
        regs = [{"acronym": acronym(r, model.descriptions), "offset": f"0x{r.offset:03X}",
                 "svg": svg_path(module, r, model.descriptions), "wavedrom": diagram(r)}
                for r in module.registers]
        body = {"generated_by": f"python3 {GENERATOR} --write", "module": module.key,
                "heading": strip_md(module.heading), "registers": regs}
        out[f"{DIAGRAM_DIR}/{module.key}.json"] = json.dumps(body, indent=2) + "\n"
    return out
