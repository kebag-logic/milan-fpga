#!/usr/bin/env python3
"""Lane B16, round 7: controls of check_b16_figures.py, each on an altered copy (offline, documents only).

usage: r7_check_controls.py <check_b16_figures.py> <findings.md> <packet root> <scratch dir> <out controls.json>

Round 6's r6_check_controls.py: its 39 controls (rounds 3 to 6), their alterations, expectations and code
unchanged; then the round 7 controls (R625-6-F1), from="round 7". R625-6's four comment forms are appended
where R625-6 appended them, to the B16c summary's attribution row: an ordinary comment, the short forms
<!--> and <!--->, and the short form before a unit no list names (furlongs). R625-5's two comment forms,
on one line and over a line break, go where R625-5 put them, on the B16c channels paragraph. A raw tag
splits a number from its unit (7<span></span>ppm), and a comment stands inside a code span, both on the
attribution row. One of the page's former table markers is put back on the blank line it left, and a
generator's marker, one byte off, is appended at the end of the page. Each must fail the check with that
line named MARKUP, and where it adds a digit, that digit named UNCOVERED at the line. Last, the generator's
marker itself, byte for byte, appended the same way, must pass: no MARKUP, nothing named UNCOVERED or
in a row that the unchanged page does not name, the same exit status as the unchanged page (0 at the
head), and the two appended lines read. It compares with the unchanged page, not with exit 0, so its
verdict does not depend on the page's own figures, which state it. With the page at a commit that still holds the former marker, that
control runs on the page as it stands.

The round 6 docstring follows.

Lane B16, round 6: controls of check_b16_figures.py, each on an altered copy (offline, documents only).

Round 5's r5_check_controls.py: its 22 controls (rounds 3 to 5), their alterations, expectations and code
unchanged; then the round 6 controls (R624-5-F1, R624-5-F2, R625-5-F1), from="round 6". On the B16c summary's
attribution row, as the earlier rounds: a descriptor index before each unit R624-5 wrote as a word (per
cent, decibels, hertz, kilohertz, parts per million and per billion, milli-, micro- and nanoseconds, msec,
usec, nsec), R624-5's lane name and clause number before milliseconds, and a descriptor index before a unit
no list names (furlongs). Each must fail the check and be named UNCOVERED at that line, as a measurement, on
standard output. R625-5's comment over a line break is applied where R625-5 applied it, on the B16c channels
paragraph, keeping every line where it is. And B-CRF's window LOCKED count changed to 595 in a copy of its
receipt: the row of lane B6's terms table that states it for both cases must be a MISMATCH naming each case.

The round 5 docstring follows.

Lane B16, round 5: controls of check_b16_figures.py, each on an altered copy (offline, documents only).

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

    # round 6 (R624-5-F2): a unit written as a word, or one no list names, after an identifier
    for i, (name, added, fig) in enumerate((
            ("a descriptor index before per cent", "The residual sat at CLOCK_DOMAIN 7 per cent.", "7"),
            ("a descriptor index before decibels", "The residual sat at CLOCK_DOMAIN 7 decibels.", "7"),
            ("a descriptor index before hertz", "The residual sat at CLOCK_DOMAIN 7 hertz.", "7"),
            ("a descriptor index before kilohertz", "The residual sat at CLOCK_DOMAIN 7 kilohertz.", "7"),
            ("a descriptor index before parts per million", "The residual sat at CLOCK_DOMAIN 7 parts per million.", "7"),
            ("a descriptor index before parts per billion", "The residual sat at CLOCK_DOMAIN 7 parts per billion.", "7"),
            ("a descriptor index before milliseconds", "The residual sat at CLOCK_DOMAIN 7 milliseconds.", "7"),
            ("a descriptor index before microseconds", "The residual sat at CLOCK_DOMAIN 7 microseconds.", "7"),
            ("a descriptor index before nanoseconds", "The residual sat at CLOCK_DOMAIN 7 nanoseconds.", "7"),
            ("a descriptor index before msec", "The residual sat at CLOCK_DOMAIN 7 msec.", "7"),
            ("a descriptor index before usec", "The residual sat at CLOCK_DOMAIN 7 usec.", "7"),
            ("a descriptor index before nsec", "The residual sat at CLOCK_DOMAIN 7 nsec.", "7"),
            ("a lane name before milliseconds", "The lock took B16 milliseconds.", "16"),
            ("a clause number before milliseconds", "The lock took IEEE 1722.1 milliseconds.", "1722.1"),
            ("a descriptor index before a unit no list names", "The residual sat at CLOCK_DOMAIN 7 furlongs.", "7"))):
        slug = f"r6-form-{i}"
        page, line = page_copy(slug, anchor, anchor.replace("Every stage", added + " Every stage"))
        rc, unc, cats, so = run_out(slug, page=page)
        found = any(u[0].endswith(f":{line}") and u[1] == fig for u in unc) and f":{line} {fig} (a measurement" in so
        record(name, f"{added!r} inserted before 'Every stage' on line {line}",
               f"exit 1, {fig} UNCOVERED at that line and named a measurement on standard output", rc, found, "round 6")

    # round 6 (R625-5-F1): R625-5's comment over a line break, where R625-5 put it; no line moves
    old = "The tone sits in channels 0 and 1 of the peer's talker stream. Channels 2 and\n3 carry -1 to 0 LSB"
    new = ("The tone sits in channels 0 and 1 of the peer's talker stream. The residual was CLOCK_DOMAIN 7<!--\n"
           "-->ppm. Channels 2 and 3 carry -1 to 0 LSB")
    page, line = page_copy("r6-comment", old, new)
    rc, unc, cats, so = run_out("r6-comment", page=page)
    found = any(u[0].endswith(f":{line}") and u[1] == "7" for u in unc) and f":{line} 7 (a measurement" in so
    record("a descriptor index before its unit beyond a comment over a line break (R625-5)",
           f"R625-5's multiline form on lines {line} and {line + 1}, 'The residual was CLOCK_DOMAIN 7<!--' and '-->ppm.'",
           "exit 1, 7 UNCOVERED at the first line and named a measurement on standard output", rc, found, "round 6")

    # round 6 (R624-5-F1): one case's count changed in its own receipt; the row for both cases must see it
    pk = SCRATCH / "r6-locked" / "packet"
    if pk.exists():
        shutil.rmtree(pk)
    shutil.copytree(PACKET, pk)
    g = pk / "r2/bcrf-poll-receipt.json"
    d = json.loads(g.read_text())
    w = d["spans"]["window-start..window-end"]
    assert w["servo"] == {"LOCKED": 596}, w["servo"]
    w["servo"] = {"LOCKED": 595, "ACQUIRE": 1}
    g.write_text(json.dumps(d, indent=1))
    rc, bad, unc = run("r6-locked", packet=pk)
    found = any(b[6] == "MISMATCH" and b[5] == "bcrf 595, baaf 596" and "r2/bcrf-poll-receipt.json" in b[3]
                and "r2/baaf-poll-receipt.json" in b[3] for b in bad)
    record("one case's window LOCKED count changed in its own receipt (R624-5-F1)",
           "r2/bcrf-poll-receipt.json window LOCKED 596 to 595 (and ACQUIRE 1)",
           "exit 1, the row stating LOCKED at 596 of 596 for both cases a MISMATCH that names each case's count and "
           "both receipts", rc, found, "round 6")
    shutil.rmtree(pk)

    # round 7 (R625-6-F1): markup is refused by line, in code or not; a generator's marker, byte for byte, passes
    def run_mk(name, page):
        rc, unc, cats, so = run_out(name, page=page)
        mk = [c for c in cats if c[-1] == "MARKUP"]
        return rc, unc, mk, so

    def mark_at(mk, so, line):
        return any(m[0].endswith(f":{line}") for m in mk) and f"MARKUP {PAGE.name}:{line} " in so

    row = "| Attribution | No loss in the network or the DUT | Every stage at the path's floor."
    for i, (name, added) in enumerate((
            ("an ordinary comment between a descriptor index and its unit (R625-6)", " CLOCK_DOMAIN 7<!-- -->ppm."),
            ("the short comment <!--> before a unit (R625-6)", " CLOCK_DOMAIN 7<!-->ppm<!-- -->."),
            ("the short comment <!---> before a unit (R625-6)", " CLOCK_DOMAIN 7<!--->ppm<!-- -->."),
            ("the short comment before a unit no list names (R625-6)", " CLOCK_DOMAIN 7<!-->furlongs<!-- -->."),
            ("a raw tag between a number and its unit", " The residual was 7<span></span>ppm."),
            ("a comment inside a code span", " See `CLOCK_DOMAIN 7<!-- -->ppm`."))):
        slug = f"r7-form-{i}"
        page, line = page_copy(slug, row, row + added)
        rc, unc, mk, so = run_mk(slug, page)
        found = mark_at(mk, so, line) and any(u[0].endswith(f":{line}") and u[1] == "7" for u in unc)
        record(name, f"{added.strip()!r} appended to the attribution row, line {line}",
               "exit 1, the line named MARKUP and 7 UNCOVERED at it", rc, found, "round 7")
    para = "The tone sits in channels 0 and 1 of the peer's talker stream. Channels 2 and\n3 carry -1 to 0 LSB"
    for i, (name, new) in enumerate((
            ("R625-5's comment on one line", "The tone sits in channels 0 and 1 of the peer's talker stream. The "
             "residual was CLOCK_DOMAIN 7<!-- -->ppm. Channels 2 and\n3 carry -1 to 0 LSB"),
            ("R625-5's comment over a line break", "The tone sits in channels 0 and 1 of the peer's talker stream. The "
             "residual was CLOCK_DOMAIN 7<!--\n-->ppm. Channels 2 and 3 carry -1 to 0 LSB"))):
        slug = f"r7-r625-5-{i}"
        page, line = page_copy(slug, para, new)
        rc, unc, mk, so = run_mk(slug, page)
        found = mark_at(mk, so, line) and any(u[0].endswith(f":{line}") and u[1] == "7" for u in unc)
        record(name + ", refused as markup", f"R625-5's form on line {line}, where R625-5 applied it, no line moved",
               "exit 1, the comment's first line named MARKUP and 7 UNCOVERED at it", rc, found, "round 7")
    text = PAGE.read_text(encoding="utf-8")
    old = "McASP0's 300 s at (c), graded by `b9_thdn.py`:\n\n\n| Run | Tone | Blocks |"
    held = "McASP0's 300 s at (c), graded by `b9_thdn.py`:\n\n<!-- b16c-grade -->\n| Run | Tone | Blocks |"
    if old in text:
        page, line = page_copy("r7-marker", old, held)
        line, how = line + 2, "put back on the blank line it left"
    else:
        page, line = page_copy("r7-marker", held, held)
        line, how = line + 2, "as the page at this commit holds it"
    rc, unc, mk, so = run_mk("r7-marker", page)
    record("a former table marker of the page", f"'<!-- b16c-grade -->' on line {line}, {how}",
           "exit 1, the line named MARKUP", rc, mark_at(mk, so, line), "round 7")
    base = run_mk("r7-base", PAGE)
    lines0 = json.loads(base[3].splitlines()[0])["lines"]
    told0 = sorted(x for x in base[3].splitlines()[1:] if not x.startswith("MARKUP "))
    for name, marker, want in (("a generator's marker one byte off", "<!-- solution-cpu-contract:start  -->", 1),
                               ("a generator's marker, byte for byte", "<!-- solution-cpu-contract:start -->", 0)):
        slug = "r7-generated-" + str(want)
        assert text.endswith("\n")
        page, line = page_copy(slug, text, text + "\n" + marker + "\n")
        line = text.count("\n") + 2
        rc, unc, mk, so = run_mk(slug, page)
        read = json.loads(so.splitlines()[0])["lines"] == lines0 + 2
        same = rc == base[0] and sorted(x for x in so.splitlines()[1:] if not x.startswith("MARKUP ")) == told0
        if want:
            record(name, f"{marker!r} appended as the page's last line, line {line}", "exit 1, the line named MARKUP",
                   rc, mark_at(mk, so, line), "round 7")
        else:
            out.append(dict(control=name, alteration=f"{marker!r} appended as the page's last line, line {line}",
                            expect="no MARKUP, nothing named beyond the unchanged page, its exit status, and the two "
                                   "appended lines read (the exception)",
                            observed=dict(rc=rc, unchanged_page_rc=base[0], named=bool(mk), as_unchanged=same,
                                          lines_read=read),
                            verdict="PASS" if not mk and same and read else "FAIL", **{"from": "round 7"}))

    OUT.write_text(json.dumps(dict(note="Lane B16 rounds 3 to 7: controls of check_b16_figures.py on altered copies; "
                                        "offline, no bench action", controls=out), indent=1) + "\n")
    print(json.dumps({c["control"]: c["verdict"] for c in out}))
    return 0 if all(c["verdict"] == "PASS" for c in out) else 1


if __name__ == "__main__":
    sys.exit(main())
