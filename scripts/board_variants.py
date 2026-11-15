#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The deployment guide's board-variant table, read from the sources (#911).

Each row names a board variant, the `build.sh` recipe that builds it, the
programmer part its image set is bound to, the QSPI offset of its entity model
and the flash device the SoC drives. Every value comes from where the build
reads it: `build.sh`'s board facts and recipe, `FLASHBOOT_LAYOUT` and
`FLASHBOOT_BITSTREAM_SLOT` in `sw/litex/milan_soc.py` through
`flash_map.layout_for()`, and the litespi module the SoC instantiates.

usage: board_variants.py [--write | --selftest | --layout RECIPE LAYOUT_JSON]
With no argument the guide's block is checked: 0 agrees, 1 differs.
"""

from __future__ import annotations

import ast
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sw" / "litex"))
from flash_map import layout_for  # noqa: E402

BUILD_SH = Path("sw/litex/build.sh")
SOC = Path("sw/litex/milan_soc.py")
BOARD_DOC = Path("docs/guides/BOARD_DEPLOYMENT.md")
START = "<!-- board-flash-variants:start -->"
END = "<!-- board-flash-variants:end -->"
#: The variants the guide lists: its label for each, and the recipe it is read from.
VARIANTS = (("AX7101", "ax7101"), ("XC7A200T variant", "ax7a200t"))
FACTS = re.compile(r'\s*([a-z0-9|]+)\)\s+echo "\$AX_FTDI\s+\S+\s+(\S+)\s+\S+\s+(\S+)";;')
FLASH_MODULE = re.compile(r'if board == "arty"\s+else (\w+)\(SpiCodes')
DIFFERS = "board flash variant table differs from source"


class Row(NamedTuple):
    """One variant, as the build states it."""

    label: str
    recipe: str
    part: str
    aem_offset: int
    flash_device: str


def _soc_literals(soc_text: str) -> dict[str, object]:
    """The two flash-map literals of the SoC source, parsed, never imported."""
    found = {}
    for node in ast.parse(soc_text).body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in ("FLASHBOOT_LAYOUT", "FLASHBOOT_BITSTREAM_SLOT")):
            found[node.targets[0].id] = ast.literal_eval(node.value)
    if "FLASHBOOT_LAYOUT" not in found:
        raise ValueError(f"{SOC}: no FLASHBOOT_LAYOUT literal")
    return found


def _recipe_facts(build: str, recipe: str) -> tuple[str, str | None]:
    """(programmer part, --fpga-part or None) that build.sh gives `recipe`."""
    part = None
    for line in build.splitlines():
        found = FACTS.match(line)
        if found and recipe in found.group(1).split("|"):
            part = found.group(2)
    if part is None:
        raise ValueError(f"{BUILD_SH}: no board facts for {recipe}")
    body = re.search(rf"^cfg_{recipe}\(\).*?^}}", build, re.M | re.S)
    die = re.search(r'--fpga-part (\S+?)"', body.group(0)) if body else None
    return part, die.group(1) if die else None


def variant_rows(root: Path) -> list[Row]:
    """Every VARIANTS row, each value read from the tree at `root`."""
    build = (root / BUILD_SH).read_text(encoding="utf-8")
    soc_text = (root / SOC).read_text(encoding="utf-8")
    literals = _soc_literals(soc_text)
    module = FLASH_MODULE.search(soc_text)
    if module is None:
        raise ValueError(f"{SOC}: no AX7101 flash module")
    rows = []
    for label, recipe in VARIANTS:
        part, die = _recipe_facts(build, recipe)
        layout = layout_for(literals["FLASHBOOT_LAYOUT"],
                            literals.get("FLASHBOOT_BITSTREAM_SLOT", {}), die)
        rows.append(Row(label, recipe, part, layout["aem"]["offset"], module.group(1)))
    return rows


def variant_table(root: Path) -> str:
    """The guide's block, markers included, as the sources state it."""
    lines = [START,
             "| Board | `build.sh` recipe | Part | Entity model offset | Flash device |",
             "|---|---|---|---|---|"]
    lines += [f"| {r.label} | `{r.recipe}` | `{r.part}` | `0x{r.aem_offset:06x}` | `{r.flash_device}` |"
              for r in variant_rows(root)]
    return "\n".join(lines + [END])


def _block(text: str) -> str:
    """The generated block of the guide, markers included; refused if ambiguous."""
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError(f"{BOARD_DOC}: markers must appear exactly once")
    return START + text.split(START, 1)[1].split(END, 1)[0] + END


def check(root: Path) -> list[str]:
    """Where the guide's table no longer reads what the sources say."""
    try:
        if _block((root / BOARD_DOC).read_text(encoding="utf-8")) != variant_table(root):
            return [f"{BOARD_DOC}: {DIFFERS}"]
    except (OSError, SyntaxError, ValueError) as error:
        return [f"{BOARD_DOC}: board flash variant table unavailable: {error}"]
    return []


def write(root: Path) -> None:
    """Regenerate the guide's block in place from the sources."""
    path = root / BOARD_DOC
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace(_block(text), variant_table(root)), encoding="utf-8")


def layout_errors(root: Path, recipe: str, layout_path: Path) -> list[str]:
    """Where one built flashboot_layout.json disagrees with the guide's row."""
    rows = {r.recipe: r for r in variant_rows(root)}
    if recipe not in rows:
        return [f"no board variant row for recipe {recipe!r}"]
    row = rows[recipe]
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    errors = []
    built = "xc" + str(layout.get("bitstream_fpga_part", "")).lower()
    if built != row.part.lower():
        errors.append(f"{layout_path}: bitstream part {built} != guide {row.part}")
    aem = [i.get("offset") for i in layout.get("images", []) if i.get("name") == "aem"]
    if aem != [row.aem_offset]:
        errors.append(f"{layout_path}: entity model offset {aem} != guide 0x{row.aem_offset:06x}")
    if str(layout.get("flash_device", "")).upper() != row.flash_device.upper():
        errors.append(f"{layout_path}: flash device {layout.get('flash_device')!r} != guide {row.flash_device}")
    return errors


#: (label, file, old text, new text): each must turn the check red with DIFFERS.
MUTATIONS = (
    ("guide variant part", BOARD_DOC,
     "| XC7A200T variant | `ax7a200t` | `xc7a200tfbg484` |",
     "| XC7A200T variant | `ax7a200t` | `xc7a100tfgg484` |"),
    ("variant programmer part", BUILD_SH,
     "ft232    xc7a200tfbg484 boot", "ft232    xc7a100tfgg484 boot"),
    ("variant die", BUILD_SH,
     '--fpga-part xc7a200t-fbg484-2"', '--fpga-part xc7a100t-fgg484-2"'),
    ("variant bitstream slot", SOC,
     '{"xc7a200t-fbg484-2": 0xA0_0000}', '{"xc7a200t-fbg484-2": 0x90_0000}'),
    ("entity model offset", SOC,
     '"aem":       {"offset": 0x40_0000,', '"aem":       {"offset": 0x50_0000,'),
    ("board flash module", SOC,
     "else N25Q128A13(SpiCodes", "else N25Q256A(SpiCodes"),
)


def selftest() -> int:
    """The live tree is clean and every mutation of a copy is caught."""
    if check(ROOT):
        print("board variants selftest: the live tree fails", check(ROOT))
        return 1
    with tempfile.TemporaryDirectory(prefix="board-variants-") as tmp:
        fixture = Path(tmp)
        for relative in (BUILD_SH, SOC, BOARD_DOC):
            (fixture / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, fixture / relative)
        for label, relative, old, new in MUTATIONS:
            path = fixture / relative
            original = path.read_text(encoding="utf-8")
            if original.count(old) != 1:
                print(f"board variants selftest: no single fixture for {label}")
                return 1
            path.write_text(original.replace(old, new), encoding="utf-8")
            found = check(fixture)
            path.write_text(original, encoding="utf-8")
            if not any(DIFFERS in finding for finding in found):
                print(f"board variants selftest: {label} escaped: {found}")
                return 1
    print(f"board variants selftest: OK ({len(MUTATIONS)} mutation controls)")
    return 0


def main(argv: list[str]) -> int:
    """The check by default; --write, --selftest or --layout as asked."""
    if argv == ["--selftest"]:
        return selftest()
    if argv == ["--write"]:
        write(ROOT)
        return 0
    if len(argv) == 3 and argv[0] == "--layout":
        errors = layout_errors(ROOT, argv[1], Path(argv[2]))
        print("\n".join(errors + [f"board flash variant {argv[1]}: {'FAIL' if errors else 'OK'}"]))
        return 1 if errors else 0
    if argv:
        print(__doc__)
        return 2
    errors = check(ROOT)
    print("\n".join(errors) if errors else
          f"board variants: OK ({len(VARIANTS)} rows agree with {BOARD_DOC})")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
