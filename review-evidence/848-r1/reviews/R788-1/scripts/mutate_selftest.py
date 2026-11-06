#!/usr/bin/env python3
"""Plant one defect at a time in a copy of docs_inventory.py and report whether --selftest kills it.

Usage: mutate_selftest.py HEAD_SCRIPT BASE_SCRIPT WORKDIR
Every mutant is (name, old, new, applies-to-base). A mutant whose `old` text is
absent from a script is reported as n/a for that script, never as killed.
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

M = [
 # --- rendered-page duties the needle widening could hide
 ("page copy row loses its recording page", "| {cell(source_of(finding))} | {cell(finding.correction)} |\")",
  "| {cell(finding.source)} | {cell(finding.correction)} |\")"),
 ("page drops the citations baseline", 'f"Findings cite source lines at dev `{cited_at}` and its submodule pins.", ""]',
  '"Findings cite source lines.", ""]'),
 ("page drops the verified baseline", 'f"Statements on D0 pages were checked at dev `{verified_at}`."', '"Statements on D0 pages were checked."'),
 ("page never says re-verify", 'where = "on page" if line else "re-verify: quote not found"', 'where = "on page"'),
 ("page quote cell blank", '| {where} | {cell(finding.quote)} ', '| {where} | -- '),
 ("page correction cell blank", '| {cell(source_of(finding))} | {cell(finding.correction)} |', '| {cell(source_of(finding))} | -- |'),
 # --- the removed feature coming back
 ("line number back in Located cell", 'where = "on page" if line else', 'where = str(line) if line else'),
 ("line number back in banner evidence", 'return "superseded", f"banner names `', 'return "superseded", f"banner at line {head[:banner.start()].count(chr(10)) + 1} names `'),
 ("per-status byte length back in summary", 'rows += [f"| {state} | {sum(p.status == state for p in pages)} |" for state in STATUSES]',
  'rows += [f"| {state} | {sum(p.status == state for p in pages)} {sum(len(p.path) for p in pages)} |" for state in STATUSES]'),
 ("line count smuggled into evidence", 'return "current", "no recorded contradiction"', 'return "current", f"no recorded contradiction ({text.count(chr(10))})"'),
 ("line count smuggled into purpose", 'return cell(PurePosixPath(path).name)\n', 'return cell(PurePosixPath(path).name) + str(text.count(chr(10)))\n'),
 ("line count smuggled into a titled purpose", 'return cell(re.sub(r"\\[([^\\]]+)\\]\\([^)]*\\)", r"\\1", match.group(1)))',
  'return cell(re.sub(r"\\[([^\\]]+)\\]\\([^)]*\\)", r"\\1", match.group(1))) + str(text.count(chr(10)))'),
 # --- the re-indexed column reader
 ("status gate reads nine columns", 'section == "Inventory" and len(parts) == 8', 'section == "Inventory" and len(parts) == 9'),
 ("status gate reads the wrong status cell", 'states[link.group(1)] = parts[4]', 'states[link.group(1)] = parts[5]'),
 # --- summary counts
 ("status count ignores the status", 'rows += [f"| {state} | {sum(p.status == state for p in pages)} |" for state in STATUSES]',
  'rows += [f"| {state} | {len(pages)} |" for state in STATUSES]'),
 ("total off by one", 'rows.append(f"| **total** | **{len(pages)}** |")', 'rows.append(f"| **total** | **{len(pages) + 1}** |")'),
 # --- findings-dir: the only output naming a line
 ("locate counts from zero", 'enumerate(text.split("\\n"), start=1)', 'enumerate(text.split("\\n"), start=0)'),
 ("carried line off by one", 'return bisect_right(flat[1], match.start()) if match else None', 'return bisect_right(flat[1], match.start()) - 1 if match else None'),
 ("lane file line is always 1", 'body += [f"## {finding.ident}: {finding.page}:{line or \'?\'}", "",', 'body += [f"## {finding.ident}: {finding.page}:{1 if line else \'?\'}", "",'),
 ("lane file hides a lost quote", "{finding.page}:{line or '?'}", "{finding.page}:{line or 0}"),
 ("lane file keeps only its first finding", "for finding, line in entries:\n            body +=", "for finding, line in entries[:1]:\n            body +="),
 ("lane file keeps only its last finding", "for finding, line in entries:\n            body +=", "for finding, line in entries[-1:]:\n            body +="),
 ("lane file drops the statement", 'f"- Statement: {finding.quote}", ', ''),
 ("lane file drops the source", 'f"- Contradicted by: {source_of(finding)}",', ''),
 ("lane file drops the correction", 'f"- Correction: {finding.correction}", ""]', '""]'),
 ("lane file drops copy rows", "for finding, line in located:\n        grouped.setdefault", "for finding, line in [e for e in located if not e[0].origin]:\n        grouped.setdefault"),
 ("findings-dir writes nothing", 'for lane, entries in sorted(grouped.items()):', 'for lane, entries in []:'),
 # --- gate behaviour
 ("check ignores the status rule", 'if actual == expected and not broken:', 'if actual == expected:'),
 ("check never stale", 'if actual == expected and not broken:', 'if not broken:'),
 ("banner scan window is one line", 'BANNER_SCAN_LINES = 15', 'BANNER_SCAN_LINES = 1'),
 ("judged status ignored", 'if path in judged:\n        return judged[path]', 'if False:\n        return judged[path]'),
 ("population ignores a removed page", 'found = sorted({p for p in tree.files if is_document(p) and (tree.root / p).is_file()} | {OUTPUT})',
  'found = sorted({p for p in tree.files if is_document(p)} | {OUTPUT})'),
]


def one(args):
    label, script, work, index, name, old, new = args
    text = Path(script).read_text(encoding="utf-8")
    if old not in text:
        return label, name, "n/a"
    target = Path(work) / f"{label}-{index:02d}.py"
    target.write_text(text.replace(old, new, 1), encoding="utf-8")
    done = subprocess.run([sys.executable, "-I", str(target), "--selftest"], capture_output=True, text=True, timeout=300)
    tail = (done.stdout + done.stderr).strip().splitlines()
    verdict = "SURVIVED" if done.returncode == 0 else "killed"
    return label, name, f"{verdict} rc={done.returncode} :: {tail[0][:150] if tail else ''}"


def main():
    head, base, work = sys.argv[1:4]
    Path(work).mkdir(parents=True, exist_ok=True)
    jobs = [(lab, s, work, i, *m) for lab, s in (("head", head), ("base", base)) for i, m in enumerate(M)]
    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(one, jobs))
    table = {}
    for label, name, verdict in results:
        table.setdefault(name, {})[label] = verdict
    for name, row in table.items():
        print(f"{name}\n   head: {row['head']}\n   base: {row['base']}")
    print("head survivors:", sum(r['head'].startswith('SURVIVED') for r in table.values()),
          "of", sum(r['head'] != 'n/a' for r in table.values()))
    return 0


raise SystemExit(main())
