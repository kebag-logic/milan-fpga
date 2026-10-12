#!/usr/bin/env python3
"""Lane B16, round 5: controls of check_b16_figures.py, each on an altered copy (offline, documents only).

usage: r5_check_controls.py <check_b16_figures.py> <findings.md> <packet root> <scratch dir> <out controls.json>

Round 4's r4_check_controls.py: its eight controls (round 3's five and round 4's three), their alterations,
expectations and code unchanged; then the round 5 controls (R624-4-F1, R625-4-F1), from="round 5". Each adds
to the B16c summary's attribution row, the row R625-3 and both round 4 reviews used, a measurement in a form
the token pattern does not read or set off from its unit by more than a single space (a number glued to s, dB
and ms; a leading point, with and without a sign; an exponent; a descriptor index before ppm after a double
space, a non-breaking space and a hyphen). Each must fail the check and be named UNCOVERED at that line, in
the spelling it was written in, and as a measurement on standard output. R625-4's continuation is applied
where it stands, on the B16c channels paragraph: a table row cannot hold a line break. Then round 5's own
bindings: a Unicode minus before a figure a row claims (that row an ERROR, the signed number UNCOVERED), a
cited path that names no packet file and an anchor that names no heading (their digits UNCOVERED), and a
category planted first in a copy of the check that matches every number (live, and the added measurement the
only thing UNCOVERED).

Each control copies what it alters under the scratch directory, alters one thing, runs the check on the
copy with the real repository as --repo, and reads the check's exit status and its rows and coverage
output. A control passes when the check exits 1 and its output names the altered figure as the control
expects. The alterations are found by their text, not by line number, so this file does not depend on the
page's layout. Nothing on the bench is read or written.
"""
import json
import shutil
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

CHECK, PAGE, PACKET, SCRATCH, OUT = (Path(a).resolve() for a in sys.argv[1:6])
REPO = PAGE.parents[2]


def page_copy(name, old, new):
    """The findings page and its README copied, with one text replaced once; returns (page, line number)."""
    d = SCRATCH / name / "docs" / "findings"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(PAGE.parent / "README.md", d / "README.md")
    text = PAGE.read_text(encoding="utf-8")
    assert text.count(old) == 1, old
    line = text[:text.index(old)].count("\n") + 1
    (d / PAGE.name).write_text(text.replace(old, new), encoding="utf-8")
    return d / PAGE.name, line


def run_out(name, page=PAGE, packet=PACKET, check=CHECK):
    """As run, with the check's standard output too (round 4)."""
    rows, cov = SCRATCH / f"{name}-rows.tsv", SCRATCH / f"{name}-coverage.tsv"
    p = subprocess.run([sys.executable, "-I", str(check), str(page), str(packet), str(rows), str(cov), "--repo", str(REPO)],
                       capture_output=True, text=True, timeout=600)
    unc = [x.split("\t") for x in cov.read_text().splitlines()[1:] if x.endswith("\tUNCOVERED")]
    cats = [x.split("\t") for x in cov.read_text().splitlines()[1:] if not x.endswith("\tUNCOVERED")]
    return p.returncode, unc, cats, p.stdout


def run(name, page=PAGE, packet=PACKET, check=CHECK):
    rows, cov = SCRATCH / f"{name}-rows.tsv", SCRATCH / f"{name}-coverage.tsv"
    p = subprocess.run([sys.executable, "-I", str(check), str(page), str(packet), str(rows), str(cov), "--repo", str(REPO)],
                       capture_output=True, text=True, timeout=600)
    bad = [x.split("\t") for x in rows.read_text().splitlines()[1:] if not x.endswith("\tOK")]
    unc = [x.split("\t") for x in cov.read_text().splitlines()[1:] if x.endswith("\tUNCOVERED")]
    return p.returncode, bad, unc


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    out = []

    def record(control, alteration, expect, rc, found, src="round 3"):
        out.append(dict(control=control, alteration=alteration, expect=expect, observed=dict(rc=rc, named=found),
                        verdict="PASS" if rc == 1 and found else "FAIL", **{"from": src}))

    # 1. a figure changed on the page
    old = "| `bcrf` | 9,973 Hz, channel 1 | 300 | 0 | 300 | -123.97 (-123.90) |"
    page, line = page_copy("figure", old, old.replace("-123.97 (-123.90)", "-123.96 (-123.90)"))
    rc, bad, unc = run("figure", page=page)
    found = (any(b[1] == str(line) and b[2] == "-123.97" and b[6].startswith("ERROR") for b in bad)
             and any(u[0].endswith(f":{line}") and u[1] == "-123.96" for u in unc))
    record("a figure changed on the page", f"B-CRF's 9,973 Hz floor median at (c), line {line}: -123.97 to -123.96",
           "exit 1, that row an ERROR (its figure gone from the line) and -123.96 UNCOVERED there", rc, found)

    # 2. a value changed in a receipt
    pk = SCRATCH / "receipt" / "packet"
    if pk.exists():
        shutil.rmtree(pk)
    shutil.copytree(PACKET, pk)
    g = pk / "summary/bcrf/c-b9-grade.json"
    text = g.read_text()
    at = text.index('"thdn_db_median": ', text.index('"ch1_floor"'))
    end = text.index(",", at)
    assert text[at:end].endswith("-123.97"), text[at:end]
    g.write_text(text[:at] + '"thdn_db_median": -123.96' + text[end:])
    assert json.loads(g.read_text(), parse_float=Decimal)["summary"]["ch1_floor"]["thdn_db_median"] == Decimal("-123.96")
    rc, bad, unc = run("receipt", packet=pk)
    found = any(b[3] == "summary/bcrf/c-b9-grade.json" and b[2] == "-123.97" and b[6] == "MISMATCH" for b in bad)
    record("a value changed in a receipt", "summary/bcrf/c-b9-grade.json ch1_floor.thdn_db_median: -123.97 to -123.96",
           "exit 1, a MISMATCH row reading that receipt", rc, found)
    shutil.rmtree(pk)

    # 3. a figure added without a row
    old = "So B-CRF and B-AAF meet three of lane B6's four terms; the timed ratio was not"
    page, line = page_copy("added", old, old + " It held 7 polls.")
    rc, bad, unc = run("added", page=page)
    found = any(u[0].endswith(f":{line}") and u[1] == "7" for u in unc)
    record("a figure added without a row", f"' It held 7 polls.' appended to line {line}",
           "exit 1, the token 7 UNCOVERED at that line", rc, found)

    # 4. a row pointing at the wrong line
    src = CHECK.read_text()
    rows = src[src.index("# ROWS-BEGIN\n") + len("# ROWS-BEGIN\n"):src.index("# ROWS-END")]
    first = next(x for x in rows.splitlines() if x[:1].isdigit())
    ln, rest = first.split("\t", 1)
    moved = f"{int(ln) + 1}\t{rest}"
    chk = SCRATCH / "rowline" / CHECK.name
    chk.parent.mkdir(parents=True, exist_ok=True)
    chk.write_text(src.replace(first + "\n", moved + "\n", 1))
    rc, bad, unc = run("rowline", check=chk)
    found = any(b[0] == "1" and b[1] == str(int(ln) + 1) and b[6].startswith("ERROR") for b in bad)
    record("a row pointing at the wrong line", f"row 1 moved from line {ln} to line {int(ln) + 1}",
           "exit 1, row 1 an ERROR: the figure is not on that line", rc, found)

    # 5. a clock time rounded instead of cut, on the page and in its row
    old = "| PASS | 06:22:29 to 06:22:34 CEST,"
    page, line = page_copy("rounded", old, old.replace("06:22:34", "06:22:35"))
    src = CHECK.read_text()
    row = next(x for x in src.splitlines() if x.startswith(f"{line}\t06:22:34\t"))
    chk = SCRATCH / "rounded" / CHECK.name
    chk.write_text(src.replace(row + "\n", row.replace("\t06:22:34\t", "\t06:22:35\t", 1) + "\n", 1))
    rc, bad, unc = run("rounded", page=page, check=chk)
    found = any(b[1] == str(line) and b[2] == "06:22:35" and b[5] == "06:22:34" and b[6] == "MISMATCH" for b in bad)
    record("a clock time rounded instead of cut", f"lane B16b's identity gate end, line {line}, on the page and in its row: "
           "06:22:34.993 shown as 06:22:35", "exit 1, a MISMATCH row at that line recomputing 06:22:34", rc, found)

    # round 4 (R625-3-F1): R625-3's line, the B16c summary's attribution row, and its figure with a unit
    anchor = "| Attribution | No loss in the network or the DUT | Every stage at the path's floor. See [B16c: attribution](#b16c-attribution) |"
    # Each also adds a figure with no unit in the same form, which the guard does not hold: it fails only
    # because the form is no longer exempt.
    for name, added in (("quoted", 'The measured residual was "7.25 ppm" in "37" blocks. '),
                        ("linked", "The measured residual was [7.25 ppm](#b16c-attribution) in [37](#b16c-attribution) blocks. ")):
        page, line = page_copy(name, anchor, anchor.replace("Every stage", added + "Every stage"))
        rc, unc, cats, so = run_out(name, page=page)
        found = (all(any(u[0].endswith(f":{line}") and u[1] == x for u in unc) for x in ("7.25", "37"))
                 and f":{line} 7.25 (a measurement" in so and f":{line} 37 " in so and f":{line} 37 (a measurement" not in so)
        record(f"a figure with its unit added {'inside a quoted phrase' if name == 'quoted' else 'as a link label'}",
               f"{added.strip()!r} inserted before 'Every stage' on line {line}",
               "exit 1, the tokens 7.25 (a measurement) and 37 (not one) both UNCOVERED at that line and named on "
               "standard output", rc, found, "round 4")

    # round 4: a category planted first that matches every token; a figure with its unit in plain text still fails
    src = CHECK.read_text()
    chk = SCRATCH / "planted" / CHECK.name
    chk.parent.mkdir(parents=True, exist_ok=True)
    chk.write_text(src.replace("# EXCLUDE-BEGIN\n", '# EXCLUDE-BEGIN\nX("planted: every token", r".+")\n', 1))
    page, line = page_copy("planted", anchor, anchor.replace("Every stage", "The measured residual was 7.25 ppm. Every stage"))
    rc, unc, cats, so = run_out("planted", page=page, check=chk)
    live = sum(1 for c in cats if c[2] == "planted: every token")
    found = (live > 0 and any(u[0].endswith(f":{line}") and u[1] == "7.25" for u in unc)
             and f":{line} 7.25 (a measurement: only a row can claim it)" in so)
    record("a category planted that matches every token, and a figure with its unit added in plain text",
           f"X('planted: every token', '.+') first in EXCLUDE; 'The measured residual was 7.25 ppm.' inserted on line {line}",
           "exit 1, the planted category live (it covers other tokens), the token 7.25 UNCOVERED at that line and "
           "named a measurement on standard output", rc, found, "round 4")
    out[-1]["observed"]["planted_category_covered"] = live

    # round 5 (R624-4-F1, R625-4-F1): a measurement the token pattern does not read, or set further from its unit
    for i, (name, added, fig) in enumerate((
            ("a number glued to s", "The residual settled in 26s.", "26"),
            ("a number glued to dB", "The residual sat 10dB above the floor.", "10"),
            ("a number glued to ms", "The probe answered after 300ms.", "300"),
            ("a decimal with a leading point", "The measured residual was .5 ppm.", ".5"),
            ("a decimal with a sign and a leading point", "The measured residual was -.25 ppm.", "-.25"),
            ("a number in exponent form", "The measured residual was 7e2 ppm.", "7e2"),
            ("a descriptor index before its unit after a double space", "The measured residual was CLOCK_DOMAIN 7  ppm.", "7"),
            ("a descriptor index before its unit after a non-breaking space",
             "The measured residual was CLOCK_DOMAIN 7\u00a0ppm.", "7"),
            ("a descriptor index before its unit after a hyphen", "The measured residual was CLOCK_DOMAIN 7-ppm.", "7"))):
        slug = f"r5-form-{i}"
        page, line = page_copy(slug, anchor, anchor.replace("Every stage", added + " Every stage"))
        rc, unc, cats, so = run_out(slug, page=page)
        found = any(u[0].endswith(f":{line}") and u[1] == fig for u in unc) and f":{line} {fig} (a measurement" in so
        record(name, f"{added!r} inserted before 'Every stage' on line {line}",
               f"exit 1, {fig} UNCOVERED at that line and named a measurement on standard output", rc, found, "round 5")

    # round 5 (R625-4-F1): R625-4's unbound continuation, where the continuation stands
    old = "The tone sits in channels 0 and 1 of the peer's talker stream. Channels 2 and"
    page, line = page_copy("r5-continuation", old, old.replace("Channels 2 and", "Channel 2 reports samples:"))
    rc, unc, cats, so = run_out("r5-continuation", page=page)
    found = (any(u[0].endswith(f":{line + 1}") and u[1] == "3" for u in unc) and f":{line + 1} 3 " in so
             and f":{line + 1} 3 (a measurement" not in so)
    record("a channel index on a continuation line, its keyword removed (R625-4)",
           f"'Channels 2 and' on line {line} replaced by 'Channel 2 reports samples:'",
           f"exit 1, the 3 that starts line {line + 1} UNCOVERED and not a measurement", rc, found, "round 5")

    # round 5: a sign the token pattern does not read, before a figure a row claims
    old = "| `bcrf` | 9,973 Hz, channel 1 | 300 | 0 | 300 |"
    page, line = page_copy("r5-minus", old, old.replace("| 300 | 0 |", "| \u2212300 | 0 |"))
    rc, bad, unc = run("r5-minus", page=page)
    found = (any(b[1] == str(line) and b[2] == "300" and b[6].startswith("ERROR") and "longer number \u2212300" in b[6]
                 for b in bad) and any(u[0].endswith(f":{line}") and u[1] == "\u2212300" for u in unc))
    record("a Unicode minus before a figure a row claims", f"B-CRF's 9,973 Hz floor count at (c), line {line}: 300 to "
           "U+2212 300", "exit 1, that row an ERROR (part of a longer number) and the signed number UNCOVERED there",
           rc, found, "round 5")

    # round 5: a cited path that names no packet file, an anchor that names no heading
    for slug, name, added, figs in (
            ("r5-path", "a cited path that names no packet file", "See `runs/pts9/events.jsonl`.", ("9",)),
            ("r5-anchor", "an anchor that names no heading", "See [the round](#b16-round-9).", ("16", "-9"))):
        page, line = page_copy(slug, anchor, anchor.replace("Every stage", added + " Every stage"))
        rc, unc, cats, so = run_out(slug, page=page)
        found = all(any(u[0].endswith(f":{line}") and u[1] == f for u in unc) for f in figs)
        record(name, f"{added!r} inserted before 'Every stage' on line {line}",
               f"exit 1, {' and '.join(figs)} UNCOVERED at that line", rc, found, "round 5")

    # round 5: a category planted first that matches every number; the added measurement is all that fails
    src = CHECK.read_text()
    chk = SCRATCH / "r5-planted" / CHECK.name
    chk.parent.mkdir(parents=True, exist_ok=True)
    chk.write_text(src.replace("# EXCLUDE-BEGIN\n", '# EXCLUDE-BEGIN\nX("planted: every number", r"(?P<t>\\d+(?:\\.\\d+)?)")\n', 1))
    page, line = page_copy("r5-planted", anchor, anchor.replace("Every stage", "The measured residual was 7.25 ppm. Every stage"))
    rc, unc, cats, so = run_out("r5-planted", page=page, check=chk)
    live = sum(1 for c in cats if c[2] == "planted: every number")
    found = (live > 0 and [(u[0].endswith(f":{line}"), u[1]) for u in unc] == [(True, "7.25")]
             and f":{line} 7.25 (a measurement: only a row can claim it)" in so)
    record("a category planted that matches every number, and a figure with its unit added",
           f"X('planted: every number', r'(?P<t>\\d+(?:\\.\\d+)?)') first in EXCLUDE; 'The measured residual was 7.25 ppm.' "
           f"inserted on line {line}", "exit 1, the planted category live, and 7.25, named a measurement, the only "
           "UNCOVERED", rc, found, "round 5")
    out[-1]["observed"]["planted_category_live"] = live > 0

    OUT.write_text(json.dumps(dict(note="Lane B16 rounds 3 to 5: controls of check_b16_figures.py on altered copies; "
                                        "offline, no bench action", controls=out), indent=1) + "\n")
    print(json.dumps({c["control"]: c["verdict"] for c in out}))
    return 0 if all(c["verdict"] == "PASS" for c in out) else 1


if __name__ == "__main__":
    sys.exit(main())
