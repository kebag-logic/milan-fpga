#!/usr/bin/env bash
# camp.sh <campaign> <jobs> [driver args...]: one processor campaign in the campaign clone, through gate.sh, with the
# capped Verilator first on PATH and the drivers' scratch copies on disk (TMPDIR), not in the memory-backed /tmp
set -u
R=<runs>; C=$R/camp-clone; O=$R/camp; N=$1; J=$2; shift 2
export PATH=<tools>/vl-j4:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TMPDIR=$R/tmp
G=<tools>/gate.sh
case $N in
  aecp-dispatch) $G $O $N $C/tb/pp_top python3 -B aecp_dispatch_mutants.py --output $O/$N-out --jobs $J "$@" ;;
  aecp) $G $O $N $C/tb/pp_top python3 -B aecp_mutants.py --output $O/$N-out --jobs $J "$@" ;;
  d3) $G $O $N $C/tb/pp_top python3 -B d3_mutants.py --output $O/$N-out --jobs $J "$@" ;;
  notify) $G $O $N $C/tb/pp_top python3 -B notify_mutants.py --output $O/$N-out --jobs $J "$@" ;;
  ctr) $G $O $N $C/tb/pp_top python3 -B ctr_mutants.py --output $O/$N-out --jobs $J "$@" ;;
  gsi) $G $O $N $C/tb/pp_top python3 -B gsi_mutants.py --output $O/$N-out --jobs $J "$@" ;;
  acmp) $G $O $N $C/tb/pp_top python3 -B acmp_mutants.py --output $O/$N-out --jobs $J "$@" ;;
  name-wr) $G $O $N $C/tb/pp_top python3 -B name_wr_mutant.py --output $O/$N-out "$@" ;;
  elab-guards) $G $O $N $C/tb/elab_guards make mutants MUTANT_OUTPUT=$O/$N-out "$@" ;;
  aecp-cmds) $G $O $N $C/tb/aecp_cmds make mutants MUTANT_OUTPUT=$O/$N-out "$@" ;;
  adp-engine) $G $O $N $C/tb/adp_engine make mutants JOBS=$J MUTANT_OUTPUT=$O/$N-out "$@" ;;
  *) echo "unknown campaign $N"; exit 2 ;;
esac
touch $O/$N.done
