#!/bin/sh
# Usage: flags_guard_probe.sh <clone> <scratchdir> <make43-dir>
# (A) control: prefix (b9b38961) vs head integration.mk SRCS capture under each make, w+j8.
# (B) head DP_FLAGS capture: job bound and absence of directory lines, per make and context.
# (C) guards: a fake ../milan_dp whose print-srcs emits nothing / a non-file / fails.
set -u
C=$1; S=$2; M43=$3; M=$C/tb/verilator/maap
rm -rf "$S"; mkdir -p "$S"
printf '\nprobe-flags:\n\t@echo "SRCS-WORDS=$(words $(SRCS)) DIRLINES=$(words $(filter make% Entering Leaving,$(DP_SRCS) $(DP_FLAGS))) JFLAG=[$(word 2,$(filter -j %%,$(DP_FLAGS)))] JPOS=[$(wordlist 4,5,$(DP_FLAGS))]"\n' > "$S/tail.mk"
git -C "$C" show b9b389611:tb/verilator/maap/integration.mk > "$S/prefix.src"
cat "$S/prefix.src" "$S/tail.mk" > "$S/prefix.mk"; cat "$M/integration.mk" "$S/tail.mk" > "$S/head.mk"
printf 'all:\n\t+@$(MAKE) -s -C %s -f $(PROBE) probe-flags $(EXTRA)\n' "$M" > "$S/parent.mk"
for mk in "$M43/make" "$(command -v make)"; do
  echo "#### $($mk --version | head -1)"
  for v in prefix head; do
    for ctx in plain w j8 w+j8; do
      case $ctx in
        plain) out=$(cd "$M" && env -u MAKEFLAGS -u VERILATOR_JOBS "$mk" -s -f "$S/$v.mk" probe-flags 2>&1);;
        w)     out=$(cd "$M" && env -u VERILATOR_JOBS MAKEFLAGS=w "$mk" -s -f "$S/$v.mk" probe-flags 2>&1);;
        j8)    out=$(cd / && env -u MAKEFLAGS -u VERILATOR_JOBS "$mk" -j8 -f "$S/parent.mk" PROBE="$S/$v.mk" 2>&1);;
        w+j8)  out=$(cd / && env -u VERILATOR_JOBS MAKEFLAGS=w "$mk" -j8 -f "$S/parent.mk" PROBE="$S/$v.mk" 2>&1);;
      esac
      echo "== $v $ctx rc=$? :: $(printf '%s\n' "$out" | grep -E 'SRCS-WORDS|non-files|error|Error' | cut -c1-240 | tr '\n' ' ')"
    done
  done
  # job bound: default (integration.mk ?= 2), parent command line (mutants.py shape), environment
  out=$(cd / && env -u VERILATOR_JOBS MAKEFLAGS=w "$mk" -j8 -f "$S/parent.mk" PROBE="$S/head.mk" 2>&1); echo "== bound default w+j8 :: $out"
  out=$(cd / && env -u VERILATOR_JOBS MAKEFLAGS=w "$mk" -j8 -f "$S/parent.mk" PROBE="$S/head.mk" VERILATOR_JOBS=5 2>&1); echo "== bound cmdline=5 w+j8 :: $out"
  out=$(cd / && env VERILATOR_JOBS=7 MAKEFLAGS=w "$mk" -j8 -f "$S/parent.mk" PROBE="$S/head.mk" 2>&1); echo "== bound env=7 w+j8 :: $out"
  # the same through the suite's own target chain: make -j8 -C maap integration-build (dry run, recipe text only)
  out=$(cd / && env -u VERILATOR_JOBS MAKEFLAGS=w "$mk" -n -j8 -s -C "$M" integration-build DP_MDIR="$S/obj-dry" VERILATOR_JOBS=3 2>&1 | grep -o -- '--build -j [0-9]*' | sort | uniq -c); echo "== suite chain cmdline=3 (-n) :: $out"
  # control: drop the explicit VERILATOR_JOBS pass-through, bound is lost
  sed 's/ VERILATOR_JOBS=\$(VERILATOR_JOBS))/)/' "$S/head.mk" > "$S/nopass.mk"
  out=$(cd / && env -u VERILATOR_JOBS MAKEFLAGS=w "$mk" -j8 -f "$S/parent.mk" PROBE="$S/nopass.mk" VERILATOR_JOBS=5 2>&1); echo "== control no-pass cmdline=5 :: $out"
done
# (C) guard fault injection on a disposable fake tree, both makes
G=$S/g; mkdir -p "$G/tb/verilator/maap" "$G/tb/verilator/milan_dp"; cp "$S/head.mk" "$G/tb/verilator/maap/integration.mk"
: > "$G/tb/verilator/maap/real.sv"
for mk in "$M43/make" "$(command -v make)"; do
  echo "#### guards $($mk --version | head -1)"
  for case in good empty blank nonfile mixed fail flagfail; do
    case $case in
      good)    srcs='echo real.sv'; flags='echo --cc --build -j $(VERILATOR_JOBS)';;
      empty)   srcs='@true'; flags='echo x';;
      blank)   srcs='echo "   "'; flags='echo x';;
      nonfile) srcs='echo make[1]:'; flags='echo x';;
      mixed)   srcs='echo real.sv no_such.sv'; flags='echo x';;
      fail)    srcs='false'; flags='echo x';;
      flagfail) srcs='echo real.sv'; flags='false';;
    esac
    printf 'print-srcs:\n\t@%s\nprint-dp-vflags:\n\t@%s\n' "$srcs" "$flags" | sed 's/@@/@/' > "$G/tb/verilator/milan_dp/Makefile"
    out=$(cd "$G/tb/verilator/maap" && env MAKEFLAGS=w "$mk" -s -f integration.mk probe-flags VERILATOR_JOBS=4 2>&1)
    echo "== $case rc=$? :: $(printf '%s' "$out" | tr '\n' ' ' | cut -c1-240)"
  done
done
