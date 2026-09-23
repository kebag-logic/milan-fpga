[A215]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN (documentation only). Every documentation gate passes at every commit, and
`sw/builder/test_builder.py` passes at the head except one arm it could not run
(gate 11 needs a local build report that is absent here). `394-510-511-decisions`
-> `dev`, head `64bcf768d28b4b9763fbe5917a734bcefa2a66e0`, base `759da623072358afdb0e9d570a7b4b6a788492c9`.

## Linked Issue / roles

Closes #511
Relates to #394: acceptance 2 (the bench proof under option (a): ten `e1` link
drops with streams bound and gPTP locked, the `GET_COUNTERS` increments, the
restart time against #75, and the same run on an `--eth-port e2` build) needs
hardware and is not done by this documentation lane. Acceptance 1, 3 (not
applicable under (a)) and 4 are met.
Relates to #510: acceptance 2 is met in this repository but not in the protocol
processor. At the pinned `424c688` its F01.5 table still lists
`P-EN-MVU-SUID` / `P-EN-MVU-MCR` at 1 / 1, which that repository's issue 77
owns. Acceptance 3's byte-exact `NOT_IMPLEMENTED` evidence at the pin covers
`GET_SYSTEM_UNIQUE_ID` (`0x0002`, pp_top M4) only. `0x0001`, `0x0003` and
`0x0004` reach the same arm by inspection, with no per-command check.

Executor: `[A215]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

This lane records the three owner decisions of 2026-09-23 as directed
limitations, each with its specification clause and revisit trigger. It makes
no RTL, firmware, builder or configuration change.

| Decision | Where it is recorded |
|---|---|
| [#394](https://github.com/kebag-logic/milan-fpga/issues/394#issuecomment-5789765478): v1.2 stays a declared non-redundant end station; Milan v1.2 Section 8 is revisited with the P4/P5 PCB (#416/#417) | README roadmap (P3 becomes a one-port link loss/return proof; P4 carries the Section 8 revisit), `REQUIREMENTS.md` Section 9 and the Milan reference row, FR_NFR FR-MVU-03, NFR-SCOUT-05, step 10, the Section 5 out-of-scope list and a Section 6 row, the compliance matrix profile row and row 8.x, roadmap Section 3 (all in commit `909d8fe` for acceptance 1) |
| [#510](https://github.com/kebag-logic/milan-fpga/issues/510#issuecomment-5789766089): the MVU SYSTEM_UNIQUE_ID and MEDIA_CLOCK_REFERENCE_INFO rows are RECOMMENDED for October; P4 implements them if the conformance lab requires it | FR_NFR FR-MVU-02 (M to S, RFC 2119 SHOULD = RECOMMENDED), the Section 2.0 ledger row and a note that says this is a decision, not a re-grade, and the Section 6 MVU row. Also compliance matrix Section 1.4, roadmap Section 3, the feature-status page's served-MVU note, and a `SUBMODULES.md` known-conflict row for the protocol processor's F01.5 |
| [#511](https://github.com/kebag-logic/milan-fpga/issues/511#issuecomment-5789766257): delayAsymmetry is excluded for v1.2; the live UART tuner stays donor-bench-only | A new design record in `docs/design/GPTP_PLANE.md` ("Propagation asymmetry is not modelled": contract, clause check, revisit trigger, what an adoption must define and prove, ownership), a REQ-PTP-06 scope note and a Section 9 entry in `REQUIREMENTS.md`, an FR_NFR Section 2.6 scope note, out-of-scope entry and Section 6 row, compliance matrix Section 4, traceability AS-13 with an `Excluded` state, `TIME_SYNC.md` and the gPTP manager guide |

## Authoritative references

- Milan v1.2 (2023-11-30): Section 4.2.5 (redundancy optional; REDUNDANCY bit),
  Section 5.4.4.1 with Table 5.20 (`features_flags` bit 31), Sections 5.4.4.2
  to 5.4.4.5 and 7.6 (each carries the note that support is a recommendation),
  Table 5.18 (MVU command types), Table 5.19 (`NOT_IMPLEMENTED`), Section 8.1
  (not mandatory) and Section 8.3.1 (two AVB-capable ports).
- IEEE 802.1AS-2011 (with Cor1-2013): 8.3 (definition and sign; measurement not
  required), 10.2.4.8 (unmodelled means zero), 10.2.12 and 11.2.13.2.1 (where the
  term enters), 11.2.15.2.4 (the Pdelay mean has no asymmetry term), 14.6.9
  (managed object, recommended), 8.4.3 (`ingressLatency` / `egressLatency`).
- `REQUIREMENTS.md` REQ-PTP-06 and REQ-PTP-09; `docs/reference/FR_NFR.md`
  FR-MVU-01..03, FR-CLK-01, NFR-SCOUT-05, NFR-REL-01.

## How to get into the same state

```sh
git fetch origin
git switch --detach 64bcf768d28b4b9763fbe5917a734bcefa2a66e0
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

## How to validate

```sh
python3 -B scripts/docs_check.py
python3 -B scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9
python3 -B scripts/check_feature_status.py --self-test
python3 -B scripts/check_baremetal_only.py --check
python3 -B docs/traceability/gen_module_matrix.py --check
python3 -B scripts/check_gptp_docs.py --with-submodule
python3 -B scripts/check_doc_style.py
python3 -B scripts/gen_toc.py --check
python3 -B scripts/gen_toc.py --verify-anchors
python3 -B scripts/check_doc_paths.py
python3 -B scripts/check_submodule_docs.py
git diff --check 759da623 HEAD
python3 -B sw/builder/test_builder.py
make -C protocol-processor/tb/pp_top run   # the MVU fallback evidence at the pin
```

Expected result / pass criteria: every command exits 0. `check_em_dash` reports
0 findings over 199 added lines in 11 pages. `test_builder.py` ends
`ALL GATES PASS EXCEPT 1 NOT RUN` where the build report of gate 11 is absent.
pp_top ends `1371 checks: 1371 PASS, 0 FAIL`.

## Known limitations / out of scope

- The #394 bench proof (acceptance 2) needs the two-board bench (#117) and is
  not attempted here.
- The protocol processor's F01.5 MVU parameter claim and a per-command
  `NOT_IMPLEMENTED` arm for `0x0001`, `0x0003` and `0x0004` belong to that
  repository (issues 55, 56 and 77). They are recorded here as a known conflict,
  not fixed.
- `CHANGELOG.md`, `docs/integration/BAREMETAL_FIRMWARE.md` and
  `docs/ENDSTATION_BUILDER.md` are held by other lanes and untouched. No
  acceptance criterion needs them.
- `docs/testing/MILAN_V12_AUDIT_2026-08-16.md` is a dated record and is not
  rewritten; it already names the non-redundant profile.
- Stated for review: the #511 revisit trigger (a second cabled port, or a
  REQ-PTP-06 amendment before any runtime correction) is derived from the two
  grounds the decision cites.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#511 yes; #394 and #510 partly, see above)
- [ ] New or changed behavior has self-checking tests (no behavior change)
- [x] Required local verification bar passes (documentation gates; builder tests)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
