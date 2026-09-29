#!/usr/bin/env python3
"""Cross-page consistency of the PR's pages with the pages dev landed (PR #620,
B1) at the candidate head. Run from the repository root."""
import hashlib, re, subprocess, sys
def show(rev, p): return subprocess.run(["git", "show", f"{rev}:{p}"], check=True, capture_output=True).stdout
H = "61752396"
p606 = show(H, "docs/findings/606_FIRST_BIND_MEASUREMENT.md").decode()
p608 = show(H, "docs/findings/608_75_WITHDRAWAL_AND_RESTART.md").decode()
p599 = show(H, "docs/findings/599_394_E1_LINK_CYCLES.md").decode()
p387 = show(H, "docs/findings/387_SOFTWARE_GM_STEP.md").decode()
ok = True
def both(tok, *pages):
    global ok
    r = all(tok in p for p in pages); print(f"{'OK ' if r else 'BAD'} {tok}"); ok &= r
for tok in ("0x00020060", "acad92b9", "d84bce7b", "93742dd2", "bf44ccc9", "809fcffa",
            "690d87e407bbb7f7bba52bbe7a7e0dc85cd264df2db5eec87bfaf85f99bda24b",
            "6597f7a601ddb3dbba1bf058c38716277e8feb1147fb89edcf1d39e755dc369f",
            "9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404",
            "7723d0b8129df7b77b3b49980366f18c91adb15f8c38526f48a5ebd32d1207a2",
            "13eda870d1a6cf3f946fc228a98862366b08d102"):
    both(tok, p606, p599)
# B1 final saved-state row equals B2 start and end rows
b1 = re.findall(r"^\| (NVM slots A / B, image sequence|Commits ok / failed|`PP_STAT`, `nvm_pend` \(bit 11\)|`PP_NVM_STAT`) \| [^|]+\| ([^|]+)\|$", p599, re.M)
b2 = re.findall(r"^\| (NVM slots A / B, image sequence|Commits ok / failed|`PP_STAT`, `nvm_pend` \(bit 11\)|`PP_NVM_STAT`) \| ([^|]+)\| ([^|]+)\|$", p606, re.M)
b2_608 = re.findall(r"^\| (NVM slots A / B, image sequence|Commits ok / failed|`PP_STAT`, `nvm_pend` \(bit 11\)|`PP_NVM_STAT`) \| ([^|]+)\| ([^|]+)\|$", p608, re.M)
b1_387 = re.findall(r"^\| (NVM slots A / B, image sequence|Commits ok / failed|`PP_STAT`, `nvm_pend` \(bit 11\)|`PP_NVM_STAT`) \| [^|]+\| ([^|]+)\|$", p387, re.M)
print("B1 599 final:", b1); print("B1 387 final:", b1_387)
for k, s, e in b2:
    fin = dict(b1)[k].strip()
    r = s.strip() == e.strip() == fin; print(f"{'OK ' if r else 'BAD'} 606 {k}: start={s.strip()} end={e.strip()} B1final={fin}"); ok &= r
r = [(k, s.strip(), e.strip()) for k, s, e in b2] == [(k, s.strip(), e.strip()) for k, s, e in b2_608]; print("606 and 608 saved-state tables equal:", r); ok &= r
r = [(k, v.strip()) for k, v in b1] == [(k, v.strip()) for k, v in b1_387]; print("599 and 387 final rows equal:", r); ok &= r
# counters: B1 end LINK_UP/DOWN 12/11; GPTP_GM_CHANGED 22 after 599, 387 edges 9x3+1x1 = 28
both("12 / 11", p599); both("LINK_UP 12, LINK_DOWN 11 and GPTP_GM_CHANGED 50", p608)
both("rose by 3 at nine edges and by 1 at one", p387)
print("22 + 9*3 + 1 =", 22 + 27 + 1)
ok &= 22 + 27 + 1 == 50
# outlets and peer configuration
both("OUT1 and OUT3 OFF, the other five ON", p599); both("configuration 1 at 48 kHz", p599, p606)
both("They set a sticky pending source that only a reset clears", p387)
both("SET_CLOCK_SOURCE writes, whose sticky level only a DUT reset clears", p606)
# UART grader hash at 13eda870 and at the candidate
for rev in ("13eda870", H):
    h = hashlib.sha256(show(rev, "scripts/baremetal_uart_smoke.py")).hexdigest()
    r = h == "bc41ab03e64198b10a517124f960b9b59b77d7143661f728fe5666314e433886"; print(f"{'OK ' if r else 'BAD'} uart smoke {rev} {h}"); ok &= r
print("RESULT", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
