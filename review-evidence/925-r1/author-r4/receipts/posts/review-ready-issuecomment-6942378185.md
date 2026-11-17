[A790] REVIEW READY
Commit: `0fdfdba7`, branch `925-srp-ta-tf`: one documentation commit on round 3's `5f625090` (PR #932). Nothing pushed. Round 4 answers R849-2 (PR #932 issuecomment-6941202858), exactly its F1 and R1; R850-2 is POSITIVE at `5f625090`.

Changed (2 files, +5 -4; no code change):
- R849-2 F1 (MINOR, Docs): `docs/design/SPLIT_CONTROL_MEMORY.md` section 3.
  - The line that stated the 59.0 / 60.5 caps in the present tense now gives them as the state until #925.
  - It then states the owner's decision of 2026-11-15 (#665 issuecomment-6892332745): the caps are no longer stop conditions for the flip lanes, and an image past its entry raises it to its measured size at the next half tile.
  - It states the entries as they now stand: 59.0 for the size fixture's point and 61.0 for the platform's, refused at 59.5 and 61.5.
  - The planted-ledger lines now name the test's own plants (`ctrl_memory_ledger.planted()`): the platform's entry at 61.5, and the fixture's entry at the platform's 61.0.
- R849-2 R1 (RESIDUE): the `sw/litex/ctrl_memory.py` comment now reads "as debt owed to the hybrid XIP work (#665 decision D3)". The string literals are data and are unchanged, as the report says.
- R849-2's S1 and S2 (suggestions) are not taken: the round is exactly F1 and R1.

Validation (clean clones, each in its own unit):
- Image identity, `5f625090` vs `0fdfdba7`, every image: `plat_ledger.py`'s four platform images and both shapes' split-SoC stand-in and mapped images, and the release recipe at both configs. All 24 images are byte-identical: the eight `ctrl_app.elf`, the NVM shape images, the descriptors and `bios.bin`. The debug-stripped `bios.elf` and its disassembly are identical at both configs. Only the static archives and the unstripped `bios.elf` differ, by the clone's directory name in their debug and archive data.
- `plat_ledger.py` at `0fdfdba7`: rc 0, every point PASS (118,128 / 119,712 / 130,752 / 132,304 B of `rom`; 43 / 44 / 56 / 61 RAMB36, as in round 3).
- `python3 -B sw/litex/test_ctrl_memory.py` at `0fdfdba7`: rc 0, 0 failures (the platform's own image at 61.0 accepted; at 61.5 refused).
- `docs.yml`, every job replayed step by step at `0fdfdba7`: 9 jobs rc 0; 61 steps rc 0, 34 hosted-only steps not run with their stated reasons, 0 bad (`verify_wf.py` rc 0; gen_toc --check and --verify-anchors, the idiom gates and docs_check among them).
- `docs_check.py` and `check_py_idiom.py`: rc 0.
- Round 3's other gates at `5f625090` carry: the firmware shards, coverage, both CPU-budget legs, the reviewers' scripts and the rtl-fast replays. This round changes one design document and one Python comment, and no image.

Acceptance criteria: the desk part is met (round 3's evidence, unchanged). The bench part, Listener Ready within 1 s of the Talker Advertise, is the gating run's.

Open risks/questions: none new. Routes remain misses at the base, owed to #927 (no image change); the 8x8/1if stated-cost lines remain #914's.
