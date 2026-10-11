#!/usr/bin/env bash
# camp_table.sh: markdown table of every campaign, base and head, with the identity verdict
R=<scratch>/rec
declare -A CMD=(
 [d3]="python3 tb/pp_top/d3_mutants.py" [notify]="python3 tb/pp_top/notify_mutants.py"
 [srp_top]="python3 tb/srp_top/mutants.py" [acmp]="python3 tb/pp_top/acmp_mutants.py"
 [aecp]="python3 tb/pp_top/aecp_mutants.py" [aecp_dispatch]="python3 tb/pp_top/aecp_dispatch_mutants.py"
 [adp_engine]="python3 tb/adp_engine/mutants.py" [gsi]="python3 tb/pp_top/gsi_mutants.py"
 [maap]="python3 tb/maap/mutants.py" [ctr]="python3 tb/pp_top/ctr_mutants.py"
 [srp_admission]="python3 tb/srp_admission/mutants.py" [name_state]="python3 tb/name_state/mutants.py"
 [name_wr]="python3 tb/pp_top/name_wr_mutant.py" [desc_mem_guard]="python3 tb/desc_mem_guard/mutate.py"
 [nvm_figures]="make -C tb/nvm_port figures")
summ() { # the campaign's own closing verdict line
  local f=$1
  grep -hE 'KILLED by their named checks|detected by named checks|decode killed|detected=|figures agree|^[0-9]+ checks: [0-9]+ PASS' "$f" | tail -1 | sed 's/^ *//' | cut -c1-90
}
echo "| Campaign | Base | Head | Identity |"
echo "|---|---|---|---|"
for n in d3 notify srp_top acmp aecp aecp_dispatch adp_engine gsi maap ctr srp_admission name_state name_wr desc_mem_guard nvm_figures; do
  b=$R/base/camp_$n; h=$R/head/camp_$n
  hb="rc $(cat $b.rc), $(summ $b.log)"
  if [ -f $h.rc ]; then hh="rc $(cat $h.rc), $(summ $h.log)"; id=$(<scratch>/scripts/camp_compare.sh $n | sed "s/^$n: //"); else hh="PENDING"; id="PENDING"; fi
  [ "$n" = name_state ] && { hb="rc $(cat $b.rc), $(grep -c ': KILLED' $b.log) arms KILLED"; [ -f $h.rc ] && hh="rc $(cat $h.rc), $(grep -c ': KILLED' $h.log) arms KILLED"; }
  echo "| \`${CMD[$n]}\` | $hb | $hh | $id |"
done
