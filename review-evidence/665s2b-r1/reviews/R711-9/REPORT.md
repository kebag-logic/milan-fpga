[R711] POSITIVE - exact head 325514224bcc356a6b43843f1003c2323f09de25

# R711-9: internal cleared-context delta review of PR #810 (#665 Mark II split, stage S2b), round 30

Exact head `325514224bcc356a6b43843f1003c2323f09de25`, tree `a3ca67b9b69d9de4ef9da684e56082c4a05d3bae`. Delta from round 29's `b2d39235` (R711-8, NEGATIVE).

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open.
- Both round-29 MINOR findings (F1 platform ledger, F2 SRP control) are closed at this head.
- The RTL fix, both merges, the restated costs, the load gate, the ledger gate and the cost controls hold against code and receipts.
- Two RESIDUE items (wording only) and four SUGGESTIONs are recorded below. None affects the verdict or any lens.

## Method and scope

- Context was rebuilt in this order:
  1. AGENTS.md, then CONTRIBUTING.md through AGENTS.md;
  2. the #665 rulings 6828629878 (round 29, items 1-6), 6831583372, 6835550732 and 6842347916 (the three STOPs);
  3. the owner decisions 6824896581 and 6845315282;
  4. REVIEW READY 6848807388;
  5. the diff and history `b2d39235..32551422` (first parent: nine commits, merge `187eeed8`, ten commits, merge `32551422`);
  6. the signed packet `review-evidence/665s2b-r1/author-r30` at archive `8d591986`.
- The round-29 reviews (R711-8 6828561870, R712-8 6828619213) were read only after my own pass over the diff.
- The packet's integrity: all 820 `author-r30` files match `MANIFEST.json`'s `published_sha256` (`receipts/packet_manifest_verify.txt`).
- **Own probes**, on a `git archive` copy of the head under `scratch/` (the clone was not modified; `receipts/clone_integrity.txt`):
  - the mover bench `make run-dma`, with the pinned Verilator 5.050 (wrapper sha256 `905795b9...`, `--version` 5.050 rev v5.050);
  - `dma_mutants.py --jobs 16`;
  - `ctrl_retry_search.py` as committed, and with `AECP_ROUND_COLD_US` 2if set to 184 and to 186;
  - `load_grade.py --check` and `--selftest`;
  - `flip_grade.py --selftest` and `--check --point 1x1/1if`;
  - a replay of merge `187eeed8` with `git merge-tree`;
  - a re-derivation of the trigger-1 tally (`scripts/rederive_trigger1.py`);
  - a comment-rule scan of every added non-Markdown line.
- Heavy legs, builder banks, Yosys, the harness legs, plat_ledger's builds and the full sweep were not re-run. For those I rely on the author's published final-head receipts (`receipts/final-5bea2597/` in the packet), whose tree equals this head's.

## Findings

No BLOCKER, MAJOR or MINOR.

### RES-1 - RESIDUE - Docs - live PR #810 body - the PR body is still round 28's

- **Evidence.** The live body opens `[A683zm]` and states round 28's status. The packet's `author-r30/PR-BODY.md` (434 lines) is round 30's. This retains R712-8 RES-1, which is still unfixed.
- **Impact.** It is wording only. A cold reader of the PR sees round 28's figures (for example R4 73.02 ms). No measurement, test or code changes.
- **Exact fix.** Publish `review-evidence/665s2b-r1/author-r30/PR-BODY.md` (archive `8d591986`) as the PR #810 body.
- **Verification.** The live body's first line is `[A683zo]` and its Status section reads "round 30".

### RES-2 - RESIDUE - Docs - `sw/litex/ctrl_memory.py:257`, `:264` - new ledger reason text names a lane

- **Evidence.**
  - Two strings added in the delta say "ROM debt owed to S14" (`receipts/comment_rule_scan.txt`).
  - They are reason strings in `LEDGERED`, not comments, so the owner comment rule (2026-10-15) applies only in spirit.
  - The neighbouring "lane S14 ... rulings 6412739248" text predates the delta and is tracked by #746.
  - No added source **comment** in the delta carries a lane label, round, reviewer ID or comment ID.
- **Impact.** Wording only. `test_ctrl_memory.py` compares each entry's symbols and tiles, not its reason.
- **Exact fix.** "ROM debt owed to S14" -> "ROM debt owed to the hybrid XIP work (#665 decision D3)", at both lines.
- **Verification.** `grep -n 'owed to S14' sw/litex/ctrl_memory.py` returns nothing, and `test_ctrl_memory.py` passes.

### S1 - SUGGESTION - RTL, Robustness - `hdl/milan/mailbox/KL_mbx_dma.sv:296`, `:391` - the mover's own answers are still counted by cycle

- The CPU path now waits for `host_ack_i` (`:407`).
- The mover's own requests still take their answer to be the next cycle: `hold_r <= fill_req_w || ring_wr_w`, and the buffer captures at `hold_r` without `host_ack_i`.
- That is correct for the event and receive ring words, which `KL_mbx` answers the cycle after (`KL_mbx.sv:1424`).
- But a `ring_base_i` programmed outside those rings would be a register read, answered two cycles later. The mover would capture noise silently.
- This is driver misprogramming only, it predates the delta, and the ruling's item 1 covers the CPU path. Optional: gate the capture on `host_ack_i`, or state the precondition on `ring_base_i` in the header.

### S2 - SUGGESTION - Tests - `tb/verilator/mbx/dma_main.cpp:86`

- D11 runs against a hand-copied model of `KL_mbx`'s register/ring split (`kRingReads`).
- The real pairing is pinned only by the split boot, which reads registers with the mover mostly idle.
- Optional: a co-simulation of `KL_mbx_dma` on the real `KL_mbx`, with a register read held behind a transfer and one issued in a transfer's first cycle. That would pin the pairing without the model.

### S3 - SUGGESTION - Conformance, Docs - trigger 2's reading

- The fresh 8x8 legs at `6c284a97` printed 34 `STATED` lines for "a pass's polls base" over the then-table 28,000 cycles, with a maximum of 30,659 (packet `receipts/ruling3/legs-F-GN8.txt`).
- REVIEW READY reports trigger 2 as "no round or pass given whole over its stated cost". That reads "stated cost" as the firmware-stated costs, and the polls base as a grader-table item.
- That reading matches the ruling's own split between **Stated costs** and **Tables**, and that table item had already been named to the ruler at `da1869a3` (the STOP3 README). I accept it.
- Optional: say so in one line in section 13, so that a later reader does not take those `STATED` lines for a fired trigger.

### S4 - SUGGESTION (carried) - Tests - `test_aecp.cpp` refusal and lost-frame tests

- R711-8 S6 (from R711-7 S6) is unchanged: no test resumes a walk across interfaces.
- Ruling 6828629878 item 6 does not route it, so it stays a suggestion here.

## Round-29 findings at this head

| Item | Status | Evidence at this head |
|---|---|---|
| R711-8 F1 = R712-8 F1 (MINOR): the platform 8x8/2if ledger at 59.0 against the owner's 60.0 | **Closed** | `ctrl_memory.py:259-260` LEDGERED platform 60.0, refused at 60.5; the fixture is at 58.5 by the STOP ruling (`:252-253`). `plat_ledger.py --self-test` at `5bea2597` passes: 8x8-if2 59.5 within `platform-8x8-two-interfaces`, the other points within 56, 7 of 7 controls as required, among them `stale-key` and `past-its-tiles` (`final-5bea2597/lane/plat_ledger.log`). `SPLIT_CONTROL_MEMORY.md:264` states the decision; no "56 RAMB36 or fewer at every point" or "stays 59.0" text remains. |
| R711-8 F2 = R712-8 F2 (MINOR): the SRP control escapes | **Closed** | Option (c): `run.reference_run` and `reference_verdict` (`run.py:593`, `:623`), at `REFERENCE_MARGIN_PERCENT = 5` (`poll_items.py:137`). The final-head control is caught at 34,551 against 30,989 cycles unplanted, 11.5 % (`final-5bea2597/harness/controls/ctl-srp-compared-by-memcmp-5bea2597.log`). Six self-test plants guard the reference (`selftest_mutants.py`). README `:1421-1428` and section 13 `:2281` describe it as built. The table rule is unchanged; no stated cost was lowered. |
| R711-8 S1 = R712-8 S1: rule windows off the 2 ms grid | Taken | `rows_grade.rule_windows` (`:346`) adds each solved row's W and R4's edge +/-1 us. Control "SRP's arrivals cut by two records of AECP" is in `flip_grade.RULE_CONTROLS`; `flip_grade.py --selftest` gives 132 of 132 (own run). |
| R711-8 S2: RETAINED_ROWS reading | Unchanged by ruling item 5 | Published open risk; #894. |
| R711-8 S3: no gate links the platform image | Taken | `plat_ledger.py` (above). |
| R711-8 S4 (mover ERR resend), F-HOOKS | Routed to their own issues by ruling item 6 | Not in this delta. |
| R711-8 S5; R712-8 S3, S4 | Routed to #894 | Not in this delta. |
| R711-8 S6 | Carried | S4 above. |
| R711-8 S7 = R712-8 S6: the packet's index | Manager duty (ruling item 6) | 800 of 819 `INDEX.md` rows verify against the published files. The 19 that do not are exactly the 19 `path_redacted` entries of `MANIFEST.json`, whose `original_sha256` equals the index hash (`receipts/author_index_verify.txt`). The redaction ran after indexing, so this is a publication step, not an author defect. |
| R712-8 S2: driver test T7 and its plant | Taken | `test_mbx_dma_driver.cpp:443` and the `mover-fan-end-refuses-before-the-last-frame-is-committed` plant; the final mutant runs are 698/698 control (REVIEW READY). |
| R712-8 S5: `--check` refuses swapped columns | Taken | `load_grade.unbound` (`:348`) is in `findings`; `binding_controls` (`:515`) plants swap, drop and equal copy. Own `--selftest`: 25 of 25 (12 controls + 13 periods). |
| R712-8 S7: `also` on the expiry row | Taken | `acmp_mutants.py:784`. |
| R712-8 RES-1: PR body | **Retained** | RES-1 above. |

## The brief's checks

**(2) Both merges.**
- **`187eeed8`.** A `git merge-tree` replay of `70e30d7b` + `8bc1dfc0` conflicts in 11 files (`receipts/merge1_replay.txt`). Against the replay, the recorded merge differs in those 11 and in two others (`receipts/merge1_resolution_stat.txt`, `merge1_resolution_code.diff`):
  - `nvm_store.c` keeps this branch's `nvm_mark(id)` with the other side's `nvm_open_set(&nvm.dirty, id)`. `nvm_mutants.py`'s `budget_rearmed_by_change` follows it.
  - `coverage.ratchet` takes the composed tree's counts. `fw_coverage.py --check` passes over 39 files at the final head.
  - The ledger, ledger test and ledger text take this branch's 60.0 with the composed `nvm_stage` 13,594. `ctrl_plat` stays 20,288, this branch's struct.
  - `split_soc.py`'s docstring is the union of both sides.
  - Two files that did not conflict change: `nvm_any` leaves `ctrl_split.ld` and `ctrl_split_hot.txt`. The function is still in `nvm_store.c:154`, inlined, and a hot-list name with no section refuses the link. The change is named in the merge subject and in section 5 `:467`. `ctrl_hot.py --check` gives 206 entries in order.
  - No RTL, mailbox-contract or protocol file is touched by the resolution.
- **`32551422`.** Its tree is `a3ca67b9`, identical to `5bea2597`'s (`receipts/merge2_identity.txt`). Over the merge base `8bc1dfc0`, `e5f88a8e` adds only 4 changed lines in two docs. This branch's kept text states the same facts at round 30's values: README `:49`, `:247` give 58.5; section 5 `:442-470` gives the margins. No behaviour is dropped.

**(3) The RTL fix (`420d44e4`).**
- `cpu_wait_r <= cpu_issue_w || (cpu_wait_r && !host_ack_i)` (`KL_mbx_dma.sv:407`) holds a CPU request from its issue to `KL_mbx`'s answer, however long it takes. No second latency is coded.
- `cpu_ack_o = host_ack_i && cpu_wait_r` (`:240`).
- The mover's requests, beats and `rready` wait while a CPU request is in flight (`:200-201`, `:212`, `:271`).
- The rule comes from the merged port: `KL_mbx.sv:42` and `:1424`, with `ack_r <= (host_req_i && !reg_rd_w) || rd_q_r`.
- `KL_mbx_wb` issues one pulse and none until its answer, so `cpu_issue_w` is one cycle per request. A request held for a transfer is issued once, when `pend_r` clears.
- **Own run of `make run-dma`:** 520,041 checks, 0 failures (`receipts/run-dma.log`).
- **Own run of `dma_mutants.py --jobs 16`:** 24 of 24 caught (`receipts/dma_mutants.log`). These include:
  - `cpu-answer-one-cycle`, the old pairing restored, caught at "D11 a CPU register read is answered two cycles after its request";
  - `beat-during-cpu-answer` and `mover-during-cpu-answer`.
- The author's final-head sweep `mbx.log` shows the same 520,041 and 24/24.
- **CDC:** `split-cdc` step 10, 13 checks, 0 failures.
- **Lint:** the ratcheted lint gate passes, 89 <= 89.
- **Yosys:** `yosys-elaboration` step 7, 3 of 3 tops.
- **Area:** 704 flops before and after, LUTs 484 -> 487 (`rtl-fix/area/SUMMARY.txt`), within "its own few flops".
- **Split boot at the final head** (`lane/boot_*.log`): PASS at 1x1/1if, 8x8/1if and 8x8/2if, ready at 26.370, 66.017 and 68.371 ms, matching `ctrl_split_boot/README.md`. Its plants: 6 of 6 native controls, 3 of 3 plants, 8 of 8 placement controls.
- The boot at `a4faefd4` failed "mailbox contract mismatch" (`resume-mover-ack/boot-a4faefd4-1x1.log`). So the gate fails for the defect it claims.

**(4) The stated costs.**
- **Re-derived trigger 1** from the published tally (`receipts/trigger1_rederive.txt`): every (n, k) row's implied cold cost (dearest/100 - 365n or 255n - 34k) matches the author's to 0.01 us.
- The dearest is GN8 n=0 k=2 at 180.16 us, within 183.1. No k=0 or k=1 round is near it; the dearest k=1 is 81.41.
- Every row's dearest is within its stated line, C + nW + 34k, at C = 185 (8x8/2if) and C = 85 (1x1/1if).
- The fresh-build tally (`ruling3/trigger2-rounds-fresh-8x8.txt`) is row for row identical to the 8x8 legs'.
- The final-head regrades (`final-5bea2597/harness/X-*-regrade.log`) print no `STATED` line, 0 refusals, the 7 recorded misses and no pass over the share. Each sample's image is byte-identical to the graded build, and its sample log is identical.
- **The retry search (own runs):**

  | Copy | Result |
  |---|---|
  | as committed (185 us) | PASS, first notice 22 ms at 2if (`AECP_QUEUED_FIRST_MS` 22 unchanged, `aecp_mbx.h:53`) |
  | 184 us | PASS |
  | 186 us | FAIL, "the first notice at 2 interface(s): 28 ms over AECP_QUEUED_FIRST_MS" |

  So 185 is the largest the search holds, as ruled.
- **Restated firmware costs.** `ctrl_loop.h:270-271` gives 1,010 and 430 us at 1x1. From 96,033 and 40,700 cycles, the rule gives 1,008.3 -> 1,010 and 427.4 -> 430.
- **The margin exception** is stated in all three places, with its expiry and #890's 176.1 us: `aecp_mbx.h:21-27`, `FR_NFR.md:372` (inside 3.4.1, `:331-441`) and `SPLIT_CONTROL_MEMORY.md:2178-2180`.
- **The tables against the tally** (`poll_grade.py:63`, `load_grade.py`; maxima computed from the published verdict lines):

  | Item | Measured maximum | Rule figure | Table |
  |---|---|---|---|
  | polls base, 8x8 | 30,659 | 321.9 -> 325 | 325 |
  | polls base, 1x1 | 19,159 (the ruling's) | 201.2 -> 205 | 205 |
  | rebuild, 8x8 | 65,390 | 686.6 -> 690 | 690 |
  | walk, 1x1 | 3,026 | 31.8 -> 35 | 35 |
  | SRP apply, 1x1 | 26,067 | 273.7 | 280 (>= the rule figure) |

**(5) The load gate (own run).**
- `load_grade.py --check`: 1x1/1if 0.501 at the pin and 0.499 with #32, both within 0.70, RESULT PASS.
- The output is byte-identical to the author's final-head receipt.
- `--selftest` gives 25 of 25. `flip_grade.py --check --point 1x1/1if` exits 1 at R4 74.83 ms against 20, the #894 tier row that stays red by design.

**(6) The ledger gate and the four cost controls.**
- `plat_ledger.py`: as in F1.
- The controls at the final head, each caught with 0 refusals:

  | Control | Planted | Against |
  |---|---|---|
  | `notice-fan-out-as-it-was` | 30,266 | 27,000 |
  | `polls-rebuild-in-the-base` | 74,295 | 32,500 (restated) |
  | `polls-rebuild-twice` | 109,171 | 69,000 (restated) |
  | `srp-compared-by-memcmp` | 34,551 | 30,989 unplanted |

**(7) The full pass at the final head.**
- Three clean clones at `5bea2597`, 0 changed paths.
- The workflow steps: 139 rc 0 and 226 not run, each with its reason (`workflows/verify-table.md`, 139 step logs published).
- The full sweep in four shards; the lane gates are all rc 0, apart from the three flip checks that exit 1 by design.
- `5bea2597`'s tree equals this head's, so the receipts carry to `32551422`.
- Hosted at this exact head: 13 contexts succeeded, 1 skipped, and 30 were queued or in progress when inspected (`receipts/hosted_checks_at_head.txt`). Hosted and act acceptance is the manager's.

**Commit form.** All 21 first-parent commits in the range are one line with no trailers (`receipts/commit_lines.txt`).

## Lens results (each with its artifact)

- [R711] PASS Conformance — `ctrl_memory.py:252-265`, `aecp_mbx.h:21-29,53`, `ctrl_loop.h:270-271`, `FR_NFR.md:372`, `KL_mbx.sv:42,1424`, own retry-search, load and flip runs — the rulings' items 1-4, the STOP rulings' constants and triggers 1-4, and the owner decisions against the code and the re-derived tally.
- [R711] PASS RTL — `KL_mbx_dma.sv:200-240,296,391,407` against `KL_mbx.sv:1405-1439` and `KL_mbx_wb.sv`; the CDC, lint and Yosys step logs; `rtl-fix/area/SUMMARY.txt` — request tracking and answer routing on the merged port, with no new crossing or clock.
- [R711] PASS Robustness — the D11 cases (alone, held behind a transfer, in a transfer's first cycle, and no request while one awaits its answer), D8 reset, own 24/24 mutants; `flash.hpp:116` refuses spans that are not whole blocks; the journal bound and its set-span cases. S1 is optional.
- [R711] PASS Tests — own `run-dma`, `dma_mutants`, `load_grade --selftest`, `flip_grade --selftest`; the final-head control and boot plant receipts; T7 and its plant; the binding controls; the merge's `nvm_mutants` arm — each new check can fail for the defect it names.
- [R711] PASS Docs — `SPLIT_CONTROL_MEMORY.md:264,442-470,2178-2180,2281,2299`, `MAILBOX_SPLIT.md`, `ctrl_split_boot/README.md` (the gate at every sync, the ready times), `ctrl_service_budget/README.md:49,247,1421-1430` — each against the head and the receipts. RES-1 and RES-2 are wording only.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | rulings 6828629878, 6831583372, 6835550732, 6842347916; decisions 6824896581, 6845315282; `ctrl_memory.py`, `aecp_mbx.h`, `ctrl_loop.h`, `FR_NFR.md` 3.4.1; trigger-1 re-derivation; own retry-search, load and flip runs | R711-9 | `325514224bcc356a6b43843f1003c2323f09de25` |
| RTL | CLEAN | `KL_mbx_dma.sv`, `KL_mbx.sv`, `KL_mbx_wb.sv`; split-cdc, lint and Yosys elaboration logs; area summary | R711-9 | `325514224bcc356a6b43843f1003c2323f09de25` |
| Robustness | CLEAN | D11, D8, the 24 mover mutants, `flash.hpp` journal span, the merge's `nvm_mark` path | R711-9 | `325514224bcc356a6b43843f1003c2323f09de25` |
| Tests | CLEAN | `dma_main.cpp`, `dma_mutants.py`, `test_mbx_dma_driver.cpp` T7, `selftest_mutants.py`, `load_grade.binding_controls`, `rows_grade.rule_windows`, `plat_ledger.py`; own runs and final receipts | R711-9 | `325514224bcc356a6b43843f1003c2323f09de25` |
| Docs | CLEAN (RES-1 and RES-2 carried as residue) | `SPLIT_CONTROL_MEMORY.md` sections 5 and 13, `MAILBOX_SPLIT.md`, the harness, split-boot and mbx READMEs, the live PR body | R711-9 | `325514224bcc356a6b43843f1003c2323f09de25` |

## Real limits

- **Raw harness logs are not published.** The per-round logs (`results/*.log`, MB-sized) are not in the packet. Trigger 1 is re-derived from the author's tally JSON and the verdict lines, not from raw rounds. I did not re-run any harness leg, control or plat_ledger build.
- **The full sweep, workflow jobs and lane gates** are the author's receipts at `5bea2597`, the same tree as this head. I re-ran only the mover bench and mutants, the retry search, the load gate and the flip gate.
- **No physical evidence.** Physical calibration was NOT RUN, and field or hardware skips are not hardware proof. No manager source bank runs at this head, and none is claimed.
- **The 8x8/2if margin exception (2.7 %)** is the ruled exception. It expires at the 8x8/2if flip, which waits on #890.
- **Tier rows stay red and belong to #894.** By every source, 1x1/1if R4 is 74.83 ms against 20.

## Pending manager duties

- **Hosted evidence.** Wait for the exact-head hosted contexts that were still running, and accept act/hosted evidence.
- **Merge candidate.** At the merge turn, build and validate the current-dev candidate (source base `e5f88a8e`, live dev `b7d69295`), including the builder and native banks.
- **Packet index.** Republish the packet's `receipts/INDEX.md` with the post-redaction hashes, or note that `MANIFEST.json` carries both. This is R711-8 S7 / R712-8 S6, per ruling item 6.
- **Residue.** Carry RES-1 (publish the round-30 PR body) and RES-2 to the residue checklist.

R711-9 FINISHED
