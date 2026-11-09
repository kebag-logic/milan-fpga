arm-trial.tsv / .log: tools/arm_counts.py on a scratch tree of 06cce32 with two extra patches: push-twice-alone (= push-twice-top.patch here, the first hunk of push-twice-encoder-appends) and push-twice-encoder-appends (as committed in 60094a2), each on tb/srp_top group onevec.
push-twice-alone: 12 checks, 12 PASS (the encoder merge absorbs the second hand-over).
push-twice-encoder-appends: 12 checks, 1 PASS, 11 FAIL: OV0 to OV10.
second-queueing alone on onevec at 06cce32: 12 checks, 12 PASS (head-06cce32/camp-srp/camp-srp.log, the UNPROVEN line and the onevec tally after it).
