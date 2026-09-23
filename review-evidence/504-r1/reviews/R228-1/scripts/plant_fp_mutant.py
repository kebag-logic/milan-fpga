#!/usr/bin/env python3
"""Plant one probe mutant FIRST in gate 1b's mutation table of a SCRATCH copy.

Usage: plant_fp_mutant.py <scratch-copy> <float|double|uint32>
The mutant is the exact shape of the existing resolver-only control
"entity enabled by a struct-overlay store through a paged base", with only
the member type (and a literal whose bit 0 is set) changed. It is pinned on
the same reason (RESOLVER_STORE_PIN). assert_rejected() then either accepts
it (the gate fails naming it), refuses it for another reason (the gate
names that reason), or refuses it on the pin (the gate continues).
Never run against the review clone.
"""

import sys
from pathlib import Path

copy, kind = Path(sys.argv[1]), sys.argv[2]
member, value = {"float": ("volatile float", "1.0000001f"),        # 0x3f800001
                 "double": ("volatile double", "1.0000000000000002"),  # low word bit 0
                 "uint32": ("volatile uint32_t", "1u")}[kind]
path = copy / "sw/builder/test_builder.py"
text = path.read_text()
anchor = "    for mutation in mutations:\n        assert_rejected(*mutation)\n"
assert text.count(anchor) == 1
probe = (
    "    r228_probe = replace_once(\n"
    "        stored_before_aem(\n"
    "            f\"((milan_adp_r228)((csr_page << 16) | {adp_name}))->ctrl = " + value + ";\",\n"
    "            \"R228 " + kind + " struct-overlay store through a paged base\"),\n"
    "        \"static int aem_loaded;\",\n"
    "        \"typedef struct { " + member + " ctrl; } *milan_adp_r228;\\n\"\n"
    "        f\"static unsigned int csr_page = 0x{csr_base >> 16:04x}u;\\n\\n\"\n"
    "        \"static int aem_loaded;\", \"R228 paged " + kind + " overlay typedef\")\n"
    "    print(\"R228 PROBE planted: " + kind + " overlay store, pinned on RESOLVER_STORE_PIN\", flush=True)\n"
    "    assert_rejected(\"R228 PROBE: entity enabled by a " + kind.upper() +
    " struct-overlay store through a paged base\", r228_probe, docs_source, csr_source,\n"
    "                    RESOLVER_STORE_PIN)\n"
    "    print(\"R228 PROBE REFUSED ON THE RESOLVER PIN: " + kind + "\", flush=True)\n"
)
path.write_text(text.replace(anchor, probe + anchor))
print(f"planted {kind} probe into {path}")
