#!/usr/bin/env python3
"""Show the controller library's only STREAM_INPUT counters check at the tag the
probe was built against (public source), and evaluate its condition on the pairs
that matter for #653. usage: library_check.py <library_source_checkout>"""
import re, subprocess, sys
from pathlib import Path
src = Path(sys.argv[1]); f = src / "src/controller/avdeccControllerImpl.cpp"
rev = subprocess.run(["git", "-C", str(src), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
tag = subprocess.run(["git", "-C", str(src), "describe", "--tags", "--exact-match"], capture_output=True, text=True).stdout.strip()
lines = f.read_text().splitlines()
i = next(n for n, l in enumerate(lines) if "Invalid MEDIA_LOCKED / MEDIA_UNLOCKED counters value on STREAM_INPUT" in l)
print(f"library tag {tag} commit {rev}; src/controller/avdeccControllerImpl.cpp:{i-13}-{i+1}")
print("\n".join(f"{n+1}: {lines[n]}" for n in range(i - 14, i + 1)))
cond = lines[i - 2].strip()
assert cond == "if (lockedValue != unlockedValue && lockedValue != (unlockedValue + 1))", cond
hits = subprocess.run(["grep", "-rn", "--include=*.cpp", "--include=*.hpp", "MediaUnlocked", str(src / "src"), str(src / "include")], capture_output=True, text=True).stdout
print("all MediaUnlocked uses in src/ and include/:\n" + "\n".join(l.replace(str(src) + "/", "") [:160] for l in hits.splitlines()))
flag = lambda ml, mu: ml != mu and ml != mu + 1
for ml, mu, what in ((1, 0, "locked, or the pre-#655 CRF window after an unbind"), (1, 1, "after the unlock, whether the push precedes or follows the response"), (2, 0, "a genuinely invalid pair")):
    print(f"pair {ml}/{mu} ({what}): library flags = {flag(ml, mu)}; connection state is not an input")
