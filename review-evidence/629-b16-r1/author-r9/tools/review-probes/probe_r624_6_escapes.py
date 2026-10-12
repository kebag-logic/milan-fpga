#!/usr/bin/env python3
"""R624-6 own escape probes against lane B16's figures check (per-digit coverage + closed follower list).

usage: probe_r624_6_escapes.py <check_b16_figures.py> <findings page> <packet root> <repo> <work dir> <out.json>
Each probe edits a copy of the page (README.md copied beside it), runs the check unchanged, and records
the exit code and whether the output names the inserted text. 'inline' probes replace text on the B16c
attribution row (line 3244) without moving any line; 'append' probes add lines at the end of the page,
which is inside the covered text (round 6's subsection is the page's last), so no line before moves.
expect: 'fail' = a measurement a reader sees, which the check must refuse; 'any' = recorded only."""
import json, os, shutil, subprocess, sys
CHECK, PAGE, PKT, REPO, WORK, OUT = sys.argv[1:7]
src = open(PAGE, encoding="utf-8").read().split("\n")
ANCHOR = 3244
row = src[ANCHOR - 1]
assert row.startswith("| The tone source and the peer's path into its talker |"), row[:60]
TAIL = "every worst block is -123.93 dB. |"
assert row.endswith(TAIL)
def inline(ins):
    return lambda L: L[:ANCHOR - 1] + [row[:-len(TAIL)] + TAIL[:-2] + " " + ins + " |"] + L[ANCHOR:]
def append(block):
    return lambda L: L + block.split("\n")
P = [
 ("of-unit", "fail", inline("Drift on CLOCK_DOMAIN 7 of ppm.")),
 ("and-unit", "fail", inline("Drift on CLOCK_DOMAIN 7 and ppm.")),
 ("possessive-unit", "fail", inline("Drift on CLOCK_DOMAIN 7's ppm.")),
 ("br-tag", "fail", inline("Drift on CLOCK_DOMAIN 7<br>ppm.")),
 ("sup-tag", "fail", inline("Drift on CLOCK_DOMAIN 7<sup>ppm</sup>.")),
 ("entity-digit", "fail", inline("Drift on CLOCK_DOMAIN &#55; ppm.")),
 ("hex-entity-digit", "fail", inline("Drift on CLOCK_DOMAIN &#x37;&#x20;ppm.")),
 ("word-joiner", "fail", inline("Drift on CLOCK_DOMAIN 7⁠ppm.")),
 ("bom-joiner", "fail", inline("Drift on CLOCK_DOMAIN 7﻿ppm.")),
 ("narrow-nbsp", "fail", inline("Drift on CLOCK_DOMAIN 7 ppm.")),
 ("ideographic-space", "fail", inline("Drift on CLOCK_DOMAIN 7　ppm.")),
 ("fullwidth-unit", "fail", inline("Drift on CLOCK_DOMAIN 7 ｐｐｍ.")),
 ("arabic-indic-digit", "fail", inline("Drift on CLOCK_DOMAIN ٧ ppm.")),
 ("math-bold-digit", "fail", inline("Drift on CLOCK_DOMAIN \U0001d7d5 ppm.")),
 ("range-to-unitword", "fail", inline("Drift on CLOCK_DOMAIN 7 to 8 parts per million.")),
 ("lane-glued", "fail", inline("Drift of B16 7ppm.")),
 ("issue-number-unit", "fail", inline("Drift of #645 ppm.")),
 ("uncited-issue", "fail", inline("See #7.")),
 ("step-index-ms", "fail", inline("Lock at step 7 ms.")),
 ("mcasp-index", "fail", inline("Drift of McASP7 ppm.")),
 ("table-cell-colon", "any", inline("Drift: CLOCK_DOMAIN 7: ppm.")),
 ("full-stop", "any", inline("Drift on CLOCK_DOMAIN 7. Ppm.")),
 ("fenced-code", "fail", append("\n```text\n7 ppm\n```")),
 ("html-block", "fail", append("\n<div>\n7 ppm\n</div>")),
 ("image-alt", "fail", append("\n![7 ppm](#b16-limits)")),
 ("abbr-title-attr", "any", append("\n<abbr title=\"7 ppm\">drift</abbr>")),
 ("link-ref-title", "any", append("\n[d]: #b16-limits \"7 ppm\"")),
 ("table-two-cells", "any", append("\n| Drift | Unit |\n|---|---|\n| CLOCK_DOMAIN 7 | ppm |")),
 ("heading-measure", "fail", append("\n#### Drift 7 ppm")),
 ("blockquote", "fail", append("\n> 7 ppm")),
 ("list-item-7", "fail", append("\n7. ppm")),
 ("words-hundred", "any", append("\nA drift of a hundred ppm.")),
 ("or-so-unit", "any", inline("Drift on CLOCK_DOMAIN 7 or so ppm.")),
 ("or-more-unit", "any", inline("Drift on CLOCK_DOMAIN 7 or more ppm.")),
 ("and-a-half-unit", "any", inline("Drift on CLOCK_DOMAIN 7 and a half ppm.")),
 ("to-some-unit", "any", inline("Drift on CLOCK_DOMAIN 7 to some ppm.")),
 ("channel-or-so-dB", "any", inline("Residual on channel 1 or so dB.")),
]
res = []
for name, expect, f in P:
    d = os.path.join(WORK, name)
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    open(os.path.join(d, "page.md"), "w", encoding="utf-8").write("\n".join(f(list(src))))
    shutil.copy(os.path.join(os.path.dirname(PAGE), "README.md"), os.path.join(d, "README.md"))
    pr = subprocess.run([sys.executable, "-I", CHECK, os.path.join(d, "page.md"), PKT, os.path.join(d, "rows.tsv"),
                         os.path.join(d, "cov.tsv"), "--repo", REPO], capture_output=True, text=True)
    out = pr.stdout + pr.stderr
    try:
        cov = open(os.path.join(d, "cov.tsv"), encoding="utf-8").read()
    except OSError:
        cov = ""
    named = [l for l in (out + cov).splitlines() if "UNCOVERED" in l or "MEASURE" in l.upper() and "uncovered_measurements" not in l]
    detected = pr.returncode != 0
    ok = detected if expect == "fail" else True
    res.append(dict(probe=name, expect=expect, rc=pr.returncode, detected=detected, meets_expectation=ok,
                    named=named[:3], summary=pr.stdout.strip().splitlines()[-1][:300] if pr.stdout.strip() else pr.stderr[-300:]))
    print(f"{name:22s} expect={expect:4s} rc={pr.returncode} detected={detected} ok={ok} {named[:1]}")
json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
print("not meeting expectation:", [r["probe"] for r in res if not r["meets_expectation"]])
