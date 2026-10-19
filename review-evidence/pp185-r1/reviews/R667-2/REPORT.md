[R667] POSITIVE - exact head 4865184c9ba88dd85aba3fc8036a6b74bcdb7073

# R667-2: independent round-2 review of processor PR #196 (Closes #185, #186)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #196, branch `185-186-control-unlock`
- Exact head `4865184c9ba88dd85aba3fc8036a6b74bcdb7073`, tree `2f850bcae69e2361992a32e5f91ac97e4a81f979` (verified in the review clone, `receipts/clone_restore_check.txt`)
- Round-2 delta: five commits on `b0f6f9c3` (`43a7987`, `4ba8c02`, `acc059a`, `7368215`, `4865184`); PR base `b48312e1`
- Reviewer role: internal independent reviewer, cleared context, own clone. No source edits, commits, pushes or GitHub writes.

## Verdict

POSITIVE. The round-2 delta resolves every prior finding at its cause, and I found no open BLOCKER, MAJOR or MINOR item. All five lenses are CLEAN.

- **One cause per LOCK_ENTITY notification (#186).** The rule holds in the author's LC0 to LC7 and in my own independent cycle-level sweep. The sweep has 22,828 runs. It injects the expiry, a LOCK and an UNLOCK at every clock offset over two rounds, and its engine model raises a one-cycle done strobe as `KL_aecp_engine` does. The same sweep fails 15,833 runs at base `b0f6f9c3`, which reproduces both round-1 defects.
- **The CONTROL overlay is limited to IDENTIFY (#185).** RDC0 to RDC7 pass, and the six `rdc-ctype-*` controls are KILLED.
- **Records and wording.** R667-1-F3 (total 125), R667-1-R1 and R668-1-F2 are applied.
- **No top-level change.** Round 2 changes no top-level port, parameter or register map.

I found one pre-existing defect outside this delta and record it as a SUGGESTION with a manager duty (S1): in the identify build, an IDENTIFY frame can be lost. The suggestions below do not affect the verdict.

## Reconstruction (order followed)

1. The repository has no tracked AGENTS.md or CONTRIBUTING.md. I read `docs/README.md` (conventions, single-source rules, registries).
2. Scope:
   - The bodies of issues #185 and #186.
   - The manager's assignment (issuecomment-6249574548).
   - The #186 correction (issuecomment-6253571045): both unlock notifications carry UNLOCK with locked_id 0.
   - The round-2 assignment (issuecomment-6264668094), read exactly.
   - The author's REVIEW READY at `4865184`.
   - This review's start (issuecomment-6273071258).
3. Authorities:
   - IEEE 1722.1-2021: §7.5.2, §7.4.2.1 with Table 7-143, §7.2.22, §7.3.6.2, Table 7-98 (IDENTIFY = 90-E0-F0-00-00-00-00-01).
   - Milan v1.2: Table 5.22 and §5.3.12.
   - In-tree contracts: 06 §6.1/§6.8/F06.14, 00 rows 15/16, 09 §8.4 and the Identify row, and `T-LOCK-UNLOCK`.
4. Diff and history:
   - `git diff b48312e1..4865184` (34 files).
   - The round-2 delta `b0f6f9c3..4865184` (22 files), read hunk by hunk.
   - `KL_aecp_notify.sv`: the lock expiry intake, the N_IDLE claim, N_EMIT_RD/WAIT/WB, the rgy face and the identify sequencer.
   - `gen_ucode.py`: E_RDESCCT, E_RDESCID, E_LOCKEN and E_LOCKUNS.
   - `KL_aecp_engine.sv`: the job load, `uns_done_o` and the rgy routing.
5. Public executable evidence: `kebag-logic/milan-fpga@992033a936efe4add5139167612f2b268be01134/review-evidence/pp185-r1/author-r2/`, checked against its `MANIFEST.json` (below).
6. Prior public findings (R667-1, R668-1). I read them only after my own pass over the diff was complete. I did not read any round-2 report from another reviewer.

## Executions at the exact head (this reviewer)

Pinned simulator 5.050 (identity checked: `--version` reports 5.050 rev v5.050). Runs were concurrent, with at most 16 jobs. All work was done in disposable copies under `scratch/`; the review clone was never built in.

| Run | Result | Receipt |
|---|---|---|
| Published evidence: every `author-r2/` file against `MANIFEST.json` published_sha256 | 1478 OK, 0 mismatch, 0 missing, 0 unlisted | `receipts/evidence_manifest_check.txt` |
| `tb/aecp_notify` suite (`make`, all builds and SC runs) | 131 checks: 131 PASS (author: 131) | `receipts/head_runs/notify_suite.log` |
| `tb/ucpu` suite | 447 checks: 447 PASS (author: 447) | `receipts/head_runs/ucpu_suite.log` |
| `tb/pp_top` suite, all seven builds | 10634 checks: 10634 PASS (author: 10634); default 10079, line 292, identify 178 and others 0 FAIL | `receipts/head_runs/pp_top_suite.summary.txt` |
| `notify_mutants.py --only` the ten new lock-cause controls, `--jobs 4` | golden PASS; 10 of 10 KILLED by their named LC checks | `receipts/head_runs/notify_lc_mutants.log`, `notify_lc_out/` |
| `aecp_dispatch_mutants.py --only` the six `rdc-ctype-*` arms, `--jobs 3` | 7 checks PASS (control plus 6 arms KILLED by RDC7) | `receipts/head_runs/dispatch_rdc_mutants.log`, `dispatch_rdc_out/` |
| Head `tb/aecp_notify` bench against base `b0f6f9c3`'s `KL_aecp_notify.sv` | 12 FAIL: LC1 ×6, LC2, LC3, LC4, LC5, LC6, LC7. This matches the PR's "twelve of these fail" | `receipts/lc_bench_at_base_rtl.log` |
| Own sweep probe, head RTL (S1 to S5) | 22828 runs: 22828 PASS | `receipts/sweep_head.summary.txt`, `receipts/sweep_head.classified.txt` |
| Own sweep probe, base `b0f6f9c3` RTL (S1 to S5) | 22828 runs: 15833 FAIL (rule A/C: LOCK flags with locked_id 0, UNLOCK flags with Y's id, lost automatic unlock) | `receipts/sweep_base.summary.txt`, `receipts/sweep_base.classified.txt`, `receipts/sweep_base.head120.txt` |
| Own S6 margin probe (engine tail after the holder read: 2 to 7 cycles) | head: tail 2 always loses the done strobe and tail 3 loses it twice; tails 4 to 7 are clean. Base: tail 2 always (its tails 3 to 7 fail rule A) | `receipts/sweep_head.classified.txt` |
| Own identify-build probe S7 (button press at every offset around a LOCK round) | 54 of 243 runs lose the IDENTIFY frame and repeat a LOCK frame. The count is the same at head, base `b0f6f9c3`, main `b48312e1` and main `08ae0013` (S1 below) | `receipts/sweep_{head,base,mainb48,main08}_idn.log` |
| `rdc-ctype-w88-nop` planted, `tb/ucpu` run | RC3 FAILS (446 PASS, 1 FAIL), so RC3 has a killing control | `receipts/ucpu_w88_probe.log` |
| `scripts/lint_hdl.sh`, `make check`, `gen_matrix.py --check`, `check_upc_map.py` (disposable clone at the head) | all rc 0; matrix 94 rows, 0 untested; UPC map 92 entry points | `receipts/gate_*.log` |
| Review clone after the work | HEAD and index tree equal the head tree; 0 porcelain lines (ignored files included); 0 gitlinks (this repository has none); 646 mode-100644 and 17 mode-100755 entries | `receipts/clone_restore_check.txt` |

About the sweep probe (`scripts/probe_sweep/`):

- It is portable. `build.sh TREE OUT SIM [args]` builds it against any tree's `KL_aecp_notify.sv`, with N_CTRL_P=4 so that four controllers fit. `-CFLAGS -DIDENT` with `-GEN_IDENTIFY_NOTIF_P=1` selects S7, and `-DNO_FLAGS` builds against pre-#186 main.
- Its first draft had two artifacts of my own model, which I corrected before taking the numbers above:
  - it issued a new rgy request in the cycle after dropping the previous one;
  - it used a 3-cycle engine tail, below E_LOCKUNS's eight µops after the read.
- Checks per run:
  - A: every frame is the (flags, locked_id) pair of one cause.
  - B: no frame carries a change to that change's own requester.
  - C: every registered controller's last frame is the final state. The final change's requester is exempt, and after a final expiry every controller, the former owner included, must last see (UNLOCK, 0).
  - D: every done strobe lands while its job is presented.
  - E: the holder read is answered within 3 cycles.
  - F: each destination's sequence_id advances by exactly 1.
- Scenarios:
  - S1: the expiry at offsets 0 to 140 after X's LOCK, with words 0 and 0x00010000, C, X and D registered, and four engine timings.
  - S2: Y's LOCK at offsets 0 to 120 after X's UNLOCK, with the UNLOCK at three positions.
  - S3: X's UNLOCK at offsets 0 to 120 during its LOCK round.
  - S4: an expiry at k1 by Y's LOCK at k2 (61 × 81 offsets).
  - S5: an expiry at k1 by X's re-lock at k2.

## Focus checks

1. **One cause per LOCK_ENTITY notification (IEEE 1722.1-2021 §7.5.2, §7.4.2.1, Table 7-143; Milan v1.2 Table 5.22).**
   - The mechanism is in `KL_aecp_notify` alone (`hdl/aecp/KL_aecp_notify.sv:957-969`, `:1420-1450`, `:1478-1529`, `:1540-1543`):
     - the expiry is owed (`lk_exp_r`);
     - it is deferred while a LOCK job is presented and in the N_IDLE cycle that takes a state query;
     - the claim waits a cycle when the expiry applies in an idle cycle;
     - an expiry, a take or a release during a lock round re-latches `em_arg1/0` and the exclusion, and pends the next round;
     - ops decide on `lk_on_w`.
   - I traced every path in which the arguments loaded with a job could disagree with the holder read. The engine loads in N_EMIT_WAIT, which is deferred. The read is withdrawn N_EMIT_WAIT → N_IDLE with `rgy_new_w && rgy_state_i`, which is deferred. The answer is in N_ANS, and the expiry applied at its edge does not change the sampled word. No solicited op can come between a load and its read, because the engine is single-threaded.
   - The assignment's specific cases:
     - The expiry one clock before, on and after the claim, with words 0 and nonzero and the former owner registered: LC1, and S1 at every offset.
     - The third path, an expiry between a job load and its holder read and in the read cycle: LC2, LC3, and S1/S4 with gaps of 1 to 3 cycles.
     - A LOCK by another controller during an UNLOCK round: LC4, LC5 and S2. No job carries UNLOCK once the holder is non-zero.
   - No timeout notification is lost: rule C holds for all 22,828 runs. The exclusion is correct (rule B; LC5 and S2 with Y registered).
   - The command-word echo and #181's queue are kept: LF, LN0-4, L5b, L6d, CQ and OC1 all pass.
   - Every new LC check has a KILLED control. LC0 is covered by `lock_take_keeps_old_flags` in the author's full-campaign record (`compare/failsets-notify-base-vs-head.txt`).
2. **IDENTIFY-only overlay (IEEE 1722.1-2021 §7.2.22, §7.3.6.2, Table 7-98; Milan v1.2 §5.3.12).**
   - `E_RDESCID` (`hdl/aecp/ucode/gen_ucode.py:1351-1378`) reads lane 80..87 into r5 and compares @82, @84 and @86 (r5 >> 32, >> 16, and the low word against r12 = 0). It compares @88 from r4, which is lane 88..95 and still unshifted from E_RDESCCT+8. `CHECK_ARG` on a mismatch goes to `SET_STATUS OK` and then `E_RDESC`. The words 90E0, F000, 0000 and 0001 match Table 7-98.
   - A non-IDENTIFY one-octet linear CONTROL is served whole (RDC7: a vendor type and one type off in each word; RC3).
   - RDC0 to RDC6 pass. Every `rdc-ctype-*` arm is KILLED.
   - No top-level wiring (`identify_index_i` is unused, as the assignment allows).
3. **R667-1-F3 and the RESIDUE items.** `tb/pp_top/README.md:2866-2872` states 125 = 98 + 11 + 16 at the merge, and `:2881` states 135; `notify_mutants.py` has 135 `Mutant(` entries. R667-1-R1: 06 §6.8 (`docs/architecture/06_aecp_engine.md:814`) and 00 row 16 say "on `T-LOCK-UNLOCK` expiry", and no "one-minute" remains in 06. R668-1-F2: no bench label is left in any comment line the whole PR adds to `tb/pp_top`, `tb/ucpu` or `tb/aecp_notify` sources (scan of `b48312e1..4865184`).
4. **No top-level port, parameter or register-map change.**
   - Round 2 touches nothing under `hdl/top`, `hdl/common`, `KL_aecp_engine.sv`, 01, 02 or 07.
   - The `KL_aecp_notify` port and parameter lines are identical at `b0f6f9c3` and the head.
   - Over the whole PR, `protocol_processor_top.sv`'s input/output and parameter lines hash identical at `b48312e1` and the head. The only change there is round 1's internal `aecp_rgy_flags_w`.
   - Parent gate 11 is rc 1 byte-identical at base and head in the author's receipts (`parent-base/` vs `parent-head/g11_lint_rtl.log`, compared here), from #190's `cfg_tspec_max_frame_i`. As scoped, it is not this delta.

## Prior findings at this head

| ID | Severity (prior) | Status at `4865184` | Evidence |
|---|---|---|---|
| R668-1-F1 | MAJOR | RESOLVED: a claim never meets an expiry; the round carries UNLOCK/0 and the automatic unlock is not lost | LC1 (killed by `lock_claim_beside_expiry`); sweep S1 at every offset; fails at base |
| R667-1-F1 | MINOR | RESOLVED: a lock change re-latches the running round | LC4, LC5, LC6 (three controls KILLED); sweep S2/S3; the author's mid-round probe rc 0 at the head (`author-r2/receipts/round2/probes-head/`) |
| R667-1-F2 | MINOR | RESOLVED: E_RDESCID tests `control_type` | RDC7, RC3; 6 arms KILLED; the author's vendor probe rc 0 at the head |
| R667-1-F3 | MINOR | RESOLVED | `tb/pp_top/README.md:2866-2872` |
| R667-1-R1 | RESIDUE | APPLIED | 06 `:814`, 00 row 16 |
| R668-1-F2 | RESIDUE | APPLIED | comment scan (focus check 3) |
| R667-1-S1 to S5 | SUGGESTION | Not assigned; retained as suggestions. S4's stale "the µISA has no shift" comments are still at `gen_ucode.py:357`, `:724`, `:829` and `:967`, beside E_RDESCID's three new `SHIFT_R`s | grep at the head |

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE items. Suggestions follow; they do not affect the verdict.

### S1. SUGGESTION (pre-existing, outside the delta): in the identify build, an IDENTIFY frame can be lost when the button press lands just after a LOCK job's holder read

- **Lenses:** Robustness, RTL. Not attributable to this delta.
- **Where:** `hdl/aecp/KL_aecp_notify.sv:1098-1100`. `own_r` takes the face whenever `n_st_r != N_EMIT_WAIT`. During a taken LOCK job's holder read, the registry machine is in N_IDLE/N_ANS/N_EMIT_RD for about 3 cycles while the engine still runs E_LOCKUNS.
- **Evidence:**
  - Probe S7 (`P-EN-IDENTIFY-NOTIFICATION = 1`, `receipts/sweep_head_idn.log`) gives 54 of 243 press offsets with these effects:
    - E_LOCKUNS's done retires the identify job (`done_w`), so no IDENTIFY frame is built;
    - the LOCK job is presented again and its frame is repeated with the same sequence_id.
  - The count is identical at base `b0f6f9c3`, main `b48312e1` and main `08ae0013` (`receipts/sweep_{base,mainb48,main08}_idn.log`). On the two main commits, the S7 runs also fail rules A/C, because those heads predate #186's flags. The lost-frame count is the measure that compares. The defect predates #185/#186.
  - It contradicts the existing comment at `:1098-1099` ("a job the engine may already hold is never replaced under it"). It also qualifies the round-2 banner sentence at `:181-183` ("a job the engine has taken is retired by its done in that re-presentation"), which holds for the registry path.
- **Impact:** A lost IDENTIFY_NOTIFICATION burst frame and one duplicate LOCK_ENTITY frame, in a narrow press window.
- **Suggested outcome:** A separate processor issue. For example, hand the face to the identify sequencer only when the registry machine holds no taken job; a "taken" flag would be set at the load and cleared by `core_done_w`. Add an identify-build regression. The S7 probe is a template.
- **Verification:** S7 with 0 lost frames.

### S2. SUGGESTION: record the done-strobe margin the re-presentation relies on

- **Lenses:** Robustness, Docs.
- **Where:**
  - `hdl/aecp/KL_aecp_notify.sv:1540-1543` (the claim's one-cycle wait);
  - `:1749-1761` (`core_done_w` is honoured only in N_EMIT_WAIT);
  - `hdl/aecp/KL_aecp_engine.sv:2679` (`uns_done_o` is a one-cycle strobe).
- **Evidence:** In probe S6, a job taken before its holder read must be re-presented before the engine's done strobe:
  - base needs at least 3 cycles after the answer;
  - the head needs at least 4 when an expiry applies in that N_IDLE cycle.
  - E_LOCKUNS has eight µops after the read, plus the TX wait, so the real margin holds, and every suite passes.
- **Suggested outcome:** State the bound in 06 §6.8 (or the banner at `:176-185`), or add a simulation assertion that `uns_done_i` only arrives in N_EMIT_WAIT or while `own_r` is set.

### S3. SUGGESTION: record RC3's control

- **Lenses:** Tests, Docs.
- **Where:** `tb/ucpu` RC3 and `tb/ucpu/README.md`.
- **Evidence:** No campaign grades RC3. Planting `rdc-ctype-w88-nop` fails it (`receipts/ucpu_w88_probe.log`).
- **Suggested outcome:** A line in the `tb/ucpu` README naming that control.

### S4. SUGGESTION: review labels in new README record lines

- **Lenses:** Docs.
- **Where:**
  - `tb/pp_top/README.md:1322-1323`, `:1396` ("the program before round 2, the R667-1 F2 reproduction"), `:1470`, `:2881`, `:2888`, `:3006`, `:3012`;
  - `tb/aecp_notify/README.md:434` and `:519`.
- **Why:** These are suite record prose, not source comments, and the README already uses the idiom (for example `:2855` and `:3020` "review R420-1 S1"). So this is not a violation of the comment rule. A neutral wording ages better, for example "the program before the `control_type` test (issue #185)" in place of "the program before round 2, the R667-1 F2 reproduction".

## Lens notes (artifact-specific)

- **Conformance:** The rule of the #186 correction and the round-2 assignment is met: a LOCK echoes its word with its holder, and an UNLOCK or the automatic unlock carries UNLOCK (or the UNLOCK's word) with 0. Table 7-98's IDENTIFY test is exact over all four words. Every other CONTROL is served from its image (§7.2.22, §7.3.6.2). Artifacts: `KL_aecp_notify.sv`, E_RDESCID, E_LOCKUNS, LC/RDC7/RC3 and the sweep.
- **RTL:**
  - The delta is limited to `KL_aecp_notify.sv` and `gen_ucode.py`, with no port change.
  - `lk_exp_r` resets to 0. It is set only while the lock is held, and cleared when it applies. `lk_on_w` keeps `lk_denied_w` and `lk_is_holder_w` consistent in the expiry cycle.
  - The re-latch is guarded by `em_active_r && em_kind_r == PP_UNS_LOCK_C`.
  - The ROM placement (656, in the free 653..671 run) is asserted, and the UPC map gate passes with 92 entry points.
  - lint_hdl is rc 0.
- **Robustness:** The deferral is bounded by one presented job. `amap_busy_o` makes the job outrank commands, so the engine takes it promptly. A command in that window sees the lock held, as 06 `:843-845` documents. Coalescing keeps the final state (sweep C). Two items fall outside the delta or are margin notes: S1 is pre-existing, and S2 is a margin note.
- **Tests:**
  - LC0 to LC7 grade @24..@35, the destination and sequence_id byte-exact, and 12 of them fail on base RTL.
  - All ten lock-cause controls and all six `rdc-ctype-*` arms are KILLED in my runs.
  - The author's full campaigns record 135 of 135 and 73 of 73 at the head (`head-final2/campaigns/notify.log`, `compare/`).
  - The three suites that build changed files pass here with counts identical to the author's.
- **Docs:**
  - 06 §6.1, the new "One cause per notification" paragraph in §6.8, F06.14's answer rows, 00 rows 15/16, the Identify row and §8.4 of 09 ("eleven", with the LC row added) and the READMEs agree with the code and with my runs. `make check` is rc 0.
  - The PR body's round-2 section matches the commits and receipts. Its "twelve of these fail at b0f6f9c3" was reproduced.
  - Comment-rule scan of the delta's source comment lines (`hdl/`, `tb/` sources, scripts): no lane label, lane name, review round, reviewer ID or issue-comment ID. "round" there means a notification round and "lane" a memory lane.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issues #185/#186, the assignment, the #186 correction, the round-2 assignment; IEEE 1722.1-2021 §7.5.2, §7.4.2.1/Table 7-143, §7.2.22, §7.3.6.2, Table 7-98; Milan v1.2 Table 5.22, §5.3.12; `KL_aecp_notify.sv` lock paths; E_RDESCID/E_RDESCCT/E_LOCKUNS; LC, RDC7, RC3; sweep S1-S5 | R667-2 | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |
| RTL | CLEAN | `KL_aecp_notify.sv` (expiry intake, claim, EMIT states, rgy face, identify hand-off), `gen_ucode.py`, `KL_aecp_engine.sv` (job load, done strobe); port and parameter hashes; lint_hdl; UPC map | R667-2 | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |
| Robustness | CLEAN (S1 is pre-existing and outside the delta; S2 is a margin note) | sweep S1-S6 at head and base; identify probe S7 at head, base and two main commits; deferral bound; coalescing; exclusion | R667-2 | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |
| Tests | CLEAN | `tb/aecp_notify` (131), `tb/ucpu` (447), `tb/pp_top` (10634) run here; 10 lock-cause and 6 rdc-ctype controls run here, all KILLED; LC bench on base RTL (12 FAIL); RC3 control probe; author campaign receipts at the head | R667-2 | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |
| Docs | CLEAN (S3, S4 suggestions) | 06 §6.1/§6.8/F06.14/answers, 00 rows 15/16, 09, the `tb/pp_top`, `tb/aecp_notify` and `tb/ucpu` READMEs, PR body round-2 section; `make check`, `gen_matrix --check`; comment-rule scan | R667-2 | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |

## Real limits

- I did not run the full processor suite bank (`run_suites.sh`), Yosys, elab-guard or the other campaigns, and I did not run parent consumer gates. For those I relied on the author's published receipts at `4865184`, which I checked against their manifest and spot-read: `run_suites` 1,030,205 checks rc 0; notify 135 of 135; parent gates 16 of 17 rc 0, with gate 11 rc 1 byte-identical at base; the parent gitlink pinned at `4865184`; the #180 and #176 parent patches applied.
- My notify campaign run covered only the ten new lock-cause controls, and my dispatch campaign run only the six new arms.
- The sweep is a unit-level probe of `KL_aecp_notify` with an engine model. It is not a `tb/pp_top`-level end-to-end run. The engine model's timings (load-to-read gap 1 to 3 cycles, tail at least 8) are my approximation of E_LOCKUNS. Only the S6 margin runs use shorter tails.
- Two sweep logs exceed 200 KB and are not published. They are listed by hash in `receipts/OVER-200KB.sha256`, and their summaries and classifications are published.
- Local paths in the receipts are redacted to `<home>`, `<packet>`, `<clone>`, `<pinned-sim>` and `<sim-install>`.
- Standards text: clause references follow the in-tree transcriptions and the issue statements. I consulted no separate licensed standards PDF.
- There is no manager source bank at this exact head, and I claim none. Hosted checks at the head, read-only at review time: docs-gates and portability completed with success; suites were in progress. The manager owns hosted and act acceptance.
- Physical calibration NOT RUN. No hardware or field qualification is implied.

## Pending manager duties

- Hosted/act acceptance at this head. The suites job was still in progress when I looked.
- At the merge turn, build and validate the current-dev merge candidate (source base `b48312e1`, live dev `e26f1816e456dc8027924bc2e5d327a8aa6e46db`) with the builder and native banks, adopt the #190 parent patch that clears gate 11, and link the receipts on the PR.
- Open a processor issue for S1, the pre-existing lost IDENTIFY frame in the identify build. Optionally route S2 to S4 and the retained R667-1 S1 to S5.
- The merge needs a second independent positive review at this head.

R667-2 FINISHED
