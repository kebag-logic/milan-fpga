#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# lockstep_suites.sh CLONE PACKET_DIR
# Runs the committed tb/srp_top and tb/pp_top suites of the head with the
# base-vs-head lockstep checker bound into every KL_srp_top instance. The
# suites themselves are not edited: a scratch tree from `git archive` of the
# head gets hdl/lockstep/ (the generated checker and the base modules renamed
# _ref) and two Makefile lines appending them to SRCS. pp_top's `run` target
# loses only its two compile-refusal preflights (fixture-guards,
# line-guards), which compile the source list and are disturbed by the extra
# files; they do not exercise SRP.
set -eu
CLONE=$1; P=$2; S=$P/scratch
HEAD=65324390d1b83c4587f299d06597f7a571d7fa61; BASE=c4cb84ff8cecad19bedaa85dde594a8ed68012f6
mkdir -p "$S/head" "$S/base" "$S/lstree"
git -C "$CLONE" archive $HEAD | tar -x -C "$S/head"
git -C "$CLONE" archive $BASE | tar -x -C "$S/base"
python3 "$P/scripts/gen_lockstep.py" "$S/base/hdl" "$S/head/hdl" "$S/ls"
git -C "$CLONE" archive $HEAD | tar -x -C "$S/lstree"
mkdir -p "$S/lstree/hdl/lockstep/ref"
cp "$S"/ls/ref/*.sv "$S/lstree/hdl/lockstep/ref/"
cp "$S/ls/lockstep_chk.sv" "$S/ls/lockstep_bind.sv" "$S/lstree/hdl/lockstep/"
for mk in tb/srp_top/Makefile tb/pp_top/Makefile; do
  python3 - "$S/lstree/$mk" <<'EOF'
import sys
p = sys.argv[1]; s = open(p).read()
i = s.index('\nSRCS'); j = s.index('\n\n', i)
s = s[:j] + ('\nLS_SRCS = $(wildcard $(HDL)/lockstep/ref/*.sv) '
             '$(HDL)/lockstep/lockstep_chk.sv $(HDL)/lockstep/lockstep_bind.sv\n'
             'SRCS += $(LS_SRCS)\n') + s[j:]
open(p, 'w').write(s)
EOF
done
sed -i 's/^run: fixture-guards line-guards ltn_rom.hex ucode.hex/run: ltn_rom.hex ucode.hex/' "$S/lstree/tb/pp_top/Makefile"
(cd "$S/lstree/tb/srp_top" && make run > ls_run.log 2>&1; echo $? > ls_run.rc)
(cd "$S/lstree/tb/pp_top" && make run > ls_run.log 2>&1; echo $? > ls_run.rc)
grep -h "LOCKSTEP SUMMARY\|checks:" "$S"/lstree/tb/{srp_top,pp_top}/ls_run.log
