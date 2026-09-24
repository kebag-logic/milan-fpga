#!/usr/bin/env bash
# Export the exact head, then run the guard, desc_store and pp_top suites plus
# the unguarded baseline and the shipped hold-deleted mutation control.
source "$(dirname "$0")/00_env.sh"
{ echo "verilator: $(command -v verilator)"; verilator --version; sha256sum "$VBIN/verilator"; } > $RCPT/tool-identity.txt
rm -rf "$TREE"; mkdir -p "$TREE"
git -C "$SRC" archive "$HEAD_SHA" | tar -x -C "$TREE"
run() { local tag=$1; shift; set +e; ( "$@" ) > "$RCPT/$tag.log" 2>&1; echo "$tag rc=$?" | tee -a "$RCPT/rc.txt"; set -e; }
: > "$RCPT/rc.txt"
run guard-suite       make -C "$TREE/tb/desc_mem_guard"
run guard-baseline    make -C "$TREE/tb/desc_mem_guard" baseline
run guard-mutate-ctl  python3 "$TREE/tb/desc_mem_guard/mutate.py" --output "$PKT/scratch/mutctl"
cp "$PKT/scratch/mutctl/mutant-no-hold.log" "$RCPT/guard-mutate-ctl.inner.log"
run desc-store-suite  make -C "$TREE/tb/desc_store"
run pp-top-suite      make -C "$TREE/tb/pp_top"
