# Lane 925, round 4: handoff ([A790])

## 1. Scope

The manager's round 4 (resume of 2026-11-17), answering R849-2 (PR #932 issuecomment-6941202858; R850-2 is POSITIVE
at `5f625090`):
- F1 (MINOR, Docs): `docs/design/SPLIT_CONTROL_MEMORY.md:145` and `:173-174` state the platform entry's current cap
  and the current planted ledgers, as the report gives them.
- R1 (RESIDUE): no lane name in the `sw/litex/ctrl_memory.py` comment.
- No code change; every image verified byte-identical to `5f625090`'s; the docs jobs on a clean clone; one REVIEW
  READY. Push nothing. Not taken: R849-2's S1 and S2 (suggestions), outside "exactly F1 and R1".

## 2. Commit (on 5f625090, nothing pushed)

`0fdfdba7` "State the platform entry at 61.0 refused at 61.5 and the planted ledgers at 61.5 and 61.0, and name the
hybrid XIP work for the debt in the ledger's comment (#925)": 2 files, +5 -4.
- `SPLIT_CONTROL_MEMORY.md:145`: the 59.0 / 60.5 caps recast as history ("Until #925 ..."); the owner's decision of
  2026-11-15 (caps no longer stop conditions; an image past its entry raises it at the next half tile); the entries
  as they stand, 59.0 and 61.0, refused at 59.5 and 61.5.
- `:173-174`: "plans 61.5" (the platform's planted ledger) and "plans the platform's 61.0" (the fixture's), as
  `ctrl_memory_ledger.planted()` holds them.
- `ctrl_memory.py:250`: "as debt owed to S14" -> "as debt owed to the hybrid XIP work (#665 decision D3)". The
  string literals naming S14 (`:257`, `:265`, `:269`, `:281`) are data, unchanged per the report.

## 3. Evidence (receipts/)

| Gate | Head | Result | Receipt |
|---|---|---|---|
| image identity, every image (plat_ledger's 4 platform and 4 split-SoC images, the release recipe at both configs), each head on its own clean clone and unit | 5f625090 vs 0fdfdba7 | all 24 images (ctrl_app.elf x8, NVM shape images, descriptors, bios.bin) byte-identical; stripped bios.elf and its disassembly identical; only archives and unstripped bios.elf differ, by the clone path | identity/ |
| plat_ledger.py | 0fdfdba7 (clean) | rc 0, PASS at every point (same figures as round 3) | identity/ |
| test_ctrl_memory.py | 0fdfdba7 (clean) | rc 0, 0 failures | ledger/ |
| docs_check, check_py_idiom (worktree = 0fdfdba7) | 0fdfdba7 | rc 0 | (session) |
| docs.yml replay, every job | 0fdfdba7 | 9 jobs rc 0; 61 steps rc 0, 34 hosted-only steps not run with their stated reasons, 0 bad (`verify_wf.py` rc 0; gen_toc --check and --verify-anchors, the idiom gates and docs_check among them). | workflows/ |

Round 3's other gates (firmware shards, coverage, both budget legs, the reviewers' scripts, the rtl-fast replays) carry
from `5f625090`: the round changes one design document and one Python comment, and no image changes.

## 4. Run history

- 08:0x resumed (host restarted; no helper unit ran; tree clean at 5f625090); R849-2 report and the round read.
- 08:1x the fix, committed `0fdfdba7`; image units (base and head) and the docs replay started (96-CPU host, 0-63).
- 08:2x images identical; test_ctrl_memory PASS on the clean clone.
- 09:05 docs replay rc 0 (61 rc 0, 34 with reasons, 0 bad).
- 09:1x receipt.sh wrote this round's receipts into round3/receipts (its directory was fixed); moved here, and round 3's three overwritten files (ledger/test_ctrl_memory.log, workflows/docs-verify.md, workflows/docs.log) restored from the archive: round3/receipts equals author-r3/receipts again (diff -r empty).
- 09:1x REVIEW READY posted: #925 issuecomment-6942378185.
