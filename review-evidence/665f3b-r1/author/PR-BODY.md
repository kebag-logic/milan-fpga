[A612]

## Contents

- **[Status](#status)** -- Local evidence and branch.
- **[Linked Issue / roles](#linked-issue--roles)** -- Scope and independent review.
- **[Description](#description)** -- Declaration predicate and reviewed pin.
- **[Authoritative references](#authoritative-references)** -- Rulings and contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Revision and dependencies.
- **[How to validate](#how-to-validate)** -- Reproducible gates.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Evidence boundaries.
- **[Definition of Done](#definition-of-done)** -- Remaining merge requirements.

## Status

REVIEW READY -- touched local gates pass. `665-f3b-parent` -> `dev`.
Base: `d40e4e9827be2516f8f34b9d65f0a483fff2194c`.
Candidate: `db29bdd07529fbc697b7956827092f64b1241714`.
Parent mutations: 519 control, 76 AECP and 278 SRP caught, zero escapes.
Standalone stack: 388/388 caught. Coverage: 30 files at adjusted 100% lines/branches.
Publication census: 120 controls and 31 rule removals pass.

## Linked Issue / roles

Relates to #665.

Executor: `[A612]`.
Internal cleared-context reviewer: pending assignment.
External reviewer: pending assignment.

## Description

`DA_GATE` now requires a valid destination and either an answered probe younger
than 15000 ms or a registered Listener, matching `acmp_declaring_o`. Address
allocation alone leaves the gate closed. Each interface's gate is written before
its allocation report; idle service ticks observe probe expiry.

Listener presence is separate from the existing media licence. Asking Failed
counts as declaration demand while leaving that licence closed. Real mailbox
and SRP composition controls exercise both interfaces, withdrawal and expiry.

The stack pin moves from `405dc683` to reviewed merge `70936b77`, adopting
stack #19, #20 and #25 under the corrected scope. Parent tests cover the added
ADP short-frame, version and control-data-length refusals. The contract,
service bounds, dependency map and generated diagrams reflect the change.

The default fabric firmware binary and descriptor image are byte-identical.
Across five shapes and three firmware compositions, Release load growth is
1004 to 1320 bytes, within the 2048-byte ceiling. The handoff records every
before/after image digest, raw size, gate control and coverage/mutation row.

## Authoritative references

- [Assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6151273346).
- [Corrected F3b scope](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6151422598).
- [Release ceiling](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6126295947).
- Milan v1.2 4.3.3.1, T-SRP-DAFRESH; IEEE 1722.1 ADP reception.
- `protocol-processor/docs/architecture/05_acmp_engine.md:405`.
- `sw/mailbox/mailbox.yaml`, `docs/reference/MAILBOX_CONTRACT.md` and `docs/design/MAILBOX_SPLIT.md`.

## How to get into the same state

Use the recorded candidate commit in the implementation branch. Initialize only
the dependencies needed by these gates, then verify each is its own checkout.
The stack origin must be the public HTTPS origin recorded in `.gitmodules`.
No dependency branch changes or dependency pushes are required.

```sh
git switch 665-f3b-parent
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
for submodule in protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis; do
    test "$(git -C "$submodule" rev-parse --show-toplevel)" = "$PWD/$submodule" || exit 1
    git -C "$submodule" remote get-url origin
done
```

Use CPython 3.12.3, the repository's locked dependencies and pinned compiler
versions. Set `TMPDIR` to disk-backed scratch. Set `MILAN_RV32_CC`, `VERILATOR`
and `SV2V` to the matching executables. Keep build outputs under `$WORK`.

## How to validate

Run the four firmware shards separately, each with at most four jobs.

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4 --build-dir "$WORK/normal"
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4 --jobs 4 --build-dir "$WORK/control"
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 4 --build-dir "$WORK/aecp"
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4 --jobs 4 --build-dir "$WORK/srp"
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$WORK/coverage"
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 third_party/tsn-c-stack/scripts/validate.py --jobs 2 --work "$WORK/stack"
python3 third_party/tsn-c-stack/scripts/baremetal.py --jobs 2 --work "$WORK/stack-rv32"
python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32 --out "$WORK/image-controls"
python3 sw/mailbox/gen_mailbox.py --check --crosscheck --selftest
python3 sw/mailbox/publication_census.py --check --selftest --jobs 2
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_rtl_source_lists.py --selftest
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
python3 scripts/lint_rtl.py --check --self-test --jobs 2
python3 scripts/docs_check.py
python3 scripts/check_submodule_docs.py
python3 docs/diagrams/submodule_boundaries.gen.py --check
```

Expected result: every command returns zero, every planted defect is caught,
and firmware coverage is 100% lines/branches after documented exclusions.
The image table uses the repository image generators and equal toolchains on
both sides; the handoff includes the remaining documentation controls and
complete image reproduction details.

## Known limitations / out of scope

- No shipping placement switch, hardware access, flashing or bitstream build.
- Experimental image fixtures prove link/ABI and growth; they do not establish shipping RAM fit or physical timing.
- No existing DA_GATE/acmp_declaring_o differential was found; predicate controls run through the firmware composition.
- Local evidence does not supply independent review, hosted contexts, candidate-merge validation or post-merge containment.
- This assignment prohibits pushing and changing a PR. This body is prepared for later publication.

## Definition of Done

- [x] Assigned F3b acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Touched local verification gates pass
- [ ] Full repository merge validation passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
