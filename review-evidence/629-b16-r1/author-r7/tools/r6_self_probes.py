#!/usr/bin/env python3
"""Lane B16, round 6: further escape forms against check_b16_figures.py, each on an altered copy (offline).

usage: r6_self_probes.py <check_b16_figures.py> <findings.md> <packet root> <scratch dir> <out.json>

Round 5's r5_self_probes.py ran 36 forms; this runs them again, read unchanged from that file (its FORMS
list), then round 6's: the forms R625-5 found passing in its own campaign, a word no list names after each
kind of identifier, separators and spellings the normalisation reads (an entity, an escape, a comment in
code or holding a blank line), a range into a figure a row claims, and a code literal before a unit. Each
inserts one sentence before 'Every stage' on the B16c summary's attribution row ("row"), after 'exponent. '
in round 5's paragraph on the rule ("para"), or replaces one text ("sub"), and runs the check on the copy
with the real repository as --repo. A probe is DETECTED when the check exits 1 and names, on standard
output, an UNCOVERED number at the line the inserted text's first number is on.

Some forms pass by the rule as stated (expect "pass"), and are run so that the record shows it: a mark
that ends a phrase (a full stop, a comma, a colon, a dash set off by spaces) or a possessive after an identifier,
a code literal before a word, and round 5's page marker, now inside a comment the check drops. A form
meets its expectation when it is DETECTED and expected "detect", or exits 0 and expected "pass". Nothing
on the bench is read or written.
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
R5 = Path(__file__).with_name("r5_self_probes.py")
R5_FORMS = next(ast.literal_eval(n.value) for n in ast.parse(R5.read_text()).body
                if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "FORMS")
# round 5's forms whose expectation round 6 changes by design
R5_PASS = {"page marker not in the list": "inside a comment, which the check drops before it reads the text"}
D = "The residual sat at CLOCK_DOMAIN 7"
FORMS = [  # (name, inserted text or (old, new), where, expect, why a pass is expected)
    ("descriptor index, small hyphen-minus (R625-5)", D + "﹣ppm.", "row", "detect", ""),
    ("descriptor index, fullwidth hyphen-minus (R625-5)", D + "－ppm.", "row", "detect", ""),
    ("descriptor index, em dash (R625-5)", D + "—ppm.", "row", "detect", ""),
    ("descriptor index, closing bracket (R625-5)", D + ") ppm.", "row", "detect", ""),
    ("descriptor index, apostrophe (R625-5)", D + "' ppm.", "row", "detect", ""),
    ("descriptor index, en dash", D + "–ppm.", "row", "detect", ""),
    ("descriptor index, figure dash", D + "‒ppm.", "row", "detect", ""),
    ("descriptor index, minus sign", D + "−ppm.", "row", "detect", ""),
    ("descriptor index, slash (R624-5-S1)", D + "/ppm.", "row", "detect", ""),
    ("descriptor index, single quotes (R624-5-S1)", D + " 'ppm'.", "row", "detect", ""),
    ("descriptor index in brackets (R624-5-S1)", "The residual was (CLOCK_DOMAIN 7) ppm.", "row", "detect", ""),
    ("descriptor index, dBm (R624-5-S1)", D + " dBm.", "row", "detect", ""),
    ("descriptor index, degrees", D + "°.", "row", "detect", ""),
    ("descriptor index, a dash set off by spaces, then a unit", D + " -- ppm.", "row", "detect", ""),
    ("descriptor index, escaped hyphen", D + "\\-ppm.", "row", "detect", ""),
    ("descriptor index, entity space, a word", D + "&#32;furlongs.", "row", "detect", ""),
    ("descriptor index, a word no list names", D + " furlongs.", "row", "detect", ""),
    ("descriptor index, a count noun (R624-5-S1)", "The decode found STREAM_INPUT 2 events.", "row", "detect", ""),
    ("channel index, a count noun (R624-5-S1)", "The playback logged channel 3 underruns.", "row", "detect", ""),
    ("channel pair, a count noun (R624-5-S1)", "The listener made channels 0 and 4 drops.", "row", "detect", ""),
    ("step index, a word", "The lock took step 7 furlongs.", "row", "detect", ""),
    ("round index, a word", "The lock took round 7 furlongs.", "row", "detect", ""),
    ("lane name, a word", "The lock took lane B16 furlongs.", "row", "detect", ""),
    ("review name, a word", "The lock took R624-5 furlongs.", "row", "detect", ""),
    ("operator, a word", "The lock took [A603] furlongs.", "row", "detect", ""),
    ("serial port, a word", "The lock took McASP0 furlongs.", "row", "detect", ""),
    ("hash name, a word", "The lock took SHA-256 furlongs.", "row", "detect", ""),
    ("issue number, a word", "The lock took #629 furlongs.", "row", "detect", ""),
    ("clause number, a word", "The lock took IEEE 1722.1 furlongs.", "row", "detect", ""),
    ("clause pair, a word", "The lock took Milan v1.2 Table 5.4 furlongs.", "row", "detect", ""),
    ("descriptor index into a claimed measurement (a range)",
     ("CRF sink +10.60 to +10.65 ppm", "CRF sink +10.60 to CLOCK_DOMAIN 7 to +10.65 ppm"), "sub", "detect", ""),
    ("entity digits before a unit", "The residual was &#55;&#48; ppm.", "row", "detect", ""),
    ("a comment shown in a code span", "See `<!-- 7 ppm -->`.", "row", "detect", ""),
    ("a comment holding a blank line, inside a paragraph", D + "<!--\n\n-->ppm.", "para", "detect", ""),
    ("a code literal before a unit", "See `pts1` milliseconds.", "row", "detect", ""),
    ("descriptor index, full stop, a unit (R625-5)", "The residual was CLOCK_DOMAIN 7. ppm.", "row", "pass",
     "a full stop ends the identifier's phrase"),
    ("channel pair, full stop, a unit (R625-5)", "The residual was channels 7 to 8. ppm.", "row", "pass",
     "a full stop ends the identifier's phrase"),
    ("descriptor index, comma, a word", D + ", furlongs.", "row", "pass", "a comma ends the identifier's phrase"),
    ("descriptor index, colon, a unit (R624-5-S1)", D + ": ppm.", "row", "pass", "a colon ends the identifier's phrase"),
    ("descriptor index, a dash set off by spaces, a word", D + " -- furlongs.", "row", "pass",
     "a dash set off by spaces ends the identifier's phrase"),
    ("descriptor index, possessive, a word", D + "'s furlongs.", "row", "pass", "a possessive is on the list"),
    ("a code literal before a word", "See `pts1` furlongs.", "row", "pass", "a code literal ends with its code word"),
]


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    text = PAGE.read_text(encoding="utf-8")
    assert text.count(ROW) == 1 and text.count(PARA) == 1
    forms = [(n, a, w, "pass" if n in R5_PASS else "detect", R5_PASS.get(n, ""), "round 5") for n, a, w in R5_FORMS]
    forms += [f + ("round 6",) for f in FORMS]
    out = []
    for i, (name, added, at, expect, why, src) in enumerate(forms):
        d = SCRATCH / f"p{i}" / "docs" / "findings"
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(PAGE.parent / "README.md", d / "README.md")
        if at == "sub":
            old, new = added
            added = new
        else:
            old = ROW if at == "row" else PARA
            new = old.replace("Every stage", added + " Every stage") if at == "row" else old.replace(
                "exponent. ", "exponent. " + added + " ")
        assert text.count(old) == 1, old
        (d / PAGE.name).write_text(text.replace(old, new), encoding="utf-8")
        first = re.search(r"\d|zero|seven|½|&#5", added)
        line = text[:text.index(old)].count("\n") + 1 + (added[:first.start()].count("\n") if first else 0)
        p = subprocess.run([sys.executable, "-I", str(CHECK), str(d / PAGE.name), str(PACKET), str(d / "rows.tsv"),
                            str(d / "cov.tsv"), "--repo", str(REPO)], capture_output=True, text=True, timeout=600)
        named = [x for x in p.stdout.splitlines() if x.startswith("UNCOVERED ") and f":{line} " in x]
        det = p.returncode == 1 and bool(named)
        out.append(dict(probe=name, **{"from": src}, inserted=added, line=line, rc=p.returncode, detected=det,
                        measurement=any("(a measurement" in x for x in named),
                        named=[x.split(" | ")[0] for x in named], expect=expect, why_pass=why,
                        met=det if expect == "detect" else p.returncode == 0))
        print(f"{'MET ' if out[-1]['met'] else 'NOT '} {expect:6s} {'DETECTED' if det else 'passed  '} {name}")
    OUT.write_text(json.dumps(dict(note="Lane B16 round 6: further escape forms against the check, each on an altered "
                                        "copy, round 5's first; offline, no bench action",
                                   detected=sum(x["detected"] for x in out), expected_pass=sum(x["expect"] == "pass" for x in out),
                                   met=sum(x["met"] for x in out), probes=out), indent=1, ensure_ascii=False) + "\n")
    return 0 if all(x["met"] for x in out) else 1


if __name__ == "__main__":
    sys.exit(main())
