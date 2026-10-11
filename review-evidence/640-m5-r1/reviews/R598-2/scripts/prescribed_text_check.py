#!/usr/bin/env python3
"""Check that the round-2 prescribed texts are present verbatim at a head.
Usage: prescribed_text_check.py <clone> <rev> <pr-body.md>"""
import re, subprocess, sys
clone, rev, body_path = sys.argv[1:4]
show = lambda p: subprocess.run(["git", "-C", clone, "show", f"{rev}:{p}"],
                                capture_output=True, text=True, check=True).stdout
plan = show("docs/design/MARK_II_AREA_PLAN.md")
csr = show("hdl/common/csr/milan_csr.sv")
body = open(body_path, encoding="utf-8").read().replace("\r", "")
# banner words with comment markers and line breaks removed
banner = " ".join(w for line in csr.splitlines()[1062:1071]
                  for w in line.replace("//!", " ").split())
norm = lambda s: " ".join(s.split())
checks = [
    ("R599-1-F1 example text, plan", plan,
     "[#649](https://github.com/kebag-logic/milan-fpga/issues/649) measured 211 LUTs per stream inside the datapath synthesis; that scope was not re-measured here.\n"
     "Out of context the base block grows about 12 per stream alone and about 62 in the integration proxy (M5: about 49 and 56)."),
    ("R599-1-F1 old claim gone, plan", None, "do not reproduce"),
    ("R598-1-S1 assignment sentence, plan", plan,
     "At M5's measured 121, the partial-central scenario becomes about 38,436, 396 over 38,040, pending the week-4 re-measure (D8)."),
    ("RES-1 exact text, banner (whitespace-normalised)", banner,
     "and stage 2 (an OR of the two stage-1 words since lane M5 of #640) loads r_data a cycle later on rd_pend2"),
    ("RES-1 stale phrase gone, banner", None, "four-way select into r_data"),
    ("RES-2 exact text, plan", plan, "M5 saved 121 LUTs routed and 127 post-synthesis in its scope"),
    ("RES-3 exact text, PR body", body, "the dev `e8454e27` block byte for byte apart from the module name"),
    ("F1/F2 disjoint attribution, PR body", body,
     "in three disjoint parts: `csr` -121 (credited); the processor wrapper -342, nearly all of it in `u_pp` (-344, nested inside the wrapper, not added); and about -227 in other untouched blocks."),
    ("F1/F2 old -686 gone, PR body", None, "-686"),
    ("S1 consequence, PR body", body,
     "At the measured 121, the partial-central scenario becomes about 38,436, 396 over 38,040, pending that re-measure (D8)."),
]
bad = 0
for name, hay, needle in checks:
    if hay is None:
        hits = {"plan": plan.count(needle), "banner": banner.count(needle), "body": body.count(needle)}
        ok = not any(hits.values())
        print(f"{'ok ' if ok else 'BAD'} {name}: occurrences {hits}")
    else:
        n = norm(hay).count(norm(needle))
        ok = n == 1
        print(f"{'ok ' if ok else 'BAD'} {name}: {n} occurrence(s)")
    bad += not ok
# arithmetic
print("sum -121-342-227 =", -121 - 342 - 227)
print("partial central 37,957 + (600-121) =", 37957 + 600 - 121, "; over 38,040 by", 37957 + 600 - 121 - 38040)
print("per-stream (N 1->8, 7 steps): base alone", round((3038 - 2955) / 7, 1), "proxy", round((2494 - 2058) / 7, 1),
      "M5 alone", round((2859 - 2515) / 7, 1), "proxy", round((2295 - 1903) / 7, 1))
sys.exit(1 if bad else 0)
