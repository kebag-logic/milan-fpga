"""Run check_doc_style.analyze on the head page with the proposed residue fixes applied in memory (the tree is not touched)."""
import sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import check_doc_style as c
page = sys.argv[1] + "/docs/design/MARK_II_AREA_PLAN.md"
text = open(page, encoding="utf-8").read()
fixes = [("`ctrl_memory`'s `rom` and `sram` banks hold them until stage 3.",
          "Until stage 3, `ctrl_memory`'s banks hold both regions."),
         ("| LiteDRAM controller and PHY; BIOS ROM and SRAM, 18 RAMB36 measured |",
          "| LiteDRAM controller and PHY; BIOS ROM and SRAM, 18 RAMB36 measured, already gone at the switch-over |")]
before = {(f.line, f.reason) for f in c.analyze(text)}
for old, new in fixes:
    assert text.count(old) == 1, old
    text = text.replace(old, new)
after = {(f.line, f.reason) for f in c.analyze(text)}
print("findings before", len(before), "after", len(after), "new", sorted(after - before))
