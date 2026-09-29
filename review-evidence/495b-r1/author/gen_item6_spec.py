#!/usr/bin/env python3
"""Write mutants/item6.json: item 6's before-state and mutants for mutate.py.

The anchors are the exact source text at the item 6 commit, so a stale anchor
stops mutate.py by name instead of running an unmutated check.
"""
import json
from pathlib import Path

PY = "$VALIDATION_STORAGE/a433/pins-venv/bin/python3"
B = "sw/builder/endstation_builder.py"
NAMED = [PY, "-c", "import test_declarations as t; t.test_mac_shape_contract(); t.test_hex_shape_contract()"]
PINS = [PY, "-c", "import test_declarations as t; t.test_station_mac_string_contract(); "
        "t.test_declared_hex_string_contract(); t.test_hex_scalar_contract(); t.test_formats_list_contract()"]
GATE25B = [PY, "-c", "import test_builder as t; t.test_schema_12_refusals()"]
HEX = r'HEX_TEXT = re.compile(r"(?:0[xX])?([0-9A-Fa-f](?:_?[0-9A-Fa-f])*)")'
OCT = r'MAC_OCTETS = re.compile(r"[0-9A-Fa-f]{2}([:-])[0-9A-Fa-f]{2}(?:\1[0-9A-Fa-f]{2}){4}")'
OLD_EUI = '''    return _hex_text(v, EUI64_MAX.bit_length(), ctx, "a hex EUI-64")'''
OLD_UINT = '''    return _hex_text(v, bits, ctx, "a hex integer")'''
LENIENT = '''    try:
        n = int(v, 16)
    except ValueError:
        raise ConfigError(f"{ctx}: {v!r} is not a hex integer") from None
    if not 0 <= n < 1 << {bits}:
        raise ConfigError(f"{ctx}: {v!r} is outside {bits} bits")
    return n'''


def edit(old: str, new: str, count: int = 1) -> dict:
    """One in-place replacement in the builder."""
    return {"path": B, "old": old, "new": new, "count": count}


mutants = [
    {"name": "control named tests", "expect": "pass", "edits": []},
    {"name": "control 595 pins", "expect": "pass", "check": PINS, "edits": []},
    {"name": "control gate 25b", "expect": "pass", "check": GATE25B, "edits": []},
    {"name": "BEFORE builder at 51ca45c7 (named tests)", "edits": [{"path": B, "base": "51ca45c7"}]},
    {"name": "BEFORE builder at 51ca45c7 (595 pins, new zero/width refusals)", "check": PINS,
     "edits": [{"path": B, "base": "51ca45c7"}]},
    {"name": "BEFORE builder at 51ca45c7 (gate 25b sign row)", "check": GATE25B,
     "edits": [{"path": B, "base": "51ca45c7"}]},
    {"name": "M6a sign accepted by HEX_TEXT",
     "edits": [edit(HEX, HEX.replace('r"(?:0[xX])?', 'r"[+-]?(?:0[xX])?'))]},
    {"name": "M6b hex whitespace stripped",
     "edits": [edit("    match = HEX_TEXT.fullmatch(v)\n", "    match = HEX_TEXT.fullmatch(v.strip())\n")]},
    {"name": "M6c MAC whitespace stripped",
     "edits": [edit("    octets = MAC_OCTETS.fullmatch(v)\n    text = HEX_TEXT.fullmatch(v)\n",
                    "    v = v.strip()\n    octets = MAC_OCTETS.fullmatch(v)\n    text = HEX_TEXT.fullmatch(v)\n")]},
    {"name": "M6d any underscores in HEX_TEXT",
     "edits": [edit(HEX, 'HEX_TEXT = re.compile(r"(?:0[xX])?_*([0-9A-Fa-f][0-9A-Fa-f_]*)")')]},
    {"name": "M6e \\d for 0-9 in HEX_TEXT (Unicode digits)",
     "edits": [edit(HEX, HEX.replace("0-9A-Fa-f", r"\dA-Fa-f"))]},
    {"name": "M6f value width instead of digit count",
     "edits": [edit("    if len(digits) > bits // 4:\n", "    if int(digits, 16) >> bits:\n")]},
    {"name": "M6g MAC fewer than twelve digits accepted",
     "edits": [edit("    if len(digits) != MAC48_MAX.bit_length() // 4:\n",
                    "    if not 0 < len(digits) <= MAC48_MAX.bit_length() // 4:\n")]},
    {"name": "M6h MAC more than twelve digits accepted",
     "edits": [edit("    if len(digits) != MAC48_MAX.bit_length() // 4:\n",
                    "    if len(digits) < MAC48_MAX.bit_length() // 4:\n")]},
    {"name": "M6i MAC unpadded octets (separators deleted, twelve digits counted)",
     "edits": [edit(OCT, 'MAC_OCTETS = re.compile(r"[0-9A-Fa-f]{1,3}([:-])(?:[0-9A-Fa-f]{1,3}\\1){4}[0-9A-Fa-f]{1,3}")')]},
    {"name": "M6j MAC mixed separators (either separator deleted)",
     "edits": [edit(OCT, OCT.replace(r"(?:\1", "(?:[:-]")),
               edit("        digits = v.replace(octets[1], \"\")\n",
                    "        digits = re.sub(\"[:-]\", \"\", v)\n")]},
    {"name": "M6k MAC underscores deleted before the octet match",
     "edits": [edit("    octets = MAC_OCTETS.fullmatch(v)\n", "    octets = MAC_OCTETS.fullmatch(v.replace(\"_\", \"\"))\n"),
               edit("        digits = v.replace(octets[1], \"\")\n",
                    "        digits = v.replace(octets[1], \"\").replace(\"_\", \"\")\n")]},
    {"name": "M6l MAC 0x prefix allowed on octets",
     "edits": [edit("    octets = MAC_OCTETS.fullmatch(v)\n", "    octets = MAC_OCTETS.fullmatch(v.removeprefix(\"0x\"))\n"),
               edit("        digits = v.replace(octets[1], \"\")\n",
                    "        digits = v.removeprefix(\"0x\").replace(octets[1], \"\")\n")]},
    {"name": "M6m stream DMAC parsed 64 bits wide",
     "edits": [edit("    dmac = _hex_text(s[\"stream_dmac_base\"], MAC48_MAX.bit_length(),",
                    "    dmac = _hex_text(s[\"stream_dmac_base\"], EUI64_MAX.bit_length(),")]},
    {"name": "M6n all-zero MAC accepted", "check": PINS,
     "edits": [edit("    if not n:\n        raise ConfigError(f\"{ctx}: {v!r} is the all-zero MAC-48\")\n", "")]},
    {"name": "M6o 0X prefix refused",
     "edits": [edit(HEX, HEX.replace("0[xX]", "0x"))]},
    {"name": "M6p _eui64 bypasses HEX_TEXT (lenient int)",
     "edits": [edit(OLD_EUI, "    if not isinstance(v, str):\n        raise ConfigError(f\"{ctx}: quote the hexadecimal value "
                             "as a YAML string\")\n" + LENIENT.replace("{bits}", "64", 1).replace("{bits} bits", "64 bits"))]},
    {"name": "M6q _declared_uint bypasses HEX_TEXT (lenient int)",
     "edits": [edit(OLD_UINT, "    if not isinstance(v, str):\n        raise ConfigError(f\"{ctx}: quote the hexadecimal value "
                              "as a YAML string\")\n" + LENIENT.replace("<< {bits}", "<< bits"))]},
]
spec = {"check": NAMED, "cwd": "sw/builder", "timeout": 900, "mutants": mutants}
Path(__file__).with_name("mutants").joinpath("item6.json").write_text(json.dumps(spec, indent=1) + "\n")
print(f"{len(mutants)} entries")
