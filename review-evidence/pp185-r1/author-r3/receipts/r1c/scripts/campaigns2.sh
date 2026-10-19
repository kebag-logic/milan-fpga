#!/usr/bin/env bash
# usage: campaigns2.sh <root> <record-dir> <name...>   the named campaigns, serially, unpiped,
# through gate.sh; each output directory is fresh and outside the tree
root="$1"; rec="$2"; shift 2; mkdir -p "$rec"
G=$VALIDATION_STORAGE/pp185-a647/scripts/gate.sh
export PYTHONDONTWRITEBYTECODE=1 TMPDIR=$VALIDATION_STORAGE/pp185-a647/tmpdir
out="$rec/out"; mkdir -p "$out"
c() { local name="$1" dir="$2"; shift 2; rm -rf "$out/$name"
      "$G" "$rec" "$name" "$root/$dir" "$@" --output "$out/$name"; }
git -C "$root" rev-parse HEAD > "$rec/HEAD-$1.txt"
for n in "$@"; do case "$n" in
  aecp_dispatch) c aecp_dispatch tb/pp_top python3 aecp_dispatch_mutants.py --jobs 2 ;;
  notify) c notify tb/pp_top python3 notify_mutants.py --jobs 2 ;;
  aecp_cmds) c aecp_cmds tb/aecp_cmds python3 -B mutants.py --jobs 2 ;;
  aecp) c aecp tb/pp_top python3 aecp_mutants.py --jobs 2 ;;
  ctr) c ctr tb/pp_top python3 ctr_mutants.py --jobs 2 ;;
  gsi) c gsi tb/pp_top python3 gsi_mutants.py --jobs 2 ;;
  name_wr) c name_wr tb/pp_top python3 name_wr_mutant.py ;;
  name_state) c name_state tb/name_state python3 mutants.py --jobs 2 ;;
  maap) c maap tb/maap python3 mutants.py --jobs 2 ;;
  adp) c adp tb/adp_engine python3 mutants.py --jobs 2 ;;
  acmp) c acmp tb/pp_top python3 acmp_mutants.py --jobs 2 ;;
  elab_guards) c elab_guards tb/elab_guards python3 -B mutants.py --jobs 2 ;;
  d3) c d3 tb/pp_top python3 d3_mutants.py --jobs 3 ;;
  *) echo "unknown campaign $n"; exit 2 ;;
esac; done
echo ALL-DONE > "$rec/done-$1"
