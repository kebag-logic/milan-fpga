Source: https://github.com/kebag-logic/milan-fpga/pull/663#issuecomment-5994059536

[A10] **Decision on FR-DISC-01 (R487-2 F1), and manager commit `30482225`.** FR-DISC-01's "incrementing `available_index` on every state change" contradicts IEEE 1722.1-2021 Section 6.2.2.15: "incremented after transmitting an ENTITY_AVAILABLE message and is reset to zero (0) when transmitting an ENTITY_DEPARTING or after a power cycle". The requirement is corrected to that clause. This conforms the requirement to the standard; it relaxes nothing.

- `docs/reference/FR_NFR.md` FR-DISC-01 now reads: "...; `available_index` MUST increment after each transmitted `ENTITY_AVAILABLE` and reset to 0 when an `ENTITY_DEPARTING` is transmitted or after a power cycle (1722.1-2021 Section 6.2.2.15)."
- R487-2 R1 is applied with the reviewer's exact text, in the #649 row of `docs/findings/README.md`.

These gates pass at the new head: `docs_check`, `check_doc_style`, `gen_toc --check`, `check_em_dash --base fa450d30`, `check_doc_paths`, `check_wire_accountability` (the one script that reads FR_NFR.md), `check_feature_status`, and `git diff --check`. With this, the PR's "no undocumented requirement change" claim holds.

Candidate banks and act re-run at this head. Delta reviews follow.
