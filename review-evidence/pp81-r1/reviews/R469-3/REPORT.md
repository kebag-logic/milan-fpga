[R469] POSITIVE - exact head f9b8f0ee6604a73b9fa82c62b91811e9f53b320a

# R469-3: external independent review of issue #81 / #84, PR #157

- Exact head `f9b8f0ee6604a73b9fa82c62b91811e9f53b320a`, tree `0e4e1c96a8bbd9fd7812dc0c1c84697a9adb6242`.
- Source base `83999eba1ef4756e9e769e4fba164f5095761604`. The head merges processor `main` `07b1469d` (PR #154) into the lane head `1d6c78f1`.
- The review ran in a cleared context in a detached clone that was never edited.
- No open BLOCKER, MAJOR or MINOR finding.
  - New this round: one RESIDUE (PR-body wording only) and two SUGGESTIONs.
  - Prior findings (section 5): R468-1 F1 (MINOR) is resolved. R469-1 R1 (RESIDUE) and three SUGGESTIONs are retained.

## 1. Scope, reconstructed

The scope comes from the public sources only:

- the #81 and #84 issue bodies and their acceptance lists;
- the manager's lane-opening comment on #81 (5977862493) and its rulings (5981958399);
- the PR #157 body and the manager's PR comments (5981967051, 5982389600, 5982471302);
- the repository's README, `docs/README.md` and the architecture documents 02, 03, 06, 08 and 09.

The repository has no AGENTS.md or CONTRIBUTING.md. `docs/README.md` sets the authoring rules: single-source rules and `make check`.

PR #140 (merged) landed #81 acceptance 1 to 3 and #84 acceptance 1 to 3. The manager ruled that this lane closes what is left:

| Item | Source | What it requires at this head |
|---|---|---|
| 1 | #81 acc. 4; manager item 1, as amended by ruling 5981958399 | F08.1 marks T-IDENT-BURST and T-IDENT-REARM landed and graded, and T-CTR-OBSERVE integrator-owned. No other claim says they are graded. |
| 2 | #81 acc. 4; manager item 2 | A check pins T-NOTIF-TIMELIMITED = 300,000 ms and T-LOCK-UNLOCK = 60,000 ms at the top's defaults, preferably through prescaler compression. Each check has a failing default-changing mutant. |
| 3 | #84 acc. 4; manager item 3 | 02 §2 rule 5 states the synchronous active-low reset. No other async-reset wording in docs/architecture is left unreconciled. |
| 4 | manager item 4 (R419-2 F5) | A GET_DYNAMIC_INFO carrying a STREAM_INPUT k record is serialized against sink k's listener steps. It is graded by a G0-style pp_top arm and a mutant that reverts it to the NONE key. HZ8 is amended for exactly this case. 03 §6 and the classifier comment are updated. |
| C | manager constraints | No register-map, port or parameter change. Every other record stays identical. Only the classifier, the GDI key, and these docs and tests are touched. |

The review covers the PR's effective change against processor `main` `07b1469d`: 16 paths, +379/−57. That change is the lane commits `4ffd8f0`, `371505d`, `bacad0e`, `beb7c22` and `7b95590`, the manager's docs commit `1d6c78f`, and the two merges `db2c4eb` and `f9b8f0e`. The merged `main` content (PRs #153 and #154) was reviewed in its own PRs. Here it is checked only for a clean merge.

## 2. Findings

### R469-3-RES1 (RESIDUE): the PR body's head sentence and one line range are stale at this head

- **Lenses:** Docs.
- **Location:** the PR #157 body.
  - Second paragraph: "Six commits: one per item, one README record, and the merge of `main` `c050d971`, which moved during the lane. The head is `db2c4eb`."
  - Section 4, Docs bullet: "`docs/architecture/03_packet_engine.md:264-278`".
- **Evidence:**
  - The exact head is `f9b8f0e`. The body's own closing paragraphs record the manager commit `1d6c78f` and the merge `f9b8f0e`.
  - `1d6c78f` added one line to 03 §6, so the classifier paragraph the bullet cites is now `:265-279`. Line 264 is the READ_DESCRIPTOR sentence, and line 279 ends the GET_DYNAMIC_INFO text.
- **Impact:** wording only. No measurement, figure, verdict, test, code, generated artifact or clause claim changes, and no privacy rule is touched.
- **Exact fix:**
  - Replace the two sentences with: "The lane's six commits (one per item, one README record, and the merge of `main` `c050d971`) end at `db2c4eb`. The manager's round-1b commit `1d6c78f` and the merge of `main` `07b1469d` (PR #154) follow, and the head is `f9b8f0e`."
  - Change `03_packet_engine.md:264-278` to `03_packet_engine.md:265-279`.
- **Verification:** `git log --oneline --first-parent 83999eba..f9b8f0e` and `sed -n 265,279p docs/architecture/03_packet_engine.md` at the head.

### R469-3-S1 (SUGGESTION): grade the waited batch's own answer and the talker side of the GDI cross-lock

- **Lenses:** Tests.
- **Location:**
  - `tb/pp_top/sim_main.cpp:13703-13743`: HZ8's batch and HZ13a/b/c.
  - `beside_or_after` and `acmp_beside_or_after` (`:13411-13470`).
- **Evidence:**
  - HZ8's batch and HZ13a discard the GET_DYNAMIC_INFO answer they waited for (`(void)beside_or_after(...)`). Nothing checks that the serialized batch still answers SUCCESS.
  - HZ13 grades the listener side only. 03 §6 says the batch is held "against every in-flight `STREAM_CFG` step", and that "an ACMP stream step [waits] for the batch".
  - The reviewer probe `scripts/probe_hz_gdi.py` (receipts `probe-hz-gdi.*`) adds RP1 to RP6. All pass at the head (HZ 212 checks, 0 failures):
    - RP1/RP2: a batch naming STREAM_INPUT 2 or 1 waits for a held UNBIND_RX of sink 1, then answers SUCCESS.
    - RP3/RP4: a DISCONNECT_TX of source 1 or 2 waits for a held batch naming STREAM_OUTPUT 1, and the batch answers SUCCESS.
    - RP5/RP6: a GET_TX_STATE, or a GET_RX_STATE of another sink, runs beside it.
  - With `hz-gdi-key-none` planted (receipts `probe-hz-gdi-neg-control.*`), RP1 to RP4 fail with the lane's 7 failures (15 in all). So the probe arms are live.
- **Impact:** none on correctness at this head. The behaviour holds. It is only that no product check would catch an answer lost after the wait, or a talker-side regression specific to GET_DYNAMIC_INFO. The class pair (MAP_CFG, talker STREAM_CFG) is already graded by HZ11 with ADD_AUDIO_MAPPINGS.
- **Suggested outcome:** check `status(...) == AECP_SUCCESS` on the batch answers HZ8 and HZ13a return. Optionally add one talker-side row (as RP3).

### R469-3-S2 (SUGGESTION): bound the two TD windows from both sides in the campaign

- **Lenses:** Tests.
- **Location:** `tb/pp_top/aecp_mutants.py:61-67`.
- **Evidence:**
  - The planted arms push TD1 below its window (59,000) and TD2 above it (301,000).
  - The reviewer probe `scripts/probe_td_window.sh` adds the other side of each, and confirms the wrap's guard is load-bearing. Each fails its named check:
    - `LOCK_TIMEOUT_MS_P` 60,030: TD1 fails, no unlock by 60,021 ms.
    - `REG_TL_TIMEOUT_MS_P` 299,990: TD2 fails, got 299,992 ms.
    - the wrap's `ifndef PP_TOP_TIM_DEFAULTS` removed: TD1 and TD2 fail.
- **Impact:** none at this head. The checks are two-sided by construction, and the probes show it.
- **Suggested outcome:** optionally plant the opposite-side arm of each check, so the campaign records both bounds.

## 3. Lens evidence

### Conformance

- **Item 2.**
  - TD1 grades the auto-unlock notification at the 60,000 ms default: Milan v1.2 §5.4.2.2 and IEEE 1722.1-2021 §7.4.2. Measured: 60,003 ms.
  - TD2 grades the TIME_LIMITED expiry at the 300,000 ms default: IEEE §7.4.37.2. Measured: 300,002 ms, with 6 monitor probes answered (Milan §5.4.5.3). Both are in `receipts/head-pp_top-full.log`.
  - The top's defaults are `REG_TL_TIMEOUT_MS_P = 300_000` and `LOCK_TIMEOUT_MS_P = 60_000`. TD runs on the first build's 1 ms = 100 clk prescaler, as the manager preferred.
- **Item 4.**
  - IEEE §7.4.76.1 handles each GDI record "as if it were an independent command". A GET_STREAM_INFO record of STREAM_INPUT k reads sink k's listener binding record (Milan §5.4.2.10). The batch now waits for that sink's listener step, as the stand-alone getter does (HZ6).
  - The accepted over-serialization is the one the manager allowed: a read batch waits for any stream step, and HZ8 is amended for exactly that case.
  - F03.7 (the RO_SNAPSHOT and MAP_CFG rows), the 03 §6 classifier list and paragraph, F06.14's GDI class cell and 08 §4's ACMP hold list all name the landed MAP_CFG / NONE-key class.
- **Items 1 and 3.**
  - The identify rows cite IEEE §7.5.1 and §7.5.1.2.1. The default `EN_IDENTIFY_NOTIF_P = 1'b0` (`protocol_processor_top.sv:207`) matches the row's "not at its default 0".
  - T-CTR-OBSERVE is integrator-owned, which matches 06 §6.6 and F08.4's reserved slot.
- **Result: CLEAN.**

### RTL

- **The change.** `hdl/top/protocol_processor_top.sv:1645-1646` adds one case arm, GET_DYNAMIC_INFO → `PP_HZ_MAP_CFG` with the default NONE key `{6'h3F,10'h000}`, and updates the comment at `:1539-1554`. The diff against both `07b1469d` and `83999eba` is only these two hunks: no port, parameter or register change.
- **Who reads the class.** `hazard_class` is read only at the scoreboard's admission mux (`:3572`, `:3575`). Its only other appearance is where the normalizer stamps it (`KL_pp_normalizer.sv:136`). No AECP module reads it.
- **What MAP_CFG means for GDI in `KL_pp_scoreboard.sv`:**
  - Rule 5's class-wide cross-lock holds the batch against any STREAM_CFG holder.
  - Rule 2 conflicts with RO_SNAPSHOT only on the same key. No ACMP transaction presents type 0x3F, so ACMP reads still run beside.
  - Rule 3 (LOCK_OP vs a lock-protected member) and rule 4 (MAP_CFG per key) need a second AECP hold. The top keeps one AECP owner (`aecp_sb_active_r`), so neither pair can meet.
- **No starvation.** ACMP holds at most one transaction (`!acmp_sb_active_r` in `acmp_sb_candidate_w`). An ACMP grant sets `sb_prefer_aecp_r`. So a refused GDI head wins the first clock after the ACMP hold frees, and it cannot be starved by a stream of ACMP steps.
- **Deadline.** The deadline stays as stamped at reception (`:3683`). A batch that waited past `T-BUDGET-AECP-WC` is preempted at admission into the forced response (DL4), as any waiting AECP head is.
- **Clean merge.** `scripts/check_merge_union.sh` (receipt `merge-union.txt`) shows `f9b8f0e` is the exact union of `1d6c78f` and `07b1469d`: 16 lane paths and 50 main paths, none changed by both, and every blob equals its side.
- **Gates.** `./scripts/lint_hdl.sh` rc 0, 41 modules, pinned Verilator 5.050.
- **Result: CLEAN.**

### Robustness

- **Faults planted and caught:**
  - the base classification (`hz-gdi-key-none`): 7 failures, plus RP1 to RP4 in the probe build;
  - over-classification (`hz-gdi-as-barrier`): HZ1 and HZ13b;
  - both sides of both default windows (lane arms plus reviewer probes);
  - loss of the wrap guard: TD1 and TD2 fail.
- **Talker side.** A talker step waits for a held batch (RP3, RP4) and a talker read does not (RP5). The batch answers SUCCESS after waiting (RP1b, RP2b) and when held (RP3b).
- **Over-serialization cost.** The added ACMP wait behind a batch is bounded by the batch's own hold. That is preemptible at `T-BUDGET-AECP-WC` plus the op in progress, and 08 §4 states it (`:194-217`).
- **Result: CLEAN.**

### Tests

All runs are at the exact head, in `git archive` copies, with pinned Verilator 5.050. Its identity is in `receipts/verilator-identity.txt`. A wrapper caps each build's `-j 0` at 2 to 4 threads, to keep within the 16-job budget.

- **`make -C tb/pp_top`, all six builds: rc 0, 10,431 checks, 0 failures.**
  - Default build: 9,943, with HZ 189, DL 64 and AX 231. Then fixture 20, identify 178, line 231, timebase 56 (TB) and defaults 3 (TD).
  - This equals the PR body's record: 10,431 total, HZ 177 → 189, TD 3.
- **`aecp_mutants.py --jobs 3`, the lane's six arms: rc 0.** The hazards and timer-defaults controls PASS, and all six arms are KILLED with the failure counts the README tables record:
  - `td-lock-default-59s`: 1, at 59,003 ms;
  - `td-tl-default-301s`: 1, got −1;
  - `hz-gdi-key-none`, `-held` and `-no-stream`: 7 each;
  - `hz-gdi-as-barrier`: 2.
- **`aecp_mutants.py --jobs 3`, the three arms whose counts moved: rc 0, all KILLED.** `hz-stub-restored` 81, `hz-acmp-reads-as-steps` 27, `hz-barrier-no-priority` 139. The README's new counts match exactly.
- **Reviewer probes:**
  - RP1 to RP6: 23 extra checks, all PASS at the head. The negative control fails RP1 to RP4.
  - Three TD window probes, each failing its named check: see S2.
- **`git diff --check`:** rc 0 against both `07b1469d` and `83999eba`.
- **Not re-run here:**
  - the full 61-arm AECP campaign;
  - every other campaign and `run_suites.sh`;
  - base-vs-head record comparison of the unchanged arms.

  The manager's banks own these (see limits).
- **Result: CLEAN.** S1 and S2 are suggestions only.

### Docs

- **`make check`: rc 0.** 41 mermaid and 18 wavedrom blocks, 1,133 links, the matrix (115 REQ rows, 17 GAPs; 94 module rows, 0 untested), and parameters 28/28/28.
- **`python3 scripts/gen_matrix.py --check`:** rc 0.
- **02 §2 rule 5** (`02_interfaces.md:115-124`).
  - Its claims hold. All 164 `always_ff` blocks in `hdl/` are `@(posedge clk_i)`, and there is no `negedge` and no `always @(posedge ...)`. The top has one reset port, `rst_n`, declared synchronous active-low (`:233`).
  - Rule 5 agrees with the integrator guide §1, the hdl-engineer guide's reset row and 01 §5's hold-based boot order.
  - The other "async" wording in `docs/architecture` is FIFO and NVM-commit wording, not reset wording.
- **F08.1 rows** (`08_timing.md:30-32`).
  - They name `KL_aecp_notify` and the grading suites, `tb/pp_top` ID and `tb/aecp_notify` FT. Both exist, and their READMEs cite the T-IDs.
  - 09 F09.3's TIM goal (`:53`) now excludes the integrator-owned row. No other doc claims T-CTR-OBSERVE is graded (grep over `docs`, `hdl` and `tb`).
- **09 §8.3 and the `tb/pp_top` README.**
  - They describe TD, HZ8's exception and HZ13 as the bench implements them.
  - The campaign table rows for the six new arms and the three moved counts match what was measured here.
- **Result: CLEAN.** RES1 is RESIDUE (PR body only).

## 4. Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #81/#84 acceptance and rulings; F08.1, F03.7, F06.14, 03 §6, 08 §4; IEEE §7.4.2, §7.4.37.2, §7.4.76.1, §7.5.1; Milan §5.4.2.2, §5.4.2.10, §5.4.5.3; TD measured values | R469-3 | f9b8f0ee6604a73b9fa82c62b91811e9f53b320a |
| RTL | CLEAN | `protocol_processor_top.sv` classifier and admission/deadline blocks; `KL_pp_scoreboard.sv` matrix; `KL_pp_normalizer.sv` stamp; merge union; lint 41/41 | R469-3 | f9b8f0ee6604a73b9fa82c62b91811e9f53b320a |
| Robustness | CLEAN | lane arms; reviewer probes RP1 to RP6 and their negative control; TD window and wrap-guard probes; starvation and deadline reasoning | R469-3 | f9b8f0ee6604a73b9fa82c62b91811e9f53b320a |
| Tests | CLEAN | `make -C tb/pp_top` six builds 10,431/0; AECP campaign 6 new arms and 3 moved-count arms with controls; probe receipts; `git diff --check` | R469-3 | f9b8f0ee6604a73b9fa82c62b91811e9f53b320a |
| Docs | CLEAN (RESIDUE RES1 and retained R469-1 R1 carried) | `make check`, `gen_matrix --check`; 02 §2 rule 5; F08.1; F09.3; 09 §8.3; 03 §6; 06 F06.14; 08 §4; `tb/pp_top` README; PR body | R469-3 | f9b8f0ee6604a73b9fa82c62b91811e9f53b320a |

## 5. Prior public review findings at this head

I read R469-1 (5982146515, POSITIVE at `db2c4eb`) and R468-1 (5982374908, NEGATIVE at `db2c4eb`) only after my own pass, verdict and ledger above were written. R468-2 and R469-2 were withdrawn unfinished (5982471302) and carry no findings. Each prior finding is checked at `f9b8f0e` below.

| Prior finding | Severity | State at this head | Evidence |
|---|---|---|---|
| R468-1 F1: F06.14, F03.7 and the 03 §6 classifier list still called GET_DYNAMIC_INFO RO_SNAPSHOT | MINOR | **RESOLVED** by `1d6c78f` | See below. |
| R468-1 S1 / R469-1 S1: TD pins each default within a 20 ms window | SUGGESTION | **RETAINED** as a suggestion, folded into this round's S2 | `notify_phases.hpp` is unchanged since `db2c4eb`; `SLACK_MS = 20`. |
| R468-1 S2: HZ13 discards the batch answers; talker side ungraded | SUGGESTION | **RETAINED** as a suggestion, the same as this round's S1, which I reached independently | `sim_main.cpp` is unchanged since `db2c4eb`. |
| R468-1 S3: add "Relates to #71" | SUGGESTION | **RESOLVED** | The PR body carries "Relates to #71" (manager note 5982389600). |
| R469-1 S2: #84 "What remains" (3), F01.5's P-EN-PLAIN-IEEE-PROFILE has no RTL consumer and is not recorded | SUGGESTION | **RETAINED** for the manager's residue checklist or a follow-up issue | `01_overview.md:193` still reads "selects IEEE ROM columns", and `01_overview.md` is unchanged since `83999eba`. It is not one of #84's frozen acceptance items. |
| R469-1 R1: 09 restates two F08.1 values (`09_verification.md:254`, `:272`), against `docs/README.md` §2's timing single-source rule | RESIDUE | **RETAINED** as RESIDUE | Both lines are unchanged at this head. `make check` does not flag them. |

**R468-1 F1, the evidence for RESOLVED:**

- `06_aecp_engine.md:269`, the F06.14 GDI class cell, reads "MAP_CFG at admission, no-descriptor key (assigned by the top's classifier, 03 §6); records RO".
- `03_packet_engine.md:235`: RO_SNAPSHOT covers "all GETs but GET_DYNAMIC_INFO".
- `03_packet_engine.md:238`: the MAP_CFG row lists GET_DYNAMIC_INFO.
- `03_packet_engine.md:252`: "GET_DYNAMIC_INFO `MAP_CFG` (below)".
- `grep "RO per record"` is empty, and `make check` passes.
- HZ1's GDI row (MAP, NONE) now agrees with both tables.

**R469-1 R1, the exact fix:**

- `:254`: "at the top's own defaults ([F08.1](08_timing.md#fig-08-constants)), not the 400 ms override …".
- `:272`: "waits out the real `T-NOTIF-TIMELIMITED`, 30 million clocks".

The fix R469-1 published embedded a mis-rendered absolute link. The relative link above is the one to apply.

The retained items are a SUGGESTION or a RESIDUE, so none leaves a lens unclean. **R419-2 F5**, the PR #140 finding this lane remedies, is resolved at this head:

- HZ13a passes.
- `hz-gdi-key-none` reproduces the old admission ("refused 0 clocks"), and is KILLED.

## 6. Real limits

- **Not run here.** The full parent, PP, gPTP, Yosys and builder banks, `run_suites.sh`, and the other campaigns: the full 61-arm AECP campaign, dispatch, ACMP, ctr, d3, gsi, name_wr, notify, maap and adp. Nor was base-vs-head record identity of untouched arms re-measured. Those are the manager's source banks.
- **Manager evidence not found in the pinned tree.** The pinned evidence tree `5de7b6be…/review-evidence/pp81-r1` holds the author packet only: HANDOFF, PR body and three parent patches. I found no manager bank receipt for `f9b8f0e` there. The manager's statement that donor and consumer banks passed at this head is taken from the PR comments, not from receipts I read.
- **Area not re-measured.** No Vivado or out-of-context run. The PR body's area table is at `83999eba`, `7b95590`, `c050d971` and `db2c4eb`, and the manager's ruling (5981958399) covers it. The merge of PR #154 (SRP storage) after `db2c4eb` is not re-measured.
- **No hardware.** No physical calibration and no hardware run. Field skips are not hardware proof.
- **Verilator version.** Builds used Verilator 5.050 through a thread-capping wrapper (`scripts/verilator-jcap.sh`). It only rewrites a bench's `-j 0` build parallelism.
- **No submodules.** This tree has no `.gitmodules` and no gitlinks, so there were no submodule gitlinks to verify.

## 7. Pending manager duties

- Carry to the residue checklist:
  - RES1's exact fix (PR body);
  - R469-1 R1's exact fix (`09_verification.md:254` and `:272`, section 5);
  - R469-1 S2, the P-EN-PLAIN-IEEE-PROFILE note in F01.5, or a follow-up issue for it.
- Build and accept the final current-dev candidate at the merge turn (source base `83999eba`, live dev `fea346e7`), with the hosted/act acceptance. That includes PR #153's parent patch (`parent-adoption-232-241f9184.patch`), which the pin bump owes.
- Publish this packet: `REPORT.md` and the files listed in `MANIFEST.sha256`.

## 8. Clone state after the review

Recorded in `receipts/clone-integrity.txt`:

- The clone is at `f9b8f0e` with tree `0e4e1c96`. Worktree and index equal HEAD in content and mode.
- There are 0 untracked or ignored entries. The 558 index entries equal the HEAD tree, and every file's `hash-object` equals its HEAD blob.
- Every probe ran in `git archive` copies under `scratch/`, never in the clone.

R469-3 FINISHED
