[R399] POSITIVE - exact head 412efeb750e358a65b04bae1cbb3086134d15b7e

# R399-2: external independent delta review of processor PR #133 (lane C1: issues #29, #108, #64, #65)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #133, round R399-2.
- Exact head `412efeb750e358a65b04bae1cbb3086134d15b7e`, tree `f12258a0111546105e68bfdee95a1ebf141676f8`.
- Source base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`. Delta under review: `81b8d6d7..412efeb7`, three commits: `e2c631d`, `c9584bc` and `412efeb`, plus the round-2 PR body.
- Assignment: processor issue #108 comment 5886235840 (round 2), answering R399-1 S1-S3 and the prior-round internal review.
- **Review clone.** Detached at the exact head and never written.
  - `ls-files -s` has 326 entries, digest `9ab75ce4…3156`. There is no `.gitmodules` and there are no mode-160000 gitlinks, so there are no submodule gitlinks to verify.
  - The digest is unchanged at the end (`receipts/clone-integrity*.txt`); porcelain including ignored files is empty.
- **Scratch.** Every build, mutant and probe ran in a `git archive` copy under `scratch/`, which is not published.
- **Verdict basis.** There is no open BLOCKER, MAJOR or MINOR finding. Three SUGGESTIONs (S1-S3) are recorded; none of them blocks.

## 1. Reconstruction (what was read, in order)

1. **Contributor guidance.** The processor has no `AGENTS.md` or `CONTRIBUTING.md`. The conventions used were `README.md`, `docs/README.md` (ID registries, single-source rules, citation style), the `hdl/` banners and the tb READMEs.
2. **Frozen scope.** Issue #108 (body, acceptance 1-3), the lane assignment (comment 5883702094), and the round-2 assignment (comment 5886235840: items 1-4, the gates and the review).
3. **Requirements and interfaces, as cited in the tree.**
   - 802.1Q-2014: Table 10-5 rLA!, 10.6, 10.7.4.3, 10.7.5.20 b)1)/b)2) with its NOTE, and 10.7.5.22.
   - Milan v1.2: Table 4.3, 4.3.2 and 4.4.1.
   - The `KL_pp_timer_service` arm/expiry contract and its wrap-safe compare (`KL_pp_timer_service.sv:160-193`).
   - The processor top's timer wiring (`protocol_processor_top.sv:793-812`, `:2233-2293`) and the arm-port priority mux (`:2607-2706`).
4. **Code and tests.**
   - `git diff c951a9ff..412efeb7`, and in detail `81b8d6d..412efeb7`: `KL_srp_top.sv`, docs 10, and all of the tb/srp_top changes (harness, wrapper, README, `mutants.py`, 5 patches).
   - `KL_srp_top.sv:1016-1242` in full: the guard, the cadence plane, the draw path and rLA!.
   - `KL_srp_encoder.sv:556-619`: E_IDLE, E_ALLOC and E_COLLECT, for the §6.2 claim about the MVRP drain.
5. **Public evidence.**
   - milan-fpga `a6427910` `review-evidence/ppC1-r1`: MANIFEST.json, `author/HANDOFF.md` and `author/PR-BODY.md`. The hashes match.
   - The round-2 author packet at `616889dd`, `author-r2/HANDOFF.md` and `PR-BODY.md`. The hashes match its MANIFEST, and the archived PR body equals the live PR body.
   - Hosted check runs at the exact head.
   - The parent, read only, at dev `57b8c867` and live dev `9e3ccbfb`.
   - The issue and the PR carry no manager evidence comment for round 2 beyond the review-start notice.
6. **Independence.**
   - No private author material, lane scratchpad or management directory was read.
   - The same-round internal report (R398-2) was not read.
   - The prior-round internal report (R398-1) was read only after this report's verdict and ledger were written, to resolve its findings (section 6).
   - My own R399-1 report was re-read as the round-1 record.

## 2. Judgement per assigned item

### (1) PR body: the parent-visible list names `tb/verilator/milan_dp/README.md`

- **Verified.** Section 4 names the file, blob `3f05559f` at `57b8c867`.
- **The same blob is at live dev `9e3ccbfb`.** Its line 443 is the `[C]` row, "76 s bound across five DUT and five switch LeaveAll MRPDUs". Its lines 528-530 are the "What it cannot show" sentence, "does not restart on a received LeaveAll (processor issue 108)". Both match the PR text.
- **The PR states the two amendments:**
  - the `[C]` row becomes "at least three DUT and three switch LeaveAll MRPDUs";
  - the sentence becomes "now implemented", citing docs 10 §6.5.
- **Other items still match.**
  - `sim_crf_licence.cpp:953,956` still assert `>= 4` at both devs.
  - The parent `protocol-processor` gitlink is still `c951a9ff` at `9e3ccbfb`.
- **Completeness.** A read-only search of the parent at `9e3ccbfb` finds no other reference to issue 108 or to a LeaveAll count consumer outside `ieee8021q.md` MRP-5, the `milan_dp` README and `sim_crf_licence.cpp`. All three are on the list (`receipts/parent/milan_dp-readme-check.txt`).

### (2) `e2c631d`: the latency-independent stale-expiry guard

**The change.** `KL_srp_top.sv:1025-1033`. A LeaveAll-slot expiry is stale while any of these holds:
- a draw is requested (`need_draw_r`);
- a draw is in flight for that application (`dr_inflight_r` with a matching `dr_app_r`);
- `now_ms_i` is before the intended deadline, i.e. bit 31 of `now_ms_i - cad_dl_r[slot]` is set.

The code comment and docs 10 §6.5 (`:630-639`) state the clause: Table 10-5 rLA! and 10.7.5.22.

**Why a genuine expiry is never stale.** The guard uses the timer service's own `now_ms` and the same modular compare:
- the top wires `now_ms_w` and the combinational `exp_valid_w` from `u_timer` straight into `u_srp`;
- the service fires only when bit 31 of `now_ms_r - deadline` is clear (`KL_pp_timer_service.sv:191-193`), on the same cycle and the same value;
- `cad_dl_r[CAD_LA_*]` is written only when a draw lands (`:1159-1169`) and at reset, and it is the value the arm carries (`:1106`).

So a genuine expiry is never stale. The reviewer mutant `age-le-zero`, which is also stale at age 0, confirms that the boundary is exact: it fails 191 checks under 40 assertion IDs (`receipts/probe-guard/extra-mutants-full-suite.txt`).

**Committed arm (P8).**
- `sim_main.cpp:1442-1529` and the wrapper delay line (`srp_top_wrap.sv:193-228`, tb only, default 0).
- My run reports 0 own LeaveAll offsets at arm delays 3, 4, 8 and 16, for both applications (`ARMDELAY … own_msrp=0 own_mvrp=0`, `receipts/suites/srp_top.log`).
- `rearm-at-issue` (the issue-time guard restored) turns it red with 8 failing checks. The own MSRP LeaveAll offsets are 4, 4, 7 and 15, at -11..-8, -11..-8, -14..-8 and -22..-8. The own MVRP LeaveAll offsets are 2, 2, 6 and 14. This reproduces R399-1's receipts exactly.
- R399-1's own probe, unmodified, reports 0 of 83 offsets at delays 0, 2, 3, 4, 8 and 16 (`receipts/probe-armrace/summary.txt`). At `81b8d6d` it reported 0, 0, 4, 4, 5 and 5.

**Peer sweep.**
- M10 and P6 now sweep from -12 to +1 clocks, and placement is graded against the calibrated edge.
- P7 is the MVRP equal edge: at -1 and 0 the flag is dropped; at +1 it is accepted and goes out. That is the right reading of Table 10-5: the tick was tx!.

| Mutant | Killed by |
|---|---|
| `r-rearm-no-inflight` | M10 (3) and P6 (6) |
| `r-rearm-no-deadline` | M10 (3) and P8 (8) |
| `r-flag-ignores-edge-peer` | P7 (1) |

**Additional reviewer mutants, run on the full default suite:**

| Mutant | Result |
|---|---|
| `cross-deadline` (the applications' deadlines swapped) | killed, 18 checks |
| `mvrp-no-deadline` (the MVRP term alone removed) | killed by P8, 4 checks |
| `unsigned-compare` | survives, see S2 |

**Stale-forever hunt** (`scripts/probe_guard.py`, `receipts/probe-guard/`):

| Case | Stimulus | Result |
|---|---|---|
| Restart cycle, arm delay 0 and 16 | Peer MVRP and MSRP LeaveAlls 3 s before each own deadline | Each restarted timer fires 10-15 s after its peer, then 10-15 s later (MSRP +11.1 s, then 12.8 s and 13.0 s; MVRP +13.6 s, then 11.4 s and 13.2 s) |
| now_ms wrap between events | The same scenario with the 32-bit wrap placed at 12 points from before the first draw to after the second restarted cycle, at delays 0 and 16 | Identical results at every point |
| now_ms wrap at the expiry | P8 with the own MSRP deadline at `0xFFFFFFFF`, so the superseded deadline is before the wrap and the restarted one after it | Head: 13/13. A non-wrap-safe `now_ms_i < cad_dl_r` variant: 8 FAIL. The head's modular compare is required and correct at the wrap |
| Reset | One `rst_n` resets the timer service and the engine together (`protocol_processor_top.sv:800`, `:2248`) | Armed bits clear with `cad_dl_r`, and `need_draw_r` covers the first draw, so no stale expiry is possible after reset |
| A restart whose deadline never arrives | The restarted MSRP arm is dropped on its way to the timer service | The superseded expiry is swallowed and the MSRP LeaveAll timer stays silent for the 40 s observed. Under the issue-time guard it self-heals: the superseded deadline acts at +3.1 s and the cycle continues |

In the same-scenario peer/restart groups run at the wrap, the head's failures are artefacts of the harness: its `until_ms` compare is not modular, so `own_ms=0` is never reached. They are not DUT behavior, and the probe checks above use a modular wait.

The dropped-arm case is the only way to reach a stale-forever state. The author disclosed it in the PR body's "Round 2: what remains". It needs a counted arm-queue overrun at the top (`protocol_processor_top.sv:2699-2701`). The same overrun already stops the join and periodic cadence slots permanently, so the hazard is pre-existing and not widened in kind. It is recorded as S1.

**Result.** The assigned outcome is met.

### (3) `c9584bc` and `412efeb`: docs 10 §6.2 and §6.5

§6.2 (`:251-280`) states three things:

1. **The licence bound.** At most one `T-MRP-JOIN` plus any wait for a TX slot or the TX arbiter. It also names the encoder's own hold, where an MVRP drain waits behind a canceled own LeaveAll reservation. That hold was checked against the code: E_COLLECT keeps the encoder out of E_IDLE, so a start of an MVRP drain waits (`KL_srp_encoder.sv:556-607`).
2. **VLAN-table overflow.** The licence stays closed until the source is re-declared once an entry is free. Checked against the code:
   - `N_VIDS_P = 4` (`KL_srp_vlan.sv:49`);
   - `user_err_o` becomes `dbg_vlan_err_o` (`KL_srp_top.sv:434`);
   - `dbg_vlan_err_o` is not exported (`protocol_processor_top.sv:2323`).

   R399-1's licence probe, re-run unmodified, gives 8/8, and every line is identical to the round-1 receipt (S7: closed, still closed after a slot frees, open 149 ms after the re-declaration).
3. **The integrator ordering assumption.**

§6.5 (`:649-665`) states the per-application restart against per-type aging, with 10.7.5.20 and the NOTE. No RTL change was made for it, as the assignment directs. The PR body's section 4 carries the same three licence statements.

**Result.** The assigned outcome is met.

### (4) The parent consumer set, 16/16 with the declared crflic edit

- **Author's claim.** The PR body's "Round 2 validation" reports 16/16 rc 0 at `57b8c867` with the gitlink at `412efeb` and the declared edit. With the edit reversed, it reports exactly the two crflic counts failing, 3 and 3 counted.
- **Round-2 logs.** The round-2 author packet (`616889dd`) publishes the handoff and PR body but no round-2 parent logs.
- **Not re-run here.** This review does not run the parent bank; the brief does not allow it.
- **Evidence it is consistent with:**
  - the round-1 attribution receipts;
  - the fact that the change's parent-visible behavior is unchanged from round 1. `e2c631d` only narrows the window in which a stale expiry can act.
- **Manager duty.** The parent consumer bank at `9e3ccbfb` belongs to the manager (section 9).

## 3. Lenses

**Conformance: CLEAN.**
- The guard implements Table 10-5 rLA! (Start leavealltimer, Passive) with 10.7.5.22: a superseded deadline is no leavealltimer!.
- It is independent of the arm-path latency.
- The per-application reading and its per-type aging caveat are stated with 10.7.5.20 and the NOTE.
- Milan 4.3.2 is unchanged and re-verified (licence probe).

**RTL: CLEAN.**
- The guard reuses the service's `now_ms` and its modular compare.
- It does not suppress a genuine expiry (proved by construction and by `age-le-zero`).
- It is wrap-safe (the wrap-at-expiry probe).
- No new port. Zero-tolerance lint passes for every module.
- The dropped-arm residual is S1.

**Robustness: CLEAN.**
- Arm delays 0-16: no stale action, and the restarted cycles fire.
- The wrap at 12 event positions and at the expiry itself: correct.
- Reset: covered.
- The only stale-forever path is a counted, pre-existing arm-queue overrun (S1).

**Tests: CLEAN.**

| Suite | Checks |
|---|---|
| srp_top | 2200 |
| srp_stream_fsms | 1219 |
| srp_encoder | 581 |
| pp_top | 7751 |

- All four suites have 0 FAIL.
- The full srp_top campaign: 11/11 controls pass, and 78/78 arms are KILLED by their named assertions. Assertion coverage, the union of 8 chunks, is 65/65.
- Every count in the README's round-2 section matches my measurement.
- Test gaps are S2 and S3.

**Docs: CLEAN.**
- Read against the code: docs 10 §6.2 and §6.5, the `KL_srp_top.sv` guard comment, and the tb/srp_top README (P6-P8 rows and the round-2 section).
- The PR body's parent-visible list was checked against parent files at two devs.
- `make check` and `gen_matrix --check` rc 0, and `git diff --check c951a9ff..412efeb7` rc 0.
- The stale table cells are S3.

## 4. Findings

There are no BLOCKER, MAJOR or MINOR findings.

### S1: SUGGESTION. Lenses: Robustness, RTL, Docs

**Where:**
- `hdl/srp/KL_srp_top.sv:1215-1227`: a stale expiry is dropped with nothing re-armed;
- `docs/architecture/10_srp_engine.md:630-639`;
- `hdl/top/protocol_processor_top.sv:2610-2617` and `:2699-2701`: the arm queue drops the newest arm on overrun and counts it, visible in snapshot word 24.

**Authority.**
- 802.1Q-2014 10.6: the leavealltimer runs continuously.
- Table 10-5: rLA! restarts the timer, it does not stop it.

**Evidence.** `receipts/probe-guard/drop-head.txt` and `drop-rearm-at-issue.txt`, arm delay 0, the restarted MSRP arm dropped:

| Guard | Own MSRP LeaveAlls in 40 s | MSRP expiries |
|---|---|---|
| Head | 0 | 1 (the swallowed superseded one) |
| Issue-time guard | 4, the first at +3.1 s | 4 |

**Impact.**
- A counted arm-queue overrun on the SRP face after an rLA! leaves that application's own LeaveAll silent until the next received LeaveAll or reset.
- Before `e2c631d` the superseded deadline self-healed it. The same overrun already stops a join or periodic slot permanently, so the class of hazard is not new.
- It is disclosed only in the PR body, which does not survive into the tree.

**Suggested outcome.** Either:
- on a LeaveAll-slot expiry that is stale with no draw outstanding, set `cad_pend_r[slot]` so that `cad_dl_r[slot]` is re-issued (a duplicate arm is harmless, because the service overwrites the slot); or
- state the residual in §6.5 and track it in an issue.

**Verification.** With the re-issue, the drop probe shows the own MSRP LeaveAll resumes at `cad_dl_r`, and P1-P8 stay green.

### S2: SUGGESTION. Lenses: Tests, Robustness

**Where:**
- `hdl/srp/KL_srp_top.sv:1024`, which claims "same wrap-safe compare as the service";
- `tb/srp_top/sim_main.cpp:1442-1529` (P8).

**Evidence.**
- The reviewer mutant `unsigned-compare` (`now_ms_i < cad_dl_r[slot]`) passes the full committed suite, 2200/2200 (`receipts/probe-guard/suite-unsigned-compare.txt`).
- It fails 8 checks only when P8 runs with the own deadline at `0xFFFFFFFF` (`w14097-armdelay-unsigned-compare.txt`). The head passes that run 13/13.
- P8 also asserts no own LeaveAll and a restarted deadline register. It does not assert that the restarted deadline then fires under arm delay. My probe shows that it does, at delay 16.

**Impact.** The wrap-safety that the comment claims is correct at this head, but no committed check pins it. A regression would act only at the 49.7-day rollover coinciding with a stale window.

**Suggested outcome.**
- Add a tb-only way to start the timebase near the rollover and run one P8 delay there.
- Optionally, assert in P8 that the restarted timer fires once.

**Verification.** The `unsigned-compare` edit turns the new check red, and the head stays green.

### S3: SUGGESTION. Lenses: Docs, Tests

**Where.** The mutant tables in `tb/srp_top/README.md`:
- `:369-372`: `stale-expiry-honoured` 1, `mvrp-stale-expiry-honoured` 1, `mvrp-passive-lost` 4, `mvrp-flag-at-expiry` 6;
- `:263`, `:276` and `:281`: `pending-peer-ignored` 14, `leaveall-expiry-lost` 18 including M10, `preparation-before-slot` 22 including M10.

**Evidence.** Measured at the head (`receipts/mutants-full/`):

| Arm | Measured failing checks |
|---|---|
| `stale-expiry-honoured` | 7 |
| `mvrp-stale-expiry-honoured` | 7 |
| `mvrp-passive-lost` | 6 |
| `mvrp-flag-at-expiry` | 11 |
| `pending-peer-ignored` | 26 |
| `leaveall-expiry-lost` | 16, M10 no longer failing |
| `preparation-before-slot` | 21, M10 no longer failing |

These current counts appear only in the prose at `:409-413`. `mutants.py` gates on assertion names, not on counts, so no gate is wrong.

**Impact.** A reader of the tables sees superseded counts and tags.

**Suggested outcome.** Update the cells, or label the older tables as historical records superseded by `:409-413`.

**Verification.** Read the README against `receipts/mutants-full/`.

## 5. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_srp_top.sv:1016-1242` (guard, rLA!, expiry and draw paths); docs 10 §6.5; 802.1Q-2014 Table 10-5, 10.6, 10.7.5.20 and its NOTE, 10.7.5.22; Milan 4.3.2 and 4.4.1 (licence probe) | R399-2 | 412efeb750e358a65b04bae1cbb3086134d15b7e |
| RTL | CLEAN | the `hdl/` delta (`KL_srp_top.sv`); `KL_pp_timer_service.sv` compare and arm shadow; top timer wiring, reset and arm mux; `KL_srp_encoder.sv` E_IDLE/E_ALLOC/E_COLLECT; `KL_srp_vlan.sv`; lint_hdl rc 0; reviewer mutants `age-le-zero`, `cross-deadline`, `mvrp-no-deadline` and `unsigned-compare` | R399-2 | 412efeb750e358a65b04bae1cbb3086134d15b7e |
| Robustness | CLEAN (S1, S2) | `probe_guard`: arm delays 0 and 16, wrap at 12 points plus at the expiry, drop; R399-1 `probe_arm_race` at delays 0, 2, 3, 4, 8 and 16 (0/83 each); R399-1 `probe_licence` 8/8, identical; reset reasoning | R399-2 | 412efeb750e358a65b04bae1cbb3086134d15b7e |
| Tests | CLEAN (S2, S3) | srp_top 2200, srp_stream_fsms 1219, srp_encoder 581 and pp_top 7751, all 0 FAIL; full campaign 11 controls, 78/78 KILLED, coverage 65/65; P6-P8 and M10 source; 5 new or regenerated patches; README counts | R399-2 | 412efeb750e358a65b04bae1cbb3086134d15b7e |
| Docs | CLEAN (S1, S3) | docs 10 §6.2 (`:251-280`) and §6.5 (`:630-665`); RTL guard comment; tb/srp_top README; the PR body's parent-visible list against parent `57b8c867` and `9e3ccbfb`; `make check`, `gen_matrix --check` and `git diff --check` rc 0 | R399-2 | 412efeb750e358a65b04bae1cbb3086134d15b7e |

## 6. Prior public review findings at this head

### R399-1 (my own round 1, POSITIVE)

| Finding | Status | Evidence |
|---|---|---|
| S1 | RESOLVED | The guard is latency-independent (`e2c631d`). P8 is committed, and the round-1 probe reports 0 offsets at every delay. The residual it opens is new S1 |
| S2 | RESOLVED | docs 10 §6.2 and the PR body state the bound, the overflow and the ordering. The licence probe is identical to round 1 |
| S3 | RESOLVED | docs 10 §6.5 `:649-665` |

### R398-1 (prior-round internal review)

It was read only after the verdict and the ledger above were written. Nothing in it changes them.

| Finding | Status | Evidence at this head |
|---|---|---|
| F1 (MINOR, Docs): the parent-visible list omits `tb/verilator/milan_dp/README.md` | RESOLVED | The PR body's section 4 names the file (blob `3f05559f`), the `[C]` row at line 443 re-based to three and three, and lines 528-530 as now implemented. Verified against the parent at `57b8c867` and `9e3ccbfb` (section 2 item 1) |
| S1 (Robustness, Docs): a full VLAN table holds the licence closed | RESOLVED | docs 10 §6.2 `:261-271` and the PR body's section 4. The optional retry or export was not taken; the round-2 assignment put `dbg_vlan_err_o` out of scope. Licence probe S7 is unchanged |
| S2 (Tests): three narrow guards were unexercised (`rvw-rearm-no-inflight`, `rvw-rearm-no-cadpend`, `rvw-flag-ignores-edge-peer`) | RESOLVED | See the note below |
| S3 (Docs): the residual ordering assumption for the integrator | RESOLVED | docs 10 §6.2 `:273-280` and the PR body's section 4. The integrator guide's `srp_active_o` row (`docs/guides/integrator.md:330`) links to that section rather than restating it, as the single-source rule of `docs/README.md` §2 directs |

**Note on S2.** Each of the three arms is now killed by a named check:

| R398-1 arm | Checked-in arm | Killed by |
|---|---|---|
| `rvw-rearm-no-inflight` | `r-rearm-no-inflight`, the same edit | M10 (3) and P6 (6) |
| `rvw-rearm-no-cadpend` | re-based as `r-rearm-no-deadline`: the `cad_pend_r` term no longer exists, and the arm removes its replacement | M10 (3) and P8 (8) |
| `rvw-flag-ignores-edge-peer` | `r-flag-ignores-edge-peer`, the same edit | P7 (1) |

- M10 and P6 now sweep from -12 to +1 clocks.
- P7 is the MVRP equal-edge case.

## 7. Executed evidence (this packet)

- **Simulator.** Verilator 5.050, the CI pin.
  - The specified wrapper path does not exist.
  - A private wrapper onto the same 5.050 install was used.
  - Its binary hashes equal R399-1's (`receipts/verilator-identity.txt`).
- **Suites, gates and mutants:**
  - suites: `receipts/suites/`;
  - static gates: `receipts/static-rc.txt` and the three logs;
  - the full mutant campaign: `receipts/mutants-full/`, with `summary.txt` giving 78 KILLED, 0 other, 11 controls and coverage 65/65.
- **Probes:**
  - `receipts/probe-armrace/`: R399-1's probe, unmodified;
  - `receipts/probe-licence.txt`: R399-1's probe, unmodified;
  - `receipts/probe-guard/`: this round's probes.
- **Scripts.** `scripts/run_focused.sh` reproduces all of the above. `scripts/probe_guard.py` and `scripts/run_guard_sweep.sh` hold the round-2 probes, and `scripts/guard_jobs.txt` is the job list.
- **Public records:**
  - `receipts/evidence/`: the round-1 and round-2 author packets, with hashes;
  - `receipts/parent/`: the parent README and crflic checks;
  - `receipts/hosted-check-runs*.txt`.

## 8. Hosted checks at the exact head

These are observations only; the manager owns hosted and act acceptance. There are two runs: 36552665106 (push) and 36552673879 (pull_request).

| Check | Observed |
|---|---|
| `docs-gates` | completed with success in both runs |
| `portability` | completed with success in both runs |
| `suites` | still in progress in both runs at 10:31 UTC (`receipts/hosted-check-runs-final.txt`) |

**`suites` step detail at 10:31 UTC:**

| Step | Status |
|---|---|
| "Build Verilator v5.050" | skipped (cache hit), not executed |
| "Lint (zero tolerance) + every suite" | success in both runs |
| "SRP LeaveAll mutation campaign" | running |
| "Traceability matrix no-drift + untested budget 0" | pending |
| "nvm_port README figures" | pending |

No hosted result replaces a local run here.

## 9. Real limits and pending manager duties

**Not run by this review:**
- the parent consumer bank, the donor full bank, the gPTP bank, the Yosys bank and the builder;
- hosted or act runs;
- hardware.

Parent 16/16 is the author's claim. No round-2 parent log is public.

**Physical calibration.** NOT RUN. Field skips are not hardware proof.

**Clause text.** The 802.1Q and Milan PDFs are not distributed. Clause text, including the numbering of 10.7.5.22, is taken as quoted in the tree.

**Probe scope.**
- The wrap and drop probes are tb-only edits in scratch copies.
- Arm-queue overrun reachability at the real top was not measured.

**Manager duties at the merge turn:**
- build the final current-dev candidate at live dev `9e3ccbfb` (the gitlink is still `c951a9ff`);
- run the parent consumer set with the declared crflic re-base (`sim_crf_licence.cpp:953,956`, `>= 4` to `>= 3`);
- carry the parent document updates listed in the PR body's section 4, now including `tb/verilator/milan_dp/README.md` lines 443 and 528-530;
- complete hosted/act acceptance, including both `suites` jobs, which were still in progress at 10:31 UTC.

R399-2 FINISHED
