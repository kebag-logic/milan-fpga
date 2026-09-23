#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer probe: this repository's gates on disposable checkouts.
#
# Usage: repo_gates.sh HEAD_CHECKOUT BASE_CHECKOUT OUT_DIR PHASE
#   PHASE guards: fixture-guards-test and fixture-guards at BASE and HEAD
#   PHASE docs:   the CI docs-gates commands and gen_matrix --check at HEAD
#   PHASE lint:   lint_hdl.sh at HEAD
#   PHASE suite:  the full tb/pp_top suite at HEAD
# (split so that each phase is one bounded foreground run)
# Environment: PINNED_VERILATOR (required) - the pinned Verilator wrapper; its
# directory goes first on PATH. (Not VERILATOR_BIN: Verilator reads that name.)
#
# HEAD: the CI docs-gates job commands, gen_matrix --check, lint_hdl.sh and
# the full tb/pp_top suite (unit test, fixture guards, both builds, tally).
# BASE and HEAD: `make fixture-guards` stdout and `make fixture-guards-test`
# output, captured for a byte comparison.
# Parallelism is capped at 8: the suite's `-j 0` is replaced by `-j 8` (the
# only change to VFLAGS; parallelism cannot change a result) and every command
# runs under `taskset -c 0-7`.
set -euo pipefail
head=$(cd "$1" && pwd)
base=$(cd "$2" && pwd)
mkdir -p "$3"
out=$(cd "$3" && pwd)
phase=$4
: "${PINNED_VERILATOR:?set PINNED_VERILATOR}"
PATH="$(dirname "$PINNED_VERILATOR"):$PATH"
export PATH
pin="taskset -c 0-7"

summary="$out/summary-$phase.tsv"
printf 'rev\tstep\texit\n' > "$summary"
step() { # rev dir name command...
    local rev=$1 dir=$2 name=$3
    shift 3
    local log="$out/$rev-$name.log"
    set +e
    (cd "$dir" && echo "\$ $*" && $pin "$@") > "$log" 2>&1
    local rc=$?
    set -e
    echo "exit=$rc" >> "$log"
    printf '%s\t%s\t%s\n' "$rev" "$name" "$rc" >> "$summary"
}

{
    echo "verilator on PATH: $(command -v verilator)"
    verilator --version
    echo "python3: $(python3 --version 2>&1)"
    echo "c++: $(c++ --version | head -1)"
    echo "head: $(git -C "$head" rev-parse HEAD) tree $(git -C "$head" rev-parse 'HEAD^{tree}')"
    echo "base: $(git -C "$base" rev-parse HEAD) tree $(git -C "$base" rev-parse 'HEAD^{tree}')"
} > "$out/00-tools-$phase.txt" 2>&1

vflags_j8() { # checkout -> that checkout's tb/pp_top VFLAGS with -j 0 -> -j 8
    make -s -C "$1/tb/pp_top" -f Makefile -f - print-vflags <<'EOF'
print-vflags:
	@echo '$(subst -j 0,-j 8,$(VFLAGS))'
EOF
}
echo "VFLAGS override (head): $(vflags_j8 "$head")" >> "$out/00-tools-$phase.txt"
echo "VFLAGS override (base): $(vflags_j8 "$base")" >> "$out/00-tools-$phase.txt"

if [ "$phase" = guards ]; then
for rev in base head; do
    dir=$base; [ "$rev" = head ] && dir=$head
    step "$rev" "$dir" fixture-guards-test make -s -C tb/pp_top fixture-guards-test
    step "$rev" "$dir" fixture-guards make -s -C tb/pp_top fixture-guards "VFLAGS=$(vflags_j8 "$dir")"
done
fi
if [ "$phase" = docs ]; then
step head "$head" check-links python3 scripts/check-links.py
step head "$head" check-matrix python3 scripts/check-matrix.py
step head "$head" wavedrom-check python3 scripts/render-wavedrom.py --check
step head "$head" make-stale make -s stale
step head "$head" gen-matrix-check python3 scripts/gen_matrix.py --check
fi
if [ "$phase" = lint ]; then
step head "$head" lint-hdl ./scripts/lint_hdl.sh
fi
if [ "$phase" = suite ]; then
    step head "$head" pp-top-suite make -C tb/pp_top "VFLAGS=$(vflags_j8 "$head")"
fi
cat "$summary"
