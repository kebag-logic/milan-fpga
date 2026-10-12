#!/usr/bin/env python3
"""Lane B16, round 7: further forms against check_b16_figures.py, each on an altered copy (offline).

usage: r7_self_probes.py <check_b16_figures.py> <findings.md> <packet root> <scratch dir> <out.json>

Round 5's forms (r5_self_probes.py) and round 6's (r6_self_probes.py), read unchanged from those files,
then round 7's: markup of every kind CommonMark knows, written so that it holds no digit, so only the
refusal can catch it (a tag, a closing tag, a tag in capitals, self-closing or with an attribute; a
comment and both short comment forms; a processing instruction, a declaration, a CDATA section; an
autolink; a tag or comment in a code span or in a fenced block; an HTML block; a comment after a
backslash; an unclosed tag; a tag in a link label; a generator's marker inside a line or one byte off);
angle brackets around a link target, which is Markdown, not markup, and fails on its anchor's digits; and
R624-6-S1's forms. Each inserts one sentence before 'Every
stage' on the B16c summary's attribution row ("row"), after 'exponent. ' in round 5's paragraph on the
rule ("para"), replaces one text ("sub"), or appends lines at the end of the page ("end"), inside the
covered text, and runs the check on the copy with the real repository as --repo. A probe is DETECTED when
the check exits 1 and names, on standard output, an UNCOVERED number or a MARKUP line at the line of the
inserted text's first digit or "<".

Some forms pass by the rule as stated (expect "pass"): round 6's stated passes; a generator's marker as
its own line, byte for byte (the exception); an entity-escaped tag, a less-than sign before a space and a
fullwidth one, none of them markup; and R624-6-S1's forms, a word of the closed list followed by words
that hold no number and then a unit, and a list marker before a unit. Round 5's page marker, which round 6
passed inside a dropped comment, is now expected to be detected. A form meets its expectation when it is
DETECTED and expected "detect", or, expected "pass", when the check names nothing at that line and exits as
it does on the unchanged page (0 at the head): a comparison with the unchanged page, not with exit 0, so
the record does not depend on the page's own figures, which state it. Nothing on the bench is read or
written.
"""
import ast
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

CHECK, PAGE, PACKET, SCRATCH, OUT = (Path(a).resolve() for a in sys.argv[1:6])
REPO = PAGE.parents[2]
ROW = "| Attribution | No loss in the network or the DUT | Every stage at the path's floor."
PARA = "exponent. The token pattern is unchanged and now only finds the figures a row"


def forms_of(name):
    """The FORMS list of an earlier round's tool, with the D it builds on: those two assignments only."""
    ns = {}
    body = [n for n in ast.parse(Path(__file__).with_name(name).read_text()).body
            if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) in ("D", "FORMS")]
    exec(compile(ast.Module(body=body, type_ignores=[]), name, "exec"), {}, ns)
    return ns["FORMS"]


D = "The residual sat at CLOCK_DOMAIN 7"
S1 = "R624-6-S1: a word of the closed list, then words that hold no number"
FORMS = [  # (name, inserted text or (old, new), where, expect, why a pass is expected)
    ("an open and a closing tag", "See <b>this</b>.", "row", "detect", ""),
    ("a closing tag alone", "See </b>this.", "row", "detect", ""),
    ("a tag in capitals", "See <SPAN>this</SPAN>.", "row", "detect", ""),
    ("a self-closing tag", "See <br/>this.", "row", "detect", ""),
    ("a tag with an attribute", "See <span title=\"this\">that</span>.", "row", "detect", ""),
    ("a comment", "See <!-- this -->.", "row", "detect", ""),
    ("the short comment <!-->", "See <!-->this.", "row", "detect", ""),
    ("the short comment <!--->", "See <!--->this.", "row", "detect", ""),
    ("a processing instruction", "See <?x this?>.", "row", "detect", ""),
    ("a declaration", "See <!X this>.", "row", "detect", ""),
    ("a CDATA section", "See <![CDATA[this]]>.", "row", "detect", ""),
    ("an autolink", "See <https://example.com/>.", "row", "detect", ""),
    ("a tag in a code span", "See `<b>this</b>`.", "row", "detect", ""),
    ("a comment after a backslash", "See \\<!-- this -->.", "row", "detect", ""),
    ("an unclosed tag", "See <b this.", "row", "detect", ""),
    ("a tag in a link label", "See [<b>this</b>](#b16-round-6-the-closed-list).", "row", "detect", ""),
    ("angle brackets around a link target", "See [this](<#b16-round-6-the-closed-list>).", "row", "detect", ""),
    ("a generator's marker inside a line", "See <!-- solution-cpu-contract:start -->.", "row", "detect", ""),
    ("a tag in a fenced block", "```text\n<b>this</b>\n```", "end", "detect", ""),
    ("an HTML block", "<div>\nthis\n</div>", "end", "detect", ""),
    ("a generator's marker with a space after it", "<!-- solution-cpu-contract:start --> ", "end", "detect", ""),
    ("a generator's marker as its own line", "<!-- solution-cpu-contract:start -->", "end", "pass",
     "a line equal byte for byte to a marker a repository generator writes"),
    ("an entity-escaped tag", "See &lt;b&gt;this&lt;/b&gt;.", "row", "pass", "an entity is not markup"),
    ("a less-than sign before a space", "See a < b.", "row", "pass", "not markup"),
    ("a fullwidth less-than sign", "See ＜b＞this.", "row", "pass", "not markup"),
    ("descriptor index, 'or so', a unit (R624-6-S1)", D + " or so ppm.", "row", "pass", S1),
    ("descriptor index, 'or more', a unit (R624-6-S1)", D + " or more ppm.", "row", "pass", S1),
    ("descriptor index, 'and a half', a unit (R624-6-S1)", D + " and a half ppm.", "row", "pass", S1),
    ("descriptor index, 'to some', a unit (R624-6-S1)", D + " to some ppm.", "row", "pass", S1),
    ("channel index, 'or so', a unit (R624-6-S1)", "The residual sat on channel 1 or so dB.", "row", "pass", S1),
    ("descriptor index, 'of', a unit (R624-6-S1)", D + " of ppm.", "row", "pass", S1),
    ("descriptor index, 'and', a unit (R624-6-S1)", D + " and ppm.", "row", "pass", S1),
    ("a list marker before a unit (R624-6-S1)", "7. ppm", "end", "pass", "a list marker ends with a full stop"),
]


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    text = PAGE.read_text(encoding="utf-8")
    assert text.count(ROW) == 1 and text.count(PARA) == 1 and text.endswith("\n")
    r6 = forms_of("r6_self_probes.py")
    forms = [(n, a, w, "detect", "", "round 5") for n, a, w in forms_of("r5_self_probes.py")]
    forms += [f + ("round 6",) for f in r6] + [f + ("round 7",) for f in FORMS]
    out = []
    d0 = SCRATCH / "unchanged"
    d0.mkdir(parents=True, exist_ok=True)
    rc0 = subprocess.run([sys.executable, "-I", str(CHECK), str(PAGE), str(PACKET), str(d0 / "rows.tsv"), str(d0 / "cov.tsv"),
                          "--repo", str(REPO)], capture_output=True, text=True, timeout=600).returncode
    for i, (name, added, at, expect, why, src) in enumerate(forms):
        d = SCRATCH / f"p{i}" / "docs" / "findings"
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(PAGE.parent / "README.md", d / "README.md")
        if at == "end":
            new, line0 = text + "\n" + added + "\n", text.count("\n") + 2
        else:
            if at == "sub":
                old, new = added
                added = new
            else:
                old = ROW if at == "row" else PARA
                new = old.replace("Every stage", added + " Every stage") if at == "row" else old.replace(
                    "exponent. ", "exponent. " + added + " ")
            assert text.count(old) == 1, old
            line0 = text[:text.index(old)].count("\n") + 1
            new = text.replace(old, new)
        (d / PAGE.name).write_text(new, encoding="utf-8")
        first = re.search(r"\d|zero|seven|½|&#5|<", added)
        line = line0 + (added[:first.start()].count("\n") if first else 0)
        p = subprocess.run([sys.executable, "-I", str(CHECK), str(d / PAGE.name), str(PACKET), str(d / "rows.tsv"),
                            str(d / "cov.tsv"), "--repo", str(REPO)], capture_output=True, text=True, timeout=600)
        named = [x for x in p.stdout.splitlines() if x.split(" ")[0] in ("UNCOVERED", "MARKUP") and f":{line} " in x]
        det = p.returncode == 1 and bool(named)
        out.append(dict(probe=name, **{"from": src}, inserted=added, where=at, line=line, rc=p.returncode, detected=det,
                        markup=any(x.startswith("MARKUP ") for x in named),
                        measurement=any("(a measurement" in x for x in named),
                        named=[x.split(" (")[0] for x in named], expect=expect, why_pass=why,
                        met=det if expect == "detect" else (p.returncode == rc0 and not named)))
        print(f"{'MET ' if out[-1]['met'] else 'NOT '} {expect:6s} {'DETECTED' if det else 'passed  '} {name}")
    OUT.write_text(json.dumps(dict(note="Lane B16 round 7: further forms against the check, each on an altered copy, "
                                        "round 5's and round 6's first; offline, no bench action",
                                   unchanged_page_rc=rc0, detected=sum(x["detected"] for x in out),
                                   expected_pass=sum(x["expect"] == "pass" for x in out),
                                   met=sum(x["met"] for x in out), probes=out), indent=1, ensure_ascii=False) + "\n")
    return 0 if all(x["met"] for x in out) else 1


if __name__ == "__main__":
    sys.exit(main())
