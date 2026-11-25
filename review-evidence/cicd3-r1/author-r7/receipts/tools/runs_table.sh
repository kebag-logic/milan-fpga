#!/bin/bash
# runs_table.sh: every direct run of r7 (rounds q, m, l) as one row: tree, base, gPTP pin, round, case, CPUs, wall,
# rc, the whole output's sha256 (stdout then stderr, the receipt's form), the [#207] line and the tally.
R=/data-2/milan/tmp/cicd-a839/r7
printf '%-4s %-9s %-9s %-9s %-5s %-9s %-5s %8s %-4s %-16s %-28s %s\n' tree base head pin round case cpus wall rc output_sha256 '[#207] rp/wp' tally
for t in B0 H0 O0 B1 H1 O1; do
  case $t in *0) base=2509db68;; *1) base=e608f8d8;; esac
  case $t in B*) hd=base;; H*) hd=9c625393;; O*) hd=45d5c35a;; esac; pin=$(git -C $R/wt/$t rev-parse HEAD:gptp-processor | cut -c1-8)
  for g in q m l; do for k in gptp gptp-lat; do
    f=$R/meas/$t/$g-$k; [ -e "$f.time" ] || continue
    if [ -e "$f.out" ]; then o=$(cat "$f.out"); else o=$(cat "$f.stdout" "$f.stderr"); fi
    sha=$( { if [ -e "$f.out" ]; then cat "$f.out"; else cat "$f.stdout" "$f.stderr"; fi; } | sha256sum | cut -c1-16)
    cpus=$(grep -m1 " $g $k cpus=" <(grep "^$t " $R/meas/progress) | sed 's/.*cpus=\([^:]*\):.*/\1/')
    l=$(printf '%s\n' "$o" | grep -m1 '^\[#207\]' | sed 's/.*rp \([0-9]*->[0-9]*\), wp \([0-9]*->[0-9]*\)/rp \1, wp \2/')
    printf '%-4s %-9s %-9s %-9s %-5s %-9s %-5s %8s %-4s %-16s %-28s %s\n' $t $base $hd $pin $g $k "$cpus" "$(awk 'NR==1{print $1}' $f.time)" \
      "$(tail -1 $f.time)" $sha "$l" "$(printf '%s\n' "$o" | grep -m1 -E '^[0-9]+ checks')"
  done; done
done
