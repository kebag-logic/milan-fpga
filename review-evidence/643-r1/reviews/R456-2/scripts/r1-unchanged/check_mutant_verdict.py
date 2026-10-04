#!/usr/bin/env python3
"""R456-1: unit checks of tdm8_render_mutants.verdict()'s tuple handling and of
LAW_PHASES == kLawPhases. Usage: check_mutant_verdict.py SUITE_DIR"""
import re, sys
from pathlib import Path
suite = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(suite))
import tdm8_render_mutants as m  # noqa: E402
cpp = (suite / "sim_tdm8_render.cpp").read_text()
body = re.search(r"kLawPhases = \{([^}]*)\}", cpp).group(1)
k = tuple(int(x) for x in body.replace("\n", " ").split(",") if x.strip())
ok = True
def chk(name, cond):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + name)
chk(f"LAW_PHASES == kLawPhases ({len(k)} phases)", m.LAW_PHASES == k)
chk("18 settled names", len(m.LAW_SETTLED) == 18 and len(set(m.LAW_SETTLED)) == 18)
fails = "\n".join(f"  [FAIL] {n}" for n in m.LAW_SETTLED)
tail = "\n== tdm8_render: checks: 88   failures: 18 ==\nRESULT: FAIL\n"
chk("all 18 failed -> caught", m.verdict(1, fails + tail, m.LAW_SETTLED) == "caught")
miss = "\n".join(f"  [FAIL] {n}" for n in m.LAW_SETTLED if "+1302:" not in n)
v = m.verdict(1, miss + tail.replace("18 ==", "17 =="), m.LAW_SETTLED)
chk(f"17 of 18 failed -> not caught ({v[:60]})", v.startswith("failed, but not the named check") and "+1302:" in v)
# a +130 failure must not stand in for +1302 (prefix collision)
only130 = "  [FAIL] T30 INTERNAL LAW +130: the aligner held its settled report through the phase"
v = m.verdict(1, only130 + tail, ("T30 INTERNAL LAW +1302: the aligner held its settled report through the phase",))
chk("+130 does not satisfy +1302", v != "caught")
chk("string form still works", m.verdict(1, fails + tail, m.LAW_SETTLED[0]) == "caught")
arm = [x for x in m.MUTATIONS if x[0].startswith("A2-a removed")]
chk("A2-a arm present, --law-only, tuple target", len(arm) == 1 and arm[0][4] == "--law-only" and arm[0][5] == m.LAW_SETTLED)
sys.exit(0 if ok else 1)
