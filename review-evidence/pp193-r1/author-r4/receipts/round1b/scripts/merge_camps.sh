#!/usr/bin/env bash
# one directory per side with each campaign's top-level log, rc and sec,
# taken from the runner that ran it to the end
S=<scratch>
R=$S/rec
rm -rf $R/camps; mkdir -p $R/camps/base $R/camps/head $R/camps/head-final
for c in srp_top acmp notify d3 aecp dispatch; do cp $R/base-camps/$c.{log,rc,sec} $R/camps/base/; done
for c in elab_mutants name_state name_wr gsi ctr; do cp $R/base-camps-d/$c.{log,rc,sec} $R/camps/base/; done
for c in srp_top acmp notify aecp dispatch ctr gsi name_wr name_state elab_mutants; do cp $R/head-camps/$c.{log,rc,sec} $R/camps/head/; done
[ -f $R/head-camps-d3/d3.rc ] && cp $R/head-camps-d3/d3.{log,rc,sec} $R/camps/head/
cp $R/head2-camps/gsi.{log,rc,sec} $R/camps/head-final/
{ echo "base: srp_top acmp notify d3 aecp dispatch from runner 1; elab_mutants name_state name_wr gsi ctr from runner 2 (the helper)";
  echo "head 67b90c17: d3 from its own run at --jobs 4; every other from runners A and B";
  echo "head-final 788425db: gsi (the only campaign that reads a file commit 3 changed)"; } > $R/camps/SOURCES.txt
