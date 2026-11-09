[R802] NEGATIVE - exact head 84f6d6ad77d51d678f8efdf26b45aae011a42001

# R802-2: external independent review of processor issue #216 / PR #218, round 2

- Exact head `84f6d6ad77d51d678f8efdf26b45aae011a42001`, tree `3582db8c1c23012840dcbcf2cfd1a1e91f560119`. Source base `044cb25f`. Delta reviewed: `60094a26..84f6d6a` (four commits `b655100`, `b5f9e53`, `ceb6a98`, `84f6d6a`). Code the delta does not touch keeps its R802-1 lens verdict unless the delta changes what it depends on.
- Authority: issue #216 body (frozen acceptance) and the round 2 ruling (issue #216 issuecomment-6740735425); IEEE 802.1Q-2018 Table 10-3, Table 10-4, 10.7.5.1, 10.7.5.2, 10.7.6.3, 10.7.8, 10.7.9 / Table 10-5; Milan v1.2 Table 4.3; `docs/README.md` single-source rules; the owner comment rule.
- The processor repository has no AGENTS.md or CONTRIBUTING.md; its rules are `docs/README.md`, the Makefile `check` target and `.github/workflows/hdl.yml`.
- Order kept: the issue, the ruling and the PR were read first. Then the full delta. Then the public evidence. The prior public review findings (R801-1, R802-1) were read only after the independent pass over the diff. The other reviewer's current-round report was not read.

## Verdict

NEGATIVE, on one MINOR. Every ruling item is built, graded and killed by name at this head:
- the VID Registrar goes to MT at LINK_DOWN and LINK_UP;
- each VID Applicant takes Begin! and New! at LINK_UP;
- AP8 and VR12 to VR18, DA6 and DA7;
- the `N_VIDS_P <= ENC_DEPTH_P` guard;
- GAP-18;
- the README count.

Every processor gate this review ran is rc 0. Every focused campaign arm and every reviewer probe is killed.

The open defect is one new clause claim in 10 section 6.2: "Flush! is a Registrar event only (§10.7.5.2)". The PR's own published clause record says 10.7.5.2 also signals the LeaveAll state machine. The engine does not signal it, and the repository does not record that it doesn't (F1). It changes no behaviour on the wire. It is still a clause claim, so by the owner rule it cannot be RESIDUE.

## Findings

### F1 - MINOR - 10 section 6.2 says Flush! is "a Registrar event only (§10.7.5.2)"; the PR's own clause record says 10.7.5.2 also signals the LeaveAll state machine, which this engine does not do

- Lenses: Docs, Conformance.
- Where: `docs/architecture/10_srp_engine.md:524-525`: "Flush! is a Registrar event only (§10.7.5.2), so LINK_DOWN leaves the Applicants as they are". It is new in `ceb6a98`.
- Authority and evidence:
  - The author's published round-2 clause record (`author-r2/receipts/STANDARDS.txt` at evidence commit `6ef09f9d`) reads, for 10.7.5.2: "It is a Registrar event; Table 10-3 has no Flush! row. (Its second paragraph also signals leavealltimer! to the LeaveAll state machine; this engine does not, and this round changes no LeaveAll timing ...)".
  - The engine's `link_up_i` reaches only `KL_srp_domain`, `KL_srp_vlan` and `KL_srp_listener_fsm` (`hdl/srp/KL_srp_top.sv:399,476,670`). Neither participant's LeaveAll machine sees a link change.
  - This review did not read the standard's text itself. The finding rests on the contradiction between the document and the PR's own clause record.
- Impact:
  - The conclusion drawn is correct: Table 10-3 has no Flush! row, so the Applicants keep their state.
  - The cited basis ("only") misstates the clause. It also hides a partial Flush! mapping, which the repository records nowhere.
  - No wire effect: this engine pairs every Flush! with a Begin! at LINK_UP before frames flow, and MRP timers are out of #216's scope ("MRP timers unchanged"). So this is a disclosure defect, not a behaviour defect.
- Required outcome, either of these:
  - (a) Reword to the accurate basis and disclose the omission. For example: "Table 10-3 has no Flush! row, so LINK_DOWN leaves the Applicants as they are. §10.7.5.2 also signals leavealltimer! to the LeaveAll state machine; this engine's LINK_DOWN does not (no MRP timer changes under issue #216)". Optionally add a line in 00's gap register.
  - (b) Show from the clause text that 10.7.5.2 signals Flush! to the Registrar alone, and correct the author's clause record instead.
- Verification: `make check` rc 0; a reviewer reads the reworded 10 section 6.2 sentence against 10.7.5.2.

### R1 - RESIDUE - "(below)" points at a section that does not mention a link change

- Lens: Docs. Where: `docs/architecture/10_srp_engine.md:532`: "A link change does not reset the talker's streaming licence (below)."
- The "Join before the stream" paragraph below (`:549`) never mentions a link change. This is wording only; the behaviour statement is right (`sent_r` is not reset on a link edge, `hdl/srp/KL_srp_vlan.sv:357,478`).
- Exact fix: "A link change does not reset `vid_sent_o`, the talker's streaming licence of [Join before the stream](#sec-10-join-before-stream) below."

### R2 - RESIDUE - one unwrapped long line in 10 section 6.2

- Lens: Docs. Where: `docs/architecture/10_srp_engine.md:509` (142 characters; the paragraph around it wraps at about 95).
- Exact fix: break the line after "never JoinIn without IN." so that "The last user's leave is Lv! (LA): the entry stays until its tx! sends the Lv" starts a new line. No other change.

### S1 - SUGGESTION - the three AP8 arms are graded on the prefix `AP8:`, which the AP8 setup row also carries

- Lens: Tests. Where: `tb/srp_top/mutants.py` (rows `vlan-link-keeps-registrar`, `vlan-link-no-begin` and `top-vlan-link-unwired`, each expecting `'AP8:'`); `tb/srp_top/sim_main.cpp:4104` ("AP8: setup: ...").
- Today each arm fails the post-bounce rows, not the setup row. This review's campaign shows `failures=2`, `1` and `2`, and the `top-vlan-link-unwired` log names both post-bounce rows.
- A future arm that broke only the setup (for example, the Registrar never IN) would still count as killed "by name". Suggested words: `AP8: VID 2's Registrar` for the two Registrar arms, and `AP8: VID 2 restarts` for `vlan-link-no-begin`.

### S2 - SUGGESTION - carry `vid_sent_o` across a link bounce into #220

- Lenses: Conformance, Robustness.
- The VID now declares New again to a new link partner, but `vid_sent_o` (the talker's licence, Milan 4.3.2) stays set across the bounce.
- Today this is safe: the talker's Listener registrations are flushed at LINK_DOWN (the author's stream probe shows `tk_reg(0)=0` while the link is down). Also, the new partner's Ready can only come back after our Talker Advertise, which is later than the VID's first New.
- When #220 makes the Talker Advertise go out New at LINK_UP, that ordering margin shrinks. Suggested: re-check the licence's assumption under #220 and state it there.

### S3 - SUGGESTION - pre-existing, outside the delta: an arm graded on two suites keeps only the last suite's log

- Lens: Tests. Where: `tb/srp_top/mutants.py` `campaign()` writes `output/<label>.log` per unit, so for example `vlan-link-keeps-registrar.log` holds only the encoder run.
- The verdict is computed from in-memory output, so no result changes. Only the saved evidence for the `srp_top` half is lost. Suggested: name the file `<label>-<suite>-<group>.log`. Not this PR's to fix.

## Round 1 findings (R802-1, and R801-1 as cross-referenced by the ruling), resolved at this head

| Prior finding | Severity | Status at `84f6d6a` | Evidence |
|---|---|---|---|
| R802-1 F1: VID Registrar keeps IN across LINK_DOWN / LINK_UP | MAJOR | RESOLVED | `KL_srp_vlan.sv:187-188,279-280` (both edges: MT, after rx/rLA!/txLA!), `:289-290` (LINK_UP: VO, then VN for entries with users), `:452-454,474` (a held push is withdrawn); wired at `KL_srp_top.sv:476`. My round-1 link probe (`probes/r1/r802-link-bounce.tb.patch`) re-run here passes, `2 checks: 2 PASS`: `VID 2 after LINK_UP: New@3801 New@4001 JoinMt@4201 ...`. AP8 is in the suite; `vlan-link-keeps-registrar`, `vlan-link-no-begin` and `top-vlan-link-unwired` are KILLED on AP8 in this review's campaign. |
| R802-1 F2 = R801-1-F01: README records 7 where the arm fails 8 | MINOR | RESOLVED | `tb/srp_encoder/README.md:277` reads exactly `8 FAIL — V10, W4, W5 (two), B1 (four)` (the ruling's text). |
| R802-1 S1: three Table 10-3 VP cells not distinguished | SUGGESTION | RESOLVED | DA6, DA7, VR12 and VR13 (`tb/srp_encoder/sim_main.cpp` `domain_vp_is_not_ap`, `vlan_vp_is_not_ap`). My probes `p09`, `p12` and `p19`, re-run here as published, each give `1659 checks: 1657 PASS, 2 FAIL` (p09: DA6, VR12; p12 and p19: DA7, VR13). The arms `vp-*` are KILLED. |
| R802-1 S2: MVRP round stalls if `N_VIDS_P > ENC_DEPTH_P` | SUGGESTION | RESOLVED | `KL_srp_top.sv:272-275` `g_vids_fit`. `guards.py --frontend yosys --only KL_srp_top.g_vids_fit`: 34 PASS. Its five arms (`error`, `warning`, `initial`, `tightened`, `loosened`): `5 of 5 killed`. The bound is analytically right: separate MVRP RAM of `DEPTH_P` (`KL_srp_encoder.sv:327,416-417`), at most one push per entry per walk, and the walk waits out a running drain. |
| R802-1 R1 = R801-1-F02: 6.5 timing value outside F08.1 | RESIDUE | RESOLVED | `10_srp_engine.md` 6.5 reads "every `T-MRP-LEAVEALL` ([F08.1](08_timing.md#fig-08-constants)) from Begin!", the exact fix. |
| R802-1 S3 = R801-1-F03: VID registered before the first join | SUGGESTION | RESOLVED (as ruled) | GAP-18 in `00_MILAN_COMPLIANCE_REVIEW.md:369-382`, its F00.2 row and its REQ-SRP-006 link. The basis is as ruled (note 11 covers the Applicant; Table 10-4 / 10.7.8 would read IN). 10 section 6.2 cites it. `make check` (matrix, links) OK. |

## The ruling items

1. **VID Registrar and Applicants at a link change: met.** Flush!/Begin! take every VID Registrar to MT, after the clock's received events, so they win (VR16; my probe `q1-flush-only-at-up` fails VR14 and VR16). LINK_UP is Begin! then New! on each VID with users (VR15; probe `q4-down-restarts-applicant` fails VR14 and VR18, which shows LINK_DOWN keeps the Applicants). A VID with no user is VO and sends nothing (VR17; probe `q2-begin-declares-every-entry` fails VR17). A held push is withdrawn (VR18; probe `q3-held-message-still-valid` fails VR18). The ruling's check is AP8 (Registrar IN, a 30 ms bounce, then no JoinIn, then New, New, JoinMt, the first within 240 ms, inside F08.1's T-MRP-JOIN range of 180–240). `vlan-link-keeps-registrar` fails `AP8:` by name (2 rows), as do `vlan-link-no-begin` (1) and `top-vlan-link-unwired` (2). 10 section 6.2 "A link change" and the F10.3 edges match the RTL, apart from F1's basis sentence. The rest of the behaviour the delta changes (`KL_srp_vlan.sv` reset of `link_q_r` to 0, the same as `KL_srp_domain.sv:210`) is consistent with the Domain.
2. **Stream Applicants across a bounce, report only: met.** `git diff --stat 60094a26..84f6d6a -- hdl` touches only `KL_srp_vlan.sv` and `KL_srp_top.sv`. `KL_srp_top`'s change is one wiring line and the guard. The talker and listener FSMs and the `vid_sent_o` expression are unchanged. The author's probe (`stream-link-bounce/streamlink.tb.patch`, a disposable group that prints and asserts nothing about streams) is sound for a report: Talker Advertise `JoinMt@4203` (872 ms after LINK_UP, no New); Listener `Lv@3403`, then New, New, JoinMt once the peer's Talker Advertise registers again. It is filed as #220 (open).
3. **README count, VP/AP checks, N_VIDS guard, gap entry: met** (table above).
4. **The seven stale `tb/srp_top/README.md` counts: not required by the ruling.** Ruling item 2 names only the `tb/srp_encoder` row. The seven rows are untouched by this PR (`git diff 044cb25f..HEAD` changes none of their figures). The author's round-1 receipt (`author/receipts/pre-existing-counts/arm-base-stale.tsv`, measured at base `044cb25f`) gives the same counts as the head campaign. So they were stale before #216. Not a finding against this PR; a follow-up issue is owed (manager duty).
5. **Area: verified against receipts.** `area-60094a2-out/SUMMARY.md` and `area-84f6d6a-out/SUMMARY.md` give `KL_srp_vlan` 594 to 643 LUT (+49) and 147 to 148 FF (+1); `KL_srp_top` 14,109 to 14,108 (2x2) and 28,814 to 28,903 (8x8), FF unchanged. Those are the figures in 10 section 5.1 (`:339-347`) and in the PR body. The base column equals the round-1 receipt. Not re-synthesised here.
6. **The 40 scratch-parent gates and the twin: verified from receipts.** `parent-84f6d6a`: 40 rc files, all `0`. The pin record shows `protocol-processor` at `84f6d6ad77d5...` on dev `ac0a01e3` with two local commits (pin and ROM digests). `twin-84f6d6a`: rc 2, with exactly `fabric-mvrp-leave-all`, `fabric-domain-one-new` and `fabric-vid2-join-in` reported "the defect has gone". The remaining `[OWED]` rows are not this issue's. Not re-run here (parent banks are outside this review's allowance).
7. **The shard stand-in and the ten-minute pause: neither could change a result.**
   - `tools/proc-shard.sh` runs the repository's own `scripts/run_suites.sh` text, with only its suite loop's list replaced. It refuses to run unless that loop occurs exactly once. The pre-checks, each suite's `make` and the verdict lines are the script's own.
   - `tools/merge-shards.py` requires every shard rc 0 with its `0 failing` line. It also requires every `tb/*/Makefile` suite PASS in exactly one shard, and no FAIL or UNREADABLE. `sweep/merge.log`: 36 of 36, `MERGE OK`; the shard totals 10667 + 2866 + 1013119 + 5461 = 1032113.
   - Partitioning can only make an inter-suite dependency fail, never pass, and none exists: each suite builds in its own directory.
   - The SIGSTOP/SIGCONT pause hit the maap, adp, aecp_cmds and elab-guard campaign chain. `tb/common/mutant_pool.py` and those drivers have no wall-clock limit (no `timeout`, `time.`, `alarm` or `signal`). The only "timeout" in `tb/aecp_cmds/sim_main.cpp` is a simulated-cycle budget (`TRIAL_BUDGET`). A pause can only lengthen wall time.

## Gates and probes run by this review at the exact head

Each run was on its own `--shared` clean clone at `84f6d6a`, with Verilator 5.050 (the pinned build, `--version`: `Verilator 5.050 2026-07-01 rev v5.050`), sv2v v0.0.12, Yosys 0.66 and mermaid-cli 11.16.0 (the CI pin). Receipts are under `receipts/gates` and `receipts/probes`, each with cmd, log, rc, start and end.

| Gate | Command | rc | Result |
|---|---|---|---|
| whitespace | `git diff --check 044cb25f HEAD` | 0 | empty |
| matrix | `python3 scripts/gen_matrix.py --check` | 0 | `matrix: OK (94 rows, 0 untested)` |
| HDL lint | `bash scripts/lint_hdl.sh` | 0 | 41 `LINT OK` |
| docs | `make check` | 0 | every gate OK (`lint: 41 mermaid + 18 wavedrom blocks checked, OK`, links 1328, matrix 115 REQ / 18 GAP, ids, figures, aecp). A first attempt with the mermaid CLI off PATH failed only at `mmdc: command not found` (`make_check-nommdc.*`, kept). |
| suite | `make -C tb/srp_encoder` | 0 | `1659 checks: 1659 PASS, 0 FAIL` |
| suite | `make -C tb/srp_top` | 0 | `8706 checks: 8706 PASS, 0 FAIL` (applicant group `21 checks: 21 PASS`) |
| elab guard | `guards.py --frontend yosys --only KL_srp_top.g_vids_fit` | 0 | `34 checks: 34 PASS` (refused at 13 by both front ends, elaborates at 12) |
| guard arms | `elab_guards/mutants.py --only KL_srp_top.g_vids_fit:{error,warning,initial,tightened,loosened}` | 0 | `5 of 5 killed` |
| SRP campaign (focused) | `tb/srp_top/mutants.py --jobs 4 --only` the 10 new arms, the 4 re-expressed arms and the 4 acceptance arms | 0 | `34 checks: 34 PASS, 0 FAIL`, each arm KILLED. The per-arm failure counts equal the README rows (for example `vlan-joinin-registrar-mt` 5 and 19, `vlan-registrar-never-in` 2 and 9, `vlan-link-no-begin` 1 and 5). |
| reviewer probes | `scripts/run-probes.sh` with `probes/r2/q1..q4` and `probes/r1/p09,p12,p19` (srp_encoder), and `probes/r1/r802-link-bounce.tb.patch` (srp_top `r802link`) | 2 x 7, 0 x 1 | q1: VR14, VR16; q2: VR17; q3: VR18; q4: VR14, VR18 (two); p09: DA6, VR12; p12 and p19: DA7, VR13; link probe `2 checks: 2 PASS` |

I did not re-run the full 36-suite sweep, the other campaigns (AECP, MAAP, ADP, aecp_cmds, the full SRP campaign and the full elab campaign), Yosys portability or the nvm_port figures. The delta touches none of their inputs except the SRP sources, which the focused runs cover. For those I rely on the author's published receipts, checked below.

After the probes the review clone was verified byte-exact: HEAD and `write-tree` both equal tree `3582db8c...`, `git status --porcelain --ignored` is empty, and there is no index or worktree diff. The repository has no `.gitmodules` and no gitlinks (`receipts/clone-restore-verify.txt`).

## Published evidence checked

- The evidence link named for this review (`8844ce1c`, `review-evidence/pp216-r1`) holds round 1 only (head `60094a2`). The round 2 author receipts are on the same branch `pp216-review-evidence` at commit `6ef09f9dbf39c5522b9d3368f41b19508feeb1c8` ("Round 2 author receipts"), under `review-evidence/pp216-r1/author-r2/`.
- Every `author-r2/` file's sha256 matches `MANIFEST.json`: 521 OK, 0 bad, 0 missing, 0 unlisted. Nine files are path-redacted by the publisher (`receipts/evidence-manifest-verify.txt`).
- Neither commit carries a signature (`verification.verified=false, reason=unsigned`). Integrity rests on the manifest hashes, not on a signature.
- Spot-checked against the receipts: the sweep merge, the req-tags rc 0 (`266 evidence lines, 14 suites, OK`), the SRP campaign count-change file (only the 12 re-measured arms moved; 10 added; none removed), the area summaries, the parent rc files, and the twin compare.

## Hosted evidence at the exact head (inspected, not owned)

`receipts/hosted-check-runs.txt` (read at about 21:35 local time):
- workflow `hdl`, push run `42671237160`: `completed failure` with no job listed, so no job executed in it;
- pull_request run `42671247024`: `in_progress`, its `suites` job started 18:08:05Z and not complete.

No executed hosted job has passed or failed at this head. Hosted acceptance is the manager's.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1; S2) | VID Registrar and Applicant at link edges against Table 10-4 / Table 10-3 Begin!, New! and note 11 as the engine maps LINK_DOWN/UP; VP rows (note 4, txLA!) via DA6/DA7/VR12/VR13; GAP-18 basis against 10.7.8 and note 11; the 10.7.5.2 claim against the PR's clause record; unchanged rows keep R802-1's verdict | R802-2 | 84f6d6ad77d51d678f8efdf26b45aae011a42001 |
| RTL | CLEAN | full delta of `KL_srp_vlan.sv` and `KL_srp_top.sv` (edge detection, ordering in `entry_next`, W_PUSH withdrawal, guard); lint rc 0; Yosys guard elaboration | R802-2 | 84f6d6ad77d51d678f8efdf26b45aae011a42001 |
| Robustness | CLEAN (S2 optional) | link edge on the same clock as rx, rLA!, periodic!, a user op, W_EVAL and W_PUSH; reset value of `link_q_r`; the guard bound against the encoder's MVRP RAM; four reviewer mutation probes | R802-2 | 84f6d6ad77d51d678f8efdf26b45aae011a42001 |
| Tests | CLEAN (S1, S3 optional) | AP8, DA6, DA7, VR12–VR18 source; the 18-arm focused campaign; seven reviewer probes; srp_top and srp_encoder suites; the guard bench and its five arms; README counts against measured counts | R802-2 | 84f6d6ad77d51d678f8efdf26b45aae011a42001 |
| Docs | UNCLEAN (F1; R1, R2 residue) | 10 sections 5.1, 6.1, 6.2 / F10.3, 6.5; 00 GAP-18, the REQ-SRP-006 and F00.2 rows; 09 8.15; the `tb/srp_top`, `tb/srp_encoder` and `tb/elab_guards` READMEs; the comment rule over every added source and test comment (no lane label, lane name, review round, reviewer ID or comment ID); `make check` | R802-2 | 84f6d6ad77d51d678f8efdf26b45aae011a42001 |

## Real limits

- This review did not read the IEEE 802.1Q-2018 text. Clause content comes from the PR's own published clause record and the repository's docs. F1 is stated as an inconsistency between the two.
- Not run here (the allowance excludes full banks; the delta does not reach their inputs): the full suite sweep, the AECP, MAAP, ADP and aecp_cmds campaigns, the full SRP and elab-guard campaigns (coverage `185/185`), Yosys portability, the nvm_port figures, the scratch parent and the twin. For these this review relies on the author's receipts, verified by manifest hash and spot-checked.
- Area is not re-synthesised here; it was checked only against the published stat summaries.
- No behavioural simulation at `N_VIDS_P == ENC_DEPTH_P`. The guard's bound is judged from the encoder's MVRP storage and the walk, and graded only by elaboration.
- The seven stale counts' base values are from the author's base receipt, not re-measured here.
- Physical calibration NOT RUN. No hardware proof; any field skips are not hardware proof.
- No manager source bank runs at this exact head, and none is claimed or inferred. This review is source validation only, distinct from the current-dev merge candidate (source base `044cb25f`, live dev `123f57a922bf07476cd69f91867f3b6f07080804`).

## Pending manager duties

- Carry F1 to the author. Carry R1 and R2 to the residue checklist. S1 to S3 are optional.
- File the follow-up for the seven pre-existing stale `tb/srp_top/README.md` counts (`pending-peer-ignored`, `mvrp-supersedes-msrp`, `leaveall-expiry-lost`, `preparation-before-slot`, `mvrp-expiry-only-redraw`, `stale-expiry-honoured`, `mvrp-stale-expiry-honoured`); the PR says "left for a follow-up", and no issue was found.
- Link the round 2 author receipts (`pp216-review-evidence` at `6ef09f9d`, `author-r2/`) in the PR evidence comment; the named link `8844ce1c` holds round 1 only.
- Hosted acceptance: the push run concluded `failure` with no job, and the PR run's `suites` job was still in progress when inspected.
- At the merge turn, build and validate the current-dev candidate (builder and native banks), and have the parent delete the three twin owed rows when it adopts this head.

R802-2 FINISHED
