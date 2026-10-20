#!/usr/bin/env bash
# the base records the reset of 14:5x cut: run_suites (and the REQ-tag check
# that reads it), then the consumer gates milan_dp and test_builder, then OOC
S=<scratch>
bash $S/scripts/run_gates.sh $S/base-pp $S/rec/base-gates run_suites req_tags_executed
bash $S/scripts/run_consumers.sh $S/rec/base-cons-2 milan_dp test_builder
bash $S/scripts/run_ooc.sh $S/rec/base-ooc
echo done > $S/rec/BASE-REST.done
