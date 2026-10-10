#!/bin/sh
# Usage: derive_probe.sh <clone> <scratchdir>
# Exercises the #696 integration source derivation at the checked-out head and
# with disposable copies of integration.mk (pre-fix form, injected pollution).
# Each copy gets one appended parse-only target (probe-print) so no recipe of the
# suite runs; no tracked file is edited (copies live in <scratchdir>, passed with -f).
set -u
C=$1; S=$2; M=$C/tb/verilator/maap
mkdir -p "$S"
echo "head=$(git -C "$C" rev-parse HEAD) make=$(make --version | head -1)"
mk() { # name, source-file -> $S/name.mk with the probe target appended
  { cat "$2"; printf '\nprobe-print:\n\t@echo "SRCS-WORDS=$(words $(SRCS)) NONFILE=[$(strip $(foreach w,$(SRCS),$(if $(shell test -f $(w) && echo y),,$(w))))] FLAGS-WORDS=$(words $(DP_FLAGS))"\n'; } > "$S/$1.mk"
}
run() { # label, env-makeflags, makefile, extra args...
  L=$1; MF=$2; F=$3; shift 3
  out=$(cd "$M" && env MAKEFLAGS="$MF" make -f "$F" probe-print "$@" 2>&1); rc=$?
  echo "== $L MAKEFLAGS='$MF' rc=$rc"
  printf '%s\n' "$out" | grep -E 'SRCS-WORDS|non-files|failed' | cut -c1-400
}
git -C "$C" show HEAD:tb/verilator/maap/integration.mk | cmp - "$M/integration.mk" && echo "worktree integration.mk == HEAD blob"
mk head "$M/integration.mk"
git -C "$C" show f909d6c46:tb/verilator/maap/integration.mk > "$S/old.src"; mk old "$S/old.src"
sed 's/ --no-print-directory//' "$M/integration.mk" > "$S/noflag.src"; mk noflag "$S/noflag.src"
sed 's/print-srcs)/print-srcs; echo not_a_source_file.sv)/' "$M/integration.mk" > "$S/word.src"; mk word "$S/word.src"
sed 's#print-srcs)#print-srcs; echo ../milan_dp)#' "$M/integration.mk" > "$S/dir.src"; mk dir "$S/dir.src"
sed 's#print-srcs)#print-srcs; echo "../../../hdl/ieee1722/maap/*.sv")#' "$M/integration.mk" > "$S/glob.src"; mk glob "$S/glob.src"
sed 's#$(MAKE) -s --no-print-directory -C ../milan_dp print-srcs)#true)#' "$M/integration.mk" > "$S/empty.src"; mk empty "$S/empty.src"
echo "--- 1. head (byte-identical copy + probe target)"
run head-plain '' "$S/head.mk"
run head-w w "$S/head.mk"
echo "--- 2. pre-fix f909d6c4 form: the hosted pollution reproduces under MAKEFLAGS=w"
run old-plain '' "$S/old.mk"
run old-w w "$S/old.mk"
echo "--- 3. guard alone (flag removed), MAKEFLAGS=w: guard must refuse"
run noflag-w w "$S/noflag.mk"
echo "--- 4. guard vs injected non-file word / directory / glob / empty list"
run inject-word '' "$S/word.mk"
run inject-dir '' "$S/dir.mk"
run inject-glob '' "$S/glob.mk"
run inject-empty '' "$S/empty.mk"
echo "--- 5. DP_SRCS overridden on the command line with a non-file word (head)"
run cmdline-override '' "$S/head.mk" DP_SRCS=not_a_file
echo "--- 6. observation: an outer 'make -n' reaches the nested capture (head suite entry)"
(cd "$M" && env -u MAKEFLAGS make -n integration-build 2>&1 | grep -E 'non-files' ; true)
