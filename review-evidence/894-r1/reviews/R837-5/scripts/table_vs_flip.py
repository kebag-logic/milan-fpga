"""SPLIT_CONTROL_MEMORY.md's current rows table (THE TIERS: "| 1x1/1if | 900 us |" and "| 8x8/2if | 1,300 us |") and the
summary's "R4 <x> ms ([THE TIERS]" against flip_grade.py --check --point output files, cell for cell.
usage: table_vs_flip.py DOC FLIP_1x1 FLIP_8x8"""
import re, sys
doc = open(sys.argv[1]).read(); bad = 0
for point, slice_, path in (("1x1/1if", "900 us", sys.argv[2]), ("8x8/2if", "1,300 us", sys.argv[3])):
    flip = {m[1]: m[2] for m in re.finditer(rf"^\| {re.escape(point)} \| (\w+) \| ([\d.]+) \|", open(path).read(), re.M)}
    row = re.search(rf"^\| {re.escape(point)} \| {re.escape(slice_)} \| (.*)\|$", doc, re.M)[1].split("|")
    for name, cell in zip(("R4", "R5", "R6", "first", "last"), row):
        t = re.match(r"\s*([\d.]+)", cell)[1]; ok = t == flip[name]; bad += not ok
        print(f"{point} {name}: table {t}, flip {flip[name]}, {'equal' if ok else 'DIFFERENT'}")
s = re.search(r"R4 ([\d.]+) ms \(\[THE TIERS\]", doc)[1]
f = re.search(r"^\| 1x1/1if \| R4 \| ([\d.]+) \|", open(sys.argv[2]).read(), re.M)[1]
bad += s != f; print(f"summary R4 {s}, flip 1x1/1if R4 {f}, {'equal' if s == f else 'DIFFERENT'}")
print(f"RESULT {'PASS' if not bad else 'FAIL'}"); sys.exit(1 if bad else 0)
