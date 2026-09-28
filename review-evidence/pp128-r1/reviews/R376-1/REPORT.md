[R376] NEGATIVE - exact head 9476898b28ffc8f77b2aa5f873f3899a17287d3a

# R376-1 independent review: processor PR #129 / issue #128

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head `9476898b28ffc8f77b2aa5f873f3899a17287d3a`, tree `0a41c0be33df4fa4113f2c4ac752e7a976487369` (verified in the review clone)
- Base `16be6768f710e79450aace277abacd6c2c3336e5` (one commit, `main` = the parent's current pin)
- Round R376-1, internal reviewer, cleared context, own detached clone

## Verdict

**NEGATIVE.** The retry design is sound. I independently confirmed that enabled `NO_DA` sources get paced (100 ms), rotating reattempts. The parent first-probe claim reproduces both ways. All 11 ACMP/MAAP/SRP/integration suites pass. The author's 28-mutant matrix reproduces exactly.

However, four findings at MINOR or above remain open:

- Two consumer-gate failures are attributable to this head and verified independently (F1, F2).
- A parent test-evidence ratchet is exceeded by the new mutation runner (F3).
- Non-equivalent mutants of acceptance-relevant behaviour survive both the talker and the full integration suite (F4). Four were found in my own pass. Four more were verified after reading the concurrent report: one starves solicited commands, and three were pinned by the base suite.

## What was reconstructed

1. **Rules and docs.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`, so the rules come from `README.md` and `docs/README.md`: the single-source rules for `T-`/`P-` IDs and the `make check` gate.
2. **Scope.** Issue #128 body. The manager's assignment comment (issuecomment-5861093499) gives the frozen decisions: bounded fair reattempts, honest failure, no retry storm, no starving of commands, no conflict/PCP backoff change, no interface change, and "record what the parent test needs".
3. **Parent analysis.** kebag-logic/milan-fpga#606 and its analysis comment 5860869610.
4. **Parent consumer code (read-only, dev `931f396e`).**
   - `hdl/milan/KL_pp_maap_shim.sv`, whose sha256 `965fbee0…` equals the author receipt.
   - `tb/verilator/pp_shadow/sim_main.cpp` case `[H]`.
   - `scripts/measure_test_evidence.py` with its two helper modules.
5. **Diff and history.** `git diff 16be6768..9476898b`: 10 files, +680/−63.
6. **Public evidence.** `review-evidence/pp128-r1` at milan-fpga `b367df5d`: 48 files, all under `author/`. All 48 published hashes verify.
7. **Manager receipts on the PR.** Comments 5861504990 and 5861562548 (parent consumer gates at this head: 8 of 11 pass, 3 fail).
8. **Hosted checks at the exact head.** Six executed jobs, all `success`: `suites`, `docs-gates` and `portability`, each in two runs (36363095702 and 36363093608). No skipped contexts are listed. The legacy combined status has no contexts.

## Independent results (receipts under `receipts/`)

| Evidence | Result |
|---|---|
| `suites-head.txt` | ACMP talker 1107, listener 2544, NVM 349, lsn_admit 18, MAAP 75, SRP admission 991231, decoder 190, encoder 556, stream FSMs 1087, SRP top 1531, `pp_top` 7751: **all PASS, 0 failing** (pinned Verilator 5.050, ≤ 8 build jobs) |
| `lint-head.txt` | zero-warning lint of `KL_acmp_talker` and `protocol_processor_top`: 0 findings; `make check` rc 0; matrix 92 rows, 0 untested |
| `author-mutants-rerun.txt`, `author-mutants-coverage-rerun.txt` | author runner re-executed: 28/28 killed with assertion failures; baseline and restored rc 0; 38/38 sites witnessed; coverage identical to the published file |
| `own-mutant-no-round-pptop.txt` | removing the retry round fails `pp_top` S10 and MP3 (integration pins the fix) |
| `parent-harness-reconstructed.txt` | published harness source + unmodified parent shim + reviewer-reconstructed top (`harness/first_probe_top.sv`). Head + fixed oracle: **PASS** (first probe status 0, DA 91e0f0006818). Base + original oracle: PASS (status-3 defect reproduced). Head + original: FAIL "unexpected retry"; base + fixed: FAIL "automatic retry sweep missing". The talker sha256 `7a242dc7…` equals the author receipt. |
| `own-mutants-talker.txt` | 17 reviewer mutants on the talker suite: 7 killed, 10 survived |
| `own-mutants-survivors-talker-pptop.txt` | m01, m02, m07, m17 also survive the full `pp_top` suite (7751/7751) |
| `own-mutants-demand-head.txt`, `own-mutants-demand-base.txt`, `own-mutants-demand-pptop-a.txt`, `own-mutants-demand-pptop-b.txt` | m19–m22 survive the head talker and `pp_top` suites; m20–m22 are killed by the base talker suite (I4, I3, E3) |
| `probes-head-base.txt`, `probes-vs-mutants.txt` | reviewer probes P1–P3 and P5 pass at head and kill m01, m02, m07, m17 and m19. The other six survivors (m03, m04, m05, m10, m11, m13) pass every probe; I judge them equivalent or masked by redundant guards. The base passes P1/P2/P5 and fails P3b. P4 records the `[H]` mechanism (head 0 vs base 1 probe-caused `ALLOC_DA` in the same round). |
| `use-before-decl.txt` | head: `set_conflict_w` referenced at `KL_acmp_talker.sv:891`, declared at `:1110`; base: none |
| `parent-evidence-rules.txt` | the parent gate's own detectors flag `tb/acmp_talker/retry_mutants.py` as wall-clock dependent and as a DUT-source reader with no disposition; the existing `tb/pp_top/name_wr_mutant.py` is not wall-clock dependent and has a recorded disposition |
| `clone-integrity.txt` | review clone at exact head/tree, detached, index = tree, every worktree blob re-hashes equal, no untracked/ignored files, 0 gitlinks in this repository |

## Findings

### F1 — MAJOR — Identifier used before its declaration in the edited talker (RTL)

- **Where.** `hdl/acmp/KL_acmp_talker.sv:891`: `if (!cfg_src_en_i[i] || !en_q_r[i] || set_conflict_w[i])` in `always_ff retry_round` (added by this PR). The declaration of `set_conflict_w` is at `:1110`.
- **Authority and evidence.**
  - SystemVerilog requires a simple identifier to be declared before it is referenced. The parent's Vivado elaboration gate enforces this (VRFC 10-3380).
  - The manager's consumer receipt (PR comment 5861504990 item 1, clarified in 5861562548) shows this is the only new `xvlog` finding on this PR.
  - My own scan (`use-before-decl.txt`) finds it at head and nothing at base.
  - Verilator and the processor's own lint accept it, which is why the processor's gates are green.
- **Impact.** The parent's `scripts/xvlog_gate.py --check` fails once the pin moves. The RTL does not elaborate cleanly in the parent's FPGA toolchain.
- **Required outcome.** Declare `set_conflict_w` (or the whole `pe_sets` signal group) before `retry_round`, or move `retry_round` below `pe_sets`, with no behaviour change.
- **Verification.** `use_before_decl.py` reports nothing for the talker. The parent `xvlog_gate.py --check` is back within its ratchet (4 pre-existing findings). All talker and integration suites stay green.

### F2 — MAJOR — Probe-triggered allocation is now deferred to the next round; the parent `pp_shadow [H]` consumer gate fails and the change is not recorded for the consumer lane (Conformance, Docs)

- **Where.**
  - `hdl/acmp/KL_acmp_talker.sv:455`: `init_ready_w` masks `retry_wait_r`.
  - `:894-895`: an `ALLOC_DA` attempt sets `retry_wait_r`.
  - `:1145`: a PROBE_TX in `NO_DA` only sets `pe_init`.
  - `docs/architecture/05_acmp_engine.md:412-413`: "one attempt per source per round … including probe/listener-triggered requests".
  - Parent `tb/verilator/pp_shadow/sim_main.cpp:1864-1875` at dev `931f396e`.
  - Author handoff, "Parent harness result and consumer work" (line 195).
- **Authority.**
  - The assignment's decision says "Record what the parent test needs, and do not edit the parent."
  - The issue's scope requires honest failure with no interface change, and the parent's consumer gates must hold on pin adoption.
  - The manager's receipt (5861504990 item 2) reports `[FAIL] the processor ASKED and the shim ACCEPTED — no request seen`.
- **Evidence.**
  - Case `[H]` snapshots the shim's accept count, injects one PROBE_TX while no block is claimed, runs 4000 cycles, and requires at least one new `ALLOC_DA`.
  - My probe P4 reproduces that shape on the talker bench: a refused startup attempt, then a PROBE_TX in the same round.
    - Head: 0 probe-caused `ALLOC_DA` requests (status 3 answered), then 8 once one round elapses.
    - Base: 1 request at once.
  - So the behaviour the parent test encodes (a probe re-asks at once) was deliberately changed. The PR records only that the consumer regression needs "the 100 ms plus sweep acquisition allowance". It does not mention that this existing parent case will fail, or why.
- **Impact.** The pin cannot be adopted: a parent consumer gate is red. The consumer lane has no recorded reason or instruction for reconciling it.
- **Second parent case.** The concurrent R377-1 report adds that the parent's crf build also fails `[I]` "granted DA == KL_maap base + source index". I confirmed the mechanism in the parent source only: `sim_main.cpp` `[I]` compares the *last* grant with source 0's address. With two outputs now auto-acquired, the last grant is source 1's. I have not seen that build's log. It is retained here as part of the same reconciliation.
- **Required outcome.** Reconcile explicitly, in one of two ways:
  - (a) keep the pacing, and record in the PR evidence (and in 05 §6bis or the integrator guide) that a probe no longer causes an immediate `ALLOC_DA` within the round of a prior attempt. State exactly what `[H]` must observe instead: for example, advance parent time by one `T-ACMP-DA-RETRY` round, or count the next round's attempt.
  - (b) allow a bounded probe-triggered attempt, which would also need the pacing tests updated.
- **Verification.** The manager's pin-adopting candidate shows `pp_shadow` `[H]` green, with the reason recorded publicly. The talker suite pins whichever behaviour is chosen.

### F3 — MINOR — The new mutation runner exceeds two parent test-evidence ratchets (Tests)

- **Where.**
  - `tb/acmp_talker/retry_mutants.py:59`: `subprocess.run(..., timeout=900, ...)` is a host wall-clock deadline.
  - `:86`: `rtl.read_text()` reads DUT source, and the parent's `DUT_READER_DISPOSITIONS` has no entry for it.
- **Authority and evidence.**
  - Parent `scripts/measure_test_evidence.py --check` fails with "4 wall-clock-dependent suite file(s) > ratchet 3" and "1 unexplained DUT-source reader(s) > ratchet 0" (manager receipt 5861504990 item 3).
  - I re-applied the parent gate's own detector functions to the head's files (`parent-evidence-rules.txt`): `retry_mutants.py` gives `wall_clock=True dut_source_reader=True disposition=NONE`.
  - The processor's existing `tb/pp_top/name_wr_mutant.py` uses no wall-clock deadline.
- **Impact.** Another consumer gate fails on pin adoption. Mutation evidence whose verdict could depend on host load is counted as non-deterministic.
- **Required outcome.**
  - Remove the subprocess wall-clock deadline (the suite is cycle-bounded).
  - Supply the one-line disposition text for the parent's DUT-reader table (a mutation campaign that plants its named defects in a scratch copy and requires assertion failures), so the pin-adoption lane can record it.
- **Verification.** Parent `measure_test_evidence.py --check` passes on the pin-adopting candidate, and `retry_mutants.py` still kills all 28 mutants.

### F4 — MINOR — Acceptance-relevant behaviour is unpinned: eight non-equivalent mutants survive every suite (Tests)

- **Where.**
  - `hdl/acmp/KL_acmp_talker.sv:890-893`: the conflict and enable/disable clears of `retry_wait_r`, which implement 05 §6bis "Initial enable and conflict start a new acquisition lifetime".
  - `:594-597`: the `txn_eligible_w` terms, which implement "Commands and pending events alternate when both are present".
  - Three demand-driven allocation arcs that the base suite pinned: the probe arc `:1145`, the listener arc `:843` and the backoff-exit arc `:815`.
  - No check in `tb/acmp_talker/retry_cases.hpp` or `tb/pp_top/sim_main.cpp` depends on any of these.
- **Authority.**
  - The assignment says "every new check is pinned by a killed mutant (plant your own too)".
  - The issue requires "no change to the conflict … backoff" and "no starving".
- **Evidence.** These mutants pass the talker suite (1107/1107) and `pp_top` (7751/7751):
  - `m01` drops the conflict clear.
  - `m02` drops the enable/disable clear.
  - `m07` drops `pe_rel_r` from eligibility.
  - `m17` keeps only the INIT term.

  Yet they change observable behaviour, which my probes show:
  - P1: at base and head, a `DA_OK` conflict reallocates at once. Under m01 it waits up to a full round, a latency regression on the conflict path.
  - P2: a source disabled and re-enabled within the round of its last attempt allocates at once. Under m02 it waits.
  - P3b: an owed `RELEASE_DA` is offered while commands are continuous. Under m07 and m17 it starves, as it did at base.

  Added after reading the concurrent R377-1 report, and independently re-verified here (`own-mutants-demand-*.txt`, `probes-vs-mutants.txt`):
  - `m19` removes `maap_avail_w &&` from the INIT eligibility term. It survives the talker and `pp_top` suites. My probe P5 shows that while an accepted allocation is unanswered and other sources have retries pending, the second consecutive command is never consumed. That violates the frozen "no starving of solicited commands" property. The head passes P5.
  - `m20`, `m21` and `m22` remove the probe, listener and backoff-exit re-allocation requests. All three survive the head talker and `pp_top` suites. All three were killed by the base suite (I4, I3, E3): the new time steps land on retry-round boundaries and mask them.
- **Impact.** A later edit can silently regress any of the following with every suite green: command service under a hung allocator, conflict re-allocation latency, the re-enable path, release fairness, or the demand-driven allocation arcs. The last group is coverage this PR removed.
- **Required outcome.** Add port-level checks equivalent to P1, P2, P3b and P5, and restore demand-arc checks that do not coincide with a retry boundary. Add m01, m02, m07, m17 and m19–m22 to `retry_mutants.py` as named mutants so that all eight are killed.
- **Verification.** Re-run `scripts/own_mutants.py` (or the extended author runner): all eight are killed, and baseline/restored stay green.

### Suggestions (do not affect the verdict)

- **S1 (Tests, Docs).** The parent-harness claim reproduced only after I reconstructed the missing glue: the driver `run_first_probe.py` and the top that exposes `block_valid_i`. Neither is in the public packet or attached to #606. My reconstruction is `harness/first_probe_top.sv` plus `run_first_probe_reconstructed.sh`. Publish the original driver and wrapper with the evidence.
- **S2 (Docs).** Two comments are stale:
  - `tb/acmp_talker/sim_main.cpp:957` still says "dispatch outranks the pending-init flag".
  - The `MAAP_RSP_MS_P` rationale at `hdl/acmp/KL_acmp_talker.sv:174-179` says an allocation is "normally [requested by] the PROBE_TX that pinged the source". It is now normally the retry round.
- **S3 (Docs).** 05 §6bis repeats the value "100 ms" beside `T-ACMP-DA-RETRY` (lines 412, 434, 440), against the docs/README single-source rule (02 has precedent). F05.12 shows no `NO_DA` retry arc.
- **S4 (Robustness).** Retries now depend on a running `now_ms_i`. If the millisecond timebase is stalled, then after one refused attempt no further attempt occurs, not even on a probe (the base re-asked on every probe). State this dependency in the integrator guide.

## Other public review findings at this head

This PR had no public review findings before this round. The concurrent external report R377-1 (PR comment 5861647041, same exact head) was posted during this round. I read it only after my verdict, findings F1–F4 (without the later F4 extension) and ledger were written. Each of its findings is resolved against this head below:

| R377-1 finding | Disposition at 9476898b |
|---|---|
| F1 use before declaration (MINOR there) | **Retained** as my F1. I rate it MAJOR because the parent FPGA elaboration gate fails on the edited RTL. |
| F2 `retry_mutants.py` breaks parent evidence rules | **Retained** as my F3 (same MINOR). |
| F3 five non-equivalent survivors (`init_elig_no_avail`, `no_conflict_wait_clear`, `no_probe_initset`, `no_lsn_initset`, `no_backoff_exit_initset`) | **Retained** and merged into my F4. I independently re-planted all five as m19, m01, m20, m21 and m22: all survive the head talker and `pp_top` suites, m20–m22 are killed at base, and m19 is killed by my probe P5. |
| F4 undeclared consumer-visible behaviour change (`[H]`; `[I]` in crf) | **Retained** as my F2. The `[H]` mechanism is verified by P4; the `[I]` mechanism is confirmed from parent source only. |
| S1–S3 | Consistent with my equivalent-mutant set and suggestions S1–S2. No change to the verdict. |

## Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | Issue #128 decisions; Milan §4.3.3.1 / §5.5.4.1 behaviour (honest status 3, no declaration without ownership, freshness); IEEE 1722-2016 Annex B paced refusals (internal allocator `KL_pp_maap.sv` and parent shim refuse in one cycle, no wire traffic); unchanged ports and parameters of talker and top; parent `[H]` consumer contract | R376-1 | 9476898b28ffc8f77b2aa5f873f3899a17287d3a |
| RTL | UNCLEAN (F1) | `KL_acmp_talker.sv` full read (retry round, rotating picker, command/event alternation and ready/valid independence vs the top scoreboard loop, obsolete-grant kill, stale credits, S_EV_MAAP bounds); lint 0; use-before-declaration scan | R376-1 | 9476898b28ffc8f77b2aa5f873f3899a17287d3a |
| Robustness | CLEAN | Pacing (1 attempt/source/round, R2/R7), disabled and out-of-block sources, absent and silent allocators (R3/R5), wrap (R5/R8), command gap ≤ 1088 cycles (R3), backoff untouched (R6), release under continuous commands (P3), kill paths (m03/m04/m05/m10/m11/m13 masked); S4 only | R376-1 | 9476898b28ffc8f77b2aa5f873f3899a17287d3a |
| Tests | UNCLEAN (F3, F4) | `retry_cases.hpp` R1–R8, `pp_top` MP3/S10, author 28-mutant rerun, 22 reviewer mutants (head, base, `pp_top`), probes P1–P5, reconstructed parent harness four ways, 11 focused suites | R376-1 | 9476898b28ffc8f77b2aa5f873f3899a17287d3a |
| Docs | UNCLEAN (F2) | 02 §4.2, 05 §6bis, 08 F08.1 `T-ACMP-DA-RETRY`, talker/`pp_top` READMEs, RTL banners, author handoff; `make check` rc 0; S2/S3 | R376-1 | 9476898b28ffc8f77b2aa5f873f3899a17287d3a |

## Real limits

- **Pinned tool.**
  - The assignment named `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`, but that path does not exist.
  - I first used the manager's same-head wrapper under `pp128-manager-9476898b`. Mid-review, another process overwrote that file with unrelated text; I did not modify it.
    - The concurrent R377-1 report discloses and explains that overwrite (about 03:00:48–03:01:14 CEST) and its byte-exact restore. The file now hashes to `905795b9…` again.
    - My one run inside that window produced build failures with no tally; I discarded it and did not count it.
  - Every published receipt was regenerated with a scratch copy of the byte-identical 372-series wrapper (sha256 `905795b9…`, reporting `Verilator 5.050 2026-07-01 rev v5.050`, executable sha256 `44898b22…`).
- **Parent gates not run by me.** I did not run the parent's `xvlog`, `pp_shadow` or evidence banks (not permitted). For F1–F3 I verified the mechanism independently (source scan, the parent gate's own detector functions, the talker-level P4 probe), but the gate results themselves are the manager's receipts.
- **Parent harness.** It was reproduced with a reviewer-reconstructed wrapper, not the original driver. Its millisecond jump (100 → 10000 ms) proves recovery after the bound, not the bound's tightness. The exact 100 ms boundary is proven by R1/R8 and was re-verified here.
- **No manager bank receipts in the packet.** The public evidence packet contains author material only. The statement that the manager's source static/builder and native banks passed at this head rests on the assignment, not on a receipt I could read.
- **Not run by me.** The full processor suite sweep (33 suites), Yosys portability and the builder bank.
- **Writes outside the packet.** Two small transient files (a `make check` log and a file list) were written to `/tmp` and deleted. The review clone was never written; it re-verified clean at the end (`clone-integrity.txt`).
- **No hardware.** Physical calibration was NOT RUN, and no bench, hardware or field result exists for this head. Field skips are not hardware proof.

## Pending manager duties

- Run the parent consumer gates again on the next pin-adopting candidate (`xvlog_gate`, `pp_shadow` `[H]`, `measure_test_evidence`) and publish the receipts.
- Record the parent `[H]` reconciliation and the `retry_mutants.py` disposition in the pin-adoption lane.
- Build the final current-dev candidate at the merge turn (source base `16be6768`, live dev `931f396e`).
- Own hosted/act acceptance and the parent MAAP-shim integration regression.
- Re-measure the first bind on the bench after pin adoption; physical calibration is still NOT RUN.

R376-1 FINISHED
