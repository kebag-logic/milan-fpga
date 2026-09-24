[A226]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Correction round 1](#correction-round-1)** -- How R274-1 and R275-1 F1/F2 were answered.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN (documentation only). Every documentation gate passes at the head.

- `394-510-511-decisions` -> `dev`.
- Head: `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6`.
- Base: `759da623072358afdb0e9d570a7b4b6a788492c9`.
- Correction round 1 adds one commit on top of `64bcf768d28b4b9763fbe5917a734bcefa2a66e0`, the head that R274-1 and R275-1 reviewed.
- `sw/builder/test_builder.py` passed at `64bcf768` except one arm it could not run: gate 11 needs a local build report that is absent here. It was not re-run at this head, because the round changes only Markdown that no builder or test code reads.

## Linked Issue / roles

Closes #511

Relates to #394: acceptance 2 is not done by this documentation lane, because it needs hardware. That is the bench proof under option (a):

- ten `e1` link drops with streams bound and gPTP locked;
- the `GET_COUNTERS` increments;
- the restart time against #75;
- the same run on an `--eth-port e2` build.

Acceptance 1, 3 (not applicable under (a)) and 4 are met.

Relates to #510: acceptance 2 is met in this repository but not in the protocol processor.

- At the pinned `424c688`, its F01.5 table still lists `P-EN-MVU-SUID` / `P-EN-MVU-MCR` at 1 / 1. That repository's issue 77 owns the fix.
- Acceptance 3's byte-exact `NOT_IMPLEMENTED` evidence at the pin covers `GET_SYSTEM_UNIQUE_ID` (`0x0002`, pp_top M4) only.
- `0x0001`, `0x0003` and `0x0004` reach the same arm by inspection, with no per-command check.

Roles:

- Executor: `[A215]`; correction round 1: `[A226]`.
- Internal cleared-context reviewer: `[R274]`.
- External reviewer: `[R275]`.

## Description

This lane records the three owner decisions of 2026-09-23 as directed
limitations. Each carries its specification clause and revisit trigger. The
lane makes no RTL, firmware, builder or configuration change.

| Decision | Where it is recorded |
|---|---|
| [#394](https://github.com/kebag-logic/milan-fpga/issues/394#issuecomment-5789765478): v1.2 stays a declared non-redundant end station; Milan v1.2 Section 8 is revisited with the P4/P5 PCB (#416/#417) | README roadmap (P3 becomes a one-port link loss/return proof; P4 carries the Section 8 revisit), `REQUIREMENTS.md` Section 9 and the Milan reference row, FR_NFR FR-MVU-03, NFR-SCOUT-05, step 10, the Section 5 out-of-scope list and a Section 6 row, the compliance matrix profile row and row 8.x, roadmap Section 3 (all in commit `909d8fe` for acceptance 1) |
| [#510](https://github.com/kebag-logic/milan-fpga/issues/510#issuecomment-5789766089): the MVU SYSTEM_UNIQUE_ID and MEDIA_CLOCK_REFERENCE_INFO rows are RECOMMENDED for October; P4 implements them if the conformance lab requires it | FR_NFR FR-MVU-02 (M to S, RFC 2119 SHOULD = RECOMMENDED), the Section 2.0 ledger row and a note that says this is a decision, not a re-grade, and the Section 6 MVU row. Also compliance matrix Section 1.4, roadmap Section 3, the feature-status page's served-MVU note, and a `SUBMODULES.md` known-conflict row for the protocol processor's F01.5 |
| [#511](https://github.com/kebag-logic/milan-fpga/issues/511#issuecomment-5789766257): delayAsymmetry is excluded for v1.2; the live UART tuner stays donor-bench-only | A new design record in `docs/design/GPTP_PLANE.md` ("Propagation asymmetry is not modelled": contract, clause check, every place the term enters the arithmetic, revisit trigger, what an adoption must define and prove, ownership), a REQ-PTP-06 scope note and a Section 9 entry in `REQUIREMENTS.md`, an FR_NFR Section 2.6 scope note, out-of-scope entry and Section 6 row, compliance matrix Section 4, traceability AS-13 with an `Excluded` state, `TIME_SYNC.md` and the gPTP manager guide |

## Correction round 1

Commit `70f2c50d` answers R274-1 F1/F2 and R275-1 F1/F2, which are the same two
MINORs. It is Markdown only: 4 files, +40/-9.

**F1: every place delayAsymmetry enters the arithmetic.** `GPTP_PLANE.md` gains a "Where the term enters" table. The 2011 text with Cor1/Cor2 applies the term here:

- **11.2.13.2.1 f)** subtracts `delayAsymmetry/rateRatio` from `upstreamTxTime`.
- **10.2.12 Figure 10-9** adds `+delayAsymmetry` to `syncReceiptTime`.
- **10.2.12 Figure 10-9** adds `+delayAsymmetry/rateRatio` to `syncReceiptLocalTime`. That undoes the f) subtraction, to within the Figure 10-4 `neighborRateRatio` update, which 11.2.13.2.1 NOTE 2 calls usually negligible.
- **11.2.14.2.3 a)** carries the first term into a relayed Follow_Up. Only a port that relays another port's Sync does this (10.2.11).
- **Annex E.5.2.2 (CSN):** not applicable.
- **An 802.1AS-2020 comparison row:** with CMLDS, 11.2.17.2 a) folds the term into the mean link delay.

The net effect is stated: `syncReceiptTime` gains `delayAsymmetry`, and its paired local time does not move. The adoption "Application point" row names all three terms.

**F2: Table 14-6 and the management condition.** The "Is it managed?" row now states the Table 14-6 grade (14.6.25). Cor1's replacement table keeps this row.

- **The grade:**
  - Operations: read-write.
  - Conformance: `Tdot3FD`, "Required for time-aware IEEE 802.3 full-duplex port".
  - "(recommended)" qualifies the `scaledNs` data type, as 14.3.2 states for `offsetFromMaster`.
  - Management is optional: PICS `MGT` (A.5) is `O`. The product claims none.
- **The revisit trigger** adds "before the product claims 802.1AS management". A write to that object is a runtime correction that first needs the REQ-PTP-06 amendment.
- **The same condition is added in three more places:** the `REQUIREMENTS.md` REQ-PTP-06 scope note, the FR_NFR Section 5 out-of-scope entry and the compliance matrix Section 4 row.
- **The Units row** cites Table 14-6 for `scaledNs`, because 10.2.4.8 names no data type. R274-1 marked this point optional.

The adoption proof plan ("What an adoption must prove" through the ownership
table) is byte-identical to `64bcf768`.

## Authoritative references

- Milan v1.2 (2023-11-30):
  - Section 4.2.5: redundancy is optional; the REDUNDANCY bit.
  - Section 5.4.4.1 with Table 5.20: `features_flags` bit 31.
  - Sections 5.4.4.2 to 5.4.4.5 and 7.6: each carries the note that support is a recommendation.
  - Table 5.18 (MVU command types) and Table 5.19 (`NOT_IMPLEMENTED`).
  - Section 8.1 (not mandatory) and Section 8.3.1 (two AVB-capable ports).
- IEEE 802.1AS-2011, with Cor1-2013 and Cor2-2015, the edition of record:
  - 8.3: definition and sign; measurement not required.
  - 10.2.4.8: unmodelled means zero; no data type named.
  - 10.2.12, Figure 10-9: `syncReceiptTime` and `syncReceiptLocalTime`.
  - 11.2.13.2.1 f): `upstreamTxTime`.
  - 11.1.3 d) and e), and Table 11-5: descriptions of the same arithmetic.
  - 11.2.14.2.3 a): the relayed correction field. 10.2.11: relay only between ports.
  - 11.2.15.2.4: the Pdelay mean has no asymmetry term.
  - 14.6.9: the managed object's definition.
  - Table 14-6 (14.6.25): RW, `Tdot3FD`.
  - Annex A.5 PICS `MGT`: `O`.
  - 8.4.3: `ingressLatency` / `egressLatency`.
- IEEE 802.1AS-2020, for comparison only: 10.2.13, 11.2.14.2.1, 11.2.15.2.3 and 11.2.17.2 a) (CMLDS).
- `REQUIREMENTS.md` REQ-PTP-06 and REQ-PTP-09.
- `docs/reference/FR_NFR.md`: FR-MVU-01..03, FR-CLK-01, NFR-SCOUT-05 and NFR-REL-01.

## How to get into the same state

```sh
git fetch origin
git switch --detach 70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6
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
python3 -B scripts/check_wire_accountability.py
git diff --check 759da623 HEAD
python3 -B sw/builder/test_builder.py
make -C protocol-processor/tb/pp_top run   # the MVU fallback evidence at the pin
```

Expected result: every command exits 0.

- `check_em_dash` reports 0 findings over 230 added lines in 11 pages.
- `check_wire_accountability` reports 42 checks and 0 findings.
- `test_builder.py` ends `ALL GATES PASS EXCEPT 1 NOT RUN`, where the build report of gate 11 is absent. It was last run at `64bcf768`.
- pp_top ends `1371 checks: 1371 PASS, 0 FAIL`. That was run at the unchanged pin `424c688`.

## Known limitations / out of scope

- The #394 bench proof (acceptance 2) needs the two-board bench (#117) and is
  not attempted here.
- The protocol processor's F01.5 MVU parameter claim, and a per-command
  `NOT_IMPLEMENTED` arm for `0x0001`, `0x0003` and `0x0004`, belong to that
  repository (issues 55, 56 and 77). They are recorded here as a known conflict,
  not fixed.
- `CHANGELOG.md`, `docs/integration/BAREMETAL_FIRMWARE.md` and
  `docs/ENDSTATION_BUILDER.md` are held by other lanes and untouched. No
  acceptance criterion needs them.
- `docs/testing/MILAN_V12_AUDIT_2026-08-16.md` is a dated record and is not
  rewritten. It already names the non-redundant profile.
- Stated for review: the #511 revisit trigger is derived, not owner-stated. It has three conditions:
  - a second cabled port;
  - a claim of 802.1AS management (added in correction round 1 for F2);
  - a REQ-PTP-06 amendment before any runtime correction.

  The first and third come from the two grounds the decision cites; the second comes from Table 14-6.
- These optional SUGGESTIONs are not taken:
  - R275-1 S2: gate AS-13 in `check_gptp_docs.py`.
  - R275-1 S3 = R274-1 S1: a builder test that plants an asymmetry key.
  - R275-1 S4: label AS-13's clause edition.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#511 yes; #394 and #510 partly, see above)
- [ ] New or changed behavior has self-checking tests (no behavior change)
- [x] Required local verification bar passes (documentation gates; builder tests at `64bcf768`, Markdown-only since)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed (R274-1/R275-1 F1 and F2 fixed at `70f2c50d`; re-review pending)
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
