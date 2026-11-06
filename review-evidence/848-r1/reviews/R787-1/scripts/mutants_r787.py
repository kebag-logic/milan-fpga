#!/usr/bin/env python3
"""Disposable mutation campaign for scripts/docs_inventory.py.

Usage: mutants_r787.py HEAD_SCRIPT BASE_SCRIPT WORKDIR RECEIPT
Each mutant is one exact, unique text replacement. The mutated script's own --selftest decides: nonzero means
killed. A mutant whose target also exists in the base script runs there too, so a survivor at head can be
compared with the base script's controls.
"""
import subprocess, sys, shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROW = 'f"| {p.status} | {cell(p.evidence)} | {p.verified} | {p.lane} |" for p in pages if p.area == area]'
SRC = 'f"| {cell(source_of(finding))} | {cell(finding.correction)} |")'
M = [
 # the removed feature coming back in some form
 ("L1", "Findings cell shows the line number again", 'where = "on page" if line else', 'where = str(line) if line else'),
 ("L2", "banner evidence names a line again", 'return "superseded", f"banner names `', 'return "superseded", f"banner at line {head[:banner.start()].count(chr(10)) + 1} names `'),
 ("L3", "a per-page line count leaks through the evidence cell", 'state, evidence = status_rule(*status(text, path, judged), page_findings)', 'state, evidence = status_rule(*status(text, path, judged), page_findings); evidence += f" ({text.count(chr(10))})"'),
 ("L4", "a per-page byte count leaks through the purpose cell", 'pages.append(Page(path, area_of(path), audience_of(text, path), purpose_of(text, path),', 'pages.append(Page(path, area_of(path), audience_of(text, path), purpose_of(text, path) + f" {len(text)}",'),
 ("L5", "summary total shows a size", 'rows.append(f"| **total** | **{len(pages)}** |")', 'rows.append(f"| **total** | **{len(pages)}** | {sum(len(p.path) for p in pages)} |")'),
 # the Located cell
 ("F1", "Located always says on page", 'where = "on page" if line else "re-verify: quote not found"', 'where = "on page"'),
 ("F2", "Located always says re-verify", 'where = "on page" if line else "re-verify: quote not found"', 'where = "re-verify: quote not found"'),
 # the Findings row and copy rows
 ("R1", "Findings row loses the recording page (source_of bypassed on the page only)", SRC, 'f"| {cell(finding.source)} | {cell(finding.correction)} |")'),
 ("R2", "copy rows dropped from the page", 'for finding, line in located:\n        where', 'for finding, line in [x for x in located if not x[0].origin]:\n        where'),
 # the page's own row
 ("O1", "the page's own inventory row is dropped from the table while still counted", ROW, 'f"| {p.status} | {cell(p.evidence)} | {p.verified} | {p.lane} |" for p in pages if p.area == area and p.path != OUTPUT]'),
 ("O2", "the page is left out of the population", '| {OUTPUT})\n', ')\n'),
 ("O3", "the page's own row reads the file on disk", '"\\n".join(OWN_HEAD) if path == OUTPUT\n             else (tree.root / path)', '(tree.root / path)'),
 ("O4", "the page's own row is rendered from a short header", 'texts = {path: "\\n".join(OWN_HEAD) if path == OUTPUT', 'texts = {path: "" if path == OUTPUT'),
 # the status-rule reader of the committed page
 ("C1", "status-rule reader expects the old 9-cell row", 'if section == "Inventory" and len(parts) == 8:', 'if section == "Inventory" and len(parts) == 9:'),
 ("C2", "status-rule reader reads the wrong cell", 'states[link.group(1)] = parts[4]', 'states[link.group(1)] = parts[5]'),
 ("C3", "status-rule reader ignores the Findings table", 'elif section == "Findings" and len(parts) == 6:', 'elif section == "Findings" and len(parts) == 7:'),
 ("C4", "status-rule reader reads the wrong Findings cell", 'link = ROW_LINK_RE.match(parts[1])', 'link = ROW_LINK_RE.match(parts[2])'),
 # --findings-dir traceability
 ("W1", "--findings-dir prints None for a lost statement", "{finding.page}:{line or '?'}", "{finding.page}:{line}"),
 ("W2", "--findings-dir names no line", "{finding.page}:{line or '?'}", "{finding.page}:?"),
 ("W3", "locate is off by one", 'for number, line in enumerate(text.split("\\n"), start=1):', 'for number, line in enumerate(text.split("\\n"), start=0):'),
 ("W4", "carried_line is off by one", 'return bisect_right(flat[1], match.start()) if match else None', 'return bisect_right(flat[1], match.start()) + 1 if match else None'),
 ("W5", "--findings-dir omits copy rows", 'for finding, line in located:\n        grouped', 'for finding, line in [x for x in located if not x[0].origin]:\n        grouped'),
 ("W6", "--findings-dir keeps only the last finding of a lane", 'grouped.setdefault(lanes[finding.page], []).append((finding, line))', 'grouped[lanes[finding.page]] = [(finding, line)]'),
 ("W7", "--findings-dir keeps only the first finding of a lane", 'grouped.setdefault(lanes[finding.page], []).append((finding, line))', 'grouped.setdefault(lanes[finding.page], [(finding, line)])'),
 ("W8", "--findings-dir omits the statement", 'f"- Statement: {finding.quote}", ', ''),
 ("W9", "--findings-dir writes no files", '(directory / f"{slug}.md").write_text("\\n".join(body), encoding="utf-8")', 'pass'),
 # status, supersession and page set
 ("S1", "a recorded judgement is ignored", 'if path in judged:\n        return judged[path]', 'if False:\n        return judged[path]'),
 ("S2", "a banner is never read", 'banner = BANNER_RE.search(head)', 'banner = None'),
 ("S3", "the status rule is dropped", 'if page_findings and state == "current":', 'if False:'),
 ("S4", "summary counts every page under every status", 'rows += [f"| {state} | {sum(p.status == state for p in pages)} |" for state in STATUSES]', 'rows += [f"| {state} | {len(pages)} |" for state in STATUSES]'),
 ("S5", "the status column is dropped from the summary", 'rows = ["| Status | Pages |", "|---|---:|"]', 'rows = ["| Status | Count |", "|---|---:|"]'),
 ("S6", "banner window grows past the rule", 'BANNER_SCAN_LINES = 15', 'BANNER_SCAN_LINES = 10000'),
 ("S7", "banner window shrinks", 'BANNER_SCAN_LINES = 15', 'BANNER_SCAN_LINES = 3'),
 ("S8", "the gate passes a stale page", 'if actual == expected and not broken:', 'if not broken:'),
 ("S9", "the gate ignores the status rule", 'if actual == expected and not broken:', 'if actual == expected:'),
 ("S10", "untracked pages join the population", 'found = sorted({p for p in tree.files if is_document(p) and (tree.root / p).is_file()} | {OUTPUT})', 'found = sorted({p.relative_to(tree.root).as_posix() for p in tree.root.rglob("*.md") if ".git" not in p.parts} | {p for p in tree.files if is_document(p) and (tree.root / p).is_file()} | {OUTPUT})'),
 ("S11", "a removed page keeps its row", 'found = sorted({p for p in tree.files if is_document(p) and (tree.root / p).is_file()} | {OUTPUT})', 'found = sorted({p for p in tree.files if is_document(p) and ((tree.root / p).is_file() or p.endswith("B.md"))} | {OUTPUT})'),
]

def run(script: Path) -> tuple[int, str]:
    done = subprocess.run([sys.executable, "-I", str(script), "--selftest"], capture_output=True, text=True, timeout=300)
    lines = (done.stdout + done.stderr).strip().splitlines()
    fails = [l for l in lines if l.startswith("selftest: FAIL")]
    return done.returncode, (f"{len(fails)} fail; first: {fails[0][:110]}" if fails else (lines[-1][:110] if lines else ""))

def one(item, src, side, work):
    ident, what, old, new = item
    text = src.read_text(encoding="utf-8")
    if text.count(old) != 1:
        return ident, side, what, None, f"target count {text.count(old)}"
    d = work / side / ident / "scripts"; d.mkdir(parents=True, exist_ok=True)
    (d / "docs_inventory.py").write_text(text.replace(old, new), encoding="utf-8")
    rc, note = run(d / "docs_inventory.py")
    return ident, side, what, rc, note

def main():
    head, base, work, receipt = map(Path, sys.argv[1:5])
    shutil.rmtree(work, ignore_errors=True)
    jobs = [(m, head, "head") for m in M] + [(m, base, "base") for m in M]
    with ThreadPoolExecutor(16) as pool:
        out = list(pool.map(lambda j: one(j[0], j[1], j[2], work), jobs))
    res = {(i, s): (rc, note) for i, s, _, rc, note in out}
    lines = ["# mutant | head result | base result | what | head note"]
    def word(rc): return "n/a" if rc is None else ("killed" if rc != 0 else "SURVIVED")
    for ident, what, *_ in M:
        h, b = res[(ident, "head")], res[(ident, "base")]
        lines.append(f"{ident} | {word(h[0])} | {word(b[0])} | {what} | {h[1]}")
    survivors = [i for i, w, *_ in M if res[(i, 'head')][0] == 0]
    regress = [i for i in survivors if res[(i, 'base')][0] not in (0, None)]
    lines.append(f"# total {len(M)}, head survivors {survivors}, killed at base but surviving at head {regress}")
    Path(receipt).write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

main()
