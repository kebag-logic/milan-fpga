Status: REVIEW READY (16:45). Every finding of R967-1 and R968-1 is closed in the tree at `47f2a3d7`, each named mutant is caught, #1027 is cited as the contract, and the receipts are staged as extracted text. Every gate passes at `47f2a3d7`:
- harness self-tests, the service self-test (323/323) and the mutants (8/8);
- docs and idiom;
- identity, the 4x4 ELF (`1b8066e4…`) and the 4x4 boot with native controls 6/6;
- the builder suite, ALL GATES PASS EXCEPT gate 11, NOT RUN with its reason.
ETA: done. Next: publish the packet and link it from PR #1026 and #1027, re-review, then the bench.

[A863], round 5. Worktree `$LANES/arty-4x4`, branch `arty-4x4-1127`, head `47f2a3d7ffdf7ef701c69267a91ac92892a1c99e`. Nothing pushed or posted; no bench, no flash. The PR #1026 branch on GitHub is still at `12ab4b18`; this round's seven commits are local.

## Round-5 commits

- `f7c1b674e` #1027 named as this point's task contract (config header, harness comments, builder and build pages, section 15 renamed "Arty split points" with the 4x4's decisions, stated costs, qualifying rows and tie-break).
- `988b13a8d` each Arty point's 100 Mb/s stream load held, CRF frame included; `--packet`/`--structural --point`; FR_NFR's structural and queued figures per point.
- `8c5047efa` the 4x4's record classes at its own clock, configuration and ACMP record cost.
- `8bca16462` the ledger's planted cycle held to each point's configured clock.
- `5ed652182` and `47f2a3d7f` `egress_fixed.py` runs isolated, refuses a malformed SYS_HZ and has `--selftest`.
- `8018399b2` the harness README.

## What was done for each item

1. #878 to #1027: each reference that named this point as #878's now names #1027. #878 is kept where it is the 1x1's or a historical fact (the 1,465 ns reading, the bench compensation rule). The PR body says `Closes #1027`.
2. Findings: REVIEW-READY.md maps each finding to its control and evidence. `receipts/gates5/mutants/mutants.json` plants each named mutant in the tree. Each is caught by a named assertion, and the restored tree passes.
3. Receipts: rounds 1, 3 and 4 have 123 `.gz` receipts and one `.tar.gz`. All are extracted to text under `receipts/earlier/`. The census-4 extract (334 files, 20.7 MB) regrades both the egress row and the ledger. Every file is already in its published form: the archiver's path and privacy rules are applied, and a second pass changes nothing. The sha256 in INDEX.md is therefore the published file's.
4. Gates and identity: these ran at `47f2a3d7` (REVIEW-READY.md, `receipts/gates5/`). Builder outputs, the existing product ELFs and the 4x4 ELF are byte-identical. The config header edit changes no image byte and no generated include.

## For the manager

- Publish the packet and link it from PR #1026 and #1027. R968 F5 asks for the evidence commit to be linked from the PR.
- R967 S5 (#1022's body naming `arty-4x4`'s owed records) and R968 S3 (a published-qualification link in the README) need a public record; they were not done here.
- #1027's bench item (4+4 streams and CRF at once, the correction pair at 100 MHz) is still owed.

Receipts: `receipts/` (824 files, 84 MB; INDEX.md lists each file's published sha256 and maps every earlier `.gz` to its extracted file). `tools/receipts5.py`, the staging script, is withheld because it states the archiver's own agent-token rule.

Scratch `$VALIDATION_STORAGE/arty4x4-a863` is about 8.5 GB. Gate outputs at the superseded head `8018399b2` are in `gates5-8018399b2/`.

REVIEW READY 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e
