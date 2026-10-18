[R648] POSITIVE - exact head c5afc0a42f200af01dd83e67b579dc3badc42601

# R648-2 independent review: issue #181 / PR #187 (notify-queue to event-router cut), round 2

- **Reviewed:** exact head `c5afc0a42f200af01dd83e67b579dc3badc42601`, tree `90ca8e745ab0842df12e7a98b3f99e002c50bab6`. The previously reviewed head is `42eb9aef`. The delta is three commits on it:
  - `2cacc920`, a merge of processor main `08ae0013` (#176, SET_STREAM_INFO 2013 body);
  - `a0a57895`, comments only;
  - `c5afc0a4`, the in-tree occupancy checks.
- **Reviewer:** R648 (internal reviewer, cleared context, own detached clone), round R648-2.
- **Scope sources, in this order:**
  - The repository has no `AGENTS.md` or `CONTRIBUTING.md`, so I read `docs/README.md`.
  - Issue #181's body, its [A10] assignment (6241709741), the [A10] ruling on acceptance item 1 (6249065327) and REVIEW READY at `c5afc0a4` (6252495012).
  - The round-2 assignment on PR #187 (6249816230), read in full, and the PR body at this head.
  - The authorities the delta cites: `docs/00_MILAN_COMPLIANCE_REVIEW.md:466-467` (REQ-NOT-001/002, Milan v1.2 §5.4.5.1/.2), `:541` (REQ-REU-001), `docs/architecture/02_interfaces.md:16,485` (F02.6) and 06 §7.
  - `git diff 08ae0013..c5afc0a4`, the per-commit diffs and the merge's history.
  - The public evidence at `kebag-logic/milan-fpga@57275d0c` `review-evidence/pp181-r1/author-r2/`.
- **Prior public findings:** I read R648-1 (6249813126) and R649-1 (6249229516) only after my own pass over the diff. Each finding is resolved below.
- **Manager source bank:** none ran at this exact head, and none is claimed or inferred here. Source-head execution evidence is the author's published round-2 receipts, plus my own focused runs listed below.

## Verdict summary

Every check the round-2 assignment asks for holds at this head.

1. **In-tree occupancy checks.**
   - `tb/aecp_notify` OC1 checks `cmdq_nempty_r == (cmdq_count_r != 0)` at every clock edge of all five runs.
   - CQ1 pushes in the clock of a claim and makes that the last push. CQ2 fills the queue to `P-NOTIF-QUEUE-DEPTH` (16) with a push beside the first claim.
   - CQ1b and CQ2b hold `amap_busy_o` from the first push to the last job.
   - My round-1 mutants N4, N5 and N7 each fail named in-tree checks, both in the author's campaign and in my own reproduction:
     - N4 fails CQ1 and OC1;
     - N5 fails CQ1b and CQ2b;
     - N7 fails CQ2 and OC1.
2. **Published receipts.** The round-2 receipts reproduce every round-2 figure in the PR body:
   - OOC: 22 → no path at 1x1, 33 → no path at 8x8; occupancy to select 19 / 21 levels; WNS -4.819 / -4.819 / -10.720 / -5.844 ns.
   - Routed (route-1x1 with #760 at `c5afc0a4`): WNS +0.220 ns and resource gate rc 0. Count to select has no path. Occupancy to select is 22 levels at +3.510 ns. The worst path is `u_aecp/u_ucpu` to `u_aecp/u_d3`, 34 levels.
   - Proofs: router equivalence 91/205/286/505/859 cells with 0 unproven, and five mutants with 2-8 unproven each. Occupancy induction is proven at three shapes; six writer mutants fail it and the reader mutant passes it.
   - The receipts index and the run records mark each receipt with the head it ran at.
3. **The merge kept both sides.**
   - Its tree is exactly `git merge-tree 42eb9aef 08ae0013`. The PR's own delta over `08ae0013` is byte-identical to its delta over `77cf6fb4`, and every main-side file equals `08ae0013`. The one file both sides changed, `06_aecp_engine.md`, is combined.
   - Behaviour at head: `tb/pp_top`'s default build (10017/10017, including the SET_STREAM_INFO rows), `tb/aecp_cmds` (176/176) and `tb/event_router` (81/81) pass.
4. **R649-1-F2.** It is applied word for word, in a comment-only commit. The cited IDs exist.

There is no port, parameter or register-map change: the delta's only `hdl/` edits are comments. No open MINOR, MAJOR or BLOCKER finding remains. Two RESIDUE items and six SUGGESTIONs are listed for the author's single pass.

## Findings

### RES-1 - RESIDUE - Lens: Docs (evidence prose) - "`sha256sum -c sums/MANIFEST-*.sha256` passes" is not true of the published bytes

- **Where:**
  - `review-evidence/pp181-r1/author-r2/HANDOFF.md`, "Step 1: receipts": "`sha256sum -c sums/MANIFEST-*.sha256` passes".
  - `author-r2/receipts-r2/RECEIPTS.md`, first paragraph: "`sums/MANIFEST-<dir>.sha256` [hold] the bytes as published".
- **Evidence:** `receipts/evidence/evidence_check.txt`.
  - At `57275d0c`, eight files report FAILED: `camp/{base,head}/notify/adoption_no_strobe.log`, `camp/{base,head}/notify/results.json`, `route-head760/route.sh`, `scripts/route.sh`, `scripts/chain_parent.sh` and `scripts/ooc_run2.sh`.
  - The evidence root's `MANIFEST.json` lists each of them as `path_redacted: true`. Its `original_sha256` equals the inner manifest's digest, and its `published_sha256` equals the published bytes. The redaction was applied at publication.
  - All 1940 `author-r2/` files match `MANIFEST.json`, and no file on disk is unlisted.
- **Impact:** wording only. The integrity chain is intact through `MANIFEST.json`, and no figure, verdict, test or code depends on the sentence. Still, a reader who follows the instruction sees eight FAILED lines.
- **Exact fix:** after "`sha256sum -c sums/MANIFEST-*.sha256` passes" in HANDOFF.md, and at the end of RECEIPTS.md's first paragraph, add: "At publication, eight files were redacted further (`camp/base/notify/adoption_no_strobe.log`, `camp/base/notify/results.json`, the same two under `camp/head/notify/`, `route-head760/route.sh`, `scripts/route.sh`, `scripts/chain_parent.sh`, `scripts/ooc_run2.sh`). For these, `sums/MANIFEST-*.sha256` holds the digest before that step, so `sha256sum -c` reports them FAILED. The evidence root's `MANIFEST.json` records both digests, and every published byte matches it."
- **Verification:** run `scripts/verify_evidence.sh` from this packet. Exactly those eight files must fail, and `MANIFEST.json` must show 0 mismatches.

### RES-2 - RESIDUE - Lens: Docs (PR body) - the campaign-record identity sentence is narrower than the records

- **Where:** PR #187 body, "Gates at the round-2 head", second bullet: "Every record is identical once line numbers are normalised, except the notify campaign's eleven new arms and its golden run's tally."
- **Evidence:**
  - The base and head notify records also differ in 41 existing arm logs and in four golden logs (identify, interfaces, collision, failure-window). Each differs only in its own tally line. For example, `[build default] 42 checks, 4 failures` became `51 checks, 4 failures`, and `[build interfaces] 19 checks` became `20 checks`. The reason is that every `tb/aecp_notify` run gains OC1, and the default run also gains CQ's eight checks.
  - `camp_compare_lines.py` grades lines matching `checks?:`, so it does not see the `N checks, M failures` form. It also prints only the first 12 of its 13 differing records; the 13th is `results.json`.
  - My own compare: no arm present at both base and head changes its verdict or its failing-check set.
- **Impact:** wording only. No verdict, figure or kill changes.
- **Exact fix:** replace the sentence with: "Every graded record is identical once line numbers are normalised, except in the notify campaign: its eleven new arms, its golden run's tally and `results.json`. Each `tb/aecp_notify` run's own tally line (`N checks, M failures`) grows by the new checks (OC1 in every run, and CQ's eight in the default run). No existing arm changes its verdict or its failing checks."
- **Verification:** compare `camp/base/notify` with `camp/head/notify`, including tally lines.

### S-1 - SUGGESTION (retained from R648-1 S-1) - Lens: Docs (source comment) - `hdl/packet_engine/KL_pp_event_router.sv:104-105`

This comment was not touched by the delta. The first sentence still reads "minus the event delivered this cycle; base = one past the delivered source". The paragraph at `:110-118` qualifies it. Consider "minus the presented event (it leaves on its delivery); base = one past the presented source".

### S-2 - SUGGESTION (retained from R648-1 S-2) - Lenses: Tests, Docs

- Router mutants R4 (the select reloads outside the enable) and R5 (no grant clears the select) are still killed only by the out-of-tree equivalence. If the idle `evt_src_o` / `evt_payload_o` value is part of the contract, a `tb/event_router` check would pin it.
- In `syn/ooc/README.md:261`, "Worst path from `cmdq_count_r`: 2 levels" sits above a 3-level row. "Worst (least slack)" would remove the apparent contradiction.

### S-3 - SUGGESTION - Lens: Docs - `syn/ooc/README.md:243-247`

The record names its base (`22c139a4`) but not the change's head. With the same RTL logic, this head measures 19 (1x1) / 21 (8x8) levels from occupancy to select, not 22, because main's merges changed the engine. Consider "against base `22c139a4` and the change on that base (`16c89c53`)".

### S-4 - SUGGESTION - Lens: Tests (evidence) - publish the #760 patch

The route's #760 composition is identified by three things:
- the branch sha `22840662`;
- the patch sha256 `003e4985…` (`route-head760/chain.txt`);
- the working-tree status in `route.out`.

The commit is not retrievable from the public parent repository (`receipts/evidence/evidence_check.txt`; the API answers "No commit found"). Publishing the patch file beside `chain.txt` would let a reader rebuild the "+#760" input from public files alone.

### S-5 - SUGGESTION - Lens: Tests (evidence) - stamp the head in each campaign receipt

`scripts/campaigns.sh` records `git status --short` after the run, but not `git rev-parse HEAD`. Each campaign's head is established only by the chain: `gates.sh` stamps `c5afc0a4` in the same lane first, and the status after the run is clean. One `echo "head $(git rev-parse HEAD)"` in `done.txt` would make each campaign receipt self-identifying.

### S-6 - SUGGESTION - Lens: Tests (evidence tooling) - `camp_compare_lines.py`

Grade `N checks, M failures` tally lines, and list every differing record instead of the first 12. This would have surfaced RES-2 mechanically.

## Prior findings at this head

| Finding | Severity | Status at `c5afc0a4` | Evidence |
|---|---|---|---|
| R648-1 F-1 (receipts) | MINOR | **CLOSED** | `author-r2/receipts-r2` at `57275d0c` holds the gate logs; the OOC and route reports with exact commands (`scripts/`, the Vivado `Command :` lines); and the proof, control and mutant logs. Each has its head, in `RECEIPTS.md`'s index and in the run records (`logs/*/env.txt`, `ooc/chain-ooc.txt`, `route.out`, `pgates/*/gitlink.txt`, proof sources byte-equal to `git show c5afc0a4:` / `08ae0013:`). I re-derived every round-2 figure in the PR body from them (`receipts/evidence/evidence_check.txt`). Wording residue: RES-1. |
| R648-1 F-2 (duplicated occupancy state) | MINOR | **CLOSED** under the manager's round-2 disposition (assignment item 2) | `tb/aecp_notify` sections CQ and OC (`sim_main.cpp:47-75,968-1113`, `port_tuple.hpp:74,91,634`, `occupancy.vlt`). Every posedge in both harnesses goes through the sampled `tick()` (`sim_main.cpp:140,1194`, `port_tuple.hpp:89`), so OC1 does see every edge. N4 → CQ1 + OC1, N5 → CQ1b + CQ2b, N7 → CQ2 + OC1, in the author's campaign (`camp/head/notify`, 109/109) and in my reproduction (`receipts/occupancy/`). The arms use my round-1 edits verbatim (`r648-inputs/`). Part (a)'s router-equivalence gate was not taken into the assignment; its residue is S-2. |
| R648-1 RES-1 (PR body first paragraph) | RESIDUE | **CLOSED** | The PR body's first paragraph is the exact fix text. |
| R648-1 S-1, S-2 | SUGGESTION | **RETAINED** as S-1, S-2 | not applied (HANDOFF "Not done, and why") |
| R649-1-F1 (receipts) | MAJOR | **CLOSED** on this reviewer's evidence check | Identities (processor head/base, parent `7d79ffb2`, #760 branch and patch digest, tool builds), commands and rc files, the unchanged recipe, OOC queries and reports, routed timing and the resource-gate output, and proof/control/mutant scripts and logs are all published, with head per receipt. #760's inclusion is shown by `chain.txt` (apply rc 0, revert rc 0, the round-1 patch digest) and the working tree in `route.out`. The limit on the patch's public content is S-4. |
| R649-1-F2 (comment traceability) | RESIDUE | **CLOSED** | `a0a57895` replaces `(issue #181)` with `(issue #181; REQ-NOT-001, REQ-NOT-002)` at `KL_aecp_notify.sv:426`, and with `(issue #181; REQ-REU-001, F02.6)` at `KL_pp_event_router.sv:110`, exactly. It changes nothing else in `hdl/` (`receipts/merge/merge_check.txt`). |

## Lens evidence

**Conformance.**
- The notification obligations (REQ-NOT-001 fan-out to every registered controller but the requester, at each controller's next sequence_id; REQ-NOT-002 every successful state-changing command) are now graded by CQ through a full queue. The same jobs and the same `amap_busy_o` trace pass on the RTL before the flop: my `baseRTL` arm runs `08ae0013`'s `KL_aecp_notify.sv` under the head's bench, 76/76, with a probe-only wire for the monitor. So the cut changes no notification behaviour.
- #176's SET_STREAM_INFO behaviour is kept beside the cut: `tb/pp_top` default build 10017/10017 and `tb/aecp_cmds` 176/176 at head.
- The ruling's purpose holds at this head: route-1x1 with #760 closes at +0.220 ns, above the +0.030 ns floor. The worst path is outside the cone, and no path runs from count to select.

**RTL.**
- In both RTL files, the delta changes only comments. The logic and its round-1 verdict carry, and the delta changes nothing they depend on: main's merge touches neither file and no interface they use.
- The author's proofs re-ran on the head's exact bytes: router equivalence at `N_SRC_P` 1, 5, 8, 16 and 29 with 0 unproven, and occupancy induction at three shapes.
- The writer sites are unchanged: `KL_aecp_notify.sv:1196-1197` (reset), `:1299-1300` (push) and `:1508-1513` (pop, with the push-beside-pop hold). The readers are unchanged too: `:833` and `:1166`.
- `occupancy.vlt` is bench-only (`public_flat_rd`) and changes no RTL.

**Robustness.**
- The duplicated state is now guarded in tree on every run of all three builds.
- An extra arm of my own, N8 (a pop clears the occupancy one entry early, `!= 5'd2`), fails OC1, CQ1, CQ2, DR2 and DR2b.
- CQ2 drives the queue to its depth of 16 with one entry in the round. Every entry is delivered in order: 26 jobs.

**Tests.**
- My runs at head: `tb/aecp_notify` `make check` 80/80. The README's 51 + 5 + 20 + 4 is confirmed per run.
- The author's receipts at head:
  - `run_suites.sh`: 1030013 checks, 0 failing; base 1030000.
  - Req-tags: 227 evidence lines; base 226.
  - `lint_hdl`, `make check`, `gen_matrix --check`, `syn/yosys/run.sh` and the elaboration guards: rc 0, with a clean status afterwards.
  - Ten campaigns: rc 0. Notify kills 109 of 109; base 98 of 98.
  - Parent consumer rc tables: identical at base and head, and the ROM digests are identical.
  - The three rc-1 rows (`check_submodule_docs`, `measure_test_evidence` and its self-test) have byte-identical logs at base and head.
- Hosted runs at the exact head (snapshot `receipts/hosted/hosted_snapshot.txt`): `docs-gates` and `portability` completed successfully. `suites` is still in progress, and its "Build Verilator v5.050" step is skipped (a setup step, not a validation job).

**Docs.**
- The `09_verification.md` CQ and OC rows and "nine of the notification block's" are correct.
- The `06_aecp_engine.md:998` sentence is correct, and so are the `tb/aecp_notify/README.md` tallies and mutation record. The record matches `camp/head/notify` arm by arm.
- The PR body's round-2 figures match the receipts.
- Comment rule: the delta adds no lane label, review round, reviewer ID or issue-comment ID to any source comment. Its comments state behaviour and reason with issue and requirement IDs.
- Wording residue: RES-1 and RES-2.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #181, the item-1 ruling and the round-2 assignment; REQ-NOT-001/002, REQ-REU-001, F02.6; CQ on head and base RTL; `tb/pp_top` default build and `tb/aecp_cmds` at head; route-1x1 with #760 reports | R648-2 (delta); R648-1 (unchanged logic) | c5afc0a42f200af01dd83e67b579dc3badc42601 |
| RTL | CLEAN | `git diff 08ae0013..c5afc0a4` and the per-commit diffs; the writer/reader sites of `cmdq_nempty_r`; merge tree versus `merge-tree`; proof sources byte-checked; no port, parameter or register-map change | R648-2; logic R648-1 | c5afc0a42f200af01dd83e67b579dc3badc42601 |
| Robustness | CLEAN | OC1 sampling coverage across every posedge path; CQ1/CQ2 queue-boundary cases; N4/N5/N7 plus my extra N8 | R648-2 | c5afc0a42f200af01dd83e67b579dc3badc42601 |
| Tests | CLEAN | my `tb/aecp_notify` arms (head, baseRTL, N4, N5, N7, N8), `tb/pp_top` default, `tb/aecp_cmds`, `tb/event_router`; the author's gate, campaign, proof, OOC, route and parent-gate receipts; hosted snapshot | R648-2 | c5afc0a42f200af01dd83e67b579dc3badc42601 |
| Docs | CLEAN (RES-1, RES-2 carried to the residue checklist) | `09_verification.md`, `06_aecp_engine.md:998`, `tb/aecp_notify/README.md`, `syn/ooc/README.md`, PR body, HANDOFF.md, RECEIPTS.md, `MANIFEST.json`; comment-rule scan of the delta | R648-2 | c5afc0a42f200af01dd83e67b579dc3badc42601 |

## Real limits

- I ran no Vivado. The OOC and routed figures were checked against the published Vivado reports, including their embedded `Command :` lines; I did not re-derive them. The OOC and route runs are the author's.
- The #760 patch content is identified by its digest only, and the commit is not publicly retrievable (S-4).
- This round I did not re-run the router equivalence or the occupancy induction. The proof sources are byte-equal to the head's, the logic is unchanged since my round-1 proofs at `42eb9aef`, and the author's round-2 logs show the same results.
- I did not run `run_suites.sh`, the mutation campaigns, the lint, matrix, Yosys or req-tag gates, the elaboration guards, `tb/pp_top`'s six override builds, or any parent consumer gate. For these I rely on the author's receipts.
- The hosted `suites` jobs were in progress at the snapshot.
- Physical calibration NOT RUN. No hardware claim is made.

## Pending manager duties

- The current-dev merge-candidate builder and native banks at the merge turn (source base `08ae0013`, live dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`), with receipts linked on the PR.
- Hosted/act acceptance, including the in-progress `suites` jobs of runs 39146743313 and 39146740703.
- Disposition of the parent rows that return rc 1 at both base and head:
  - the documented pin;
  - the test-evidence ratchet and its self-test, which list `tb/aecp_cmds/mutants.py`, `tb/elab_guards/guards.py` and `tb/elab_guards/mutants.py` without a disposition.
- The re-measure of route-1x1 on the next pin adoption's image, as the ruling records.
- RES-1 and RES-2 on the residue checklist.
- The second independent review (R649-2); merge needs two POSITIVE reviews.

## Packet

- `scripts/`: the portable probe scripts. Paths are arguments, and the tool path can be set with `VERILATOR`.
  - `probe_cq.sh`: the occupancy arms.
  - `probe_compose.sh`: the merge-composition suites.
  - `verify_evidence.sh`: the published-receipt checks.
- `receipts/`: raw logs, rc files and summaries, with host paths redacted.
  - `occupancy/`, `compose/`, `evidence/`, `merge/`, `hosted/`, `integrity/` and `tools.txt`.
  - Tool identity: Verilator 5.050 (`2026-07-01 rev v5.050`), the pinned wrapper, sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`.
- `MANIFEST.sha256` lists every published file except this report.
- Every probe ran on `git archive` exports under the unpublished `scratch/`. Afterwards the review clone was checked (`receipts/integrity/clone_integrity.txt`):
  - HEAD and tree are exact, and `git status` is empty, ignored files included;
  - all 633 tracked blobs match in bytes and modes, and the index equals HEAD;
  - the tree has no submodule gitlinks.

R648-2 FINISHED
