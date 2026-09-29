#!/usr/bin/env python3
"""R398-3 F1 verification on the PR #133 body (read-only, portable).

usage: f1_body_check.py <body.md> <parent milan_dp/README.md at dev 79c36963>
Exit 0 when the body meets F1's required outcome (option 1), 1 otherwise.
Each criterion prints PASS or FAIL.
"""
import re
import sys

body = open(sys.argv[1], encoding="utf-8").read()
readme = open(sys.argv[2], encoding="utf-8").read().split("\n")
ok = True


def crit(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok &= bool(cond)


# 1. no sentence saying the two lists' parent edits are disjoint
flat = re.sub(r"\s+", " ", body)
disjoint = [m.group(0) for m in re.finditer(
    r"[^.]*\b(touch no common parent file|share no (common )?parent file|disjoint)[^.]*\.", flat)]
bad = [s for s in disjoint if "code edits share no parent file" not in s]
crit("no sentence calls the two lists' adoption edits parent-file disjoint "
     f"(matches: {len(disjoint)}, unqualified: {len(bad)})", not bad)
crit("the correction names where the documentation updates meet",
     re.search(r"code edits share no parent file\. Their documentation updates meet in "
               r"`tb/verilator/milan_dp/README\.md`", flat) is not None)

# 2. the combined README entry covers both lanes' updates
note = flat[flat.find("Composed head `99bfd4bc`"):]
for token in ("`:443`", "`:528-530`", "`:633-637`", "`:877-883`", "`gmstep`",
              "`gptp`/`gptp-lat`", "`ax1x1gptp`", "two hold checks", "every `sim_nxn.cpp` leg",
              "edits once for both"):
    crit(f"composed-head note names {token}", token in note)

# 3. closing references
closes = sorted(int(n) for n in re.findall(
    r"(?im)^\s*(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+#(\d+)", body))
crit(f"closing references exactly #29 #64 #65 #108 (found {closes})", closes == [29, 64, 65, 108])

# 4. the cited parent lines hold the text the note describes (dev 79c36963)
def line(n):
    return readme[n - 1]


crit(":443 is the [C] row", line(443).startswith("| `[C]` |"))
crit(":528-530 is the issue-108 sentence",
     "does not" in line(528) and "processor issue 108" in line(529) and "measures that" in line(530))
crit(":633-637 is the walk-starter list",
     "starts the restore walk" in line(633) and "`sim_main`, `sim_nxn`, `sim_aclk`" in line(637))
crit(":877-883 is the [AECP] degrade-arm paragraph",
     "The `[AECP]` checks in `sim_nxn.cpp` grade that path" in line(877)
     and "padded to 60." in line(882) and line(883).strip() == "")

print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
