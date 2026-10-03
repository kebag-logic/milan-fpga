#!/usr/bin/env bash
# Read-only static checks over the review clone ($1, default: current dir) at the exact head
set -uo pipefail
cd "${1:-.}" || exit 2
H=e2c7d97d158a30e44289a06a33f8ff4c5e289b87; B=c74711d45a8bbc0d6b38cb49211b26a4a6413e88; L=751e1c0a940d9fe9c242caa9f2233d451b29c447
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
echo "gitlinks (mode 160000): $(git ls-files -s | awk '$1==160000' | wc -l)"
MB=$(git merge-base $L $B); echo "merge-base $MB"
echo "== (6) merge keeps both sides of the two shared READMEs"
for f in tb/pp_top/README.md tb/adp_engine/README.md; do
  a=$(diff <(git diff -U0 $L $H -- $f | grep '^[-+][^-+]') <(git diff -U0 $MB $B -- $f | grep '^[-+][^-+]') >/dev/null && echo same || echo DIFFER)
  b=$(diff <(git diff -U0 $B $H -- $f | grep '^[-+][^-+]') <(git diff -U0 $MB $L -- $f | grep '^[-+][^-+]') >/dev/null && echo same || echo DIFFER)
  echo "$f main-side-hunks:$a lane-side-hunks:$b"
done
echo "files changed on both sides: $(comm -12 <(git diff --name-only $MB $B|sort) <(git diff --name-only $MB $L|sort) | tr '\n' ' ')"
echo "== (3) removed tick: readers at base, references at head"
git grep -n "gm_changed_tick\|adp_gm_tick" $B -- . | sed 's/^/base: /'
git grep -n "gm_changed_tick\|adp_gm_tick" $H -- . | sed "s/^/head: /"
echo "== (4) 02 and the docs: removed adapter op/event names"
for w in READ_AS_PATH INPUT_CONFIGURE INPUT_ENABLE INPUT_DISABLE INPUT_START INPUT_STOP OUTPUT_SET_PT_OFFSET OUTPUT_STATUS GET_MCR_DEFAULTS MC_LOCKED AS_CAPABLE_CHANGE PATH_CHANGE; do
  printf '%s 02:%s all-docs:%s\n' $w "$(grep -c "$w" docs/architecture/02_interfaces.md)" "$(grep -rn "$w" docs | wc -l)"; done
grep -rnE "avtp\.[A-Z_]+|srp \+ avtp adapters|gptp · avtp · mclk adapters|srp\+avtp adapters" docs hdl | cut -c1-200
echo "== (1) face wiring at head"
grep -n "assign ctr_desc_index_o\|assign ctr_desc_type_o\|assign ctr_word_o" hdl/aecp/KL_aecp_engine.sv
grep -n "ev_ctr_index_i == 16'd0" hdl/aecp/KL_aecp_notify.sv
grep -n ">= 32'd1000" hdl/aecp/KL_aecp_notify.sv
