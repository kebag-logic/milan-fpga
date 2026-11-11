[R806] POSITIVE - exact head 2905c8749a4573450b9999dd546bb20ae5c7fc38

# R806-6: external independent delta review of #823 (format only) / PR #880

- **Head:** `2905c8749a4573450b9999dd546bb20ae5c7fc38`, tree `c28f687748dec7d97d4346844d5bfce183aa010d`, `823-format` -> `dev-soft-core`.
- **Merge base:** `dev-soft-core` `1d6bf555` (PR #861's merge, a descendant of the stated source base `a9d69c77`). `a9d69c77..1d6bf555` is PR #861, already on `dev-soft-core`. It is not this PR's change and was not re-judged.
- **Delta judged:** `30ca4b21..2905c874`. That is round 4's head, which R806-4 reviewed, plus seven commits: `249cca50`, `8e29bc74`, `64c3565e`, `4d0353e3`, `0d9e9b50`, `e0adcc09` and `2905c874`. It touches 21 files, +215/-80 (`receipts/delta_scope.txt`). Code outside the delta keeps R806-4's lens verdicts at `30ca4b21`, except where the delta changes something it depends on.
- **Authorities read:** AGENTS.md; the #823 body and amendment; the owner's 0.5 s save bound; the round 1 assignment and the round 5 ruling (issuecomment-6754858510); the round 6 split ruling (PR #863 issuecomment-6767385787) and its #823 note (issuecomment-6767387406); #876's acceptance; the author's TAKEN and REVIEW READY (issuecomment-6767475589, -6778926856); the PR #880 body; my own R806-4 (PR #863 issuecomment-6754770706) and R806-5 (issuecomment-6767224297). I read no other reviewer's report at this head.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open. I record two RESIDUE items and two SUGGESTIONs below. None of them leaves a lens unclean.

Summary of the four questions:

1. **Scope is the format only, as the split ruling defines it.**
   - The branch is `30ca4b21` plus seven commits. They are items 2 to 5 of the round 5 ruling, RS-d and R806-5 R2.
   - No save-path code is present:
     - no compaction, suspend or append symbol is in `sw/firmware/ctrl_nvm/*.[ch]`;
     - the RV32 section sizes of the store equal round 4's at all five shapes (`receipts/rv32_sizes_vs_r4.txt`).
   - No HDL, gitlink or `configs/generated` path changes against `1d6bf555`, and the six gitlinks are identical (`receipts/delta_scope.txt`).
   - The format page (`:6`, `:240-242`, `:332`, `:472-474`, T7-T13/T15, decisions 3-5 and 7) and the PR body (`Description`, `Known limitations`) say section 4 is designed here and built under #876.
   - #876's body carries R806-5 F1, F2 and F4, and its memory-ledger item 5 covers F3.
2. **Every R806-4 and R806-5 finding** is resolved at this head, or is correctly outside the round (table below).
3. **The format's tests and plants are green at this head, and the new plants can fail:**
   - store gate 132/132;
   - drift gate self-test, with six line-citation plants that the old pattern misses five of;
   - reference gate 6/6;
   - gate 39 10/10.
4. **Hosted CI at the exact head:**
   - 68 of 68 executed jobs succeeded, with 1,063 steps succeeded and 0 failed;
   - the 283 skipped steps are all cache, tool-install or cancel conditionals;
   - the one skipped context is `Physical gPTP (nightly and manual)`, which is not a PR job.

   No manager candidate bank receipt is published on PR #880 yet (3 comments, none of them a bank). That is a pending manager duty, not something I claim.

## Findings

### RS-1 — RESIDUE — Docs — `scripts/nvm_format_32x32_tables.py:427` — lane label in a source docstring this PR added

- **Evidence:** `"""Section 3: the ppmem window and the F1 stage."""`. "F1" is #665's lane label.
  - The line is added by this PR against `dev-soft-core`, so it is not one of the existing instances #746 tracks.
  - R806-4 RS-a asked for the same wording in "the other instances". The author replaced "F1 store" in every comment it listed, but not this docstring.
  - The `Anchor("F1 codec"/"F1 store"/...)` labels and the T-row strings in the same file are generated page text, not comments, so they are not residue.
- **Exact fix:** `"""Section 3: the ppmem window and the split store's stage."""`.
- **Optional, same wording:** the runtime message `sw/builder/endstation_builder.py:2812` "the F1 store would refuse this shape" is not a comment and is not required.

### RS-2 — RESIDUE — Tests (wording), Docs — `sw/firmware/ctrl_nvm/test/nvm_bench.py:114` — `Bench` docstring names the wrong reference

- **Evidence:** `"""One shape's reference side: its frames and how nvm_klj2.py packs them."""`.
  - The frames are packed by `scripts/nvm_klj3.py` (`frame_record3`, `REC_HDR3`, `expected3`, imported at `nvm_bench.py:40`).
  - Only `payload_bytes` still comes from `nvm_klj2` (`:39`).
  - The PR re-wrapped this line (it was `1d6bf555:...nvm_bench.py:101`).
  - The author disclosed it in REVIEW READY as found and not changed, because it is outside the ruled lists.
- **Exact fix:** "One shape's reference side: its frames and how scripts/nvm_klj3.py packs them."

### S-1 — SUGGESTION — Tests — `scripts/check_nvm_format_32x32.py:15,58` (`LINE_CITE_RE`)

- `receipts/linecite_probe.txt` (`scripts/linecite_probe.py`) runs the gate's own `findings()` on the real page plus one planted sentence per form.
- **Caught:** every form R806-4 S-a listed, plus a spaced list, "`path` lines N-M" and a `#L-L` range.
- **Still accepted:**
  - an unquoted "path line 179";
  - "line 179 of `path`";
  - "`path`, line 179";
  - "`path:L179`";
  - "`path` (line 179)".
- The page carries none of these today (0 matches).
- The docstring says "in any form:" and then lists the forms, so the claim is bounded by its list. The PR body says "no line number in any form" with the same list.
- **Suggestion:** either widen the pattern to those forms, or say "in these forms" in the docstring and the PR body.

### S-2 — SUGGESTION — Docs — `sw/litex/milan_soc.py:166` — the `user` slot comment predates the new ownership text

- The comment says `user` holds "raw bare-metal records: entity/group names, channel maps, mixer state, and the rotating compressed CTF fault log".
- FASTCONNECT section 5 says "no current product owner", and QSPI_FLASHBOOT (as N2 rewrote it) says "`user` has no owner today".
- The comment is unchanged since `1d6bf555:161` and outside this delta. Carry it to the residue checklist (#495/#746).

## Ruling items and prior findings, at their cause

| Item | At `2905c874` | Evidence |
|---|---|---|
| R806-4 **N1** MINOR (`SPLIT_CONTROL_MEMORY.md:144`) | **RESOLVED** | `:144` reads "3,344 against 13,264 bytes" again. That equals `a9d69c77:docs/design/SPLIT_CONTROL_MEMORY.md:144`, and `c20ed894` is a commit in the tree that predates KLJ3. `:146-147` say the run printed KLJ2 sizes and point to section 5, whose `:176` gives both formats (3,344 / 13,264 B KLJ2; 3,454 / 13,594 B KLJ3). The KLJ3 figures match the stage this run printed at 1x1 and 8x8 two-interface (`receipts/store_selftest.log`: `stage=3454`, `stage=13594`) |
| R806-4 **N2** MINOR (`QSPI_FLASHBOOT.md:58-66`) | **RESOLVED** | `:58-69` names each reserved range's owner and links FASTCONNECT section 5. `journal_klj3` is written only by the split store. `journal` belongs to the all-fabric writer, and the split store reads its two headers and never writes it. `user` has no owner. This matches FASTCONNECT section 5's table and prose (`SAVED_STATE_FASTCONNECT.md`, section 5 table rows and the `journal_klj3` paragraph). The "nothing writes or reads them" and blank-flash sentences are gone |
| R806-4 **RS-a** RESIDUE | **RESOLVED**, one instance left as RS-1 | `nvm_klj2.c:3`, `nvm_klj2.h:4` and `nvm_shape.h:4` read "(#665, the split placement's saved-state store)". The same wording is in `nvm_layout3.h`, `nvm_layout3.py`, `nvm_klj3.py`, `check_nvm_klj3.py`, `endstation_builder.py` and `test_builder.py`. "F1 store" now appears only in generated page labels and one runtime message (`git grep`, above) |
| R806-4 **RS-b** RESIDUE | **RESOLVED** | `test_nvm_write.cpp:15,67,75,83,98,667` name `nvm_klj3.py`. `nvm_rig.cpp:179` and `test_nvm_boot.cpp:12` are kept, as ruled; both statements are true (`nvm_klj2.payload_bytes`; the all-fabric KLJ2 container) |
| R806-4 **RS-c** RESIDUE | **Outside the round**, carried to #495 as ruled | Recorded in the PR body, Known limitations |
| R806-4 **S-a** SUGGESTION | **ADOPTED** | Six plants, one per form, each caught by a finding that names the whole citation (`receipts/drift_selftest.log:8-13`). Against the old single-form pattern, five of the six plants are missed (`receipts/linecite_probe.txt`), so they can fail. Residual forms: S-1 |
| R806-4 **S-b** SUGGESTION | **ADOPTED** | `at width: MILAN_NVM3_MAPIN_ENTRIES_0 = 255, its table's limit, compiles`. Control `mapin_limit_one_early` (`>= 255u`) is caught. `doctor` refuses a constant that is absent or defined twice (`nvm_bench.py:196-202`), so the 255 edit cannot be skipped silently |
| R806-4 **S-c** SUGGESTION | **ADOPTED** | `nvm_shape.h:180-182` `#error`, after `nvm_shape_gen.h` is included (`:35`). Only `nvm_bench.py:157` defines `NVM_HOST_TEST`, under `build_suite`'s `host_test=True` (`:212`). No target header defines it (`git grep`). `doctored_outside` requires the refusal in its words, and control `doctored_error_removed` is caught |
| R806-5 **F1, F2, F3** MAJOR (append path) | **Outside the round** (split ruling items 1-2) | The append path is not on this branch (scope, above). #876's acceptance carries F1 (power-cut campaign), F2 (cadence) and the memory ledger (F3) |
| R806-5 **F4** MINOR (page worst case vs the model) | **Outside the round**, moved with #876 | The model it compares against (`save_bound`) is not on this branch. The page's section 4 is labelled as the design built under #876, and #876 item 4 names "R806-5 F2, both F4" |
| R806-5 **R1** RESIDUE (= RS-d) | **RESOLVED** | `nvm_rig.hpp:18` and `nvm_suite.hpp:9` name `scripts/nvm_klj3.py` |
| R806-5 **R2** RESIDUE | **RESOLVED** | Page `:330`: "The room, taken from the all-fabric worst case (404.71 ms) and so conservative for the split, is 95.29 ms". Both figures are inline and drift-gated (gate: 0 findings). The PR body (Description table, R806-5 R2 row) uses the same wording, and the old "leaves 95.29 ms" sentence is absent |
| R806-5 **S1** SUGGESTION | Outside the round (append path) | |
| Round 5 ruling **RS5, RS6** | **RESOLVED** | FASTCONNECT contents entry ("three reserved slots, `journal_klj3`, `journal` and `user`") and status row (`journal_klj3` at `0xE4_0000`, 640 KiB) |
| Split ruling **#818 waiver** | **MET as ruled** | No HDL, gitlink or `configs/generated` change against `1d6bf555`. The author's AX7101 generated-RTL comparison is in the receipts and verified against the manifest; its normalised Verilog digest is equal at base and head (`waiver/elab/normalised.sha256`). Page `:472-474` cites the memory plan, 57.5 RAMB36 |
| **Comment rule**, round 6 delta | No new instance | Every added line of `30ca4b21..2905c874` was scanned for lane, round, reviewer and comment-ID tokens. The only hit is in the format page, a design page, which links the ruling's issuecomment. Source comments add only `(#823)` |

## Lens results (each clean result carries its artifact)

```text
[R806] PASS Conformance — split ruling PR #863 issuecomment-6767385787 item 1 vs `git log 30ca4b21..2905c874`, receipts/delta_scope.txt, SAVED_STATE_FORMAT_32X32.md:6,240-242,330-332,472-474,512-520,534-538, PR #880 body — base 30ca4b21 plus seven commits; items 2-5, RS-d and R2 present; no save path; section 4 labelled designed here and built under #876; waiver diff empty; "Closes #823"
[R806] PASS RTL — receipts/delta_scope.txt (no .sv/.svh/.v/.vh/.vhd, hdl, syn, submodule or configs/generated path vs 1d6bf555; six gitlinks identical); nvm_shape.h:35,180-188 — the #error sits after the generated header and leaves NVM_MAPI_WIDE/NVM_MAPO_WIDE unchanged; 255 input entries compile and 256 are refused; RV32 sizes identical to round 4 (receipts/rv32_sizes_vs_r4.txt)
[R806] PASS Robustness — nvm_shape.h:180-182, nvm_bench.py:147-157,196-202,212, test_ctrl_nvm.py:111-122,206-235,358-385 — the doctored seam compiles only under the host header; the target path cannot define NVM_HOST_TEST (git grep); doctor refuses a missing constant; the boundary entry at 255 is pinned, with its off-by-one control
[R806] PASS Tests — receipts/store_selftest.log (rc 0, 5 shapes, 506 tests, 132/132 incl. the two new controls), receipts/drift_gate.log + drift_selftest.log (0 findings; six line-number plants; moved-lines control 0), receipts/linecite_probe.txt (old pattern misses 5 of 6 new plants), receipts/klj3_selftest.log (6/6), receipts/builder_g39.log (gate 39 10/10, gate 38 9/9), receipts/fw_coverage.log (PASS), receipts/hosted_job_steps.tsv (68 jobs, 0 failed steps)
[R806] PASS Docs — SPLIT_CONTROL_MEMORY.md:140-147,176; QSPI_FLASHBOOT.md:56-69 vs SAVED_STATE_FASTCONNECT.md section 5; FASTCONNECT contents entry and status row; format page R2 sentence and #876 labels; ctrl_nvm/README.md:451-457,556-559; PR #880 body — N1, N2, RS5, RS6 and R2 fixed truthfully; RS-1 and RS-2 are wording-only residue
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The split ruling and round 5 ruling items vs the delta; the format page's #876 labelling; the PR body; the waiver diff; #876's carried findings | R806-6 | `2905c8749a4573450b9999dd546bb20ae5c7fc38` |
| RTL | CLEAN | No HDL, gitlink or generated RTL vs `1d6bf555`; `nvm_shape.h` compile-time rules; RV32 sizes vs round 4 | R806-6 | `2905c8749a4573450b9999dd546bb20ae5c7fc38` |
| Robustness | CLEAN | The doctored-build seam, the 255-entry boundary, `doctor`'s refusal, `NVM_HOST_TEST` reachability | R806-6 | `2905c8749a4573450b9999dd546bb20ae5c7fc38` |
| Tests | CLEAN | Store gate 132/132; drift gate and self-test; line-citation probe; reference gate; gates 38/39; coverage; hosted job steps | R806-6 | `2905c8749a4573450b9999dd546bb20ae5c7fc38` |
| Docs | CLEAN (RS-1, RS-2 residue) | SPLIT_CONTROL_MEMORY, QSPI_FLASHBOOT, FASTCONNECT sections 1 and 5, the format page, the store README, the PR body | R806-6 | `2905c8749a4573450b9999dd546bb20ae5c7fc38` |

## What I ran (exact head, this clone; receipts listed in MANIFEST.sha256)

| Command | Result | Receipt |
|---|---|---|
| `test_ctrl_nvm.py --require-rv32 --self-test --jobs 10` (RV32: Buildroot riscv32-linux-gcc 14.3.0) | rc 0, `OK across 5 shape(s), 506 tests, and all 132 planted defects reddened`; at-width and doctored-outside lines printed; both new controls caught | `receipts/store_selftest.log` |
| RV32 sizes vs the author's round 4 receipt at `30ca4b21` | identical at 5 shapes | `receipts/rv32_sizes_vs_r4.txt` |
| `check_nvm_format_32x32.py` / `--self-test` | rc 0, 0 findings / `self-test: PASS`, six line plants caught, `control moved-lines: 0 finding(s)` | `receipts/drift_gate.log`, `receipts/drift_selftest.log` |
| `scripts/linecite_probe.py` (gate's own `findings()`, 14 forms; old pattern vs the six plants) | 9 caught, 5 rarer forms missed (S-1); old pattern misses 5 of 6 plants | `receipts/linecite_probe.txt` |
| `check_nvm_klj3.py --self-test` | rc 0, 6/6 plants | `receipts/klj3_selftest.log` |
| `nvm_layout3.py`; `flash_map.py` | rc 0; NAME 222..1128 of 1129; `journal_klj3` at `0x0E40000`, 640 KiB | `receipts/layout3.log`, `receipts/flash_map.log` |
| `test_builder.py --gates` (gates 38, 39) | rc 0, 9/9 and 10/10 plants | `receipts/builder_g39.log` |
| `fw_coverage.py --check` | rc 0, PASS (35 files) | `receipts/fw_coverage.log` |
| HDL/gitlink/generated diff vs `1d6bf555`; gitlinks | empty; 6 gitlinks identical | `receipts/hdl_diff.log`, `receipts/delta_scope.txt` |
| Hosted check runs and every job step at the head (read-only API) | 68 success + 1 nightly context skipped; 1,063 steps success, 283 skipped (cache, install or cancel conditionals only), 0 failed | `receipts/hosted_check_runs.tsv`, `receipts/hosted_workflow_runs.tsv`, `receipts/hosted_job_steps.tsv` |
| Author round 6 packet (`12ebd8b9`, `review-evidence/823-r1/author-r6`) vs its `MANIFEST.json` | 650 listed, 650 match, 0 unlisted. The packet commit carries no cryptographic signature (`%G?` = N); its integrity is the manifest's digests | `receipts/evidence_manifest_r6.txt` |
| Restore check | worktree and index equal HEAD, blobs rehash equal, index tree `c28f6877`, 0 untracked or ignored, 6 gitlinks as recorded | `receipts/restore_check.txt` |

## Real limits

- **No full banks.** I did not run the parent sweep, Yosys or the builder bank. For the source head I rely on the author's published receipts (manifest-verified) and on hosted CI at the exact head. I claim no manager source bank.
- **Generated SoC RTL.** Only the AX7101 shipping SoC was compared, by the author. The Arty launch line fails in that LiteX environment, and the split SoC (`--ctrl-mailbox`) is not compared. Its effect is the KLJ3 stage and the `MILAN_NVM3_*` constants, which the ruling covers through the memory plan's 57.5 RAMB36.
- **Target hardware.** The target platform's split image was not linked again this round, and the split target harness's recorded results predate KLJ3 (PR body). Physical calibration NOT RUN; field skips are not hardware proof.
- **Hosted acceptance is the manager's.** I read the hosted runs and did not judge act or protection settings.
- **Where I re-ran.** I re-ran the author's store gate on a host with load average 60 to 80. It passed, and I did not repeat it under lower load.

## Pending manager duties

- Build and validate the current-`dev-soft-core` merge candidate (builder and native banks), and link its receipts on PR #880. `dev-soft-core` has moved to `764482b4` (PR #874) past the merge base `1d6bf555`. The candidate must include that move.
- Carry RS-1, RS-2, S-2 and R806-4 RS-c to the residue checklist (#495/#746), and decide whether to adopt S-1.
- After merge, run post-merge containment and close #823 through `Closes #823`.

R806-6 FINISHED
