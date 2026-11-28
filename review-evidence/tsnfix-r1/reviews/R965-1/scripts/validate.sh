#!/bin/bash
# validate.sh PACKET REPO WORK: the quality job's command at the repo's checked-out head.
P=$1; R=$2; W=$3
. "$P/scripts/env.sh" "$P"
cd "$R" || exit 2
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree}) dirty $(git status --porcelain | wc -l)"
echo "gcc: $(gcc --version | head -1); clang: $(clang --version | head -1); clang-tidy: $(clang-tidy --version | grep version); cppcheck: $(cppcheck --version); gtest: $CMAKE_PREFIX_PATH; mmdc $(mmdc --version); cmake $(cmake --version | head -1)"
python3 scripts/validate.py --work "$W" --jobs 16 --graphs
echo "validate rc=$?"
