[R315] POSITIVE - exact head a43d07668ff03efc299fbbf2a3891f2aa90255f7

# R315-1: external independent review of processor PR #117 (issue #116)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `a43d07668ff03efc299fbbf2a3891f2aa90255f7`, tree `0615673c1cc7e6d2760d0141eedeab64b173c997`
- Source base: `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b` (tree `60b6e1b11dfa57558a2d839a36d8a6769c0a4e72`)
- Parent consumer: kebag-logic/milan-fpga branch `508-pp-pin-adopt` at `35f0695815c202392b6b4806bb9f59dd110687ed`
- Reviewer role: external, cleared context, from public state only. I did not read any other reviewer's report, private author material or lane scratch.

## Verdict

POSITIVE. At this head, every frozen acceptance criterion of #116 holds:

1. In a parent consumer (508 branch, this head committed locally as the only change, a gitlink), all three gates exit 0. With `a8f8ce81` as the control, each exits 1 and reports exactly the issue's findings. The parent's rule files and budgets are unchanged, so the parent adds no identity and raises no ratchet.
2. Nothing behaves differently:
   - Both changed SV files have identical comment-free token streams and identical Verilator preprocessed output.
   - Each runner's syntax tree changes only by losing its `timeout=` keyword.
   - All three mutation campaigns give identical verdict tables and identical per-leg check tallies at base and head.
   - Each dropped deadline has a real termination argument, which I checked against the harness code and against six probes designed to hang. Every probe stopped on its own.
3. The processor's own gates pass at this head: docs gates, module matrix, diagram lint and zero-tolerance HDL lint, run locally. The exact-head hosted `hdl` workflow ran and passed all six jobs, including 1,008,919 suite checks with 0 failing.

There are no BLOCKER, MAJOR or MINOR findings. There is one SUGGESTION (S1), which does not affect coverage.

## Scope reconstructed

- **Contributor rules.** The processor repository has no AGENTS.md or CONTRIBUTING.md. I read the parent's AGENTS.md (reviewer procedure §6, completion §7) and the processor's `docs/README.md` conventions, including the single-source rule for timing values.
- **Issue #116.** The acceptance criteria are frozen. Three parent `docs-check` gates refuse processor content added since `09f9bf38`:
  - 7 literal-bound `u_nvm_arb.m1_*` connections have no rationale.
  - 2 new naming identities: `s_rsp_data_o` and `srp_sr_admitted_o`.
  - 6 wall-clock suite files exceed the ratchet of 3, because 3 processor runners pass `timeout=`.

  The acceptance is: the three gates return 0 in a parent consumer, nothing behaves differently (counts and verdict tables identical, termination shown by construction), and the processor's own gates pass. The only public comment is the executor's REVIEW READY. There are no maintainer scope changes.
- **PR #117.** It has no review bodies. Its only comments are the two review-start notices (internal and external). There are **no prior public review findings** on this PR to resolve or retain.
- **Diff** `a8f8ce81..a43d0766` (one commit, 5 files, +18/-9):
  - `hdl/top/protocol_processor_top.sv`: two rationale comments above the `u_nvm_arb` manager-1 literal runs. The `srp_sr_admitted_o` `//!` loses its latency sentence, which moves to a plain comment above the port's assignment.
  - `hdl/aecp/KL_aecp_desc_mem_guard.sv`: `s_rsp_data_o` doc changes from "response bytes, unchanged" to "response data, unchanged".
  - Three runners each drop `timeout=` from `subprocess.run` and gain a one-comment termination argument.

## Lens results (each with the artifact examined at this head)

```text
[R315] PASS Conformance — issue #116 acceptance 1-3; receipts/gates/*.rc|*.log, receipts/equivalence/*, receipts/campaigns/comparison.txt, receipts/processor-gates/rc.txt, receipts/hosted/check-runs.tsv — Parent consumer at 35f06958 plus a local gitlink-only commit 28bbe553 pinning a43d0766: check_port_contracts rc=0, measure_naming --check rc=0 ("NAMING RATCHET: PASS (96 ... all recorded by identity)"), measure_test_evidence --check rc=0 ("3 <= 3 wall-clock-dependent suite file(s)"). Control at gitlink a8f8ce81: all three rc=1, reporting exactly the issue's 7 u_nvm_arb.m1_* connections, 2 NEW identities and "6 > ratchet 3". scripts/test_evidence.budget sha256 is the same in both runs, and the parent commit changes only the gitlink.
[R315] PASS RTL — hdl/top/protocol_processor_top.sv:2529-2544, hdl/packet_engine/KL_pp_nvm_mgr_arb.sv:11-55,122-183, docs/architecture/02_interfaces.md:556-562; hdl/aecp/KL_aecp_desc_mem_guard.sv:40 — Comment-free SV tokens are identical at base and head (248/248 and 21,867/21,867), and the Verilator 5.050 `-E -P` output is byte-identical. A tokenizer negative control (m1_abort_i 1'b0->1'b1) is detected. The rationale is true against the arbiter. With m1_req_i=0, iss1_w never fires, own_r never becomes O_M1 and the drain term `(own_r==O_M1)&&m1_abort_i` can never be true. So "nothing to abort" holds, and manager 0 (the KL_acmp_nvm_shadow binding manager) is the only user. This matches the arbiter banner, the top's own `//!` at :2437-2440 and 02 §8.2 ("tied idle ... until one lands"). Zero-tolerance lint passes: 40 tops OK, rc=0.
[R315] PASS Robustness — tb/desc_mem_guard/sim_main.cpp:129-194, tb/pp_top/gsi_internal.hpp:22-361 + tb/pp_top/sim_main.cpp:1155-1720, tb/srp_admission/sim_main.cpp:116-263, tb/srp_top/sim_main.cpp:404-472,1301-1305; receipts/hang-probes/results.jsonl — Termination without a host deadline holds for every mutant each runner can express, including ones that hang. Details below. Six hang-oriented probes (memory mute, debt never clears, restore never done, MAC TX silent, admission round never completes, verdict toggling every clock) all exited on their own in 5-18 s, with tallies and named failures. The only deadline in the probe driver is my reviewer-side guard, which was never hit.
[R315] PASS Tests — receipts/campaigns/{head,base}-{desc,srp,gsi}.*, receipts/campaigns/comparison.txt, receipts/hosted/*-suites.txt — I ran all three campaigns at base and head myself with the pinned Verilator 5.050. desc: rc=0/0, "18 checks: 17 PASS, 1 FAIL" and the same named failure. srp: 12/12 legs PASS both times, with identical tallies (12615 / 991231 / 1531 controls; 402/5473/105, 175/1067/205, 146/695/90 mutants). gsi: 13 mutants detected plus golden and restored PASS both times, with identical results.json and per-run tallies. 32/32 rows are identical. Each runner's AST equals its base AST minus the `timeout=` keyword alone (600 / 1800 / 1200 s dropped). All three verdict predicates (`judge`, `check_variant`, the desc `detected` expression) are unchanged, so no test was weakened. Suite bank: the author's before/after suite lines and the exact-head hosted `suites` job lines are identical (33 PASS lines, 1,008,919 checks, 0 failing).
[R315] PASS Docs — hdl/top/protocol_processor_top.sv:519-525,819-820; docs/architecture/10_srp_engine.md:276-331 (§6.3); docs/guides/integrator.md:254,285; hdl/aecp/KL_aecp_desc_mem_guard.sv:40,50; tb/*/README.md; receipts/processor-gates/* — Both rewords keep every fact, and neither documents a unit the value lacks. The parent rule (measure_naming.py docstring) is about a unit of measure that describes the VALUE. `s_rsp_data_o` is a 64-bit pass-through payload with no quantity. "data, unchanged" keeps both facts, and byte order stays on the input it passes (m_rsp_data_i:50, "big-endian byte order"). `srp_sr_admitted_o` is a per-source verdict vector with no unit. The "clocks" figure was a timing property, not the value's unit. Its authoritative home under docs/README single-source rules is 10 §6.3 (the 3*M+1 conservative bound, at most three rounds, 4 clocks at M=1, and measured cases), which the port `//!` still links. The integrator guide row :285 repeats it, and the exact sentence survives next to the driving assign at :819-820. So no information is hidden, and nothing was stripped from a budgeted identity. No README or doc mentions the dropped host deadlines. At head, processor links (855), matrix (115 REQ, 17 GAP), module matrix (92 rows, 0 untested), wavedrom (18), diagram lint (41+18) and stale all return 0.
```

### Termination arguments, checked per runner

Each claim below is from my own reading of the harness at this head.

- **`tb/desc_mem_guard/mutate.py:28-30`** ("late-only case bounds boot and every read by BOUND cycles; its remaining idle steps have fixed counts, even if memory stalls"). **True.**
  - With `--late-only`, `main` runs only `late_case` (`sim_main.cpp:339-340`).
  - `boot` is `idle(4)` plus at most `BOUND` = 4160 ticks.
  - Each `read` is at most `BOUND` ticks plus 1.
  - `idle(80)` is fixed.
  - `tick()` has no loop, and the memory model is a deque driven by the tick count.
  - So the bound is independent of the RTL under test.
  - Probes `desc-memory-mute` and `desc-debt-forever` both finish in about 5 s: "18 checks: 9 PASS, 9 FAIL", first failure "boot image did not validate".
- **`tb/pp_top/gsi_mutants.py:79-82`** ("boot, query and frame waits have cycle budgets; the other loops consume finite inputs"). **True for any RTL edit.**
  - `--gsi-internal-only` runs only `InternalStreamInfoPhase::run` (`sim_main.cpp:9502-9504`).
  - Its `boot` loop is budgeted at 400,000. `query` is 500·`MS_CYC`. `wait_frame`/`wait_any` are `timeout_ms`·`MS_CYC` with `MS_CYC`=100. `run_ms`/`idle` are fixed. `listener_news` and `input_uns` loop over fixed ms and pop finite queues.
  - `feed` presents one byte per cycle and never waits on `ready`.
  - `step()` has only fixed or finite-container loops. `parse_mrpdu` advances its index by at least 2 per iteration, bounded by the frame size.
  - The unbudgeted `sync_join` and `la_guard` helpers are not reachable from this phase.
  - Probes: `gsi-tx-silent` (no frame ever leaves the MAC) finishes in 17.6 s with "132 checks, 124 failures". `gsi-restore-never-done` finishes in 7.5 s.
- **`tb/srp_admission/mutants.py:61-64`** ("twelve legs use fixed source/case loops and cycle observations; decoder drains and the recurring timer cadence are not mutated"). **True, and the premise is structural.**
  - The runner writes only `hdl/srp/KL_srp_admission.sv` (`mutants.py:89`).
  - The admission bench's loops are fixed (`N`, `SETTLE`=3N+4).
  - srp_top has three unbudgeted waits:
    - `feed` (:404, decoder `mrp_ready_o`). The decoder's only inputs are clk, rst and `mrp_*` (`KL_srp_decoder.sv:72-79`), so there is no downstream ready.
    - `sync` (:466, `now_ms_o`). This comes from `KL_pp_timer_service`'s free-running counter.
    - `next_tick` (:1301, `p_join_fsm_r`). The cadence rearms itself, and it competes only with talker and listener leave-timer arms. Those are driven by registrar, LeaveAll and gate events (`KL_srp_talker_fsm.sv:642-712`), not by `sr_admitted_i`. The listener FSM has no admission input.
  - Admission outputs reach none of the three.
  - Probes `srp-round-never` and `srp-verdict-toggles` finish every leg in 5-11 s.

## Findings

No BLOCKER, MAJOR or MINOR findings.

```text
[R315] SUGGESTION Tests, Docs — tb/srp_admission/mutants.py:61-62 — S1: name the srp_top waits that the termination argument depends on
Requirement/evidence: the in-source argument compresses a structural premise that
  holds today. srp_top's feed (sim_main.cpp:404), sync (:466) and next_tick
  (:1301) are unbudgeted loops. They terminate only because admission outputs
  reach neither the decoder's mrp_ready_o nor the timer/join cadence. The full
  argument exists only in the review packet's HANDOFF.md, not in the tree.
Impact: none at this head. A future edit that lets the runner mutate another SRP
  file, or that couples admission into the cadence, could silently void the
  argument, and the comment would not warn the editor.
Required outcome (optional): one more comment line naming those three waits and
  why admission cannot reach them. Alternatively, give them cycle budgets.
Verification: read the comment; the hang probes in this packet stay green.
```

### Prior public findings

None exist on PR #117 or issue #116 at the time of this review, so there is nothing to resolve or retain.

### Out-of-scope observation (not a finding against this head)

`tb/srp_admission/README.md:92` says the srp_top control has "1527 in srp_top". The suite prints **1531** at both base and head (receipts/campaigns/*-srp/control-srp-top.log), and `tb/srp_top/README.md:14` also says 1531. The drift came in with the PR #114 lineage (`git log -S` finds `fbabb94`). This PR does not touch it, and #116's frozen scope excludes it. I recommend a separate issue under AGENTS.md §4. It does not affect any lens of this round, because it is neither introduced nor changed by the diff under review.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #116 acceptance 1-3; parent gates in the 508 consumer (candidate rc 0/0/0, control rc 1/1/1); budget hash; gitlink-only parent diff | R315-1 | a43d07668ff03efc299fbbf2a3891f2aa90255f7 |
| RTL | CLEAN | protocol_processor_top.sv:519-525,819-820,2529-2544; KL_aecp_desc_mem_guard.sv:40; KL_pp_nvm_mgr_arb.sv; token and preprocess equivalence; lint 40/40 | R315-1 | a43d07668ff03efc299fbbf2a3891f2aa90255f7 |
| Robustness | CLEAN | termination of all three runners traced through desc/pp_top/srp_admission/srp_top harnesses and SRP RTL dependencies; 6 hang probes | R315-1 | a43d07668ff03efc299fbbf2a3891f2aa90255f7 |
| Tests | CLEAN (S1 open, SUGGESTION only) | 3 campaigns × {base, head} run by the reviewer, 32-row identity; runner AST equivalence; hosted and author suite totals 1,008,919 / 0 failing | R315-1 | a43d07668ff03efc299fbbf2a3891f2aa90255f7 |
| Docs | CLEAN (S1 open, SUGGESTION only) | both reworded `//!` against the parent naming rule, 10 §6.3, integrator guide :254/:285, tb READMEs; processor docs gates | R315-1 | a43d07668ff03efc299fbbf2a3891f2aa90255f7 |

## Evidence index (all under this packet, listed in MANIFEST.sha256)

- `scripts/run_parent_gates.sh`, `receipts/gates/{control-a8f8ce81,candidate-a43d0766}.{identity,rc,*.log}`: the three parent gates. The consumer is my own scratch clone of milan-fpga at `35f06958`. The candidate is a local, never-pushed commit `28bbe553` whose only change is the gitlink to `a43d0766`. `receipts/state/parent-consumer.txt` records the consumer's gitlinks.
- `scripts/semantic_equivalence.py`, `receipts/equivalence/*`: SV token and Python AST equivalence, the Verilator preprocess comparison and the tokenizer negative control.
- `scripts/run_campaign.sh`, `scripts/compare_campaigns.py`, `receipts/campaigns/**`: all three campaigns at base and head, with wall times (desc 6/5 s, srp 90/90 s, gsi 280/287 s, well under the dropped 600/1200/1800 s) and the 32-row comparison.
- `scripts/hang_probes.py`, `receipts/hang-probes/**`: six hang-oriented probes with per-leg logs and `results.jsonl`.
- `receipts/processor-gates/*`: processor docs gates and HDL lint at head.
- `receipts/hosted/*`: exact-head check runs (6 jobs across 2 `hdl` runs, push and pull_request, all executed, all `success`, none skipped) and the suite-line identity of the hosted, author-before and author-after results.
- `receipts/tool-identity.txt`: pinned Verilator 5.050 wrapper and target hashes.
- `scripts/verify_clone_state.sh`, `receipts/state/*`: post-review state of the review clone, plus a negative control on the verifier.

Build logs are raw, except that I redacted the host path of the pinned tool root to `$VERILATOR_ROOT` / `$VERILATOR_PREFIX`. I reran the comparison on the redacted receipts and it is still identical.

## Post-review state

- The review clone `$REVIEWS/r315-1-pp116` is exactly the reviewed head and tree:
  - the index equals the HEAD tree (246 entries, modes and blobs);
  - every tracked file's bytes and mode equal its index blob;
  - there are 0 untracked, ignored or modified entries;
  - the processor tree has no gitlinks or `.gitmodules`.
- The parent consumer's required gitlink (`protocol-processor` → `a43d0766`) and its unchanged `gptp-processor` (`e5dcea6e`), `external` (`efeb541a`) and `verilog-axis` (`48ff7a7e`) gitlinks are recorded.
- All probes and builds ran in scratch copies only.
- I made no source edits, commits to any published repository, pushes or GitHub writes.

## Real limits

- I did not run the full processor suite bank (`run_suites.sh`), the NVM figure campaign or Yosys portability; they are outside my allowance. Suite-count identity rests on:
  - my proof that the RTL is comment-only;
  - the unchanged suite sources;
  - the published author before/after logs;
  - the exact-head hosted `suites` job, whose lines match exactly.
- Only these three parent gates ran in the consumer, with `external` and `third_party/verilog-axis` left uninitialised. The gates did not need them: the control reproduced the issue exactly. I did not run the other parent checks the author lists, such as idioms, frontend and integration.
- The build-parallelism cap follows each runner: gsi pins itself to 8 CPUs, srp builds with `-j 8`, and my probe driver pins to 8 CPUs. The pp_top build's own `-j 0` therefore ran on 8 CPUs.
- Termination is argued structurally for the runners' own mutant tables and any edit to the files they mutate. Verilator's own convergence limits, and host or compiler failures, are outside the argument, as the runners already state.
- Physical calibration was NOT RUN, and field skips are not hardware proof. This change touches no hardware path.

## Pending manager duties

- Build and validate the final current-dev candidate at the merge turn (source base `a8f8ce81`, live dev `ffcbd33d`). This round covers source validation only.
- Own hosted/act acceptance for the candidate.
- Obtain the second independent positive (the internal R314 round) under the completion bar.
- Route the out-of-scope `tb/srp_admission/README.md:92` count drift as a new issue if the maintainer agrees.
- Decide whether to take S1 (optional).

R315-1 FINISHED
