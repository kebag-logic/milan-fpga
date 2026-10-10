#!/bin/sh
# Parse-time probes of tb/verilator/maap/integration.mk's derived-source guard.
# Usage: guard_probes.sh <tree-root>   (a disposable copy of the repository)
# Each variant is written next to integration.mk as probe_<name>.mk, evaluated
# with a side makefile whose `probe-srcs` target only prints the derived
# Verilator source list (no build, no -n: -n would leak into the nested
# $(shell make) through MAKEFLAGS), and removed afterwards.
set -u
root=$1; d=$root/tb/verilator/maap; mk=$d/integration.mk
old8='$(shell $(MAKE) -s -C ../milan_dp print-srcs)'
new8='$(shell $(MAKE) -s --no-print-directory -C ../milan_dp print-srcs)'
run() { # name makeflags file [extra make args]
  name=$1; mf=$2; f=$3; shift 3
  out=$(cd "$d" && MAKEFLAGS=$mf make -f "$f" -f probe_side.mk probe-srcs "$@" 2>&1); rc=$?
  ent=$(printf '%s\n' "$out" | grep -c 'Entering directory') 
  echo "== $name MAKEFLAGS='$mf' rc=$rc entering_lines_in_output=$ent"
  printf '%s\n' "$out" | grep -E '\*\*\*' | head -3
  printf '%s\n' "$out" | grep '^SRCS' | awk '{n=0; for(i=2;i<=NF;i++){n++; if(!(system("test -f \""d"/"$i"\"")==0)) bad=bad" "$i}; print "   SRCS words=" n " non-regular-files:" (bad==""?" none":bad)}' d="$d"
}
printf 'probe-srcs:\n\t@echo SRCS $(SRCS)\n' > "$d/probe_side.mk"
mkvar() { # name sed-expression
  sed "$2" "$mk" > "$d/probe_$1.mk"
}
# head file as-is
run head_plain "" integration.mk
run head_w w integration.mk
# f909d6c4 form: no --no-print-directory, no guard
git -C "$root" show f909d6c460344527f102f24b8e7a77f09959e755:tb/verilator/maap/integration.mk > "$d/probe_f909.mk"
run f909_w w probe_f909.mk
run f909_plain "" probe_f909.mk
# guard kept, print-directory suppression removed on the source capture
mkvar oldcap_guard "8s|--no-print-directory ||"
run oldcap_guard_w w probe_oldcap_guard.mk
# a non-file word appended to the derived list
mkvar nonfile "8s|print-srcs)|print-srcs; echo bogus_not_a_file.sv)|"
run nonfile "" probe_nonfile.mk
# a glob word
mkvar glob "8s|print-srcs)|print-srcs; echo '*.cpp')|"
run glob "" probe_glob.mk
# a directory entry (exists, is not a regular file)
mkvar dir "8s|print-srcs)|print-srcs; echo ../milan_dp)|"
run directory "" probe_dir.mk
# an empty derived list
mkvar empty "8s|print-srcs)|print-srcs >/dev/null)|"
run empty "" probe_empty.mk
# command-line override of DP_SRCS with a non-file word
run override_cmdline "" integration.mk DP_SRCS=bogus_not_a_file.sv
# failing nested make still reported by the status check
mkvar status "8s|print-srcs)|no-such-target)|"
run nested_fail "" probe_status.mk
rm -f "$d"/probe_*.mk
