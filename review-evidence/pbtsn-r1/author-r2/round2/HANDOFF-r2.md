Status: REVIEW READY, 2026-11-28 11:40. tsn-c-stack `pocket-beagle` head 40c3111. Round 2 closes every finding of both PR #43 reviews. Main bf02d81 is merged.
ETA: none outstanding for this round. Board work continues with the BSP lane; see the end.

## What changed since ef5e5ce

| Commit | Content |
| --- | --- |
| 70a437f | Merge of main bf02d81 (PR #44). My exemption commit and #44's edit the same lines. Resolved to #44's text: one entry for the #41 merge, documented in IMPORT.md and VERIFICATION.md, with a self-test that checks each exempt merge. My duplicate changelog line is dropped. |
| 9d06d80 | Clause citations in `src/pbaem.c` corrected. LOCALE `en-US`. Golden CRC 0xd891cd2f. |
| 9e2a466 | Four new test cases and 12 new plants. |
| ee3c173 | AEM-01 origin is issue 42. Format wording. TRACEABILITY regenerated. |
| b03d499 | RV32 gate diagnostics name the AEM model. |
| 40c3111 | PocketBeagle page: unpublished evidence stated, golden provenance, porting contract, DEV-01. |

## Gates at 40c3111, run in the CI replica

- `validate.py`: 27 of 27 gates rc 0. The mutation campaign catches 550 of 550 plants, 0 escaped and 0 errors; all 27 `pbaem-` plants are caught.
- `baremetal.py`: Debug and Release, rc 0.
- Graphs: 5 rendered, on the host.
- Privacy gate: 107 commits, pass.
- Receipts are in `../receipts/round2/`.

## Board-facing

- The BSP lane already applied 0001..0007 and runs the 4x4 + CRF model on the board.
- The only entity change this round is the locale. It is a one-line config patch, `pb-interface/a866/patches-locale/0001`, explained in `A866-REPLY-5.md`. The model ID is unchanged.
- Checked against the BSP head 126e7af with the patch applied: the AECP suite passes, and the config generates the `pbaem` golden exactly.

## Open

- Owner/manager: the published round-1 packet files carried bench labels and "private" headers (external review, manager duty). Round 2 files use neutral names only.
- Board validation (switch path with SRP, soak, flashable image) is the BSP lane's, in progress.

Nothing pushed or posted. No board or bench device touched by this lane.
