#!/usr/bin/env python3
"""Lane B16, round 9: further forms against check_b16_figures.py, each on an altered copy (offline).

usage: <parser python> r9_self_probes.py <check_b16_figures.py> <findings.md> <packet root> <scratch dir> <out.json>

Round 8's r8_self_probes.py, with round 8's forms read unchanged from it after round 5's to round 7's, then
round 9's: constructs that open on an uncovered line and close on a covered one, or the reverse, at the
introduction, the section's heading and the Contents entry; each way the parser counts fewer line breaks
than the source holds, with a figure where a reader would see it; and, expected to pass, line breaks and
constructs the parser places correctly, and R624-8-S1's emoji shortcode. A round 9 form ("lines") replaces
whole lines, so no line moves; it is DETECTED when the check exits 1 and names an edited line.

Round 8's docstring follows.

Lane B16, round 8: further forms against check_b16_figures.py, each on an altered copy (offline).

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
    """The FORMS list of an earlier round's tool, with what it builds on: its D, F and S1 assignments only."""
    ns = {}
    body = [n for n in ast.parse(Path(__file__).with_name(name).read_text()).body
            if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) in ("D", "F", "S1", "FORMS")]
    exec(compile(ast.Module(body=body, type_ignores=[]), name, "exec"), {}, ns)
    return ns["FORMS"]


RULED = {  # round 7's forms the parser reads as text or a link: expected to pass, and why
    "an autolink": "a link, read on its text, which holds no digit",
    "a tag in a code span": "code is text a reader sees: the tag is shown as written",
    "a comment after a backslash": "the backslash makes the comment text, shown as written",
    "an unclosed tag": "not a tag: the parser yields it as text",
    "angle brackets around a link target": "a target that resolves is not read",
}
F = " THD+N -90 dB"
FORMS = [  # round 9: (name, edits, "lines", expect, why a pass is expected); an edit is (line, how, text)
    ("a <pre> block opened above the section's heading, closed on it after a figure",
     [("heading-1", "set", "<pre>"), ("heading", "end", F + "</pre>")], "lines", "detect", ""),
    ("a <pre> block opened above the Contents entry, closed on it after a figure",
     [("toc-1", "set", "<pre>"), ("toc", "end", F + "</pre>")], "lines", "detect", ""),
    ("a comment opened above the introduction, closed on its first covered line after a figure",
     [("intro-1", "set", "<!--"), ("intro", "end", F + " -->")], "lines", "detect", ""),
    ("a <script> block opened above the Contents entry, closed on it after a figure",
     [("toc-1", "set", "<script>"), ("toc", "end", F + "</script>")], "lines", "detect", ""),
    ("a figure in struck text opened above the introduction",
     [("intro-1", "start", "~~"), ("intro", "end", F + "~~")], "lines", "detect", ""),
    ("a figure in an image's description, from the Contents entry onto the line below",
     [("toc", "end", " ![-90"), ("toc+1", "set", "dB](https://example.com/x.png)")], "lines", "detect", ""),
    ("a backslash line break above the introduction, a figure on its first covered line",
     [("intro-2", "end", "\\"), ("intro", "end", F)], "lines", "detect", ""),
    ("a link's title over a line break above the introduction, a figure on its first covered line",
     [("intro-2", "end", ' [x](#b16c-attribution "a'), ("intro-1", "start", 'b") '), ("intro", "end", F)], "lines",
     "detect", ""),
    ("a link's target over a line break above the introduction, a figure on its first covered line",
     [("intro-2", "end", " [x]("), ("intro-1", "start", "#b16c-attribution) "), ("intro", "end", F)], "lines", "detect", ""),
    ("a reference label over a line break above the introduction, a figure on its first covered line",
     [("intro-2", "end", " [x][late"), ("intro-1", "start", "label] "), ("intro", "end", F),
      ("eof", "set", "\n[late label]: #b16c-attribution\n")], "lines", "detect", ""),
    ("an image's title over a line break above the introduction, a figure on its first covered line",
     [("intro-2", "end", ' ![x](https://example.com/x.png "a'), ("intro-1", "start", 'b") '), ("intro", "end", F)],
     "lines", "detect", ""),
    ("a reference definition opening the introduction's paragraph, a figure on its first covered line",
     [("first", "set", "[late label]: #b16c-attribution"), ("intro", "end", F)], "lines", "detect", ""),
    ("a backslash line break in a paragraph of the section, a figure after it",
     "Drift held.\\\nThen" + F + ".", "end", "detect", ""),
    ("a reference definition opening a paragraph of the section, a figure in it",
     "[late label]: #b16c-attribution\nThen" + F + ".", "end", "detect", ""),
    ("a hard line break of two spaces above the introduction", [("intro-2", "end", "  ")], "lines", "pass",
     "the parser counts this break, so every line keeps its number"),
    ("emphasis over the line break into the introduction's first covered line",
     [("intro-1", "start", "*"), ("intro", "end", "*")], "lines", "pass", "emphasis is on the allowlist, read on its text"),
    ("a link whose text runs over the line break into the introduction's first covered line",
     [("intro-1", "set", "[See"), ("intro", "end", "](#b16c-attribution)")], "lines", "pass",
     "a link, read on its text, whose target resolves"),
    ("an emoji shortcode between an identifier and its unit (R624-8-S1)", "The residual sat at CLOCK_DOMAIN 7:smile:ppm.",
     "row", "pass", "the parser yields the shortcode as text, its colon ending the phrase; the emoji GitHub draws "
     "there is outside the parser it models"),
]


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    text = PAGE.read_text(encoding="utf-8")
    assert text.count(ROW) == 1 and text.count(PARA) == 1 and text.endswith("\n")
    forms = [(n, a, w, "detect", "", "round 5") for n, a, w in forms_of("r5_self_probes.py")]
    forms += [f + ("round 6",) for f in forms_of("r6_self_probes.py")] + [f + ("round 7",) for f in forms_of("r7_self_probes.py")]
    forms = [(n, a, w, "pass", RULED[n], s + ", ruled in round 8") if n in RULED else (n, a, w, e, y, s)
             for n, a, w, e, y, s in forms] + [f + ("round 8",) for f in forms_of("r8_self_probes.py")]
    forms += [f + ("round 9",) for f in FORMS]
    ls = text.split("\n")
    at_ = dict(intro=next(i for i, x in enumerate(ls) if x.startswith("In lane B16, the operator tried the reference peer's")),
               toc=next(i for i, x in enumerate(ls) if x.startswith("- **[Dev 5603c353, 2026-10-12: lane B16]")),
               heading=next(i for i, x in enumerate(ls) if x.startswith("## Dev 5603c353, 2026-10-12: lane B16")))
    at_["first"] = next(i for i in range(at_["intro"], -1, -1) if not ls[i - 1].strip())
    for k in ("intro", "toc", "heading"):
        at_[k + "-1"], at_[k + "-2"], at_[k + "+1"] = at_[k] - 1, at_[k] - 2, at_[k] + 1
    at_["eof"] = len(ls) - 1
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
        elif at == "lines":  # round 9: whole lines replaced, appended to or prefixed, so no line moves
            ls_ = list(ls)
            for k, how, t in added:
                i_ = at_[k]
                ls_[i_] = t if how == "set" else ls_[i_] + t if how == "end" else t + ls_[i_]
            new = "\n".join(ls_)
            edited = sorted({at_[k] + 1 for k, _, _ in added if k != "eof"})
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
        lines = edited if at == "lines" else range(line0, line0 + added.count("\n") + 1)
        p = subprocess.run([sys.executable, "-I", str(CHECK), str(d / PAGE.name), str(PACKET), str(d / "rows.tsv"),
                            str(d / "cov.tsv"), "--repo", str(REPO)], capture_output=True, text=True, timeout=600)
        named = [x for x in p.stdout.splitlines() if x.split(" ")[0] in ("UNCOVERED", "MARKUP")
                 and any(f":{n} " in x for n in lines)]
        det = p.returncode == 1 and bool(named)
        out.append(dict(probe=name, **{"from": src}, inserted=added if at != "lines" else [list(x) for x in added], where=at, lines=[lines[0], lines[-1]], rc=p.returncode,
                        detected=det, markup=any(x.startswith("MARKUP ") for x in named),
                        measurement=any("(a measurement" in x for x in named),
                        named=[x.split(" (")[0] for x in named], expect=expect, why_pass=why,
                        met=det if expect == "detect" else (p.returncode == rc0 and not named)))
        print(f"{'MET ' if out[-1]['met'] else 'NOT '} {expect:6s} {'DETECTED' if det else 'passed  '} {name}")
    OUT.write_text(json.dumps(dict(note="Lane B16 round 9: further forms against the check, each on an altered copy, "
                                        "rounds 5 to 8 first; offline, no bench action",
                                   unchanged_page_rc=rc0, detected=sum(x["detected"] for x in out),
                                   expected_pass=sum(x["expect"] == "pass" for x in out),
                                   ruled=sorted(RULED), met=sum(x["met"] for x in out), probes=out),
                              indent=1, ensure_ascii=False) + "\n")
    return 0 if all(x["met"] for x in out) else 1


if __name__ == "__main__":
    sys.exit(main())
