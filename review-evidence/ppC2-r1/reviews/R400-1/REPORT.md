[R400] NEGATIVE - exact head b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745

# R400-1: processor PR #135 (lane C2, MAAP), issues #66, #67, #68

- Exact head `b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745`, tree `7916d0854d52eecb28b03ac5e665d05355b7be08`, base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`.
- Scope was reconstructed from public sources only, in this order: the parent AGENTS.md / CONTRIBUTING.md at milan-fpga `82c7bcb1` (the processor repository has neither file); `docs/README.md`; issues #66, #67 and #68 (bodies plus the assignment comment 5884446021); IEEE 1722-2016 Annex B as the issues and `docs/architecture/11_maap_engine.md` cite it; `git diff c951a9ff..b03d36f2` and each of its four commits; then the public evidence at milan-fpga `82c7bcb1:review-evidence/ppC2-r1`, the hosted checks and my own runs.
- Prior public findings on PR #135: none. This is round 1, and the PR carries only the two review-start comments, so nothing needs resolving or retaining.
- Verdict: **NEGATIVE**. Four MINOR findings are open (F1 to F4), plus two SUGGESTIONs.
- The three issues' acceptance lists are met. So is the Release! fix, on the arc it changes.
- The findings are:
  - two gaps in the regression tests, each shown by a mutant that survives the head suite;
  - two Release! corners in the same engine that 11 §6 describes wrongly. The PR body mentions them, but no issue tracks them, and my probes show one of them goes further than the PR body says.

## Evidence I produced (packet paths)

| Run | Result | Receipt |
|---|---|---|
| Tool identity: Verilator 5.050 | The path in the brief (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin`) does not exist. I used the 5.050 wrapper at `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin`, and its identity and sha256 are recorded. All builds ran on 8 pinned CPUs. | `receipts/tool-identity.txt` |
| Head: `tb/maap` | rc 0, 114/114 | `receipts/head-maap-run.log` |
| Head: `tb/rx_validator` | rc 0, 453/453 | `receipts/head-rx_validator-run.log` |
| Head: `tb/pp_top maap-internal` | rc 0, 33 checks, 0 failures | `receipts/head-pp_top-maap-internal.log` |
| Head: `scripts/lint_hdl.sh` | rc 0, `KL_pp_maap` LINT OK | `receipts/head-lint_hdl.log` |
| Head: `git diff --check c951a9ff b03d36f2` | rc 0 | (command output; the file list is in `receipts/diff-name-status.txt`) |
| The PR's own `make -C tb/maap mutants` on a pristine export | rc 0. 3 controls PASS and 13/13 arms KILLED, with the same tallies as the ledger in `tb/maap/README.md` | `receipts/author-campaign.log`, `receipts/author-campaign/*` |
| Reviewer mutants (`mutations/r400-*.patch`) | See the table below | `receipts/r400-mutants/*` |
| Reviewer probes P1 to P5 on the head RTL (harness-only additions) | See F1, F2 and F4 | `receipts/probes-head-maap.log` |
| Base `KL_pp_maap.sv` with the head harness | U17b phases 1 to 3 and U18 fail. P4: all 8 drop offsets leave the engine unable to probe again, which is the wedge the fix removes. | `receipts/r400-mutants/base-rtl-probes-maap.log` |
| Clone integrity after the probes | HEAD, tree, index and all 321 tracked blobs match, including modes. No untracked or ignored files. No gitlinks exist in this repository. | `receipts/clone-verify.txt` |
| Hosted checks at b03d36f2 (snapshot 08:29 UTC) | On both workflow runs (push and pull_request), `portability` and `docs-gates` completed with success. `suites` is still in progress: its "Lint + every suite" step succeeded, and the SRP and MAAP campaign steps have not finished. | `receipts/hosted-checks.txt` |

### Reviewer mutants

| Arm | Planted defect | Head suites | Outcome |
|---|---|---|---|
| `r400-release-waits-for-draw` (my mutant against the Release! fix) | At `:569` the W_ADDR exit becomes `!eng_w && !draw_act_r`, so a Release! waits for the draw's answer before leaving. | `tb/maap` 114/114 | **SURVIVES**. Only probe P4 kills it (F4). |
| `r400-release-clears-mark-only-if-prng-idle` | The mark is cleared only when the PRNG is idle at the fall. | `tb/maap` 1 FAIL (U17b phase 2) | KILLED |
| (the PR's arm) `release-keeps-draw-mark` | The fix removed | `tb/maap` 22 FAIL (U17b phases 1 to 3 and onward) | KILLED |
| `r400-seed-clamp-off-by-one` | The seed clamp compares against `0xFE00 - count + 1` | `tb/maap` 114/114 | **SURVIVES** (F3) |
| `r400-compare-mac-word-reversed` | compare_MAC reverses 16-bit words instead of octets | `tb/maap` 7 FAIL; MP 5 FAIL | KILLED |
| `r400-compare-mac-last-octet-only` | compare_MAC compares only the last wire octet | `tb/maap` 114/114; MP 33/33 | **SURVIVES** (S1) |

## Findings

### F1: MINOR (Conformance, RTL, Robustness, Docs)

**Where:** `hdl/maap/KL_pp_maap.sv:610-677` (W_IVAL, the TX states and W_POST) and `:559-565`, compared with `:57` and `docs/architecture/11_maap_engine.md:135-137`.

**What happens:** a Release! that lands while a frame is being drawn or built sends that PDU anyway. It can publish a claim after the Release!, and a link bounce or outage can be absorbed completely.

**Authority and evidence**
- IEEE 1722-2016 Table B.7 says Release! goes to INITIAL and stops the timers, and footnote c says no PDU is sent. PortOperational! then starts a fresh walk. `11 §6` and the RTL banner at `:57` state the same rule.
- W_IVAL..W_POST never test `eng_w`, and the rise edge is sampled only in W_OFF (`:561`).
- Probe results at the exact head (`probes/release_probes.cpp`, `receipts/probes-head-maap.log`):
  - **P2** drops the link at each of 160 consecutive cycles after the 4th PROBE's lane grant. In 69 of them a PDU is sent after the Release!. In 70 of them `addr_valid_o` rises after the Release! (a DEFEND claim published for 1 cycle, which also triggers the per-source conflict fan-out).
  - **P3** applies a 5-cycle link bounce inside the sDefend TX path. The claim never drops, the DEFEND goes out, and the machine stays in DEFEND with no fresh walk.
  - **P5** holds a 100 ms outage while the lane is not granting. `addr_valid_o` stays 1 for the whole outage, and afterwards the same claim is kept with no re-probe.
- This is pre-existing: the PR's only RTL hunk is `:569-577`.
- The PR body's "What remains" mentions only "a frame ... still leaves the wire". The claim published after the Release! and the absorbed Release!/PortOperational! pair are not mentioned. No follow-up issue exists: I checked the processor issue list during this pass.

**Impact**
- Annex B's Release! semantics are broken on reachable arcs, and 11 §6 and `:57` state the opposite.
- The parent does not see this today, because it ties `cfg_maap_internal_i` to 0 (`hdl/milan/milan_datapath.sv:7695` at dev `57b8c867`). It affects any integrator who enables the engine.
- P5 depends on the MAC egress stalling while the link is down. That is integrator behaviour and was not measured in `tb/pp_top`.

**Required outcome:** either of the following.
- Fix it in this lane. Every walker state must honour an engage fall: no PDU after the fall, no advance of `pstate`, and a fall followed by a rise while the walker is busy must still produce INITIAL and a fresh walk. Each must have a failing arm.
- Or record an owner decision to defer it. That means a tracked issue carrying this evidence, and text in 11 §6 and at `:57` stating the known exception until the fix lands.

**Verification:** probes P2, P3 and P5 pass, or the issue link and the corrected doc text exist at the new head.

### F2: MINOR (RTL, Robustness, Docs)

**Where:** `hdl/maap/KL_pp_maap.sv:569-577` (the exit this PR changed), compared with `:294-299` and `docs/architecture/11_maap_engine.md:135-137`.

**What happens:** whether the footnote-a seed is re-armed depends on where the Release! lands.

**Authority and evidence**
- 11 §6 says every Release! ends with "seed re-armed for the next engage". The RTL comment at `:294-299` says "only a Release!/engage fall re-arms it".
- The W_ADDR exit leaves `seed_used_r` set.
- **P1** provisions seed 0x2000, forces a conflict yield and drops the link during the redraw. The next engagement probes `0x8ad6`.
- **P1c** is the same sequence, except the Release! lands after the yield-walk's first PROBE. The next engagement probes `0x2000`.
- This is the author's Observation A, which is not acted on and not tracked.
- It does not break Annex B: footnote a is permissive.

**Impact:** a provisioned or persisted range is re-probed or not depending on a few cycles of timing, and two contract texts describe it wrongly.

**Required outcome:** choose one rule, for example "re-arm on every Release!" or "never re-arm after an in-engagement conflict". Then make the RTL, the `:294-299` comment and 11 §6 agree, and add a test that grades both arcs. Alternatively, file a tracked issue and annotate the docs, as for F1.

**Verification:** P1 and P1c both give the result the stated rule predicts.

### F3: MINOR (Tests)

**Where:** `tb/maap/sim_main.cpp:687-715` (U18).

**What happens:** the boundary of the seed clamp is not graded.

**Authority and evidence**
- The Tests lens asks for boundary behaviour. Issue #66 targets the seed clamp directly.
- `r400-seed-clamp-off-by-one` passes 114/114. U18 seeds only `0xFFFF`, and U15 seeds only `0x1234`.
- Under that mutant, a seed of `0xFE00 - count + 1` claims a block ending at `91:E0:F0:00:FE:00`. That is outside the Table B.9 pool (B.1), which is exactly the mis-provisioned block the U18 comment says the clamp prevents.
- By contrast, the fit clamp's boundary is graded: U17 uses `0xFD02` and `0xFD01`, and the PR has a `fit-compare-off-by-one` arm.

**Impact:** a real B.1 defect in the clamp that issue #66 names would pass the suite.

**Required outcome:**
- Add byte-exact seeded cases at `0xFE00 - count + 1`, which must be clamped, and at `0xFE00 - count`, which must be taken as given.
- Add a ledger row for the boundary mutant.

**Verification:** `mutations/r400-seed-clamp-off-by-one.patch` fails `tb/maap` on the new named check, and the head stays green.

### F4: MINOR (Tests)

**Where:** `tb/maap/sim_main.cpp:662-684` (U17b).

**What happens:** the regression test for the Release! fix cannot tell the fix apart from a non-conformant alternative.

**Authority and evidence**
- The fix states that "a draw still in flight is abandoned" (`KL_pp_maap.sv:571-572`).
- `r400-release-waits-for-draw` passes 114/114. U17b drops the link only while every draw overhangs, and on that path the mutant behaves identically to the fix.
- **P4** drops the link during a draw that does fit.
  - At the head: of the 5 drop offsets that land before the answer, none sends a PDU, and the next engage probes after every offset.
  - With the mutant: 3 offsets send a PROBE after the Release!, which footnote c forbids.

**Impact:** a later change could reintroduce a PDU after Release! on this arc without turning any test red.

**Required outcome:**
- U17b, or a sibling scenario, also drops the link during a draw that fits, and asserts that no frame follows the Release! and that the next engage probes.
- Add a ledger row for the mutant.

**Verification:** `r400-release-waits-for-draw` fails `tb/maap` on the named check, and the head stays green.

### S1: SUGGESTION (Tests)

**Where:** `tb/maap/sim_main.cpp:51-52` (`WIN_MAC`, `LOSE_MAC`) and `tb/pp_top/sim_main.cpp` (MP4).

**Suggestion:** every tie-break pair differs in the least significant wire octet, so `r400-compare-mac-last-octet-only` survives both suites. Add one pair whose low octets are equal, so that a higher reversed octet decides the tie-break (B.3.6.4 compares all 48 bits).

### S2: SUGGESTION (Tests)

**Where:** `tb/maap/Makefile:4`.

**Suggestion:** `MUTANT_OUTPUT` defaults to the fixed shared path `/tmp/maap-mutants`, so concurrent campaigns overwrite each other's receipts. A per-run default would avoid that. The scratch trees are already per-run.

## Items examined and found correct (not findings)

- **#66, item 1 (fit clamp reject arm).** U17 (`sim_main.cpp:625`) uses the wrapper's kind-7 stub (`tb/maap/maap_wrap.sv`, harness only; kinds 5 and 6 pass through) to feed 0xFDFF, 0xFD02 and then 0xFD01.
  - Result: 3 draws, claim `…:FD:01` with count 255, the block ends at `…:FD:FF`, and the PROBE is byte-exact.
- **#66, item 2 (seed clamp).** U18 seeds 0xFFFF and probes `…:FD:F8` byte-exact with no draw. It then claims the block and grants the last source `…:FD:FF`.
- **#66, item 3 (mutations).** `fit-compare-forced-true` and `seed-clamp-removed` were each KILLED 4/114 (reproduced), and both are recorded in `tb/maap/README.md`.
- **#66, the fix, on its own arc:**
  - Every entry into W_ADDR has `pstate` INITIAL, so no stale claim is possible.
  - No timer is armed: a yield cancels the running slot (`:748-752`), and entry from W_OFF arms nothing.
  - No PDU is sent (P4 at the head).
  - The seed is not re-used (`seed_used_r` stays set; see F2 for the doc mismatch).
  - An answer abandoned in flight is harmless in both environments:
    - unit PRNG: busy falls on the same edge valid rises, so a re-engaged W_ADDR does not consume the stale answer (its mark is clear);
    - top: the owner mux routes the stale answer to MAAP while its mark is clear, and the shared busy signal covers the whole flight (`protocol_processor_top.sv:2708-2739`).
  - Both mutants that restore the old behaviour are KILLED.
- **#67:**
  - F28 (`tb/rx_validator/sim_main.cpp:684`) sends versions 2, 0 and 31. Each is committed, demuxed to `PP_PROTO_MAAP`, and delivers its version in the status lane. The header beat is checked against the independent model. Result: 453/453.
  - MP7 (`tb/pp_top/sim_main.cpp:8512`) sends version-2 and version-0 PROBEs against the DEFEND claim. Each gets a byte-exact unicast DEFEND carrying version 1 and the B.3.6.6 overlap, and the claim is kept.
  - `validator-maap-version-1-only` is KILLED in both suites: 47/453 and 4/33.
- **#68:**
  - The MAC pairs check their own premise (`only_reversed_lower`), and forward and reversed order disagree in both directions for PROBE/rProbe! (U9/U19), DEFEND/rAnnounce! (U7/U8) and DEFEND/rDefend! (U20/U21).
  - U22 drives PROBE/rAnnounce! from a peer that is reversed-higher.
  - MP4 uses `F2:11:22:33:44:01`, which disagrees in both orders against `0A:0B:0C:0D:0E:0F`.
  - `compare-mac-forward` is KILLED: `tb/maap` 9 FAIL, MP4 5 FAIL.
  - The ledger exists in the SRP form.
- **b03d36f.** A behaviour-neutral restructuring of the F28 case table: same three cases, same checks, 453/453. The parent rule-11 gate result is for the manager to confirm.
- **Parent-visible list.**
  - It is complete: one RTL hunk, and no change to ports, parameters or interfaces.
  - The other changes do not reach the parent:
    - harness-only ports in `maap_wrap.sv`;
    - the new entry points `make -C tb/maap mutants` and `tb/pp_top maap-internal`;
    - `.gitattributes`, and the CI step in `.github/workflows/hdl.yml`.
  - The parent at dev `57b8c867` ties `cfg_maap_internal_i` to 0 at `hdl/milan/milan_datapath.sv:7695`, and its gitlink is `c951a9ff`.

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | The acceptance lists of #66, #67 and #68 against U17/U17b/U18, U7-U10/U19-U22, F28, MP4 and MP7, and Annex B B.1, B.2.3, B.3.5, B.3.6.4 and Table B.7 (footnotes a and c) against `KL_pp_maap.sv:408-429, 559-777`; probes P2, P3 and P5 | R400-1 | b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745 |
| RTL | UNCLEAN (F1, F2) | `KL_pp_maap.sv:294-299, 559-777` (the walker, the fix, the draw serializer); `KL_pp_prng.sv:166-189`; `protocol_processor_top.sv:2708-2770` (PRNG owner mux); lint rc 0 | R400-1 | b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745 |
| Robustness | UNCLEAN (F1, F2) | Release! and link loss at every walker phase (U17b; P1 to P5); maximum count 255; seed 0xFFFF; maap_version 0 and 31; stale PRNG answers | R400-1 | b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745 |
| Tests | UNCLEAN (F3, F4; S1, S2) | `tb/maap/sim_main.cpp`, `maap_wrap.sv`, `mutants.py`, `mutations/*.patch`; `tb/rx_validator` F28; `tb/pp_top` MP4 and MP7; the PR campaign (16/16) and 5 reviewer mutants (3 survive) | R400-1 | b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745 |
| Docs | UNCLEAN (F1, F2) | `docs/architecture/11_maap_engine.md` §6 and §11; `tb/maap/README.md` (ledger tallies match my run); `tb/pp_top/README.md`; `tb/rx_validator/README.md`; the PR body (including its parent-visible list and "What remains") | R400-1 | b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745 |

## Limits

- The Verilator path given in the brief was missing. I used an identical-version (5.050) wrapper at a sibling path; its identity is in `receipts/tool-identity.txt`.
- Not run by me, either because the brief does not allow it or because it is the manager's duty:
  - the full `run_suites.sh`, the SRP campaign, Yosys, `make check`, the nvm figures;
  - any parent bank.
- At my snapshot the hosted `suites` job, including the MAAP campaign step, had not finished.
- P5 depends on the lane stalling during the outage. Whether the top's egress stalls while the link is down was not measured in `tb/pp_top`.
- The probes time their drop points inside the unit wrapper using knowledge of the RTL's internal timing.
- I found no manager evidence comment on the PR or the issues other than the review-start comments. The public executable evidence I used was the author packet at milan-fpga `82c7bcb1`. Its U17b receipt from before the fix was built with 5.052; I reproduced the same failures with 5.050.
- Annex B was judged from the clause citations in the issues and in 11. The standard itself is not distributed.
- No physical calibration was run (NOT RUN), and no hardware was involved. Skipped field contexts are not proof of hardware behaviour.

## Pending manager duties

- Run the donor full bank and the parent consumer bank (16 commands) at milan-fpga dev `57b8c867`, with the gitlink at `b03d36f2`.
- Confirm the parent rule-11 gate result for b03d36f.
- Accept the hosted `suites` job at the exact head, including the MAAP mutation campaign step.
- Decide on F1 and F2: fix them in this lane, or record a deferral with tracked issues and doc annotations.
- Get a re-review of the corrected head.
- Publish this packet: `REPORT.md` and the files listed in `MANIFEST.sha256`.

R400-1 FINISHED
