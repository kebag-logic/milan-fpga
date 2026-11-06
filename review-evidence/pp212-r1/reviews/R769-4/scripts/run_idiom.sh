#!/bin/sh
# Usage: run_idiom.sh <scratch-parent> <receipts-dir>
# Runs the parent's scripts/check_cpp_idiom.py (plain, --list, --selftest)
# with the protocol-processor gitlink staged at each pin, in a disposable
# parent checkout whose protocol-processor is a clone holding all pins.
PAR=$1; R=$2
cd "$PAR" || exit 2
for pin in 6162885ffee5d8e8897732be6479982b8dceaec9 834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1 a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645; do
  s=$(echo $pin | cut -c1-7)
  git -C protocol-processor checkout -q --detach $pin
  git update-index --cacheinfo 160000,$pin,protocol-processor
  { echo "parent HEAD $(git rev-parse HEAD)"; git submodule status -- protocol-processor gptp-processor; } > "$R/idiom-$s.pins"
  python3 -I scripts/check_cpp_idiom.py > "$R/idiom-$s.log" 2>&1; echo $? > "$R/idiom-$s.rc"
  python3 -I scripts/check_cpp_idiom.py --list > "$R/idiom-$s.list.log" 2>&1; echo $? > "$R/idiom-$s.list.rc"
done
git -C protocol-processor checkout -q --detach 6162885ffee5d8e8897732be6479982b8dceaec9
git update-index --cacheinfo 160000,6162885ffee5d8e8897732be6479982b8dceaec9,protocol-processor
python3 -I scripts/check_cpp_idiom.py --selftest > "$R/idiom-6162885.selftest.log" 2>&1; echo $? > "$R/idiom-6162885.selftest.rc"
sha256sum scripts/check_cpp_idiom.py scripts/code_quality_scope.py scripts/cpp_idiom.budget > "$R/idiom-tool.sha256"
