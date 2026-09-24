[R310] POSITIVE - exact head af53f79854564bcca35e436758fa625d486c4993

# R310-2 internal independent delta review: processor issue #113 / PR #115

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan
- **Exact head:** `af53f79854564bcca35e436758fa625d486c4993`, tree `6c50bc44d630e12507c298962d2fa859b9cbf3ce`
- **Source base:** `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b`
- **Round-1 head (R310-1):** `29840136bb2d21bc0fbe92c7c533368f40837ff6`
- **Round-2 authored commit:** `4f6185ce97e31f3bdacc090ec1ab7ede32456d2e`. The merge of main `265d6762` (processor #117) gives the exact head.
- **Review start:** PR #115 comment 5823567056. Round-2 assignment: issue #113 comment 5823271483.

## Verdict summary

POSITIVE. Round-1 F1 (MINOR, Tests and Docs) is closed at this head.

- **New coverage:** the response-level test now walks a one across sink 0 (Advertise) and a zero across sink 1 (Failed). Every one of the 32 comparator bits is, at some step, the only bit that differs between two consecutive committed latches, in both directions.
- **Round-1 probes, unchanged:** all four truncations that survived at round 1 ([2:0], [15:0], [30:0], [31:30]) now fail named walk checks. Both of that script's controls pass.
- **Retained mutants:** all six truncation mutants the PR adds ([7:0], [15:0], [31:16], [30:0], [31:30], bit 31 masked) fail their named checks. So do the 14 existing mutants, and the golden and restored controls pass.
- **RTL:** unchanged since round 1, apart from the comment-only edits merged from #117.
- **Merge:** the merge commit is a pure automatic three-way merge. `gsi_mutants.py` keeps both the new mutants and #117's removal of the host deadline.
- **Documentation:** now describes what the test exercises.

No MINOR, MAJOR or BLOCKER finding is open. Both prior MINORs (R310-1 F1 and R311-1-F1) are resolved. The round-1 SUGGESTIONs (R310-1 S1 to S3 and R311-1-SA) are retained. They are optional and do not affect the verdict.

## Independent reconstruction

1. **Contributor rules:** this repository has no AGENTS.md or CONTRIBUTING.md. The contributor rules are `README.md` (gates: suites, lint, `make check`, matrix drift) and `docs/README.md` (single-source rules, citation, MSB-first warning, editing workflow). The per-bench `tb/pp_top/README.md` carries the test and mutation contract.
2. **Frozen scope:**
   - Issue #113 body and decision 5821292534: implement; the trigger is a committed change of `acc_latency[sink]`; unchanged refreshes stay silent; other-sink isolation; a trigger-removal mutant; docs; area.
   - Round-2 assignment 5823271483:
     1. a walking one and a walking zero, each step giving exactly one notification and each unchanged repeat none;
     2. mutants for [7:0], [15:0], [31:16], [30:0] and [31:30], plus bit 31 dropped, each failing a named check and wired into the existing runner;
     3. README and docs wording, with no RTL change;
     4. gates, with existing suite counts identical and the new checks counted separately.
3. **Authority:** Milan v1.2 §5.4.5.2 with Table 5.22, GET_STREAM_INFO row, "MSRP accumulated latency (Stream Input only)". The round-1 conformance check against the printed pages stands. This round changes no RTL and no normative text.
4. **Diff and history:**
   - I read `git diff a8f8ce81..af53f798` in full, and separately the round-2 authored delta `29840136..4f6185ce` and the merge delta `4f6185ce..af53f798`.
   - The merge parents are 4f6185ce and 265d6762, with merge base a8f8ce81. `git merge-tree --write-tree 4f6185ce 265d6762` gives `6c50bc44…`, identical to the head tree, so the merge authors no content (`receipts/merge_identity.txt`).

## Delta verification

### F1 closure (the comparator width is now exercised)

`tb/pp_top/gsi_internal.hpp:302-331` `latency_walks()` runs after the original cases in `latency_changes()` (`:333-347`). At entry, sink 0's latch is 0 (after `latency_refresh(0, 0, …)`, `:343`) and sink 1's is 0xFFFFFFFF (`:344`), so the baselines hold.

For each bit, the walk runs four refreshes:
- baseline→baseline^bit, changed;
- the same value repeated, unchanged;
- a return to baseline, changed;
- the return repeated, unchanged.

Each changed refresh differs from the previous committed latch in exactly the named bit. That gives 128 single-bit changed refreshes and 128 unchanged repeats. Each one runs through the unchanged `latency_refresh()` gate (`:271-297`):
- the exact unsolicited count;
- the byte-exact pushed frame;
- the solicited read;
- other-sink silence and its unchanged latch;
- an empty AECP queue.

**Peer maintenance:** before each bit, a graded unchanged refresh of the peer runs (64 in total). It must stay silent, so a re-registration notification cannot stand in for a latency notification. The mutation results below confirm that no substitution occurs.

**Check tallies:**
- The run prints `GI latency walks added: 5568 checks, 0 failures`.
- The GI total is 6,182, which is 614 + 5,568.
- The full `tb/pp_top` suite has 7,642 checks, which is 2,074 + 5,568.
- The other suite counts are unchanged: hosted srp_top has 1,531 and srp_stream_fsms has 1,087, the same as round 1.

### My round-1 truncation probes, run unchanged

`scripts/r310_probes.py` is byte-identical to the round-1 published copy (sha256 `67b3e356…`). Its results are in `receipts/probes/probes.jsonl`.

| Variant | Round 1 (29840136) | This head |
|---|---|---|
| golden | PASS 614 | PASS 6,182 |
| golden-plus (reviewer additions) | PASS 763 | PASS 6,331 |
| cmp-low3 `[2:0]` | SURVIVES | KILLED: first `FAIL: GI LATENCY-WALK-ONE bit 3 step: exactly one unsolicited response for sink 0, got 0` |
| cmp-low16 `[15:0]` | SURVIVES | KILLED: `… bit 16 step …` |
| cmp-no-bit31 `[30:0]` | SURVIVES | KILLED: `… bit 31 step …` |
| cmp-high2 `[31:30]` | SURVIVES | KILLED: `… bit 0 step …` |
| cmp-*-plus (four) | KILLED-BY-NAMED | KILLED-BY-NAMED |
| trigger-removed, always-pulse, wrong-sink, broadcast | KILLED-BY-NAMED | KILLED-BY-NAMED |

### The PR's own mutation runner, at this head

I used the runner's `mutations()` and `check_variant()` unchanged, with the same edit-site counts and named-failure rule. `scripts/r310_2_runner_split.py` splits them into 7 groups of about 3 mutants, so that each group fits a bounded foreground step. Each group has its own golden and restored control. Results are in `receipts/runner/group*/results.json` and `receipts/runner/driver-g*.txt`.

- **Outcome:** all 20 mutants are detected by their named check, and the golden and restored controls pass in all 7 groups.
- **The six truncation mutants:**
  - low8 is caught at bit 8;
  - low16 at bit 16;
  - high16 at bit 0;
  - low31 at bit 31;
  - high2 at bit 0;
  - bit31-dropped at bit 31.

  Each is a `GI LATENCY-WALK-ONE bit N step: exactly one unsolicited response` failure.
- **Agreement with the author's run:** these results match the author's published round-2 runner log at 4f6185ce.

### Round-2 reviewer probes (new)

These are in `scripts/r310_2_probes.py`, with results in `receipts/probes2/probes.jsonl`. They check the claims that the walks work "in both directions" and that the walking zero adds coverage:

| Variant | Comparator | Result |
|---|---|---|
| golden | unchanged | PASS 6,182 |
| rising-only | `\|(new & ~old)` | KILLED; named `WALK-ONE bit 0 return` present |
| falling-only | `\|(old & ~new)` | KILLED; named `WALK-ONE bit 0 step` present |
| parity | `^(old ^ new)` | KILLED only by the original `LATENCY-CHANGE` case (Hamming distance 10); every single-bit walk passes, as expected |
| sink1-low16 | sink 1 alone truncated to [15:0] | KILLED by `WALK-ZERO bit 16 step` |
| sink1-no-bit0 | sink 1 alone drops bit 0 | KILLED by `WALK-ZERO bit 0 step` |
| sink0-no-bit31 | sink 0 alone drops bit 31 | KILLED by `WALK-ONE bit 31 step` |

### RTL unchanged apart from the merged #117 comments

- **hdl/syn trees:** `hdl` is `83128bca…` at both 29840136 and 4f6185ce. `syn` is `1b062a92…` at 29840136, 4f6185ce and af53f798.
- **Patch identity:** the stable patch-id of `git diff 29840136 af53f798 -- hdl syn` equals that of main's `git diff a8f8ce81 265d6762 -- hdl syn` (`ec6dce31…`; `receipts/rtl_patchid.txt`).
- **What that change contains:** it is comment-only.
  - `KL_aecp_desc_mem_guard.sv:40`: port comment wording;
  - `protocol_processor_top.sv:522-524`: port comment shortened;
  - `:819-820`: the admission-latency comment moved;
  - `:2531-2532` and `:2546`: manager-1 tie-off comments.

### Composed `tb/pp_top/gsi_mutants.py`

- **Round-2 content kept:** the new mutants are at `:23-37`, next to `latency-trigger-removed` at `:20-22`.
- **#117 content kept:** `run()` at `:94-100` calls `subprocess.run` without `timeout=`, with #117's cycle-budget comment. `grep timeout` finds nothing in the file.
- **README agreement:** the 20 `mutations()` entries and the 20 rows of the `tb/pp_top/README.md` mutation table match exactly, both ways (`receipts/readme-vs-runner.txt`).

## Lens results

### Conformance: CLEAN
This round changes no RTL and no normative text. Milan §5.4.5.2 / Table 5.22 (the GET_STREAM_INFO row for Stream Inputs) is still implemented as a committed-latch comparison with unchanged-refresh silence. The walks now show the obligation over the full 32-bit field. The round-1 conformance ledger stands.

### RTL: CLEAN
The hdl/syn delta against round 1 is exactly main #117's comment-only change (patch-id identity above). The latency comparator at `hdl/srp/KL_srp_listener_fsm.sv:738` and its wiring are byte-identical to round 1. The round-1 RTL ledger stands, including the OOC area figures, because the RTL is unchanged. Hosted off-vendor elaboration (portability) passed at this head.

### Robustness: CLEAN
- **Mutants:** direction-only and per-sink truncation mutants are caught, so both transition directions and both sinks are graded.
- **No notification substitution:** peer maintenance is graded silent before each isolated step, so a lapse and re-registration cannot mask a missing latency strobe.
- **Timing:** the long sweep completes in about 30 s per GI run here.
- **Runner:** the composed runner has no host deadline and relies on the bench's own cycle budgets (#117).
- **Clone:** unmodified after all probes.

### Tests: CLEAN
- F1 is closed; the evidence is above.
- **Reruns at this head:** GI focused 6,182 / 0 failures, and full `tb/pp_top` 7,642 / 7,642 (`receipts/pp_top-suite.log`). The hosted push-run suite log shows `suites: 1014613 checks total, 0 failing` and pp_top 7,642 (`receipts/hosted-push-suites-job-log.txt`).
- **Probes:** 14 round-1 variants, 20 runner mutants with 14 controls, and 7 new round-2 variants all give the expected verdicts.

### Docs: CLEAN
- **`tb/pp_top/README.md:59-76`:**
  - it now describes the original cases, the walking one and walking zero, the return-to-baseline single-bit property, the 128 changed and 256 total refreshes, and the 64 silent maintenance refreshes;
  - it notes that the added checks have a separate subtotal;
  - it states that bit 0 is the least significant bit, which avoids confusion with the MSB-first spec tables;
  - all of these match the code;
  - the mutation table (`:92-99`) matches the runner.
- **REQ-NOT-003 (`docs/00_MILAN_COMPLIANCE_REVIEW.md:377`):** now cites the walks and the six truncation mutants. The status stays P, which is correct because other triggers are still partial.
- **Gates:** the documentation gates pass on an extract of the head (lint, wavedrom-check, links, matrix, modmatrix; `receipts/docs-gates.txt`). The freshness gate `make stale` passes in the clone. The hosted docs-gates job succeeded at this head.
- **Retained suggestions:** round-1 S1 and S2 (integrator note; A15/A8 clear) are retained as optional SUGGESTIONs.

## Findings

No open MINOR, MAJOR or BLOCKER.

### S1: SUGGESTION (Docs). Retained from R310-1
`docs/guides/integrator.md:290` and the paragraph that follows could tie the STREAM_INPUT selector 3 answer to the live `srp_acc_latency_o` port, because the processor now pushes on latency changes. Not required.

### S2: SUGGESTION (Docs). Retained from R310-1
`docs/architecture/10_srp_engine.md` §6.4 could state that the A15/A8 clear of `acc_latency[sink]` raises no latency strobe, because the ACMP status notification reports that transition. Not required.

### S3: SUGGESTION (RTL, area). Retained from R310-1
One shared 32-bit comparator, instead of one per sink, would be possible by the same lineage argument as the FailureInformation detector. Optional; +73 LUTs is small.

## Prior public review findings: resolved or retained at this head

I read these only after my own pass and verdict. They come from R310-1 (PR comment 5822538155) and R311-1 (PR comment 5823269222), both at 29840136.

| Prior finding | Disposition at af53f798 | Evidence |
|---|---|---|
| R310-1 F1, MINOR (Tests, Docs): comparator width not covered; README claims full width | **RESOLVED** | The walking one and walking zero isolate all 32 bits. The round-1 probes [2:0], [15:0], [30:0] and [31:30], run unchanged, are now killed by named walk checks. Six retained truncation mutants are killed by named checks. The README wording matches the code. |
| R311-1-F1, MINOR (Tests, Docs): the same gap; its probes narrowed to [7:0], [15:0], [31:16] and bit 31 dropped | **RESOLVED** | Its preferred outcome (a) is met, and more than met. The runner's `latency-cmp-low8`, `-low16`, `-high16`, `-low31` and `-bit31-dropped` are all killed by named `GI LATENCY-WALK-ONE bit N step` checks in my run at this head, which covers the named [15:0] and [30:0] kills. The claim at `tb/pp_top/README.md:65-66` is replaced. |
| R310-1 S1, SUGGESTION (Docs): integrator note | RETAINED, non-blocking | `docs/guides/integrator.md:290` is unchanged. |
| R310-1 S2, SUGGESTION (Docs): the A15/A8 clear raises no strobe | RETAINED, non-blocking | 10 §6.4 is unchanged. |
| R310-1 S3, SUGGESTION (RTL, area): shared comparator | RETAINED, non-blocking | The RTL is unchanged by design. |
| R311-1-SA, SUGGESTION (Tests): wire-level guard that a latency-only change sends no Listener New, plus a mutant feeding the difference into `ind_reg_w` | RETAINED, non-blocking | Not adopted. The head's `listener_news()` is used only in the FailureInformation cases (`gsi_internal.hpp:407,411`), and `gsi_mutants.py` has no such mutant. The behaviour holds at this head: my unchanged round-1 `golden-plus` probe includes `R310 LATENCY wire: a latency-only change sends no Listener New` and passes, 6,331 checks with 0 failures. |

## Reviewer ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 §5.4.5.2 / Table 5.22 (round-1 check stands); issue #113 decision 5821292534 and round-2 assignment 5823271483; the walks as evidence over the full field | R310-1 + R310-2 | af53f79854564bcca35e436758fa625d486c4993 |
| RTL | CLEAN | hdl/syn tree ids at 29840136, 4f6185ce, 265d6762 and af53f798; patch-id identity with main #117; comment-only diff content; hosted portability job | R310-1 + R310-2 | af53f79854564bcca35e436758fa625d486c4993 |
| Robustness | CLEAN | `latency_walks()` baselines and peer maintenance; rising-only, falling-only, parity and per-sink truncation probes; the composed runner without a host deadline; clone integrity after probes | R310-2 | af53f79854564bcca35e436758fa625d486c4993 |
| Tests | CLEAN | `gsi_internal.hpp:271-347`, `gsi_mutants.py` (full), GI 6,182 and pp_top 7,642 reruns, 14 round-1 probes run unchanged, 20 runner mutants with controls, 7 round-2 probes, hosted suites log | R310-2 | af53f79854564bcca35e436758fa625d486c4993 |
| Docs | CLEAN | `tb/pp_top/README.md` (walk text and mutation table against the runner), 00 REQ-NOT-003, the documentation gates locally and hosted | R310-2 (round-1 docs ledger stands for 02/06/10/ooc) | af53f79854564bcca35e436758fa625d486c4993 |

## Evidence consulted (public)

- **Author round-2 packet** at `kebag-logic/milan-fpga@21af9e2e…/review-evidence/pp113-r1/author-r2/`: `round2/mutants.log`, `mutants.json`, `final-integrity.json`, `focused-live-peers.json`, `docs-final.json`, `lint.json`, `parent-consumer.json` and `parent-builder.json`.
  - All of them record processor 4f6185ce, the pre-merge commit, not this head.
  - The runner verdicts there (20/20 with controls) match my independent run at af53f798.
  - The parent consumer and builder show rc 0 at local parent 399cb14f. I did not rerun them, per the review rules.
  - I found no manager-bank receipts for af53f798 inside that tree. I take the manager's static/builder and native bank results from the review brief.
- **Hosted checks at the exact head** (`receipts/hosted-check-runs.txt`):
  - There are two workflow runs: push 36069982021 and pull_request 36069985542.
  - Each has three executed jobs (docs-gates, suites, portability), all success: 6 of 6.
  - In each suites job, only the step "Build Verilator v5.050" was skipped, on a cache hit. That skipped step is a context, not a job. Lint, every suite, matrix and the nvm_port figures executed.
  - The pull_request run reports the PR head SHA. The hosted workflow does not run the GSI mutation runner, which is why I ran it locally.
  - The manager owns hosted/act acceptance.

## Real limits

- **Scope of runs:** I ran focused tests and disposable probes only: GI, full `tb/pp_top`, the documentation gates and the mutation runner, all in isolated extracts. I did not run the full PP, parent, gPTP, off-vendor elaboration or builder banks, OOC synthesis, Docker/act or hardware.
- **Round-1 ledger:** it stands for everything this delta does not touch: the conformance clause reading, RTL internals, area and 02/06/10 docs.
- **Hardware:** physical calibration was NOT RUN. Field skips are not hardware proof. There is no routed-timing claim.
- **Probe status:** the reviewer probe edits are probes only, not proposed patches.

## Pending manager duties

- The final current-dev candidate build and banks at the merge turn: source base a8f8ce81, live dev ffcbd33d.
- Hosted/act acceptance.
- The second independent review ([R311]) at this head.
- The parent re-pin as a separate lane after merge.
- The PR body names processor head 4f6185ce and its round-2 validation. Reconcile it with the published merge head af53f798 when accepting.

## Reproduction

- **Round-1 probes:** `scripts/r310_probes.py --repo <clone> --commit af53f79854564bcca35e436758fa625d486c4993 --work <scratch> --out <dir> --verilator <simulator 5.050> --cpus <cpus> golden golden-plus trigger-removed always-pulse wrong-sink broadcast cmp-low3 cmp-high2 cmp-no-bit31 cmp-low16 cmp-low3-plus cmp-high2-plus cmp-no-bit31-plus cmp-low16-plus`
- **Round-2 probes:** `scripts/r310_2_probes.py …` with the same arguments, variants `golden rising-only falling-only parity sink1-low16 sink0-no-bit31 sink1-no-bit0`.
- **Runner in groups:** `scripts/r310_2_runner_split.py --repo <clone> --work <scratch> --out <dir> --verilator <simulator 5.050> --group G --groups 7 --cpus a,b` for G = 0..6.
- **Clone integrity after all probes** (`receipts/clone-integrity.txt`):
  - HEAD and tree are exact, and the index and worktree equal HEAD.
  - All 246 tracked files were rehashed with 0 byte mismatches, and there are 0 mode mismatches.
  - Index modes and blobs equal the HEAD tree.
  - The repository has no submodule gitlinks (mode 160000).
  - Importing the runner created an ignored `tb/pp_top/__pycache__/`. I inspected it (a single `.pyc`) and removed it. No untracked or ignored entries remain.
- **Tool identity:** `receipts/tools.txt`.

R310-2 FINISHED
