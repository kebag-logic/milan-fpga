#!/bin/sh
# Remove the build outputs this review's runs created in the clone, then
# prove the clone is at the exact head with tracked bytes, modes, index and
# submodule gitlinks unchanged. Usage: clone_integrity.sh <clone>
set -u
C=$1
HEAD_EXP=354f781828d8b4d73037129f297b072320a10f9c
TREE_EXP=27d0094ad4a11b5d2fe55091b6ae93d9f1f70237
cd "$C" || exit 2
# outputs of make in the suites this review ran (all git-ignored)
for d in gptp_tables gptp_shadow gptp_txts gptp_plane; do
  rm -rf "tb/verilator/$d/obj_dir" "tb/verilator/$d/gptp_ucode.hex" "tb/verilator/$d/__pycache__"
done
rm -rf scripts/__pycache__ syn/ooc/__pycache__
rm -rf gptp-processor/tb/__pycache__ gptp-processor/tb/verilator/engine/obj_dir \
       gptp-processor/tb/verilator/engine/seedrun gptp-processor/tb/verilator/engine/syncseedrun \
       gptp-processor/tb/verilator/parser/obj_dir gptp-processor/tb/verilator/ucpu/obj_dir \
       gptp-processor/bench/arty/obj_dir gptp-processor/tb/tsngen/obj_dir \
       gptp-processor/tb/verilator/gaskets/obj_dir
fail=0
say() { printf '%s\n' "$*"; }
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}')
say "HEAD $h"; say "TREE $t"
[ "$h" = "$HEAD_EXP" ] || fail=1
[ "$t" = "$TREE_EXP" ] || fail=1
git diff --quiet HEAD -- || { say "worktree differs from HEAD"; fail=1; }
git diff --cached --quiet || { say "index differs from HEAD"; fail=1; }
# index entries (mode, blob, path) equal the HEAD tree's
git ls-files -s | awk '{print $1, $2, $4}' | sort > /tmp/r593_idx.$$
git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sort > /tmp/r593_tree.$$
if cmp -s /tmp/r593_idx.$$ /tmp/r593_tree.$$; then say "index modes/blobs == HEAD tree ($(wc -l < /tmp/r593_tree.$$) entries)"; else say "index modes/blobs DIFFER"; fail=1; fi
rm -f /tmp/r593_idx.$$ /tmp/r593_tree.$$
# every tracked regular file's bytes hash to its HEAD blob
bad=$(git ls-tree -r HEAD | awk '$1!="160000"{print $3" "$4}' | while read -r b p; do
  [ "$(git hash-object -- "$p")" = "$b" ] || echo "$p"; done | wc -l)
say "tracked files whose bytes differ from HEAD blob: $bad"; [ "$bad" -eq 0 ] || fail=1
st=$(git status --porcelain --ignored | wc -l)
say "status entries (including ignored): $st"; [ "$st" -eq 0 ] || { git status --porcelain --ignored; fail=1; }
say "gitlinks at HEAD:"; git ls-tree HEAD gptp-processor protocol-processor third_party/verilog-axis third_party/lwSRP external
say "submodule status:"; git submodule status
g=$(git -C gptp-processor rev-parse HEAD)
[ "$g" = 18dd997b2459699e41e5ce9bceca1181e41fa5fe ] || { say "gptp-processor at $g"; fail=1; }
gs=$(git -C gptp-processor status --porcelain --ignored | wc -l)
say "gptp-processor status entries (including ignored): $gs"; [ "$gs" -eq 0 ] || { git -C gptp-processor status --porcelain --ignored; fail=1; }
for s in protocol-processor third_party/verilog-axis; do
  n=$(git -C "$s" status --porcelain | wc -l); say "$s status entries: $n"; [ "$n" -eq 0 ] || fail=1
done
say "INTEGRITY $( [ $fail -eq 0 ] && echo PASS || echo FAIL )"
exit $fail
