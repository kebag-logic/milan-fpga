#!/usr/bin/env python3
"""Lane B16, round 5: further escape forms against check_b16_figures.py, each on an altered copy (offline).

usage: r5_self_probes.py <check_b16_figures.py> <findings.md> <packet root> <scratch dir> <out.json>

Beyond the controls: each probe inserts one sentence (a measurement, or an identifier before a unit, in a
spelling or with a separator the controls do not try) before 'Every stage' on the B16c summary's attribution
row, or, for a line break, after 'exponent.' in the round 5 paragraph on the rule. It runs the check on the
copy with the real repository as --repo. A probe is DETECTED when the check exits 1 and names, on standard
output, an UNCOVERED number at the line the inserted text's first number is on; 'measurement' records
whether one was named a measurement. Nothing on the bench is read or written.
"""
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
FORMS = [  # (name, inserted text, where)
    ("descriptor index, unit after a line break", "The residual sat at CLOCK_DOMAIN 7\nppm.", "para"),
    ("descriptor index, unit in bold", "The residual sat at CLOCK_DOMAIN 7 **ppm**.", "row"),
    ("descriptor index, unit in code", "The residual sat at CLOCK_DOMAIN 7 `ppm`.", "row"),
    ("descriptor index, unit in brackets", "The residual sat at CLOCK_DOMAIN 7 (ppm).", "row"),
    ("descriptor index, unit after an HTML entity", "The residual sat at CLOCK_DOMAIN 7&nbsp;ppm.", "row"),
    ("descriptor index, unit after an HTML comment", "The residual sat at CLOCK_DOMAIN 7<!-- -->ppm.", "row"),
    ("descriptor index, unit after a thin space", "The residual sat at CLOCK_DOMAIN 7 ppm.", "row"),
    ("descriptor index, unit after a zero-width space", "The residual sat at CLOCK_DOMAIN 7​ppm.", "row"),
    ("descriptor index, unit after a backslash space", "The residual sat at CLOCK_DOMAIN 7\\ ppm.", "row"),
    ("descriptor index, unit in capitals", "The residual sat at CLOCK_DOMAIN 7 PPM.", "row"),
    ("descriptor index, per mille", "The residual sat at CLOCK_DOMAIN 7 ‰.", "row"),
    ("channel index pair, unit after", "The residual sat at channels 2 and 7 s.", "row"),
    ("step index, unit after", "The residual settled by step 7 s.", "row"),
    ("round index, glued unit", "The residual settled by round 7s.", "row"),
    ("list-item index, unit after a line break", "The residual sat at\n7. ppm", "para"),
    ("lane name before a unit", "The residual was B16 ppm.", "row"),
    ("review name before a unit", "The residual was R624-4 ppm.", "row"),
    ("clause number before a unit", "The residual was Milan v1.2 Table 5.4 ppm.", "row"),
    ("issue number before a unit", "The residual was #629 ppm.", "row"),
    ("fullwidth digit", "The residual was ７ ppm.", "row"),
    ("vulgar fraction", "The residual was ½ ppm.", "row"),
    ("superscript exponent", "The residual was 10⁻⁶ of the rate.", "row"),
    ("Unicode minus, new figure", "The floor was −130.00 dB.", "row"),
    ("number in a quoted mention, unit after", 'The residual was "7.25" ppm.', "row"),
    ("number word zero before a unit", "The residual was zero ppm.", "row"),
    ("number word before a unit", "The residual was seven ppm.", "row"),
    ("hex word before a unit", "The residual was 0x7 ppm.", "row"),
    ("fraction before a unit", "The residual was 1/2 ppm.", "row"),
    ("range, second end", "The residual stayed in 2-9 s.", "row"),
    ("thin-space thousands", "The run held 1 234 frames.", "row"),
    ("percent glued", "The residual was 7%.", "row"),
    ("path in code naming no file", "See `summary/bcrf/c-b9-grade7.json`.", "row"),
    ("link target off the repository", "See [the note](https://example.com/7ppm).", "row"),
    ("link target to no heading", "See [the round](#b16-round-7-ppm).", "row"),
    ("page marker not in the list", "<!-- b16-725 -->", "row"),
    ("identifier glued to a unit", "The residual sat at McASP0s.", "row"),
]


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    text = PAGE.read_text(encoding="utf-8")
    assert text.count(ROW) == 1 and text.count(PARA) == 1
    out = []
    for i, (name, added, at) in enumerate(FORMS):
        d = SCRATCH / f"p{i}" / "docs" / "findings"
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(PAGE.parent / "README.md", d / "README.md")
        old = ROW if at == "row" else PARA
        new = old.replace("Every stage", added + " Every stage") if at == "row" else old.replace(
            "exponent. ", "exponent. " + added + " ")
        (d / PAGE.name).write_text(text.replace(old, new), encoding="utf-8")
        first = re.search(r"\d|zero|seven|\u00bd", added)
        line = text[:text.index(old)].count("\n") + 1 + added[:first.start()].count("\n")
        p = subprocess.run([sys.executable, "-I", str(CHECK), str(d / PAGE.name), str(PACKET), str(d / "rows.tsv"),
                            str(d / "cov.tsv"), "--repo", str(REPO)], capture_output=True, text=True, timeout=600)
        named = [x for x in p.stdout.splitlines() if x.startswith("UNCOVERED ") and f":{line} " in x]
        out.append(dict(probe=name, inserted=added, line=line, rc=p.returncode,
                        detected=p.returncode == 1 and bool(named), measurement=any("(a measurement" in x for x in named),
                        named=[x.split(" | ")[0] for x in named]))
        print(f"{'DETECTED' if out[-1]['detected'] else 'MISSED  '} {name}: {out[-1]['named']}")
    OUT.write_text(json.dumps(dict(note="Lane B16 round 5: further escape forms against the check, each on an altered "
                                        "copy; offline, no bench action", probes=out), indent=1) + "\n")
    return 0 if all(x["detected"] for x in out) else 1


if __name__ == "__main__":
    sys.exit(main())
