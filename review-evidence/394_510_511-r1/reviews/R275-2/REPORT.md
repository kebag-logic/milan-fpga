[R275] POSITIVE - exact head 70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6

Round R275-2. External, cleared-context review of issue #511 / PR #537.

- Head `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6`, tree
  `ef96bf2fe0d66dd9c0b1ba45c6b4300d89ba658c`.
- Source base `759da623072358afdb0e9d570a7b4b6a788492c9`, an ancestor of the
  head. Seven linear one-line commits, with no bodies and no trailers.
- Eleven Markdown files changed, +230/-26. No non-Markdown file and no
  gitlink changed (`receipts/diff-identity.txt`).
- Correction round 1 is the single commit `70f2c50d` on `64bcf768`: four
  pages, +40/-9. Its diff hashes to the same value as the executor's
  published round patch.

All five lenses were applied to the whole PR at this head, not only to the
correction round.

Reconstructed from, in this order:

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. The #511 body and all its comments: the owner decision, both
   assignments, and the [A215] and [A226] REVIEW READY comments.
3. The PR body and the manager's round-start comments.
4. REQUIREMENTS.md, FR_NFR.md, the compliance matrix and the traceability
   page.
5. The local IEEE 802.1AS-2011, Cor1-2013, Cor2-2015 and 802.1AS-2020 texts,
   802.1BA-2011 and Milan v1.2.
6. The diff and its history.
7. The public packet at `9c71d05f` (`review-evidence/394_510_511-r1`),
   `author/` and `correction-a226/` only.
8. The exact-head hosted check runs.

The prior review reports (R274-1, R275-1) were read only after this round's
verdict and ledger were written (`receipts/verdict-before-prior-findings.txt`,
then `receipts/prior-findings-read.txt`).

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head. All five
lenses are covered clean. Five optional SUGGESTIONs follow; none affects
coverage.

Both MINORs from the previous round (R274-1 F1/F2 = R275-1 F1/F2) are
resolved at this head. The verification follows.

## Correction round: verified against the standard

Line numbers on the right are lines of the text extraction recorded in
`receipts/standards-clause-receipts.txt`, with the PDF hashes.

| Record statement at this head | 802.1AS text | Result |
|---|---|---|
| `GPTP_PLANE.md:385` 11.2.13.2.1 f): `upstreamTxTime = <syncEventIngressTimestamp> - neighborPropDelay/neighborRateRatio - delayAsymmetry/rateRatio` | 2011 lines 7396-7401 (7399); Cor1 1947-1952, restated unchanged | Matches |
| `:386` Figure 10-9 `syncReceiptTime ... + delayAsymmetry` | 2011 lines 4614-4615 | Matches |
| `:387` Figure 10-9 `syncReceiptLocalTime = upstreamTxTime + neighborPropDelay/neighborRateRatio + delayAsymmetry/rateRatio` | 2011 lines 4616-4617 | Matches. Cor1 changes only 10.2.12.2.1 prose (line 1206), not the figure |
| `:387` The two `rateRatio` values differ by the Figure 10-4 update, which NOTE 2 calls usually negligible | 11.2.13.2.1 e) uses the Follow_Up value; Figure 10-4 adds `neighborRateRatio - 1.0` (4026); NOTE 2 ends "The same is true of any delayAsymmetry" (7409-7411) | Matches |
| `:388` 11.2.14.2.3 a) carries the first term in a relayed Follow_Up; 11.1.3 e) and Table 11-5 describe it; only a relaying port (10.2.11) | 7548-7562; 6938-6944; Table 11-5 8464-8475; 10.2.11 sends only on a MasterPort (4440-4447) | Matches. A one-port slave never sends; a one-port grandmaster's PortSyncSync comes from ClockMasterSyncSend, which carries no asymmetry term |
| `:389` Annex E.5.2.2: a CSN egress port reads the 10.2.12 inputs, delayAsymmetry included, from the TLV | 17060-17071 | Matches; not applicable (AS-11) |
| `:392-394` Net effect: `syncReceiptTime` gains delayAsymmetry and `syncReceiptLocalTime` does not move; omitting the local-time term roughly doubles the shift | Follows from the three formulas above | Correct |
| Completeness: "applies it only here" (`:380`) | All 47 extracted 2011 lines naming delayAsymmetry were classified (`receipts/delayasymmetry-line-census.txt`). The arithmetic lines are Figure 10-9 (2), 11.2.13.2.1 f) (3, with its NOTEs) and the Annex E.5.2 CSN lines (4). The rest are definitions (8.3, 10.2.4.8, 14.6.9), prose (11.1.3, 11.2.5, Table 11-5) or management (Table 14-6 and 20 Clause 15 MIB lines). 11.2.14.2.3 carries the term through `upstreamTxTime` without naming it. Cor2 changes only Figure 11-8 and has no asymmetry text (line 365) | Complete for the 2011 edition of record |
| `:360` Table 14-6 (14.6.25): RW, `Tdot3FD`, "Required for time-aware IEEE 802.3 full-duplex port"; "(recommended)" qualifies `scaledNs`, as 14.3.2 does for `offsetFromMaster`; 14.6.9 does not grade it; Cor1 keeps the row | 2011 11189-11226 and 14.6.9 at 11063-11067; 14.3.2 at 10706-10710 with Table 14-2 row 10782-10783; Cor1 2648-2689 | Matches (S1 concerns only the `MGT` wording) |
| `:418` Units: `scaledNs` from Table 14-6; 10.2.4.8 names no data type | 3802-3804; its neighbours 10.2.4.5-10.2.4.7 each name one | Matches |
| Revisit trigger with the management condition | `GPTP_PLANE.md:402-410`, `REQUIREMENTS.md:141-146`, `FR_NFR.md:421-424`, `MILAN_COMPLIANCE_MATRIX.md:226`. Every page that restates the trigger now carries the condition. `git grep` finds no remaining "recommended" grade for the object | Consistent |

## Findings

All five are SUGGESTION: optional, and outside coverage.

### S1 - SUGGESTION - Conformance, Docs - `docs/design/GPTP_PLANE.md:360`, `docs/reference/MILAN_COMPLIANCE_MATRIX.md:226` - the `MGT` item is worded for Bridges

- **Authority/evidence:** 802.1AS-2011 A.5 `MGT` reads "Is management of
  the timing synchronization in Bridges supported?", with status `O` and
  reference Clause 15 (lines 15166-15167). Cor1 does not change A.5.
  - For an end station, optionality rests on more than `MGT`: Clause 5.3
    lists no Clause 14 or 15 obligation, and A.5 `MIB` is also `O`
    (line 15132).
  - 802.1BA-2011 adds no management requirement: it has no MIB or
    management-of line.
- **Impact:** none on the decision. "Management is optional" is correct. A
  cold reader who opens `MGT` sees only Bridge wording, and has to infer
  the end-station case.
- **Required outcome (optional):** cite 5.3 and the `MIB` item next to
  `MGT`, or say that `MGT` is worded for Bridges.
- **Verification:** read the two cells against A.5 and 5.3.

### S2 - SUGGESTION - Tests - `sw/builder/endstation_builder.py:3940-3948` - no permanent arm plants an asymmetry key (retains R274-1 S1 = R275-1-S3)

- **Authority/evidence:** "Can a configuration set it? No"
  (`GPTP_PLANE.md:361`) and REQUIREMENTS.md's "No configuration key ...
  sets an asymmetry" both rest on the `_known_gp` whitelist.
  `sw/builder/test_builder.py` has no unknown-`gptp`-key arm. This round's
  disposable probe shows the claim holds at this head
  (`receipts/probe-builder-asym-key.txt`):
  - the shipped `endstation_ax7101_1x1_tdm8.yaml` loads, and so does a
    scratch round-trip copy;
  - four planted keys (`delay_asymmetry_ns`, `delayAsymmetry`,
    `delay_asymmetry`, `asymmetry_ns`) are each refused by name, both
    through `_load_gptp` and end to end through `load_config`.
- **Impact:** none today. If `_known_gp` were later widened, no gate would
  catch it.
- **Required outcome (optional):** a builder arm that plants such a key and
  requires the refusal.
- **Verification:** the arm fails when the key is added to `_known_gp`.

### S3 - SUGGESTION - Tests, Docs - `docs/design/GPTP_PLANE.md:430-439` - the proof plan has no dropped-term mutation

- **Authority/evidence:** the record now names this failure mode itself
  (`:394`: omitting the `syncReceiptLocalTime` term roughly doubles the
  shift). The proof plan names a sign-swap mutation but no term-omission
  mutation. "Positive and negative" ("moves by the configured value")
  catches a doubling only if the adopting lane grades the magnitude.
- **Impact:** none now, because nothing is implemented. Acceptance 3's
  "exact arithmetic/sign discrimination" is met by the magnitude wording.
- **Required outcome (optional):** name a dropped-term mutation arm next to
  "Sign".
- **Verification:** the adopting lane's suite fails with that term deleted.

### S4 - SUGGESTION - Docs - `docs/design/GPTP_PLANE.md:390` - the 2020 row cites only 11.2.17.2 a)

- **Authority/evidence:** 802.1AS-2020 11.2.17.2 lists the CMLDS
  differences as a) to f) (lines 11108-11145).
  - Items b) and f) also route delayAsymmetry, through the Pdelay_Req
    `correctionField` and the `neighborRateRatio` computation.
  - 10.2.13 still applies both ClockSlaveSync terms (lines 5728-5730).
- **Impact:** none for the 2011 edition of record. The row is informative.
- **Required outcome (optional):** cite "11.2.17.2 a) to f)".
- **Verification:** read the row against 11.2.17.2.

### S5 - SUGGESTION - Docs, Conformance - `docs/traceability/ieee8021as.md:49` - AS-13 has no edition label (retains R275-1-S4)

- **Authority/evidence:** AS-13 cites the 2011 numbers 10.2.4.8 and 14.6.9.
  The 2020 equivalents are 10.2.5.9 and 14.8.10/14.16.8. The same table
  uses 2020 numbering elsewhere: AS-8 cites 11.2.19, the 2020 MDPdelayReq
  clause. The page header allows 2020 citations for hardware-assist context.
- **Impact:** a reader could look the clause up in the wrong edition.
- **Required outcome (optional):** label AS-13's clauses 802.1AS-2011.
- **Verification:** read the row.

## Per-lens results

```text
[R275] PASS Conformance - docs/design/GPTP_PLANE.md:348-455, REQUIREMENTS.md:130-148,275-279, docs/reference/FR_NFR.md:228-236,416-424,444, docs/reference/MILAN_COMPLIANCE_MATRIX.md:226, docs/traceability/ieee8021as.md:49 at 70f2c50d; receipts/standards-clause-receipts.txt, receipts/delayasymmetry-line-census.txt - every arithmetic, management and units statement checked line by line against 802.1AS-2011 (+Cor1, +Cor2) 8.3, 8.4.3, 10.2.4.5-8, 10.2.11, 10.2.12/Fig 10-9, Fig 10-4, 11.1.3, 11.2.13.2.1, 11.2.14.2.3, Table 11-5, 11.2.15.2.4, 14.3.2, 14.6.9, Tables 14-2/14-6, A.5, A.7, E.5.2 (all 47 delayAsymmetry lines classified); the 2020 row against 10.2.13, 11.2.14.2.1, 11.2.15.2.3, 11.2.17.2; Milan v1.2 4.2.1/4.2.5/4.2.6, 5.4.4.1-5, Tables 5.18-5.20, 7.6, 8.1, 8.3.1 and 802.1BA-2011 for the #394/#510 rows and the "Milan never mentions asymmetry" claim (0 hits); #511 acceptance 1-5 met with the owner decision 5789766257; S1, S5 optional
[R275] PASS RTL - receipts/diff-identity.txt (11 *.md, 0 hdl/sw/config/gitlink changes) and the RTL the record cites: hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:115-116,259-269,345,986; KL_gptp_txret.sv:147,283; hdl/milan/milan_datapath.sv:99-100,1478-1479,6771-6772; receipts/asym-census.txt - the two elaboration constants are applied once inside the shadow hierarchy and published at GPTP_LAT; no asymmetry identifier in hdl sw configs avdecc scripts tb (exit 1); the gPTP processor pin c1b6174 names asymmetry only under docs/history/v1/prototype (hdl/syn/scripts/tb/bench exit 1); protocol-processor 424c688 hdl has no MVU SUID/MCR parameter and only command_type 0x0000 takes the GET_MILAN_INFO arm (KL_aecp_engine.sv:707,1290-1296)
[R275] PASS Robustness - sw/builder/endstation_builder.py:3940-3948 driven by scripts/probe_builder_asym_key.py (receipts/probe-builder-asym-key.txt) - malformed-configuration path: shipped-config and round-trip controls load, 4 planted asymmetry keys x 2 entry points refused naming the key; adoption contract rows for range, default/reset, update, sign and double compensation (GPTP_PLANE.md:412-424) checked against the #511 scope and REQ-PTP-06/09; option-off and one-port scope unchanged by the diff
[R275] PASS Tests - receipts/docs-gates-at-head.txt, receipts/hosted-check-runs-at-head.tsv, receipts/consumers-of-round-pages.txt, receipts/proof-plan-unchanged.txt - no test or gate file changed; 26 documentation gate commands exit 0 at this head, including em-dash vs both bases and its 57-arm selftest, feature-status 46/46, gPTP-docs 30 controls, solution-docs 43 controls, baremetal-only 377 arms, TOC/anchors/paths, diagram checks and git diff --check; hosted: 8 contexts executed and succeeded, 7 skipped; no executable consumer reads the four pages this round changed, so the executor's builder and pp_top results at 64bcf768 and the unchanged pin are not invalidated; the adoption proof plan is byte-identical to 64bcf768 and names a failing condition per arm; S2, S3 optional
[R275] PASS Docs - all 11 changed pages at 70f2c50d; receipts/fragment-check.txt; receipts/commit-hygiene.txt - new and cross-page anchors resolve (0 bad); every restatement of the #511 trigger carries the management condition; no stale "recommended" grading; the three owner-decision links resolve to the decisions they cite; commits one line, no body, no trailers; the [A226] REVIEW READY explicitly supersedes the two [A215] statements R274-1 named; the PR body and the issue let a cold reader reconstruct the round; S1, S3, S4, S5 optional
```

## Prior public review findings

| Prior finding | Severity | Lenses | Disposition at `70f2c50d` | Evidence |
|---|---|---|---|---|
| R274-1 F1 = R275-1-F1: the record omits a place delayAsymmetry enters | MINOR | Conformance, Docs | **RESOLVED** | `GPTP_PLANE.md:359,378-394,422` name all three terms at their clauses, add the relay carry and CSN rows, and state the net effect. "Both terms" is gone. The [A226] REVIEW READY supersedes the [A215] statement |
| R274-1 F2 = R275-1-F2: Table 14-6 misstated; trigger misses management | MINOR | Conformance, Docs | **RESOLVED** | `GPTP_PLANE.md:360` states Table 14-6 as written. The trigger condition is at `:402-410`, `REQUIREMENTS.md:141-146`, `FR_NFR.md:421-424` and `MILAN_COMPLIANCE_MATRIX.md:226`. The optional Units point is taken at `:418`. [A226] supersedes the [A215] statement |
| R274-1 S1 = R275-1-S3: no builder arm plants an asymmetry key | SUGGESTION | Tests | **RETAINED**, optional, as S2 | `test_builder.py` has no such arm; the probe passes |
| R275-1-S2: AS-13 is not gated | SUGGESTION | Tests, Docs | **RETAINED**, optional | `scripts/check_gptp_docs.py:73-75` still requires `AS-1` to `AS-12` only (`range(1, 13)`); no script changed in this PR |
| R275-1-S4: AS-13 edition label | SUGGESTION | Docs, Conformance | **RETAINED**, optional, as S5 | `ieee8021as.md:49` is unchanged by the round |

At the re-check (`receipts/prior-findings-read.txt`), the PR head was still
`70f2c50d`. The thread held 8 comments, no review objects and no inline
comments. The #511 thread ended at the [A226] REVIEW READY. No finding newer
than R275-1 exists.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `GPTP_PLANE.md:348-455`; `REQUIREMENTS.md:130-148,275-279`; `FR_NFR.md:228-236,416-424,444`; `MILAN_COMPLIANCE_MATRIX.md:226`; `ieee8021as.md:49`; the #394/#510 rows. Read against 802.1AS-2011 (+Cor1/Cor2), 802.1AS-2020, 802.1BA-2011 and Milan v1.2 (`receipts/standards-clause-receipts.txt`). #511 acceptance 1-5 and the three owner decisions | R275-2 | `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` |
| RTL | CLEAN | `receipts/diff-identity.txt`; `KL_gptp_shadow.sv:115-116,259-269,345,986`; `KL_gptp_txret.sv:147,283`; `milan_datapath.sv:99-100,1478-1479,6771-6772`; `receipts/asym-census.txt`; gPTP processor `c1b6174` tree; protocol-processor `424c688` `KL_aecp_engine.sv:707,1290-1296` | R275-2 | `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` |
| Robustness | CLEAN | `endstation_builder.py:3940-3948` under `receipts/probe-builder-asym-key.txt` (2 controls; 4 keys x 2 entry points); adoption contract `GPTP_PLANE.md:412-424` against the #511 scope and REQ-PTP-06/09 | R275-2 | `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` |
| Tests | CLEAN | `receipts/docs-gates-at-head.txt` (26/26 exit 0); `receipts/hosted-check-runs-at-head.tsv`; `receipts/consumers-of-round-pages.txt`; `receipts/proof-plan-unchanged.txt`; proof plan `GPTP_PLANE.md:426-455` | R275-2 | `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` |
| Docs | CLEAN | All 11 changed pages; `receipts/fragment-check.txt`; `receipts/commit-hygiene.txt`; trigger restatements; owner-decision links; PR body and #511 comments | R275-2 | `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` |

Every lens is covered at the merge candidate's source head itself. A later
commit that touches a lens's scope un-covers that lens.

## Executed evidence in this packet

Every file listed in `MANIFEST.sha256` is published with this report. The
review clone is written `$CLONE`. The scripts take their paths as arguments.

- **Builder probe:** `scripts/probe_builder_asym_key.py` produced
  `receipts/probe-builder-asym-key.txt`. It imports the builder in-process
  with bytecode writing off, and writes planted YAMLs only to scratch.
- **Asymmetry census:** `scripts/asym_census.sh` produced
  `receipts/asym-census.txt`.
- **Documentation gates:** `scripts/docs_gates.sh`, plus the eight further
  docs-workflow checks appended to the same receipt, produced
  `receipts/docs-gates-at-head.txt`. One gate subprocess wrote an ignored
  bytecode file, `scripts/__pycache__/png_artifact.cpython-314.pyc`. It was
  deleted; the second batch ends with 0 status entries.
- **Clause receipts:** `scripts/clause_receipts.sh` produced
  `receipts/standards-clause-receipts.txt`. It holds single matched lines
  only, with the PDF hashes. `scripts/classify_asym_lines.py` produced
  `receipts/delayasymmetry-line-census.txt`, over the same extraction.
- **Anchors:** `scripts/check_fragments.py` produced
  `receipts/fragment-check.txt`.
- **Clone integrity:** `scripts/verify_clone_integrity.py` produced
  `receipts/clone-integrity-final.txt`:
  - HEAD and tree are exact, and the index equals the HEAD tree (876
    entries);
  - 0 flagged index entries;
  - all 872 tracked non-gitlink paths rehash to their blobs with matching
    mode bits;
  - 0 untracked, ignored or submodule status entries;
  - the three required gitlinks equal their clean checkouts.
- **Other receipts:** `receipts/hosted-check-runs-at-head.tsv`,
  `receipts/diff-identity.txt`, `receipts/commit-hygiene.txt`,
  `receipts/consumers-of-round-pages.txt` and
  `receipts/proof-plan-unchanged.txt`.
- **Ordering:** `receipts/verdict-before-prior-findings.txt` was written
  before the prior reports were opened; `receipts/prior-findings-read.txt`
  records the read after it.
- **Dry merge:** `receipts/dry-merge-live-dev.txt` holds a disposable
  textual `git merge-tree` of the head onto live `dev` `50e78097`. It ran in
  a scratch clone, never the review clone, and is not a gated candidate.

## Real limits

- **Not run:** the full parent, processor, gPTP, Yosys and builder banks;
  `test_builder.py`; pp_top; Docker/act; the host act runner; hardware. No
  Verilator was used, so its identity was not needed. Physical calibration
  is NOT RUN, and field skips are not hardware proof.
- **Manager bank evidence:** the brief reports that the manager's full
  source static/builder and native banks passed at this head. The public
  tree at `9c71d05f`, the evidence branch tip, holds the executor's
  packets, and no separate manager bank log for this head was found there
  or in the PR/issue comments. That pass is taken from the brief; no
  conclusion here relies on it.
- **Hosted, exact head:** 8 contexts executed and succeeded:
  `bdd-conformance`, `changes`, `docs-check`, `docs-check-no-git`,
  `elaborate`, `full-ci-gate`, `rtl-fast` and `wire-accountability`.
  - 7 were skipped: `verilator-suites`, `yosys-portability`, their two
    shard contexts, `verilator-lint`, `yosys-elaboration` and Physical gPTP.
  - A skipped context is not executed evidence. The legacy combined status
    reads `pending`, with zero statuses.
  - Hosted and act acceptance is the manager's.
- **Standards texts:** read from text extractions of local copies. The
  Figure 10-9 formulas and the Table 14-6 row extract cleanly as text.
- **Live `dev` drift:** `50e78097` is 14 commits past the base, and touches
  four of this PR's pages: `TIME_SYNC.md`, `MILAN_V12_ROADMAP.md`,
  `FR_NFR.md` and the compliance matrix. Those hunks are CRF-counter text,
  in different places. The textual merge is clean (tree
  `348267ed0ccdf364f4e81bbd9ffe1939126f33c9`), but it is not a validated
  candidate.
- **Out-of-diff observation, not a finding:** `ieee8021as.md:47` (AS-11)
  labels clauses "12-16" "Non-Ethernet media layers". In both editions that
  range also spans the management clauses 14 and 15. It is harmless now,
  because no management is claimed. It is pre-existing and untouched here.

## Pending manager duties

1. **Revisit trigger:** obtain owner confirmation or replacement of the
   #511 revisit trigger. It is derived, and has three conditions: a second
   cabled port, a claim of 802.1AS management, and a REQ-PTP-06 amendment
   before any runtime correction. The executor asked again in the [A226]
   REVIEW READY. No owner answer exists at this head.
2. **Out-of-diff item:** file the item both prior rounds carried, if it is
   not already filed. `tests/features/aecp_response_contract.feature:98-106`
   asserts `NOT_IMPLEMENTED` for `GET_MILAN_INFO`, which the pinned engine
   serves. A read-only issue search found no issue for it.
3. **Bank receipts:** publish, or point to, the manager's own bank receipts
   for this head.
4. **Candidate merge:** build the candidate against live `dev` `50e78097`
   with the full local bar. Four pages overlap, so run the documentation
   gates on the merged tree, including `check_em_dash` against the
   candidate's merge base, the TOC gate and the feature-status gate. Also
   own hosted and act acceptance, and post-merge containment.
5. **Other issues:** keep #394 open for its bench proof and #510 open for
   processor F01.5 and the per-command checks, as the PR body states. #511
   closes by the merge.
6. **Suggestions:** optionally route S1-S5 and R275-1-S2. None blocks this
   merge.

R275-2 FINISHED
