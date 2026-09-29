#!/usr/bin/env python3
"""Item 6 inventory: every in-tree MAC/hex declaration and documented example,
graded against the assignment's strict shapes (5880790651 item 6).

Run from the repository root with an interpreter that has PyYAML. Nothing is
written. The shapes, from the assignment text:
  MAC: exactly six two-digit hex octets with one uniform separator, ':' or '-'.
  hex: hex digits with an optional 0x/0X prefix.
The current behaviour column calls the builder's own parsers.
"""
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "sw/builder"))
import endstation_builder as eb  # noqa: E402

MAC = re.compile(r"[0-9A-Fa-f]{2}([:-])[0-9A-Fa-f]{2}(?:\1[0-9A-Fa-f]{2}){4}")
HEX = re.compile(r"(?:0[xX])?[0-9A-Fa-f]+")
#: key path -> shape, for every raw field the builder hands to _mac48,
#: _declared_uint or _eui64 (_model_id, _fmt64, _crf_format, _srp_dmac).
FIELDS = {
    ("platform", "mac_address"): "MAC",
    ("entity", "vendor_oui"): "hex",
    ("entity", "entity_capabilities"): "hex",
    ("entity", "entity_model_id"): "hex",
    ("entity", "model_id_pin"): "hex",
    ("entity", "entity_id"): "hex",
    ("clocking", "crf_format"): "hex",
    ("clocking", "crf_output", "format"): "hex",
    ("srp", "stream_dmac_base"): "hex",
}
SELECTORS = {"hash-derived", "mac-derived", "maap"}


def strict(shape: str, value) -> bool:
    """The assignment's shape for a quoted value."""
    return isinstance(value, str) and bool((MAC if shape == "MAC" else HEX).fullmatch(value))


def current(shape: str, value) -> str:
    """What today's parser does with the value."""
    try:
        if shape == "MAC":
            eb._mac48(value, "probe")
        else:
            eb._eui64(value, "probe")
        return "accepted"
    except eb.ConfigError as exc:
        return f"refused ({exc})"


def walk(raw: dict, source: str, rows: list) -> None:
    """Collect every field value FIELDS names, and every stream formats entry."""
    for path, shape in FIELDS.items():
        node = raw
        for key in path:
            node = node.get(key) if isinstance(node, dict) else None
        if node is not None:
            rows.append((source, ".".join(path), shape, node))
    for direction in ("listeners", "talkers"):
        streams = (raw.get("streams") or {}).get(direction) or raw.get(direction) or []
        for i, stream in enumerate(streams if isinstance(streams, list) else []):
            for j, word in enumerate((stream or {}).get("formats") or []):
                rows.append((source, f"streams.{direction}[{i}].formats[{j}]", "hex", word))


def line_of(path: Path, value: str) -> str:
    """First line of `path` carrying `value`, for the listing."""
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if str(value) in line:
            return f"{path.relative_to(ROOT)}:{n}"
    return str(path.relative_to(ROOT))


class AnyTag(yaml.SafeLoader):
    """SafeLoader that reads an application tag (the barectf trace config) as plain data."""


def _untagged(loader: yaml.SafeLoader, _suffix: str, node: yaml.Node):
    """Construct a tagged node as its untagged kind."""
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node, deep=True)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node, deep=True)
    return loader.construct_scalar(node)


AnyTag.add_multi_constructor("", _untagged)
rows: list = []
tracked = subprocess.run(["git", "ls-files", "*.yaml", "*.yml"], capture_output=True, text=True,
                         check=True).stdout.split()
for name in tracked:
    path = ROOT / name
    before = len(rows)
    for raw in yaml.load_all(path.read_text(), Loader=AnyTag):
        if isinstance(raw, dict):
            walk(raw, name, rows)
            walk(raw.get("overrides") or {}, name + " (overrides)", rows)
    if len(rows) == before:
        print(f"no MAC/hex builder field: {name}")
# Code defaults that reach the same parsers.
rows.append(("sw/builder/endstation_builder.py SRP_DEFAULTS", "srp.stream_dmac_base", "hex",
             eb.SRP_DEFAULTS["stream_dmac_base"]))
rows.append(("sw/builder/endstation_builder.py CRF_FORMAT_DEFAULT", "clocking.crf_format", "hex",
             eb.CRF_FORMAT_DEFAULT))
print()
print("IN-TREE DECLARATIONS")
refused = []
for source, field, shape, value in rows:
    if isinstance(value, str) and value in SELECTORS:
        verdict = "selector (not a hex value)"
    else:
        verdict = "conforms" if strict(shape, value) else "WOULD BE REFUSED"
    where = source if " " in source else line_of(ROOT / source, value)
    print(f"  {where}: {field} = {value!r} [{shape}] -> {verdict}; today {current(shape, value)}")
    if verdict == "WOULD BE REFUSED":
        refused.append((where, field, value))

print()
print("DOCUMENTED EXAMPLES AND RULE STATEMENTS")
# Every backticked value in the two pages that one of the shapes, or the
# lenient rule, could apply to: quoted or bare MAC/hex tokens, and the lines
# stating which spellings are accepted.
token = re.compile(r'`"?([0-9A-Fa-fxX:_\-+ ]{6,})"?`')
statement = re.compile(r"separator|underscore|0x. prefix|spellings", re.I)
for page in ("docs/ENDSTATION_BUILDER.md", "sw/builder/README-parameters.md"):
    for n, line in enumerate((ROOT / page).read_text().splitlines(), 1):
        for match in token.finditer(line):
            text = match.group(0)
            value = match.group(1)
            if not re.search(r"[0-9A-Fa-f]{4}", value):
                continue
            quoted = text.startswith('`"')
            shape = "MAC" if re.search(r"[:\-_]", value) or len(value.replace("0x", "")) == 12 else "hex"
            if not quoted:
                verdict = "bare (a YAML non-string or a prose value; the string rule applies)"
            else:
                verdict = "conforms" if strict(shape, value) or (shape == "MAC" and strict("hex", value)
                                                                 and "mac" not in line.lower()) \
                    else "WOULD BE REFUSED"
            print(f"  {page}:{n}: {text} [{shape}] -> {verdict}")
            if verdict == "WOULD BE REFUSED":
                refused.append((f"{page}:{n}", "documented example", value))
        if statement.search(line) and ("MAC" in line or "Hexadecimal" in line or "hex" in line.lower()):
            print(f"  {page}:{n}: RULE STATEMENT: {line.strip()}")
print()
print(f"WOULD BE REFUSED: {len(refused)}")
for where, field, value in refused:
    print(f"  {where}: {field} {value!r}")
