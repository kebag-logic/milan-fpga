[R729] POSITIVE - exact head 409c3075a6c5525d283de5a93584ad87a4528137

# R729-2: independent internal review of FPGA-gPTP PR #95 (issue #94), round 2

- **Head:** `409c3075a6c5525d283de5a93584ad87a4528137`, tree `b552de2244475b15bfc430b683f8a4fe9c6a7db3`. Seven commits on the round-1 head `9d509029`, which sits on main `f97c1803`.
- **Scope:** a delta review of `9d509029..409c3075`. I resolved every named round-1 finding at its cause. Code the delta does not touch keeps its round-1 lens verdict, except where the delta changes what that code depends on.
- **Order of work:** I reconstructed scope from the repository guides, the issue's frozen acceptance and the manager's two assignment comments. Then I read the authorities, the delta and the published evidence. I made my own pass over the delta, wrote my own probes and ran the gates before I read either round-1 report.

## Verdict

**POSITIVE.** All five lenses are clean. The three round-1 behavioural findings are fixed at their cause, and each now has a permanent check and a planted control. I found no new behavioural defect and no missing gate.

- **The fixes, re-checked here:**
  - Both mutation arms: 113/113 at base and 136/136 at head.
  - The engine suite: 2,048 ×3 + 60 at head.
  - Both round-1 reviewers' probes at head.
  - Seven new probes of my own: 36 checks, all passing at head.
  - The parent `milan_dp` `gptp` and `gptp-lat` legs: 205/205 each, on a parent snapshot with gitlink `409c3075`.
- **Open findings:** none at MINOR, MAJOR or BLOCKER. There is no RESIDUE in the delta.
- **Suggestions:** three, none blocking (S1 to S3).
- **Manager duty before merge:** the live PR body is still the round-1 text, with round-1 figures. The round-2 body is ready in the evidence packet. See "Pending manager duties".

## Prior findings at this head

| Finding | Defect at `9d509029` | Fix at `409c3075` (cause) | Verification here | State |
|---|---|---|---|---|
| R729-F1 = R730-F3 | A warm reset taken with the port low inside a cease. The first rise raised no edge, so the retained cease ran out its countdown. | `port_seen_r` became `port_ref_r <= 1'b1` (`hdl/top/KL_gptp_engine.sv:1124`). The first sample after release is now the reference level, so a port low at release makes its rise an edge (`:1127`). | My round-1 probe D: `first request 0 ms after the rise`, where round 1 gave 3000 ms. The R730 probe gives `elapsed=245` cycles, where round 1 gave 7,800,201. My Q2 gives 245 cycles. The new phase 51 checks this; control "the first rise after a disabled release raises nothing" fails it. | **Resolved** |
| R729-F2 = R730-F2 | NOT_ENABLED left the armed `S_RSPSEQ` in place. A Follow_Up after the fall paired, published 701 ns and committed. | NOTEN zeroes `S_RSPSEQ` (`hdl/ucode/gen_gptp_ucode.py:2211`). A zero word is "no response" (`:489`), and the armed value carries bit 16 (`:154`), so sequenceId 0 cannot alias it. `S_PDGOT`, set by NOTEN, also refuses a new arm (`:1319-1324`). The request claim is cleared while the port is disabled (`KL_gptp_engine.sv:1100-1103`), so a pair frozen for its t1 cannot complete. | Probe A: `pdelay before 601 after 601; commits after the FU 0`. The R730 probe: `delay_before=601 delay_after=601 commits=0`. My Q1, with Resp and Follow_Up both heard while disabled: 0 commits, 601→601. Its enabled control Q1c pairs (601→701, one commit), which shows the stimulus can pair. Phase 48's three orderings check this; control "NOT_ENABLED keeps the armed response" fails them. | **Resolved** |
| R730-F1 | A stalled serializer held NOTEN back, so asCapable stayed up. It could also start a frame while the port was disabled. | **Withdrawal:** `KL_gptp_tx_slot` gains `cancel_i`. A frame whose first byte is unaccepted is withdrawn, with valid masked in the same cycle (`hdl/wire/KL_gptp_tx_slot.sv:127`, `:129`, `:148-150`), driven by `!port_en_r` (`KL_gptp_engine.sv:1161`). A started frame runs to its last byte. **Dispatch:** NOTEN dispatches ahead of the result and the queue without waiting for `ser_idle` (`:624-629`, `:652-660`). Its leg builds and sends nothing. | The R730 probe: `flags=b valid=0 sof=0` and 0 frames after ready returns; round 1 gave `flags=f valid=1`. Phases 49 and 50 check this (byte 0, then bytes 1, 34 and 67). My Q5 (a reply SEND while disabled, ready high) and Q6 (a rise during a stalled started frame) pass. Five controls fail these checks. | **Resolved** (see the Robustness lens for the parent boundary) |

Both round-1 probe sets reproduce byte for byte at head, matching the author's published head receipts. `receipts/r729-1-probes-at-head.txt`, `r729-1-sweep-at-head.txt` and `r730-1-probe-run-at-head.log` are each `cmp`-identical to `author-r2/receipts/probes/*`. The round-1 cadence sweep C (151 rise offsets) still gives `0 with two or more requests, 0 with none`.

The 12 new repository checks that fail at the round-1 RTL fail exactly where the findings stood. I reproduced this by building the head harness against the round-1 RTL and generator: `receipts/probes-at-round1-rtl-run.log`, 14 FAIL, which are the author's 12 plus my two Q2 checks.

## Findings

None at MINOR, MAJOR or BLOCKER. No RESIDUE: no added line in `hdl`, `tb`, `scripts` or `docs` shows a lane label, lane name, review round, reviewer ID or issue-comment ID. I checked this with a pattern search over every added line of `9d509029..409c3075`.

### S1: name the "Resp heard while disabled" refusal in a permanent check (SUGGESTION)

- **Lenses:** Tests.
- **Where:** `docs/HDL_DEVELOPER.md` says "`S_PDGOT` also refuses a new response arm", and the `prog_leg_noten` docstring in `hdl/ucode/gen_gptp_ucode.py:2197-2202` says the same. Phase 48 covers a response that arrives before the fall. No repository check names a Pdelay_Resp and its Follow_Up that both arrive after the fall.
- **Evidence:** my probe Q1 passes at head: 0 commits, delay unchanged. Its enabled control pairs. The behaviour is correct today. Only the named gate is absent, and the existing control "a portEnabled edge leaves the interval unanswered" would very likely fail Q1 as well.
- **Suggested outcome:** add Q1's shape (`scripts/probes.inc`, `probe_q1`) to phase 48 as a fourth ordering, with that control naming it.

### S2: check the cadence after a disabled-release rise (SUGGESTION)

- **Lenses:** Tests, Conformance.
- **Where:** phase 51 (`tb/verilator/engine/sim_main.cpp`, `end_a_retained_cease_at_the_first_rise`) checks only the first request after the rise, and the re-earn. Phase 44 also checks "then one request every interval".
- **Evidence:** my Q2 passes at head. The first request leaves 245 cycles after the rise, and the next four gaps are 999.978, 1000.000, 1000.000 and 1000.000 ms. Figure 11-8's pdelayIntervalTimer restarts at the send.
- **Suggested outcome:** have phase 51 also grade the following gaps, as phase 44 does.

### S3: carry the byte-face withdrawal exception into the parent adoption (SUGGESTION)

- **Lenses:** Robustness, Docs.
- **Where:** `docs/INTEGRATION.md:120-134` now states an exception to "Outputs remain stable while ready stays low": a disabled port's frame still waiting at its first byte is withdrawn, so valid falls with no transfer. This is how R730-F1 is fixed, and the manager's round-2 assignment frames it the same way.
- **Evidence:** at the companion base `e06ade31`, both parent consumers of the engine byte face count accepted bytes only. These are the shadow's gearbox (`KL_gptp_shadow.sv:789`, `tx_byte_w = eng_tx_valid_w & eng_tx_ready_w`) and `KL_gptp_txticket` (`:147`, `beat_w = tx_valid_i & tx_ready_i`; allocation on `beat_w & tx_eof_i`). So a withdrawn first byte leaves nothing behind. The round-2 companion patch says so in `KL_gptp_shadow.sv` and `docs/design/GPTP_PLANE.md`.
- **Suggested outcome:** record the exception where the adoption (milan-fpga #806) lists engine-face contract points, so any later consumer keeps acceptance-qualified framing. No change is needed at this head.

An optional wording note, not a defect: `docs/INTEGRATION.md:230` ("their replies are dropped") is still true in effect. "Withdrawn before their first byte" would match the new mechanism's word.

## Lens evidence

### Conformance: CLEAN

- **Authorities:** Milan v1.2 4.2.6.2.5 (cease exit on a portEnabled toggle) and 4.2.6.2.4 (2 to 5 exchanges). IEEE 802.1AS-2011 10.2.4.11 (portEnabled), 11.2.15.3 and Figure 11-8, with Cor1 and Cor2: NOT_ENABLED takes no Follow_Up, and INITIAL_SEND_PDELAY_REQ sends at once with lostResponses = 0 and asCapable = FALSE.
- **NOT_ENABLED at the fall:**
  - asCapable falls with a commit within 2 ms, including behind a stalled byte face (phases 49 and 50, and the R730 probe).
  - No exchange completes while the port is disabled: Follow_Up after the fall, t1 after the fall, Follow_Up queued before the fall (phase 48), and Resp plus Follow_Up both after the fall (my Q1).
  - No frame starts while the port is disabled (phase 49, Q5).
- **INITIAL_SEND_PDELAY_REQ at the rise:** one request at once, whatever the reset history (phase 51, probe D, Q2). Then one request every interval (Q2, and phase 44). asCapable takes two exchanges each time.
- **A one-cycle glitch inside a cease ends it:** my Q3 sends a request 358 cycles after the glitch; round-1 probes B1 and B3 agree.
- **Unchanged (round-1 accepted behaviour):**
  - The countdown exit: phase 47, and the parent check "the cease countdown exit is unchanged".
  - A warm reset inside a cease with the port enabled at release keeps the cease. That is not a toggle under 4.2.6.2.5. My Q4: 0 requests in 1.2 s after release, then the countdown exit.
  - With the port high at release, nothing is raised.
- **Not done, recorded in the PR (round 1, not a finding):** Cor2's `neighborRateRatio = 1.0` and the random sequenceId at INITIAL_SEND_PDELAY_REQ.

### RTL: CLEAN

- **`port_enable` block (`KL_gptp_engine.sv:1116-1132`):**
  - The reference-level edge detector is sound. The first post-release cycle samples without comparing; every later difference is an edge.
  - A fall withdraws an owed beat.
  - A fall and rise before NOTEN dispatches give one NOTEN and one beat, and `pop_w`'s `!pe_noten_r` keeps the beat behind it.
- **Dispatch:**
  - `pe_pop_w` (`:624`) and its dispatch arm (`:652-660`) enter the timer table's default entry 512 with slot 6, the same path as a queued slot-6 event.
  - `txts_pop_w` and `pop_w` both yield to `pe_noten_r` (`:625-629`), so no event after an edge runs before its leg.
  - Skipping `ser_idle` is safe: NOTEN runs `S_*` writes, then `PDBAD` (`gen_gptp_ucode.py:2159-2168`: S_PDOK, flags word, COMMIT, END). It does no lane write and no SEND.
- **Serializer (`KL_gptp_tx_slot.sv:117-158`):**
  - `ser_drop_w = cancel_i && ser_sof_r`. `ser_sof_r` implies `ser_run_r`.
  - The drop branch sits ahead of the ready branch, so a withdrawn frame never advances its address.
  - `tx_valid_o` is masked in the drop cycle, and `cancel_i` comes from the registered `port_en_r`, so there is no new combinational input-to-output path.
  - A SEND while disabled rises and is withdrawn the next cycle with valid masked throughout (Q5).
- **Claims:** both egress claims are cleared every cycle the port is disabled (`:1100-1103`), so a stamp that returns after the rise finds no claim (phase 48, ordering 1).
- **ROM:**
  - I regenerated the images: 1,022 words shipping and 1,023 seeded at head, 1,021 at base.
  - The tracked engine image is byte-identical to its regeneration.
- **Static gates at head (rc 0):** `make contract`, `make lint`, `make docs` (source evidence 20 exact), `make diagrams-check` and the ooc clock self-test (`receipts/head-static-gates.txt`).
- **Area:** the round-2 body's −64 LUTs, +4 FFs, −67 placed LUTs, −29 slices and WNS +0.506 ns match the author's place and synth reports (`author-r2/receipts/area/*`). I did not run Vivado (see limits).

### Robustness: CLEAN

- **Probed at head, all passing:**
  - A stall at the first byte, and after 1, 34 and 67 bytes (phases 49 and 50).
  - A rise during a stalled started frame: the frame completes whole, the request follows 340 cycles after ready returns, and nothing is torn (Q6).
  - A reply SEND issued while disabled with ready high (Q5).
  - A one-cycle glitch (Q3), and one- and three-cycle glitches (round-1 B1 and B3).
  - A disabled warm reset with no cease: no frame starts while disabled after release, the rise sends at once, and the cadence is correct (Q2).
  - The rise swept across the beat's expiry: 151 offsets, no double and no missing request (sweep C).
- **The parent boundary for the withdrawal:** source-verified (S3). The gearbox and the ticket take accepted bytes only, and a started frame completes into the frame FIFO.
- **Round-1 robustness verdicts on untouched code stand:** the frame built across the fall, and the count restart.

### Tests: CLEAN

- **Engine suite at head:** `2048 checks: 2048 PASS, 0 FAIL` ×3, and `60 checks: 60 PASS` (`receipts/head-engine-run.log`, rc 0).
- **Mutation arms, run here in full:**
  - My driver `scripts/par_arm.py` calls the arm's own `stage`, `build`, `generate_image`, `run_harness` and `run_mutant` unchanged; only the scheduling is concurrent.
  - Head: `136 checks: 136 PASS, 0 FAIL`. Base `f97c1803`: `113 checks: 113 PASS, 0 FAIL` (`receipts/arm-head.log`, `arm-base.log`, both rc 0).
  - My set of 135 caught mutant names at head is identical to the author's `repo-head-arm/01.log`.
  - All 22 controls that name a #94 check were caught on every check they name, under the arm's strict #94 rule.
- **Coverage:** the author's coverage receipt reports all 71 #94 checks failed by at least one control (`uncovered: []`, `not caught on named: []`). Each round-1 reviewer probe is now a permanent check (phases 48 to 51) with a named control.
- **Gaps:** none that leaves a lens unclean. S1 and S2 are suggestions for gates on behaviour that already holds.

### Docs: CLEAN

- **Accuracy:** the delta's text in `docs/INTEGRATION.md` (transmit exception, port-enable section), `docs/HDL_DEVELOPER.md`, `docs/TEST_DEVELOPER.md` (five lines) and the four new `docs/SOURCE_EVIDENCE.md` rows matches the RTL and microcode as I read them and probed them.
- **Round-1 docs findings:** the two lines R729-1 flagged (the boot cadence serving a first enable, and "commits nothing while disabled") are now true at head.
- **Anchors:** re-pointed; `make docs` reports 20 exact. The two evidence strings in `scripts/check_source_evidence.py` and `scripts/generate_diagrams.py` follow the new `tx_valid_o` line.
- **Source comments:** they state behaviour and reason with issue and clause IDs. There is no new instance under the comment rule.

## Parent companion (milan-fpga, lands with the adoption #806)

- **Patch:** the round-2 `author-r2/milan-fpga-companion.patch` (sha256 `aeeab9c8…34`) applies with `git apply --index` to `e06ade31` and moves `gptp-processor` to `409c3075`. I checked out that gitlink from this head (`receipts/integrity.txt`).
- **Legs, run here:**
  - `make -C tb/verilator/milan_dp gptp`: `205 checks: 205 PASS, 0 FAIL`, rc 0.
  - `gptp-lat`: `205 checks: 205 PASS, 0 FAIL`, rc 0 (`receipts/parent-milan_dp-gptp*.log`).
  - Base was 202/202 (author receipt), so the difference is the three new #94 checks.
- **From the author's receipts, verified by manifest only:** the full parent consumer list rc 0 on the snapshot (`parent-head-A`), the physical leg's Pdelay and verdict lines identical to base (`parent-head-B/head-pB-lines-vs-base.diff`, 0 bytes), and four parent controls caught (`parent-controls/results.json`).

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #94 acceptance and both manager assignments; Milan v1.2 4.2.6.2.4/4.2.6.2.5; 802.1AS-2011 10.2.4.11, 11.2.15.3, Figure 11-8 (Cor1/Cor2); NOTEN, PDRESP arm, PDPOST, PDBAD; phases 44-51; round-1 probes A, B1, B3, C, D; R730 probes; Q1-Q6 | R729-2 | 409c3075a6c5525d283de5a93584ad87a4528137 |
| RTL | CLEAN | `KL_gptp_engine.sv` (port_enable block, push arbitration, pe_pop/txts_pop/pop, dispatch arm, claim clear, cancel wiring); `KL_gptp_tx_slot.sv` (cancel_i, ser_drop_w); `gen_gptp_ucode.py` NOTEN and arm gates; four ROM images regenerated (1,022/1,023); contract, lint, docs, diagrams-check, ooc self-test; author area reports | R729-2 | 409c3075a6c5525d283de5a93584ad87a4528137 |
| Robustness | CLEAN | Stalls at byte 0, 1, 34, 67; a rise during a stalled frame (Q6); SEND while disabled (Q5); one-cycle glitch (Q3, B1, B3); disabled warm reset with and without a cease (D, Q2, phase 51); enabled warm reset in a cease (Q4); 151-offset rise sweep; parent gearbox and ticket qualification at `e06ade31` | R729-2 | 409c3075a6c5525d283de5a93584ad87a4528137 |
| Tests | CLEAN | Engine suite 2,048 ×3 + 60; head arm 136/136 and base arm 113/113, run here; 22 strict #94 controls; author coverage (71 checks, none uncovered); new checks at round-1 RTL (12 FAIL, reproduced); parent `milan_dp` gptp and gptp-lat 205/205, run here | R729-2 | 409c3075a6c5525d283de5a93584ad87a4528137 |
| Docs | CLEAN | `docs/INTEGRATION.md`, `docs/HDL_DEVELOPER.md`, `docs/TEST_DEVELOPER.md`, `docs/SOURCE_EVIDENCE.md`, evidence strings in two scripts, source comments of the delta (comment-rule search), round-2 PR body in the packet, companion `GPTP_PLANE.md` | R729-2 | 409c3075a6c5525d283de5a93584ad87a4528137 |

## Real limits

- **No manager source bank at this head.** Source-head execution evidence is the author's published receipts plus the focused runs listed here. I neither claim nor infer a manager source bank.
- **Packet integrity, not signature:** the evidence commit `4c00cace` is unsigned. All 535 `MANIFEST.json` entries match their published sha256 (`receipts/evidence-verification.txt`).
- **Area:** I ran no Vivado or ooc build, so the area and timing figures are the author's reports, checked against the round-2 body.
- **Parent:**
  - I ran only the `milan_dp` `gptp` and `gptp-lat` legs, on a local snapshot (`e06ade31` plus the round-2 patch, gitlink `409c3075`).
  - The full parent consumer list, `milan_dp_gptp`, the parent controls and the extra suites rest on the author's receipts.
  - This snapshot is not the manager's current-dev merge candidate.
- **The mutation arms ran with a concurrent driver.** Each mutant builds with one compile job instead of four. Verdict logic and harness are the arm's own.
- **Probes use the engine harness's own peer and stamp models.** Its egress-stamp return is idealised.
- **Hosted:** at this head there are 0 check-runs and 0 workflow runs, and the combined status is pending with 0 contexts. I claim nothing hosted.
- **Hardware:** physical calibration NOT RUN. I touched no hardware. The in-house link-toggle scenario the issue promises has not been posted, and field skips are not hardware proof.

## Pending manager duties

- **PR body, before merge:**
  - The live PR #95 description (sha256 `f9d3f3b6…`) is the round-1 text. It is byte-identical to `author/PR-BODY.md` and states round-1 figures: 2,002 checks, a 128/128 arm, ROM "1,021 shipping … as on main", area −68/−4.
  - The round-2 body `author-r2/PR-BODY.md` (sha256 `59dd4bc5…`) carries the figures I verified at this head: 2,048 checks, arms 113/113 and 136/136, ROM 1,022/1,023, area −64/+4/−67/−29.
  - Publish it in place of the live body. I raise this as a publication step, not a finding against the head: the head's source, docs and the author's round-2 text are correct.
- **Merge candidate:** build and validate the current-dev merge candidate (source base `f97c1803`, live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`) with the builder and native banks, and link the receipts on the PR.
- **Hosted acceptance:** hosted and act acceptance.
- **Adoption (#806):** the parent area re-measure (route-1x1, ooc-1x1, ooc-8x8), the link-toggle scenario on the built image, and S3.
- **Other reviewer:** R730's own findings need its own re-review. Its round-1 probes pass at this head, `cmp`-identical to the author's receipt.

## Receipts and scripts

All files are listed in `MANIFEST.sha256`, with host paths replaced by placeholders. The scripts:

- `scripts/par_arm.py`: the concurrent mutation-arm driver.
- `scripts/probes.inc` and `scripts/run_probes.sh`: my Q1-Q6 probes, run as `JOBS=2 run_probes.sh <harness-tree> <rtl-tree> <outdir>`.
- `scripts/r729-1/`: the round-1 probe scripts, unchanged.
- `scripts/r730-1/`: the R730 round-1 probe script, with only its pinned `HEAD` constant moved to `409c3075`.

The tracked bytes, modes and index of the review clone match `b552de22` after every run, and the tree has no gitlinks (`receipts/integrity.txt`).

R729-2 FINISHED
