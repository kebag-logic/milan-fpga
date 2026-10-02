#!/bin/bash
# usage: without.sh <label> <rev> <path>...: copy the working tree, put <path> back
# at <rev>, run the packer gate, and list the failing tests.
label=$1; rev=$2; shift 2
dst=$VALIDATION_STORAGE/c8-a501/without/$label
rm -rf "$dst"; mkdir -p "$dst"
cp -a $LANES/ppC8-desc-lint/hdl $LANES/ppC8-desc-lint/tb "$dst/"
for p in "$@"; do git -C $LANES/ppC8-desc-lint show "$rev:$p" > "$dst/$p"; done
cd "$dst/tb/desc_store" && python3 -B test_gen_desc_image.py > ../../gate.log 2>&1
echo "rc=$?"; grep -E "^(FAIL|ERROR):" ../../gate.log | sort | uniq -c; grep -E "^Ran|^FAILED|^OK" ../../gate.log
