#!/bin/sh
# Focused suites at the exact head, in a disposable export (never the clone).
# Steps: export | mga-build | mga-run | chmap
# Usage: 20_suites.sh <clone> <scratch-dir> <step>   (VERILATOR must be set)
# The only edit to the export is the Verilator build parallelism, capped at 8
# jobs (the Makefiles ask for -j 0 = every core); nothing else is touched.
set -eu
clone=$1
scratch=$2
step=$3
: "${VERILATOR:?set VERILATOR to the pinned 5.050 binary}"
HEAD_SHA=2accfadfd3d4d8a318e3e714ee0dc87fc84e4164
exp="$scratch/head"
case "$step" in
  export)
    rm -rf "$exp"; mkdir -p "$exp"
    git -C "$clone" archive "$HEAD_SHA" hdl tb | tar -x -C "$exp"
    for mk in tb/verilator/media_grid_align/Makefile tb/verilator/chmap_capture/Makefile; do
      git -C "$clone" show "$HEAD_SHA:$mk" | cmp -s - "$exp/$mk" && echo "export $mk: head bytes"
      sed -i 's/--build -j 0/--build -j 8/' "$exp/$mk"
      echo "  capped: $(grep -c -- '--build -j 8' "$exp/$mk") build line(s) now -j 8"
    done
    # every exported file under hdl/ and tb/ must equal its head blob, bar the two Makefiles
    n=0; bad=0
    for f in $(git -C "$clone" ls-tree -r --name-only "$HEAD_SHA" hdl tb); do
      case "$f" in tb/verilator/media_grid_align/Makefile|tb/verilator/chmap_capture/Makefile) continue;; esac
      n=$((n+1))
      [ "$(git -C "$clone" rev-parse "$HEAD_SHA:$f")" = "$(git hash-object --no-filters "$exp/$f")" ] || { bad=$((bad+1)); echo "  MISMATCH $f"; }
    done
    echo "export check: $n files compared, $bad mismatches"
    ;;
  mga-build)
    cd "$exp/tb/verilator/media_grid_align"
    make clean >/dev/null
    # the Makefile's 'run' recipe builds all four binaries, then runs them;
    # build only, by running every recipe line up to the first run line
    make -n run VERILATOR="$VERILATOR" | sed '/^\.\/obj_dir\/Vmedia_grid_align_sim$/,$d' | grep -v '^echo ' > build_only.sh
    sh -e build_only.sh > build.log 2>&1
    echo "mga build rc=0; binaries:"; ls obj_dir/Vmedia_grid_align_sim obj_mut_usign/Vmedia_grid_align_sim obj_mut_keepoff/Vmedia_grid_align_sim obj_mut_coin/Vmedia_grid_align_sim
    echo "verilator warnings in build log: $(grep -c '^%Warning' build.log || true)"
    grep '^%Warning' build.log | sort | uniq -c | sed 's/^/  /' || true
    ;;
  mga-run)
    cd "$exp/tb/verilator/media_grid_align"
    make run VERILATOR="$VERILATOR" > run.log 2>&1 && echo "make run rc=0" || echo "make run rc=$?"
    ;;
  chmap)
    cd "$exp/tb/verilator/chmap_capture"
    rm -rf obj_dir
    make obj_dir/Vchmap_wrap VERILATOR="$VERILATOR" > build.log 2>&1
    rc=0; ./obj_dir/Vchmap_wrap > run.log 2>&1 || rc=$?
    echo "chmap_capture sim rc=$rc"
    tail -3 run.log
    ;;
  *) echo "unknown step $step"; exit 2;;
esac
