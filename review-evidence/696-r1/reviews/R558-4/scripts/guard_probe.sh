#!/bin/sh
# Usage: guard_probe.sh <clone> <scratchdir> <make-binary-dir>
# (1) control: the pre-delta capture form (no MAKEFLAGS=) must still leak under the
#     hosted shape (MAKEFLAGS=w, recursive -j8 parent) with the given make, and the
#     non-file guard must refuse it; the head form must not.
# (2) job bound: DP_FLAGS printed from the head integration.mk must carry -j <N>
#     for VERILATOR_JOBS=N given to the outer make on its command line, in plain and
#     w+j8 contexts; a variant without the explicit pass shows what it would lose.
# (3) guards: disposable copies whose derivation directory is a fake suite that
#     prints an empty list / a directory line / a non-file word / fails.
set -u
C=$1; S=$2; MB=$3; M=$C/tb/verilator/maap
mkdir -p "$S"; export PATH="$MB:$PATH"
echo "head=$(git -C "$C" rev-parse HEAD) make=$(make --version | head -1)"
# simpler job extraction: print the two words following --build
addj() { { cat "$1"; printf '\nprobe-print:\n\t@echo "SRCS-WORDS=$(words $(SRCS))"; echo "$(DP_FLAGS)" | grep -o -- "--build -j [0-9]*"\n'; } > "$2"; }
addj "$M/integration.mk" "$S/head.mk"
sed 's/\$(shell MAKEFLAGS= \$(MAKE)/$(shell $(MAKE)/' "$M/integration.mk" > "$S/prefix.src"; addj "$S/prefix.src" "$S/prefix.mk"
sed 's/ VERILATOR_JOBS=\$(VERILATOR_JOBS))/)/' "$M/integration.mk" > "$S/nopass.src"; addj "$S/nopass.src" "$S/nopass.mk"
printf 'all:\n\t+@$(MAKE) -s -C %s -f $(PROBE) probe-print $(EXTRA)\n' "$M" > "$S/parent.mk"
run() { # variant ctx extra
  case $2 in
    plain) (cd "$M" && env -u MAKEFLAGS make -s -f "$S/$1.mk" probe-print $3 2>&1);;
    w+j8)  (cd / && env MAKEFLAGS=w make -j8 -f "$S/parent.mk" PROBE="$S/$1.mk" EXTRA="$3" 2>&1);;
  esac; echo "rc=$?"; }
for v in head prefix nopass; do for ctx in plain w+j8; do for x in "" "VERILATOR_JOBS=5"; do
  echo "== $v $ctx [$x]"; run $v $ctx "$x" | grep -E 'SRCS-WORDS|--build|non-files|empty|failed|rc=' | cut -c1-240
done; done; done
# (3) guard power on fake derivation suites
for kind in empty dirline nonfile fail; do
  F=$S/fake-$kind; mkdir -p "$F"
  case $kind in
    empty)   body='@echo';;
    dirline) body="@echo $M/integration.mk make[2]: Entering directory \\\\'/tmp\\\\'";;
    nonfile) body="@echo $M/integration.mk /no/such/file.sv";;
    fail)    body='@exit 2';;
  esac
  printf 'print-srcs:\n\t%s\nprint-dp-vflags:\n\t@echo --build -j $(VERILATOR_JOBS)\n' "$body" > "$F/Makefile"
  sed "s#-C \.\./milan_dp#-C $F#g" "$M/integration.mk" > "$S/g-$kind.src"; addj "$S/g-$kind.src" "$S/g-$kind.mk"
  for ctx in plain w+j8; do echo "== guard $kind $ctx"; run g-$kind $ctx "" | grep -E 'SRCS-WORDS|non-files|empty|failed|Error|rc=' | cut -c1-240; done
done
