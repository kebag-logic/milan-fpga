#!/usr/bin/env bash
# Extract the two sh fences of "Reproduce L11b core pricing" and execute the
# first (Tcl writer) in a clean environment (PATH=/usr/bin:/bin), once as
# printed and once with the leading command-proxy prefix removed (the words
# before `bash` on the first line). The second (Vivado) block is only parsed.
# The prefix token is reported as <proxy>. Usage: repro_block_probe.sh <repo> <workdir>
set -u
repo=$1; work=$2
rm -rf "$work"; mkdir -p "$work/asis" "$work/stripped"
page="$repo/docs/design/MARK_II_AREA_PLAN.md"
awk '/^### Reproduce L11b core pricing/{s=1} s&&/^```sh$/{f++; inb=1; next} s&&inb&&/^```$/{inb=0; next} s&&inb{print > (W "/block" f ".sh")}' W="$work" "$page"
grep -n -E '^### Reproduce L11b core pricing' "$page" | sed 's/^/heading at line /'
prefix=$(head -1 "$work/block1.sh" | sed -E 's/^(.*) bash -c .*/\1/')
tok=${prefix%% *}
echo "block1 first-line prefix words: $(echo "$prefix" | wc -w) (shown as <proxy> ...)"
echo "block2 first line starts with the same prefix: $(head -1 "$work/block2.sh" | grep -c "^$prefix ")"
for b in 1 2; do printf 'block%s bytes=%s sha256=%s\n' $b "$(wc -c < "$work/block$b.sh")" "$(sha256sum < "$work/block$b.sh" | cut -c1-64)"; done
for b in 1 2; do bash -n "$work/block$b.sh"; echo "parse block$b rc=$?"; done
env -i PATH=/usr/bin:/bin WORK="$work/asis" bash "$work/block1.sh" > "$work/asis.out" 2>&1; r=$?
echo "block1 as printed, clean PATH: rc=$r"; sed -e "s#$work#WORK#g" -e "s#$tok#<proxy>#g" "$work/asis.out"
test -e "$work/asis/price_core.tcl" && echo "tcl written (as printed)" || echo "no tcl written (as printed)"
sed "1s#^$prefix ##" "$work/block1.sh" > "$work/block1_stripped.sh"
env -i PATH=/usr/bin:/bin WORK="$work/stripped" bash "$work/block1_stripped.sh"; echo "block1 without prefix, clean PATH: rc=$?"
test -s "$work/stripped/price_core.tcl" && echo "tcl written (without prefix): $(wc -c < "$work/stripped/price_core.tcl") bytes sha256=$(sha256sum < "$work/stripped/price_core.tcl" | cut -c1-64)"
if command -v tclsh >/dev/null; then
  echo 'set f [open [lindex $argv 0]]; set s [read $f]; puts "tcl info complete: [info complete $s]"' > "$work/complete.tcl"
  tclsh "$work/complete.tcl" "$work/stripped/price_core.tcl"
else echo "tclsh absent; Tcl completeness not checked"; fi
