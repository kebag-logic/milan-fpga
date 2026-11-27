Held for one manager decision, the publication size of the census extract (see HANDOFF-r8.md); otherwise ready as below.

[A829] REVIEW READY

Commit: `011aaa6f080321e0a89f915720ebb3ee14807a16` (local; nothing pushed or posted). Round 8 is evidence, documentation and comments only: no firmware, RTL, row or image change.

Changed:
- `bdbd7b7c4`: section 15 cites #1022 for the owed registration cost, states the no-disposition control, the derivation's choice of row and the ROM headroom.
- `367c1dcdb`: `census_extract.py`, and the receipt regrader reads an extract's stated part limit (at most 15 MB).
- `9f15ecb30`: the service README cites the installed row's qualification at `907764eb` (`076e7cc7...`, 147 cases) and names the 145-case receipt as the superseded row's.
- `64a76076e`: wording residues RS-A, R927-1 RS1/RS3/RS4/RS5 and R928-2-RS1.
- `011aaa6f0`: four end-of-file blank lines (R928-2-SG1).

Findings answered:
- R927-2-F1: #1022 cited; control derivation published. NO QUALIFIED MODEL, least last notice 225.54 ms.
- R927-2-F2: README pointer.
- R928-2-F1 / R928-1-F1: compact census extract, 762 files, 1.43 GB, largest 14.0 MB. It reproduces all 147 grades and the cross-case PASS line for line as the full census. The missing-`srp-bound` control is refused identically. Paired step-1/step-2 executable, ELF and stimulus inventory, and the `flash: null` explanation (non-XIP).
- R928-2-F2: post-route utilization from both retained routed checkpoints. Round 7 33015 / 40369 / 13791 / 78 and round 6 the same: LUT delta 0.
- RS-B/RS-C/RS-D and R927-1 RS6 in the PR body.

Validation at the head: 10 documentation/idiom gates; `rows_tiers`, `load_grade`, `egress_ledger`, `record_classes`, `arty_grade` and `kept_grade` self-tests; `arty_grade` model; fixture-value identity; unchanged generated split configuration. All pass. Firmware, native and service gates stand at `74f942be5`.

Open risks/questions:
- The extract is 1.43 GB against the ~300 MB target. It is the smallest extract of original lines that regrades: the grades count every pass's polls, rounds and slices.
- `census_extract.py` and the regrader's limit have no planted-control self-test; the regrade and control runs on the extract are their evidence.

Evidence: [PR-BODY.md](PR-BODY.md), [receipts/INDEX.md](receipts/INDEX.md).
