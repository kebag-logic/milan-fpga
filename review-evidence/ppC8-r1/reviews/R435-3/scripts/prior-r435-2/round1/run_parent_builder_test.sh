#!/bin/sh
# Run the parent's builder test in a scratch parent tree (dev cdf49d1a with
# parent-c4-disposition.patch then parent-adoption-c8-cdf49d1a.patch applied
# and protocol-processor replaced by the processor tree at e6cca1ff).
# usage: run_parent_builder_test.sh <parent-tree> <log> <rcfile>
cd "$1" || exit 2
python3 -B sw/builder/test_builder.py > "$2" 2>&1
echo $? > "$3"
