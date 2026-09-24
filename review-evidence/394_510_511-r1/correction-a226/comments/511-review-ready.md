[A226] REVIEW READY

This is correction round 1 of PR #537. It fixes the two MINORs that R274-1 F1/F2 and R275-1 F1/F2 raise (https://github.com/kebag-logic/milan-fpga/pull/537#issuecomment-5805065861, https://github.com/kebag-logic/milan-fpga/pull/537#issuecomment-5805241709).

Commit: `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` on `394-510-511-decisions`, tree `ef96bf2fe0d66dd9c0b1ba45c6b4300d89ba658c`. Its parent is `64bcf768d28b4b9763fbe5917a734bcefa2a66e0`, the head both rounds reviewed. It is one commit with a one-line subject and no trailers. It is committed locally and not pushed; the push belongs to the manager.

Changed: Markdown only, 4 files, +40/-9.

**F1: the #511 record now names every place delayAsymmetry enters the arithmetic** (`docs/design/GPTP_PLANE.md`, new table "Where the term enters"). The 2011 text with Cor1/Cor2 applies it here and nowhere else:

| Clause | Arithmetic |
|---|---|
| 11.2.13.2.1 f) `setMDSyncReceive()` (11.1.3 d) describes it) | `upstreamTxTime = <syncEventIngressTimestamp> - neighborPropDelay/neighborRateRatio - delayAsymmetry/rateRatio` |
| 10.2.12, Figure 10-9 | `syncReceiptTime = ... + delayAsymmetry` |
| 10.2.12, Figure 10-9 | `syncReceiptLocalTime = upstreamTxTime + neighborPropDelay/neighborRateRatio + delayAsymmetry/rateRatio` |
| 11.2.14.2.3 a) `setFollowUp()` (11.1.3 e) and Table 11-5) | `upstreamTxTime` carries the first term into a relayed Follow_Up `correctionField`. Only a port that relays another port's Sync does this (10.2.11), so a one-port end station never does |
| Annex E.5.2.2 | A CSN egress port reads the 10.2.12 inputs from the CSN TLV. Not applicable, because the product has no CSN port (AS-11) |
| 802.1AS-2020, not the edition of record | The same terms at 10.2.13, 11.2.14.2.1 and 11.2.15.2.3. With CMLDS, 11.2.17.2 a) folds the term into the mean link delay |

- **Net effect, as the record now states it:** `syncReceiptTime` gains `delayAsymmetry`, and its paired local time does not move. The `syncReceiptLocalTime` term adds back the f) subtraction. The only residue comes from the Figure 10-4 `neighborRateRatio` update, which NOTE 2 of 11.2.13.2.1 calls usually negligible.
- **Stated for adopters:** an adoption that omits that term roughly doubles the shift.
- **Wording fixes:** "both terms" is gone. The "Where would it enter?" row cites Figure 10-9's two assignments, and the adoption "Application point" row names all three terms.

**F2: the management row states Table 14-6 correctly, and the revisit trigger includes the management condition.**

- **The corrected row** cites Table 14-6 (14.6.25), whose row Cor1's replacement table keeps:
  - Operations: read-write.
  - Conformance: `Tdot3FD`, "Required for time-aware IEEE 802.3 full-duplex port". So such a port must carry the object wherever 802.1AS management is implemented.
  - "(recommended)" qualifies the `scaledNs` data type, as 14.3.2 spells out for `offsetFromMaster`.
  - 14.6.9 defines the object without grading it.
  - Management is optional: PICS item `MGT` (A.5) is `O`. The product claims none.
- **The revisit trigger** now also fires before the product claims 802.1AS management, and is checked before the P4 802.1AS conformance run. A write to that managed object is a runtime correction, so it first needs the REQ-PTP-06 amendment.
- **The same condition is added in three more places:**
  - the REQUIREMENTS.md REQ-PTP-06 scope note;
  - the FR_NFR Section 5 out-of-scope entry, which restated the trigger;
  - the compliance matrix Section 4 row, which cites 14.6.9.
- **R274-1's optional point is taken.** The Units row cites Table 14-6 for `scaledNs`, because 10.2.4.8 names no data type.

**What this round does not change:**

- The adoption proof plan, from "What an adoption must prove" through the ownership table, is byte-identical to `64bcf768` (sha256 `5efb63097a2e0cec4dab93cd1eea0f2ae0521f3ecb7c11c83c52863dc60d0ce3` at both heads).
- There is no RTL, firmware, builder, configuration, test or gitlink change.
- `CHANGELOG.md`, `docs/integration/BAREMETAL_FIRMWARE.md` and the builder page are untouched. The brief names the builder page `docs/design/ENDSTATION_BUILDER.md`, but the tree holds it at `docs/ENDSTATION_BUILDER.md`; neither path is in the diff.

**Corrections to the [A215] REVIEW READY above.** Two of its statements are superseded:

- "it enters only 10.2.12 `syncReceiptTime` and 11.2.13.2.1 `upstreamTxTime`" is replaced by the three terms above.
- "14.6.9 is a recommended RW object" is replaced by the Table 14-6 grade above.

Validation at `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6`, with the submodules at their gitlinks. Every command exits 0:

```text
python3 -B scripts/docs_check.py                        0 finding(s), 164 md + 848 scrubbed files
python3 -B scripts/check_em_dash.py --base 759da623     0 finding(s) over 230 added lines in 11 pages
python3 -B scripts/check_em_dash.py --base 64bcf768     0 finding(s) over 40 added lines in 4 pages
python3 -B scripts/check_feature_status.py --self-test  46/46; 0 finding(s)
python3 -B scripts/check_baremetal_only.py --check      OK, 0 findings (--selftest 377 arms PASS)
python3 -B docs/traceability/gen_module_matrix.py --check   up to date (69 modules)
python3 -B scripts/check_gptp_docs.py --with-submodule  OK (8 pages, donor checkout verified); --selftest 30 controls
python3 -B scripts/check_doc_style.py                   OK (22 documents); --selftest OK
python3 -B scripts/gen_toc.py --check / --verify-anchors   OK / 154 fragment links
python3 -B scripts/check_doc_paths.py                   OK (832 paths)
python3 -B scripts/check_submodule_docs.py              OK (4 exact gitlinks); --selftest OK
python3 -B scripts/check_solution_docs.py               OK; --selftest 43 controls
python3 -B scripts/check_wire_accountability.py         42 checks, 0 findings
python3 -B docs/DOC_MAP.gen.py --check, docs/diagrams/timesync_chain.gen.py --check,
  docs/diagrams/submodule_boundaries.gen.py --check, scripts/check_diagram_pngs.py   OK
git diff --check 759da623 HEAD; git diff --check 64bcf768 HEAD   clean
```

- **Not re-run at this head:** `sw/builder/test_builder.py` and the protocol-processor `pp_top` run. This round changes only Markdown that no builder or test code reads; `git grep` finds the four pages only in two style/gPTP gates' page lists, a docstring and a comment. The processor pin is unchanged. The [A215] results at `64bcf76` still describe those.
- **Clause readings** come from `pdftotext -layout` of the local 802.1AS-2011, Cor1-2013, Cor2-2015 and 2020 PDFs. Cor2 has no delayAsymmetry text. Cor1 changes only 10.2.12.2.1's prose in 10.2.12, not Figure 10-9, and restates 11.2.13.2.1 f) unchanged.

Acceptance criteria (#511):

| # | Status | Evidence |
|---|---|---|
| 1 | Met | The clause-backed decision now carries the full arithmetic (F1) and the correct management grade (F2) |
| 2 | Met | The design record's parameter and management contract states Table 14-6, and the single compensation owner is unchanged |
| 3 | Met | The adoption plan's application point names all three terms, and the proof plan is unchanged. No result is claimed |
| 4 | Met (no implementation approved) | Unchanged |
| 5 | Met | The gates above |

Open risks/questions:

- **The #511 revisit trigger is still derived, not owner-stated.** It is the decision's two grounds (a second cabled port, and a REQ-PTP-06 amendment before any runtime correction) plus the management condition F2 requires. Please confirm or replace it.
- **The 802.1AS-2020 row is informative.** The edition of record stays 2011 (decision #139).
- **SUGGESTIONs not taken this round, all optional:**
  - R275-1 S2: gate AS-13 in `check_gptp_docs.py`.
  - R275-1 S3 = R274-1 S1: a builder test that plants an asymmetry key.
  - R275-1 S4: label AS-13's clause edition.
- **Scope of the change for re-review:** only `REQUIREMENTS.md`, `GPTP_PLANE.md`, `FR_NFR.md` and the compliance matrix changed. No file in RTL or Robustness scope changed, and no gate or proof-plan text changed.
