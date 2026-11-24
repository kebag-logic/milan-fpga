[A829]

## Description

The Arty split image now retains its required one AAF talker, one AAF listener and one CRF input at exactly 80 MHz sys/CPU and 50 MHz datapath. Its `(1,1,2)` FPGA scheduler point uses independently measured costs, a 950 us slice and 9 ms pace. All five owner bounds pass across the complete 145-case campaign: load 0.4966771140, txL 48.74 ms, maximum pass 1.6813375 ms, last notice 121.84 ms and ACMP 28.82 ms.

MII advertises only 100BASE-TX full duplex under Milan v1.2 4.2.1 and IEEE 802.1BA-2011 Table 6-1 and 6.5. The port includes split boot/region support and configuration-gated writable timestamp corrections. Seven held-egress misses retain their authorized, independently measured 80 MHz ledger; a new or larger miss still fails. Existing scheduler rows and AX7101 generated/product artifacts remain byte-identical. No Linux scheduling entry is added.

The new Arty firmware ledger records a 159532-byte ELF and 44/56 RAMB36 equivalents. All three directives completed; ExtraTimingOpt is selected at worst WNS 0.617 ns and WHS 0.017 ns. All four reports meet the floor, and copied deployment inputs pass offline identity checks.

## Linked Issue / roles

Closes #878
Relates to #665, #818, #829, #894, #983

Target: `pf-arty-split-1` -> `dev-soft-core`.
Executor: `[A829]`.
Internal cleared-context reviewer: pending assignment.
External reviewer: pending assignment.

## Authoritative references

- [Issue #878 and its three owner rulings](https://github.com/kebag-logic/milan-fpga/issues/878).
- Milan v1.2 7.2.2/7.2.3 and 4.2.1; IEEE 802.1BA-2011 Table 6-1 and 6.5.
- `ctrl_loop.h`, THE SHAPES and THE SHARE; `docs/design/SPLIT_CONTROL_MEMORY.md`, section 15.
- `docs/AAF_LATENCY_TAPS.md`, `docs/litex/CLOCK_DOMAINS.md`, `docs/integration/BUILDING.md`.

## How to get into the same state

Local commit `248d85c1453213b0f1642967a4046f395c82c56b` on base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`. The branch has not been pushed. The round-4 report and receipt index contain exact source, firmware, trace and deployment-input hashes and reproducible command records.

## Validation

- Four complete firmware shards, including Arty host and RV32 cases: PASS.
- All 145 service cases across eight variants, complete cost census and all six qualification checks: PASS; 297 grader mutants caught.
- Arty boot, six native controls, six planted defects and eight placement controls: PASS.
- Region decode and both original mutants, plus wrong-clock controls: PASS.
- MII policy: eight host cases and seven planted defects pass.
- Writable timestamp integration: 237 checks pass; seventeen timestamp and nine shadow defects caught.
- Exact clocks and VCO, existing scheduler-row identity, 42 AX generated/product and thirteen raw SoC-export comparisons: PASS.
- Builder checks, RTL lint, front-end checks and eleven final documentation gates: PASS for executed checks; historical area calibration skipped for its absent external reference.

## Limitations and remaining work

The seven held-egress rows remain recorded misses against 20 ms; their ledger is not a normative wait allowance. AX identity covers generated artifacts, full firmware images and controlled SoC exports; AX bitstreams were not rebuilt. The manager performs the bench after IMAGE READY. Independent reviews, hosted checks and candidate-merge validation remain pending. No push or hardware operation occurred.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied, including the manager's bench work
- [x] Changed behavior has self-checking tests
- [ ] Full required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] Changed contracts and the Arty memory ledger are documented
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated
- [ ] Post-merge containment is checked before the Issue moves to Done
