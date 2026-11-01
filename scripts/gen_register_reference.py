#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the Milan CSR register reference from the RTL (#797).

Why this exists. The register map was a hand-written page of about 2,600
lines that no gate tied to the RTL. It lost the ETH_GUARD word at 0x7D8 for
months, and kept describing PHY_RESET and MAC_STATUS long after the SoC stopped
wiring them that way. #797 asks for the reference to be generated, in the style
of a technical reference manual, and for a gate that fails on any difference.

What is read, and from where:

  * `hdl/common/csr/milan_csr.sv` is the source of truth for the Milan CSR
    block. The offsets are its `A_*` localparams. The reset values are its
    `csr_default` table and its reset block. Which words a write changes, and
    how, is its write decodes. What a read returns is its read decodes. Field
    names are the RTL names: the output port a stored bit drives, or the
    signal a read concatenation places at that bit.
  * the parameters the shipping build elaborates come from the builder
    export's top-level Verilog, recorded with the export's `csr.csv` (memory
    map, LiteX CSR banks) and `aem_desc.json` (the processor windows) in
    `scripts/register_map_soc.json`. That file is written by this script from
    the export (`--soc-from`), never by hand.
  * `scripts/register_descriptions.json` carries the prose: a purpose per
    register, a description per field and notes. It is keyed by RTL register
    and field name, and the generator refuses a key the RTL lacks.
  * the feature-status rows come from `docs/reference/milan_feature_status.json`.

What is written: `docs/reference/REGISTER_MAP.md`, one WaveDrom `reg` source
per module under `docs/diagrams/regmap/` and one SVG per register beside it.

Usage:
    python3 scripts/gen_register_reference.py --write
    python3 scripts/gen_register_reference.py --check
    python3 scripts/gen_register_reference.py --selftest
    python3 scripts/gen_register_reference.py --soc-from DIR   # refresh the SoC extract
    python3 scripts/gen_register_reference.py --check --soc-from DIR

`--check` is the freshness gate: it regenerates everything in memory and fails
on any byte that differs from the tree. With `--soc-from` it also re-extracts
the SoC facts from a builder export and fails if the committed extract differs.

Exit status: 0 fresh or written, 1 stale or a failed control, 2 refused (an
input the generator cannot read, or a description key the RTL lacks).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_doc_style  # noqa: E402
from register_diagrams import mechanisms  # noqa: E402
from register_fields import Deriver, Field, Register, reset_text  # noqa: E402
from register_page import (DESCRIPTIONS, DIAGRAM_DIR, PAGE, RECORD, SOC, Model, Module, Wording, acronym,  # noqa: E402
                           anchor, module_sources, render_page, strip_md)
from register_rtl import (CSR_INCLUDE_DIR, DATAPATH, ROOT, RTL, SHAPE_INCLUDE_DIR, Refusal, RtlFacts,  # noqa: E402
                          csr_parameters, extract_soc, load_rtl, read_text, soc_text, strip_comments)

LEDGER = "docs/reference/milan_feature_status.json"
REGISTER_KEYS = {"acronym", "name", "purpose", "fields", "notes", "rename", "record", "split"}
EM_DASH = "\u2014"
MAX_CELL_WORDS = 200


# ------------------------------------------------------------------- model --
def load_json(root: Path, rel: str) -> dict:
    """A tracked JSON input, refused by name when absent or malformed."""
    try:
        return json.loads(read_text(root, rel))
    except json.JSONDecodeError as exc:
        raise Refusal(f"{rel} is not valid JSON: {exc}") from exc


def build_model(root: Path, soc: dict | None = None) -> tuple[Model, RtlFacts]:
    """Read every input and assemble the model the page is rendered from."""
    soc = soc if soc is not None else load_json(root, SOC)
    overrides, table = csr_parameters(root, soc)
    facts = load_rtl(root, soc["shape"], overrides)
    desc = load_json(root, DESCRIPTIONS)
    literal_words = {int(addr, 16): name for addr, name in desc.get("literal_words", {}).items()}
    regs = Deriver(facts, literal_words).all_registers()
    rename_fields(desc, regs)
    split_fields(desc, regs)
    validate(desc, regs, soc)
    check_record_links(root, desc)
    modules = build_modules(desc, regs)
    ledger = load_json(root, LEDGER)
    features = [(f["id"], f["status"], f.get("value", "-")) for f in ledger["features"] if PAGE in f["documents"]]
    model = Model(regs, modules, soc, table, facts.version, desc, features, guards(regs, desc))
    model.root = root
    model.wording = Wording(facts, regs, desc)
    model.mechanisms = mechanisms(model)
    return model, facts


def rename_fields(desc: dict, regs: list[Register]) -> None:
    """A positional field name the RTL gives no better word for may take a
    name from the descriptions; a key naming no derived field is refused."""
    known = {r.label: r for r in regs}
    for key, entry in desc.get("registers", {}).items():
        for old, new in entry.get("rename", {}).items():
            fields = {f.name: f for f in known[key].fields} if key in known else {}
            if old not in fields:
                raise Refusal(f"{DESCRIPTIONS} renames field {key}.{old}, which {RTL} lacks")
            fields[old].name = new


def split_fields(desc: dict, regs: list[Register]) -> None:
    """A word the RTL reads whole from an input has bit meanings only the
    producer knows. The descriptions may name them, as [bits, name, text] rows
    that cover the derived field exactly; anything else is refused. Access and
    reset stay the derived field's."""
    known = {r.label: r for r in regs}
    for key, entry in desc.get("registers", {}).items():
        for name, rows in entry.get("split", {}).items():
            reg = known.get(key)
            parent = next((f for f in reg.fields if f.name == name), None) if reg else None
            if parent is None:
                raise Refusal(f"{DESCRIPTIONS} splits field {key}.{name}, which {RTL} lacks")
            spans = [tuple(int(x) for x in (row[0].split(":") * 2)[:2]) for row in rows]
            covered = sorted(n for hi, lo in spans for n in range(lo, hi + 1))
            if covered != list(range(parent.lo, parent.hi + 1)):
                raise Refusal(f"{DESCRIPTIONS}: the split of {key}.{name} does not cover bits {parent.bits} exactly")
            parts = [Field(hi, lo, row[1], parent.access, reset_text(reg.reset_bits[lo:hi + 1], short=True),
                           list(parent.notes))
                     for (hi, lo), row in zip(spans, rows)]
            index = reg.fields.index(parent)
            reg.fields[index:index + 1] = parts
            entry.setdefault("fields", {}).update({row[1]: row[2] for row in rows if row[1] != "RESERVED"})


def guards(regs: list[Register], desc: dict) -> dict[str, str]:
    """storage -> `ACRONYM[bit]` for every one-bit field that reads a
    storage register directly, so a guarded write can name its guard; and
    `guarded:<storage>` -> the sentence listing what that guard refuses."""
    out: dict[str, str] = {}
    for reg in regs:
        for fl in reg.fields:
            if fl.hi == fl.lo and fl.name != "RESERVED" and "R" in fl.access:
                out.setdefault(fl.name.lower(), f"`{acronym(reg, desc)}[{fl.bits}]`")
    dropped: dict[str, list[str]] = {}
    masked: dict[str, list[str]] = {}
    for reg in regs:
        for fl in reg.fields:
            for note in fl.notes:
                kind, _, arg = note.partition(":")
                arg = arg.strip()
                if kind == "cond" and arg.startswith("!") and arg[1:] in out:
                    dropped.setdefault(arg[1:], [])
                    name = f"`{acronym(reg, desc)}`"
                    if name not in dropped[arg[1:]]:
                        dropped[arg[1:]].append(name)
                elif kind == "masked" and arg in out:
                    masked.setdefault(arg, []).append(f"`{acronym(reg, desc)}[{fl.bits}]` ({fl.name})")
    for storage in set(dropped) | set(masked):
        parts = []
        if dropped.get(storage):
            parts.append("writes to " + ", ".join(dropped[storage]) + " are dropped")
        if masked.get(storage):
            parts.append(", ".join(masked[storage]) + " is stored as 0")
        out["guarded:" + storage] = "While it is 1, " + "; ".join(parts) + "."
    return out


def validate(desc: dict, regs: list[Register], soc: dict) -> None:
    """Refuse a description of anything the RTL or the export lacks."""
    known = {r.label: r for r in regs}
    for reg in regs:
        entry = desc.get("registers", {}).get(reg.label, {})
        if not entry.get("purpose") or not entry.get("name"):
            raise Refusal(f"{DESCRIPTIONS}: register {reg.label} at 0x{reg.offset:03X} needs a name and a purpose")
    for key, entry in desc.get("registers", {}).items():
        if key not in known:
            raise Refusal(f"{DESCRIPTIONS} describes register {key}, which {RTL} lacks")
        extra = set(entry) - REGISTER_KEYS
        if extra:
            raise Refusal(f"{DESCRIPTIONS}: register {key} has unknown keys {sorted(extra)}")
        names = {f.name for f in known[key].fields}
        for fname in entry.get("fields", {}):
            if fname not in names:
                raise Refusal(f"{DESCRIPTIONS} describes field {key}.{fname}, which {RTL} lacks "
                              f"(its fields: {', '.join(sorted(names))})")
    shown = [acronym(r, desc) for r in regs]
    dupes = sorted({a for a in shown if shown.count(a) > 1})
    if dupes:
        raise Refusal(f"{DESCRIPTIONS}: acronyms used twice: {dupes}")
    csr_names = {r["name"] for r in soc["csr_registers"]}
    for name in desc.get("soc_registers", {}):
        if name not in csr_names:
            raise Refusal(f"{DESCRIPTIONS} describes LiteX CSR {name}, which the export's csr.csv lacks")
    banks = {b["name"] for b in soc["csr_banks"]}
    for name in desc.get("csr_banks", {}):
        if name not in banks:
            raise Refusal(f"{DESCRIPTIONS} describes CSR bank {name}, which the export's csr.csv lacks")
    regions = {r["name"] for r in soc["memory_regions"]} | {
        "milan_flashboot_aem", "milan_flash_journal", "milan_flash_user",
        "pp_window", "pp_desc", "pp_stage", "pp_live", "pp_resp"}
    for name in desc.get("regions", {}):
        if name not in regions:
            raise Refusal(f"{DESCRIPTIONS} describes region {name}, which the export lacks")


def check_record_links(root: Path, desc: dict) -> None:
    """Every design-notes link points at a heading that exists on that page."""
    seen: dict[str, int] = {}
    anchors = {anchor(h, seen) for h in re.findall(r"^#{1,6} (.+)$", read_text(root, RECORD), re.M)}
    wanted = [desc.get("page", {}).get("record"), desc.get("soc_record")]
    wanted += [m.get("record") for m in desc.get("modules", [])]
    wanted += [r.get("record") for r in desc.get("registers", {}).values()]
    for target in wanted:
        if target and target not in anchors:
            raise Refusal(f"{DESCRIPTIONS} links design note #{target}, which {RECORD} lacks")


def build_modules(desc: dict, regs: list[Register]) -> list[Module]:
    """The modules of the descriptions file, each holding the registers its
    offset range covers. Every register belongs to exactly one module."""
    modules = []
    for m in desc.get("modules", []):
        modules.append(Module(m["key"], m["heading"], int(m["start"], 16), int(m["end"], 16),
                              m["purpose"], m.get("notes", []), record=m.get("record", "")))
    modules.sort(key=lambda m: m.start)
    for a, b in zip(modules, modules[1:]):
        if b.start <= a.end:
            raise Refusal(f"{DESCRIPTIONS}: modules {a.key} and {b.key} overlap")
    for reg in regs:
        last = reg.offset + reg.stride * (reg.count - 1)
        home = [m for m in modules if m.start <= reg.offset and last <= m.end]
        if len(home) != 1:
            raise Refusal(f"{RTL}: register {reg.rtl_label} at 0x{reg.offset:03X} has no module in "
                          f"{DESCRIPTIONS}; the map would be missing it")
        home[0].registers.append(reg)
    empty = [m.key for m in modules if not m.registers]
    if empty:
        raise Refusal(f"{DESCRIPTIONS}: modules {empty} hold no register")
    return modules


# ----------------------------------------------------------------- outputs --
_SVG_CACHE: dict[str, str] = {}


def render_svg(source: dict) -> str:
    """One WaveDrom `reg` render, through the pinned `wavedrom` package."""
    key = json.dumps(source, sort_keys=True)
    if key not in _SVG_CACHE:
        try:
            import wavedrom
        except ImportError as exc:
            raise Refusal("the 'wavedrom' package is missing: python3 -m pip install "
                          "wavedrom==2.0.3.post3") from exc
        _SVG_CACHE[key] = wavedrom.render(json.dumps(source)).tostring() + "\n"
    return _SVG_CACHE[key]


def outputs(model: Model) -> dict[str, str]:
    """Every generated file: the page, the per-module sources, the SVGs."""
    page = render_page(model)
    problems = [f"{PAGE}:{f.line}: {f.reason}: {' '.join(f.text.split())[:80]}"
                for f in check_doc_style.analyze(page)]
    problems += oversized_cells(page)
    if EM_DASH in page:
        problems.append(f"{PAGE}: the page carries an em dash")
    seen: dict[str, int] = {}
    anchors = [anchor(h, seen) for h in re.findall(r"^#{1,6} (.+)$", page, re.M)]
    problems += [f"{PAGE}: heading anchor {a} is not unique" for a in anchors if re.search(r"-\d+$", a)
                 and a.rsplit("-", 1)[0] in anchors]
    if problems:
        raise Refusal("the rendered page breaks the documentation rules:\n  " + "\n  ".join(problems))
    out = {PAGE: page, CATALOG: catalog(model), FINGERPRINT: fingerprint(model.root, model.soc["shape"])}
    sources = module_sources(model)
    out.update(sources)
    for text in sources.values():
        for reg in json.loads(text)["registers"]:
            out[reg["svg"]] = render_svg(reg["wavedrom"])
    return out


def oversized_cells(page: str) -> list[str]:
    """A table cell over the limit is prose in disguise: the gate reads no
    table, so the generator holds the cells it writes."""
    problems = []
    for number, line in enumerate(page.splitlines(), start=1):
        if line.startswith("|"):
            for text in re.split(r"(?<!\\)\|", line.strip().strip("|")):
                words = len(check_doc_style.WORD.findall(check_doc_style.normalized_prose(text)))
                if words > MAX_CELL_WORDS:
                    problems.append(f"{PAGE}:{number}: a table cell has {words} words; maximum is {MAX_CELL_WORDS}")
    return problems


CATALOG = "docs/diagrams/README.md"
FINGERPRINT = f"{DIAGRAM_DIR}/rtl_fingerprint.txt"
CATALOG_START = "<!-- register-diagrams:start -->"
CATALOG_END = "<!-- register-diagrams:end -->"


def catalog(model: Model) -> str:
    """The diagram catalog with its generated register-source block."""
    text = read_text(model_root(model), CATALOG)
    if text.count(CATALOG_START) != 1 or text.count(CATALOG_END) != 1:
        raise Refusal(f"{CATALOG} needs exactly one {CATALOG_START} ... {CATALOG_END} block")
    rows = ["| Module source | Module | Registers | Renders |", "|---|---|---|---|"]
    titles = {m.key: strip_md(m.heading).split("  -  ", 1)[-1].split("  (", 1)[0] for m in model.modules}
    for m in model.modules:
        rows.append(f"| [`regmap/{m.key}.json`](regmap/{m.key}.json) | {titles[m.key]} | {len(m.registers)} "
                    f"| `regmap/{m.key}/*.svg` |")
    rows += ["", "| Mechanism | Kind | Section |", "|---|---|---|"]
    for mech in model.mechanisms:
        rows.append(f"| {mech.title} | Mermaid `{mech.kind}` | {titles.get(mech.module, 'Reading this page')} |")
    head, rest = text.split(CATALOG_START, 1)
    _, tail = rest.split(CATALOG_END, 1)
    return head + CATALOG_START + "\n" + "\n".join(rows) + "\n" + CATALOG_END + tail


def model_root(model: Model) -> Path:
    """The tree the model was read from."""
    return model.root


def stale(root: Path, outs: dict[str, str]) -> list[str]:
    """Every generated path whose committed bytes differ, is missing, or
    should not exist."""
    bad = [rel for rel, text in sorted(outs.items())
           if not (root / rel).is_file() or (root / rel).read_text(encoding="utf-8") != text]
    diagram_dir = root / DIAGRAM_DIR
    if diagram_dir.is_dir():
        for path in sorted(diagram_dir.rglob("*")):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and rel not in outs:
                bad.append(f"{rel} (not generated)")
    return bad


def write(root: Path, outs: dict[str, str]) -> None:
    """Write every generated file and remove stale diagrams."""
    diagram_dir = root / DIAGRAM_DIR
    if diagram_dir.is_dir():
        for path in sorted(diagram_dir.rglob("*"), reverse=True):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and rel not in outs:
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()
    for rel, text in outs.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")


def fingerprint(root: Path, shape: str) -> str:
    """The comment-stripped CSR sources' digests. Any code change fails the
    gate here even where the page cannot show it, so a change to behaviour the
    hand-kept prose describes reaches a human; a comment-only edit does not."""
    rels = [RTL]
    rels += sorted(p.relative_to(root).as_posix() for d in (CSR_INCLUDE_DIR, SHAPE_INCLUDE_DIR.format(shape=shape))
                   for p in (root / d / "gen").glob("*.svh"))
    lines = ["# GENERATED by scripts/gen_register_reference.py: sha256 of each comment-stripped CSR source.",
             "# A difference means the RTL changed: regenerate, then reread the prose of the registers it touches."]
    for rel in rels:
        code = " ".join(strip_comments(read_text(root, rel)).split())
        lines.append(f"{hashlib.sha256(code.encode()).hexdigest()}  {rel}")
    text = strip_comments(read_text(root, DATAPATH))
    m = re.search(r"\bmilan_csr\s*#\s*\(", text)
    if not m:
        raise Refusal(f"{DATAPATH} instantiates no milan_csr")
    instance = " ".join(text[m.start():text.index(");", m.start())].split())
    lines.append(f"{hashlib.sha256(instance.encode()).hexdigest()}  {DATAPATH} (the milan_csr instance)")
    return "\n".join(lines) + "\n"


def dump(facts: RtlFacts) -> None:
    """Print the facts read, for a reviewer comparing them with the RTL."""
    for name, off in sorted(facts.addresses.items(), key=lambda kv: (kv[1], kv[0])):
        tags = "W:" + "|".join(b for b, _ in facts.write_arms[name]) if name in facts.write_arms else ""
        print(f"0x{off:03X} {name:20s} {tags}")
    print("params", facts.params)


def dump_fields(facts: RtlFacts) -> None:
    """Print every derived register and its fields."""
    desc = load_json(ROOT, DESCRIPTIONS)
    literal_words = {int(addr, 16): name for addr, name in desc.get("literal_words", {}).items()}
    for reg in Deriver(facts, literal_words).all_registers():
        print(f"0x{reg.offset:03X} {reg.label} x{reg.count} reset={reg.reset} {reg.side_effects} "
              f"{reg.array_resets or ''}")
        for fl in reg.fields:
            print(f"      [{fl.bits:>5}] {fl.name:24s} {fl.access:6s} {fl.reset:10s} {fl.span} {fl.notes}")
        for effect in reg.effects:
            print(f"      effect {effect.target} {effect.action} trigger={effect.trigger}")


def check_soc(root: Path, build: Path) -> list[str]:
    """The committed SoC extract against a fresh extraction of an export."""
    fresh = soc_text(extract_soc(build))
    committed = (root / SOC).read_text(encoding="utf-8") if (root / SOC).is_file() else ""
    return [] if fresh == committed else [f"{SOC} (differs from the export at {build.name})"]


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    """Command-line entry; see the module docstring."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="regenerate the page and the diagrams")
    mode.add_argument("--check", action="store_true", help="fail on any difference from the tree")
    mode.add_argument("--selftest", action="store_true", help="planted stale-page controls")
    mode.add_argument("--dump", action="store_true", help="print the RTL facts read")
    mode.add_argument("--dump-fields", action="store_true", help="print every derived field")
    ap.add_argument("--soc-from", type=Path, help="a builder export directory (csr.csv, aem_desc.json)")
    args = ap.parse_args(argv)
    if args.selftest:
        from register_selftest import selftest
        return selftest(main)
    try:
        soc = None
        if args.soc_from and args.write:
            soc = extract_soc(args.soc_from)
            (root / SOC).write_text(soc_text(soc), encoding="utf-8")
            print(f"wrote {SOC} from {args.soc_from.name}")
        model, facts = build_model(root, soc)
        if args.dump:
            dump(facts)
            return 0
        if args.dump_fields:
            dump_fields(facts)
            return 0
        outs = outputs(model)
    except Refusal as exc:
        print(f"register reference: REFUSED: {exc}")
        return 2
    if args.write:
        write(root, outs)
        print(f"register reference: wrote {PAGE} and {len(outs) - 1} diagram files "
              f"({len(model.registers)} registers, {len(model.modules)} modules)")
        return 0
    bad = stale(root, outs)
    if args.soc_from:
        try:
            bad += check_soc(root, args.soc_from)
        except Refusal as exc:
            print(f"register reference: REFUSED: {exc}")
            return 2
    if bad:
        for rel in bad:
            print(f"STALE {rel}")
        print(f"register reference: STALE ({len(bad)} files); run python3 {Path(__file__).relative_to(ROOT)} --write")
        return 1
    print(f"register reference: fresh ({len(model.registers)} registers, {len(model.modules)} modules, "
          f"{len(outs)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
