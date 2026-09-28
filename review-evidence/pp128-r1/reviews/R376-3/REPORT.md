[R376] POSITIVE - exact head 66451539ee49262d97403bc6b010202bb773d272

# R376-3 independent review: processor PR #129 / issue #128, round 3

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head `66451539ee49262d97403bc6b010202bb773d272`, tree `8007bb9891167941cf8db57da813e86dfb1f2f56`, verified in the detached review clone (`receipts/clone-integrity.txt`)
- Head is a merge:
  - parent 1: `8eefb7b9`, the round-3 commit, on `cc7c911e`;
  - parent 2: processor main `97bd3786`, PR #130.
- Round-3 assignment: issue #128 comment 5862928771. Review start: PR comment 5864919319.
- Round R376-3, internal reviewer, cleared context, own detached clone.

## Verdict

**POSITIVE.** Every round-3 requirement is met at this head, and every prior public finding is resolved or out of scope. No MINOR, MAJOR or BLOCKER finding is open. One SUGGESTION is recorded (S1); it does not affect the verdict.

1. **R377-2 F1 (event classes under continuous commands).**
   - Committed regression R16 (`tb/acmp_talker/retry_cases.hpp:394-431`) holds a GET_TX_STATE continuously valid on source 3. It then raises one event each: conflict, PCP, freshness and listener. It samples the gate level before commands stop and requires more than 100 responses while they are held.
   - The four `txn_eligible_w` mutants are in `retry_mutants.py:218-233`. Each fails exactly one named assertion, `R16 <class> event served under continuous commands` (`:429`). No term was argued redundant.
   - I reran the full campaign at this head with the pinned simulator:
     - 62 killed, 7 equivalent controls, 1 performance control;
     - baseline and restored runs 1342/1342, rc 0;
     - all 59 retry assertion sites witnessed (`receipts/author-campaign/`).
   - The README table matches my rerun on all 70 rows.
   - My own probe P10 uses a different shape: two gates open, the command on source 7, and five effects including listener departure. It independently kills the same four mutants, and head passes with effects in 3–31 cycles.
2. **R376-2 S1 (absent-allocator pacing).**
   - R17 (`:436-451`) counts offers with ready tied low and time held fixed across repeated probes.
   - `wait_only_on_accept` (my m27) is in the table and killed by `R17 absent same-round probes cannot re-offer`.
   - My m27 is now killed by the committed suite, and my P9 still kills it.
3. **R376-2 S2 / R377-2 S1 (redundant and performance-only terms).**
   - m29 (`sticky_kill_ignores_accept`), the EVC_INIT maap-busy else branch (`init_busy_else_removed`) and the `pe_off_r` term of `maap_kill_w` (`kill_w_no_off`) are stated as equivalent controls, with construction arguments.
   - m28 (`init_ready_no_en`) is stated as a performance control and is never counted as equivalent.
   - The EVC_REL comment is updated.
   - The only RTL edit this round is that comment: code with comments stripped is identical to `cc7c911e`.
   - I checked each equivalence argument by construction (below). Each of the three is trace-identical to head on 300/300 randomized seeds, while a known defect diverges.
4. **R376-2 S3 (lifetime restart after a conflict).** 05 §6bis `:416-418` now states: "A conflict in `DA_OK` queues allocation at once; a conflict cancelling an in-flight allocation discards and releases its grant, then waits for new demand or the next `T-ACMP-DA-RETRY` round." This matches the RTL (`:782-785`, `:898-899`) and probes P1 and P8.
5. **No interface change.**
   - The talker's parameters, ports and leading declarations are identical to main `97bd3786`, with comments stripped.
   - The talker is the only `hdl/` path changed against main.
   - `hdl/top` is unchanged since the branch base (`receipts/rtl-delta-and-interface.txt`, `receipts/merge-and-interface-script.txt`).
6. **Composition with main `97bd3786` is sound.**
   - No file overlaps between the two sides. `git merge-tree` of the two parents yields exactly the head tree. Each side's paths are byte-identical to its parent (`receipts/merge-composition.txt`).
   - `KL_srp_top`'s header is unchanged; the `KL_srp_encoder` port delta is internal to SRP (`receipts/composition-interfaces.txt`).
   - At the merge head, every ACMP and SRP suite and `pp_top` pass (below).
   - `retry_mutants.py` passes (item 1).
   - The SRP campaign (`tb/srp_top/mutants.py`) kills 56/56 arms, all 5 chunk runners return rc 0, and assertion coverage is 49/49 (`receipts/srp-campaign/`). The hosted job also ran it unrestricted and it succeeded.

## Reconstruction (in order)

1. **Rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md`, `docs/README.md` (single-source `T-`/`P-` rules, the `make check` gate) and `hdl/README.md`.
2. **Scope.**
   - Issue #128 body: the frozen acceptance.
   - Assignments 5861093499 (round 1), 5861952375 (round 2, option (a) paced rounds) and 5862928771 (round 3: items above; R377-2 S2 is out of scope; no interface change; no GitHub comment edited or deleted). No issue or PR comment has been edited.
   - The PR body's "Round 3" section.
   - Manager comment 5865084506 at this head: donor bank 9/9, parent consumer 9/11, with the two remaining checks being the declared pin-adoption items.
3. **Authorities.** Processor 05 §6bis (F05.12), 02 §4.2 and 08 F08.1 `T-ACMP-DA-RETRY`; the talker RTL; the `tb/acmp_talker` README and runner.
4. **Diff and history.**
   - `git diff 97bd3786..66451539`: 12 files, +1264/−83. Round-3 delta `cc7c911e..8eefb7b9`: 5 files, +191/−28.
     - `retry_cases.hpp` +63/−0; no test was removed.
     - `retry_mutants.py` +63/−2; only the summary print changed.
     - 05: one sentence.
     - The talker: comment only.
     - The README.
   - Merge `6645153` has no content of its own.
5. **Public evidence.**
   - `kebag-logic/milan-fpga@b367df5d:review-evidence/pp128-r1` is the round-1 author packet.
   - The evidence branch has no round-3 author packet. The latest author packet is `author-r2` at `938a9bcb`.
   - Manager evidence: comment 5865084506, plus the same-head bank receipts, read-only (excerpts in `receipts/manager/manager-receipt-excerpts.txt`).
6. **Prior public findings.** I wrote my verdict and ledger to disk before I read R377-2's report (5862827252). I did not read the concurrent round-3 review of the other reviewer.

## Independent results (receipts under `receipts/`)

| Receipt | Result |
|---|---|
| `suites-focused-head.txt` | 14 suites at the merge head with pinned 5.050 and ≤ 8 build jobs, all rc 0: `acmp_talker` 1342, `acmp_listener` 2544, `acmp_nvm` 349, `maap` 75, `pp_top` 7751, `srp_decoder` 190, `srp_encoder` 562, `srp_stream_fsms` 1215, `srp_top` 1987, `srp_admission` 991231, `scoreboard` 3705, `dispatch` 211, `timer_service` 48, `lsn_admit` 18. `srp_encoder`, `srp_stream_fsms` and `srp_top` grew with main's PR #130. |
| `author-campaign/driver.txt`, `author-campaign/logs/*` | full unrestricted `retry_mutants.py` at head in one run (371 s): `PASS: 62 mutants killed; 7 equivalence controls; 1 performance controls; baseline and restored rc 0`; `coverage.txt` 59/59 sites, 0 UNCOVERED |
| `readme-table-vs-rerun.txt` | README table 70/70 rows match the rerun: rc, exact failure count, named assertion present, control class |
| `section-r-count.txt` | instrumented baseline: 503 section-R checks, 59 sites, 17 scenarios, as the README states. R16 has 21 checks and R17 has 5. |
| `srp-campaign/chunk-{0..4}.txt`, `aggregate.txt` | `tb/srp_top/mutants.py`, unchanged, run through `--only` slices (one unrestricted run exceeds one foreground call here: `unchunked-attempt-timeout.txt`). Every slice's positive controls PASS and every runner returns rc 0. Aggregate: 56/56 arms killed; coverage 49/49 using the runner's own rule. |
| `own/own-mutants-head-talker.txt` | my 31 round-2 mutants against the committed talker suite: **27 killed** by named assertions (m27 now by R17). m03, m29 are stated equivalents, m28 is the stated performance control; m30 is my round-2 behaviour note. |
| `own/own-mutants-r3-n05.txt`, `own/n05-invariants.txt` | new reviewer mutant n05, where only an EVC_INIT dispatch returns the command turn. It is killed by the talker suite (J5, 34 failures). It survives `pp_top`, and it breaks I2 in 295/300 seeds. |
| `own/probes-head-r3.txt` | at head, probes P1–P3, P5, P7, P9 and P10 (five classes) PASS. The 300-seed randomized run covers 107,787 commands with I1 = 0 and I2 = 0. |
| `own/probes-vs-mutants-r3.txt` | lockstep port-trace digests against head (300 seeds each); see below |
| `rtl-delta-and-interface.txt`, `merge-and-interface-script.txt`, `merge-composition.txt`, `composition-interfaces.txt` | comment-only RTL delta; interface identity; clean no-overlap merge |
| `static-gates-head.txt`, `lint-*.log`, `make-check-head.log`, `gen-matrix-head.log`, `decl-order-probe.txt` | `lint_hdl.sh` rc 0 (through the top); talker lint rc 0; `make check` rc 0 (925 links, matrix, parameters 24/24); `gen_matrix --check` 92 rows with 0 untested; `git diff --check 97bd3786 HEAD` rc 0; declaration order 0 findings |
| `hosted-checks.txt` | six executed hosted jobs at the exact head, all success: `suites` (including the "SRP LeaveAll mutation campaign" step), `portability` and `docs-gates`, in runs 36379246299 (pull_request) and 36379242893 (push). No skipped context; the only skipped step is the cached simulator build. Legacy combined status has 0 contexts. |
| `clone-integrity.txt` | detached at the exact head and tree; index tree = HEAD tree; 309 tracked entries re-hash equal in bytes and mode; 0 gitlinks, and no `.gitmodules` (this repository has no submodules); 0 untracked or ignored files after restore |

### Lockstep and probe results under mutants (`own/probes-vs-mutants-r3.txt`, 300 seeds)

**Trace-identical to head in 300/300 seeds, all probes pass:**

- the three new equivalents: `init_busy_else_removed`, `kill_w_no_off` and `sticky_kill_ignores_accept` (also my m29);
- the four earlier equivalents: `no_sticky_gp_window`, `accept_kill_zero`, `kill_no_pending_conflict` and `accept_kill_no_disable` (my m03).

**Performance control.** `init_ready_no_en` (my m28) produces traces that differ in 298/300 seeds, as expected for a latency-only change. I1 and I2 stay at 0 and every probe passes, which supports the "performance control, not equivalence" classification.

**Divergence control.** Known defect `kill_no_live_conflict` diverges in 6/300 seeds. So the digest can detect a rare cancellation race; the committed suite kills that defect by R13.

**Four eligibility mutants.** Each diverges in 278–296/300 seeds. P10 fails only for the dropped class, and both listener effects fail for `elig_drop_lsn`: for example, "conflict effect after 4352 cycles, final gates 0x12 want 0x02".

### Equivalence arguments, checked by construction

- **`init_busy_else_removed`.** EVC_INIT is dispatched only if `maap_avail_w` (`:631`). Between `S_IDLE` and `S_EV_ACT`, `maap_busy_r` can only rise on an accept, which requires `S_EV_MAAP`. `gp_valid_r` needs a live response, which requires busy. `maap_stale_r` increments only on a response timeout, which also requires busy. So `maap_avail_w` still holds at `:868`, and the else branch at `:870-872` is unreachable.
- **`kill_w_no_off`.** A set `pe_off_r[s]` implies a disable edge of `s` at some cycle t0 (`:1142`).
  - If `s`'s request was accepted before t0, then `busy || gp_valid` held at t0. `!cfg_src_en_i` made `maap_kill_w` true, so the sticky kill latched (`:1090`). An accept cannot coincide, because it requires avail.
  - If it was accepted while `pe_off_r[s]` was pending, the accept-side expression latches the kill (`:1083`).
  - `maap_kill_r` clears only on the next accept, so the term never changes `maap_kill_r || maap_kill_w` at EVC_GRANT or at the sticky latch.
- **`sticky_kill_ignores_accept`.** An accept requires `busy = gp_valid = 0`, so the sticky condition is already false on that edge.
- **`init_ready_no_en` (performance only).** A disabled source with a pending INIT can be picked. The action-side guard (`:866-867`: enable, `!pe_off_r`, `!pe_conflict_r`) prevents an offer, and the visit clears the bit. The effect is a no-op walker visit, and only the cycle traces change.

## Resolution of prior public findings at this head

| Finding | Disposition at 66451539 |
|---|---|
| **R377-2 F1 (MINOR, Tests):** four `txn_eligible_w` terms unpinned | **Resolved.** R16 is committed. `elig_drop_conflict`, `elig_drop_pcp`, `elig_drop_tmr` and `elig_drop_lsn` are in the runner, and each is killed by its named R16 assertion. The full campaign keeps baseline and restored at rc 0 with 59/59 sites witnessed. My P10 confirms this independently. |
| **R377-2 S1:** EVC_INIT busy branch unreachable, `pe_off_r` kill term redundant, EVC_REL comment | **Resolved.** Both are stated equivalent controls, and I verified the arguments above. The EVC_REL comment (`KL_acmp_talker.sv:856-858`) now describes the busy fallback as redundant. |
| **R377-2 S2:** parent `[I]` grant-snapshot timing | **Out of scope by assignment.** Recorded for the parent pin-adoption lane; the PR body's round-3 section carries it forward. Retained under pending manager duties. |
| R377-2's benign survivors (`turn_not_on_grant`, `tick_sets_all`, `t0_reset_zero`) | No finding was raised, and none is raised here. |
| **R376-2 S1:** absent-allocator pacing | **Resolved.** R17 is committed and `wait_only_on_accept` is killed. |
| **R376-2 S2:** m29, m28 | **Resolved.** m29 is stated equivalent; m28 is a performance control. m30 is my own behaviour note: it was not requested and no property covers it. |
| **R376-2 S3:** lifetime restart | **Resolved.** 05 §6bis `:416-418`. |
| R376-1 F1–F4, S1–S4 and R377-1 F1–F4, S1–S3 | **Still resolved.** They were resolved at `cc7c911e` (R376-2, R377-2). The RTL is code-identical to `cc7c911e`. The round-3 test delta only adds tests, and the suite and campaign pass at this head. |

## Findings

No MINOR, MAJOR or BLOCKER finding is open.

### S1: SUGGESTION. The README's round-3 lockstep receipts are not locatable (Tests, Docs)

- **Where:** `tb/acmp_talker/README.md:310-315`:
  - "The three controls above and the identity control each show no output divergence in 16 seeds of 3,000,000 cycles … A known live-conflict cancellation defect diverges in 12 of those seeds."
  - "The earlier four equivalence controls and the removed enable-edge term also have 16-seed lockstep receipts from round 2."
  - The PR body repeats this ("16-seed lockstep receipts").
- **Evidence:**
  - Neither the lockstep harness nor its receipts are in the tree, and the README gives no location.
  - The round-2 receipts that match the description are public only as the other reviewer's R377-2 packet (`review-evidence/pp128-r1/reviews/R377-2/receipts/30-lockstep/`).
  - No round-3 author packet is on the evidence branch (tip `b715e3b0`), so the round-3 numbers cannot be traced at review time.
- **Impact:** a reader cannot reproduce the committed quantitative claim from the tree or a cited location. The substance is independently confirmed: my 300-seed lockstep shows 0 divergence for all seven controls, and a known defect diverges. The README also correctly says these are "not formal proofs". That is why this is not MINOR.
- **Suggested outcome:** archive the round-3 lockstep harness and receipts with the author's round-3 packet and cite that location. Alternatively, reword the README to point at the reviewer receipts.
- **Verification:** the cited location resolves, and its receipt names 66451539 or 8eefb7b9.

## Reviewer-owned lens ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #128 body and round-1/2/3 assignments (5861093499, 5861952375, 5862928771). Talker interface identity against main `97bd3786`, with `hdl/top` unchanged. Merge composition (no overlap, merge-tree = head tree, `KL_srp_top` header unchanged). Manager comment 5865084506 and same-head bank receipts (donor 9/9; parent 9/11, the two declared pin-adoption items). Honest status and pacing: P4 none-then-8, P7, P9, R17. No GitHub comment edited. | R376-3 | 66451539ee49262d97403bc6b010202bb773d272 |
| RTL | CLEAN | Round-3 talker delta is comment-only (stripped code identical to `cc7c911e`). New EVC_REL comment checked for accuracy. Construction checks of `init_busy_else_removed`, `kill_w_no_off` and `sticky_kill_ignores_accept`, plus 300-seed trace identity. `init_ready_no_en` is performance-only (action guard `:866-867`). Declaration order 0. `lint_hdl.sh` and talker lint rc 0. | R376-3 | 66451539ee49262d97403bc6b010202bb773d272 |
| Robustness | CLEAN | P10: all five event effects under a command presented every cycle, within 3–31 cycles, with responses flowing. 300-seed randomized run: I1 no cross-source DA and I2 command bound, 0 violations over 107,787 commands. n05 turn-starvation mutant is caught (J5; I2 violated). Absent-allocator pacing: P7, P9, R17. P3b release fairness. P5 silent-accept service. | R376-3 | 66451539ee49262d97403bc6b010202bb773d272 |
| Tests | CLEAN | R16 and R17 source read. `retry_mutants.py` full rerun: 62 killed, 7 equivalent, 1 performance; 59/59 sites; baseline and restored rc 0; performance-control branch requires rc 0. README table 70/70. Section R 503 checks. SRP campaign 56/56 arms, 49/49 coverage. 32 reviewer mutants (27 + n05 killed by name). 14 focused suites rc 0. Hosted `suites` job including the SRP campaign step. S1 (suggestion). | R376-3 | 66451539ee49262d97403bc6b010202bb773d272 |
| Docs | CLEAN | 05 §6bis lifetime-restart sentence against the RTL and P1/P8. EVC_REL comment. `tb/acmp_talker/README.md` (R16/R17 rows, counts 1342/503/59, campaign table, `PERFORMANCE_MUTATIONS` text, equivalence arguments). PR body round-3 section. `make check` rc 0; `gen_matrix --check` rc 0. S1 (suggestion). | R376-3 | 66451539ee49262d97403bc6b010202bb773d272 |

## Real limits

- **Pinned tool.** The assigned path `<VALIDATION_STORAGE>/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used the manager's same-head wrapper `<VALIDATION_STORAGE>/pp128-manager-66451539/pinned-tool-bin/verilator`, read-only.
  - Wrapper sha256 `905795b9…`, the same bytes as rounds 1 and 2; it reports `5.050 2026-07-01 rev v5.050`.
  - Executable sha256 `44898b22…`.
  - Build jobs were capped at 8 (`receipts/tool/verilator-identity.txt`).
- **SRP campaign.** Run in five `--only` slices, because one unrestricted run exceeds a single foreground call here. The coverage rule was re-applied to the union of slices by `scripts/srp_campaign_chunk.py`. The unrestricted form ran and succeeded in the hosted `suites` job at the exact head.
- **Not run by me.** The full 33-suite bank, Yosys portability, the `nvm_port` figures, and every parent gate (`xvlog`, `pp_shadow`, `measure_test_evidence`, builder). Those results are the manager's receipts at this head: donor bank 9/9 exit 0 (1,015,815 checks); parent consumer 9/11, where `pp_shadow` `[H]` fails in base, vid73 and crf, `[I]` fails in crf, and the reader-disposition row is missing. `xvlog` passes with the 4 pre-existing findings. I did not rerun the parent first-probe replay: the talker code is identical to `cc7c911e`, where I replayed it (PASS).
- **Author evidence.** No round-3 author packet was public at review time. The author's lockstep receipts were therefore not inspected (S1).
- **Equivalence evidence.** It rests on construction arguments plus randomized trace identity, not a formal proof.
- **Writes.** Everything went to this packet. Read-only `importlib` loads created two ignored `__pycache__` directories in the review clone. I removed them and re-verified the clone clean. No GitHub write was made.
- **Source validation only.** This is source validation. The final current-dev candidate (source base `97bd3786`, live dev `54ce8773`) is built by the manager at the merge turn.
- **No hardware.** Physical calibration NOT RUN. No bench, hardware or field result exists for this head. Field skips are not hardware proof.

## Pending manager duties

- **Pin-adoption lane:**
  - update `pp_shadow` `[H]` and `[I]` as the PR body specifies, including R377-2 S2: count grants per source from MAAP enable, including grants during ANNOUNCE polling;
  - add the `retry_mutants.py` DUT-reader disposition row;
  - keep the real-shim first-probe regression;
  - re-run `pp_shadow` (all builds) and `measure_test_evidence.py --check`.
- **Merge turn:** build and validate the final current-dev candidate (source base `97bd3786a56020adec99068369642d2025b801e4`, live dev `54ce877371ee6e8878cf67294e86c2a8481b62f6`).
- **Hosted/act acceptance.**
- **Evidence archive:** archive the round-3 author packet and consider S1.
- **Bench:** re-measure the first bind after pin adoption. Physical calibration is still NOT RUN.

## Packet

Portable scripts in `scripts/` take the tree, the scratch directory and the receipt as arguments. They need `PINNED_VERILATOR`, and none writes to a checkout.

| Script | Purpose |
|---|---|
| `verilator_j8.sh` | caps build jobs at 8 |
| `run_focused_suites.sh` | named suites |
| `own_mutants_r2.py` | round-2 set, anchors unchanged |
| `own_mutants_r3.py` | n05 |
| `r3_probes.cpp`, `run_r3_probes.sh`, `probe_mutants_r3.py` | probes P1–P10 and the lockstep digests |
| `srp_campaign_chunk.py` | sliced SRP campaign and coverage aggregate |
| `readme_table_check.py` | README table against the rerun |
| `merge_and_interface.sh` | merge, comment-only and interface checks |
| `decl_order_probe.py` | declaration-order scan |

Receipts are listed in `MANIFEST.sha256`. Host paths are redacted to `<PACKET>`, `<VALIDATION_STORAGE>`, `<LANES>`, `<REVIEWS>`, `<HOME>` and `<TOOLROOT>`.

R376-3 FINISHED
