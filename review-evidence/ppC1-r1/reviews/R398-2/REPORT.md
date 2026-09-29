[R398] POSITIVE - exact head 412efeb750e358a65b04bae1cbb3086134d15b7e

# R398-2: independent internal delta review of processor PR #133 (lane C1, round 2)

- Exact head `412efeb750e358a65b04bae1cbb3086134d15b7e`, tree `f12258a0111546105e68bfdee95a1ebf141676f8`.
- Delta: `81b8d6d7..412efeb7`, three commits (`e2c631d`, `c9584bc`, `412efeb`), plus the PR-body amendment.
- Source base: `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`. The full `c951a9ff..412efeb7` diff was also read, for context.
- Assignment: processor issue #108 comment 5886235840 (round 2).

## Verdict

POSITIVE. This review has no open BLOCKER, MAJOR or MINOR finding.

- **R398-1 F1 (MINOR): resolved.** The only open finding from round 1.
- **Round-1 suggestions:** all five are resolved at this head (R398-1 S1-S3 and R399-1 S1-S3; R399-1 S2 and R398-1 S1 are the same item).
- **New suggestions:** two, S1 and S2. Neither affects the verdict.
  - S1 is the stale-forever case the brief asked me to hunt. It exists only when the processor top's arm queue drops the re-arm (a counted overrun). The author discloses it, and it belongs to a failure class that already existed at the source base.

## How this review was reconstructed

1. **Contributor guides.** The processor repository has no `AGENTS.md` or `CONTRIBUTING.md` (searched the whole tree). The conventions are `docs/README.md`: single-source rules, spec citation, and `make check` before commit.
2. **Scope.** Issue #108:
   - the body and its frozen acceptance: Table 10-5 rLA!; docs 10 section 6.5 and docs/10 agree; donor and parent consumer gates;
   - lane assignment 5883702094;
   - round-2 assignment 5886235840;
   - TAKEN and REVIEW READY markers.
3. **PR #133 body at this head.** Round-1 sections, section 4 as amended, and the "Round 2" section.
4. **Authorities**, as quoted in the issue, the assignment and the docs: 802.1Q-2014 Table 10-5 rLA!, 10.6, 10.7.5.20 (b and NOTE), 10.7.5.22; Milan v1.2 4.3.2 and 4.4.1. The standards PDFs were not available to me.
5. **Code and docs read:**
   - `git diff 81b8d6d..412efeb`: `hdl/srp/KL_srp_top.sv`, `tb/srp_top/{sim_main.cpp,srp_top_wrap.sv,README.md,mutants.py,mutations/*}`, `docs/architecture/10_srp_engine.md`;
   - the whole guard context: `KL_srp_top.sv:940-1248`;
   - the timer service: `hdl/common/KL_pp_timer_service.sv`, including its compare, arm shadow and reset;
   - the processor top's wiring of `now_ms`, expiry and reset (`protocol_processor_top.sv:784-813,2233-2300`) and its arm queue (`:2608-2705`);
   - encoder drain gating (`KL_srp_encoder.sv:316-348,556-605,762-763`);
   - the integrator row (`docs/guides/integrator.md:330`).
6. **Public evidence.**
   - The manager's tree `kebag-logic/milan-fpga@a6427910/review-evidence/ppC1-r1` holds `MANIFEST.json`, `author/HANDOFF.md` and `author/PR-BODY.md`. I read MANIFEST.json only, and diffed the published PR-BODY against the live body.
   - Parent blobs at dev `57b8c867` and `9e3ccbfb`.
   - Hosted check runs at `412efeb7`.
7. **Prior public reviews.** R398-1 and R399-1 were read only after my own pass over the diff and my probes. No round-2 report by another reviewer was read.

## Answers to the brief's focus items

### (1) The PR body's parent-visible list names `tb/verilator/milan_dp/README.md`: yes

Section 4, "Parent documents to update at adoption", names the file (blob `3f05559f` at `57b8c867`). It covers both locations:

- the `[C]` row, line 443 ("76 s bound across five DUT and five switch LeaveAll MRPDUs"), re-based to "at least three DUT and three switch";
- the "What it cannot show" sentence, lines 528-530 ("... does not restart on a received LeaveAll (processor issue 108), and nothing here measures that."), marked as now implemented, with a pointer to docs 10 section 6.5.

Checks against the parent:

- Line numbers and wording match the parent blob byte for byte.
- At the manager's dev `9e3ccbfb` the README blob is still `3f05559f`, `sim_crf_licence.cpp` is still `6f9d17b1` (lines 953/956 `>= 4`), and the processor gitlink is `c951a9ff`. The declared edit and the list therefore apply unchanged at the merge dev.
- Receipt: `raw/parent_blob_check.txt`.

### (2) `e2c631d`: the stale guard is latency-independent, with no stale-forever case except a dropped arm

**RTL.** At `KL_srp_top.sv:1025-1033`, `la_rearm_w` is now:

`need_draw_r[app] || draw in flight for app || (now_ms_i - cad_dl_r[slot])[31]`

The third term is modular age, the same compare as `KL_pp_timer_service.sv` `age_w`. Consequences:

- `cad_dl_r[LA slot]` is written only when a draw lands (`:1162-1168`), and in the same clock `cad_pend_r` is set so that exact value is armed. Reset clears it (`:1055`).
- The service fires only when `now_ms_r - deadline >= 0`.
- The engine and the service share the same `now_ms_w` wire and the same `rst_n` at the processor top (`protocol_processor_top.sv:802,2248,2286`). Expiries reach the engine directly (`exp_valid_w`).
- So a genuine expiry of the restarted deadline always sees an age >= 0 and is honoured. A superseded deadline firing before it is stale, whatever the arm-path latency.
- The comment cites Table 10-5 rLA! and 10.7.5.22, and docs 10 section 6.5 (`:630-639`) states the rule.

**Committed probe (P8).** `srp_top_wrap.sv` adds a tb-only arm delay line (0 to 16 clocks). P8 runs by default and as `RUN_ARGS=armdelay`. At head:

```
ARMDELAY delay=3 offsets=-15..+2 own_msrp=0 own_mvrp=0
ARMDELAY delay=4 offsets=-16..+2 own_msrp=0 own_mvrp=0
ARMDELAY delay=8 offsets=-20..+2 own_msrp=0 own_mvrp=0
ARMDELAY delay=16 offsets=-28..+2 own_msrp=0 own_mvrp=0
```

That is 0 own-LeaveAll offsets at 3, 4, 8 and 16 (`raw/head_srp_top_armdelay.log`).

**Mutation arms**, re-run here from the checked-in patches (`raw/mutants_A.log` … `_C.log` and `raw/mutants/`):

| Arm | Result here | Kills and counts |
|---|---|---|
| `rearm-at-issue` (the issue-time guard restored) | KILLED | P8, 8 failures. Own MSRP at 4/4/7/15 offsets and own MVRP at 2/2/6/14, for delays 3/4/8/16 |
| `r-rearm-no-inflight` (= R398-1 `rvw-rearm-no-inflight`, same edit) | KILLED | M10: 3 (peer -4..-2); P6: 6 (-7..-2) |
| `r-rearm-no-deadline` (R398-1 `rvw-rearm-no-cadpend`, re-based) | KILLED | M10: 3; P8: 8 |
| `r-flag-ignores-edge-peer` (= R398-1's arm, same edit) | KILLED | P7: 1 (delta 0) |
| `stale-expiry-honoured` / `mvrp-stale-expiry-honoured` | KILLED | 7 (M10) / 7 (P6) |
| `expiry-only-redraw` / `mvrp-expiry-only-redraw` / `draw-kind-0` | KILLED | 15 / 17 / 6 |
| `mvrp-passive-lost` / `mvrp-flag-at-expiry` | KILLED | 6 / 11 |
| `pending-peer-ignored` / `leaveall-expiry-lost` / `preparation-before-slot` | KILLED | 26 / 16 / 21 |

- `rvw-rearm-no-cadpend` is re-based because the term it removed (`cad_pend_r`) no longer exists; `r-rearm-no-deadline` removes the term that replaced it. The rebase is legitimate.
- Every count equals the PR body and `tb/srp_top/README.md:381-413`.
- The positive controls (armdelay, peer, restart, timers) pass.

**Sweep widths.**

- M10 (`sim_main.cpp:878`) and P6 (`:1350`) now sweep -12..+1 clocks (`REARM_CLOCKS = 12`, `:613`). That exceeds the -7 clocks the guard needs at delay 0.
- They grade placement against the calibrated edge.
- P7 (`:1390`) is the MVRP equal-edge case: -1 and 0 drop the flag, +1 sends it.

**Stale-forever hunt.**

- **Wrap of `now_ms`: clean.**
  - Probe `scripts/probe_guard.py wrap` resets the timebase to a value near 2^32. The DUT and timer run on absolute time; the bench sees reset-relative time. The timebase then wraps 5, 12 or 16 s after reset: around the startup arms, inside the MVRP restart, and inside the MSRP restart.
  - At head, `armdelay`, `restart`, `peer` and `timers` all pass at every placement (13/13, 49/49, 89/89, 7/7), with P8 0/0 at every delay. The base-0 control of the probe also passes.
  - The discriminating control replaces the modular compare with an unsigned `now < deadline`. It fails P8 at both straddling placements (8 and 4 failures) and fails 3 `peer` checks at 16 s.
  - So the probe can detect a wrap bug, and head has none. Receipts: `raw/probe_wrap-*.log`.
- **Reset: clean by construction.** Engine, timer service and arm queues share `rst_n` at the processor top. Reset clears `cad_dl_r`, `armed_r`, `now_ms_r` and the arm queues together, and init requests both draws (`:1179-1188`). The tb delay line also clears on reset (`srp_top_wrap.sv` `arm_delay_line`).
- **A restart whose deadline never arrives: exists only if the re-arm is dropped.** This is S1 below. Receipt: `raw/probe_drop_*.log`.

### (3) `c9584bc` and `412efeb`: docs 10 sections 6.2 and 6.5 state what was required

- **Section 6.2, `:251-259`, the licence's added wait.** One `T-MRP-JOIN` plus the wait for a TX slot or the TX arbiter. It also names the encoder's hold-back behind a canceled empty LeaveAll reservation, and says the licence rises one clock after acceptance.
  - I checked the hold-back case in the RTL. The encoder latches the MVRP tick (`KL_srp_encoder.sv:333,763`), and a fresh declaration always pushes MSRP content that releases `E_COLLECT` at the next join tick.
  - So the PR body's shorter wording ("one T-MRP-JOIN plus TX slot or arbiter wait") holds to within one MSRP MRPDU's encode time.
- **Section 6.2, `:261-271`, the VLAN-table overflow.** It holds the licence closed until re-declaration. Refusal is visible only on `dbg_vlan_err_o`, which is not exported; that matches `protocol_processor_top.sv:2227,2323` (`srp_dbg_vlan_err_nc_w`).
- **Section 6.2, `:273-279`, the ordering assumption.** The licence rises one clock after the arbiter grant, while the MRPDU is still serializing. The parent's egress must not let a licensed stream frame overtake it.
  - The integrator row (`docs/guides/integrator.md:330`) links `#sec-10-join-before-stream` (`10_srp_engine.md:239`), which heads this same subsection. The integrator therefore reaches the statement.
- **Section 6.5, `:649-664`, per-application restart versus per-type aging.**
  - Types the peer did not flag are aged about every other cycle against a same-range peer, and never against a faster one. Such a peer departs from 10.7.5.20 as #106 applies it, and the RTL does not compensate.
  - This agrees with the RTL (`:1233-1241`: any MSRP-type lane restarts the MSRP timer).
- **PR-body section 4** carries the same three 6.2 statements.

### (4) The parent consumer set with the declared crflic edit

- The PR body reports 16/16 rc 0 at dev `57b8c867`, with the edit committed in a scratch parent only (`sim_crf_licence.cpp:953,956`, `>= 4` to `>= 3`).
- It reports the attribution with the edit reversed: `crflic` fails exactly its two counts (3 and 3), matching the manager's 15/16 gitlink-only result at `81b8d6d`.
- The sixteenth command is now named (`python3 scripts/lint_rtl.py --check`).
- I did not re-run parent banks; the brief forbids that. The manager runs the parent consumer bank at `9e3ccbfb`. The two blobs involved are unchanged there (item 1).

### Hosted processor checks at `412efeb7`

Last snapshot 2026-09-29 10:22 UTC (`raw/hosted_checks_412efeb*.txt`, `raw/hosted_suites_steps_*.txt`). There are two `hdl` runs, one on push and one on pull_request:

| Job | State |
|---|---|
| `docs-gates` | success, both runs |
| `portability` | success, both runs |
| `suites`, step "Lint (zero tolerance) + every suite" | success, both runs (finished 10:12 and 10:13) |
| `suites`, step "SRP LeaveAll mutation campaign" | in progress, both runs |
| `suites`, matrix and `nvm_port` figures steps | pending |

"Build Verilator" was skipped because the cache hit. That is a skipped build step, not a skipped test. Hosted acceptance is the manager's.

## Findings

No BLOCKER, MAJOR or MINOR findings are open.

### S1 - SUGGESTION - Robustness, RTL, Docs - a dropped LeaveAll re-arm now silences that application's own LeaveAll until the next received LeaveAll or reset

**Where.**
- `hdl/srp/KL_srp_top.sv:1025-1033` (`la_rearm_w`), `:1215-1227` (a stale expiry does nothing);
- `hdl/top/protocol_processor_top.sv:2608-2705`: the SRP arm face is a 4-deep queue behind the listener, talker and ADP faces, and "a queue overrun drops the NEWEST arm and counts";
- `docs/architecture/10_srp_engine.md:630-639`.

**Authority.**
- 802.1Q-2014 Table 10-5 and 10.7.4.3: the leavealltimer always runs, restarted on rLA! and on its own expiry.
- The processor top's own contract: drops are counted, never silent (side-port register 24, `docs/guides/operator.md:137`).

**Evidence.** `scripts/probe_guard.py drop` drops the re-arm that follows a received LeaveAll (the second non-cancel arm of each LeaveAll slot). One peer MVRP and one peer MSRP LeaveAll arrive 3 s before the own deadlines, then no peer LeaveAll for 60 s:

```
head:              mvrp_expiries=1 msrp_expiries=1 own_mvrp_la_frames=0 own_msrp_la_frames=0 drops=2
issue-time guard:  mvrp_expiries=5 msrp_expiries=5 own_mvrp_la_frames=5 own_msrp_la_frames=5 drops=2
```

(`raw/probe_drop_head.log`, `raw/probe_drop_issueguard.log`)

**What this shows.**
- At head, the superseded deadline fires, is correctly stale, and nothing re-arms the slot.
- Under the round-1 guard, that superseded expiry was (non-conformantly) honoured, and the cadence healed itself.
- The author discloses this in the PR body ("Round 2: what remains").
- It is not in the durable docs.

**Impact.**
- It needs a counted arm-queue overrun on the SRP face, which is rare. It then heals at the next peer LeaveAll of that application.
- It stays silent only if the peer then stops sending LeaveAlls.
- A dropped cadence arm already stopped any cadence slot at the source base, including the LeaveAll slot after its own expiry. This PR adds one more arm per received LeaveAll to that exposure; it does not create the class.

**Suggested outcome (non-blocking).**
- Record the consequence in docs 10 section 6.5 or in a follow-up issue.
- Optionally adopt the author's own proposal: when a LeaveAll-slot expiry is stale and no draw is outstanding, set `cad_pend_r[slot]` to re-issue the intended `cad_dl_r[slot]`. This is idempotent when the arm is only late.

**Verification.** The drop probe at the fixed head shows own LeaveAlls resuming at the restarted deadline, and P8/M10/P6/P7 stay green.

### S2 - SUGGESTION - Tests - no committed check exercises the guard across a `now_ms` wrap

**Where.**
- `tb/srp_top/srp_top_wrap.sv`: the timer service resets `now_ms` to 0;
- `tb/srp_top/sim_main.cpp` (`until_ms`, `restarted`): unsigned bench arithmetic.

**Evidence.** A plain unsigned `now < deadline` guard passes every committed check. Only this packet's wrap probe (`raw/probe_wrap-*-unsigned.log`) tells it apart from the modular compare at head.

**Impact.** Wrap safety rests on reading the code plus this packet's probe. A future edit to the compare would not be caught.

**Suggested outcome (non-blocking).** A wrapper parameter for the timebase's reset value, with the bench reading reset-relative time (the probe's construction), and one wrap placement per application inside P8 or P3.

## Prior public review findings, resolved or retained at this head

| Item | State at `412efeb7` | Evidence |
|---|---|---|
| R398-1 F1 (MINOR), parent-visible list omits the milan_dp README | Resolved | PR body section 4; `raw/parent_blob_check.txt` (lines 443 and 528-530, blob `3f05559f`, unchanged at `9e3ccbfb`) |
| R398-1 S1 = R399-1 S2, VLAN overflow and licence bound | Resolved | docs 10 `:251-271`; PR body section 4 |
| R398-1 S2, narrow guards unexercised | Resolved | the M10/P6 sweep -12..+1, P7 and P8. `r-rearm-no-inflight`, `r-rearm-no-deadline` (re-based `rvw-rearm-no-cadpend`) and `r-flag-ignores-edge-peer` are killed by named checks (`raw/mutants_A.log`, `_B.log`) |
| R398-1 S3, integrator ordering assumption | Resolved | docs 10 `:273-279`, reached from `integrator.md:330` through `#sec-10-join-before-stream` |
| R399-1 S1, latency-dependent guard | Resolved | the guard at `KL_srp_top.sv:1025-1033`; P8 0/0 at delays 3/4/8/16; `rearm-at-issue` killed (P8: 8) |
| R399-1 S3, per-type aging caveat | Resolved | docs 10 `:649-664` |

No MINOR or higher finding from earlier rounds remains open.

## Lens results

- **Conformance: CLEAN.**
  - Table 10-5 rLA!, "Start leavealltimer, Passive", and 10.7.5.22: a superseded deadline's expiry is not leavealltimer!, and a genuine one is always honoured. This holds by reading and under arm delays of 0-16, three wrap placements and reset.
  - Milan 4.3.2 licence semantics are unchanged in round 2.
- **RTL: CLEAN.**
  - The guard is combinational on existing registers: 15 lines, no new state, no port or parameter change.
  - `verilator --lint-only -Wall` (the `lint_hdl.sh` flags) passes with 0 warnings for `KL_srp_top` and `protocol_processor_top` (`raw/lint_*.log`).
  - `git diff --check c951a9ff..412efeb7` returns rc 0.
- **Robustness: CLEAN.**
  - Wrap and reset were hunted, and both are clean.
  - The one stale-forever case needs an upstream counted arm drop, is disclosed, and extends a failure class that already existed. It is S1, a SUGGESTION.
- **Tests: CLEAN.**
  - Full `srp_top` at head: 2200/2200 PASS, rc 0 (`raw/head_srp_top_default.log`).
  - The armdelay, restart and peer groups pass separately.
  - 16 mutant arm/group runs across 13 arms, plus 7 positive controls: all KILLED by their named assertions, with counts equal to the recorded ones.
  - The P8 committed probe meets the brief exactly.
  - S2 (wrap not pinned) is a SUGGESTION.
- **Docs: CLEAN.**
  - Sections 6.2 and 6.5 state all four required items, and they agree with the RTL.
  - The `tb/srp_top/README.md` counts and group list are accurate.
  - The PR-body parent-visible list is complete for the milan_dp README.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Table 10-5 rLA! and 10.7.5.22 against `KL_srp_top.sv:1016-1241` and `KL_pp_timer_service.sv` compare; docs 10 sections 6.2 and 6.5; P8/M10/P6/P7 receipts; wrap and drop probes | R398-2 | 412efeb750e358a65b04bae1cbb3086134d15b7e |
| RTL | CLEAN | `KL_srp_top.sv` diff and context; processor-top `now_ms`/expiry/reset/arm-queue wiring; encoder drain gating; lint of two tops; `git diff --check` | R398-2 | 412efeb750e358a65b04bae1cbb3086134d15b7e |
| Robustness | CLEAN (S1 open as SUGGESTION) | arm-latency sweep 0-16; `now_ms` wrap at 5/12/16 s with an unsigned control; reset path; dropped re-arm probe | R398-2 | 412efeb750e358a65b04bae1cbb3086134d15b7e |
| Tests | CLEAN (S2 open as SUGGESTION) | `srp_top` default 2200/2200; groups armdelay/restart/peer; `mutants.py` arms A-E with 7 controls; `sim_main.cpp` P7/P8/M10/P6 code; `srp_top_wrap.sv` delay line | R398-2 | 412efeb750e358a65b04bae1cbb3086134d15b7e |
| Docs | CLEAN | `10_srp_engine.md:239-279,630-664`; `integrator.md:330`; `tb/srp_top/README.md`; PR body sections 4 and "Round 2"; parent README/crflic blobs at `57b8c867` and `9e3ccbfb` | R398-2 | 412efeb750e358a65b04bae1cbb3086134d15b7e |

## Executed here

All runs were in the foreground, with at most 8 parallel jobs. Builds and probes ran in disposable copies under the packet's `scratch/`; `scripts/run_probes.sh` reproduces them. In the published receipts, local paths are shortened to `<packet>`, `<clone>`, `<tmp>` and `~`, and they are listed in `MANIFEST.sha256`.

**Simulator.** The brief's path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used a byte-identical wrapper copied from the manager's `ppC1-manager-412efeb7/pinned-tool-bin`. It reports `Verilator 5.050 2026-07-01 rev v5.050`, and the wrapper and underlying binaries are hashed in `raw/verilator_identity.txt`.

| Command (work copy of the exact head) | Result |
|---|---|
| `Vsrp_top_sim` (default) | 2200 checks, 0 FAIL, rc 0, 166 s |
| `Vsrp_top_sim armdelay` / `restart` / `peer` | 13/13, 49/49, 89/89, rc 0 |
| `mutants.py --only …` (5 slices) | 7 controls PASS; 16 of 16 arm/group runs KILLED (13 arms) |
| `probe_guard.py wrap` (4 bases at head, 2 unsigned controls) | head: all PASS at every base; unsigned control: P8 8 and 4 FAIL, peer 3 FAIL |
| `probe_guard.py drop` (head, issue-time guard) | head 0/0 own LeaveAlls in 60 s; issue-time guard 5/5 |
| `verilator --lint-only -Wall` (the `lint_hdl.sh` flags), `KL_srp_top`, `protocol_processor_top` | rc 0, 0 warnings |
| `git diff --check c951a9ff..412efeb7` | rc 0 |

**Clone integrity** after all probes (`raw/clone_integrity.txt`):
- HEAD, tree and index are identical to `412efeb7`;
- the working tree is clean, including ignored files;
- every tracked file re-hashes to its blob;
- `git fsck` is clean;
- the processor tree has no gitlinks (0 mode-160000 entries), so there is no submodule gitlink to verify.

## Real limits

- No hardware and no physical calibration. Field skips are not hardware proof.
- I did not run the full processor bank (`run_suites.sh`, Yosys, nvm figures), the full 78-arm campaign, or any parent bank; the brief forbids these. Only `srp_top` (the one suite round 2 touched), the round-2 arms and the re-measured arms were run.
- The arm-drop reachability at the processor top (SRP face overrun under listener/talker/ADP contention) was not simulated. S1's probe forces the drop in the `srp_top` wrapper.
- The public evidence tree at `a6427910/review-evidence/ppC1-r1` holds round-1 author material only. The manager's bank receipts at `412efeb7` were not in public material I could inspect.
- The standards PDFs were not available. Clause wording is as quoted in the issue, the assignment and the docs.
- The hosted `suites` mutation campaign and its later steps had not finished at the snapshot.

## Pending manager duties

- **Hosted acceptance at `412efeb7`.** The `suites` job must finish: the SRP LeaveAll mutation campaign, the matrix and the `nvm_port` figures.
- **Parent consumer bank at dev `9e3ccbfb`** with the declared crflic edit (`sim_crf_licence.cpp:953,956`, `>= 3`). Without the edit, `milan_dp` `obj_crflic` [C] is expected to fail 2/415, attributed to #108 item 1.
- **The final current-dev candidate at merge** (source base `c951a9ff`, live dev `9e3ccbfb`).
- **At pin adoption,** the parent documents in PR-body section 4, including `tb/verilator/milan_dp/README.md` lines 443 and 528-530.
- **Follow-ups the author reports:**
  - the re-DECLARE_TALKER VLAN refcount leak;
  - S1's re-issue option.

R398-2 FINISHED
