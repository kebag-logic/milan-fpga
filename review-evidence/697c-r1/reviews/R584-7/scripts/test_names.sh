#!/bin/sh
# usage: test_names.sh <milan-fpga repo> <base rev> <head rev>
# Lists TEST/TEST_F/TEST_P names (Suite.Name) compiled into the core arms before and after the move:
# base: sw/firmware/ctrl/test/{test_adp,test_acmp,test_adp_reentry,test_maap,test_maap_debug}.cpp
# head: the same milan files that remain plus third_party/tsn-c-stack/tests/ at the recorded gitlink.
set -eu
R=$1; B=$2; H=$3
ext() { grep -hoE '^\s*TEST(_F|_P)?\(\s*[A-Za-z0-9_]+\s*,\s*[A-Za-z0-9_]+' | sed -E 's/.*\(\s*([A-Za-z0-9_]+)\s*,\s*([A-Za-z0-9_]+)/\1.\2/' | sort; }
for f in test_adp test_acmp test_adp_reentry test_maap test_maap_debug; do git -C "$R" show "$B:sw/firmware/ctrl/test/$f.cpp" 2>/dev/null; done | ext > /tmp/tn_base.$$
pin=$(git -C "$R" ls-tree "$H" third_party/tsn-c-stack | awk '{print $3}')
{ for f in test_adp test_maap; do git -C "$R" show "$H:sw/firmware/ctrl/test/$f.cpp"; done
  for f in test_adp test_acmp test_adp_reentry test_maap test_maap_debug; do git -C "$R/third_party/tsn-c-stack" show "$pin:tests/$f.cpp"; done; } | ext > /tmp/tn_head.$$
echo "base tests: $(wc -l < /tmp/tn_base.$$)  head tests: $(wc -l < /tmp/tn_head.$$)  duplicates head: $(uniq -d /tmp/tn_head.$$ | wc -l)"
echo "in base, not head:"; comm -23 /tmp/tn_base.$$ /tmp/tn_head.$$
echo "in head, not base:"; comm -13 /tmp/tn_base.$$ /tmp/tn_head.$$
rm -f /tmp/tn_base.$$ /tmp/tn_head.$$
