[R314] POSITIVE - exact head a43d07668ff03efc299fbbf2a3891f2aa90255f7

# R314-1 internal independent review: processor issue #116 / PR #117

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `a43d07668ff03efc299fbbf2a3891f2aa90255f7`, tree `0615673c1cc7e6d2760d0141eedeab64b173c997`
- Source base: `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b` (one commit, five files, +18/-9)
- Parent consumer: kebag-logic/milan-fpga `508-pp-pin-adopt` at `35f0695815c202392b6b4806bb9f59dd110687ed`
- Round: R314-1, cleared context, own clone. Lenses applied: Conformance, RTL, Robustness, Tests, Docs.
- Result: every lens CLEAN. Two SUGGESTIONs (non-blocking). No BLOCKER, MAJOR or MINOR.

## Reconstruction (public state only)

1. The processor has no AGENTS.md/CONTRIBUTING.md of its own. The parent's AGENTS.md (at the 508 head) defines the review procedure, the five lenses and the severities; docs/README.md defines the processor's authorities.
2. Issue #116 body (frozen acceptance): (1) in a parent consumer with this head as the gitlink, `check_port_contracts`, `measure_naming --check` and `measure_test_evidence --check` exit 0, and the parent adds no identity and raises no ratchet; (2) no behaviour change: every suite check count and every mutation verdict table is identical, and each dropped deadline has a termination-by-construction argument; (3) the processor's own gates pass. Issue comments: executor REVIEW READY only. PR #117 comments: the manager's review-start only.
3. Interface authorities: `hdl/packet_engine/KL_pp_nvm_mgr_arb.sv` header and 02 §8 (manager 1 = the integrating platform's saved-state writer, tied idle until it lands); 10 §6.3 and `docs/guides/integrator.md:285` (admission latency); the parent gate rules in `scripts/check_port_contracts.py`, `scripts/measure_naming.py`, `scripts/measure_test_evidence.py` and their budgets at 35f06958.
4. Diff and history: `diff.patch` (raw `git diff a8f8ce81..a43d0766`). The head commit's single parent is a8f8ce81.
5. Public evidence: kebag-logic/milan-fpga `1052ff4d18b9306d4424369259a028d7e288f3cf` `review-evidence/pp116-r1/`. I read it after my own loop audit, and it agrees with that audit. The only manager comment on the issue or PR is the review-start.

**Prior public review findings on PR #117:** none exist. The PR has 0 reviews and 0 review comments, and its issue and PR comments are only the executor's REVIEW READY and the review-start. There is nothing to resolve or retain.

## What I executed (all receipts listed in MANIFEST.sha256)

| Check | Result | Receipt |
|---|---|---|
| Three parent gates, candidate consumer: 35f06958 + a local gitlink-only commit `3e62a423` (protocol-processor → a43d0766), both submodules initialised at their gitlinks | port contracts 0, naming 0, test evidence 0 | `receipts/parent_gates/cand.*`, `consumer_identity.txt` |
| Same gates, control consumer: unmodified 35f06958 (gitlink a8f8ce81) | 1 / 1 / 1. Refusals exactly as in the issue: 7 `u_nvm_arb.m1_*` connections, 2 NEW identities (`s_rsp_data_o`, `srp_sr_admitted_o`), 6 wall-clock files > ratchet 3 | `receipts/parent_gates/ctrl.*` |
| Gate rules and budgets | unmodified parent 35f06958 files (hashes recorded). Candidate reports 111 ≤ 111 undocumented processor ports, 96/96 naming identities recorded, 3 ≤ 3 wall-clock files | `consumer_identity.txt`, cand logs |
| Structural no-change proof | both `.sv` files: comment-stripped token streams identical (248/248 and 22086/22086). Each runner's AST equals the base AST with its single `subprocess.run(timeout=)` keyword removed. The tokeniser has a negative control (a `1'b0`→`1'b1` edit is detected; a comment edit is not) | `receipts/structural_equivalence*.txt` |
| Mutation campaigns, unmodified runners, head and base, pinned Verilator 5.050 | all 6 runs exit 0. Runner stdout and every per-variant FAIL/tally line identical head vs base: desc 18/17/1 with the named failure; GSI golden + 13 + restored; SRP 12/12 | `receipts/campaigns/*`, `campaign_comparison.txt` |
| Focused suites, head and base | desc_mem_guard 78; srp_admission 1138/12615/41012/201073/991231; srp_top 1531; pp_top 1928+20=1948; all 0 FAIL and identical. They also match the executor's published comparison rows | `receipts/suites/*` |
| Processor `make check` at head | exit 0 (lint, wavedrom, 855 links, matrix, modmatrix, stale) | `receipts/processor_make_check.log` |
| Hang probes: disposable stalls outside the fixed tables (see Robustness) | 6 stall mutants all terminate (5–28 s). The scope control hangs, as predicted | `receipts/hang_probes/*.json` |
| Clone integrity after all work | HEAD/tree exact. Nothing untracked or ignored. Index listing hash equals the HEAD tree listing hash. 0 content mismatches. The processor has no gitlinks | `receipts/clone_integrity.txt` |

Verilator identity: wrapper `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` (sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`) reports `Verilator 5.050 2026-07-01 rev v5.050`. It is recorded in every campaign and suite status file.

## Lens results

[R314] PASS Conformance — issue #116 acceptance 1–3; `receipts/parent_gates/{cand,ctrl}.exits`, `consumer_identity.txt`, `receipts/processor_make_check.log`; hosted check-runs at a43d0766 — I ran all three gates myself. They exit 0 with this head as the committed gitlink and 1 with a8f8ce81, and the control refusals are exactly the issue's. The consumer commit changes only the gitlink, and every rule and budget file is the parent's own at 35f06958, so no identity was added and no ratchet raised. Acceptance 2 is covered below under Tests and Robustness. Acceptance 3: `make check` exits 0. Hosted `suites`, `docs-gates` and `portability` ran to completion with conclusion success in both event contexts; none were skipped.

[R314] PASS RTL — `hdl/top/protocol_processor_top.sv:2529-2530,2544`, `:521-525`, `:819-820`; `hdl/aecp/KL_aecp_desc_mem_guard.sv:40`; `hdl/packet_engine/KL_pp_nvm_mgr_arb.sv:12-18,111-114,149-150` — the RTL changes are comments only (token streams identical).
- Rationale at 2529 sits directly above the six-literal run `m1_req_i..m1_rready_i` and is true: the arbiter header names manager 1 as the saved-state writer, "tied idle until it lands", and `iss1_w` needs `m1_req_i`, so only manager 0 can issue.
- Rationale at 2544 sits directly above `m1_abort_i` and is true: manager 1 never issues, so `own_r` never becomes `O_M1`, and the abort only acts on an owned READ (`:149-150`).
- The reworded `srp_sr_admitted_o` doc keeps the no-optimistic-term, low-until-full-round and cross-source facts. It still points to 10 §6.3. The numeric bound (3·N_STREAM_OUT_P clocks; 4 at one source) is unchanged in prose at `:819-820`, `integrator.md:285` and 10 §6.3. So the fact is still in every place a reader looks; it has only left the `//!` port comment, where it read as a unit the name lacks.
- "response bytes" → "response data" drops a unit word only; the 64-bit width and the pass-through fact remain.

[R314] PASS Robustness — `tb/desc_mem_guard/mutate.py:28-30` + `sim_main.cpp:22,129-156,170-194`; `tb/pp_top/gsi_mutants.py:79-82` + `gsi_internal.hpp` (all) + `sim_main.cpp:300-345,1155-1548,1553-1700`; `tb/srp_admission/mutants.py:61-64,89` + `tb/srp_admission/sim_main.cpp` + `tb/srp_top/sim_main.cpp:333,403-414,420-440,445-475,1300-1305` + `hdl/srp/KL_srp_decoder.sv:182,515-575` + `hdl/srp/KL_srp_top.sv:430-450,1010-1110`; `receipts/hang_probes/` — I checked each removed deadline for a real termination argument that holds for every mutant.
- **desc_mem_guard.** Every loop in the `--late-only` path is counted by the harness: boot ≤ BOUND (4160) cycles, each read ≤ BOUND+1, fixed idles. The runner has one fixed mutant. Probe `desc-guard-no-request-stall` (memory never requested) ends in 5.1 s with 18 checks, 9 FAIL.
- **GSI.** In `--gsi-internal-only`, every wait has a budget: boot 400,000 cycles, query 500·MS_CYC, `wait_frame` a timeout budget. `feed` and `idle` have fixed counts, and the queue scans and the MRPDU parser advance on every iteration. The only DUT-clock wait in the harness (`sync_join`, on `dbg_now_ms_o`) and `la_guard` are not reachable from this phase. So this bound holds for any mutant, in any file. Probes `gsi-restore-never-done-stall` and `gsi-timer-frozen-stall` (the processor's whole ms timebase frozen) end in 26 s and 28 s. For contrast, the fixed `integrator-path` mutant already stops early (158 checks), and it stops through these budgets.
- **SRP.** The admission bench is fully counted (`n < N`, SETTLE). srp_top has three unbounded waits: `feed` on decoder ready, `sync()` on `now_ms_o`, and `next_tick` on the join strobe. Termination rests on facts I confirmed in the RTL:
  - the decoder's ready drops only in its ≤4-cycle drain, and it has no downstream ready;
  - the join cadence re-arms itself from the timer service;
  - timer arms come only from registrar events, which come from the decoder;
  - the admission outputs (`sr_admitted`, grant/sum, `over_limit`, `round_done`) reach only the talker FSMs' declaration path and the optimistic window;
  - the runner writes only `hdl/srp/KL_srp_admission.sv` (`mutants.py:89`), so every mutant it can express lies outside those loops.

  Probes `srp-adm-never-publish-stall-admission`, `srp-adm-never-publish-stall-top` and `srp-adm-grant-flap-stall-top` end in 5.5 s, 12.9 s and 12.9 s. The scope control `srp-top-timer-scope` freezes the timer, a file the runner never edits, and hangs until the 540 s safety net (exit 124). So the comment's precondition ("decoder drains and the recurring timer cadence are not mutated") is real and correctly stated.

[R314] PASS Tests — `receipts/campaign_comparison.txt`, `receipts/suites/comparison.txt`, `receipts/structural_equivalence.txt`; runners at head `tb/desc_mem_guard/mutate.py`, `tb/pp_top/gsi_mutants.py`, `tb/srp_admission/mutants.py` — I checked that the runners keep every verdict requirement: each AST differs from base only by the removed `timeout=` keyword. I re-ran all three campaigns at both pins. The verdict tables, named failures and per-leg tallies are identical, and each mutant is still killed by its named check. The four suites that compile the changed RTL or that the runners drive have identical tallies at both pins. The full 33-suite total (1,008,919) is the executor's and manager's banked evidence, not mine (see limits). No test was weakened, and no oracle changed.

[R314] PASS Docs — `hdl/top/protocol_processor_top.sv:519-525,819-820`; `docs/guides/integrator.md:254,285`; `docs/architecture/10_srp_engine.md` §6.3; `docs/architecture/02_interfaces.md:559-567`; `tb/{desc_mem_guard,pp_top,srp_admission}/README.md`; PR #117 body; evidence archive `1052ff4d:review-evidence/pp116-r1/author/HANDOFF.md` — no authoritative contract changes. The admission latency still appears in the integrator port table and in 10 §6.3. No README or architecture page mentions the removed host deadlines. The new in-tree comments are accurate summaries of the full arguments. One PR-prose issue is recorded as SUGGESTION S1.

## Findings

**S1 — SUGGESTION — Docs — PR #117 body, links `[HANDOFF.md](HANDOFF.md)` and `[COMPARISON.md](COMPARISON.md)`**
- Evidence: neither file is in the processor tree at a43d0766. On GitHub, relative links in a PR body resolve under the PR URL and return 404. The per-file termination arguments and the full before/after comparison exist publicly only in kebag-logic/milan-fpga `1052ff4d18b9306d4424369259a028d7e288f3cf` `review-evidence/pp116-r1/author/`, and nothing on the issue or PR links there yet.
- Impact: a cold reader starting from the PR hits dead links to the evidence behind acceptance 2. The in-tree comments carry the arguments in short form, so the tree is not affected.
- Outcome: the PR body or a manager evidence comment links the archive paths. No head change is needed.
- Verification: the links resolve from the PR page.

**S2 — SUGGESTION — Robustness, Tests — `tb/srp_admission/mutants.py:61-62`**
- Evidence: unlike the other two runners, this runner's termination depends on RTL outside the harness: the decoder drain and the timer/join cadence. That holds only because `campaign()` writes nothing but `KL_srp_admission.sv`. The `srp-top-timer-scope` probe shows srp_top hangs with no host deadline if the timer is ever mutated.
- Impact: none today. A future mutant added in another SRP file would hang silently, and the parent ratchet forbids adding a host deadline back.
- Outcome (optional): name the enforced surface in the comment, e.g. "only KL_srp_admission.sv is mutated; its outputs reach neither the decoder nor the timer".
- Verification: comment review.

## Reviewer-owned ledger

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #116 acceptance; parent gates on the cand/ctrl consumers; gate rules and budgets at 35f06958; `make check`; hosted check-runs | R314-1 | a43d07668ff03efc299fbbf2a3891f2aa90255f7 |
| RTL | CLEAN | `protocol_processor_top.sv:519-525,819-820,2512-2560`; `KL_aecp_desc_mem_guard.sv:40`; `KL_pp_nvm_mgr_arb.sv`; token-stream equivalence | R314-1 | a43d07668ff03efc299fbbf2a3891f2aa90255f7 |
| Robustness | CLEAN (S2 open, optional) | loop audit of the three harness paths; decoder/timer/cadence RTL; 7 hang probes | R314-1 | a43d07668ff03efc299fbbf2a3891f2aa90255f7 |
| Tests | CLEAN (S2 open, optional) | runner ASTs; 3 campaigns × 2 pins; 4 focused suites × 2 pins | R314-1 | a43d07668ff03efc299fbbf2a3891f2aa90255f7 |
| Docs | CLEAN (S1 open, optional) | port docs; integrator.md; 10 §6.3; 02 §8; bench READMEs; PR body; evidence archive | R314-1 | a43d07668ff03efc299fbbf2a3891f2aa90255f7 |

## Real limits

- I did not run the full processor suite bank (33 suites) or any parent, gPTP, Yosys or builder bank. That is out of scope for this role. The 1,008,919-check total and the ten-check parent consumer set (371 integration checks) are the executor's published evidence and the manager's banked runs. My own before/after coverage is the 4 affected suites, the 3 campaigns and the structural equivalence proof.
- The parent consumer is the 508 branch head 35f06958 with a local gitlink-only commit (`3e62a423`, not the executor's `ea96db32`). It is not live dev `ffcbd33d`. The final current-dev candidate belongs to the manager at the merge turn.
- The hang probes are disposable and not exhaustive. The termination claims rest on the loop audit. The probes corroborate it and show the SRP argument's scope.
- `make check` ran in a git-less export, so its `stale` leg used mtimes. The hosted `docs-gates` context at this head covers the committed-time form.
- Physical calibration NOT RUN. No hardware was used; field skips are not hardware proof.
- Receipts contain local absolute paths, so path redaction at publication is the manager's call.
- Incidental exposure: while checking how earlier PRs linked their evidence, a query on a different PR (#115) printed the opening header lines of another reviewer's verdict on that PR. I read no findings from it, and it concerns nothing in PR #117.

## Pending manager duties

- Publish this report and the MANIFEST-listed receipts, and link the pp116-r1 evidence archive from the PR or issue (S1).
- Build and validate the final current-dev candidate (source base a8f8ce81, live dev ffcbd33d) at the merge turn, including the parent consumer with the pushed gitlink.
- Accept hosted and act contexts. At this head the hosted `suites`, `docs-gates` and `portability` show success in both event contexts; the legacy combined status is empty ("pending", no contexts).
- Obtain the external independent review (R315) and meet the rest of the completion bar before any merge.

R314-1 FINISHED
