[A825] REVIEW READY: round 12 of #977, milan-fpga `pf-977-1` at `3256d1d21e525e564eb92d1cf721750ddf44fde2`. tsn-c-stack is at `main` `5a07d9b7d87298f04b15aa28f0304ec88b0aef81` and lwSRP at `main` `e27b34c9231abaa862bdb73f807238b330aa4c51`, both unchanged. Nothing is pushed or posted.

This round answers both re-reviews of round 11: PR #993 comments 7229653191 (internal R957-3) and 7229617575 (external R958-3). It follows the manager's decision on #977, comment 7229657853. The 8x8/1if load ceiling of 0.79 waits on the owner's answer. It is one droppable commit, `3256d1d2`, the last on the branch, so `git revert 3256d1d2` alone drops it.

**1. What changed** (4 commits past `3181a3ec`)

| Finding | Commit | Fix |
|---|---|---|
| Ceiling (manager's instruction) | `feefd047` | Reverts the 0.78 raise (`9976b94f`). |
| R958-3-F1 MINOR | `0a71ca6b` | Each ceiling control's name is built from `RULED_FLIP` and `EDGE_1IF`, so `controls()` and `CONTROLS` name it alike. `flip_checks()` and `load_grade.ceiling_checks()` each fail any escape they do not name. With 8x8/2if at 0.71 both paths fail the ceilings control, and an unnamed escape fails both. Two new mutants; `flip_grade --selftest` 628 of 628. |
| R957-3-F1 MAJOR; decision items 1-3 | `ddf5c568` | `DELIVERY_US` is costed against the accepted baseline: the median polls base of the ordinary passes in the 50 ms after the delivery window (the record's pass and the 2 x n_sinks deliveries after it), by the rule, over both arms at both points. It is 160 us at 8x8/1if (15,104 cycles a sink, the answering-ports swap) and 200 us at 1x1/1if (18,778, the answering-ports JoinIn of both kinds with a change owed). `DELIVERY_MEASURED` is the gate's floor, and the renamed control refuses a lower figure. `DELIVERY_BESIDE` records the 50 ms and 500 ms pre-record medians: 125 and 145 us at 8x8/1if, 190 and 200 us at 1x1/1if. The window and the reason are stated in `load_grade.py` and in design section 13, which links comment 7229657853. |
| R957-3-R1, R2; S1 | `ddf5c568` | R1: the comment describes the method without a tool's name. R2: README's pass-cost sentence names the `deliveries` exception. S1: `srp_deliver_mutants.py` says the unprefixed plants run in the two-interface campaign. |
| R957-3-F2 MINOR | `ddf5c568`, `3256d1d2` | Every citation of the decision names #977 comment 7229657853 (`load_grade.py:13,374`, `load_deliveries.py:3-4`, `flip_grade.py:64-66`), and the design document's section 13 and FR_NFR 3.4.1 link it. `git grep` finds no "manager's decision of 2026-11-27" and no link to 7226275798 in sw/, tb/ or docs/. |
| R958-3-F2; decision item 4 | `3256d1d2` (droppable) | The 8x8/1if flip ceiling is 0.79, owner decision pending. The control holds 0.790 within it and 0.791 over. FR_NFR 3.4.1 and the design document follow. The manager amends the citation when the owner answers. The PR must not merge with "pending". |
| R957-3-R3, R958-3-R1 | `PR-BODY.md` | The link labels are "[the internal review]" and "[the external review]", matching the manager's live fix. |
| R957-3-R4, R958-3-R2 (packet) | `round10/receipts/INDEX.md`, `round11/receipts/INDEX.md` | Round 10's index gets a dated note (2026-11-28) saying that round 11's packet and the current PR supersede four pieces of its wording: the pending-80-ms wording, the reviewer placeholders, the all-zero run counts and the default-option explanation. Both indexes get a publication note mapping each `.txt.gz` row to its published `.txt` path, with the published manifest as hash authority. The notes are appends only and remain to be published. |

**2. Results**

| Item | Result |
|---|---|
| Every product ELF against `25ff0632`'s | **80 of 80 byte-identical** at `3256d1d2` (plat_ledger's platform images and the harness's 72; `receipts/elf-identity-3256d1d2.txt`). Round 10d's measurement and both routes stand. No arm was re-run. |
| DELIVERY_US, against the ordinary passes after the window (both arms, 40 registering records a point) | 8x8/1if 15,104 cycles a sink, **160 us**; 1x1/1if 18,778, **200 us** (`receipts/meas/deliv-*-e59cf6ea.txt`) |
| Beside it: the 50 ms and 500 ms pre-record medians | 8x8/1if 11,573 and 13,642 cycles, 125 and 145 us; 1x1/1if 18,076 and 18,765, 190 and 200 us |
| 8x8/1if load at the pin | **0.78214** with the deliveries term (0.76614 without it; 0.77864 and 0.78064 at the two pre-record costs), within 0.79 and over 0.77. At `ddf5c568` (0.77) `flip_grade --check --point 8x8/1if` fails on it. |
| 1x1/1if load at the pin | 0.53254, against 0.70 |
| The floor | `DELIVERY_US` 155 us at 8x8/1if is refused: "under its measurement's 160 us by the rule" (`receipts/meas/load-flip-3256d1d2.txt`) |
| The ceiling's edge | 0.790 passes and 0.791 fails. With FLIP at 0.77 (the revert), both ceiling controls escape. `git apply -R --check` of `3256d1d2`'s patch is clean. |
| The adapters (R958-3-F1) | At the head neither adapter fails anything. With 8x8/2if at 0.71, `flip_checks()` and `load_grade.ceiling_checks()` both fail the ceilings control. An escape no control names fails both. |
| `load_grade --check` / `--selftest` / `load_deliveries.py` | PASS / 32 of 32 / every control refused |
| `flip_grade --check` at 1x1/1if and 8x8/1if / `--selftest` | PASS, PASS / 628 of 628 |
| Harness self-tests (clean clone at `3256d1d2`) | `run.py --self-test` 0 failures, `kept_grade` 33, `shape_costs` 25 of 25 and `--check` PASS |
| Python and C++ idiom gates | PASS |
| Docs workflow | 100 of 100 steps (em-dash base dev-soft-core `0b594023`), no tracked file changed |
| `git diff --check` over the PR delta | no hit, against `71bad8c0` and against `0b594023` |
| Firmware gate | not re-run: the only firmware-tree change is a docstring sentence in `srp_deliver_mutants.py`; round 11's four shards at `9976b94f` stand |

**3. Open for the owner and the reviewers**

- **The 8x8/1if load ceiling, 0.77 to 0.79.** The manager is asking the owner. If it is refused, revert `3256d1d2`, the 8x8/1if flip check then fails at 0.782, and 8x8/1if waits for #1025's margin recovery.

The receipts are under `receipts/`, indexed in `receipts/INDEX.md`.
