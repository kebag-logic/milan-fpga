[R502] POSITIVE - exact head ad670a71b4d2f38f59672d51d8309d59ffed0808

# R502-2: internal independent review of processor PR #164 (Closes #42), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #164, branch `pp42-domain-notify`.
- Exact head `ad670a71b4d2f38f59672d51d8309d59ffed0808`, tree `224aadfa2ffc348ad3123bd4580b573a7d97c098`; source base
  `main` `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`.
- Round 2 delta over R502-1's head `72facc6d`: the author's `--no-ff` merge of processor main `7e5415e0` (#134,
  `0f5562b`), the author's correction `9be9cd7a` (assignment 6011607356), and the manager's `--no-ff` merge of main
  `86a7b0c5` (#22, `ad670a71`). Review start: PR #164 comment 6014810222.
- The PR's own change against current main `86a7b0c5` is test and documentation only: `tb/pp_top/{notify_phases.hpp,
  sim_main.cpp, notify_mutants.py, README.md}` and `docs/architecture/09_verification.md`, +309 -12. No `hdl/`, `syn/` or
  `scripts/` line belongs to the PR. Every `hdl/` line in `e6a759de..ad670a71` arrives through the two merges.

## Verdict

POSITIVE. The round-1 MINOR is resolved at this head (R502-1 F1.1, and F1.2 = R503-1 F1). Every acceptance item of
#42 and every lane item still holds after both merges. I reproduced each one. Both merges are exact re-merges of
their parents, with no hand edits. pp_top passes at 10,459 checks. The notify campaign is 65 of 65 KILLED with 8
goldens PASS, and all 65 README record rows match the observed failing counts. The four suites fed by the merged
files pass. Two RESIDUE items are recorded. They are wording only and do not make the verdict NEGATIVE. There is no
BLOCKER, MAJOR or MINOR.

## How the review was reconstructed

1. Guidance. This repository tracks no `AGENTS.md` or `CONTRIBUTING.md` (checked with `git ls-files`). The governing
   conventions are `README.md` and `docs/README.md`: ID registries, single-source rules, and what `make check`
   enforces.
2. Scope:
   - the issue #42 body (REQ-NET-002, acceptance 1-4, GAP-04);
   - the manager's lane comment 6008771904 (items 1-6, STOP conditions, gates);
   - the round-2 assignment 6011607356 (the latency figure, the spacing statement, the merge of `7e5415e0`, re-run of
     the pp_top campaign, the notify mutants and the merged files' suites);
   - the TAKEN and REVIEW READY notices;
   - the PR #164 body, including the manager's note on the `86a7b0c5` merge.
3. Authorities:
   - `docs/00_MILAN_COMPLIANCE_REVIEW.md:489` (REQ-NET-002);
   - `docs/architecture/06_aecp_engine.md:263,1010-1011` (the GET_AVB_INFO async triggers, which include domain
     class-A priority/VID; `T-CTR-NOTIF` limits GET_COUNTERS only);
   - `08_timing.md:27,33` (`T-NOTIF-MONITOR` 30-60 s, `T-CTR-NOTIF` 1 s);
   - the landed RTL: `protocol_processor_top.sv:3176-3180,4018-4020`, `KL_srp_domain.sv:155-184` and
     `KL_aecp_notify.sv:666-671,1073,1311,1333`.
4. Diff and history. I read the full diff `e6a759de..ad670a71` and split it into the PR's own change (against
   `86a7b0c5`) and the merged main. I re-merged both merges with `git merge-tree --write-tree`.
5. Executable evidence:
   - the public packet `kebag-logic/milan-fpga@355c335c:review-evidence/pp42-r1` (MANIFEST.json, and the round-1
     author handoff and PR body at `72facc6d`, whose hashes match the manifest);
   - the exact-head hosted checks;
   - my own runs (receipts below).

   I found no manager evidence comment for this exact head on the issue or the PR. The issue has only the round-2
   assignment and the TAKEN and REVIEW READY notices.

I wrote this verdict, the findings and the ledger from my own pass over the diff and my own runs. Only after that did I
read the prior public findings (resolved in their own section below).

## Findings

### R1 - RESIDUE - lens: Docs - the first build's "Runs" cell does not name section DN

- **Where:** `tb/pp_top/README.md:1825`, the build table row for `obj_dir/Vpp_top_sim`: "every section, DV, AX, DL, D3,
  D3V and D3KR among them, then lane C6's ID0, NP, ST and RN, and lane C7's K9 to K17 last".
- **Evidence:** `sim_main.cpp:14080-14081` runs `run_domain_notify` (and `run_spacing`) in the first build's full run.
  `receipts/pp_top_full_head.log:273-279` shows DN's lines in that run. The Lane C6 intro (`README.md:2229`) counts DN
  among C6's eight sections. The cell already left out CS before this PR, and this PR adds a second omission.
- **Why RESIDUE:** this is prose only. It changes no figure, count, check, verdict or code, and "every section" already
  covers DN.
- **Exact fix:** "... then lane C6's ID0, NP, ST, RN, CS and DN, and lane C7's K9 to K17 last".

### R2 - RESIDUE - lens: Docs - the PR body's opening names the author's head, not the published head

- **Where:** the PR #164 body. Its first paragraph says "head `9be9cd7a`, five commits". Its Round 2 section says "#22
  ... merged later ... so this head does not contain it". The published head `ad670a71` does contain #22, through the
  manager's merge. The closing "Manager note (A10)" reconciles this, so the facts are on the page.
- **Why RESIDUE:** this is PR-body wording only. The validation figures are correctly labelled as measured at
  `9be9cd7a`. My runs at `ad670a71` give the same pp_top count (10,459), the same campaign result (65 of 65) and the
  same srp_top (8,656) and srp_stream_fsms (1,347) counts.
- **Exact fix:**
  - Open with "Author head `9be9cd7a` (five commits ...). The PR head `ad670a71` adds the manager's `--no-ff` merge of
    main `86a7b0c5` (#22, no shared file)."
  - Change "so this head does not contain it" to "so the author's head `9be9cd7a` does not contain it; the manager's
    merge `ad670a71` does".

No BLOCKER, MAJOR or MINOR. No SUGGESTION beyond those already on record (R502-1 S1 and S2, which the PR body lists as
not taken and which stay optional).

## Round-2 focus items, each verified at the exact head

| Item | What was required | Evidence at `ad670a71` | Result |
|---|---|---|---|
| R502-1 F1.2 = R503-1 F1: latency | DN's latency stated from the MRPDU's last byte (499) or from `feed()`'s return (495) with the 4-clock offset, and agreeing with the trace in the README, the PR body and the probe log | `README.md:2497-2500`: "[i] lines time ... from ... the return of `feed()`, which clocks four idle cycles after the MRPDU's last byte ... 495 clocks after `feed()` returns, so 499 after the MRPDU's last byte"; link edge 466. Bench comment `notify_phases.hpp:1709-1710` says the same. PR body Round 2 "Latency" bullet says the same. My print-only probe (`receipts/probe_dn_clocks.{diff,log}`): last byte 340,030, `feed()` returns 340,034, frame at 340,529 (499/495); 580,098, 580,102, 580,597 (499/495); link edges 100,000 to 100,466 and 220,000 to 220,466. The unmodified full run prints `[i]` 466, 466, 495, 495 (`pp_top_full_head.log:273-276`) | resolved |
| R502-1 F1.1: spacing | statement corrected to what the bench does, or bench changed | The author chose the text. `README.md:2506-2517`, `notify_phases.hpp:1663-1665,1689` and the PR body's Round 2 "Spacing" bullet and item-6 row all now say: `space_out` waits 1,000 ms after the latest *notification* to A; the REGISTER response is not counted; the first stimulus is at clock 100,000, 96,536 clocks (965 ms) after that response; every later stimulus follows the previous 1.2 s window directly, at least 1,000 ms after the latest notification. The probe shows: REGISTER response to A at 3,464; `space_out` returns at 100,000 (`last_sent` 0), 220,000 (100,466), 340,000 (220,466), 460,034 (340,529), 580,068 (340,529), 700,102 (580,597). Every gap is at least 100,000 clocks. Span 8,167 ms. The bench logic is unchanged (`9be9cd7` touches only `//!` comments and README prose), so the 15 checks and the nine controls are unaffected; both re-run green below | resolved |
| Author's merge of `7e5415e0` (#134) | `--no-ff`; pp_top, notify mutants and the merged files' suites pass | `0f5562b` re-merges to the identical tree `692d8f4c` (`receipts/merge_remerge.txt`). `tb/srp_top` 8,656/8,656, `tb/srp_stream_fsms` 1,347/1,347 (both match the PR body); pp_top 10,459/10,459 | pass |
| Manager's merge of `86a7b0c5` (#22) | shares no file with the PR; pp_top, notify mutants and the merged files' suites pass | `ad670a71` re-merges to the identical tree `224aadfa`. #22 changes `KL_pp_originator.sv` and `KL_pp_rx_validator.sv` only (declarations moved above first use); the PR's own files are disjoint. `tb/originator` 107/107, `tb/rx_validator` 555/555, pp_top 10,459/10,459, notify campaign 65/65 (it builds `tb/originator` and plants four arms in `KL_pp_originator.sv`). Static plant check: 397 arms or patches across nine drivers that build pp_top or a merged file, 0 refused | pass |

## Acceptance trace at the exact head

| Item | Check(s) | Reviewer evidence | Result |
|---|---|---|---|
| #42-1 / lane 1: A registered, a differing Class A Domain gives exactly one u=1 GET_AVB_INFO for AVB_INTERFACE 0, byte-exact, and no GET_AS_PATH | <bench-switch-model> (premise), DN1b, DN1c (`sequence_id` 2) | pp_top full run and the DN golden pass. Probe: frame to A #3 at 340,529, u 1, ct 0x0027, seq 2, SUCCESS. `asp_takes_domain` kills DN1b and DN2b | met |
| lane 2: the declaration back to the default gives exactly one more | DN2 (premise), DN2b, DN2c (`sequence_id` 3) | pass. The strobe is the adoption arm `KL_srp_domain.sv:184`; `adopted` stays 1 (`[i]` line), as the README says | met |
| #42-2 / lane 3: an identical re-declaration sends nothing | DN3, DN3b | pass. `domain_same_readopted` kills both. My `avb_takes_adopted_level` arm shows DN3 and DN3b catch frames that arrive with no DOMAIN_CHANGE ("saw 0 ... got 288 frames") | met |
| #42-4 / lane 4: the link-edge leg | DN4b-DN4e, DN4 (premise) | pass. `avb_link_term_dropped` kills DN4b-e. My `link_rise_only` kills DN4b and DN4c. My `link_level_while_down` kills DN4b (287 frames), which shows "exactly one" catches duplicates | met |
| #42-3 / lane 5: removing `srp_evt_domain_change_w` turns items 1 and 2 red; each new check has a control; existing arms still plant | 9 controls | `receipts/notify_mutants_head_results.json`: `avb_domain_term_dropped` fails exactly DN1b, DN1c, DN2b, DN2c (run rc 1). All nine controls fail exactly the README's sets. 65 of 65 KILLED, 8 goldens PASS. `record_vs_results.log`: all 65 README rows match the observed failing counts | met |
| lane 6: rate limit respected, not weakened | spacing in the bench; no RTL change by the PR | 06 §7 limits only GET_COUNTERS (`T-CTR-NOTIF`). GET_AVB_INFO is one pending bit (`KL_aecp_notify.sv:1073,1311`). The probe shows every stimulus at least 1 s after the latest notification. The span (8,167 ms) is under `T-NOTIF-MONITOR`'s 30 s floor | met |
| STOP: only the pp_top count moves | | pp_top 10,459 (first build 9,971; others 20/178/231/56/3). srp_top and srp_stream_fsms move only through #134, and they match the PR body's figures | met |

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REQ-NET-002 (00:489) and 06:263,1010-1011 (GET_AVB_INFO triggers include domain priority/VID; only GET_COUNTERS is rate-limited). The `avb_info()` oracle (`notify_phases.hpp:1671-1685`): GET_AVB_INFO offsets 24/26/28/36/44, u bit, SUCCESS, cdl 40. Per-entry `sequence_id` 0-3 on the wire (probe), modelled from the wire (Milan 5.4.5.1). Domain vector {5,2,VID}x2 per S8. Round-2 delta changes no oracle | R502-2 | ad670a71b4d2f38f59672d51d8309d59ffed0808 |
| RTL | CLEAN | PR-own delta has no `hdl/` line. Merged RTL: #134's `KL_srp_listener_fsm.sv`/`KL_srp_talker_fsm.sv` and #22's `KL_pp_originator.sv`/`KL_pp_rx_validator.sv`, both merges exact re-merges. Planted RTL (`protocol_processor_top.sv:4018-4020`, `KL_srp_domain.sv:157,184`, `KL_aecp_notify.sv:668,1333`, `restore_done_o`) unchanged, and each anchor is unique (plant check). Suites fed by the merged RTL pass (srp_top, srp_stream_fsms, originator, rx_validator, pp_top) | R502-2 | ad670a71b4d2f38f59672d51d8309d59ffed0808 |
| Robustness | CLEAN | DN runs on its own model, so the main timeline does not move. The windows are contiguous: late frames land in the next window, and the tail after DN3b is S1, optional. 3 reviewer arms plus a golden, all as expected: duplicates (287 frames), a missing link edge, and notifications without a strobe are each caught. The spacing gaps come from the probe. Merged-RTL suites pass, with peak RSS at most 0.5 GB per build | R502-2 | ad670a71b4d2f38f59672d51d8309d59ffed0808 |
| Tests | CLEAN | `notify_phases.hpp:1642-1849`. `9be9cd7` changes comments only. `sim_main.cpp:14049-14081` flag wiring. `notify_mutants.py` DOMAIN_NOTIFY. pp_top six builds 10,459/0. DN golden 15/0. Campaign 65/65 + 8 goldens. Static plant 397/0. Record against results 65/0. Probe log matches README and PR body | R502-2 | ad670a71b4d2f38f59672d51d8309d59ffed0808 |
| Docs | CLEAN (RESIDUE R1, R2 recorded) | `tb/pp_top/README.md` (C6 intro: eight sections, which I counted at `notify_phases.hpp`; section DN latency and spacing text at 2497-2517; mutation record of 65 rows). `09_verification.md` §8.4 row and flag. `notify_mutants.py` docstring. The PR body's Round 2, Acceptance and controls tables. Docs gates links, matrix, modmatrix, params, ids, figures and stale, `gen_matrix --check` and `git diff --check`: all rc 0. Hosted docs-gates succeeded at this head | R502-2 | ad670a71b4d2f38f59672d51d8309d59ffed0808 |

## Prior public review findings at this head

At reading time, PR #164 has no formal reviews and no inline comments. It has two public reports, R503-1 (6011470805)
and R502-1 (6011601546), plus review-start notices.

| Prior finding | Status at `ad670a71` | Basis |
|---|---|---|
| R502-1 F1 (MINOR, Tests+Docs), part 1 (F1.1): first-stimulus spacing stated as "at least 1,000 ms after the latest frame to A" | **RESOLVED** | The README (2506-2517), the bench comments (1663-1665, 1689) and the PR body now say "after the latest notification", exclude the REGISTER response, and give 100,000 / 96,536 clocks (965 ms). My probe reproduces each clock |
| R502-1 F1 part 2 (F1.2) = R503-1 F1 (MINOR, Docs): "495 after the MRPDU's last byte" | **RESOLVED** | The README (2497-2500), the bench comment (1709-1710) and the PR body now say 495 after `feed()`'s return, which is 499 after the last byte. My probe: 340,030, 340,034, 340,529 and 580,098, 580,102, 580,597 |
| R502-1 S1, S2 (SUGGESTION) | carried, optional | The PR body lists both as not taken. They are outside #42's acceptance |
| R503-1 F1's request to carry the correction into "the next public evidence summary" | done in the PR body. The evidence part is pending with the manager | The immutable round-1 handoff (`355c335c`) still carries the old caption. Superseding it in published evidence is a manager duty (below) |

## Receipts (all listed in MANIFEST.sha256)

- `scripts/run_r502_2.sh`: the commands, as run.
- `scripts/vl_jcap.sh`: the pinned Verilator wrapper that caps `--build -j 0` to `-j N`. It changes build parallelism
  only.
- `scripts/probe_dn_clocks.py`: the print-only probe. `scripts/extra_dn_mutants.py`: the reviewer arms.
  `scripts/plant_check.py`: the static plant check. `scripts/record_vs_results.py`: README record against results.
- `receipts/tool_identity.txt`: Verilator 5.050 rev v5.050 (wrapper sha256 `905795b9...e92f`). GNU Make 4.4.1, Python
  3.14.7, g++ 16.2.1. The system's 5.052 was not used.
- `receipts/probe_dn_clocks.{diff,log,rc}` and `receipts/probe_build.{log,rc}`: DN 15/0 with the trace.
- `receipts/pp_top_full_head.{log,rc}`: six builds, 10,459/0, rc 0.
- `receipts/suite_{srp_top,srp_stream_fsms,originator,rx_validator}.{log,rc}`: 8,656, 1,347, 107 and 555 checks, 0
  failures each, rc 0.
- `receipts/notify_mutants_head.{log,rc}` and `receipts/notify_mutants_head_results.json`: 65/65 KILLED, 8 goldens
  PASS, rc 0.
- `receipts/extra_dn_mutants.{log,rc}` and `receipts/extra_dn_mutants_results.json`: golden PASS and 3/3 KILLED.
- `receipts/plant_check.{log,rc}`: 397 arms, 0 refused. `receipts/record_vs_results.{log,rc}`: 65 rows, 0 mismatches.
- `receipts/docs_gate_*.log`, `receipts/docs_gates.rc` and `receipts/gen_matrix_check.log`: all rc 0.
- `receipts/merge_remerge.txt`: both merges are identical re-merges. It also holds the PR-own and #22 diffstats and the
  graph.
- `receipts/resources.txt`: peak RSS at most 0.5 GB per build. pp_top wall time was 14 min and the campaign's 12.8 min,
  run concurrently.
- `receipts/hosted_checks_snapshot.txt` and `receipts/clone_integrity.txt`.

Harness notes:
- Builds ran in `git archive` copies under `scratch/`. The `ids`/`figures` gates need a git worktree, so they ran in a
  scratch local clone at the exact head; a first attempt in a plain archive failed only for that reason.
- Home-directory paths in logs are replaced by `<VERILATOR_IMAGE>` and `<HOME>`.
- The review clone was never written to. `clone_integrity.txt` shows HEAD and tree exact, the index tree equal to HEAD,
  an empty `status --porcelain --ignored`, and all 562 tracked entries byte- and mode-exact. The repository has no
  submodule gitlinks (no `.gitmodules`, no mode-160000 entries), so there are none to verify.

## Real limits

- Not run, by the owner restriction on full banks:
  - `./scripts/run_suites.sh` (all suites);
  - `lint_hdl.sh` and Yosys;
  - `make check`'s Mermaid `lint` and `wavedrom-check` (no changed doc block holds Mermaid or WaveDrom, and hosted
    docs-gates succeeded at this head);
  - the parent consumer set of 17 (parent dev `28f9666f` with the 148 and 22 patches).

  The merged RTL is exercised here only through the five suites that build it.
- The other pp_top-building campaigns (d3, aecp, aecp_dispatch, acmp, ctr, gsi, name_wr, and the pp_top arms of
  adp_engine and maap) were checked statically only, by plant and `git apply --check` at the head. Their dynamic
  verdicts at this head rest on the author's and manager's evidence.
- I found no public exact-head evidence packet for `ad670a71`. The public packet at `355c335c` holds round-1 material
  for `72facc6d`.
- Physical calibration NOT RUN. No hardware or bench access. Field skips are not hardware proof.

## Pending manager duties

- Hosted/act acceptance. Snapshot at 2026-10-06T11:19:51Z: `docs-gates` and `portability` succeeded on both runs
  (37453485468, 37453477982); `suites` was still in progress on both and is not counted as a pass.
- The final current-dev candidate at the merge turn (source base `e6a759de`, live dev `30e3c018`), and the review of
  that delta.
- The parent consumer set (17 at `28f9666f` with the 148 and 22 patches) and the full source banks, as the manager's
  gates.
- Carry R1 and R2 to the residue checklist.
- Publish evidence for round 2 that supersedes the round-1 handoff's "495 after the MRPDU's last byte" caption, as
  R503-1 F1 asked.

R502-2 FINISHED
