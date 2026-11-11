#!/bin/bash
# gate1b_hostmake.sh: the builder's gate 1b alone, on the lane-build clone of the head, with the host's make (4.4.1)
# first on PATH; the lane run had make 4.3 first, which does not re-read MAKEFLAGS mid-parse, so 1b skipped one mutation
S=<scratch>; W=$S/gates/pass1/lane-build/wt; L=$S/gates/pass1/lane; N=builder_gate1b_hostmake
cd $W
{ echo "# head $(git rev-parse HEAD) gate $N: test_builder.py --require-rv32 --gates test_baremetal_profile_contract ($(make --version | head -1))"
  python3 sw/builder/test_builder.py --require-rv32 --gates test_baremetal_profile_contract; } > $L/$N.log 2>&1
echo $? > $L/$N.rc
