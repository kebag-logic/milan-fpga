#!/usr/bin/env python3
"""Lane B16, round 10: further forms against check_b16_figures.py, each on an altered copy (offline).

usage: <parser python> r10_self_probes.py <check_b16_figures.py> <findings.md> <packet root> <scratch dir> <out.json>

Round 9's r9_self_probes.py, with round 9's forms read unchanged from it after round 5's to round 8's, then
round 10's: autolinks the parser gives no position, at the introduction's first and last lines and on the
line above it, after a code span on a later line of a paragraph, two of them on a line, in a heading, a block
quote, a list item and a paragraph at the page's end, and at the Contents entry; a figure inside a link whose
text an address opens; an entity on the introduction's first covered line before a figure; and,
expected to pass, an e-mail address in angle brackets, in a code span or as a link's text, and a cell beyond
a table's header, which GitHub's parser drops for a reader too. A form whose block the check refuses whole is
DETECTED when it is named at that block's first covered line (NAMED); every other form as in round 9.

Round 9's docstring follows.

Lane B16, round 9: further forms against check_b16_figures.py, each on an altered copy (offline).

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
FORMS = [  # round 10: (name, edits, "lines" or "end", expect, why a pass is expected); an edit is (line, how, text)
    ("an e-mail address before a figure on the introduction's first covered line", [("intro", "end", " Write to x@example.com 7 ppm.")], "lines",
     "detect", ""),
    ("an e-mail address before a figure on the introduction's last line", [("introlast", "end", " Write to x@example.com 7 ppm.")], "lines", "detect", ""),
    ("an e-mail address on the line above the introduction's covered part, a figure on its first covered line",
     [("intro-1", "end", " Write to x@example.com."), ("intro", "end", F)], "lines", "detect", ""),
    ("an e-mail address after a code span on a later line of the section's first paragraph",
     [("para+1", "end", " See `x`, x@example.com 7 ppm.")], "lines", "detect", ""),
    ("two e-mail addresses on the section's first paragraph", [("para", "end", " x@example.com 7 y@example.com 8 ppm.")],
     "lines", "detect", ""),
    ("an e-mail address with no digit at the Contents entry", [("toc", "end", " Write to x@example.com.")], "lines",
     "detect", ""),
    ("an e-mail address before a figure in a heading of the section", [("method", "end", " x@example.com 7 ppm")],
     "lines", "detect", ""),
    ("an e-mail address before a figure in a block quote at the page's end", "> Write to x@example.com 7 ppm.", "end",
     "detect", ""),
    ("an e-mail address before a figure in a list item at the page's end", "- Write to x@example.com 7 ppm.", "end",
     "detect", ""),
    ("an e-mail address before a figure in a paragraph at the page's end", "Write to x@example.com 7 ppm.", "end",
     "detect", ""),
    ("a figure in a link whose text a mailto: address opens", [("para", "end", " [mailto:x@example.com 7](#b16c-attribution) ppm.")],
     "lines", "detect", ""),
    ("an entity on the introduction's first covered line, a figure after it", [("intro", "end", " &amp;" + F)], "lines",
     "detect", ""),
    ("an e-mail address in angle brackets in the section's first paragraph", [("para", "end", " Write to <x@example.com>.")],
     "lines", "pass", "a core autolink, which the parser places, its text holding no digit"),
    ("an e-mail address in a code span on the introduction's first covered line", [("intro", "end", " `x@example.com`")],
     "lines", "pass", "code, which the autolink extension leaves alone"),
    ("an e-mail address as a link's text in the section's first paragraph",
     [("para", "end", " [x@example.com](#b16c-attribution)")], "lines", "pass",
     "a link's text, which the autolink extension leaves alone; its target resolves"),
    ("a figure in a cell beyond the header's count in the section's first table", [("cell", "end", " 7 ppm |")], "lines",
     "pass", "GitHub's parser drops a cell beyond the header's count, so neither a reader nor the check sees it"),
]
NAMED = {  # round 10: forms whose block is refused whole, named at its first covered line
    "an e-mail address before a figure on the introduction's last line": ["intro"],
    "an e-mail address on the line above the introduction's covered part, a figure on its first covered line": ["intro"],
    "an e-mail address after a code span on a later line of the section's first paragraph": ["para"],
}

def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    text = PAGE.read_text(encoding="utf-8")
    assert text.count(ROW) == 1 and text.count(PARA) == 1 and text.endswith("\n")
    forms = [(n, a, w, "detect", "", "round 5") for n, a, w in forms_of("r5_self_probes.py")]
    forms += [f + ("round 6",) for f in forms_of("r6_self_probes.py")] + [f + ("round 7",) for f in forms_of("r7_self_probes.py")]
    forms = [(n, a, w, "pass", RULED[n], s + ", ruled in round 8") if n in RULED else (n, a, w, e, y, s)
             for n, a, w, e, y, s in forms] + [f + ("round 8",) for f in forms_of("r8_self_probes.py")]
    forms += [f + ("round 9",) for f in forms_of("r9_self_probes.py")] + [f + ("round 10",) for f in FORMS]
    ls = text.split("\n")
    at_ = dict(intro=next(i for i, x in enumerate(ls) if x.startswith("In lane B16, the operator tried the reference peer's")),
               toc=next(i for i, x in enumerate(ls) if x.startswith("- **[Dev 5603c353, 2026-10-12: lane B16]")),
               heading=next(i for i, x in enumerate(ls) if x.startswith("## Dev 5603c353, 2026-10-12: lane B16")))
    at_["first"] = next(i for i in range(at_["intro"], -1, -1) if not ls[i - 1].strip())
    at_["introlast"] = next(i for i in range(at_["intro"], len(ls)) if not ls[i + 1].strip())
    at_["para"] = next(i for i, x in enumerate(ls) if x.startswith("The loopback did not form. The peer's listener"))
    at_["para+1"] = at_["para"] + 1
    at_["cell"] = next(i for i, x in enumerate(ls) if x.startswith("| Restore | Done | See [B16: bench as left]"))
    at_["method"] = next(i for i, x in enumerate(ls) if x == "### B16: method")
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
            if name in NAMED:
                edited = [at_[k] + 1 for k in NAMED[name]]
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
    OUT.write_text(json.dumps(dict(note="Lane B16 round 10: further forms against the check, each on an altered copy, "
                                        "rounds 5 to 9 first; offline, no bench action",
                                   unchanged_page_rc=rc0, detected=sum(x["detected"] for x in out),
                                   expected_pass=sum(x["expect"] == "pass" for x in out),
                                   ruled=sorted(RULED), met=sum(x["met"] for x in out), probes=out),
                              indent=1, ensure_ascii=False) + "\n")
    return 0 if all(x["met"] for x in out) else 1


if __name__ == "__main__":
    sys.exit(main())
