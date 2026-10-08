[A560]

# Round 13 reproduction

Candidate: `154722e14781c7373f3229420b6e007f9bcf9835`.
Base: `efea74858dffc482820d4f19c26c38796a57ff75`.
Use the PR body's dependency and environment setup. Run from the candidate
checkout with all four required submodules at their recorded pins.
Use disk-backed `$SCRATCH`, the verified pinned SDK through `$MILAN_RV32_CC`,
and release 5.050 through `$VERILATOR`. Set `$TMPDIR` to `$SCRATCH`.
Copy `round13-helpers/.` into `$SCRATCH` before invoking the helper scripts.

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$SCRATCH/ctrl-build"
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$SCRATCH/coverage-build"
python3 "$SCRATCH/asan.py"
python3 "$SCRATCH/new_plants.py"
python3 "$SCRATCH/review_probes.py"
```

Expected: every command returns zero. The full campaign catches all 471 control
plants, 169 SRP plants at IF=2, and 68 selected SRP plants at IF=1, plus both
pin-refusal controls. The three new plants occur in both SRP passes.
The isolated new-plant helper repeats those six named catches. The sanitizer
helper runs seven SRP/composition suites at each interface count. Only the
first-party firmware and tests use sanitizer flags; dependency and host-model
objects retain the shared harness's ordinary flags.

The original reviewer's header is appended only to a disposable test copy.
Its three `SrpFeedback.R12*` cases pass at each count. The reproduction does
not modify the candidate or dependencies. The review input source is
`83b76bfda9cc0e02e0136806ced9500e761b9476`, directory
`review-evidence/665f4-r1/reviews/R532-12` on the evidence branch.

Every documentation command and result is listed in `ROUND13-GATES.md` and
`ROUND13-GATES.json`. Path aliases are `$SOURCE` for the candidate, `$SCRATCH`
for writable disk scratch, and `$SDK` for the verified SDK. The source archive
row runs from `$SCRATCH/source-archive`, produced by `git archive HEAD`.
No generated file is edited by hand.

For long execution, start each command with `setsid nohup`, its own log and
exit-status file, then wait in foreground intervals of at most 45 seconds.
A wait timeout is a polling interval, never a gate verdict. Do not finish while
a job remains active. Limit each campaign to four workers and any HDL build
to eight make jobs with at most two simultaneous builds.

The final follow-up commit wraps one Python line. Its syntax tree and all
mutation definitions are unchanged. Firmware, test-case bytes, dependencies,
coverage exclusions and compiler flags used by the running gates match the
candidate. `ROUND13-SOURCE.json` records the syntax-tree comparison.
