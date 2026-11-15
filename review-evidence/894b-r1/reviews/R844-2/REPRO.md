# Reproduction and receipt provenance

Review R844-2 at head 98c0b62be911f5cff7a03ebfee7f837c23847d14.
Commands were run in the detached review checkout. No source mutation was needed.
All disposable inputs are beneath this packet's scratch directory.

The public archive is commit 843c40b1e9249d89862a9174da7e2b4c32c300d1 in kebag-logic/milan-fpga.
Extract only these paths with `git archive` into a disposable archive directory:

- review-evidence/894b-r1/author-r3
- review-evidence/894b-r1/author-r4
- review-evidence/894b-r1/MANIFEST.json

Set CHECKOUT to the exact-head checkout, PACKET to this packet, and ARCHIVE to the extracted review-evidence/894b-r1 directory. The commands below require only those paths and the ordinary source prerequisites. They perform no installation or remote write. Run from CHECKOUT. Use `TMPDIR="$PACKET/scratch"` for commands that create temporary files. `-B` avoids unnecessary bytecode files.

| Receipt | Command or derivation | Observed result |
|---|---|---|
| receipts/evidence-audit.log | `python3 -B "$PACKET/scripts/evidence_audit.py" "$CHECKOUT" "$ARCHIVE"` | exit 0; 94 manifest hashes, 45 original/redacted index hashes; image pairs match; 139/226 workflow rows; 59 lane rows; six log census |
| receipts/ledger-selftest.log and .rc | `python3 -B tb/verilator/ctrl_service_budget/egress_ledger.py --selftest` | exit 0; 30 controls in each mode; eight mutants caught |
| receipts/gate-controls.log and .rc | `python3 -B "$ARCHIVE/author-r4/scripts/gate_controls.py" "$CHECKOUT" "$ARCHIVE/author-r4/scripts/gate_r4.py" "$PACKET/scratch/gate-controls"` | exit 0; all 20 controls |
| receipts/identity.log and .rc | `python3 -B "$ARCHIVE/author-r4/scripts/ast_same.py" "$CHECKOUT" 716a8ae7 6da0dc73` | exit 0; wording commit tokens/ASTs, five printed descriptions inspected |
| receipts/comments.log and .rc | `python3 -B "$ARCHIVE/author-r4/scripts/comment_scan.py" "$CHECKOUT" 7398ec0a HEAD` | exit 0; zero matching added source lines |
| receipts/prior-comment-audit.log | `python3 -B "$PACKET/scripts/source_comment_audit.py" "$CHECKOUT"` | exit 0; zero bytes/lines |
| receipts/regrade.log and .rc | `python3 -B tb/verilator/ctrl_service_budget/egress_ledger.py --point 8x8-1if "$ARCHIVE"/author-r4/receipts/regrade/legs-r3/*.log` | exit 0 |
| receipts/gate-regrade.log and .rc | Run `gate_r4.py CHECKOUT` with one `-:LOG` argument for each of the six C-A0, C-A1, C-A2, C-A3, C-AE, C-AL logs | exit 0; log-only limits printed explicitly |
| receipts/guard-probe.log | `python3 -B "$PACKET/scripts/guard_probe.py" "$CHECKOUT" "$PACKET/scratch/guard"` | exit 0; five positive/negative compile checks |
| receipts/prior-probes.log | `python3 -B "$PACKET/scripts/prior_probes.py" "$CHECKOUT" "$ARCHIVE/author-r4/scripts/gate_r4.py" "$PACKET/scratch/prior-probes"` | exit 0; original control exits 0, both fault fixtures exit 1 by name |
| receipts/integrity.log | `python3 -B "$PACKET/scripts/integrity.py" "$CHECKOUT"` | exit 0; raw blob, mode, index and five submodule pin/content proofs; clean status |
| delta.diff | `git diff 716a8ae7..98c0b62b` | reviewed four-commit delta |

The original comment audit is copied unchanged from the archive's reviews/R844-1/source_comment_audit.py, read only after the independent verdict and ledger were written. prior_probes.py preserves the fixture contents from reviews/R844-1/probe_evidence_gate.py; only gate arguments, expected statuses and explicit named-failure assertions adapt it to the corrected gate.

The archived author scripts were inspected before execution. gate_controls.py clears only its supplied disposable scratch directory. No broad bank launcher or host orchestration script was executed.

The local logs are the captured outputs of the listed commands, without path rewriting. Archive hash auditing uses the published (already redacted) files and the public manifest's original/published digest fields. The archive's unredacted originals and image binaries are not present, so their underlying bytes are not independently rehashed here; the published image digest pairs are compared. No cryptographic signature verification is claimed: the pinned archive commit has no signature header.

All files listed in MANIFEST.sha256 and REPORT.md are publishable. Nothing under scratch is listed or intended for publication.
