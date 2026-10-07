[A560]

## Contents

- **[Status](#status)** -- Candidate and validation.
- **[Linked Issue / roles](#linked-issue--roles)** -- Task and independent review.
- **[Description](#description)** -- Bare-metal SRP behavior.
- **[Round 5](#round-5)** -- Public pin and regression staging.
- **[Authoritative references](#authoritative-references)** -- Applicable contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Dependencies and environment.
- **[How to validate](#how-to-validate)** -- Reproducible checks.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Integration and release evidence.
- **[Definition of Done](#definition-of-done)** -- Remaining merge bar.

## Status

Round 5 REVIEW READY locally: `665-f4-srp` -> `dev`, head `500b8f64443777685e6a54049d933476710d26f0`. All 102 recorded round-5 commands exit 0; all 100 control plants and 70 SRP plants are caught. The unchanged 15-file coverage ratchet passes at 100% lines and branches after existing exclusions.

PR #690 already contains round-4 head `6f7deea15a9160761b30aaa93fe152f20d416695`, with both reviews POSITIVE. This new head awaits publication and fresh independent review. The manager retains the builder bank and compiler-absent check under assignment 6037276691. This status supersedes the stale local-validation STOP and publication wording identified by R532-2-R2.

## Linked Issue / roles

Relates to #665.

Executor: `[A560]`.
Internal cleared-context reviewer: `[R532]`.
External reviewer: `[R533]`.
Prior positives apply to round 4; reviewers own new verdicts, finding closure and the lens ledger.

## Description

Provide per-interface MSRP and MVRP through the bare-metal mailbox, using pinned lwSRP and entity-sized static pools. Startup declares every output, Class A Domain and its VLAN. Bound sinks reconcile Listener declarations; licences follow admission, registration and committed membership. Refused TX retains bytes and interface until commit. Firmware uses neither an OS nor a heap.

Earlier corrections recover held link changes, preserve shared Applicant state by StreamID, withdraw stale Ready, and keep the current Domain VLAN after final unbind. Wire regressions cover both slot orders and every interface, with matching plants.

## Round 5

Pin `third_party/lwSRP` to public main `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`, including merged upstream PR #12: atomic receive validation, higher-version skips, propagation retention on allocation refusal, pending-Flush snapshots, LV changed-value indications and callback ordering. Compiled dependency sources remain unmodified; no production adapter change is needed.

Four allocation-exhaustion tests now finish mailbox reception before exhausting the static pool and running the adapter poll. The new dependency reserves propagation storage before receive indications, so the old setup refused RX before reaching the allocation under test. Tests retain original refusal, retry, binding and reset assertions, including minimum-held-block checks. Existing named plants still discriminate each path.

Inventory, fetch guidance, CI descriptions and the generated submodule diagram now describe the public pin. Generated files came only from their generator. Production adapter code, pool sizes, ratchet and exclusions are unchanged.

Local dependency branch `f4-applicant-notes-r5` contains merge `ced667d8ee35929ab5f9e77a1c5396e173a693d8`, with parents `72209a53a241cd5de4786d3e1b3aefcbdf5fa5d9` and `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`. Its production sources equal public main. Both profiles pass 87 tests, three behavior scenarios and all 94 reversals: 19901 assertions with the profile disabled, 19889 enabled. The manager publishes this test branch before its dependency PR. The parent uses the already-public main pin.

## Authoritative references

- Issue #665 assignments 6030279477, 6033558691, 6035166787, 6036454509 and 6037276691; validation ruling 6036016117.
- `REQUIREMENTS.md` section 1; `docs/design/MAILBOX_SPLIT.md`; `docs/reference/FR_NFR.md`, NFR-SCOUT-02/03/08 and SRP hooks.
- Milan v1.2 4.2.7.2.2, 4.3.2, 5.5.2.7 and Table 4.3; IEEE 802.1Q-2018 Tables 10-3/10-4, 10.7.11, 35.1.2.2, 35.2.2.7.2 and 35.2.6.
- #608, #678, #679 and processor #134; `sw/firmware/ctrl/srp/README.md` records the selected processor differences.

## How to get into the same state

After publication, set disk-scratch, documentation-environment and compiler locations for the local installation:

```sh
git fetch origin 665-f4-srp
git switch --detach 500b8f64443777685e6a54049d933476710d26f0
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
export TMPDIR="$SCRATCH"
export PYTHONDONTWRITEBYTECODE=1
export PATH="$DOCS_ENV/bin:$PATH"
python3 scripts/ci_rv32_sdk.py --destination "$SDK"
export MILAN_RV32_CC="$SDK/bin/riscv32-buildroot-linux-gnu-gcc"
export VERILATOR="$PINNED_VERILATOR"
export VERILATOR_JOBS=2
```

Use HDL compiler release 5.050 and the CI-pinned ilp32d SDK distribution with the gate's RV32I/ILP32 freestanding flags. lwSRP permits anonymous HTTPS checkout. Keep products in disk scratch; cap campaigns at four workers, simultaneous HDL builds at two, and inner build jobs at eight.

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$SCRATCH/firmware-final"
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$SCRATCH/coverage-final"
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/mailbox/gen_mailbox.py --check
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/docs_check.py
python3 scripts/docs_check.py --selftest
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 scripts/check_submodule_docs.py
python3 scripts/check_diagram_pngs.py
python3 scripts/check_doc_paths.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base 6f7deea15a9160761b30aaa93fe152f20d416695
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_hygiene.py --check
git diff --check 6f7deea15a9160761b30aaa93fe152f20d416695 HEAD
```

For the mailbox gate, use a tracked copy in scratch and a wrapper around the pinned compiler that caps inner jobs at eight:

```sh
git archive --format=tar --output "$SCRATCH/mailbox-inputs.tar" HEAD tb/verilator/mbx tb/common hdl/milan/mailbox sw/firmware/ctrl sw/mailbox
mkdir -p "$SCRATCH/mailbox"
tar -xf "$SCRATCH/mailbox-inputs.tar" -C "$SCRATCH/mailbox"
make -C "$SCRATCH/mailbox/tb/verilator/mbx" -j2 VERILATOR="$HDL_J8_WRAPPER"
```

Run both dependency profiles at the notes-merge head using the unit and behavior suites plus `tests/check_reversals.py --work-dir <scratch> --prefix <unit-test-prefix> --milan OFF` or `ON`. ROUND5-GATES.md in the handoff packet expands those commands, all 76 assigned documentation-bank commands, archive checks and four linked-size commands. It records all 102 successful invocations and durations; ROUND5-GATES.json records raw and retained log hashes. HANDOFF.md contains file positions, test-to-defect maps, coverage and gate tables.

Expected result: every command exits 0; all plants fail their named observable; all 15 measured files stay at 100% after unchanged exclusions. Firmware positives include 53 adapter, three debug, four latency and five selected processor-wire cases per interface count, five entity shapes at IF=1/2, and target builds. Mailbox gates pass both buses at IF=1/2, model checks, 13 cosimulation checks and five plants.

## Known limitations / out of scope

- ACMP composition, live MAAP/stream inputs and the connected fabric licence output remain integration work; F3 is absent from the assigned base.
- Host timing uses one shared 10 ms budget and documented access/CPU allowances. Largest service time is 1020400 ns; the 11 ms full-ring stall is rejected. Target scheduling and physical timing need separate release evidence.
- New linked spans are 54592 / 65840 bytes for 1x1 at IF=1/2 and 69280 / 95296 for 8x8, up 624 / 624 / 624 / 640 bytes. Pools are unchanged. Spans include alignment and an 8192-byte stack reservation, not a whole-call-chain bound. These are size fixtures, not booted images.
- No RTL, default all-fabric build, register map or shipping-image input changed. Full processor-only suites were not rerun in round 5; the selected firmware differential was.
- The manager owns the builder bank, compiler-absent check, publication of both local heads, fresh reviews, hosted checks, trusted local replication, dependency-test PR, candidate validation and containment. No hardware validation or merge approval is claimed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are fully satisfied after integration
- [x] New or changed behavior has self-checking tests
- [x] Assigned round-5 local verification passes
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
