#!/usr/bin/env bash
# chain.sh <runs> <clone> <jobs> <name>...: run the named campaigns one after another in <clone>, each with its
# cmd/log/rc/start/end under <runs>, the pinned Verilator (build parallelism capped) first on PATH and TMPDIR on
# disk. Every campaign runs whatever the previous one's rc.
R=$1; C=$2; J=$3; shift 3
export PATH=<tools>/vl-cap:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VL_BUILD_J=4 TMPDIR=<tmp>/camp
mkdir -p $R $TMPDIR
for n in "$@"; do
  d=tb/pp_top
  case $n in
    srp) d=.; cmd=(python3 -B tb/srp_top/mutants.py --output $R/camp-srp-out --jobs $J) ;;
    acmp) cmd=(python3 -B acmp_mutants.py --output $R/camp-acmp-out --jobs $J) ;;
    aecp) cmd=(python3 -B aecp_mutants.py --output $R/camp-aecp-out --jobs $J) ;;
    gsi) cmd=(python3 -B gsi_mutants.py --output $R/camp-gsi-out --jobs $J) ;;
    ctr) cmd=(python3 -B ctr_mutants.py --output $R/camp-ctr-out --jobs $J) ;;
    name-wr) cmd=(python3 -B name_wr_mutant.py --output $R/camp-name-wr-out) ;;
    aecp-dispatch) cmd=(python3 -B aecp_dispatch_mutants.py --output $R/camp-aecp-dispatch-out --jobs $J) ;;
    notify) cmd=(python3 -B notify_mutants.py --output $R/camp-notify-out --jobs $J) ;;
    d3) cmd=(python3 -B d3_mutants.py --output $R/camp-d3-out --jobs $J) ;;
  esac
  echo "(cd $d) ${cmd[*]}" > $R/camp-$n.cmd
  date +%s > $R/camp-$n.start
  (cd $C/$d && "${cmd[@]}") > $R/camp-$n.log 2>&1
  echo $? > $R/camp-$n.rc
  date +%s > $R/camp-$n.end
done
