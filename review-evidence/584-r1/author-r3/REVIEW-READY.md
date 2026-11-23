[A818] REVIEW READY
Commit: 599c79af9cfe242bc3d60dd1c80f3e8d57cca12e (branch `pf-584-1`, PR #975, base `dev-soft-core`; round 3 on `64d539f1`).

Changed: R894 F2-R2 / R893 F6 are addressed by continuous pin collection from bind loss and reset release through rebind, the recovery lead and the later window. The actual first and every subsequent nonzero word are checked for freshness. Both pre-loss/pre-reset replay controls fail their named B3/Z3 FRESHNESS checks. Projection, adapter and bus controls remain; zero-tail, stream-epoch-mask and REMOVE-as-ADD plants are now banked too.

R894 F5-R2 / R893 F7: receipt text contains no host paths, and the packet is byte-identical after the publication rewrite. The current index is generated from those final bytes and passes complete size/hash/file-coverage verification. The historical corrections verify against the immutable publication: round 1 80/80 and round 2 16/16. Receipt explanations use plain descriptions of the redaction. Build-plan names, changelog pending wording, the timing paragraph and stream-table tap description address the documentation residues.

Validation at this head:
- `make -C tb/verilator/milan_dp_render ship8`: 130 checks, zero failures.
- `make -C tb/verilator/milan_dp_render ship8-mutants`: 11/11 PASS, including both recovery replay controls caught by name.
- Full `milan_dp_render` suite: 263, 79 and 130 checks, zero failures; all five leg-side controls pass.
- Builder CI legs: 113 gates exactly once; the same two existing arms NOT RUN (make-profile arm and physical calibration report).
- Five configurations at both placements: 153/155 generated files byte-identical to round 1; only the two 8x8 build-plan documents add the unrouted name. All 1x1/1if TDM8 and Arty artifacts, every model ID and all binaries are unchanged.
- Docs commands: 99/103 pass; the four hosted-environment commands fail locally for the same missing runner/event environment as before. No local pass is claimed for them.
- No RTL, firmware, configuration or gitlink delta this round. Prior route, saved-state, firmware, budget and twin/ledger evidence is carried with its original provenance. No reroute or hardware operation.

The owner's backing disposition remains pending: no loopback-backed input cluster, loopback disabled at 8x8, and TDM32 slot 0 standing for the first TDM8 channel. Hosted/local-replica acceptance, the hosted runtime window, independent re-review and merge remain manager duties. The packet contains HANDOFF-r3.md, PR-BODY.md, REVIEW-READY.md and indexed receipts. Commits are local; no push or PR edit was performed.

REVIEW READY 599c79af9cfe242bc3d60dd1c80f3e8d57cca12e
