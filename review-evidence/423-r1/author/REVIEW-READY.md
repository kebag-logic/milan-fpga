[A171] REVIEW READY
Commit: `fed4f63f33e6185e5c7e4735a27234db99651d24`
Tree: `330afc6078441daf4d6a59d5dc760303a501477f`
Branch: `423-retained-redundant-replay`; clean, stopped at this head.

Changed: the settled final G1 + H + T arm, bounded default-owner self-tests, and checker/CONTRIBUTING wording for historical replay, current retention and UNKNOWN. Existing containment-arm order, linear historical policy and exit codes remain unchanged. Shared Git transport preserves CRLF and undecodable path/patch bytes. No budget widened.

Validation:
- `python3 scripts/check_merge_containment.py --selftest`: exit 0, 326/326 assertions, 17.479 seconds. Original 145 assertions unchanged; new 181 comprise 44 public-matrix, 25 mutation and 112 boundary assertions.
- Unchanged public fixture builders: 31/31 verdict/exit pairs and all 31 original head/tip OID pairs reproduced. Ten production guard mutations killed; full matrix evaluated 341 CLI runs and asserted the exact changed-case sets.
- Docs, gen_toc checks/self-test/anchors, Python idiom/self-test, hygiene/self-test, em-dash, and the selected 20-command documentation/source/ratchet batch: exit 0. Receipts bind the batch's source bytes to the committed tree above. CPU capped at eight.
- Actual gPTP processor PR62 at both recorded targets remains UNKNOWN/1, naming `tb/tsngen/mutants.py` and `tb/verilator/gaskets/mutants.py`. Both raw patch hashes reproduce. Both published probe cases remain UNKNOWN/1; PR61's existing linear result remains contained/0.

Acceptance: AC1-3 have local implementation evidence. AC4 awaits A10's full local/act/hosted/current-candidate/post-merge bar and cleared R243/R244 reviews. No self-approval, final lens ledger, processor adoption or audit waiver is claimed.

Limits: exact one-merge shape only. Overlapping rewrites, differing special-file entries and unsupported measurements remain unresolved. Repeated-block controls and the separate 11,256-case raw probe provide bounded evidence, not a general alignment or semantic-preservation proof. Invalid Git configuration remains UNKNOWN; exhaustive Git/platform and large-file/resource behavior is unproved.

A10's assigned author packet contains HANDOFF.md, REVIEW-READY.md, PR-BODY.md and reproducible scripts/raw receipts. No push, PR metadata change, Docker/act, merge, delegation, hardware or full native/processor/builder sweep was performed.
