#!/usr/bin/env python3
"""Plant one defect per copy of docs_inventory.py and report whether its own --selftest kills it.

Usage: mutants.py SOURCE.py WORKDIR [--jobs N] [--only PREFIX]. A mutant survives when --selftest exits 0.
Every substitution must match the source exactly `count` times, or the run stops: a stale mutant proves nothing.
"""
import argparse
import concurrent.futures
import pathlib
import subprocess
import sys

WF = '''        for finding, line in entries:
            body += [f"## {finding.ident}: {finding.page}:{line or '?'}", "",
                     f"- Statement: {finding.quote}", f"- Contradicted by: {source_of(finding)}",
                     f"- Correction: {finding.correction}", ""]
'''
M = [
 # --findings-dir completeness (ruling: R787-1-F3 = R788-1 F2)
 ("W01 lane keeps only its first finding", "for finding, line in entries:\n            body +=", "for finding, line in entries[:1]:\n            body +="),
 ("W02 lane drops its first finding", "for finding, line in entries:\n            body +=", "for finding, line in entries[1:]:\n            body +="),
 ("W03 lane keeps only its last finding", "for finding, line in entries:\n            body +=", "for finding, line in entries[-1:]:\n            body +="),
 ("W04 statement dropped", 'f"- Statement: {finding.quote}", ', ''),
 ("W05 source dropped", 'f"- Contradicted by: {source_of(finding)}",', ''),
 ("W06 correction dropped", 'f"- Correction: {finding.correction}", ""]', '""]'),
 ("W07 line replaced by a question mark", "{finding.page}:{line or '?'}", "{finding.page}:?"),
 ("W08 only the first lane written", "for lane, entries in sorted(grouped.items()):", "for lane, entries in sorted(grouped.items())[:1]:"),
 ("W09 only the last lane written", "for lane, entries in sorted(grouped.items()):", "for lane, entries in sorted(grouped.items())[-1:]:"),
 ("W10 every lane overwrites one file", 'slug = re.sub(r"[^a-z0-9]+", "-", lane.lower()).strip("-")', 'slug = "all"'),
 ("W11 every finding filed under one lane", "grouped.setdefault(lanes[finding.page], [])", 'grouped.setdefault("one lane", [])'),
 ("W12 a copy filed under its origin's lane", "grouped.setdefault(lanes[finding.page], [])", "grouped.setdefault(lanes[finding.origin or finding.page], [])"),
 ("W13 lane heading drops the baseline", 'f"Verified against dev `{verified_at}`.",\n', '\n'),
 ("W14 lane heading drops the citation baseline", 'f"Source lines cite dev `{cited_at}`.", ""]', '""]'),
 ("W15 first finding of a lane loses its statement", 'f"- Statement: {finding.quote}", ', 'f"- Statement: {finding.quote if line != entries[0][1] else str()}", '),
 ("W16 copies dropped from the lane files", "for finding, line in located:\n        grouped", "for finding, line in [e for e in located if not e[0].origin]:\n        grouped"),
 ("W17 unlocated findings dropped from the lane files", "for finding, line in located:\n        grouped", "for finding, line in [e for e in located if e[1]]:\n        grouped"),
 # The page's route to a line (ruling: R787-1-F4 = R788-1 F3)
 ("P01 Located sentence dropped", '"`Located` says whether the quote is still on its page.",\n', ''),
 ("P02 command sentence dropped", '"`python3 scripts/docs_inventory.py --findings-dir DIR` writes each finding\'s line, one file per lane.", "",\n', '"",\n'),
 ("P03 search sentence dropped", '"A text search misses a wrapped or marked-up copy.", ', ''),
 ("P04 reach sentence dropped", '"That command still names its line.", "",', '"",'),
 ("P05 command names no script", "`python3 scripts/docs_inventory.py --findings-dir DIR` writes", "`--findings-dir DIR` writes"),
 ("P06 sentence says the page carries the line", "writes each finding's line, one file per lane.", "writes each finding's status, one file per lane."),
 ("P07 reach sentence negated", "That command still names its line.", "That command omits its line."),
 # The page's own row (ruling: R787-1-F2)
 ("O01 own row dropped from the inventory", "    for path, text in texts.items():\n        page_findings", "    for path, text in texts.items():\n        if path == OUTPUT:\n            continue\n        page_findings"),
 ("O02 own row read from disk", '"\\n".join(OWN_HEAD) if path == OUTPUT\n             else (tree.root', '"\\n".join(OWN_HEAD) if path == OUTPUT and not (tree.root / path).is_file()\n             else (tree.root'),
 ("O03 own row hidden at render", 'f"| {p.status} | {cell(p.evidence)} | {p.verified} | {p.lane} |" for p in pages if p.area == area]', 'f"| {p.status} | {cell(p.evidence)} | {p.verified} | {p.lane} |" for p in pages if p.area == area and p.path != OUTPUT]'),
 # Length independence and line numbers on the page
 ("L01 Located shows the line", 'where = "on page" if line else', 'where = str(line) if line else'),
 ("L02 banner evidence names a line", 'f"banner names `{normalise', 'f"banner at line {head[:banner.start()].count(chr(10)) + 1} names `{normalise'),
 ("L03 summary shows a length", 'rows += [f"| {state} | {sum(p.status == state for p in pages)} |" for state in STATUSES]', 'rows += [f"| {state} | {sum(p.status == state for p in pages)} | |" for state in STATUSES]'),
 ("L04 summary counts all pages per status", "sum(p.status == state for p in pages)", "len(pages)"),
 ("L05 located inverted", 'where = "on page" if line else "re-verify: quote not found"', 'where = "re-verify: quote not found" if line else "on page"'),
 ("L06 every row claims on page", 'where = "on page" if line else "re-verify: quote not found"', 'where = "on page"'),
 ("L07 Located heading reverted", "| ID | Page | Located | Statement", "| ID | Page | Where | Statement"),
 # Grading of the committed page
 ("C01 status read from the wrong cell", "states[link.group(1)] = parts[4]", "states[link.group(1)] = parts[3]"),
 ("C02 inventory width stale", 'section == "Inventory" and len(parts) == 8', 'section == "Inventory" and len(parts) == 9'),
 ("C03 check ignores the status rule", "if actual == expected and not broken:", "if actual == expected:"),
 ("C04 status rule lost in the generator", 'if page_findings and state == "current":', "if False:"),
 ("C05 status rule lost and check ignores it", 'if page_findings and state == "current":', "if False:", "if actual == expected and not broken:", "if actual == expected:"),
 # Banner window
 ("B01 window 14", "BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 14"),
 ("B02 window 16", "BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 16"),
 ("B03 window 19", "BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 19"),
 ("B04 window 20", "BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 20"),
 ("B05 window 21", "BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 21"),
 ("B06 window 6", "BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 6"),
 ("B07 window 5", "BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 5"),
 ("B08 whole page scanned", 'head = "\\n".join(text.split("\\n")[:BANNER_SCAN_LINES])', "head = text"),
 # Line naming for copies
 ("N01 copy line off by one", "return bisect_right(flat[1], match.start()) if match else None", "return bisect_right(flat[1], match.start()) + 1 if match else None"),
 ("N02 copy located literally", "carried_line(flatten(text), f.quote) if f.origin else locate(text, f.quote)", "locate(text, f.quote)"),
 ("N03 literal find line off by one", "for number, line in enumerate(text.split(\"\\n\"), start=1):\n        if quote in line:", "for number, line in enumerate(text.split(\"\\n\"), start=2):\n        if quote in line:"),
 # Harness
 ("H01 grader reads the lane text for page needles", 'if text not in (listed if text.startswith("## D0-") else rendered):', "if text not in rendered + listed:"),
 ("H02 grader reads the page for lane needles", 'if text not in (listed if text.startswith("## D0-") else rendered):', "if text not in rendered:"),
 ("H03 grader never fails", 'if text not in (listed if text.startswith("## D0-") else rendered):', "if False:"),
 # R788-1's named survivors, by its published wording
 ("V01 page row loses the recording page", 'f"| {cell(source_of(finding))} | {cell(finding.correction)} |")', 'f"| {cell(finding.source)} | {cell(finding.correction)} |")'),
 ("V02 page drops the verified baseline", 'f"Statements on D0 pages were checked at dev `{verified_at}`."', '"Statements on D0 pages were checked."'),
 ("V03 page correction cell blank", '| {cell(source_of(finding))} | {cell(finding.correction)} |', '| {cell(source_of(finding))} | -- |'),
 ("V04 line count reaches a heading-less purpose", 'return cell(PurePosixPath(path).name)\n', 'return cell(PurePosixPath(path).name) + str(text.count(chr(10)))\n'),
 # Lane files beyond the sampled entry
 ("W18 a copy's lane entry loses its statement", 'f"- Statement: {finding.quote}", ', 'f"- Statement: {str() if finding.origin else finding.quote}", '),
 ("W19 a lane entry loses the recording page", 'f"- Contradicted by: {source_of(finding)}",', 'f"- Contradicted by: {finding.source}",'),
 ("W20 --findings-dir exits nonzero after writing", '        print(f"{directory / (slug + \'.md\')}: {len(entries)} finding(s)")\n    return 0', '        print(f"{directory / (slug + \'.md\')}: {len(entries)} finding(s)")\n    return 1'),
 # Attribution: the old grading with the page-only defect planted on top
 ("X01 old grading plus page row defect", 'if text not in (listed if text.startswith("## D0-") else rendered):', "if text not in rendered + listed:", 'f"| {cell(source_of(finding))} | {cell(finding.correction)} |")', 'f"| {cell(finding.source)} | {cell(finding.correction)} |")'),
 ("X02 new grading plus page row defect", 'f"| {cell(source_of(finding))} | {cell(finding.correction)} |")', 'f"| {cell(finding.source)} | {cell(finding.correction)} |")'),
]


def apply(source, spec):
    text = source
    pairs = spec[1:]
    for old, new in zip(pairs[0::2], pairs[1::2]):
        if text.count(old) != 1:
            raise SystemExit(f"STALE MUTANT {spec[0]}: {text.count(old)} matches for {old[:60]!r}")
        text = text.replace(old, new)
    return text


def run(job):
    index, spec, text, work = job
    folder = work / f"m{index:03d}" / "scripts"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "docs_inventory.py"
    path.write_text(text, encoding="utf-8")
    done = subprocess.run([sys.executable, "-I", str(path), "--selftest"], capture_output=True, text=True, timeout=180)
    fails = [line for line in done.stdout.splitlines() if line.startswith("selftest: FAIL")]
    trace = done.stderr.strip().splitlines()[-1][:90] if done.stderr.strip() else ""
    verdict = "SURVIVED" if done.returncode == 0 else "killed"
    return spec[0], verdict, done.returncode, len(fails), (fails[0][15:110] if fails else trace)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=pathlib.Path)
    parser.add_argument("work", type=pathlib.Path)
    parser.add_argument("--jobs", type=int, default=16)
    parser.add_argument("--only", default="")
    args = parser.parse_args()
    source = args.source.read_text(encoding="utf-8")
    chosen = [spec for spec in M if spec[0].startswith(args.only)]
    jobs = [(n, spec, apply(source, spec), args.work) for n, spec in enumerate(chosen)]
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        rows = list(pool.map(run, jobs))
    for name, verdict, code, fails, first in rows:
        print(f"{verdict:8} rc={code} fails={fails:<3} {name} :: {first}")
    alive = [row[0] for row in rows if row[1] == "SURVIVED"]
    print(f"TOTAL {len(rows)} killed {len(rows) - len(alive)} survived {len(alive)}")


main()
