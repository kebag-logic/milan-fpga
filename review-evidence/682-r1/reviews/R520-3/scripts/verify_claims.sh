#!/usr/bin/env bash
# Mechanical checks of the round-3 CHANGELOG / SUBMODULES / recipe claims at
# the reviewed head. Prints one CHECK line per claim; exit 1 on any FAIL.
# Usage: verify_claims.sh <repo>
set -u
cd "$1" || exit 2
HEAD_EXP=fe8294978dd306706d659dc06468d0c07d43ce3e
R2=5428b044176f95248e6916dc00dd89c0df154078
BASE=e21c1ca024d37ea188ad15b5c8f9c2dae18628df
OLD=ead8036035affd53ef4b29979190f2f4f67084c0
NEW=2ad2f845dd583f8310075fa2380cb60a04fd091a
fail=0
check() { if eval "$2"; then echo "CHECK PASS $1"; else echo "CHECK FAIL $1"; fail=1; fi; }
G() { git -c core.quotepath=off "$@"; }
check "head is $HEAD_EXP" '[ "$(G rev-parse HEAD)" = $HEAD_EXP ]'
check "tree is 1d9982e2" '[ "$(G rev-parse HEAD^{tree})" = 1d9982e2943098fd1003e069dc7df8cc210d98ca ]'
check "only 3 Markdown files changed since round-2 head" \
  '[ "$(G diff --name-only $R2 HEAD | tr "\n" " ")" = "CHANGELOG.md docs/reference/SUBMODULES.md docs/testing/PP_SHADOW_BASELINE_RECIPE.md " ]'
check "manager commit touches only CHANGELOG.md and SUBMODULES.md" \
  '[ "$(G diff --name-only HEAD~1 HEAD | tr "\n" " ")" = "CHANGELOG.md docs/reference/SUBMODULES.md " ]'
check "no gitlink moved since round-2 head" '[ -z "$(G diff --raw $R2 HEAD | grep " 160000 ")" ]'
check "processor gitlink at $NEW" '[ "$(G ls-tree HEAD protocol-processor | awk "{print \$2, \$3}")" = "commit $NEW" ]'
check "base gitlink was $OLD" '[ "$(G ls-tree $BASE protocol-processor | awk "{print \$2, \$3}")" = "commit $OLD" ]'
check "VERSION unchanged vs base" 'G diff --quiet $BASE HEAD -- VERSION'
check "no firmware/capture/sw change vs base" '[ -z "$(G diff --name-only $BASE HEAD -- sw configs scripts/check_nvm_capture.py scripts/nvm_capture* 2>/dev/null)" ]'
PP=protocol-processor
merges="$(G -C $PP log --first-parent --format=%s $OLD..$NEW | sed -n "s/^Merge pull request #\([0-9]*\) .*/\1/p" | sort -n | tr "\n" " ")"
echo "INFO processor merges $OLD..$NEW: $merges"
check "processor PRs are exactly 156 159 160 161 162 164" '[ "$merges" = "156 159 160 161 162 164 " ]'
check "processor top byte-identical between pins" 'G -C $PP diff --quiet $OLD $NEW -- hdl/top/protocol_processor_top.sv'
check "processor ROM sources unchanged between pins" '[ -z "$(G -C $PP diff --name-only $OLD $NEW | grep -Ei "\.hex$|ucode|ltn_rom")" ]'
r_new="$(awk -F"\t" -v p=$NEW "\$1==p{print \$2\":\"\$3}" syn/yosys/rom_digests.tsv | sort | tr "\n" " ")"
r_old="$(awk -F"\t" -v p=$OLD "\$1==p{print \$2\":\"\$3}" syn/yosys/rom_digests.tsv | sort | tr "\n" " ")"
check "ROM ledger has two $NEW rows equal to the $OLD rows" '[ -n "$r_new" ] && [ "$r_new" = "$r_old" ] && [ "$(echo $r_new | wc -w)" = 2 ]'
check "xvlog budget: zero processor findings" 'grep -qx "# --- section submodules: 0 finding(s) (pinned processors) ---" scripts/xvlog.budget && ! grep -q "^protocol-processor:" scripts/xvlog.budget'
check "harness extension bounded by 2048 cycles" 'grep -q "c < cyc || (!cur.empty() && c < cyc + 2048)" tb/verilator/milan_dp/sim_nxn.cpp'
m156=21c6f7096ac80007f723de59c6f717f55bd34cfc
m157=$(G -C $PP log --first-parent --format="%H %s" 631eeb34..$OLD | sed -n "s/^\([0-9a-f]*\) Merge pull request #157 .*/\1/p")
check "PR 156 adds no synchronous-reset wording" '! G -C $PP diff $m156^1 $m156 | grep -Eiq "^\+.*(synchronous|asynchronous) (and active low|reset)|^\+.*\*\*synchronous"'
check "PR 157 ($m157) adds the synchronous-reset wording" 'G -C $PP diff $m157^1 $m157 | grep -q "^+5. Reset: one input, \`rst_n\`, \*\*synchronous and active low\*\*"'
check "PR 157 is in the earlier pin, not the new range" 'G -C $PP merge-base --is-ancestor $m157 $OLD'
check "CHANGELOG no longer credits synchronous reset to C11" '! sed -n "44,72p" CHANGELOG.md | grep -qi "synchronous reset"'
check "SUBMODULES C11 row no longer credits synchronous reset" '! grep "^| C11" docs/reference/SUBMODULES.md | grep -qi "synchronous reset"'
check "every baseline-F flow starts with the worker cap and keeps general.maxThreads 32" \
  'python3 -I -c "import json,sys;d=json.load(open(\"syn/ooc/pp_resource_baseline.json\"));sys.exit(0 if all(e[\"record\"][\"identity\"][\"flow\"][0]==\"set_param synth.maxThreads 1\" and \"set_param general.maxThreads 32\" in e[\"record\"][\"identity\"][\"flow\"] for e in d[\"endpoints\"].values()) and sorted(d[\"endpoints\"])==[\"ooc-1x1\",\"ooc-8x8\",\"route-1x1\"] else 1)"'
n="$(grep -c "pp_baseline.py \"\$WORK" docs/testing/PP_SHADOW_BASELINE_RECIPE.md)"
w="$(awk "/pp_baseline.py \"\\\$WORK/{s=1} s{buf=buf \$0} s&&!/\\\\\$/{print buf; buf=\"\"; s=0}" docs/testing/PP_SHADOW_BASELINE_RECIPE.md | grep -c -- --single-thread-synthesis)"
echo "INFO recipe measurement-preparation commands: $n; carrying --single-thread-synthesis: $w"
check "every recipe preparation command carries the flag" '[ "$n" = 5 ] && [ "$w" = 5 ]'
exit $fail
