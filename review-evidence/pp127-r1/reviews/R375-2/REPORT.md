[R375] NEGATIVE - exact head 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c

# R375-2: external independent review of processor PR #130 (issue #127), round 2

- **Head:** `00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c`, tree `95f398f31a3dc99709b167459576f5e300c3de5d`.
- **Delta reviewed:** `cf4e5c63..00b5c6c9`, one commit (executor [A398]), on base `16be6768f710e79450aace277abacd6c2c3336e5`. I also re-read the full `16be6768..00b5c6c9` diff.
- **Production RTL is unchanged in this round.** `git diff cf4e5c63 00b5c6c9 -- hdl` is empty. The round changes documentation, testbenches, the mutation driver, and 56 checked-in mutation patches.
- **Clone integrity.** The review ran in a cleared context, in a detached clone. At the end, the clone was verified byte-exact against the head (`receipts/clone-integrity.txt`):
  - HEAD and tree match;
  - all 306 tracked blobs and modes match;
  - index == HEAD, with no untracked or ignored files;
  - the repository has no submodule gitlinks.

## Verdict summary

**Every round-1 item is resolved at this head.** This covers my F1–F4 and the other round-1 review's F1–F5:

- **Consumer gates.** The parent consumer gates are 11/11 (manager, PR #130 comment 5862231642).
- **Required reviewer mutants.** All seven fail named assertions (O1–O5) in the committed suite. I confirmed this independently.
- **Coalescing and arbitration.** Join-tick coalescing (O6) and the same-cycle MVRP/prepare arbitration (encoder O8) are pinned.
- **README count.** The stream-FSM README count is fixed.
- **Canceled empty reservation.** Its TX-slot hold is documented with conditional bounds. I measured both bounds independently.
- **Parent replay.** The harness sources are published with matching hashes. I re-ran them, and the deadline-anchored oracle fails on the base RTL and passes at the head.
- **Unchanged semantics.** LV + rLv and #108 are unchanged.

**One new MINOR finding in the Tests lens (R2-F1) makes the verdict NEGATIVE.** The round adds 56 `tb/srp_top/mutations/*.patch` files, and `git diff --check 16be6768 HEAD` now exits 2 on them: 31 whitespace hits in 23 files. At round 1 the same check was clean. The manager reports this as the one failing donor bank step (8/9, comment 5862222946), and I reproduced it independently.

## Reconstruction (order followed)

1. **Contributor rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md` (`git ls-files`). I used `README.md` and `docs/README.md` instead.
2. **Frozen scope.** From the issue #127 body, the round-1 assignment 5860872275, and the round-2 assignment 5861796018. The round-2 assignment carries the required items 1–2, the taken suggestions, and the manager decision that the deadline-anchored oracle is the accepted parent-replay proof. LV + rLv and #108 stay unchanged.
3. **Authorities.** 802.1Q-2014 §10.7.9 / Table 10-5 / Table 10-4, as quoted in `docs/architecture/10_srp_engine.md` §6.5. Milan Δ13. Timer values from `docs/architecture/08_timing.md` (T-MRP-JOIN 200 ms, T-MRP-PERIODIC 1000 ms, T-MRP-LEAVEALL 10–15 s).
4. **Diff and history.** `git diff 16be6768..00b5c6c9` (71 files) and the delta `cf4e5c63..00b5c6c9` (64 files, no HDL).
5. **Public evidence.** I read these only after my own diff pass:
   - `kebag-logic/milan-fpga@88ed7be3/review-evidence/pp127-r1` (round 1);
   - the round-2 author packet, archived at `kebag-logic/milan-fpga@86750aca` `review-evidence/pp127-r1/author-r2`, on branch `pp127-review-evidence`;
   - the manager comments 5862222946 (donor bank 8/9) and 5862231642 (parent consumer gates 11/11).

   All 104 round-2 files match the archive manifest's published hashes. 67 of them are path-redacted, which is why their raw `SHA256SUMS.txt` lines do not match (`receipts/public-evidence-verification.txt`).
6. **Prior public findings.** My own R375-1 findings, plus the other round-1 review's findings (PR comment 5861793313). I read the latter only after my verdict and ledger were fixed. I did not read any same-round report.

## Tool identity

The requested path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used `$VALIDATION_STORAGE/pp127-manager-00b5c6c9/pinned-tool-bin/verilator` instead:
- It is byte-identical (sha256 `905795b9…`) to the `372-manager-r2` wrapper and to the round-1 wrapper.
- It reports `Verilator 5.050 2026-07-01 rev v5.050`.

The system 5.052 was not used (`receipts/tool-identity.txt`).

Build parallelism was capped at `-j 2` per build in the disposable extractions (build flag only), and I ran at most 8 concurrent jobs.

## Executed evidence (all in this packet)

| What | Result | Receipt |
|---|---|---|
| Head suites from a clean `git archive` extraction | srp_top 1987/1987, srp_encoder 562/562, srp_stream_fsms 1215/1215, srp_decoder 190/190, srp_admission 991231/991231, pp_top 7751/7751; all rc 0 | `receipts/head-suite-*.log`, `head-suites-rc.txt` |
| Six-cycle no-storm at head | 4, 3, 3, 3, 3, 2 frames; Ready in all six cycles (unchanged from round 1) | `head-suite-srp_top.log` |
| O7 dwell at head | `LEAVEALL_EMPTY dwell_ms=649 bound_ms=1200` | `head-suite-srp_top.log` |
| Committed campaign `tb/srp_top/mutants.py`, unmodified, pinned simulator, 14 partitions via `--only` | 56/56 arms KILLED by their required named assertions; 45/45 partition controls PASS; 49/49 assertion families K1–O8 covered; no cycle-budget exits; per-arm failure counts identical to the README table | `receipts/campaign-summary.txt`, `receipts/campaign/` |
| My round-1 probes (102 checks) at head | 102/102 PASS | `receipts/runs/head.r375.log` |
| Same probes on base RTL (counterfactual) | 20 FAIL (R1b, R1e): the #608 non-stop is reproduced | `receipts/runs/base.r375base.log` |
| New round-2 probes R8/R9 (parked-reservation release bounds) at head | 5/5 PASS | `receipts/runs/head.r375b.log` |
| My 11 round-1 mutants × (new full suite + probes) | all 11 fail the committed suite (10 in srp_top, 1 in srp_encoder O8); see Tests | `receipts/reviewer-mutants-summary.txt`, `receipts/runs/r-*.log` |
| Published parent replay re-run (`run_parent.py`, sources hash-verified) | original helper rc 1 (expected control), fixed rc 0, deadline oracle rc 0 at `00b5c6c9` | `receipts/parent-replay-rerun.log`, `receipts/parent-replay-rerun/` |
| Deadline oracle against base / head RTL | base rc 1 ("timer expiry prematurely aged registrar"); head rc 0, stops at −1/+1/+40/+80 ms and retains legitimate LV at +120/+199 ms | `receipts/parent-deadline-oracle-{base,head}.log` |
| Total DUT clocks of the full srp_top run | 103,847,705, against the new 200,000,000-clock budget | `receipts/runs/head.cyclecount.log` |
| `scripts/lint_hdl.sh` (pinned), `make links matrix modmatrix params`, `gen_matrix.py --check` | all rc 0 | `receipts/head-lint_hdl.log`, `head-make-*.log`, `head-gen_matrix-check.log` |
| `git diff --check 16be6768 HEAD` | rc 2: 26 trailing-whitespace and 5 blank-at-EOF hits, all in `tb/srp_top/mutations/` (23 of 56 patch files) | `receipts/git-diff-check.log` |
| Same check, excluding `tb/srp_top/mutations`; and `16be6768..cf4e5c63` | rc 0 for both | `receipts/git-diff-check.log` (see R2-F1) |
| Hosted checks at the exact head | 6 check runs, all executed and `success` (docs-gates, portability, suites, each under two triggers). None skipped. Zero legacy status contexts. Hosted CI does not run `git diff --check`. | `receipts/hosted-check-runs.tsv` |

The scripts are in `scripts/`:
- `prepare_trees.sh` extracts the trees;
- `run_suites.sh` runs the suites;
- `r375_campaign.py` partitions the committed driver and unions the coverage;
- `r375_run.py`, with `r375_probes.inc` and `r375_probes2.inc`, runs the reviewer probes and mutants.

## Round-1 findings: resolution at this head

**My R375-1 findings:**

| ID | Round-1 severity | Status at 00b5c6c9 | Evidence |
|---|---|---|---|
| F1 parent consumer gates | MAJOR | **RESOLVED** | See the note below the table. |
| F2 four surviving guards | MINOR | **RESOLVED** | `r-cancel-latch-dropped` fails O1, `r-cancel-consumes-new-intent` fails O2, `r-join-start-guard-dropped` fails O3/O4, and `r-sink-receive-priority-lost` fails O5. Each fails both in the committed campaign and in my own full-suite run with my own edit (`reviewer-mutants-summary.txt`). My probes R4–R7 still pass at head and catch the same edits. |
| F3(a) join coalescing | SUGGESTION | **RESOLVED** | `r-join-coalesce-dropped` fails O6 (`sim_main.cpp:1029`). |
| F3(b) MVRP/prepare arbitration | SUGGESTION | **RESOLVED** | `r-mvrp-start-during-prepare` survives srp_top (1987/1987) but fails encoder O8 (`tb/srp_encoder/sim_main.cpp:1229`): 3 O8 assertions and 2 B1-vlan with my own edit (`runs/r-mvrp-start-during-prepare.srp_encoder.log`). |
| F3(c) README count | SUGGESTION | **RESOLVED** | `tb/srp_stream_fsms/README.md:151-155`: 12/1203 and 12/1211, matching my campaign logs (control 1215). |
| F4 parent replay | SUGGESTION | **RESOLVED** | See the note below the table. |

- **F1 detail.** Manager comment 5862231642 reports 11/11 at parent dev `931f396e` with the gitlink at `00b5c6c9`. By inspection:
  - the multi-declarators are split (`tb/srp_top/sim_main.cpp:334-339`, `:726-727`, `:829-831`), and no multi-declarator remains in the added C++;
  - `mutants.py` public functions `:80`, `:89`, `:98`, `:131` are annotated and documented;
  - no line exceeds 120 columns;
  - there is no host timeout; a DUT-clock bound is at `sim_main.cpp:342-346`;
  - no source text is read for an oracle: `plant()` only copies and `git apply`s.
- **F4 detail.**
  - The manager decision is recorded on the issue (5861796018).
  - `reproduce.cpp`, `run_reproduction.py`, `reproduce-deadline.cpp`, `run_parent.py` and the patch are published with sha256 values that I recomputed and that match.
  - My re-run reproduces all three outcomes.
  - The deadline oracle discriminates: it fails on the base RTL.

**Other round-1 review (R374-1, PR comment 5861793313), read after my own verdict and ledger:**

| ID | Status at 00b5c6c9 | Evidence |
|---|---|---|
| F1 MAJOR (consumer gates) | **RESOLVED** | Same as my F1. |
| F2 MINOR (`my-join-edge-peer`, `my-cancel-eats-new-intent`, `my-reuse-flags-ignore-cancel`) | **RESOLVED** | Killed by O3/O4, O2 and O4 in my campaign re-run (`campaign-summary.txt`). |
| F3 SUGGESTION (canceled empty reservation holds a TX slot) | **RESOLVED (documented bound)** | See the note below the table. |
| F4 SUGGESTION (harness sources) | **RESOLVED** | Same as my F4. |
| F5 SUGGESTION (coalescing during wait) | **RESOLVED** | `my-drop-join-during-wait` fails O6. |

- **R374-1 F3 detail.**
  - `10_srp_engine.md:514-522` states the missing abort operation, the one-shared-standard-slot cost (1 of `TX_STD_SLOTS_P = 4`), and the MVRP-drain delay.
  - It gives the link-up bound (T-MRP-PERIODIC plus T-MRP-JOIN) and the link-down bound (next unsuperseded own action, at most T-MRP-LEAVEALL plus T-MRP-JOIN), states the unbounded repeated-cancellation case, and notes that reset clears the pool.
  - O7 pins the link-up case at 649 ms, and the `canceled-content-never-drains` arm fails O7.
  - My R8/R9 confirm the other two statements, as described under Robustness.

## Lens: Conformance — CLEAN

- **RTL unchanged.** Production RTL is byte-identical to round 1, so the round-1 `sLA` analysis stands:
  - expiry records intent only;
  - the preparation-acceptance or reuse edge is the single `sLA`, which ages registrars and starts both walks with `txLA!`;
  - receive priority holds on both planes;
  - LV + rLv, #108 and type scope are unchanged.
- **Base versus head.** Re-executed at this head, my probes still show:
  - early-window Leaves stop at head (R1);
  - base reproduces the #608 non-stop (20 failures);
  - a Leave after `sLA` keeps the documented LV path.
- **Parent proof.** The manager's accepted proof is the deadline-anchored oracle.
  - I ran the published harness myself. At deadline 14096 ms, a Leave at +1 ms clears ACTIVE for the whole 2000 ms hold, and renewal and no-renewal behave as documented.
  - The phase sweep stops at −1/+1/+40/+80 ms and retains legitimate LV at +120/+199 ms, after `sLA`.
  - Against base RTL, the same oracle fails at its first expiry-window assertion.
  - The original LV-anchored helper returns rc 1 as the disclosed control, matching the manager decision.
- **New tests.** The new tests observe behaviour that conforms to Table 10-5 and Δ13:
  - O3: a peer before or on the join opportunity supersedes the own action, and both planes stay IN;
  - O4: wire flags appear only with an uncanceled `sLA`;
  - O5: a sink-plane Lv on or before acceptance clears IN; after acceptance it retains LV.

## Lens: RTL — CLEAN

- **No production change.** `git diff cf4e5c63 00b5c6c9 -- hdl` is empty, so the round-1 RTL review (CLEAN) carries over unchanged.
- **Lint.** `scripts/lint_hdl.sh` passes with the pinned simulator.
- **pp_top.** Passes 7751/7751.
- **Test-only wrapper change.** `tb/srp_encoder/srp_tb_wrap.sv:35-37,114-117` connects `la_prepare_i`, `la_prepare_done_o` and `la_tx_o` to new wrapper ports, where they were previously tied off. `la_cancel_i` stays tied to 0. The other unit cases drive preparation low from `bring_out_of_reset()` (`tb/srp_encoder/sim_main.cpp:458`), so pre-existing cases are unaffected (562 = 556 + 6 O8 checks).
- **Documented slot facts match the RTL.**
  - The encoder requests a standard slot (`KL_srp_encoder.sv:264`); the pool has `TX_STD_SLOTS_P = 4` (`KL_pp_tx_slots.sv:44`).
  - MVRP drains need `E_IDLE` (`start1_w`).
  - The pool and the SRP engine share `rst_n` (`protocol_processor_top.sv:3888`).

## Lens: Robustness — CLEAN

**New round-2 probes** (`receipts/runs/head.r375b.log`):
- **R8, link down.** A canceled empty reservation parks at 14351 ms. With no link-up, it is released at 25400 ms by the next own `sLA`, 58 ms after the new expiry at 25342 ms. The dwell is 11049 ms, within T-MRP-LEAVEALL plus T-MRP-JOIN. That action puts exactly one flagged frame on the wire.
- **R9, link up at +3000 ms.** The reservation is released 49 ms after link-up, by content, with no own action and no flags.

These confirm the documented release bounds at `10_srp_engine.md:516-521`.

**Unbounded case.** The documented unbounded case (repeated peer cancellation on a down link) needs received MRPDUs while `link_up_i` is low. It is honestly stated as a limit, and the manager accepted "document the bound" as an alternative to releasing the handle.

**Round-1 races, still covered at head.** Probes R3–R7 pass: parked MVRP responsiveness, the join-start edge from −2 to +3, the sink edge, the encoder-busy cancel, and new intent during a canceled preparation. They are now also committed as O1–O5.

**Cycle budget.** The new DUT-clock budget is cumulative over one srp_top run. The full default suite uses 103.8 M of the 200 M clocks, so there is about 1.9× headroom. A hung mutant is reported UNPROVEN, never KILLED (`mutants.py:116-117`). This is conservative.

## Lens: Tests — UNCLEAN (R2-F1)

**What passes.**
- **Required cases (issue 127 comment 5861796018, item 2).** All are committed in the default suite and in the `guards` group (`tb/srp_top/sim_main.cpp:882-1070`):
  - O1: busy-encoder cancel;
  - O2: newer expiry during a canceled, blocked preparation;
  - O3: peer at join −1/0/+1, with the placement self-checked against the observed join clock;
  - O4: peer at reuse acceptance −1/0/+1, with the exact acceptance clock checked separately;
  - O5: Talker Advertise and Failed Lv at −1/0/+1 around acceptance on sinks 0 and 7.
- **Seven required reviewer mutants.** Each fails its named assertion and is recorded in `mutants.py` and in the README table (`tb/srp_top/README.md:274-326`). Per-arm failure counts in my re-run match that table exactly.
- **Earlier suggestions.** O6 pins coalescing; O7 pins the link-up drain; O8 pins the arbitration.
- **Round-1 counterparts.** `expiry-event` still fails 81 checks. `r-expiry-pulse-restored` now fails 95 checks in the full suite (K, L2, M7, M10, N1, N2, N11, O3, O5), and 62 in its phases group.
- **My full mutant set.**
  - Of my 11 round-1 mutants, 10 fail the new srp_top full suite (1987 checks).
  - The eleventh, `r-mvrp-start-during-prepare`, fails encoder O8.
  - None of my round-1 mutants now survives the committed suites.
- **Test hygiene.**
  - Event history is gated on `rst_n` (`sim_main.cpp:348-357`). This only excludes combinational acceptance strobes while the DUT is in reset; `reset-retains-intent` is still killed by K10.
  - The driver counts a kill only with a nonzero rc, a completed tally, no budget exit, and the arm's own named assertion.

**What fails.** R2-F1: the new patch inputs fail the repository's whitespace check (see Findings).

## Lens: Docs — CLEAN

- **`10_srp_engine.md:514-522`.** Every statement matches the RTL and my measurements: no abort operation, one standard slot, MVRP delay, the link-up and link-down bounds, the unbounded repeated-cancellation case, and reset.
- **`tb/srp_top/README.md`.**
  - The 1987-check count is exact.
  - The Round 2 section is accurate: 73 added checks, 7 controls, 56 arms, 49 families, `64 checks`, O7 measured at 649 ms, and per-arm failure counts and tags identical to my re-run.
  - The driver description at `:217-224` (patches applied in scratch; only logs read; DUT-clock budget; unproven is not a kill) matches `mutants.py`.
- **`tb/srp_encoder/README.md`.** The count of 562 and the O8 description match my run.
- **`tb/srp_stream_fsms/README.md:151-155`.** The counts are corrected, and the smaller mutated tallies are explained.
- **Docs gates.** They pass at head: `make links matrix modmatrix params` and `gen_matrix --check`.

## Findings

### R2-F1 — MINOR — lenses: Tests

- **Where:** `tb/srp_top/mutations/*.patch`, 23 of the 56 new files. Examples:
  - `talker-no-own.patch:6` (trailing whitespace);
  - `reserved-slot-not-reused.patch:11`, `already-full-missed.patch:11`, `leaveall-expiry-lost.patch:11`, `listener-sid-ignored.patch:11` and `r-expiry-pulse-restored.patch:36` (new blank line at EOF).
- **Authority/evidence:**
  - The manager's donor bank at this head is 8/9. Step 9, `git diff --check 16be6768 HEAD`, fails on these files (PR #130 comment 5862222946). The manager says "The next round fixes this".
  - I reproduced it independently, read-only on the clone: rc 2, with 26 trailing-whitespace and 5 blank-at-EOF hits across 23 patch files, and nothing outside `tb/srp_top/mutations/` (`receipts/git-diff-check.log`).
  - The same check is rc 0 at round 1 (`16be6768..cf4e5c63`) and rc 0 at this head when that directory is excluded.
  - The cause is unified-diff context lines for blank source lines, which are a single space. Where such a line ends a patch, git reports it as a blank line at EOF.
  - The manager's comment names only one EOF file; my count is five, with git 2.55.0.
- **Impact:** a required repository bank step fails at this head, so the PR does not meet the completion bar. There is no functional or RTL effect. Hosted CI does not run this check, so it passes.
- **Required outcome:** at a new head, `git diff --check 16be6768 <head>` exits 0 while the campaign stays 56/56 KILLED. The manager names two acceptable ways:
  - a scoped `.gitattributes` whitespace exemption for `tb/srp_top/mutations/*.patch`;
  - or patches regenerated without whitespace-only lines, which `git apply` accepts as empty context.
- **Verification:**
  - Run `git diff --check 16be6768 <new-head>` (rc 0).
  - Re-run `python3 tb/srp_top/mutants.py --output <dir>` (64/64, driver rc 0), or `scripts/r375_campaign.py` from this packet.
  - The manager's donor bank reports 9/9.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #127 body, the round-1 and round-2 assignments (5860872275, 5861796018) and the manager decision; 802.1Q Tables 10-4/10-5 and §10.7.9 as quoted in 10 §6.5; RTL unchanged since round 1 (empty `hdl` delta); probes R1–R7 at head vs base; published parent harness re-run plus the deadline oracle on base and head | R375-2 | 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c |
| RTL | CLEAN | empty `hdl` delta; `KL_srp_encoder.sv`/`KL_pp_tx_slots.sv`/`protocol_processor_top.sv` slot-class, pool-size and reset facts; `tb/srp_encoder/srp_tb_wrap.sv` port change; lint (pinned); pp_top 7751/7751 | R375-2 | 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c |
| Robustness | CLEAN | new probes R8/R9 (link-down and link-up release bounds); round-1 probes R3–R7; O1–O7 behaviour; DUT-clock budget headroom (103.8 M/200 M) | R375-2 | 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c |
| Tests | UNCLEAN (R2-F1 MINOR) | `tb/srp_top/sim_main.cpp` (O1–O7, budget, reset gating), `tb/srp_encoder/sim_main.cpp` O8, `tb/srp_top/mutants.py`, 56 mutation patches; committed campaign re-run (56/56, 45/45 controls, 49/49 families); 11 reviewer mutants × full suite and probes; 6 suites at head; `git diff --check`; manager comments 5862222946 and 5862231642 | R375-2 | 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c |
| Docs | CLEAN | `10_srp_engine.md:514-522`; `tb/srp_top`, `tb/srp_encoder` and `tb/srp_stream_fsms` READMEs against measured counts; `08_timing.md` values; `make links matrix modmatrix params`, `gen_matrix --check` | R375-2 | 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c |

## Real limits

- **Simulator path.** The requested path was absent. I used the byte-identical per-head wrapper (Verilator 5.050), as recorded above.
- **Campaign partitioning.** I ran the committed driver in 14 `--only` partitions, to keep each foreground command bounded. The committed driver computes family coverage only for an unpartitioned run, so the 49/49 coverage is my union across partitions (`scripts/r375_campaign.py`). The author reports the unpartitioned run as `64 checks: 64 PASS`.
- **Parent gates and banks.** I did not run the parent consumer gates, the donor bank, or any full parent/PP/gPTP/Yosys/builder bank. For those I rely on manager comments 5862231642 (11/11) and 5862222946 (8/9); I reproduced the failing step 9 independently.
- **Documentation gates.** `make lint`, `wavedrom-check` and `stale` were not run, because they need diagram tooling or git metadata in the extraction. This round changes no diagram, and the hosted docs-gates jobs succeeded at this head.
- **Scope of the parent replay.** The replay measures the SRP ACTIVE licence in simulation. It has no AVTP framer and no hardware.
- **Hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof. No bench disconnect or STREAM_STOP measurement was done.
- **Time scale.** The testbench runs at 40 clocks per tb-ms. The residual window from `sLA` to the wire (457 cycles) and the probe phase offsets are simulation-scale.

## Pending manager duties

1. Close R2-F1: confirm `git diff --check` and the donor bank at 9/9 at the next head, and re-run the consumer set there.
2. Build and gate the final current-dev candidate at the merge turn. This is distinct from the source validation here: source base `16be6768`, live dev `931f396e`.
3. Own hosted/act acceptance. All 6 hosted runs at this head executed and succeeded.
4. Parent pin adoption, with the CRF frame/STREAM_STOP integration regression required by the issue.
5. Schedule the bench re-measurement for #608 (100/100 disconnects stop).
6. Archive the harness sources, as already assigned.

R375-2 FINISHED
