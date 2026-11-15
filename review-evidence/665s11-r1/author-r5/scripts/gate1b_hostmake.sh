#!/bin/bash
# gate1b_hostmake.sh: the builder's gate 1b alone, on the model group's clone of the final head, with the host's make
# (4.4.1) for make 4.3, which does not re-read MAKEFLAGS mid-parse, so the lane run skipped one 1b mutation
S=<scratch>; W=$S/r5/pass3/lane-model/wt; L=$S/r5/pass3/lane; N=builder_gate1b_hostmake
cd $W || exit 3
. $S/tools/env.sh
export PATH=$(echo $PATH | tr ':' '\n' | grep -v 'make43' | paste -sd:)
{ echo "# head $(git rev-parse HEAD) gate $N: test_builder.py --require-rv32 --gates test_baremetal_profile_contract ($(make --version | head -1))"
  python3 sw/builder/test_builder.py --require-rv32 --gates test_baremetal_profile_contract; } > $L/$N.log 2>&1
echo $? > $L/$N.rc
git status --porcelain --untracked-files=all > $L/$N-tree-after.txt
