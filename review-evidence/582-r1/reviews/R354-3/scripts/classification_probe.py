#!/usr/bin/env python3
"""R354-3 classification probe for docs/testing/CI_WORKFLOWS.md.

Usage: python3 classification_probe.py <repo-root>

Checks, against scripts/ci_scope.py at the checked-out head:
  A. the pages the policy paragraph calls relevant equal GATE_READ_DOCS, and
     each is classified relevant (is_doc_only_path is False);
  B. every page named by a row of the "stay documentation only" table is
     classified documentation only, and the row's reader is outside the scan
     (in DOCS_JOB_PY or outside GATED_ROOTS);
  C. the tap page's reader is inside the scan and absent from DOCS_JOB_PY,
     which is the clause the page gives for its relevance;
  D. the tap page's reader is run by docs-check through the builder bank
     (docs.yml runs test_builder.py, whose __main__ imports test_tap_clock_docs).
Exit 0 only if every check holds.
"""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
import ci_scope as cs  # noqa: E402

failures = []


def check(ok, label):
    print(("ok   " if ok else "FAIL ") + label)
    if not ok:
        failures.append(label)


page = (root / "docs/testing/CI_WORKFLOWS.md").read_text()
# Anchored on the table header, not on prose wording, so an edited
# introduction is judged on content rather than failing to parse.
header = "| Reader | Skipped job that runs it |"
assert page.count(header) == 1, "reader table header not found exactly once"
para = page.split("pages under `docs/` are relevant because", 1)[1].split(header, 1)[0]
table = header + page.split(header, 1)[1].split("The derivation is a net", 1)[0]

# A. relevant pages named in the paragraph (links resolved against docs/testing/).
base = root / "docs/testing"
named = set()
for target in re.findall(r"\]\(([^)]+\.md)\)", para):
    named.add((base / target).resolve().relative_to(root).as_posix())
count_word = page.split(" pages under `docs/` are relevant because", 1)[0].rsplit("\n", 1)[-1].strip()
check(named == set(cs.GATE_READ_DOCS), f"A1 paragraph pages {sorted(named)} == GATE_READ_DOCS")
words = {"Three": 3, "Four": 4, "Five": 5}
check(words.get(count_word) == len(cs.GATE_READ_DOCS),
      f"A2 paragraph count word '{count_word}' == {len(cs.GATE_READ_DOCS)}")
for p in sorted(cs.GATE_READ_DOCS):
    check(cs.is_doc_only_path(p) is False, f"A3 {p} classified relevant")

# B. rows of the documentation-only table.
rows = [r for r in table.splitlines() if r.startswith("| `")]
check(len(rows) == 3, f"B0 table has {len(rows)} reader rows (expected 3)")
check("AAF_LATENCY_TAPS" not in table, "B1 tap page is not a row of the documentation-only table")
builder_pages = sorted(set(re.findall(r"docs/[A-Za-z0-9_./-]+\.md",
                                      (root / "sw/builder/test_builder.py").read_text())))
row_pages = {
    "sw/builder/test_builder.py": [p for p in builder_pages if p not in cs.GATE_READ_DOCS],
    "docs/traceability/gen_module_matrix.py": sorted(
        p.relative_to(root).as_posix() for p in (root / "docs/traceability").glob("*.md")),
    "scripts/ci_events.py": ["docs/testing/CI_WORKFLOWS.md"],
}
for row in rows:
    reader = re.match(r"\| `([^`]+?)(?: --check)?`", row).group(1)
    check(reader in row_pages, f"B2 row reader {reader} known to the probe")
    outside = reader in cs.DOCS_JOB_PY or not reader.startswith(tuple(r + "/" for r in cs.GATED_ROOTS))
    check(outside, f"B3 row reader {reader} is outside the scan (DOCS_JOB_PY or outside GATED_ROOTS)")
    for p in row_pages.get(reader, []):
        check(cs.is_doc_only_path(p) is True, f"B4 {reader}: {p} classified documentation only")

# C. the tap page's stated reason.
tap_reader = "sw/builder/test_clock_contract.py"
check(tap_reader not in cs.DOCS_JOB_PY, "C1 tap reader absent from DOCS_JOB_PY")
check(tap_reader in cs.gated_files(root), "C2 tap reader is a scanned gated file")
check("docs/AAF_LATENCY_TAPS.md" in (root / tap_reader).read_text(), "C3 tap reader names the tap page")

# D. docs-check reaches the tap reader through the builder bank.
docs_yml = (root / ".github/workflows/docs.yml").read_text()
tb_main = (root / "sw/builder/test_builder.py").read_text().split('if __name__ == "__main__":', 1)[1]
check("sw/builder/test_builder.py" in docs_yml, "D1 docs.yml runs the builder bank")
check("test_tap_clock_docs" in tb_main, "D2 builder bank __main__ runs test_tap_clock_docs")

print("PROBE", "PASS" if not failures else f"FAIL ({len(failures)})")
sys.exit(1 if failures else 0)
