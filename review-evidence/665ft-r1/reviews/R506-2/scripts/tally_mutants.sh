#!/bin/sh
# Probe (R506-1): plant defects into a COPY of the tally listener
# (sw/firmware/gtest/fw_gtest_main.cpp) and require tally_selftest.py to fail.
# Usage: tally_mutants.sh <repo checkout> <work dir>
set -u
REPO=$1; W=$2
plant() {  # name, perl substitution
  d="$W/$1"; rm -rf "$d"; mkdir -p "$d/sw/firmware" "$d/scripts"
  cp -r "$REPO/sw/firmware/gtest" "$d/sw/firmware/"; cp "$REPO/scripts/suite_tally.py" "$REPO/scripts/suite_tally_selftest.py" "$d/scripts/" 2>/dev/null
  perl -0pi -e "$2" "$d/sw/firmware/gtest/fw_gtest_main.cpp"
  if cmp -s "$d/sw/firmware/gtest/fw_gtest_main.cpp" "$REPO/sw/firmware/gtest/fw_gtest_main.cpp"; then echo "$1: PLANT DID NOT APPLY"; return; fi
  out=$(python3 "$d/sw/firmware/gtest/tally_selftest.py" 2>&1); rc=$?
  echo "$1: selftest exit $rc ($( [ $rc -ne 0 ] && echo caught || echo SURVIVED )); $(echo "$out" | grep -c '^\[FAIL\]') case(s) not as planted"
}
plant skip-not-counted 's/info\.result\(\)->Failed\(\) \|\| info\.result\(\)->Skipped\(\)/info.result()->Failed()/'
plant no-atexit 's/static_cast<void>\(std::atexit\(on_exit_early\)\);//'
plant no-signal-handler 's/static_cast<void>\(std::signal\(sig, on_fatal_signal\)\);/static_cast<void>(sig);/'
plant disabled-not-counted 's/failures \+= report_disabled\(unit\);//'
plant setup-failure-not-counted 's/failures\+\+;\n            \}\n        \}/}\n        }/'
plant crash-tally-passes 's/put_tally\(state\.checks \+ 1u, state\.failures \+ 1u\);\n    \}\n    static_cast/put_tally(state.checks + 1u, state.failures);\n    }\n    static_cast/'
plant disabled-not-counted-v2 's/    return disabled;\n\}/    return disabled * 0u;\n}/'
# the tally line a surviving mutant prints for the planted skip
d="$W/skip-not-counted"; b=$(mktemp -d "$W/show.XXXX")
python3 - "$d" "$b" <<'PY'
import sys; from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "sw/firmware/gtest"))
import tally_selftest as t, fw_gtest
exe = t.build(Path(sys.argv[2]))
res = fw_gtest.run([str(exe), "--gtest_filter=Skip.*"], timeout=60)
print("skip-not-counted, the planted skip's log tail:")
print("\n".join(("    " + l) for l in res.stdout.strip().splitlines()[-4:]))
print("    grade:", fw_gtest.grade(res.returncode, res.stdout + res.stderr))
PY
