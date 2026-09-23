#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer probe: stage the protocol-processor gitlink in a disposable parent
# clone at each given PP commit and run the parent gates whose population
# reads the processor's Python (plus the cheap source-list gates).
#
# Usage: parent_consumer.sh PARENT_DIR OUT_DIR LABEL=SHA [LABEL=SHA ...]
#   PARENT_DIR  a disposable parent clone whose protocol-processor/ is a git
#               checkout that contains every SHA given
#   OUT_DIR     receipts directory; one subdirectory per LABEL
# Environment: PINNED_VERILATOR (optional) is put first on PATH via its directory.
set -euo pipefail

parent=$(cd "$1" && pwd)
out=$2
shift 2
mkdir -p "$out"
out=$(cd "$out" && pwd)
if [ -n "${PINNED_VERILATOR:-}" ]; then
    PATH="$(dirname "$PINNED_VERILATOR"):$PATH"
    export PATH
fi

gates=(
    "py_idiom|python3 scripts/check_py_idiom.py"
    "py_idiom_list|python3 scripts/check_py_idiom.py --list"
    "py_idiom_selftest|python3 scripts/check_py_idiom.py --selftest"
    "cpp_idiom|python3 scripts/check_cpp_idiom.py"
    "hygiene|python3 scripts/check_hygiene.py --check"
    "todo_ownership|python3 scripts/check_todo_ownership.py"
    "fail_fast|python3 scripts/measure_fail_fast.py --check"
    "test_evidence|python3 scripts/measure_test_evidence.py --check"
    "control_flow|python3 scripts/measure_control_flow.py"
    "rtl_source_lists|python3 scripts/check_rtl_source_lists.py"
    "pp_srcs|python3 scripts/pp_srcs.py --check --selftest"
)

summary="$out/summary.tsv"
printf 'label\tpp_sha\tgate\texit\n' > "$summary"
for spec in "$@"; do
    label=${spec%%=*}
    sha=${spec#*=}
    dir="$out/$label"
    mkdir -p "$dir"
    git -C "$parent/protocol-processor" checkout --quiet --detach "$sha"
    git -C "$parent" update-index --cacheinfo "160000,$sha,protocol-processor"
    {
        echo "parent HEAD: $(git -C "$parent" rev-parse HEAD)"
        echo "staged gitlink: $(git -C "$parent" ls-files -s protocol-processor)"
        echo "submodule status:"
        git -C "$parent" submodule status
        echo "pp worktree clean: $(git -C "$parent/protocol-processor" status --porcelain | wc -l) dirty paths"
        echo "python3: $(python3 --version 2>&1)"
    } > "$dir/00-state.txt"
    n=1
    for g in "${gates[@]}"; do
        name=${g%%|*}
        cmd=${g#*|}
        log=$(printf '%s/%02d-%s.log' "$dir" "$n" "$name")
        set +e
        (cd "$parent" && echo "\$ $cmd" && eval "$cmd") > "$log" 2>&1
        rc=$?
        set -e
        echo "exit=$rc" >> "$log"
        printf '%s\t%s\t%s\t%s\n' "$label" "$sha" "$name" "$rc" >> "$summary"
        n=$((n + 1))
    done
done
cat "$summary"
