#!/usr/bin/env bash
# the processor gates at the base 47434635, after the head chain ends (so no
# more than two Verilator builds run at once)
S=<scratch>/r4
while [ ! -f $S/rec/chain.done ]; do sleep 20; done
bash $S/scripts/run_gates.sh $S/base-pp $S/rec/base-gates
echo done > $S/rec/base.done
