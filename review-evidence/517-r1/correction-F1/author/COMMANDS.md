# A183 reproduction commands

Run from $CANDIDATE. Source is frozen at ff7dac3257a321538a1fd1a310ab3190f646153d. All executable command/environment/exit records live in the matching command directories; full benchmark environments and resource limits are in each runs/*/identity.json. Command examples below use fresh output directories, never overwrite the retained evidence.

```sh
rtk proxy python3 tb/verilator/milan_dp/test_sim_pool.py
rtk proxy python3 tb/verilator/milan_dp/test_render_phase_observation.py
rtk proxy python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py --output <new-controls-directory>
rtk proxy python3 scripts/suite_tally.py --selftest
rtk proxy python3 scripts/suite_shards.py --selftest
rtk proxy python3 scripts/check_baremetal_only.py --check
rtk proxy python3 scripts/check_baremetal_only.py --selftest
```

final-focused/receipts.json enumerates all 13 focused gate commands and exact exits. final-additional/results.json and its child receipts enumerate the 11 policy/selftest commands. final-backpressure-command and final-negative-command preserve the process-control commands. A synthetic test outer timeout is UNKNOWN setup/hang evidence, never PASS. The new cancellation oracle itself requires process exit within two seconds while the reader remains blocked.

Use scripts/restored_defect.py with the lane and a fresh evidence directory. It restores exact 5874895e runner bytes only in disposable fixtures, invokes the unchanged regression and actual Makefile, and requires eight targeted blocked-shutdown rejections. It never modifies source. scripts/policy_probes.py runs the independent public literal controls in disposable repositories; all original context and refusal classes remain required.

For each fresh full-suite measurement, use bench/run_suite.py with --lane, --out, --verilator, --expect-head, --jobs and --temperature. The exact commands are retained in benchmark-commands/*/receipt.json. The four completed commands used the verified scoped selector $VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator; never replace installed tools. Preserve the same CPU affinity, memory ceiling and scratch root. Run cold-sequential then warm-sequential, followed by cold-pooled then warm-pooled. Cold invokes the existing clean target; warm retains that same-mode build. Do not overlap runs. BENCHMARK-METHOD.md records the verified public method and its limits.

bench/analyze.py reads each raw sample/log pair. bench/compare.py compares cold and warm pairs separately. scripts/verify_measurements.py additionally checks all four runs together, each command/body association, all 9324 checks, 13 tallies and 23 render identities. Raw command logs and the initial evidence-parser failure remain retained.

scripts/integrity.py takes the source root, output JSON and exact head. It verifies committed bytes, kinds, modes, stage-0 indexes, hidden flags and registered required submodule pins/bytes, with replacement objects disabled. Run it after measurements; final-integrity.json is the completed receipt. source-diff.patch and scope-proof.json bind the four changed source files and fixed artifacts to the correction parent/base. No source publication or integration gate is implied by this handoff.
