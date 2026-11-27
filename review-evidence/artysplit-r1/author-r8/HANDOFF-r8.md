Status: STOP for one decision (07:30). Every round-8 item is done and committed at `011aaa6f0`. The compact census extract regrades all 147 cases byte-identically, but it is 1.43 GB against the ~300 MB target. That is the floor for an extract of original lines, so I stopped with the sizes, as instructed.
ETA: none needed for the work. Once the size is decided: publish as is (no work), or a lossless compact encoding (about 1 day: format, decoder in the regrader, proofs).

[A829], round 8, PR #1004 (Relates to #878). Branch `pf-arty-split-1`, local head `011aaa6f080321e0a89f915720ebb3ee14807a16` on the pushed round 7 `4adfa9dc8`. Nothing pushed or posted; no hardware; no job running. Scratch `$VALIDATION_STORAGE/artysplit-a829/r8`.

## The decision

| Extract | Files | Largest file | Total | Regrades |
|---|---:|---:|---:|---|
| Round 7's full extracts | 22,600 | 180 KB parts | 3.94 GB | yes |
| **Built: original lines the graders read** | **762** | **14.0 MB** | **1.43 GB** | **yes, identical** |
| Original lines inside work passes only (measured on 4 cases, about 5 % of full) | — | — | about 0.2 GB | **no**: polls passes 44025 -> 1122, rounds, slices change |
| Read lines, delta-coded text (estimated from one case, not built) | — | — | about 0.4 GB | would need a decoder in the regrader |

The graders count every pass's poll sections, rounds and slices, so every instance of the read labels is needed (`receipts/extract-floor/filtertest.log`).
Choose one:
1. Publish the 1.43 GB extract. Every part is under 15 MB, well below GitHub's 100 MB per-file limit.
2. Have me build a lossless delta-coded extract, still over 300 MB.
3. Accept hash-listed non-archival, with access on request.

## Round 8 commits

- `bdbd7b7c4`: section 15 cites #1022 where the cost is owed. It states the no-disposition control (no qualifying row; least last notice 225.54 ms), the derivation's choice between the two qualifying rows (R927-2 SG-3), and the ROM headroom of 1404 bytes (SG-6).
- `367c1dcdb`: new `census_extract.py` builds the extract from the graders' own label constants. `receipt_regrade.py` accepts an extract's stated part limit, capped at 15 MB; the default stays 190 KB.
- `9f15ecb30`: README F2. It cites `published-qualification.json` at `907764eb` (`076e7cc7...`, PASS, 147, model equal to `arty_grade.py`'s) and names the 145-case receipt as the superseded row's. It also cites #878's held-egress ruling for R927-1 RS3.
- `64a76076e`: residues RS-A, R927-1 RS1 (R928's text), RS3, RS4, RS5 and R928-2-RS1, each with the exact text the reports give.
- `011aaa6f0`: R928-2-SG1, four EOF blank lines; `git diff --check c34e7d8b0 HEAD` is clean.

## Evidence (round8/receipts, INDEX.md)

- `census-extract/`: 147 cases. Every manifest, scenario, stimulus, grade and journal is byte for byte round 7's. `FILES.json` maps each file to its round-7 sources and their `FILES.tsv` SHA256.
  The regrader reproduces 147/147 grades and the cross-case PASS, identical line for line to the full census (its 13 timing lines aside). The control without `srp-bound` is refused identically, apart from traceback line numbers.
- `control-derivation/`: the no-disposition control over 147 cases. NO QUALIFIED MODEL, 52/52 candidates fail an owner bound, least last notice 225.54 ms, load 0.6206.
- `identity/`: paired step-1/step-2 executable and ELF hashes from each step's own files, and every stimulus, all identical. It explains `flash: null`: only XIP builds write a flash image.
- `route-utilization/`: post-route `report_utilization` on retained checkpoints. Round 7 and round 6 are both 33015 LUT / 40369 registers / 13791 slices / 78 BRAM, a delta of 0 within the ~50 band. Checkpoint and bitstream hashes are bound.
- `gates/`: ten docs/idiom gates and six standalone self-tests at the head, plus the model, fixture-value identity and an unchanged generated configuration. All pass.

## Disk

/data fell to 17 GB free (not from this round's 1 MB of scratch). I moved the superseded round-4 final census and round-6 partial census traces (9.7 GB) to `artysplit-a829/scratch-archive/` on the home filesystem, logged first in `disk-cleanup.log`. Nothing was deleted, and /data now has 26 GB free.

## Not done, by design or choice

- The optional suggestions R927-2 SG-1 (regrader tie-break), SG-2 (regrader self-test), SG-4, SG-5 and SG-7. Also R928-2's retained R927-1 SG1, SG3 and SG4.
- `9f15ecb30` also carries the README's held-egress citation (RS3), so its subject names the pointer only.
- The PR body says "Head `011aaa6f0...` (the PR head)" for after the push.

STOP: census extract regrades all 147 cases byte-identically but is 1.43 GB (762 files, largest 14.0 MB) against the ~300 MB target, the floor for original lines; all other round-8 items done at 011aaa6f0; need a publication decision
