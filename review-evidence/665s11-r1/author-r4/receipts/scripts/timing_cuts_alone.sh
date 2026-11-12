#!/bin/bash
# timing_cuts_alone.sh: elaborate-gates-1 gate_19's member test_soc_timing_cuts, alone and with no wall clock, in
# that job's own clone at the head and with the LiteX interpreter the job used (gate_19 killed it at 900 s, UNKNOWN)
S=<scratch>; W=$S/gates/pass1/elaborate.elaborate-gates-1/wt; L=$S/gates/pass1/logs
T=$L/elaborate.elaborate-gates-1__gate_19.standalone-test_soc_timing_cuts
echo "# head $(git -C $W rev-parse HEAD): test_soc_timing_cuts alone, no wall clock (gate_19 ended UNKNOWN, exit 92)" > $T.log
start=$(date +%s)
(cd $W/sw/litex && env HOME=$S/gates/home PATH=<litex>/venv/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<shared-scratch>/a662/make43/bin:/usr/local/bin:/usr/bin:/bin \
   VERILATOR=<tools>/pinned-verilator-5.050/verilator python3 test_soc_timing_cuts.py) >> $T.log 2>&1
rc=$?; echo "# exit $rc after $(( $(date +%s) - start )) s" >> $T.log; echo $rc > $T.rc
git -C $W status --porcelain >> $T.log
