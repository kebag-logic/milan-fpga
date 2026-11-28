[A825] REVIEW READY: round 14 of #977, milan-fpga `pf-977-1` at `a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35`. tsn-c-stack is at `main` `5a07d9b7d87298f04b15aa28f0304ec88b0aef81` and lwSRP at `main` `e27b34c9231abaa862bdb73f807238b330aa4c51`, both unchanged. Nothing is pushed or posted.

This round follows the owner's decision of 2026-11-28 on the 8x8/1if load ceiling (#977, comment 7235670586), which approves 0.79. It also follows the external review of round 13, R958-5 (PR #993 comment 7231383395). That review closed R958-4-F2 and kept R958-4-F1 open until the owner answered.

**1. What changed** (1 commit past `4461d77c`, no firmware change)

| Finding | Commit or file | Fix |
|---|---|---|
| R958-4-F1 MAJOR | `a5b19f70` | Every "owner decision pending" citation of the 0.79 ceiling is replaced. FR_NFR 3.4.1 (`docs/reference/FR_NFR.md:427`) and SPLIT_CONTROL_MEMORY section 13 (`:2548`) link the owner's decision. `flip_grade.py`'s docstring (`:26-28`) and FLIP comment (`:64-68`), and `load_grade.py`'s ceiling history (`:134-135`), cite "#977, the owner's decision of 2026-11-28 on the 8x8/1if load ceiling", with no comment ID. `FLIP`, `RULED_FLIP`, `EDGE_1IF` and every control are unchanged. |
| R958-5-R1 | `PR-BODY.md` | The summary reads "Code corrections are applied; the historical index notes are published beside the round-10 and round-11 receipt indexes", and links both notes (`review-evidence/977-r1/author-r10/receipts/SUPERSESSION-NOTE.md` and `.../author-r11/receipts/SUPERSESSION-NOTE.md` at `63ebbbac`, both verified present). The archived receipts and indexes keep their bytes. |

**2. Results**

| Item | Result |
|---|---|
| Every product ELF against `25ff0632`'s | **80 of 80 byte-identical** at `a5b19f70` (plat_ledger's platform images and the harness's 72; `receipts/elf-identity-a5b19f70.txt`). Round 10d's measurement and both routes stand. |
| 8x8/1if load at the pin | **0.78214** (0.76614 without the deliveries term), within the approved 0.79 |
| 1x1/1if load at the pin | 0.53254, against 0.70 |
| The ceiling's edge | FLIP and RULED_FLIP hold 0.79 at 8x8/1if, and EDGE_1IF is (0.790, 0.791). 0.790 passes and 0.791 fails. With FLIP at 0.77, both ceiling controls escape (`receipts/meas/load-flip-a5b19f70.txt`). |
| The floors | `DELIVERY_US` 155 us at 8x8/1if and 195 us at 1x1/1if are each refused |
| Citations | No "decision pending" in tb/, docs/ or sw/. No comment ID in any Python source. FR_NFR:427 and SPLIT_CONTROL_MEMORY:2548 link comment 7235670586. |
| `load_grade --check` / `--selftest` / `load_deliveries.py` | PASS / 32 of 32 / every control refused |
| `flip_grade --check` at 1x1/1if and 8x8/1if / `--selftest` | PASS, PASS / 628 of 628 |
| Harness self-tests (clean clone at `a5b19f70`) | `run.py --self-test` 0 failures, `kept_grade` 33, `shape_costs` 25 of 25 and `--check` PASS |
| Python and C++ idiom gates | PASS |
| Docs workflow | 100 of 100 steps (em-dash base dev-soft-core `0b594023`), no tracked file changed |
| `git diff --check` over the PR delta | no hit, against `71bad8c0` and against `0b594023` |
| Firmware gate | not re-run: no firmware-tree file changed this round |

**3. Open**

- Nothing for the owner. The review bar, hosted gates and the merge-candidate validation are the manager's.

The receipts are under `receipts/`, indexed in `receipts/INDEX.md`.
