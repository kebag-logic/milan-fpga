#!/bin/sh
# Disposable placement probe of S5's one-epoch record check (issue #202).
# usage: probe_s5_boundary.sh <clone> <work-dir> <verilator> <variant>
#   variant: plant      - RTL age-1 overwrite plant, suite as committed
#            plant-pre  - same plant, src5's second move 1 ms BEFORE the
#                         epoch boundary instead of 1 ms after it
#            golden-pre - committed RTL, src5's second move 1 ms before it
# Copies hdl/ tb/common/ tb/acmp_talker/ into <work-dir>/<variant>, edits
# the copy only, builds and runs; writes <variant>.log and <variant>.rc
# next to the copy. The clone is never written.
set -u
clone=$1; work=$2; vl=$3; v=$4
t=$work/$v
rm -rf "$t"; mkdir -p "$t/tb"
cp -r "$clone/hdl" "$t/hdl"
cp -r "$clone/tb/common" "$clone/tb/acmp_talker" "$t/tb/"
rm -rf "$t/tb/acmp_talker/obj_dir"
rtl=$t/hdl/acmp/KL_acmp_talker.sv
tb=$t/tb/acmp_talker/sid_cases.hpp
old_rtl='                               && (sid_rec_age_r[ev_src_r] != 2'"'"'d2))) begin'
new_rtl='                               && (sid_rec_age_r[ev_src_r] == 2'"'"'d0))) begin'
old_tb='      count_to(h, end + Q_MS + 1); now = h.d->now_ms_i;'
new_tb='      count_to(h, end + Q_MS - 1); now = h.d->now_ms_i;'
edit() { # file old new: exactly one occurrence, else refuse
  python3 -I -c '
import sys
p, o, n = sys.argv[1:4]
s = open(p).read()
if s.count(o) != 1:
    sys.exit("refused: %s occurs %d times" % (p, s.count(o)))
open(p, "w").write(s.replace(o, n, 1))' "$1" "$2" "$3"
}
case $v in
  plant)      edit "$rtl" "$old_rtl" "$new_rtl" || exit 9 ;;
  plant-pre)  edit "$rtl" "$old_rtl" "$new_rtl" && edit "$tb" "$old_tb" "$new_tb" || exit 9 ;;
  golden-pre) edit "$tb" "$old_tb" "$new_tb" || exit 9 ;;
  *) echo "unknown variant $v"; exit 9 ;;
esac
( cd "$t/tb/acmp_talker" && make VERILATOR="$vl" run ) > "$work/$v.log" 2>&1
rc=$?
echo $rc > "$work/$v.rc"
exit $rc
