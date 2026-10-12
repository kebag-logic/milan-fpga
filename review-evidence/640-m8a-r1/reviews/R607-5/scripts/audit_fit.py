#!/usr/bin/env python3
"""Check fresh images, published mappings, document rows and ledger arithmetic."""
import csv, dataclasses, hashlib, json, math, pathlib, re, sys
packet = pathlib.Path(sys.argv[1]).resolve()
root = pathlib.Path.cwd()
sys.path.insert(0, str(root / "sw/litex"))
import ctrl_memory as cm
public = packet / "receipts/public/author-r5/evidence-r5"
doc = (root / "docs/design/SPLIT_CONTROL_MEMORY.md").read_text()
mapping = {r["top"]: r for r in csv.DictReader((public / "map/ctrl_memory_ooc.tsv").open(), delimiter="\t")}
rows = []
for shape, tag in (("1x1_tdm8", "s1"), ("8x8", "s8")):
    for i in (1, 2):
        fresh = json.loads((packet / f"fit-{shape}-if{i}.json").read_text())
        author = json.loads((public / f"fit-head/split-endstation_ax7101_{shape}-if{i}.size.json").read_text())
        for field in ("shape", "interfaces", "srp", "aecp", "sections", "static_storage", "ram_sections", "split"):
            assert fresh[field] == author[field], (shape, i, field)
        assert fresh["artifacts"][2] == author["artifacts"][2], "fresh ELF differs from mapped author's image"
        image = cm.read_elf(packet / "scratch" / f"fit-{shape}-if{i}" / "ctrl_app.elf")
        cm.check_stage(image, 3344 if shape == "1x1_tdm8" else 13264, shape)
        plan = fresh["split"]
        rom, ram = (plan[k]["bytes"] for k in ("rom", "sram"))
        tiles = (math.ceil(rom / 2048) + math.ceil(ram / 2048)) / 2
        assert tiles == plan["tiles"] <= 56
        assert rom + ram <= 224 * 1024
        cols = ("RAMB36E1", "RAMB18E1", "LUT", "FF")
        mapped = [sum(int(mapping[f"{tag}i{i}_{k}"][c]) for k in ("rom", "sram")) for c in cols]
        m36, m18, lut, ff = mapped
        mapped_tiles = m36 + m18 / 2
        assert mapped_tiles <= 56
        expected_cells = [f"{rom:,}", f"{ram:,}", f"{tiles:.1f}", f"{m36} / {m18}", f"{mapped_tiles:.1f}", f"{lut} / {ff}"]
        assert " | ".join(expected_cells) in doc, expected_cells
        slack = 56 * 4096 - rom - ram
        rows.append({"shape":shape,"interfaces":i,"rom_bytes":rom,"sram_bytes":ram,
                     "planned_tiles":tiles,"mapped_tiles":mapped_tiles,
                     "mapped_primitives":mapped,"capacity_minus_used_bytes":slack,
                     "elf_sha256":fresh["artifacts"][2]["sha256"]})
        print(json.dumps(rows[-1]))
        # Grow only the final stack reservation to hit the exact planner boundary.
        stack = next(s for s in image.sections if s.name == ".stack")
        banked_ram = sum(plan["sram"]["banks"])
        room = int((56 - tiles) * 4096)
        grow = banked_ram - ram + room
        full = dataclasses.replace(image, sections=tuple(dataclasses.replace(s, size=s.size + grow) if s is stack else s for s in image.sections))
        assert cm.plan(full).tiles == 56
        over = dataclasses.replace(full, sections=tuple(dataclasses.replace(s, size=s.size + 2048) if s.name == ".stack" else s for s in full.sections))
        try:
            cm.plan(over)
        except cm.Refusal as exc:
            assert exc.rule == "budget"
        else:
            raise AssertionError("56.5 tiles were accepted")
        print(shape, i, "PASS real-image 56.0 accepted / 56.5 refused; correct staging size")
assert rows[-1]["capacity_minus_used_bytes"] == 5064
for name in ("MARK_II_AREA_PLAN.md", "AREA_BUDGET.md"):
    text = (root / "docs/design" / name).read_text()
    table = text.split("| Item | RAMB36 delta | RAMB18 delta | Tile delta | Image tiles after |", 1)[1].split("\n\n", 1)[0]
    total = 0
    for line in table.splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 5 or cells[0].startswith("---"):
            continue
        a, b, delta, expected = map(float, cells[1:])
        assert a + b / 2 == delta, line
        total += delta
        assert total == expected, line
    assert total == 114
    assert all(v in text for v in ("125", "114", "7.5", "6.5", "131", "9.5", "13.5"))
    print(name, "PASS ledger primitive arithmetic, total 114, headroom 7.5; reserve 13.5 separate")
assert 87.5-6.5+6-18+54+2 == 125
assert 125-11 == 114 and 121.5-114 == 7.5
assert 125+1-11 == 115 and 121.5-115 == 6.5
assert 125+6 == 131 and 131-121.5 == 9.5
assert 125+2-11 == 116 and 121.5-116 == 5.5
assert "`ce10328c`, on dev `ac2c5e77`" in doc and "`8ab2b539`" in doc
(packet / "receipts/independent-fit.json").write_text(json.dumps(rows, indent=2) + "\n")
print("PASS four exact-image reproductions, mapped sums, document rows, source attribution and independent budget boundaries")
