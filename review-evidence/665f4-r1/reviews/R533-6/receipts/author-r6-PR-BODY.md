[A560]

## Contents

- **[Status](#status)** -- Candidate and validation.
- **[Linked Issue / roles](#linked-issue--roles)** -- Task and independent review.
- **[Description](#description)** -- Bare-metal SRP behavior.
- **[Round 6](#round-6)** -- Receive recovery and F2 composition.
- **[Authoritative references](#authoritative-references)** -- Applicable contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Dependencies and environment.
- **[How to validate](#how-to-validate)** -- Commands and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Integration and release evidence.
- **[Definition of Done](#definition-of-done)** -- Remaining merge bar.

## Status

Round 6 REVIEW READY locally: `665-f4-srp` -> `dev`, head `cce554f64f6bdab1f6d26e5c4d7b46d54d228c52`.
All 98 final local invocations exit 0; 196 control/MAAP plants and 90 SRP
plants are caught. All 19 measured firmware files retain 100% line and branch
coverage after existing exclusions. The candidate is unpushed.

PR #690 already contains Round 5 `500b8f64443777685e6a54049d933476710d26f0`. Both Round 5 reviews are NEGATIVE
on the recoverable receive-allocation defect. Fresh independent review is owed.
This status supersedes the earlier publication and STOP wording.

## Linked Issue / roles

Relates to #665.

Executor: `[A560]`.
Internal cleared-context reviewer: `[R532]`.
External reviewer: `[R533]`.
Reviewers own verdicts, finding closure and the lens ledger.

## Description

Provide per-interface MSRP and MVRP on the bare-metal mailbox using pinned lwSRP
and entity-sized static pools. Startup declares outputs, Class A Domain and its
VLAN. Bound sinks reconcile Listener declarations; licences follow admission,
registration and committed membership. Refused output and recoverable receive
allocation preserve ordered work. Firmware uses neither an OS nor a heap.

## Round 6

An accepted SRP withdrawal could be lost when lwSRP lacked propagation storage.
The adapter now retains the complete record and retries without another peer
packet. Interface, bytes and arrival time survive repeated refusal and partial
application. Later SRP input and bindings wait; link reset cancels only its own
record. Allocation refusals are counted separately from malformed input.
The unchanged R533 probe passes at IF=1/2, including withdrawal after recovery.
Removing retry fails its required active-state check.

Merged assigned dev `e21c1ca024d37ea188ad15b5c8f9c2dae18628df` with `--no-ff`, preserving F2 MAAP tests and coverage.
The explicit application and linked fixture compose ADP, MAAP and SRP with all
receive/event/tick enables. The debug arm explicitly restores assertions after
F2's shared release flag. Eleven receive, two composition and one added timing
test have twenty new named defect plants.

Pins public lwSRP main `9197193e47a6bb1c45a56d90a18c1784123aba44`, which includes merged PR #15 and its Applicant
note tests. The prior claim that no production adaptation was needed was wrong.
The obsolete timer-removal claim is corrected; future-version and atomic-invalid
PDU behavior has adapter regressions. No dependency source change is made here.

## Authoritative references

- Issue #665 assignments 6030279477 and 6038730087; validation ruling 6036016117; R533-5 and R532-5 reports.
- `REQUIREMENTS.md` section 1; `docs/design/MAILBOX_SPLIT.md`; `docs/reference/FR_NFR.md`, NFR-SCOUT-02/03/08 and SRP hooks.
- Milan v1.2 4.2.7.2.2, 4.3.2, 5.5.2.7 and Table 4.3; IEEE 802.1Q-2018 Tables 10-3/10-4, 10.7.11, 35.1.2.2, 35.2.2.7.2 and 35.2.6.
- #608, #678, #679 and processor #134; `sw/firmware/ctrl/srp/README.md` records the selected processor differences.

## How to get into the same state

After publication, set installation-specific disk-scratch and tool locations:

```sh
git fetch origin 665-f4-srp
git switch --detach cce554f64f6bdab1f6d26e5c4d7b46d54d228c52
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
export SCRATCH SDK DOCS_ENV RUNTIME REVIEW_PACKET CGREEN PACKET PINNED_VERILATOR
export TMPDIR="$SCRATCH"
export HDL_J8_WRAPPER="$PACKET/round6-helpers/hdl-j8"
export PYTHONDONTWRITEBYTECODE=1
export PATH="$DOCS_ENV/bin:$PATH"
python3 scripts/ci_rv32_sdk.py --destination "$SDK"
export MILAN_RV32_CC="$SDK/bin/riscv32-buildroot-linux-gnu-gcc"
export VERILATOR="$PINNED_VERILATOR"
export VERILATOR_JOBS=2
```

Use HDL compiler release 5.050 and the CI-pinned ilp32d SDK, with the gate's
RV32I/ILP32 freestanding flags. lwSRP uses anonymous HTTPS. Keep products in disk
scratch; campaigns use four workers, with at most two HDL builds and eight
inner build jobs. The public dependency needs no local branch publication.

## How to validate

Run the two foreground firmware shards separately, each below ten minutes in
the recorded environment. The shards jointly cover all control plants; each
also runs the entire SRP campaign and all positives.

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard 0 2 --jobs 4 --build-dir "$SCRATCH/firmware-shard0"
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard 1 2 --jobs 4 --build-dir "$SCRATCH/firmware-shard1"
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$SCRATCH/coverage-check"
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/mailbox/gen_mailbox.py --check
python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$SCRATCH/maap-diff"
python3 scripts/docs_check.py
python3 scripts/docs_check.py --selftest
python3 scripts/check_doc_style.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 scripts/check_submodule_docs.py
python3 scripts/check_diagram_pngs.py
python3 scripts/check_em_dash.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df
git diff --check 500b8f64443777685e6a54049d933476710d26f0 HEAD
```

Run the mailbox gate in a tracked scratch export with the pinned job-limited
wrapper:

```sh
git archive --format=tar --output "$SCRATCH/mailbox-inputs.tar" HEAD tb/verilator/mbx tb/common hdl/milan/mailbox sw/firmware/ctrl sw/mailbox scripts/mutant_run.py
mkdir -p "$SCRATCH/mailbox"
tar -xf "$SCRATCH/mailbox-inputs.tar" -C "$SCRATCH/mailbox"
make -C "$SCRATCH/mailbox/tb/verilator/mbx" -j2 VBUILD_JOBS=8 VERILATOR="$HDL_J8_WRAPPER"
```

The handoff's `ROUND6-GATES.md` expands all 75 documentation-bank entries,
no-Git archive checks, dependency OFF/ON profiles, independent probe/control,
and four linked-size commands. Helpers use `$PACKET`, `$REVIEW_PACKET`,
`$CGREEN` and `$RUNTIME`; their hashes and inputs accompany the packet.
`HANDOFF.md` contains changes with line positions, test-to-plant maps, coverage,
gates and size tables. `ROUND6-GATES.json` records log hashes and durations.

Expected: every command exits 0; each plant fails its named behavioral
observable; all 19 portable files stay at 100% after unchanged exclusions.
SRP positives per interface count comprise 53 existing adapter, 11 recovery,
two composition, three debug, five timing and five processor-wire cases, plus
all five entity shapes and target builds. The reviewer probe completes the
withdrawal without retransmission and without incrementing malformed.

## Known limitations / out of scope

- F3 is absent from the assigned F2 base. ACMP binding calls, live MAAP/stream updates and the fabric licence output remain integration work.
- Timing is a conditional host envelope. Recovery retains its original arrival/deadline budget; an 11 ms exhaustion or TX stall is rejected. Permanent exhaustion cannot meet a finite bound. Target timing remains separate evidence.
- Linked RAM spans are 62560 / 75152 bytes for 1x1 at IF=1/2 and 77264 / 104608 for 8x8. They include alignment and an 8192-byte stack reservation, not a whole-call-chain bound. These fixtures are not booted images.
- RTL, register maps, default placement and shipping-image inputs are unchanged. Full processor-only SRP suites were not rerun; the selected firmware differential was.
- The manager owns the builder bank, compiler-absent check, publication, fresh reviews, hosted gates, trusted local replication, candidate validation and containment. No hardware validation or merge approval is claimed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are fully satisfied after integration
- [x] New or changed behavior has self-checking tests
- [x] Assigned Round 6 local verification passes
- [ ] Complete candidate and hosted verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive at the new head
- [ ] External review is positive at the new head
- [ ] Findings are fixed and re-reviewed at the new head
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
