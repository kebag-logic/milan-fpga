# HANDOFF r2: [A834] lwsrppin, round 2 (tests + docs only)

Status: **DONE, review-ready** (05:20 CET 2026-11-24). ETA: none, nothing is running.
Head `ed7df79c6f87a4172c885f268ad67629bd56c4eb` is committed in the worktree `/data-2/milan/tmp/lwsrppin-r2`
(branch `lwsrp-pin-r2`, parent `dbba60e6`). It is NOT pushed: the manager pushes it to `20-lwsrp-pin-d1bb4f4`
(PR #992). The worktree is clean (tracked) and on the branch. `/data-2/milan/lanes/lwsrp-pin` was not touched.

Outputs: `REVIEW-READY.md` (the delta from dbba60e6, with commands), `PR-BODY.md` (round-2 copy of the live
body), `receipts/INDEX.md`, `scripts/` (`census.py`, `r1_faults.py`, `docs_gates_r2.py`).

## Commits (one-line, no trailers, no lane labels)

- `4ad6c164` Count the twin grade self-test's checks as they run, and check that the sLA's rLA! takes a Registrar
  IN to LV at txLAF! (`twin_mrp.py`, twin `README.md`)
- `ed7df79c` Describe the own-LeaveAll arms in the firmware gate's srp entry (`test_ctrl_firmware.py` docstring)

## Brief items

| # | Item | Outcome |
|---|---|---|
| 1 | R913-1-F1 | Done. Two new self-test checks after a peer's JoinIn (Registrar IN), with the value left out of a full LeaveAll MRPDU: `omission-from-full-registrar-in` (the JoinMt is legal, configurations {(AA,LV),(AA,MT)}) and `joinin-after-omission-from-full` (JoinIn is one finding). R913-1's `twin_mutants.py`, unchanged: control PASS, 9 of 9 CAUGHT, `txlaf-registrar-kept` among them (by both new checks; it ESCAPED at dbba60e6) |
| 2 | R914-1-F1 | Done. `selftest(ran)` records each check as it runs, and `--selftest` prints that count: `OK (11 checks)`. An outside profile-hook count agrees (11, distinct). R914-1's `probe_twin.py`, run unchanged, reports 11 executed and then trips its own `== 9` pin from dbba60e6. With that constant set to 11, it passes all its probes and 5 of 5 mutations. Count corrected in PR-BODY.md. The twin README never stated a number, and now says the count is the one run. The Makefile states none |
| 3 | R913-1-S1 | Taken: the gate docstring's `srp` entry describes the `srp_own_leaveall.cpp` arms |
| 4 | Gates | `--selftest` OK (11). `make twin`: 0 findings. `make -j2 twin-plants` in one invocation: 16 of 16 refused, 32 refusals; also split in two invocations, same result. Round-1 planted faults 5 of 5 caught. Python idiom gate rc 0, its self-test 54 of 54. 44 `docs.yml` gate steps, each rc 0. Image-input diff empty. 28 of 28 ELF/bin/hex byte-identical between `plat_ledger.py` builds at dbba60e6 and ed7df79c, including `ctrl_app.elf` at 1x1/1if (`30e6ea03…`) and 8x8/1if (`c59a55a2…`) |
| 5 | PR-BODY.md | Made from the live PR body (`receipts/pr-body-live-before.md`): two new commit rows, the self-test row (11 checks, the earlier "10" was a fixed figure for 9 run, and the new planted fault), twin and plant rows at this head, the docs row, and a paragraph on which rows stand from `402834ac` and why |

## Notes for the manager

1. **Push** `lwsrp-pin-r2` (ed7df79c) to `20-lwsrp-pin-d1bb4f4`, then replace the PR body with `PR-BODY.md`.
   Re-review: Tests and Docs at ed7df79c, per both reports.
2. **R914-1's `probe_twin.py` pins `== 9`** (line 22). It also greps for the literal `"OK (10 checks)"`, which now
   prints `[]`, since no count is written into the source. At the corrected head it stops at that assert after
   printing the census. That is expected. The reviewer reruns it with 11 or reads the
   printed census.
3. **Not re-run at this head:** the firmware gate shards, the reproduction, load/flip, harness, `plat_ledger
   --self-test` controls, `test_ctrl_memory` and the OOC map. They stand from `402834ac`, whose sw/hdl/configs/
   third_party differ from this head only by the docstring, and the images are byte-identical. The two builder
   legs of `docs.yml` (`docs-gates-1#14`, `docs-gates-2#14`) were also not re-run, for the same reason.
4. **Why the twin plants were also run split.** A single `make twin-plants` ran serially for 10 to 12 min in round
   1, past this session's 10-min foreground limit. So I first ran it as two invocations of the same rule, with
   `TWIN_PLANTS`/`TWIN_CAPTURE_PLANTS` overrides. Then one unsplit `make -j2 twin-plants` finished in 5m49 (the
   `-j2` runs the two unplanted halves side by side). The unsplit run is the receipt of record.
5. **docs run interrupted once.** The second docs chunk passed the foreground limit, went to the background and was
   stopped at its limit during `docs-gates-2#15`. All 27 steps before that had reported rc 0 (their lines are kept
   from the task output). `#15` and `#16` were then re-run in the foreground, rc 0 each.
6. **Observation, not in scope:** `ci/image/tool-inventory.json` pins `test_ctrl_firmware.py` at `688f7b01…`. That
   is already stale at the base `aa30d77f` (`fe97f74e…`) and at dbba60e6 (`c00df763…`). Its last regeneration was
   2026-10-16, as image-build input. No gate run here reads it as a per-PR check, and I did not regenerate it.
7. **Housekeeping:** scratch `/data-2/milan/tmp/lwsrppin-r2-scratch` (twin mutants, ledger builds, docs copies) can be
   deleted. The worktree holds ignored build trees (`tb/verilator/milan_dp/obj_twin*`, `*.hex`, `__pycache__`).
8. Receipts carry local paths in their raw logs (as round 1's did). Two logs over 200 KB are trimmed, head and
   tail, with the full size and sha256 noted in place.

REVIEW READY ed7df79c6f87a4172c885f268ad67629bd56c4eb
