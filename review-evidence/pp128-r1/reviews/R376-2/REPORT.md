[R376] POSITIVE - exact head cc7c911e933aed4bfc9324eb5da473ae73bef618

# R376-2 independent review: processor PR #129 / issue #128, round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head `cc7c911e933aed4bfc9324eb5da473ae73bef618`, tree `3eff9b9f986b34ca2aec3e6c1b8387090978d88b`, verified in the review clone (`receipts/clone-integrity.txt`)
- Base `16be6768f710e79450aace277abacd6c2c3336e5`. Round-2 delta: `9476898b..cc7c911e`, one commit
- Round R376-2, internal reviewer, cleared context, own detached clone. Review start: PR comment 5862463405

## Verdict

**POSITIVE.** All five round-2 requirements (issue #128 comment 5861952375) are met at this head. Every round-1 finding from both reviews is resolved. No MINOR or higher finding is open. Three suggestions are recorded; they do not affect the verdict.

1. **Declaration order.** `set_conflict_w` and its group are now declared at `hdl/acmp/KL_acmp_talker.sv:878`, before `retry_round` (`:885`).
   - My declaration-order probe reports 0 findings at head, 1 at `9476898b`, 0 at base (`receipts/decl-order-probe.txt`).
   - The manager's parent `xvlog_gate.py --check` at this head passes with the 4 pre-existing findings. None of them is in the talker.
2. **Paced-round semantics are documented.**
   - 05 §6bis: "Allocation recovery" and "Consumer-visible timing change".
   - 02 §4.2 states the round semantics and that probes no longer force an immediate `ALLOC_DA`.
   - The PR body and the round-2 handoff name `pp_shadow [H]` and `[I]`, why each changes, and exactly what each must observe.
   - I checked both texts against the parent test source at `931f396e`. They match the manager's failure receipt at this head: `[H]` fails in base, vid73 and crf; `[I]` "granted DA" fails in crf.
3. **Mutation runner.** `retry_mutants.py` has no host deadline (`subprocess.run` with no `timeout`), and the DUT-reader disposition line is supplied.
   - The manager's evidence check at this head passes the wall-clock ratchet (3 ≤ 3).
   - The only remaining item is the missing parent-table row, which belongs to the pin-adoption lane.
4. **Round-1 probes and mutants are now committed regressions.**
   - Every non-equivalent round-1 mutant from my set fails a named assertion in the committed suite: m01, m02, m04–m22.
   - That includes the response-budget starvation mutant (m19 → R9) and the three demand-path mutants (m20–m22 → R12 arcs 0/1/2).
   - My probes P1, P2, P3b and P5 pass at head.
5. **Redundant terms.** The `!en_q_r[i]` term is removed. I checked its equivalence argument by construction. The four equivalent controls are stated with arguments; each is trace-identical to head across 300 randomized seeds.

## Reconstruction (in order)

1. **Rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md`, `docs/README.md` (single-source rules for `T-`/`P-` IDs, the `make check` gate) and `hdl/README.md` (tool floor, testbench and citation rules).
2. **Scope.**
   - Issue #128 body: the frozen acceptance.
   - Assignment 5861093499: bounded fair retries, honest failure, no storm or starvation, no backoff change, no interface change.
   - Round-2 assignment 5861952375: option (a), paced rounds kept; requirements 1–4 plus the S1 disposition.
   - Manager PR comments 5861504990, 5861562548 and 5862432079 (9 of 11 consumer gates pass at this head).
3. **Authorities.**
   - Processor 02 §4.2, 05 §6bis (F05.12), 08 F08.1 (`T-ACMP-DA-RETRY`), and the integrator and operator guides.
   - Parent `hdl/milan/KL_pp_maap_shim.sv` and `tb/verilator/pp_shadow/sim_main.cpp` at `931f396e`, read-only (hashes in `receipts/inputs.txt`).
4. **Diff and history.**
   - Full diff `16be6768..cc7c911e`: 12 files, +1098/−80. The only HDL file is the talker.
   - Round-2 delta: the declaration move, removal of the `!en_q_r[i]` term, and comments. Tests, runner and docs grew.
5. **Public evidence.**
   - `review-evidence/pp128-r1` at milan-fpga `b367df5d` is the round-1 author packet: 48 of 48 hashes verify.
   - The round-2 author packet (`author-r2`, [A399], at head `cc7c911e`) is on the same evidence branch at `938a9bcb`: 93 of 93 hashes verify.
   - The manager's consumer receipts at this head are read-only excerpts in `receipts/manager/`.
6. **Prior public findings.** I read R376-1 and R377-1 only after my own independent pass over the diff (RTL, docs, tests, runner). They are resolved below.

## Independent results (receipts under `receipts/`)

| Receipt | Result |
|---|---|
| `suites-focused-head.txt` | 14 suites at head with pinned Verilator 5.050 and ≤ 8 build jobs, all rc 0: `acmp_talker` 1172, `acmp_listener` 2544, `acmp_nvm` 349, `maap` 75, `pp_top` 7751, `srp_decoder` 190, `srp_encoder` 556, `srp_stream_fsms` 1087, `srp_top` 1531, `srp_admission` 991231, `scoreboard` 3705, `dispatch` 211, `timer_service` 48, `lsn_admit` 18 |
| `lint-acmp_talker-head.log`, `lint-hdl-head.txt`, `make-check-head.txt` | talker lint rc 0; `scripts/lint_hdl.sh` rc 0 (includes the top); `make check` rc 0 (41 Mermaid, 18 WaveDrom, 921 links, matrices, parameters); `gen_matrix --check` rc 0 (92 rows, 0 untested) |
| `decl-order-probe.txt` | used-before-declaration scan of the talker: head 0, round-1 head 1 (`set_conflict_w` 891/1110), base 0 |
| `author-campaign/driver.txt`, `author-campaign/logs/*`, `author-campaign/logs-vs-published.txt` | author runner re-executed at head: 56 killed, 4 equivalent controls, baseline and restored 1172/1172 rc 0, 50/50 sites witnessed. All 63 logs, `coverage.txt` included, are **byte-identical** to the published round-2 logs. The README table counts match the rerun exactly. |
| `own/own-mutants-r2-talker.txt` | my 31 mutants against the committed talker suite: **26 killed**, each by a named assertion. The 22 round-1 mutants were re-anchored; only m01/m02 needed new anchors. m03 survives; it is the author's declared equivalent `accept_kill_no_disable`. The new m27–m30 survive (S1, S2; m30 is discussed under S2). |
| `own/own-mutants-r2-pptop.txt` | `pp_top` still kills the no-round defect by name (S10, MP3). m27 survives `pp_top` too. |
| `own/probes-vs-mutants-r2.txt` | probes and a randomized differential run (300 seeds, about 105k commands) at head and under 15 mutants; details below |
| `parent-first-probe-replay.txt` | the published original driver and wrapper, the unchanged parent shim (sha256 `965fbee0…`) and the published fixed oracle. Head: **PASS**, first probe status 0, DA `91e0f0006818`, talker sha256 `a963c288…` (equal to the author's receipt). Base: **FAIL** "automatic retry sweep missing". Round 1 needed a reconstructed wrapper; this round's replay needs none. |
| `interface-identity.txt` | talker parameter/port header identical to base with comments stripped (87 lines). Only `hdl/acmp/KL_acmp_talker.sv` changed under `hdl/`. |
| `hosted-checks.txt` | six executed hosted jobs at the exact head, all `success`: `suites`, `portability` and `docs-gates` in runs 36370331782 (pull_request) and 36370328544 (push). No skipped contexts. The legacy combined status has 0 contexts. |
| `clone-integrity.txt` | clone at exact head and tree, detached. Index tree equals HEAD tree. No untracked or ignored files. All 251 tracked blobs re-hash equal with correct modes. 0 gitlinks: this repository has no submodules. |

### Probe and differential results at head (`own/probes-vs-mutants-r2.txt`)

**Round-1 probes.** P1 (DA_OK conflict reallocates at once), P2 (re-enable in the same round allocates at once), P3a/P3b (owed release served under continuous commands) and P5 (consecutive commands during a silent accept) all PASS.

**P4, the parent `[H]` shape.** Head: 0 probe-caused `ALLOC_DA` in the same round, then 8 after one round. This is the documented option-(a) behaviour.

**New probes.**
- P7: an absent allocator gets one offer per source per round (8, then 0, then 8).
- P9: same-round probes against an absent allocator cause no re-offer.
- P8 (behaviour record): a probe for source 1 creates no allocation for source 0.

**Randomized differential run.** It drives every documented input at random:
- exact-edge disable pulses and conflicts;
- 1–6-cycle and late (past `P-MAAP-RSP-MS`) allocator answers;
- ready stalls, probes and GET_TX_STATE, listener and PCP changes, expiries;
- time jumps across rounds.

Over 300 seeds and about 105,000 commands it checked two invariants, with 0 violations:
- I1: no SUCCESS answer or gate-open ever carries a DA granted to a different source.
- I2: every command is consumed within `P-MAAP-ACCEPT-CYC + 64` cycles.

**Mutants under the differential run.**
- The four declared equivalents (`accept_kill_no_disable`/m03, `no_sticky_gp_window`, `accept_kill_zero`, `kill_no_pending_conflict`) produce **port traces identical to head on all 300 seeds**.
- m29 is also trace-identical.
- m01, m02, m07, m17 and m19 fail the named round-1 probes again.

## Round-1 findings: resolution at this head

| Finding | Disposition at cc7c911e |
|---|---|
| R376-1 F1 (MAJOR) = R377-1 F1: use before declaration | **Resolved.** Declarations moved to `:878`. Probe: 0. Manager xvlog: PASS, 4 pre-existing findings only (`receipts/manager/manager-receipt-excerpts.txt`). |
| R376-1 F2 (MAJOR) = R377-1 F4: consumer-visible change, `[H]`/`[I]` | **Resolved** per the manager's option-(a) decision. Documented in 05 §6bis (`:412-458`) and 02 §4.2 (`:264-271`). The PR body and handoff give the exact `[H]` and `[I]` observations. The mechanism is confirmed by P4 and by the parent source. The parent test edits and reruns belong to the pin-adoption lane. |
| R376-1 F3 (MINOR) = R377-1 F2: mutation runner vs parent evidence rules | **Resolved.** No host deadline. The disposition line is in the PR body and handoff. Manager receipt: wall-clock 3 ≤ 3. Author receipts: rc 1 without the proposed row and rc 0 with it. |
| R376-1 F4 (MINOR) = R377-1 F3: unpinned behaviour | **Resolved.** Committed-suite kills by named assertion: m01 (R10 conflict), m02 (R10 re-enable, R15), m07 (R11 owed release), m17 (R11 disable), m19 (R9), m20/m21/m22 (R12 arcs 0/1/2). R377-1's five mutants carry the same names in the author campaign and are killed in my rerun. |
| R376-1 S1 = R377-1 S2: missing harness glue | **Resolved.** The original driver and wrapper are published, and my replay uses them unchanged. |
| R376-1 S2 = R377-1 S3: stale comments | **Resolved.** `KL_acmp_talker.sv:174-179`, `sim_main.cpp:957` and operator guide `:282` are updated. |
| R376-1 S3: F05.12 arc; value beside the T-ID | **Resolved.** `NO_DA --> NO_DA: T-ACMP-DA-RETRY` arc added. 05 cites the ID; the value appears only in F08.1. |
| R376-1 S4: running timebase | **Resolved.** Stated in `docs/guides/integrator.md:44-47`. |
| R377-1 S1: redundant or race-only terms | **Resolved.** Race terms are pinned by R13–R15: m04, m05, m10, m11, m13 are killed. Four terms are stated as equivalent controls, with arguments I verified. `!en_q_r[i]` is removed. |

## Findings

No finding at MINOR, MAJOR or BLOCKER severity is open.

### S1: SUGGESTION. Absent-allocator demand pacing is not pinned (Tests)

- **Where:** `hdl/acmp/KL_acmp_talker.sv:901-902`. The pacing bit is charged when the request is offered, so an abandoned offer is paced like a refusal (`:1036-1037`).
- **Authority / evidence:**
  - 05 §6bis `:413-415`: "One attempt per source per round … including probe/listener-triggered requests".
  - Reviewer mutant m27 charges the bit on accept instead of on offer. It survives the talker suite (1172/1172) and `pp_top` (7751/7751).
  - Probe P9 kills it. With an absent allocator (ready tied low), three same-round probes cause 3 re-offers under m27 and 0 at head.
- **Impact:** a regression would revert only the broken-allocator path to base behaviour (one 1024-cycle offer per probe). Commands stay within budget, and no acceptance item of #128 changes. That is why this is not MINOR.
- **Suggested outcome:** add a P9-like check to section R/J, and `wait_only_on_accept` to the campaign table.

### S2: SUGGESTION. Two more defensive terms are unrecorded (RTL, Tests)

- **m29.** The `!maap_accept_w` term at `:1090` is strictly redundant. On an accept, `maap_busy_r` and `gp_valid_r` are both 0: every entry to `S_EV_MAAP` requires `maap_avail_w`, and neither flag can rise before the accept. m29 is trace-identical to head on 300 seeds.
- **m28.** The `cfg_src_en_i` term in `init_ready_w` (`:455`) is masked functionally by the EVC_INIT enable guard (`:866`, pinned by R14 kind 2). It only saves no-op walker dispatches, so traces differ by cycles only, with no invariant violation.
- **Suggested outcome:** record m29 as an equivalent control, or remove the term. Record m28 as a performance-only term.
- **m30 (note, not a defect).** A probe for one source arms INIT for every source. It survives, and only speeds up other `NO_DA` sources whose pacing bit is clear. No documented property covers it.

### S3: SUGGESTION. The lifetime restart after a conflict is not stated precisely (Docs)

- **Where:** 05 §6bis `:415-416`: "Initial enable and conflict start a new acquisition lifetime".
- **Evidence:** a conflict clears the pacing bit, but only a `DA_OK` conflict queues demand (R10/P1). A conflict that cancels an in-flight allocation discards and releases the grant. It then waits for the next `T-ACMP-DA-RETRY` round: probe P8's record, and R4 advances a round before re-acquiring. A disable/re-enable re-acquires at once.
- **Suggested outcome:** one sentence in 05 §6bis stating this.

## Reviewer-owned lens ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #128 body and both assignments (option a); manager comments 5861504990/5861562548/5862432079; talker port/parameter identity with base; honest status 3 before acquisition, none-then-8 pacing (P4, R1/R2); parent shim replay head PASS / base FAIL; parent `pp_shadow` `[H]`/`[I]` source at `931f396e` against the reconciliation text and the manager's failing-check receipt; manager xvlog receipt | R376-2 | cc7c911e933aed4bfc9324eb5da473ae73bef618 |
| RTL | CLEAN | full read of `KL_acmp_talker.sv` at head (retry round, rotating picker, command/event alternation, `txn_ready_o`/valid independence, sticky kill, EVC_INIT guards, stale credits, `S_EV_MAAP` bounds); round-2 delta; equivalence of the removed `!en_q_r[i]`; declaration-order probe 0; talker and full HDL lint rc 0; S2 | R376-2 | cc7c911e933aed4bfc9324eb5da473ae73bef618 |
| Robustness | CLEAN | 300-seed randomized run: I1 no cross-source DA, I2 command bound ≤ 1088 cycles, including late/silent answers, ready stalls, conflict/PCP/expiry churn, exact-edge disable pulses; P7/P9 absent-allocator pacing; P3 release fairness; P5 silent-accept service; backoff untouched (R6) | R376-2 | cc7c911e933aed4bfc9324eb5da473ae73bef618 |
| Tests | CLEAN | `retry_cases.hpp` R1–R15, `retry_mutants.py` (no deadline, tally-required kills), `pp_top` MP3/S10; author campaign rerun byte-identical (56 + 4, 50/50 sites); 31 reviewer mutants (26 killed by name, m03 equivalent, S1/S2 survivors); 14 focused suites; S1 | R376-2 | cc7c911e933aed4bfc9324eb5da473ae73bef618 |
| Docs | CLEAN | 05 §6bis (F05.12 arc, recovery, bounds, consumer-visible change), 02 §4.2, 08 F08.1 `T-ACMP-DA-RETRY`, integrator and operator guides, talker/`pp_top` READMEs, RTL banners, PR body and round-2 handoff (`[H]`/`[I]` text, disposition line); `make check` rc 0; S3 | R376-2 | cc7c911e933aed4bfc9324eb5da473ae73bef618 |

## Real limits

- **Pinned tool.** The assigned path `<VALIDATION_STORAGE>/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used the manager's same-head wrapper under `pp128-manager-cc7c911e`, read-only.
  - Wrapper sha256 `905795b9…`, the same bytes as round 1.
  - It reports `Verilator 5.050 2026-07-01 rev v5.050`; executable sha256 `44898b22…`.
  - Build parallelism was capped at 8 jobs. See `receipts/tool/verilator-identity.txt`.
- **Parent gates.** I did not run the parent's `xvlog`, `pp_shadow` or `measure_test_evidence` (not permitted). Those results are the manager's receipts at this head. My part: the declaration scan, the parent test source reading, the P4 mechanism, and the author's parent-gate receipts.
- **Full banks.** Not run by me: the full 33-suite processor sweep, Yosys portability, and the builder bank. The manager's donor-full run at this head reports exit 0.
- **Evidence location.** The evidence path named in the brief (`b367df5d`) holds the round-1 packet. The round-2 author packet was read from the same public evidence branch at `938a9bcb`. Other reviewers' round-2 material was not read.
- **Harness scope.** The parent first-probe replay models the shim and talker only. It does not model the peer's 6.877 s retry or the bench's allocator history.
- **Equivalence evidence.** It rests on construction arguments plus randomized trace identity, not a formal proof.
- **Writes.** Every write went to the packet directory, including a shared scratch clone at the base for the replay. The review clone was never written and re-verified clean. No GitHub write was made.
- **No hardware.** Physical calibration was NOT RUN. No bench, hardware or field result exists for this head, and field skips are not hardware proof.

## Pending manager duties

- **Pin-adoption lane.**
  - Update `pp_shadow` `[H]` and `[I]` as the PR text specifies. Also make sure the rewritten `[I]` does not assume that source 0's grant lands after its probe snapshot: auto-acquisition may complete during the ANNOUNCE wait if parent time crosses a round.
  - Add the `retry_mutants.py` DUT-reader disposition row.
  - Re-run all four `pp_shadow` builds and `measure_test_evidence.py --check`.
  - Keep the real-shim first-probe regression.
- **Merge turn.** Build and validate the final current-dev candidate (source base `16be6768`, live dev `c0723222`). This is distinct from the source validation above.
- **Hosted/act acceptance.**
- **Bench.** Re-measure the first bind after pin adoption. Physical calibration is still NOT RUN.

## Packet

`scripts/` holds portable reviewer scripts. Each takes the tree, the scratch directory and the receipt as arguments, and none writes to a checkout.

| Script | Purpose |
|---|---|
| `decl_order_probe.py` | used-before-declaration scan |
| `own_mutants_r2.py` | 31 reviewer mutants; no tally is never a kill |
| `r2_probes.cpp`, `run_r2_probes.sh`, `probe_mutants_r2.py` | probes and randomized differential run |
| `run_focused_suites.sh` | named suites from an exported tree |
| `verilator_j8.sh` | caps the build at 8 jobs |

Receipts are listed in `MANIFEST.sha256`. Host paths are redacted to `<HOME>`, `<TOOLROOT>`, `<VALIDATION_STORAGE>`, `<LANES>` and `<PACKET>`.

R376-2 FINISHED
