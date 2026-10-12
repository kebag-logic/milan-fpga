#!/usr/bin/env python3
"""Lane B16, round 8: further forms against check_b16_figures.py, each on an altered copy (offline).

usage: <parser python> r8_self_probes.py <check_b16_figures.py> <findings.md> <packet root> <scratch dir> <out.json>

Round 5's, round 6's and round 7's forms, read unchanged from r5_self_probes.py, r6_self_probes.py and
r7_self_probes.py beside this file, then round 8's. Five of round 7's forms are now expected to pass, each
with its reason in RULED: the check reads what the pinned parser yields, and there each is text or a link,
not markup. Round 8's forms put Markdown that renders no character, or a figure inside a construct off the
allowlist, where a reader would see a measurement, and state the forms that render nothing a reader sees.

A form is inserted before 'Every stage' on the B16c summary's attribution row ("row"), after 'exponent. ' in
round 5's paragraph on the rule ("para"), replaces one text ("sub"), or is appended after the page's last
line ("end"), inside the covered text; the check runs on the copy with the real repository as --repo. A
form is DETECTED when the check exits 1 and names, on standard output, an UNCOVERED number or a MARKUP
construct at a line the inserted text occupies. A form expected to pass meets its expectation when the check
names nothing at those lines and exits as it does on the unchanged page. Nothing on the bench is read or
written.
"""
import ast
import json
import shutil
import subprocess
import sys
from pathlib import Path

CHECK, PAGE, PACKET, SCRATCH, OUT = (Path(a).resolve() for a in sys.argv[1:6])
REPO = PAGE.parents[2]
ROW = "| Attribution | No loss in the network or the DUT | Every stage at the path's floor."
PARA = "exponent. The token pattern is unchanged and now only finds the figures a row"


def forms_of(name):
    """The FORMS list of an earlier round's tool, with what it builds on: its D and S1 assignments only."""
    ns = {}
    body = [n for n in ast.parse(Path(__file__).with_name(name).read_text()).body
            if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) in ("D", "S1", "FORMS")]
    exec(compile(ast.Module(body=body, type_ignores=[]), name, "exec"), {}, ns)
    return ns["FORMS"]


RULED = {  # round 7's forms the parser reads as text or a link: expected to pass, and why
    "an autolink": "a link, read on its text, which holds no digit",
    "a tag in a code span": "code is text a reader sees: the tag is shown as written",
    "a comment after a backslash": "the backslash makes the comment text, shown as written",
    "an unclosed tag": "not a tag: the parser yields it as text",
    "angle brackets around a link target": "a target that resolves is not read",
}
D = "The residual sat at CLOCK_DOMAIN 7"
FORMS = [  # (name, inserted text or (old, new), where, expect, why a pass is expected)
    ("an image between a descriptor index and its unit", D + "![](x.png) ppm.", "row", "detect", ""),
    ("an image described by a full stop", D + "![.](x.png) ppm.", "row", "detect", ""),
    ("an empty link between a number and its unit", D + "[](#b16c-attribution) ppm.", "row", "detect", ""),
    ("an empty link titled with a word of the closed list", D + '[](#b16c-attribution "and") ppm.', "row", "detect", ""),
    ("a figure as a link's text before a unit", "The residual was [7](#b16c-attribution) ppm.", "row", "detect", ""),
    ("strong emphasis on the unit", D + "**ppm**.", "row", "detect", ""),
    ("an entity for a space", D + "&#32;ppm.", "row", "detect", ""),
    ("an entity for a soft hyphen", D + "&shy;ppm.", "row", "detect", ""),
    ("an autolink holding a figure before a unit", "See https://example.com/7 ppm.", "row", "detect", ""),
    ("an autolink in angle brackets holding a digit", "See <https://example.com/7>.", "row", "detect", ""),
    ("a link whose target names no heading", "See [this](#b16-round-99).", "row", "detect", ""),
    ("a figure in an image's description", "See ![7 ppm](x.png).", "row", "detect", ""),
    ("a figure in struck text", "See ~~7 ppm~~.", "row", "detect", ""),
    ("a figure in a footnote", "See this[^n].\n\n[^n]: 7 ppm.", "end", "detect", ""),
    ("a figure in a fenced code block", "```text\n7 ppm\n```", "end", "detect", ""),
    ("a figure in a raw HTML block", "<div>\n7 ppm\n</div>", "end", "detect", ""),
    ("a figure in a task list item", "- [ ] 7 ppm", "end", "detect", ""),
    ("a hard line break between a number and its unit", D + "\\\nppm.", "end", "detect", ""),
    ("a soft line break between a number and its unit", D + "\nppm.", "end", "detect", ""),
    ("a measurement in a setext heading", "Drift 7 ppm\n---", "end", "detect", ""),
    ("a measurement in a block quote", "> Drift 7 ppm", "end", "detect", ""),
    ("a figure in a link's title", 'See [this](#b16c-attribution "7 ppm").', "row", "pass",
     "a link's title is not text: a tooltip"),
    ("a figure in a reference definition", '[d]: #b16c-attribution "7 ppm"', "end", "pass", "a definition renders nothing"),
    ("a figure in a footnote nothing cites", "[^z]: 7 ppm.", "end", "pass", "a footnote nothing cites renders nothing"),
    ("a visible exclamation mark after an identifier", D + "!ppm.", "row", "pass",
     "a mark a reader sees ends the phrase (round 6's closed list)"),
    ("an escaped exclamation mark before a link", D + "\\![x](#b16c-attribution)ppm.", "row", "pass",
     "the escape makes the mark text a reader sees"),
    ("a link to a heading of the page", "See [this](#b16-round-7-no-markup).", "row", "pass", "a target that resolves"),
]


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    text = PAGE.read_text(encoding="utf-8")
    assert text.count(ROW) == 1 and text.count(PARA) == 1 and text.endswith("\n")
    forms = [(n, a, w, "detect", "", "round 5") for n, a, w in forms_of("r5_self_probes.py")]
    forms += [f + ("round 6",) for f in forms_of("r6_self_probes.py")] + [f + ("round 7",) for f in forms_of("r7_self_probes.py")]
    forms = [(n, a, w, "pass", RULED[n], s + ", ruled in round 8") if n in RULED else (n, a, w, e, y, s)
             for n, a, w, e, y, s in forms] + [f + ("round 8",) for f in FORMS]
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
        lines = range(line0, line0 + added.count("\n") + 1)
        p = subprocess.run([sys.executable, "-I", str(CHECK), str(d / PAGE.name), str(PACKET), str(d / "rows.tsv"),
                            str(d / "cov.tsv"), "--repo", str(REPO)], capture_output=True, text=True, timeout=600)
        named = [x for x in p.stdout.splitlines() if x.split(" ")[0] in ("UNCOVERED", "MARKUP")
                 and any(f":{n} " in x for n in lines)]
        det = p.returncode == 1 and bool(named)
        out.append(dict(probe=name, **{"from": src}, inserted=added, where=at, lines=[lines[0], lines[-1]], rc=p.returncode,
                        detected=det, markup=any(x.startswith("MARKUP ") for x in named),
                        measurement=any("(a measurement" in x for x in named),
                        named=[x.split(" (")[0] for x in named], expect=expect, why_pass=why,
                        met=det if expect == "detect" else (p.returncode == rc0 and not named)))
        print(f"{'MET ' if out[-1]['met'] else 'NOT '} {expect:6s} {'DETECTED' if det else 'passed  '} {name}")
    OUT.write_text(json.dumps(dict(note="Lane B16 round 8: further forms against the check, each on an altered copy, "
                                        "rounds 5 to 7 first; offline, no bench action",
                                   unchanged_page_rc=rc0, detected=sum(x["detected"] for x in out),
                                   expected_pass=sum(x["expect"] == "pass" for x in out),
                                   ruled=sorted(RULED), met=sum(x["met"] for x in out), probes=out),
                              indent=1, ensure_ascii=False) + "\n")
    return 0 if all(x["met"] for x in out) else 1


if __name__ == "__main__":
    sys.exit(main())
