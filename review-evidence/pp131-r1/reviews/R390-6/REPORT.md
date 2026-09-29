[R390] POSITIVE - exact head 9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f

# R390-6: independent internal review of processor PR #132 (issue #131, D3 lane 1), round 6

| | |
|---|---|
| Head / tree | `9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f` / `ec8876e6c9d1670a745bc0ffd00134d6ddcfea92`. Verified in the review clone, and equal to the live PR head. |
| Delta reviewed | `9dce84ea..9b4da6b5`: one commit, `9b4da6b`, 6 files, +142 / -26, all under `tb/` and `docs/`. Also the PR body's Round 6 section and its consolidated parent-visible list, and the author's round-6 archive (public `kebag-logic/milan-fpga` branch `pp131-review-evidence` at `3ad574a4`, `review-evidence/pp131-r1/author-r6/`). |
| Assignment | Processor #131 comment 5885497133 (round 6). Review start: PR #132 comment 5887937185. |
| Verdict | **POSITIVE.** No MINOR or higher finding is open, and all five lenses are CLEAN. My round-5 finding R390-5-F1 (= R391-5 S1) is **resolved**. R391-5 S2 is **carried** into the PR body. Two SUGGESTIONs are recorded; neither affects the verdict. |

## 1. How the review was reconstructed

- **Scope.**
  - The repository has no `AGENTS.md` or `CONTRIBUTING.md`, so I started from `docs/README.md` and the issue body (contract section 18.1 at parent `7a7582f0`, DR1a-DR6).
  - I read every manager comment on #131. Rounds 1-5 were already known to me from my own earlier rounds. This round adds the round-6 assignment (5885497133) and the author's REVIEW READY (5886545587).
  - The round-6 assignment has three required items and says there is no RTL change.
- **Authority for the arbiter.**
  - The arbiter's banner and drain terms: `hdl/packet_engine/KL_pp_nvm_mgr_arb.sv:38-65`, `:153-170`.
  - Parent contract section 6.4: the drain is owner-matched (lines 797-808). Its section 15 port row says an abort abandons the READ the port serves "for that manager" (line 535).
  - The round-4 ruling on the issue-cycle arm (5880658258 item 1).
  - How the binding manager raises its abort: `hdl/acmp/KL_acmp_nvm_shadow.sv:561-576`, where `nvm_abort_o = rs_tmo_w && (hs_r == H_RS_STREAM)`.
- **Diff and history.**
  - `git diff 9dce84ea..9b4da6b5` touches `tb/acmp_nvm/{sim_main.cpp, acmp_nvm_wrap.sv, README.md}`, `tb/pp_top/{d3_mutants.py, README.md}` and `docs/architecture/09_verification.md`.
  - `git diff --quiet 9dce84ea..HEAD -- hdl syn scripts .github Makefile` is true, so **no RTL changed**.
  - I reviewed the whole-lane diff from `c951a9ff` in rounds 1-5.
- **Parent.** I used a blobless public clone of milan-fpga, read-only, for facts only.
  - I checked dev `eaa88a32` (the author's measurement base) and dev `9e3ccbfb` (the manager's live dev for this round).
  - Public dev has since moved to `79c36963`, which I did not assess.
  - I applied the author's `parent_edits.py` only to disposable extracts under `scratch/`.
- **Public evidence.**
  - `review-evidence/pp131-r1` at `b657a2de`, the round-1 author packet.
  - The round-6 author archive: `parent_edits.py`, `receipts/parent-edits.diff` and `receipts/n11d-counts-9b4da6b.txt`, plus the author's receipts of my round-5 scripts.
  - The hosted check runs at the exact head (section 6).
- **Prior findings.** I read R391-5 only after my independent pass. That pass is recorded, timestamped, in `receipts/independent-verdict-before-prior-findings.txt`. R390-5 is my own report.
- **Tool.**
  - The assigned wrapper `.../372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host.
  - I used the sibling wrapper, which is byte-identical (sha256 `905795b9...`, the same across all 195 copies on the host). It runs Verilator 5.050 rev v5.050, binary sha256 `fb2cc573...`: the same identity as in R390-5 (`receipts/tool-identity.txt`).

## 2. Findings

No finding at MINOR or above is open.

### Suggestions (they do not affect the verdict)

**R390-6-S1 (Docs; Tests only for the reproduction record): the `make pinned` reproduction count in `tb/acmp_nvm/README.md` is stale.**
- **Where:** `tb/acmp_nvm/README.md:265-268`: "`make pinned` ... exits non-zero. It is the reproduction of the recorded L05 control: 107 of 349 checks fail".
- **Evidence:** I ran `make pinned` in `git archive` extracts (`receipts/pinned-*.log`):

  | Revision | Pinned run |
  |---|---|
  | base `c951a9ff` | 107 of 349 fail |
  | round-5 head `9dce84ea` | 109 of 359 fail |
  | this head | 110 of 360 fail |

  - The lane added two failures in earlier rounds (N10 and N11b) and swapped one N3 line for another.
  - This round adds N11d, which also fails under the pinned wiring because the walk does not complete as saved there. That is expected.
  - L05a still fails as the text says, and the exit is still non-zero.
- **Impact:** Small. `make pinned` is not part of the suite's run or CI, and its qualitative claim holds. Only the stated count no longer reproduces. The later LG/B/BC rows at "of 349" are dated mutation records and are fine as they are.
- **Suggested outcome:** Either restate the pinned count as 110 of 360 at the lane head, or mark "107 of 349" as the dated base record.

**R390-2-S1 (RTL, Docs), carried:** No `RX_SLOTS_P >= 2` floor is checked or stated (`protocol_processor_top.sv:86`, unchanged).

## 3. Round-6 assignment items verified

| Item (5885497133) | Result | Evidence |
|---|---|---|
| **(1) R390-5 F1 = R391-5 S1: N11d, and the two new controls** | **resolved** | Details below |
| **(2) 09 section 8.2 and the `tb/acmp_nvm` README grade exactly what the tree grades, and list the ungraded manager-0 inputs with the out-of-tree probes** | **met** | Details below |
| **(3) The PR body's Round 6 section and the consolidated list carry R391-5 S2** | **met** | Details below |
| **No RTL change** | **confirmed** | `git diff --quiet 9dce84ea..HEAD -- hdl syn scripts .github Makefile`. The DR3a and DR4 statements in the body follow from this. |

**Item (1) detail.**
- **The check is correct and cycle-exact.**
  - The harness drives before the negative edge and samples before the positive edge (`sim_main.cpp:804-811`).
  - `m0_rd_own` is set in the sample of manager 0's READ issue (`arb_req_o && mgr_req_o && !mgr_we_o`, which implies `iss0_w`). It is cleared in the sample of the cycle whose `arb_end_o` is high (`:693-705`, `:787-792`).
  - The abort term `m1_abort_over_m0 && m0_rd_own` (`:661`) therefore covers exactly issue+1 through the done or err cycle. That is the arbiter's `own_r == O_M0` window: ownership retires on the pulse, `:136`, `:148-149`.
  - It never covers the issue cycle.
  - `arb_end_o = np_done_w || np_err_w` (`acmp_nvm_wrap.sv:544`) is the same net pair the arbiter receives as `p_done_i`/`p_err_i` (`:348-349`).
  - Manager 1's request stays low, so the abort is presented alone.
- **Readings at the head.** I planted one print-only line in an extract (`scripts/r6_n11d_probe.py`, `receipts/r6-n11d-probe/`). The results:
  - the abort is present in **168 of 168** owned cycles over **8** READs, with the fewest owned cycles before an end being **12**;
  - it is present in **0 of 8** issue cycles;
  - `drain_on = -1`, `aborts = 0`, no leaks, and 360 of 360 checks pass.

  These equal the author's `n11d-counts-9b4da6b.txt` and the README.
- **The non-vacuity terms are live.** Two harness edits each make N11d fail on the head's arbiter:
  - withholding the abort in the end cycle gives 160 of 168;
  - also presenting it in the issue cycles gives 8 of 8 issue cycles.
- **Reach.** Two further reviewer arbiter edits are both KILLED by N11d alone. In each, manager 0's owned term takes manager 1's abort only while a byte is in hand, or only while none is.
- **The tree's campaign.** I ran `d3_mutants.py` from the tree in four batches (`receipts/d3-*`): **83 of 83 KILLED, and all four goldens PASS** (`acmp_nvm`, `pp_top` ×3, `rx_validator`).
  - `owned_arm_cross_intent` and `cross_own_m1_drains_m0` each fail exactly one check, N11d.
  - `issue_arm_cross_intent` still fails N11b alone.
  - `scripts/readme_counts.py` finds every one of the 83 failing-check counts equal to its README row (`receipts/readme-counts.txt`). The `rx_validator` row sits in that README's M4 table, at 4.
- **My round-5 scripts at the head.**
  - `r5_extra_mutants.py`, suites `acmp_nvm` and `pp_top` (`receipts/r5-extra/`):
    - `r5_owned_cross_m0_only` and `r5_owned_cross_both` are **KILLED by N11d** (1 failing check each), and `r5_issue_cross_m0_only` by N11b;
    - `r5_issue_cross_m1_only` and `r5_owned_cross_m1_only` still pass. They are the manager-0 halves, now declared;
    - `r5_identity` passes;
    - all six pass `pp_top --d3-only`, as in round 5.
  - `r5_owned_cross_probe.py` (`receipts/r5-owned-probe/`):
    - R5P still plants and passes, 361 of 361;
    - under `r5_owned_cross_m0_only`, R5P and N11d both fail;
    - the **unmodified harness now fails N11d** (359 of 360). The script's own label reads "SURVIVED" only because its placeholder check name matches nothing: rc 2, one FAIL, N11d.
  - The unit probe runner `run_arb_unit_mutants.py` is **byte-identical** to my R390-5 receipt: 9 of 9 at the head (`receipts/arb-unit-r5-script-at-head.txt`).
- **No side effects.**
  - Verilator's warning set equals round 5's (13 PINCONNECTEMPTY).
  - N1-N11c are unaffected: `m1_abort_over_m0` defaults false and is cleared in `reset()` (`:863`).
  - The check count goes from 359 to 360, +1.

**Item (2) detail.**
- **The 09 row** (`docs/architecture/09_verification.md:192`) now claims only manager 1's half of each rule, mapped as follows. The mutant evidence matches each mapping:

  | Rule, manager 1's half | Graded by |
  |---|---|
  | its WRITE presented with an abort is never drained | N11a, which holds the abort from strobe to end, so both the issue and the owned WRITE terms; `issue_arm_write_too` and `owned_arm_write_too` KILLED |
  | its abort drains none of manager 0's READs | N11b in the issue cycle, N11d while owned |
  | after its WRITE, its READ abandoned in the issue cycle is still drained | N11c |

  The row states that the manager-0 halves are ungraded by construction. The count is 83.
- **The `tb/acmp_nvm` README** (`:213-263`).
  - It describes N11d as it is coded, with the counts.
  - It lists five manager-0 inputs. That list is complete: two drain terms × three banner rules gives six manager-0 cells. One of them, manager 0's own issue-cycle READ abort, is the graded D3R18/N10 behaviour. That leaves five, and the README lists them.
  - Its reachability argument matches the RTL. `nvm_abort_o` rises only in a stalled `H_RS_STREAM` clock. In the first stalled cycle the per-wait count is 0, so an issue-cycle abort needs `rs_agg_i` (`KL_acmp_nvm_shadow.sv:564-576`).
- **The README's "out-of-tree probe" column, checked against my own texts** (`scripts/run_arb_unit_r6.py`, `receipts/arb-unit-r6.txt`):

  | Manager-0 input | README claim | My unit-probe result |
  |---|---|---|
  | its abort in manager 1's issue cycle | killed by case F | F only |
  | its WRITE strobe with its abort | killed by case B | B only |
  | its READ abandoned in its issue cycle after a WRITE | killed by case B, through the WRITE half | B only, through the WRITE half: with `we_r` 0 after reset, a WRITE strobe with an abort arms the drain |
  | its abort while manager 1 owns a READ | not killed by the unit probe | 9 of 9 pass |
  | its abort while it owns a WRITE | not killed by the unit probe | 9 of 9 pass |

  - The two new tree controls also pass the unit probe, as the README implies: it has no owned-cross case.
  - The citations of R391-5 (six edits, `mon_unreachable_inputs`, 17,406 sweep runs) match that review's text (5885492313).
- **Counts elsewhere.**
  - `tb/pp_top/README.md:667-669` reads seven N11 controls and 83. The seven are the five of round 5 plus the two new ones.
  - The `acmp_nvm` mutation table reads "All eleven".
  - No stale 359, 81 or "N11a-c" remains in the tree (grep).
  - `make check` rc 0 (links 968, matrix, modmatrix, params, stale).
  - `git diff --check` rc 0, both `c951a9ff..HEAD` and `9dce84ea..HEAD`.

**Item (3) detail.**
- **The PR body's Round 6 section** describes N11d, its counts, the two controls and the docs exactly as the tree has them.
- **The consolidated list** adds the "Round 6" behaviour bullet: the five manager-0 inputs, and "whatever makes manager 0 present one of them must grade it first".
- **R391-5 S2** gets its own sub-bullet: the word-36 check now precedes the moved arm, and the real edit must re-read word 36 after the arm or in its heal. It names three stale comments (the two R391-5 names plus "[AECP-WTMO] added one deliberately").
- **I checked it against a scratch extract.** I applied the author's round-6 `parent_edits.py` (sha256 `80d2c396...`, byte-identical to round 5's) at `eaa88a32` (`receipts/parent-s2-lines.txt`). The arm call is at `:2484`, after `grade_the_first_descriptors_on_the_wire()` at `:2480`. That function starts at `:2563`, and the word-36 check is at `:2609-2610`. The three comments are at `:2547-2549`, `:2560-2562` and `:2604-2606`. The body gives `:2605-2607` for the third: the comment spans 2604-2606 and 2607 is its `ck`, a one-line offset that is harmless.
- **At the manager's live dev `9e3ccbfb`,** the same script applies cleanly. Its changed lines equal the author's `parent-edits.diff`, and every cited line is at the same number (`sim_nxn.cpp`'s only change there is at line 7871).
- **The two stale harness comments** are stated as parent-side, pin-adoption work, which is correct: they are in the parent harness, not in this repository.

## 4. Prior public findings, resolved or retained at this head

| Finding | Status | Basis |
|---|---|---|
| **R390-5-F1** (MINOR: the owned half is ungraded; 09 and the limit statement overclaim) | **RESOLVED** | Section 3, items (1) and (2). My required outcome, preferred branch: a named check (N11d) with a non-vacuity count; the `owned_arm_cross_intent` control KILLED with a README row; `r5_owned_cross_m0_only` KILLED by the new check. The README records both by-construction inputs I named and the probe that covers the first (case F). |
| **R391-5 S1** (the same gap) | **TAKEN** | `cross_own_m1_drains_m0` is in the tree and KILLED by N11d. The six inputs are accounted for (five listed, one graded). |
| **R391-5 S2** (the `[AECP-WTMO]` order and stale comments, parent side) | **CARRIED** to the pin-adoption list | Section 3, item (3) |
| R390-5 limit (hosted `suites` in progress at `9dce84ea`) | superseded | R391-5 read success at `9dce84ea`; at this head, see section 6 |
| R390-3-S2 (a bound inside a healthy re-LOCATE ends CLOSED) | **still open for the manager's ruling** | no ruling in round 6; RTL and D3R15 unchanged |
| R390-2-S1 (`RX_SLOTS_P` floor) | not taken; carried | `hdl/` unchanged |
| R390-1…R390-4 and R391-1…R391-4 findings | **still RESOLVED or TAKEN** | No `hdl/` change since round 4. All their controls are among the 83 KILLED. Hosted `pp_top` 7,888/7,888. |

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | N11d and the 09 row against contract 6.4 (797-808), the line-535 port row, the arbiter banner `:38-65` and the round-4 issue-cycle ruling. The five manager-0 inputs against the shadow's abort equation (`KL_acmp_nvm_shadow.sv:561-576`). The round-6 assignment items 1-3. | R390-6 | `9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f` |
| RTL | CLEAN | No `hdl/`/`syn/` change. `KL_pp_nvm_mgr_arb.sv` re-read: own/drain equations `:133-170`. The new wrap tap `arb_end_o` is `np_done_w \|\| np_err_w`, the arbiter's `p_done_i`/`p_err_i` (`acmp_nvm_wrap.sv:88, 348-349, 544`). Unit probe 9/9 at the head. | R390-6 | `9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f` |
| Robustness | CLEAN | N11d uses the bounded `go()`/`l_finish()`. Every mutant and probe run completed with its tally: 83 tree mutants, 12 reviewer runs, 5 N11d probe runs, 3 R5P runs and 21 unit-probe runs, with no hang or crash. The warning set equals round 5's. `make pinned` still builds and exits non-zero as documented (count: S1). | R390-6 | `9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f` |
| Tests | CLEAN | `acmp_nvm` 360/360. N11d readings 168/168, 0/8 and min 12, with both non-vacuity terms shown live. `d3_mutants.py` 83/83, goldens PASS, README counts equal the run. My R390-5 scripts reproduce as required. Two new reach edits KILLED. Hosted `suites` success, both events. | R390-6 | `9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f` |
| Docs | CLEAN (S1 suggestion) | 09 section 8.2 row `:192` and the count 83. The `acmp_nvm` README: 360, N11a-d, the ungraded table, the eleven-row mutation table. The `pp_top` README: seven and 83. The `sim_main.cpp` banner `:2619-2633`. The PR body's Round 6 section and consolidated list against the scratch parent at `eaa88a32` and `9e3ccbfb`. `make check` rc 0; `git diff --check` rc 0. | R390-6 | `9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f` |

## 6. Real limits of this review

- **Hosted checks at `9b4da6b5`.** Workflow `hdl` ran twice: push run 36552529765 and pull_request run 36552533874. All six jobs executed and **completed with success**: `docs-gates`, `portability` and `suites` in each run (`receipts/hosted-checks.tsv`, polled 10:33 UTC).
  - In the push `suites` job, the only skipped step is "Build Verilator v5.050". That is a cache-hit context, not a skipped gate (`receipts/hosted-suites-steps-push.tsv`).
  - Its log shows 33 suites and 1,016,036 checks, 0 failing, including `acmp_nvm` 360 and `pp_top` 7,888 (`receipts/hosted-suites-push-tallies.txt`).
  - The manager owns hosted and act acceptance.
- **Not run by me:**
  - the full processor bank locally: lint, Yosys, the `srp_top` mutants and the `nvm_port` figures. There is no RTL change, and the hosted `suites` job covers the suites;
  - any parent bench (the consumer set, `milan_dp_gptp`/`ax1x1gptp`, `pp_shadow`, `nvm_cosim`, `milan_dp_render`), any builder, gPTP or Yosys bank, xvlog, Docker, act or hardware.

  My parent work was limited to applying the edit script to extracts and reading lines. I did not see the manager's regenerated `parent_edits.py` at `9e3ccbfb` (carrying #616, #619 and #617). The author's unchanged script applies there cleanly.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Not verified independently:** the R391-5 monitor's "none presented" result. I cite it, and I checked that the README quotes it faithfully. My own reachability reading of the RTL agrees with it.
- **Tool path.** The assigned wrapper was absent; I used an identical 5.050 wrapper (section 1).

## 7. Pending manager duties

- The donor full bank and the **patched parent consumer bank** at dev `9e3ccbfb` with the regenerated `parent_edits.py`, plus `milan_dp_gptp` (`ax1x1gptp`, outside the 16) if its inputs moved. `sim_ax1x1gptp.cpp` did change between `eaa88a32` and `9e3ccbfb`.
- The **final current-dev candidate** build at the merge turn (source base `c951a9ff`, live dev `9e3ccbfb`; public dev has since moved to `79c36963`).
- Hosted and act acceptance, recording that physical calibration is NOT RUN.
- Carry into the pin-adoption lane:
  - the consolidated list, including R391-5 S2 (word-36 re-read and three comments);
  - the five ungraded manager-0 arbiter inputs;
  - the firmware persistence-disabled boot path with its host test.
- Consider R390-6-S1 (the pinned count) and R390-2-S1. **Rule on R390-3-S2**, which is still open.

## 8. Receipts and reproduction

- **Scripts** (`scripts/`):
  - `r5_extra_mutants.py`, `r5_owned_cross_probe.py`, `run_arb_unit_mutants.py` and `arb_unit/`: carried from R390-5, unchanged;
  - `r6_n11d_probe.py`: N11d's readings, its non-vacuity and its reach;
  - `run_arb_unit_r6.py`: the unit probe against the five manager-0 halves and the new controls;
  - `readme_counts.py`: README counts against a run.
- **Commands.** Run from the review clone with `TMPDIR` under `scratch/`, 8 jobs or fewer, in the foreground:
  - `python3 tb/pp_top/d3_mutants.py --output <dir> --verilator <v> --jobs 8 --only <names>`, in four batches: `acmp_nvm` 11, then 36, 18 and 18;
  - `python3 <packet>/scripts/r5_extra_mutants.py --tree . --output <dir> --verilator <v> --jobs 8 --suites acmp_nvm pp_top`;
  - `python3 <packet>/scripts/r5_owned_cross_probe.py --tree . --output <dir> --verilator <v>`;
  - `python3 <packet>/scripts/r6_n11d_probe.py --tree . --output <dir> --verilator <v>`;
  - `python3 <packet>/scripts/run_arb_unit_mutants.py . <scratch> <v>` and `run_arb_unit_r6.py . <scratch> <v>`;
  - `python3 <packet>/scripts/readme_counts.py --tree . <results.json>...`;
  - `make pinned` in `git archive` extracts;
  - `make check` in a scratch clone.
- **Receipts** (`receipts/`):
  - mutants and probes: `d3-acmp_nvm/`, `d3-batch1/`, `d3-batch2a/`, `d3-batch2b/` (and their `-stdout.txt`), `readme-counts.txt`, `r5-extra/`, `r5-owned-probe/`, `r6-n11d-probe/`, `arb-unit-r5-script-at-head.txt`, `arb-unit-r6.txt`;
  - pinned runs: `pinned-{c951a9ff,9dce84ea,9b4da6b5}.log`;
  - gates and hosted: `make-check.txt`, `diff-check.txt`, `hosted-checks.tsv`, `hosted-checks-poll1.tsv`, `hosted-suites-steps-push.tsv`, `hosted-suites-push-tallies.txt`;
  - parent and environment: `parent-s2-lines.txt`, `tool-identity.txt`, `clone-integrity.txt`, `independent-verdict-before-prior-findings.txt`.

  Private paths are redacted to `<pinned-tool-root>`, `<pinned-tool-bin>`, `<packet>` and `<review-clone>`.
- **Clone restored.** After the probes, HEAD is `9b4da6b5` and the tree is `ec8876e6`. The index writes the same tree, and all 312 work-tree blobs rehash to their index blobs with matching modes (300 × 100644, 12 × 100755). Status, including ignored files, is empty. The repository has no gitlinks and no `.gitmodules`, so no submodule gitlink is required. The one ignored artifact my runs created, `tb/pp_top/__pycache__/`, was removed (`receipts/clone-integrity.txt`).

R390-6 FINISHED
