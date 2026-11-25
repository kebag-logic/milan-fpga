# Receipts: round 4, the CPU budget harness on the merge head's images and the PR body at 507bce7f

Merge head `507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698` (parents `30796098` and `2509db68`), pushed, unchanged this round.
Every file is text and under 200 KB, and there is no .gz. A log over 190,000 B is kept as its first and last 90,000 B,
with its full size and sha256 noted at the cut (`tools/rcopy.py`). Scratch (full logs and build trees) is under
`/data-2/milan/tmp/lwsrppin-a834/r4/`. Raw logs carry local paths, as in rounds 1 to 3.

| File | Bytes | sha256 (16) | What it is |
|---|---:|---|---|
| `budget/flip_1x1.log` | 1,784 | `1402ddc68c0914d2` | load_grade.py --check and flip_grade.py --check at the merge head |
| `budget/flip_8x8_1if.log` | 1,366 | `724e9b1077f7b8eb` | load_grade.py --check and flip_grade.py --check at the merge head |
| `budget/load_check.log` | 1,793 | `c5e1060bedf55ee4` | load_grade.py --check and flip_grade.py --check at the merge head |
| `budget/rc.txt` | 36 | `d7cc11db7fe2ea75` | load_grade.py --check and flip_grade.py --check at the merge head |
| `budget/train-compare.txt` | 123 | `7f078af2c4ab8d07` | load_grade/flip_grade at 2509db68 and the byte comparison |
| `budget/train-flip_1x1.log` | 1,784 | `1402ddc68c0914d2` | load_grade/flip_grade at 2509db68 and the byte comparison |
| `budget/train-flip_8x8_1if.log` | 1,366 | `724e9b1077f7b8eb` | load_grade/flip_grade at 2509db68 and the byte comparison |
| `budget/train-load_check.log` | 1,793 | `c5e1060bedf55ee4` | load_grade/flip_grade at 2509db68 and the byte comparison |
| `harness/build-1x1-every.json` | 7,823 | `a421bf8476e2a512` | the harness build.json (the image's recorded inputs and sha256) |
| `harness/build-1x1-later.json` | 7,818 | `c5c0601a1c476b22` | the harness build.json (the image's recorded inputs and sha256) |
| `harness/build-1x1.json` | 7,755 | `3374c6b9ba38c96b` | the harness build.json (the image's recorded inputs and sha256) |
| `harness/build-8x8-1if-every.json` | 7,648 | `49ab826ec776d53d` | the harness build.json (the image's recorded inputs and sha256) |
| `harness/build-8x8-1if-later.json` | 7,642 | `018413a0a3455871` | the harness build.json (the image's recorded inputs and sha256) |
| `harness/build-8x8-1if.json` | 7,580 | `aadb7d30500295aa` | the harness build.json (the image's recorded inputs and sha256) |
| `harness/egress-compare.txt` | 861 | `57d3952cb30216ba` | the seven egress rows: pin 402834ac (round 1), train 2509db68, merge 507bce7f, ledger |
| `harness/egress-ledger-8x8-1if.log` | 1,553 | `3a649153d7531a45` | egress_ledger.py --point 8x8-1if on arm A at the merge head |
| `harness/egress-ledger-selftest.log` | 11,842 | `ac5fc64f3d09b751` | egress_ledger.py --selftest at the merge head |
| `harness/grade-1x1-every.txt` | 1,559 | `6f0070930da729bb` | the run's grade: image identity, round 1's harness_grade.py, share_census.py, run.py's verdict lines |
| `harness/grade-1x1-later.txt` | 1,549 | `8c5104c6b5e1c561` | the run's grade: image identity, round 1's harness_grade.py, share_census.py, run.py's verdict lines |
| `harness/grade-1x1.txt` | 4,223 | `779d62006cbf30c2` | the run's grade: image identity, round 1's harness_grade.py, share_census.py, run.py's verdict lines |
| `harness/grade-8x8-1if-every.txt` | 1,568 | `88d5f403380713a6` | the run's grade: image identity, round 1's harness_grade.py, share_census.py, run.py's verdict lines |
| `harness/grade-8x8-1if-later.txt` | 1,559 | `86ffd48091aba3c6` | the run's grade: image identity, round 1's harness_grade.py, share_census.py, run.py's verdict lines |
| `harness/grade-8x8-1if.txt` | 5,041 | `47af370c82d0bd3c` | the run's grade: image identity, round 1's harness_grade.py, share_census.py, run.py's verdict lines |
| `harness/identity.txt` | 3,422 | `4ab10e7c574ccfd9` | harness ELF sha256 against the merge head's ledger images |
| `harness/kept-1x1.txt` | 2,487 | `736574c8ccd701c6` | kept_grade.py <build-dir> on arm A (the train's #969/#977 disposition) |
| `harness/kept-8x8-1if.txt` | 2,697 | `644830bcd1bab0c6` | kept_grade.py <build-dir> on arm A (the train's #969/#977 disposition) |
| `harness/la-window-1x1.txt` | 1,011 | `fce3e183a112a2e3` | la_window.py: each LeaveAll timer run-out, its MRPDU and the passes in the next second |
| `harness/la-window-8x8-1if.txt` | 2,384 | `09a3b9e0bd0c7393` | la_window.py: each LeaveAll timer run-out, its MRPDU and the passes in the next second |
| `harness/run-1x1-every.log` | 49,794 | `922db0ec5c89b2e4` | run.py's log (cut head and tail where over 190,000 B) |
| `harness/run-1x1-later.log` | 25,688 | `0726592c0feb66b2` | run.py's log (cut head and tail where over 190,000 B) |
| `harness/run-1x1.log` | 57,091 | `d11c8438e10f7457` | run.py's log (cut head and tail where over 190,000 B) |
| `harness/run-8x8-1if-every.log` | 102,879 | `5ee572bc2e34c113` | run.py's log (cut head and tail where over 190,000 B) |
| `harness/run-8x8-1if-later.log` | 25,987 | `cdf8fd5538901a91` | run.py's log (cut head and tail where over 190,000 B) |
| `harness/run-8x8-1if.log` | 58,860 | `f074e29875c551d0` | run.py's log (cut head and tail where over 190,000 B) |
| `harness/selftest.log` | 180,193 | `43ff2215ede5f0f4` | run.py --self-test (cut head and tail where over 190,000 B) |
| `harness/table-1x1-every.md` | 55,220 | `893687719a933ce1` | run.py's results/table.md (cut head and tail where over 190,000 B) |
| `harness/table-1x1-later.md` | 12,658 | `e4e60f56cef36095` | run.py's results/table.md (cut head and tail where over 190,000 B) |
| `harness/table-1x1.md` | 180,188 | `60a772a40ff0366b` | run.py's results/table.md (cut head and tail where over 190,000 B) |
| `harness/table-8x8-1if-every.md` | 142,840 | `2367082ebe1665eb` | run.py's results/table.md (cut head and tail where over 190,000 B) |
| `harness/table-8x8-1if-later.md` | 12,724 | `69baaa734bb7575b` | run.py's results/table.md (cut head and tail where over 190,000 B) |
| `harness/table-8x8-1if.md` | 180,188 | `aa48d0d128a64bd8` | run.py's results/table.md (cut head and tail where over 190,000 B) |
| `harness/times.txt` | 811 | `bb01f57f4ff98603` | each run's rc, start, end and head |
| `harness/train-2509db68/build-8x8-1if.json` | 7,651 | `5c3d51f9cd8e4932` | the train's own image at 2509db68: arm A's backlog-owed and srp-bound at 8x8/1if |
| `harness/train-2509db68/egress-ledger-base-8x8-1if.log` | 1,337 | `59289ede74676180` | the train's own image at 2509db68: arm A's backlog-owed and srp-bound at 8x8/1if |
| `harness/train-2509db68/identity-base.txt` | 580 | `4aba138da57f66cc` | the train's own image at 2509db68: arm A's backlog-owed and srp-bound at 8x8/1if |
| `harness/train-2509db68/run-8x8-1if.log` | 24,188 | `2f67b1d142988dbd` | the train's own image at 2509db68: arm A's backlog-owed and srp-bound at 8x8/1if |
| `harness/train-2509db68/table-8x8-1if.md` | 6,419 | `94b6018cafa87841` | the train's own image at 2509db68: arm A's backlog-owed and srp-bound at 8x8/1if |
| `harness/train-2509db68/times.txt` | 173 | `28ab4f95e12d907f` | the train's own image at 2509db68: arm A's backlog-owed and srp-bound at 8x8/1if |
| `harness/variant-objects.txt` | 516 | `9ad59eb50a14c210` | each variant's image objects against arm A's |
| `merge/merge-facts.txt` | 1,281 | `01ecb6282f8ab430` | the merge's parents, base, paths and git merge-tree reproduction |
| `pr-body-before-r4.md` | 11,750 | `5c3b1546930d4792` | the PR body as it read before this round (05:49Z edit) |
| `tools/grade1.sh` | 1,715 | `2803fa60ac80d1e3` | a script this round ran |
| `tools/harness1.sh` | 564 | `b92bf2048cee8c00` | a script this round ran |
| `tools/harness_grade.py` | 2,630 | `92c7ea8e07412d00` | a script this round ran |
| `tools/hbase.sh` | 651 | `1d076559cf8c401d` | a script this round ran |
| `tools/hself.sh` | 375 | `3e108e2843f5c448` | a script this round ran |
| `tools/identity.py` | 1,185 | `a67fd355c3820b75` | a script this round ran |
| `tools/index.py` | 2,986 | `f7a7ff630368dfe2` | a script this round ran |
| `tools/la_window.py` | 2,682 | `4f0a93f9bcf11dad` | a script this round ran |
| `tools/penv.sh` | 663 | `89fda3a71eaf2c84` | a script this round ran |
| `tools/poll.sh` | 555 | `cee6ef7be0271f2f` | a script this round ran |
| `tools/rcopy.py` | 1,452 | `da02e309e1ce258c` | a script this round ran |
| `tools/share_census.py` | 1,326 | `94ff5cb8627b645a` | a script this round ran |
