#!/usr/bin/env python3
"""Disposable mutants of scripts/docs_inventory.py, each graded by its own --selftest.

Usage: python3 -I mutants.py SOURCE_SCRIPT WORK_DIR RECEIPT_TSV [JOBS]

Each mutant is a list of exact (old, new) replacements; a replacement that does not match exactly once
is reported as BADMUTANT, so a mutant can never pass by failing to apply. KILLED = --selftest rc 1 with a named failed control; CRASHED = any other nonzero exit, graded by hand.
"""
import concurrent.futures
import os
import subprocess
import sys
from pathlib import Path

ROW_WHERE = 'where = "on page" if line else "re-verify: quote not found"'
GRADE = 'if text not in (listed if text.startswith(("\\0", "## D0-")) else rendered):'
LANE_HEAD = 'for finding, line in entries:\n            body += [f"## {finding.ident}: {finding.page}:{line or \'?\'}", "",'
OWN = "| {OUTPUT})"
STMT = 'f"- Statement: {finding.quote}", '
SRC = 'f"- Contradicted by: {source_of(finding)}",'
COR = 'f"- Correction: {finding.correction}", ""]'
RULE = 'if page_findings and state == "current":'
S9 = "if actual == expected and not broken:"

MUTANTS = {
    # Identity: the harness itself must leave the unmutated script passing.
    "IDENTITY": [],
    # F1: grading. G0 alone is harmless by itself; the pairs show what it hides.
    "G0_union_grading": [(GRADE, "if text not in (listed + rendered):")],
    "P1_page_drops_copy_source": [('f"| {cell(source_of(finding))} | {cell(finding.correction)} |")',
                                   'f"| {cell(finding.source)} | {cell(finding.correction)} |")')],
    "P1+G0": [('f"| {cell(source_of(finding))} | {cell(finding.correction)} |")',
               'f"| {cell(finding.source)} | {cell(finding.correction)} |")'),
              (GRADE, "if text not in (listed + rendered):")],
    "P2_page_drops_correction": [('f"| {cell(source_of(finding))} | {cell(finding.correction)} |")',
                                  'f"| {cell(source_of(finding))} | -- |")')],
    "P2+G0": [('f"| {cell(source_of(finding))} | {cell(finding.correction)} |")',
               'f"| {cell(source_of(finding))} | -- |")'),
              (GRADE, "if text not in (listed + rendered):")],
    "P3_page_drops_statement": [('| {where} | {cell(finding.quote)} "', '| {where} | -- "')],
    # Located cell and the #848 regressions.
    "P4_always_on_page": [(ROW_WHERE, 'where = "on page"')],
    "P5_always_reverify": [(ROW_WHERE, 'where = "re-verify: quote not found"')],
    "P6_line_number_back": [(ROW_WHERE, 'where = str(line) if line else "re-verify: quote not found"')],
    "P6b_banner_line_back": [('f"banner names `{normalise(', 'f"banner at line {head[:banner.start()].count(chr(10)) + 1} names `{normalise(')],
    "P6c_length_in_evidence": [('state, evidence = status_rule(*status(text, path, judged), page_findings)',
                                'state, evidence = status_rule(*status(text, path, judged), page_findings); evidence += f" {text.count(chr(10))}"')],
    # F2: the page's own row.
    "O1_population_drops_own": [(OWN, ")")],
    "O2_render_hides_own_row": [('for p in pages if p.area == area]', 'for p in pages if p.area == area and p.path != OUTPUT]')],
    "O3_own_row_wrong_title": [('"\\n".join(OWN_HEAD) if path == OUTPUT', '"\\n".join(OWN_HEAD[1:]) if path == OUTPUT')],
    # F3: --findings-dir completeness.
    "W1_first_entry_only": [("for finding, line in entries:\n            body +=", "for finding, line in entries[:1]:\n            body +=")],
    "W2_last_entry_only": [("for finding, line in entries:\n            body +=", "for finding, line in entries[-1:]:\n            body +=")],
    "W3_drop_statement": [(STMT, "")],
    "W4_drop_source": [(SRC, "")],
    "W5_drop_correction": [(COR, '""]')],
    "W6_first_lane_only": [("for lane, entries in sorted(grouped.items()):", "for lane, entries in sorted(grouped.items())[:1]:")],
    "W7_last_lane_only": [("for lane, entries in sorted(grouped.items()):", "for lane, entries in sorted(grouped.items())[-1:]:")],
    "W8_one_file_for_all_lanes": [("grouped.setdefault(lanes[finding.page], [])", 'grouped.setdefault("all", [])')],
    "W9_copy_filed_in_origin_lane": [("grouped.setdefault(lanes[finding.page], [])", "grouped.setdefault(lanes[finding.origin or finding.page], [])")],
    "W10_lines_always_unknown": [("{finding.page}:{line or '?'}", "{finding.page}:?")],
    "W11_line_always_one": [("{finding.page}:{line or '?'}", "{finding.page}:{1 if line else '?'}")],
    "W12_copy_names_origin_page": [("{finding.page}:{line or '?'}", "{finding.origin or finding.page}:{line or '?'}")],
    "W13_lane_copy_loses_copy_note": [(SRC, 'f"- Contradicted by: {finding.source}",')],
    "W14_statement_wrong_field": [(STMT, 'f"- Statement: {finding.correction}", ')],
    "W15_drop_verified_header": [('f"Verified against dev `{verified_at}`.",\n', '\n')],
    "W16_drop_cited_header": [('f"Source lines cite dev `{cited_at}`.", ""]', '""]')],
    "W17_lane_title_loses_lane": [('f"# D0 findings: {lane}"', '"# D0 findings"')],
    "W18_only_located_entries": [("for finding, line in entries:\n            body +=", "for finding, line in [e for e in entries if e[1]]:\n            body +=")],
    "W19_only_recorded_not_copies": [("for finding, line in entries:\n            body +=", "for finding, line in [e for e in entries if not e[0].origin]:\n            body +=")],
    # F4: the route on the page.
    "T1_drop_located_sentence": [('"`Located` says whether the quote is still on its page.",\n', "\n")],
    "T2_drop_command_sentence": [('"`python3 scripts/docs_inventory.py --findings-dir DIR` writes each finding\'s line, one file per lane.", "",', '"",')],
    "T3_drop_search_sentence": [('"A text search misses a wrapped or marked-up copy.", ', "")],
    "T4_drop_route_sentence": [('"That command still names its line.", ', "")],
    "T5_both_route_sentences": [('"A text search misses a wrapped or marked-up copy.", "That command still names its line.", "",', "")],
    # Pinned baselines, status rule, summary.
    "B1_baselines_swapped": [("checked at dev `{verified_at}`", "checked at dev `{cited_at}`"),
                             ("Findings cite source lines at dev `{cited_at}`", "Findings cite source lines at dev `{verified_at}`")],
    "B2_drop_verified": [('f"Statements on D0 pages were checked at dev `{verified_at}`.", ', "")],
    "B3_drop_cited": [('f"Findings cite source lines at dev `{cited_at}` and its submodule pins.", ""]', '""]')],
    "S9_check_ignores_rule": [(S9, "if actual == expected:")],
    "S9b_rule_lost": [(RULE, "if False:")],
    "S9c_rule_lost_and_check_ignores": [(RULE, "if False:"), (S9, "if actual == expected:")],
    "S10_broken_empty": [("broken = current_with_findings(actual)", "broken = []")],
    "S11_status_col_index": [("states[link.group(1)] = parts[4]", "states[link.group(1)] = parts[5]")],
    "S12_inventory_width": [('section == "Inventory" and len(parts) == 8', 'section == "Inventory" and len(parts) == 9')],
    "S13_findings_width": [('section == "Findings" and len(parts) == 6', 'section == "Findings" and len(parts) == 7')],
    "C1_summary_stale_off_by_one": [('rows += [f"| {state} | {sum(p.status == state for p in pages)} |" for state in STATUSES]',
                                     'rows += [f"| {state} | {sum(p.status == state for p in pages) + (state == \'stale\')} |" for state in STATUSES]')],
    "C2_total_off_by_one": [('rows.append(f"| **total** | **{len(pages)}** |")', 'rows.append(f"| **total** | **{len(pages) + 1}** |")')],
    "C3_summary_header_lines_back": [('rows = ["| Status | Pages |", "|---|---:|"]', 'rows = ["| Status | Pages | Lines |", "|---|---:|---:|"]')],
    "H1_heading_less_purpose": [('return cell(PurePosixPath(path).name)', 'return "--"')],
    # R788-1's fourth inherited survivor: a line count reaching a heading-less page's purpose.
    "H2_line_count_in_headless_purpose": [('return cell(PurePosixPath(path).name)', 'return cell(PurePosixPath(path).name) + f" ({text.count(chr(10))} lines)"')],
    # Banner window boundaries: the page says "first 15 lines".
    "N14_window_14": [("BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 14")],
    "N16_window_16": [("BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 16")],
    "N19_window_19": [("BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 19")],
    "N20_window_20": [("BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 20")],
    "N21_window_21": [("BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 21")],
    "N5_window_5": [("BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 5")],
}


def run(job):
    name, edits, source, work = job
    text = source
    for old, new in edits:
        if text.count(old) != 1:
            return name, "BADMUTANT", f"matches={text.count(old)} for {old[:60]!r}"
        text = text.replace(old, new)
    home = work / name.replace("+", "_")
    (home / "scripts").mkdir(parents=True, exist_ok=True)
    (home / "tmp").mkdir(exist_ok=True)
    script = home / "scripts" / "docs_inventory.py"
    script.write_text(text, encoding="utf-8")
    env = dict(os.environ, TMPDIR=str(home / "tmp"))
    done = subprocess.run([sys.executable, "-I", str(script), "--selftest"], capture_output=True, text=True,
                          env=env, cwd=home, timeout=500, check=False)
    lines = (done.stdout + done.stderr).strip().split("\n")
    first = next((l for l in lines if l.startswith("selftest: FAIL")), lines[-1])
    fails = sum(l.startswith("selftest: FAIL") for l in lines)
    verdict = "SURVIVED" if done.returncode == 0 else "KILLED" if fails else "CRASHED"
    return name, verdict, f"rc={done.returncode} fails={fails} {first[:170]}"


def main():
    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    work = Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 16
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        results = list(pool.map(run, [(n, e, source, work) for n, e in MUTANTS.items()]))
    with open(sys.argv[3], "w", encoding="utf-8") as out:
        out.write("mutant\tverdict\tdetail\n")
        for row in results:
            out.write("\t".join(row) + "\n")
    for name, verdict, detail in results:
        print(f"{verdict:10} {name:36} {detail[:120]}")


if __name__ == "__main__":
    main()
