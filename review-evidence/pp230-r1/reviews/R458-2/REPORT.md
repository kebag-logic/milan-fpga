[R458] NEGATIVE - exact head 9160f7d7f005050887cab942710940b91e34fc65

**Round:** R458-2, the internal cleared-context review of kebag-logic/milan-fpga#230 / Mister-M-alt/protocol-processor-control-plane-avb-milan PR #154.

- **Head:** `9160f7d7f005050887cab942710940b91e34fc65`, tree `bd926d188f3205a819e9248ed1a07dae14098e7f`.
- **Delta:** from my round-1 head `65324390` to `9160f7d7`:
  - the author's `--no-ff` merge of main `83999eba` (`4994ada`);
  - seven test and documentation commits;
  - the manager's `--no-ff` merge of main `c050d971` (PR #153).
- **Lenses applied:** all five (Conformance, RTL, Robustness, Tests, Docs).

**Verdict: NEGATIVE, on one open MINOR (F1, Tests and Docs).**
- **Round 1's coverage gap is closed.** My round-1 probe script, run unchanged, finds every one of its 17 probes caught by a committed suite at this head, the eight round-1 survivors included. Each kill is by a named committed check: `tb/srp_stream_fsms` WK1-WK8 and `tb/srp_top` TF1-TF5, at 1/1, 2/2, 3/5 and 9/9.
- **The campaign passes.** My run of `tb/srp_top/mutants.py` gives 126/126, assertion coverage 78/78, with 33 new killed controls. Round 1's 78 killed labels are unchanged line for line.
- **The control tables are exact.** I checked the PR body, HANDOFF and the srp_top README tables row by row against my campaign and the published logs: 0 mismatches.
- **No HDL changed since `25847d07`.** Both merges are clean.
- **What remains open (F1):** one committed summary sentence, and the round-1 table's explanation of one zero, misstate why `wsid-flops-of-control-sink` is silent at 1/1. Each implies coverage at the shipping 1/1 shape that the committed tests cannot have there, because of a simulator limit that I reproduced.

**Order of work.** My draft verdict and ledger were written first (`receipts/verdict_before_reading_prior_findings.md`, sha256 in `MANIFEST.sha256`). Only after that did I re-read R459-1 (PR comment 5978360032) and the manager's response (5978368336). Both are resolved or retained below. I read no round-2 review.

## Reconstruction

- **Authorities.** As in round 1:
  - milan-fpga `AGENTS.md` and `CONTRIBUTING.md`;
  - the processor `README.md`, `docs/architecture/10_srp_engine.md` and `docs/guides/hdl-engineer.md` section 3.1.
- **Issue #230.**
  - The frozen acceptance criteria in the issue body.
  - The lane assignment 5974045353, the STOP 5977826098, and the ruling 5977836860 (parallel evaluation final; (a) goes to #640).
  - The round-2 assignment 5978448959, with four items:
    1. committed coverage at both arms, with every reviewer probe a killed control;
    2. the row-by-row control count;
    3. the residue;
    4. the merge of `83999eba`.
  - The executor's REVIEW READY 5979936594 at `1199255`.
  - The manager's review start on the PR, 5979952766.
- **Public evidence.**
  - The brief's pointer `8dca0983` holds the round-1 author packet only.
  - The round-2 packet is on the same evidence branch at `00f848e5bb6e` (12:32:01 UTC, before this round began), under `review-evidence/pp230-r1/author-r2/`. It holds HANDOFF, PR-BODY and `lockstep-r1/` (the round-1 bench, its controls and logs).
  - All 15 author-r2 files match `MANIFEST.json`. The three path-redacted files differ from `lockstep-r1/MANIFEST.sha256` only by their redaction, and their original digests agree (`receipts/evidence_digests.txt`).
  - The live PR body equals the published `PR-BODY.md` except for one trailing empty line.
- **Hosted contexts at the exact head** (`receipts/hosted_checks_at_review_*.tsv`). Both workflow runs show `docs-gates` and `portability` succeeded. Both `suites` jobs were still in progress at my last read. The manager owns hosted acceptance.

## What I ran (all at the exact head)

The tool was the pinned Verilator 5.050, wrapper sha256 `905795b9...979e92f`, as in round 1. The host's own `verilator` is 5.052; a `PATH` shim kept it out of every run (`receipts/env.txt`). Scripts are under `scripts/` and receipts under `receipts/`.

| Check | Result | Receipt |
|---|---|---|
| HDL since round 1 | Diffs:<br>- `hdl/srp` against `65324390` and against `25847d07`: empty.<br>- `git diff c050d971..9160f7d7 -- hdl` is byte-identical to `c4cb84ff..25847d07 -- hdl` (sha256 `fede969f...`).<br>- No lane commit after round 1 touches `hdl/` or `syn/`.<br>Both merges recomputed with `git merge-tree`: the trees are equal to the commits' (`4b1fa586`, `bd926d18`), so there were no conflict edits.<br>PR #153's seven files share none with this PR's own changes. | `hdl_and_merges.txt` |
| My round-1 `lockstep/probes.py`, unchanged (byte-identical to R458-1's manifest), base `c4cb84ff` against the head | rc 0. **All 17 probes are caught by a committed suite.**<br>- The eight round-1 survivors are caught by `srp_stream_fsms`.<br>- `tf-full-guard-31` is caught by `srp_top` TF4 at all four shapes.<br>- Every lockstep cell equals the round-1 receipt. | `r1_probes_at_head.txt` |
| `tb/srp_top/mutants.py --jobs 2` | rc 0, 126 checks: 126 PASS, assertion coverage 78/78.<br>- All 33 new controls KILLED by their named checks.<br>- Round 1's 78 KILLED lines are identical: same failure counts, same tags.<br>- The new positive controls: `storage`, `walk`, `srp_stream_fsms suite` (which replaces round 1's whole-suite control) and `srp_admission`. | `campaign_srp_top_head.txt` |
| Default `make` in `tb/srp_top` and `tb/srp_stream_fsms` | rc 0. The arms run first, and the suite tally is the last line.<br>- TF: 15 checks at each shape.<br>- WK: 23, 30, 43 and 79 checks.<br>- Suites: 2,200 and 1,219 checks.<br>- The FIFO statistics equal the README/HANDOFF table at every shape. | `head_default_make.txt` |
| Round-1 control table: PR body and HANDOFF 4.2 against the published `controls-final.log` | 16 rows: 0 mismatches. "Caught at" equals the non-zero cells. The summary counts 6/4/5/1 are correct. | `table_checks.txt` |
| Round-2 control table: PR body, HANDOFF R2.4.4 and `tb/srp_top/README.md:579-607` against my campaign receipts | 29 rows: 0 mismatches in the per-shape failing checks, the named checks and "Caught at". The summary counts 18/1/6/4 are correct. | `table_checks.txt` |
| The four slope controls, admission suite one shape at a time (N = 1, 2, 3, 5, 8) | All 20 cells equal the tables. N = 1 passes (equivalent). | `table_checks.txt` |
| My round-2 probes of the forced state and the workaround (`scripts/r2_probes.py`) | - **`TM_SEL` encoding swapped in the RTL:** behaviour-neutral (the srp_top suite passes 2,200/2,200), yet the held arm fails at all four shapes.<br>- **Force dropped:** the held arm fails at all four shapes.<br>- **Talker FIFO skipped while full:** TF4 fails at all four shapes.<br>- **Listener FIFO skipped while full:** TF4 and TF5 fail at all four shapes. | `r2_probes.txt` |
| Out-of-range reads in Verilator 5.050: small modules, and the committed `wsid-flops-of-control-sink` patch | - **Packed 64-bit:** a one-element array at an out-of-range index returns element 0, with or without `--x-assign unique`.<br>- **Packed 48- and 12-bit:** return 0 or a random value.<br>- **Committed patch:** 0 failures at 1/1, 3 at 2/2.<br>- **Talker stream_id read at the gate face (my probe):** silent at 1/1, caught at 2/2. The 12-bit VLAN variant is caught at 1/1. | `oor_aliasing.txt`, `r2_probes.txt` |
| Restore check of the clone | HEAD and index tree exact, 552 blobs equal in bytes and exec mode, no flags, `git status --ignored` empty, no gitlinks. | `restore_check.txt` |

## Judgements the round asked for

- **The one forced state (the held merged issue in `srp_store_wrap.sv:164-169`) does not mask a real defect on the paths it is used to judge.**
  - **It is non-vacuous:** without the force the held arm fails at every shape.
  - **It does not hide the drain from full:** a defect in the selection while a FIFO holds 32 words is caught at every shape, because the release drains from full unforced.
  - **It touches no other path:** it holds only `tm_st_r`, and TF4's precondition proves that nothing issued while it was held. TF1-TF3 and the 2,200-check suite run unforced.
  - **Its one blind case:** a push at full in the same cycle as a pop. That case is unreachable from the ports, as the wrap's Decision argues, and the guard's semantics there are those of base.
- **The `TM_SEL` encoding workaround (`srp_store_wrap.sv:105-107`) fails loudly, never silently.** If the RTL's encoding changed, the wrap would force the wrong state, and the held arm's precondition and TF4 would fail at every shape (probe `tm-enum-swapped`).
- **The 1/1 flop-arm coverage claim holds in substance, with one simulator limit.**
  - **What 1/1 covers:**
    - WK1-WK8 check every FirstValue the walk publishes at 1/1;
    - reads at an out-of-range idle face are caught at 1/1 for the 48-bit DA and the 12-bit VLAN.
  - **What 1/1 cannot cover:** a read of the 64-bit stream_id at an out-of-range idle face, for the listener or the talker. Verilator 5.050 returns element 0 for the out-of-range index of a one-element 64-bit packed array.
  - **Where those edits are caught:** at 2/2, in the same elaboration arm. Every such committed control is killed there.
  - **What overstates it:** the PR body's round-2 table labels this correctly. The README's summary sentence and the round-1 table's explanation do not (F1).

## Findings

### F1: MINOR (Tests, Docs), OPEN. The 1/1 zero of `wsid-flops-of-control-sink` is misattributed, and a committed summary claims coverage it does not have

- **Where.**
  - `tb/srp_top/README.md:620-622` says: "Every control is caught at every shape where its arm is elaborated and the edit is not equivalent by construction."
    - Its own table row (`:606`) gives `wsid-flops-of-control-sink` at 1/1 as "0 (equivalent in simulation)", and `:568-574` explains why.
    - At 1/1 the flop arm is elaborated, and the README itself distinguishes this edit from an equivalent one.
  - The PR body's round-1 table (line 211) and HANDOFF section 4.2 (line 146) explain the same zero as "0 (one sink: same index)".
  - The HANDOFF 4.2 bullet (line 155) puts it under "the edit is equivalent by construction (one source or one sink)".
- **Evidence.**
  - **The index is not the same.** The top latches the index of every accepted request, refused ones included (`KL_srp_top.sv:840`, bound at `:617`). So the idle control face can name sink 1 at one sink, as WK6's parked arm does.
  - **Round 1's own bench reached that state.** Its runs drove out-of-range indices, and the DA edit at one source mismatched 47,564 cycles at 1/1 in the published `controls-final.log`.
  - **The zero comes from Verilator.** Verilator 5.050 reads a one-element 64-bit packed array at an out-of-range index as element 0, even with `--x-assign unique`, while 48- and 12-bit elements read 0 or a random value (`receipts/oor_aliasing.txt`).
  - **The blind spot is wider than this one control.** The same limit hides any 64-bit stream_id read through the idle face at one context: my talker probe is silent at 1/1 and caught at 2/2 (`receipts/r2_probes.txt`).
- **Authority.**
  - AGENTS section 6, Tests: each test can fail for the defect it claims to detect.
  - AGENTS section 6, Docs: evidence must be accurate for a cold reviewer.
  - Round-2 assignment item 2: state each control's shapes exactly as the table shows them.
  - Owner rule 2026-10-02: a claim about test coverage is not wording-only (the same basis as R458-1 F3).
- **Impact.**
  - A reader of the README, the committed record of the campaign, is told that every non-equivalent control is caught at every elaborated shape, including the shipping 1/1.
  - A reader of the round-1 table is told the 1/1 zero is equivalence by construction.
  - Neither learns that stream_id index faults through an idle face are invisible to the committed tests at 1/1 and rely on 2/2.
  - No RTL defect follows.
- **Required outcome.** The three places state the simulator limit, not equivalence. For example:
  - **README `:620-622`:** "...and the edit is not equivalent by construction, except `wsid-flops-of-control-sink` at 1/1: there Verilator 5.050 reads the out-of-range 64-bit element as element 0 (equivalent in simulation, above), as it would any 64-bit stream_id read at an idle face at one context; 2/2 catches those edits."
  - **PR body line 211 and HANDOFF line 146:** "0 (equivalent in simulation: the out-of-range control index reads sink 0 in Verilator)".
  - **HANDOFF line 155:** name this case beside the equivalent ones.
  - A one-line mention in `tb/srp_stream_fsms/README.md` would help, but is not required.
- **Verification.** Re-read the three places against `receipts/oor_aliasing.txt` and the README's own taxonomy (`:568-574`). No test or RTL change is needed.

### Residue (wording only; does not affect the verdict)

- **R2-R1, PR body line 9.** "Head `1199255`." is stale: the PR head is `9160f7d7`, as line 280 records.
  - **Exact fix:** "Head `9160f7d7` (the manager's `--no-ff` merge of `main` `c050d971` on the lane's `1199255`)."
- **R2-R2, `docs/guides/hdl-engineer.md:88-92`.** The sentence attributes the admission's `slope_q_r` to "those SRP arrays' walks", which are the stream-FSM arrays. The admission walk reads it.
  - **Exact fix:** "What the SRP walks read one context per cycle (the stream FSMs' tick walks and the admission walk) is distributed RAM read in the cycle of its address, with no latency: ..."

### Suggestions (not counted)

- **S1: randomise unreset memory in the FIFO arms.**
  - The store build runs without `+verilator+rand+reset+2`, so unreset FIFO words start at zero. A word read before it was written then issues with owner 0, and the scoreboard classes it as a cadence word and ignores it.
  - Lost words still show as "left", so no committed control escapes.
  - Building the store arms with `--x-initial unique` and that runtime flag, as the walk arms are built, would make such a read show as `wrong` or `invented` too.
- **S2: name the 1/1 limit next to WK6.** Record the 64-bit aliasing limit in `tb/srp_stream_fsms/README.md`, where WK6 is defined.

## Prior findings at this head

| Finding | Status at this head | Basis |
|---|---|---|
| R458-1 F1 (MINOR): new storage paths and the N <= 2 arm untested; eight probes survive | **Resolved** | 17/17 probes caught when run unchanged, the eight by WK1-WK8. Both arms elaborated at 1/1, 2/2, 3/5 and 9/9. Every probe is a killed control of the campaign (126/126, 78/78), and the README records them |
| R458-1 F2 (MINOR): Vivado evidence unpublished | **Resolved** (round 1) | `06fe795b`; no HDL changed since, so the figures stand as a base-to-head delta |
| R458-1 F3 (MINOR): control-count sentence | **Resolved as raised** | The PR body and HANDOFF give each row's count, and both tables match the logs (16 and 29 rows, 0 mismatches). The misattributed 1/1 zero inside those tables is new and is F1 |
| R458-1 S1: FIFO full boundary never exercised | **Taken** | TF4 and TF5 reach the full guard, under the one forced state judged above |
| R458-1 O1: `tb/srp_top` fails 4 checks with unreset state randomised, at base and head alike | **Retained (observation)** | Outside this diff, not re-measured; the manager files it if accepted |
| R459-1 F1 (MINOR): area figures on unpublished receipts | **Resolved** | As R458-1 F2 |
| R459-1 F2 (MINOR): PR body overstates control coverage | **Resolved** | As R458-1 F3. R459-1 too had classed `wsid-flops-of-control-sink` at 1/1 as equivalent; F1 corrects that |
| R459-1 R1 (RESIDUE): "10 section 5.1" ambiguous | **Resolved** | The PR body names `docs/architecture/10_srp_engine.md` section 5.1 everywhere. Commit subject `df02e64` stays, as R459-1 advised for history |
| R459-1 R2 (RESIDUE): "all rc 0" header | **Resolved** | Body line 245 |
| R459-1 S1: name the new memories in the storage rule | **Taken** | `hdl-engineer.md:88-92` (wording residue R2-R2) |
| R459-1 S2: commit a lockstep bench | **Resolved by substitution** | Directed arms, as the assignment preferred, and the round-1 bench published with digests at `00f848e5` |

## Lens results

- **[R458] PASS Conformance.**
  - **Criteria and the ruling** are unchanged from round 1, and the RTL is unchanged.
  - **Criterion 1** (SRP tests at 1x1 and 8x8): now also checked directly at 1/1 and 9/9 by the new arms.
  - **Criteria 2 to 4** stand on `06fe795b` as a base-to-head delta, because neither merge brings SRP HDL.
  - **Ruling (b)** is honoured.
- **[R458] PASS RTL.**
  - **No change since `25847d07`:** byte-identical HDL diff, empty `hdl/srp` deltas, and the same four blob ids as round 1.
  - **Round 1's equivalence evidence stands:** my two lockstep benches, re-run inside the probe run with every cell equal to round 1.
  - **The new arms bind the real modules unedited.** The only intrusion is the documented test-only force.
- **[R458] PASS Robustness.**
  - **Configuration arms:** the new arms run both elaboration arms and four shapes, with unreset walk memories random.
  - **Idle faces:** they are parked out of range, a state the top really produces.
  - **Reset:** WK5.
  - **The FIFO full boundary** is reached under a force that I showed is non-vacuous, fails loudly if the encoding drifts, and masks no drain defect.
  - **Limits:** the 1/1 64-bit aliasing (see Judgements), and S1.
- **[R458] UNCLEAN Tests:** F1.
  - The probe bar, the campaign and the table counts all pass.
  - The README's coverage summary and the round-1 explanation of the 1/1 zero are inaccurate.
- **[R458] UNCLEAN Docs:** F1, plus residue R2-R1 and R2-R2.
  - `10_srp_engine.md:216-222` and both new README sections are otherwise accurate against my runs.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #230 acceptance, 5974045353, 5977836860, 5978448959, 5979936594; `06fe795b` figures (re-derived in round 1); `hdl_and_merges.txt` | R458-2 | 9160f7d7f005050887cab942710940b91e34fc65 |
| RTL | CLEAN | `hdl/srp/*` (blob identity with `25847d07`), `KL_srp_top.sv:840,947-1257`, merges `4994ada` and `9160f7d7` (merge-tree), round-1 lockstep cells re-run | R458-2 | 9160f7d7f005050887cab942710940b91e34fc65 |
| Robustness | CLEAN | `srp_walk_wrap.sv`, `walk_main.cpp`, `srp_store_wrap.sv`, `store_main.cpp`, both Makefiles; forced-state and encoding probes; out-of-range aliasing | R458-2 | 9160f7d7f005050887cab942710940b91e34fc65 |
| Tests | UNCLEAN (F1) | unchanged round-1 probes (17/17 caught); `tb/srp_top/mutants.py` 126/126, 78/78; default `make` in both suites; slope controls at 5 shapes; round-2 probes; `run_suites.sh` verdict logic | R458-2 | 9160f7d7f005050887cab942710940b91e34fc65 |
| Docs | UNCLEAN (F1) | PR body (live), HANDOFF author-r2, `tb/srp_top/README.md:491-626`, `tb/srp_stream_fsms/README.md:7-9,171-207`, `docs/architecture/10_srp_engine.md:212-222`, `docs/guides/hdl-engineer.md:80-93` | R458-2 | 9160f7d7f005050887cab942710940b91e34fc65 |

## Real limits

- **Not run, by assignment:**
  - `run_suites.sh`, `make check`, `gen_matrix --check`, the Yosys gate and lint;
  - the parent consumer set, builder and gate 16;
  - Vivado.
- **Not re-run, inputs unchanged:**
  - The `srp_admission` campaign: its inputs (`hdl/srp`, `tb/srp_admission`, `tb/common`) are byte-identical to round 1, where it gave 12/12.
  - The campaigns the main merges touch (adp, maap and the pp_top campaigns): they test main's HDL, which this PR does not change.
- **Other reviewers' tooling:** R459-1's `make_controls.py` was not run by me. Its 13 defect controls are committed controls, killed in my campaign run.
- **Simulation only, one simulator.** How Vivado treats an out-of-range read of a packed array was not established.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.

## Pending manager duties

- **Hosted acceptance at the exact head:** both `suites` jobs were in progress at my last read.
- **Bank receipts:** the brief says the manager's full static/builder and native banks passed at this head. I found no public receipt for them on the evidence branch (`00f848e5`), the issue or the PR; publish them.
- **Parent adoption patch:** `parent-adoption-c10-1269cdaf.patch`, which the round-2 consumer set used, is not in the public evidence either.
- **The merge-turn candidate:**
  - source base `c4cb84ff`, live dev `fea346e7`;
  - the consumer set of 17 with c8, p2-p1, c10 and the #232 xvlog patch;
  - gate 16 is expected to pass now that #643 is fixed.
- **Evidence pointer:** the brief's evidence pointer (`8dca0983`) predates round 2; the round-2 packet is `00f848e5`.
- **Residue checklist:** R2-R1 and R2-R2, exact fixes above.
- **Filing:** file O1 if accepted.

## Restoration

I made no edit to the clone; every probe ran on copies under the packet's scratch. After the round:
- the clone's HEAD and index tree are exact;
- all 552 work-tree blobs equal their HEAD blobs in bytes and exec mode;
- `git status --ignored` is empty;
- no assume-unchanged or skip-worktree flag is set;
- the repository has no submodule gitlinks (`receipts/restore_check.txt`).

R458-2 FINISHED
