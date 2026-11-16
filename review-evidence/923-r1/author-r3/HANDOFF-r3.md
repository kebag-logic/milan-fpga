# HANDOFF round 3 — [A789] lane 923 (#923 + #924) — REVIEW READY at `d06ded5a` (#923 issuecomment-6931638262)

Round 3 fixes exactly R848-1's findings (PR #931 issuecomment-6928957357; its packet's REPORT.md and
late-timeout.log read in full) and R847-1's F1 (issuecomment-6929792570, added by the manager at 22:2x; its F2 and R1
are R848-1's F2 and F3). Branch `923-aecp-maps`, on `16ba667d`; round 2's head `70c100da` is published (PR #931,
base dev-soft-core). Round 3's commits are local; nothing pushed.

## 1. Changes (file:line at `d06ded5a`, reason)

| Commit | File:line | Change | Finding |
|---|---|---|---|
| `88676700` | `sw/firmware/ctrl/test/test_aecp.cpp` `Far` (the store model, ~3952-3990) | `mute`'s 2 on a record's commit (phase 5) or the finish (phase 2) takes the beat and loses only its reply; on a begin, a validation or the commit-begin it is held, not taken, as before. The model's comment states the contract it follows: the release engine reserves the transaction at an accepted commit-begin and has phases 5 and 2 complete without back-pressure (`protocol-processor/hdl/aecp/KL_aecp_engine.sv:465`). `beats` is now every beat the store took. | F1: the model suppressed both the write and the reply |
| `88676700` | `test_aecp.cpp` `Face.AnUnansweredEditFailsUntilItsCommitIsReserved` | `agree(14)` after each post-commit case (phase 5, phase 2); its comment says the store took the beat | F1: the phase-5 tail had no agreement check |
| `88676700` | `test_aecp.cpp` `Face.ALostReplyAfterTheReservedCommitLeavesTheStoreAndTheMapAgreeing` (new) | a two-record ADD and REMOVE with the second, then the first, record's commit reply lost: SUCCESS, the lost reply counted, the map as expected, `agree(14)` after each | F1: the reviewer's two-record ADD case, in the contract's form |
| `88676700` | `test_aecp.cpp` `Face.ALostReplyInTheRestoresCommitLeavesTheStoreAndTheMapAgreeing` (new) | the restore's commit: a removal of the reset set (restored map empty) and an addition of a restored set, each with its second, then its first, record's reply lost; the lost reply counted, the restored map stands, `agree(14)` when AECP opens | F1: the reviewer's restore-removal case, and the boot restore's agreement |
| `88676700` | `sw/firmware/ctrl/test/aecp_map_mutants.py` row `window-lost-reply-stops-the-commit` | the face stops committing at a lost reply (`aecp_face.c`'s APPLY loop `k < count && record(...)`): the store's application of the later records is missing while the edit answers SUCCESS; caught by both new tests on "GET_AUDIO_MAP and the datapath's store hold the same mappings" | F1: the plant |
| `88676700` | `sw/firmware/ctrl/aecp/README.md:184-190` | the guarantee the model follows: after an accepted commit-begin a commit or finish with no answer has been taken, only its reply lost, counted; delivery loss after the commit-begin is outside the contract and has no recovery here | F1: the claimed guarantee stated where the port is documented (no rollback contract invented) |
| `08901183` | `sw/firmware/ctrl/plat/README.md:111` | "888 B" -> "1,280 B of `rom` past what 56.0 held" (132,352 - 131,072; section 5's figure; round 1's receipts rom/images-*) | F2 |
| `d06ded5a` | `test_aecp.cpp` `Face.AnEditCommitsTheMappingsTheCorePicksAndNoOthers` (new) | through the face and the `EDIT` window, a `pick` that is not the identity: an ADD of a held and a new mapping validates and commits the new one alone (COUNT 1), and a REMOVE naming a mapping twice commits each distinct mapping once (COUNT 2); the validated and committed records asserted, `agree(14)` after each | R847-1 F1 |
| `d06ded5a` | `aecp_map_mutants.py` row `window-pick-ignored` | the face reads the command's first records (`records + 8u * (pick != NULL ? k : k)`, the reviewer's probe): caught by the new test on "the records the core picked are committed"; the reviewer's `r847_probe_mutants.py --only face-pick-ignored` turns it red (the unplanted control green) | R847-1 F1 |
| `63c60ad9` | `sw/litex/ctrl_memory.py:243-248` | "debt owed to S14" -> "debt owed to the cold-code-to-flash work", "until S14" -> "until that work lands"; the comment reflowed, #923 and #665 D3 and every figure kept | F3 |

No firmware source changed: `aecp_face.c`, `aecp_maps.c` and every other compiled file are `70c100da`'s.

## 2. Evidence (round3/receipts/, INDEX.md)

| Gate | Head | Result | Receipt |
|---|---|---|---|
| The workflow jobs of rtl-fast.yml, elaborate.yml, docs.yml, step by step on clean clones | d06ded5a | 118 steps rc 0, 130 not run with a reason, 0 bad; AECP 331/331, SRP 421/421, control 716/716; coverage PASS (39 files); census, ctrl_boundary, docs gates | workflows/verify-d06ded5a.md |
| AECP app arm, 1 and 2 interfaces | d06ded5a's content | 164 tests PASS each (161 + 3) | tests/aecp-app-if*.txt |
| Round 2's store model (write dropped with the reply) on a scratch copy | d06ded5a | the three late-reply tests fail on the agreement words: CONTROL PASS | tests/old-model-control.txt (round3/scripts/old_model_control.py) |
| Every edit-, window- and restore- plant | 88676700 | 32 of 32 caught | plants/edit-window-restore-plants.txt |
| The round's two new plants | d06ded5a's content | 2 of 2 caught by name | plants/new-round3-plants.txt |
| R847-1's probe `--only face-pick-ignored` | d06ded5a's content | the new test fails under it; the unplanted control passes | plants/r847-probe-face-pick-ignored.txt |
| Platform images 1x1/1if, 8x8/1if and the release image | d06ded5a against 70c100da | byte-identical (ctrl_app.elf caec0abc, 59b9b736, the routed ones too; exports identical outside comments; bios.bin) | images/IDENTITY.txt |
| docs_check, doc paths, doc style, cpp/py idioms, diff --check | d06ded5a | rc 0 each | (foreground) |

Carried from round 2 unchanged (no firmware, RTL or harness input changed): the six head and two base routes, the CPU
budget harness, the 4-shard sweep, twin-maps (its sources unchanged since 70c100da).
