"""Check that clause numbers and table numbers cited on release-facing pages exist in the standard texts."""
import re, sys
from pathlib import Path
root, std = Path(sys.argv[1]), Path(sys.argv[2])
TEXTS = {
    "milan": ["Milan_Specification_Consolidated_v1.2_Final_Approved_20231130.txt"],
    "1722.1": ["1722.1-2021.txt"],
    "1722": ["1722-2016.txt"],
    "802.1AS": ["802.1AS-2011.txt", "802.1AS-2011_Cor1-2013.txt", "802.1AS-2011_Cor_2-2015.txt"],
    "802.1Q": ["8021Q-2022.txt", "802.1Q-2018.txt"],
    "802.1BA": ["802.1BA-2011.txt"],
}
heads, tables = {}, {}
for key, files in TEXTS.items():
    h, t = set(), set()
    for f in files:
        txt = (std / f).read_text(errors="replace")
        h |= set(re.findall(r"(?m)^\s*(\d+(?:\.\d+)+)\.?\s+\S", txt))
        h |= set(re.findall(r"(?m)^\s*(?:Annex\s+)?([A-Z](?:\.\d+)+)\.?\s+\S", txt))
        t |= set(n.replace("\u00ad", "-") for n in re.findall(r"Table\s+([A-Z0-9]+[-.\u00ad]\d+)", txt))
        t |= set(n.replace("\u00ad", "-") for n in re.findall(r"Figure\s+([A-Z0-9]+[-.\u00ad]\d+)", txt))
    heads[key], tables[key] = h, t
STD = r"(?P<std>Milan(?: v?1\.2)?|(?:IEEE )?1722\.1(?:-2021)?|(?:IEEE )?1722(?:-2016)?|(?:IEEE )?802\.1AS(?:-2011)?(?:\s*(?:\+\s*)?Cor\s?[12](?:-20\d\d)?)?|(?:IEEE )?802\.1Q(?:-20\d\d)?|(?:IEEE )?802\.1BA(?:-2011)?)"
CITE = re.compile(STD + r"[,]?\s+(?:Section |section |clause |Clause |§\s?|subclause )?(?P<num>(?:\d+|[A-Z])(?:\.\d+)+)(?![\d.]*\d)")
TAB = re.compile(STD + r"[,]?\s+(?P<kind>Table|Figure)\s+(?P<num>[A-Z0-9]+[-.]\d+)")
def key_of(s):
    s = s.replace("IEEE ", "")
    if s.startswith("Milan"): return "milan"
    if s.startswith("1722.1"): return "1722.1"
    if s.startswith("1722"): return "1722"
    if s.startswith("802.1AS"): return "802.1AS"
    if s.startswith("802.1Q"): return "802.1Q"
    if s.startswith("802.1BA"): return "802.1BA"
pages = [p for p in sys.argv[3:]]
bad = 0; total = 0
for page in pages:
    for n, line in enumerate((root / page).read_text().split("\n"), 1):
        for m in CITE.finditer(line):
            k = key_of(m.group("std")); num = m.group("num").rstrip(".")
            total += 1
            if num not in heads[k]:
                # allow parent of a list item like 10.3.12.1.4 i)
                bad += 1
                print(f"{page}:{n}: {m.group('std')} {num} NOT A HEADING :: {line.strip()[:160]}")
        for m in TAB.finditer(line):
            k = key_of(m.group("std")); num = m.group("num")
            total += 1
            if num not in tables[k]:
                bad += 1
                print(f"{page}:{n}: {m.group('std')} {m.group('kind')} {num} NOT FOUND :: {line.strip()[:160]}")
print(f"checked {total} citations, {bad} unresolved", file=sys.stderr)
