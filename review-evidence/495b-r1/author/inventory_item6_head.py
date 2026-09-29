#!/usr/bin/env python3
"""Item 6 inventory at the head: every in-tree MAC/hex declaration and every
quoted documented example, graded by the builder's own parsers.

Run from the repository root with an interpreter that has PyYAML. Nothing is
written. A documented example on a line saying "refuse" must be refused; any
other must be accepted. Exit 1 on any in-tree refusal or documented mismatch.
"""
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "sw/builder"))
import endstation_builder as eb  # noqa: E402

#: key path -> width in bits (0: the MAC rule), for every raw field the
#: builder hands to _mac48, _hex_text, _declared_uint or _eui64.
FIELDS = {
    ("platform", "mac_address"): 0,
    ("entity", "vendor_oui"): 24,
    ("entity", "entity_capabilities"): 32,
    ("entity", "entity_model_id"): 64,
    ("entity", "model_id_pin"): 64,
    ("entity", "entity_id"): 64,
    ("clocking", "crf_format"): 64,
    ("clocking", "crf_output", "format"): 64,
    ("srp", "stream_dmac_base"): 48,
}
SELECTORS = {"hash-derived", "mac-derived", "maap"}


def grade(bits: int, value) -> str:
    """The head parser's verdict for one value."""
    try:
        if bits == 0:
            return f"accepted {eb._mac48(value, 'mac'):012X}"
        return f"accepted {eb._hex_text(value, bits, 'hex', 'hex'):X}"
    except eb.ConfigError as exc:
        return f"REFUSED ({exc})"


class AnyTag(yaml.SafeLoader):
    """SafeLoader that reads an application tag as plain data."""


def _untagged(loader: yaml.SafeLoader, _suffix: str, node: yaml.Node):
    """Construct a tagged node as its untagged kind."""
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node, deep=True)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node, deep=True)
    return loader.construct_scalar(node)


AnyTag.add_multi_constructor("", _untagged)


def walk(raw: dict, source: str, rows: list) -> None:
    """Collect every FIELDS value and every stream formats entry."""
    for path, bits in FIELDS.items():
        node = raw
        for key in path:
            node = node.get(key) if isinstance(node, dict) else None
        if node is not None:
            rows.append((source, ".".join(path), bits, node))
    for direction in ("listeners", "talkers"):
        streams = (raw.get("streams") or {}).get(direction) or raw.get(direction) or []
        for i, stream in enumerate(streams if isinstance(streams, list) else []):
            for j, word in enumerate((stream or {}).get("formats") or []):
                rows.append((source, f"streams.{direction}[{i}].formats[{j}]", 64, word))


rows: list = []
bad = 0
for name in subprocess.run(["git", "ls-files", "*.yaml", "*.yml"], capture_output=True, text=True,
                           check=True).stdout.split():
    before = len(rows)
    for raw in yaml.load_all((ROOT / name).read_text(), Loader=AnyTag):
        if isinstance(raw, dict):
            walk(raw, name, rows)
            walk(raw.get("overrides") or {}, name + " (overrides)", rows)
    if len(rows) == before:
        print(f"no MAC/hex builder field: {name}")
rows.append(("SRP_DEFAULTS", "srp.stream_dmac_base", 48, eb.SRP_DEFAULTS["stream_dmac_base"]))
rows.append(("CRF_FORMAT_DEFAULT", "clocking.crf_format", 64, eb.CRF_FORMAT_DEFAULT))
print("\nIN-TREE DECLARATIONS (head parsers)")
for source, field, bits, value in rows:
    verdict = "selector" if value in SELECTORS else grade(bits, value)
    bad += verdict.startswith("REFUSED")
    print(f"  {source}: {field} = {value!r} [{bits or 'MAC'}] -> {verdict}")

print("\nQUOTED DOCUMENTED EXAMPLES (head parsers)")
quoted = re.compile(r'`"([^"`]+)"`')
for page in ("docs/ENDSTATION_BUILDER.md", "sw/builder/README-parameters.md",
             "docs/reference/PP_DESCRIPTOR_OWNERSHIP.md"):
    for n, line in enumerate((ROOT / page).read_text().splitlines(), 1):
        for value in quoted.findall(line):
            if not re.fullmatch(r"[0-9A-Fa-fxX:_\-+ \t]+", value) or not re.search(r"[0-9A-Fa-f]", value):
                continue
            bits = 0 if "MAC" in line or "octet" in line else 64
            verdict = grade(bits, value)
            want = "REFUSED" if "refuse" in line else "accepted"
            ok = verdict.startswith(want)
            bad += not ok
            print(f"  {'ok ' if ok else 'BAD'} {page}:{n}: \"{value}\" [{bits or 'MAC'}] documented "
                  f"{want.lower()} -> {verdict}")
print(f"\nMISMATCHES: {bad}")
sys.exit(int(bad != 0))
