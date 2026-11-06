import subprocess, sys
from pathlib import Path
src = Path("scripts/docs_inventory.py").read_text(encoding="utf-8")
muts = {
 "findings cell shows the line": ('where = "on page" if line else', 'where = str(line) if line else'),
 "banner evidence names a line": ('f"banner names `{normalise', 'f"banner at line {head[:banner.start()].count(chr(10)) + 1} names `{normalise'),
 "inventory row counts lines": ('out += [f"| {page_link(p.path)} | {p.audience} |', 'out += [f"| {page_link(p.path)} | {p.audience} {p.purpose and len(open(p.path).read().splitlines()) if False else 0} |'),
 "status reader keeps the old width": ('len(parts) == 8:', 'len(parts) == 9:'),
 "status reader keeps the old index": ('states[link.group(1)] = parts[4]', 'states[link.group(1)] = parts[5]'),
 "copy line off by one": ('return bisect_right(flat[1], match.start()) if match else None', 'return bisect_right(flat[1], match.start()) + 1 if match else None'),
 "locate off by one": ('for number, line in enumerate(text.split("\\n"), start=1):', 'for number, line in enumerate(text.split("\\n"), start=2):'),
 "summary keeps a Lines header": ('rows = ["| Status | Pages |", "|---|---:|"]', 'rows = ["| Status | Pages | Lines |", "|---|---:|"]'),
 "summary total ignores the set": ('rows.append(f"| **total** | **{len(pages)}** |")', 'rows.append("| **total** | **10** |")'),
 "summary counts by status wrong": ('rows += [f"| {state} | {sum(p.status == state for p in pages)} |" for state in STATUSES]', 'rows += [f"| {state} | {len(pages)} |" for state in STATUSES]'),
 "findings-dir omits the line": ("{finding.page}:{line or '?'}", "{finding.page}:{'?'}"),
 "page length reaches the page via purpose": ('return cell(re.sub(r"\\[([^\\]]+)\\]\\([^)]*\\)", r"\\1", match.group(1)))', 'return cell(re.sub(r"\\[([^\\]]+)\\]\\([^)]*\\)", r"\\1", match.group(1))) + " " + str(text.count(chr(10)))'),
 "status ignored by the render": ('f"| {p.status} | {cell(p.evidence)} |', 'f"| current | {cell(p.evidence)} |'),
}
root = Path(sys.argv[1])
HELP = "\n\ndef ROOTLEN(p):\n    return 0\n"
for name, (a, b) in muts.items():
    assert src.count(a) >= 1, name
    (root / "scripts/docs_inventory.py").write_text(src.replace(a, b), encoding="utf-8")
    r = subprocess.run(["python3", str(root / "scripts/docs_inventory.py"), "--selftest"], capture_output=True, text=True, timeout=280)
    fails = [l for l in r.stdout.splitlines() if l.startswith("selftest: FAIL")]
    print(f"{'KILLED' if r.returncode else 'SURVIVED'} rc={r.returncode} fails={len(fails)} :: {name} :: {fails[0][15:90] if fails else r.stderr[-120:]}", flush=True)
