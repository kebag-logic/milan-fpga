[A605]

## Contents

- **[Status](#status)** -- Implementation and validation state.
- **[Linked Issue / roles](#linked-issue--roles)** -- Task and independent reviewers.
- **[Description](#description)** -- Counter and notification behavior.
- **[Authoritative references](#authoritative-references)** -- Rulings and contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Branch and dependencies.
- **[How to validate](#how-to-validate)** -- Reproducible checks.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Pending evidence and bench work.
- **[Definition of Done](#definition-of-done)** -- Remaining review and merge obligations.

## Status

Implementation committed at `acadfacd52c6daabf892d6ebe99da11ca06748cb`,
`726-stream-counters` -> `dev`. Affected suites and mutation campaigns pass; ready for independent review.
The routed shipping image uses 49,427 LUT (+35 against the supplied baseline),
53,378 FF and 87.5 BRAM tiles. Routed WNS is +0.451 ns and WHS +0.036 ns;
Slow/Fast reports pass on constrained paths. No push or PR action has been performed.

## Linked Issue / roles

Relates to #726

Complete acceptance is not claimed: simulation grades steady windows, and the
physical cadence, reference-peer reset comparison and controller display remain
merge-turn evidence.

Executor: `[A605]`
Internal cleared-context reviewer: `[R628]`
External reviewer: `[R629]`

## Description

AAF and CRF transmit counters count every AVTPDU and reset at each start.
CRF receive counters count every accepted AVTPDU. Receive totals reset on
binding and survive unbind. The AAF pending batch now uses all 32 bits.
Healthy input counter changes mark the descriptor dirty, restoring routine
notifications through the existing rate-limited scheduler.

The parent MAC fixture measures both descriptor geometries with two recipients.
Every steady input row-window was empty before the change and contains one
notification after it. Output row-windows contain one both before and after.
Ten planted defects require named failures and escape when their specific
checks are omitted. The unchanged firmware mailbox path passes both geometries.
Current documentation records the ruling; dated notes preserve historical data.

## Authoritative references

- Issue #726 and assignment comment 6125784157.
- Counter ruling 6125741685 and fixed-window ruling 6126028604.
- IEEE 1722.1-2021 7.4.42.2.5, Tables 7.157 and 7.159.
- Milan v1.2 Table 5.4 reset and 5.4.5.2 Table 5.22 notification spacing.
- `docs/reference/REGISTER_MAP.md` and `docs/testing/726_STREAM_COUNTERS.md`.

## How to get into the same state

```sh
git switch 726-stream-counters
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
```

Base: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
Use the repository-pinned environment and disk scratch.

## How to validate

```sh
make -C tb/verilator/tkdiag
make -C tb/verilator/crf_rx
make -C tb/verilator/avtp_rxmon
make -C tb/verilator/aaf
make -C tb/verilator/crf_tx
make -C tb/verilator/milan_dp counters counters-f5 counters-mutants
make -C tb/verilator/milan_dp
make -C tb/verilator/milan_dp unb-mutants crflic-mutants
syn/yosys/run.sh --top KL_avtp_rx_monitor_ctx --top KL_crf_rx --top KL_crf_tx --top KL_aaf_packetizer
syn/yosys/run.sh --top milan_datapath
python3 scripts/check_rtl_source_lists.py --selftest
python3 scripts/check_rtl_source_lists.py
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/check_soc_sources.py
python3 scripts/check_nvm_capture.py
python3 scripts/lint_rtl.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base c6bd08c6
python3 scripts/check_doc_paths.py
git diff --check
```

Expected result: every gate exits zero. Mutation drivers must reject the
planted fault by its named assertion and pass with that assertion group omitted.
The parent fixtures pass 98 and 427 checks at the shipping and largest shapes.
Steady input row-windows change from zero before the fix to one after it.
Minimum/maximum gaps are 1000.996/1001.867 ms at shipping shape and
1000.982/1012.029 ms at largest shape. Each gap stays within 1000 ms plus
that descriptor's measured service delay. All ten new plants fail by name
and escape with their corresponding check omitted.

The complete parent recipe passes when executed in foreground steps, including
media_aclk: 193 checks, 0 failures. The handoff records each gate and evidence hash. The full repository sweep,
all unrelated synthesis tops, hosted checks and independent review remain
required before marking a PR validated or merging.

## Known limitations / out of scope

- The fixed-window measurement grades steady windows 2 through 4; startup
  windows 0 and 1 are retained but not graded, and some input rows are empty.
- Protocol time is compressed; physical cadence is not established by simulation.
- Maximum controller fanout is not measured.
- The reference-peer comparison and controller display are merge-turn bench work.
- No firmware implementation or saved-state capture input changed; its guard passes.
- The legacy bench classifier still accepts historical readings; merge-turn
  acceptance must use the current packet ruling.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
