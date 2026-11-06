#!/bin/sh
# Usage: pp_top_staged.sh <tb/pp_top dir> <receipts dir> <tag> <verilator> build|sims|shards
# Reproduces tb/pp_top "make run" in stages short enough for one bounded
# foreground call each. build: every guard and all seven Verilator builds, the
# commands taken from "make -n run" minus the simulations. sims: the six
# single-section builds' simulations, as the recipe runs them. shards: the
# default build's sections, each run alone through the binary's own
# --<section>-only flags, at most PAR (default 16) at a time; the default run's section set
# is the union of these flags (the --aecp-dispatch-only shard also runs the
# dispatch focus the default build does not).
D=$1; R=$2; T=$3; V=$4; ST=$5
cd "$D" || exit 2
case $ST in
build)
  make -n run VERILATOR="$V" 2>/dev/null \
    | grep -v -e '^\./obj_' -e '^make' -e "^$(command -v make) " -e '^/usr/bin/make' > "$R/pp_top-$T.build-steps.sh"
  # drop the final awk tally (its continuation line too): it needs all seven runs
  sed -i '/^awk /,$d' "$R/pp_top-$T.build-steps.sh"
  sh -e "$R/pp_top-$T.build-steps.sh" > "$R/pp_top-$T.build.log" 2>&1; echo $? > "$R/pp_top-$T.build.rc" ;;
sims)
  rc=0
  for b in obj_vid/Vpp_top_vid obj_idn/Vpp_top_idn obj_line/Vpp_top_line obj_tim/Vpp_top_tim obj_tdf/Vpp_top_tdf obj_if2/Vpp_top_if2; do
    n=$(basename $b); mkdir -p obj_dir
    ./$b > "$R/pp_top-$T.$n.log" 2>&1; r=$?; echo $r > "$R/pp_top-$T.$n.rc"; [ $r -eq 0 ] || rc=1
  done
  echo $rc > "$R/pp_top-$T.sims.rc" ;;
shards)
  for f in arm-queue gsi-internal name-writes d3 volatile cuts acmp adp reboot aecp-dispatch deadline hazards identify notify spacing domain-notify withdraw counters tspec; do echo $f; done \
    | xargs -P "${PAR:-16}" -I{} sh -c 'timeout 560 ./obj_dir/Vpp_top_sim --{}-only > "$1/pp_top-$2.shard-{}.log" 2>&1; echo $? > "$1/pp_top-$2.shard-{}.rc"' _ "$R" "$T" ;;
esac
