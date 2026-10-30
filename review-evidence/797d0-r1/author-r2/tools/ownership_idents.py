#!/usr/bin/env python3
"""Check that every `X.name` a PP_DESCRIPTOR_OWNERSHIP row cites exists in the module its source letter names.

Usage: python3 -I ownership_idents.py <tree>

The page's source table maps letters to files (B endstation_builder.py, D
aem_descriptors.py, ...; P the pinned processor packer, read from the
protocol-processor submodule). A name exists when the file defines it as a
function, class or module-level assignment, or names it as an attribute.
"Gate N" references are looked up as `gate N` in sw/builder/test_builder.py.
"""
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1])
MODULES = {"B": "sw/builder/endstation_builder.py", "G": "sw/litex/milan_soc.py", "D": "avdecc/aem_descriptors.py",
           "A": "avdecc/aem_assemble.py", "M": "avdecc/aem_maps.py", "S": "avdecc/aem_specs.py",
           "J": "avdecc/gen_aemi_image.py", "P": "protocol-processor/hdl/aecp/desc/gen_desc_image.py"}
text = {k: (tree / v).read_text(errors="replace") for k, v in MODULES.items()}
tests = (tree / "sw/builder/test_builder.py").read_text(errors="replace")
page = (tree / "docs/reference/PP_DESCRIPTOR_OWNERSHIP.md").read_text().split("\n")
total = bad = 0
for n, line in enumerate(page, 1):
    found = []
    for m in re.finditer(r"`([BGDAMSJP])\.([A-Za-z_][A-Za-z0-9_]*)`", line):
        letter, name = m.groups()
        ok = re.search(r"(?m)^\s*(?:def|class)\s+%s\b|^\s*%s\s*[:=]|\b%s\b" % ((re.escape(name),) * 3), text[letter])
        found.append((f"{letter}.{name}", bool(ok)))
    for m in re.finditer(r"\b[Gg]ate (\d+[a-z]?)\b", line):
        ok = re.search(r"\b[Gg]ate %s\b" % re.escape(m.group(1)), tests)
        found.append((f"gate {m.group(1)}", bool(ok)))
    for m in re.finditer(r"`(test_[a-z0-9_]+)`", line):
        ok = re.search(r"\bdef %s\b" % re.escape(m.group(1)), tests) or any(
            re.search(r"\bdef %s\b" % re.escape(m.group(1)), (tree / f).read_text(errors="replace"))
            for f in ("avdecc/gen_aem_store.py", "scripts/check_entity_shape.py"))
        found.append((m.group(1), bool(ok)))
    if found:
        total += len(found)
        miss = [f for f, ok in found if not ok]
        bad += len(miss)
        print(f"{n}\t{len(found)}\t{'OK' if not miss else 'MISSING ' + ', '.join(miss)}")
print(f"{total} identifiers, {bad} not found")
