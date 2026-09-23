[R258] NEGATIVE - exact head cbccf226068c107fb30764891c98b8d70c54d775

# R258-2: independent review of FPGA-gPTP #68 / PR #74, correction round

| Item | Value |
|---|---|
| Reviewer | R258, internal cleared-context review, round R258-2 |
| Head | `cbccf226068c107fb30764891c98b8d70c54d775`, tree `e8b9fa23fe5e1d5e3bd3ab1dd3c09196760a5063` (verified, `receipts/01-clone-before.log`, `receipts/90-clone-integrity-after.log`) |
| Source base | `c1b617435824929a790739ea8585c3fe1a328cc0` (the parent's current `gptp-processor` pin) |
| Parent used for consumer runs | kebag-logic/milan-fpga live dev `ede8d48ecd7c7f589a14b957951f040d92c99c70` |
| Simulator | Verilator 5.050 through the pinned wrapper, sha256 `905795b9...e92f`, `verilator_bin` `44898b22...bfdd`; the host default 5.052 was not used (`receipts/00-tool-identity.log`) |
| Verdict | NEGATIVE: one MAJOR (F1), one MINOR (F2), one SUGGESTION (S1). Every prior BLOCKER, MAJOR and SUGGESTION from R258-1 and R259-1 is RESOLVED at this head |

The correction does what the two BLOCKERs asked. The whole written trim is clamped to exactly the parent's `PHC_ADJ_MAX_C` at every clock tried, and a locked slew riding that clamp in the parent's own bench keeps asCapable with zero refusals. The parent suites are green at live dev. The 20 us / 100 us thresholds, the exact-threshold-slews boundary and one step pulse per step are encoded exactly. What stays open is the reading the author flagged. The Sync receipt timeout and a return from mastership re-arm the link-up threshold. As a result a grandmaster failover that reaches the plane as a Sync lapse is treated as a link-up (a 50 us failover pair steps), while the owner's decision says a grandmaster change stays locked (50 us slews). That needs an owner ruling, and the guide, tests and PR body have to follow it (F1).

## Reconstruction

Read in this order, from public state only:

1. The donor has no `AGENTS.md` or `CONTRIBUTING.md`, so I read the parent's at live dev `ede8d48e`, plus Rule 1 of its code-quality guide. Then the donor `README.md`, `docs/README.md`, `MANAGER.md`, `HDL_DEVELOPER.md`, `TEST_DEVELOPER.md` and `SOURCE_EVIDENCE.md`.
2. Issue #68: the body (frozen acceptance) and all eight comments. These are the manager's two assignments, the first author's TAKEN, DECISION (5790066720) and REVIEW READY, the OWNER DECISION of 2026-09-23 (5794731372), and the correction author's TAKEN and REVIEW READY. The owner decision is mirrored byte-identically on kebag-logic/milan-fpga#387 as 5794731090.
3. Parent #387: the body and decision 5606198212 (part a superseded, part b unchanged). Parent `REQUIREMENTS.md` REQ-PTP-01, 05, 07, 08 and 09.
4. Interface authorities.
   - Donor: `docs/INTEGRATION.md`, `hdl/top/KL_gptp_engine.sv` (the PHC face, the publish-flags reset, the region map), and `hdl/ucpu/KL_gptp_ucpu.sv` (ALU, CMP, MULS and DIVU operand semantics).
   - Parent: `KL_gptp_txret.sv` (`PHC_ADJ_MAX_C` at :303-305, the eligibility test at :434-436), `KL_gptp_shadow.sv` (:139-146, :743-744, :985), and `sw/builder/endstation_builder.py` (what it parses from the generator).
5. `git diff c1b61743..cbccf226` (10 files) and both commits. Each commit message is one line with no trailers.
6. Public executable evidence.
   - milan-fpga `9c9922c4`, `review-evidence/gptp68-r1/`: `correction-a199/` (the author packet) and `manager-r1/`.
   - `manager-r2/` at `a45e04a1`, the commit the manager's PR comment links. `9c9922c4` is its parent and does not contain it.
   - The PR #74 body and the manager's PR comments.
7. The prior review reports, R258-1 (PR comment 5791184500) and R259-1 (5791704438). I read these only after this round's own pass over the diff, its runs and F1 were complete.

## Findings

### F1 MAJOR: the flagged link-up reading turns a grandmaster failover into a link-up, against "once locked, including after a grandmaster change"; it is unratified, and its main consequence is stated nowhere

- **Severity:** MAJOR.
- **Lenses:** Conformance, Tests, Docs.
- **Locations:**
  - `hdl/ucode/gen_gptp_ucode.py:1843` (SRTO writes `S_LOCK = 0`), `:1618` (BECOME writes `S_LOCK = 0`), `:1809-1815` (the asCapable rise writes `S_LOCK = 0`), `:1564-1577` (a grandmaster change leaves `S_LOCK`).
  - `docs/INTEGRATION.md:204-228`.
  - `tb/verilator/engine/sim_main.cpp:622-630` (the mirror's link-up definition), `:2990-3020` (phase 13 makes every link-up through a receipt timeout), `:3393-3418` (phase 21 expects a link-up after mastership).
  - The PR #74 body, section "Reading, flagged for the reviewers".

**Authority.** The owner decision (5794731372) reads: "the gPTP servo steps the PHC at link-up (the first synchronization after asCapable) when the offset exceeds 20 us; once locked, including after a grandmaster change, it slews offsets up to 100 us and steps above 100 us". Its basis includes that "the device stays aligned with third-party peers after a real grandmaster time jump". Parent `AGENTS.md` section 2: when a decision and the implementation conflict, the conflict is published and decided; neither side chooses an interpretation privately.

**Evidence.**

- **Three re-arms where the decision names one.** The owner defines link-up as the first synchronization after asCapable. The head re-arms the link-up threshold on three events: the asCapable rise, the 375 ms Sync receipt timeout, and this plane becoming grandmaster. A grandmaster identity change leaves the lock alone. So "locked after a grandmaster change" holds only when the new grandmaster's Syncs arrive without a lapse of 375 ms or more.
- **A failover usually has such a lapse.** When the old grandmaster falls silent, its Syncs stop. The receipt timeout (`:1838-1846`) then fires before any new grandmaster's Sync can be consumed, because the silence is detected only by timeouts upstream as well. Past 3 s the Announce watch also makes this plane grandmaster (`:1591-1600`), which is a second re-arm. So at this head two kinds of change stay locked: a better grandmaster taking over while Syncs keep flowing, and a hand-over that restores Syncs within 375 ms, such as an adjacent bridge re-selecting at once on a link drop. A failover through silence is a link-up.
- **Measured** (`receipts/40-probe-failover-head.log`, `scripts/probe_failover.py`). The probe inserts one phase after 18c, identical to 18c except for a Sync lapse. Sync-ok falls at the receipt timeout. Identity `00D0D0FFFE00000D` is adopted through the same parent. A pair 50 us off then produces **one step pulse of -50000 ns**. The same 50 us pair after 18c's grandmaster change without a lapse slews.
  - **Control:** the same binary with an image whose SRTO and BECOME `S_LOCK` writes are removed, so the link-up re-arms on an asCapable rise only. This image has 994 words, so it fits. The failover pair then slews (0 step pulses), and the only checks that fail are the 23 that encode the author's reading (phases 13 and 21, plus the mirror checks that follow them).
- **Product consequence.** In the parent each step is one counted media re-base (`tu`, one `mr` toggle, one MEDIA_RESET, #387 decision b). The reading therefore adds a counted media event to every such failover whose offset lies between 20 and 100 us, where the decision text says to slew.
- **Docs.** `INTEGRATION.md:218-226` says a grandmaster identity change "leaves the servo locked. So the next pair uses the 100 us threshold." In a failover through silence the timeout has already unlocked the servo and the next pair uses 20 us. The link-up list (`:206-210`) names the timeout but never says that failovers go through it.
- **Tests.** The oracle encodes the contested reading, and no test pins the failover case. The mirror's link-up definition includes the receipt timeout and mastership (`sim_main.cpp:622-630`), and phases 13 and 21 manufacture link-ups through them.
- **PR body.**
  - It says "The manager's assignment defines link-up as the pair that raises the sync verdict". No manager or owner comment on #68, PR #74 or #387 says this. The only public source of that definition is the first author's DECISION (5790066720), which the owner then re-decided.
  - "If only an asCapable rise was meant, delete the one `S_LOCK` write in the SRTO leg" is incomplete. BECOME writes it too (`:1618`), and the PR's own matrix row "a receipt timeout keeps the lock" shows 0 failures under "T1 after become". The mastership re-arm survives that deletion.
- **The case for the reading.** It carries forward the verdict-raising definition that R258-1 and R259-1 accepted under the 2026-09-09 rule, minus the owner's explicit grandmaster exception. A servo that has missed Syncs for 375 ms is arguably no longer locked. Both readings are safe and bounded: one counted step, or a slew of at most 100 us. Choosing between them is the owner's decision, not the author's or a reviewer's.

**Impact.** For a failover through silence, which is the ordinary way a grandmaster disappears, product behavior differs from the decision text. The guide implies the opposite, so integrators and #387 would plan media re-base behavior from a wrong premise.

**Required outcome.** A public owner ruling on #68, mirrored to #387, that explicitly covers two cases: (i) a grandmaster failover through a Sync receipt timeout, and (ii) the first pair after this plane was grandmaster. The head then matches the ruling.

- **If the reading is accepted:**
  - `INTEGRATION.md` states that a grandmaster change reached through a receipt timeout, or through this plane's mastership, is a link-up (20 us), and limits the "Locked" text to a change without a lapse.
  - An engine test pins the failover case, for example the failover +50 us pair steps once.
  - The PR body's attribution and narrowing instruction are corrected.
- **If only an asCapable rise re-arms:**
  - Both the SRTO and the BECOME `S_LOCK` writes go. The scratch-map invariant stays true, because the rise remains the single re-arm.
  - The phases that create link-ups through a receipt timeout or mastership are re-scripted around asCapable rises.
  - A test pins the failover +50 us pair slewing.
  - The two mutants for the removed writes are replaced by mutants that re-add them.

**Verification.**

- `scripts/probe_failover.py` on the fixed head gives the step count the ruling names.
- The engine suite passes on all three images, and its mutation arm catches every mutant.
- `make docs` passes.
- The ruling is linked from the PR body.

### F2 MINOR: the PR title still states the retired rule

- **Severity:** MINOR.
- **Lenses:** Docs.
- **Artifact:** PR #74 title "Step the PHC only on a first synchronization over one second", read at this head.

**Evidence.** The commit subject and the body's first line state the implemented policy ("Step over 20 us at link-up and over 100 us once locked, and clamp the whole trim to 200 ppm"). The title still describes the rule the owner superseded. Merge subjects in this repository summarise the PR (`c1b6174`, `382ebaf`).

**Impact.** The PR list, and a merge subject derived from the title, would record a policy the plane does not implement.

**Required outcome.** Retitle the PR to the implemented policy before merge. This is manager-owned metadata.

**Verification.** `gh pr view 74 --json title`.

### S1 SUGGESTION: the rate envelope section gives the slew's lower bound only

- **Severity:** SUGGESTION.
- **Lenses:** Docs, Robustness.
- **Location:** `docs/INTEGRATION.md:230-256`.

**Evidence.** The guide correctly says "A 100 us slew needs at least 0.5 s". The owner decision's basis says "100 us settles in at most 0.5 s", which does not hold once the master's own rate uses part of the ±200 ppm authority. A reviewer model of the documented rule in exact integers (`scripts/servo_envelope_model.py`, `receipts/20-23`) gives:

- **Settling:** 1.0 to 2.6 s against a ±140 ppm master, and up to about 99 s when the master sits at ±199 ppm and the jump needs the scarce headroom.
- **Overshoot:** up to 42.5 us, because the integrator keeps integrating while the whole trim sits on the clamp. The parent probe shows +25 us at its sixth pair.
- **No self-inflicted later step** anywhere inside ±199 ppm, at 2, 100 and 125 MHz.
- **A master whose relative rate lies outside ±200 ppm is stepped periodically:** about every 100 s at +201 ppm, 10 s at +210 ppm and 2 s at +250 ppm. Each step is a counted re-base in the parent.

Stating these three behaviours, and telling the owner the 0.5 s figure is a floor, would let #387 size its re-base handling. Conditional integration while the trim is clamped would cut the overshoot; that is optional. This has no effect on coverage.

## Focus items verified at this head

**The policy and the clamp, exactly.**

| Owner rule | Implementation | Evidence |
|---|---|---|
| Link-up steps above 20 us, exactly 20 us slews | T = 20000 + `S_LOCK`. The pair steps iff (offset + T) u/ (2T + 1) is nonzero. The DIVU is u64/u32 with the register divisor 2T + 1 ≤ 200001, and the quotient is tested against zero with a full 64-bit CMP (`gen:810-817`; `KL_gptp_ucpu.sv:193-203`, `:616-639`) | Phase 13: ±15, ±25, ±20 and ±(20 us + 1 ns). Suite mutant "exactly the threshold steps" and reviewer mutant RM4 (link-up threshold 1 ns wider) are caught (`receipts/30`, `receipts/33`) |
| Locked slews up to 100 us and steps above | Every consumed pair writes `S_LOCK = 80000` (`gen:847-848`) | Phase 13b: ±90, ±110, ±100 and ±(100 us + 1 ns). Reviewer mutant RM3 (locked threshold 1 ns wider) is caught |
| Locked includes after a grandmaster change | A grandmaster change leaves `S_LOCK` (`gen:1564-1577`) | Phase 18c, which has no lapse; failovers are F1 |
| Link-up is the first synchronization after asCapable | The PDPAIR rise writes `S_LOCK = 0` (`gen:1809-1815`); SRTO and BECOME do too (F1) | Phases 21 and 28b. Reviewer mutant RM1 (every good verdict re-arms) is caught |
| Every step is one pulse | The step arm writes adjtime `-offset`, then one addend with the bare integrator (`gen:818-823`); `expect_policy_pair` counts both pulses and orders them (`sim_main.cpp:845-886`) | Reviewer mutants RM6 (+offset) and RM7 (PI trim on a step) are caught |
| The whole trim (P + I) is clamped to the parent's ±200 ppm envelope | `e_sat` clamps the integrator (`gen:831`) and then the whole trim on both arms (`gen:839`). The limit is `ppm_addend(200, clk)` (`gen:425-445`), the parent's `PHC_ADJ_MAX_C` expression in exact integers | Both clamp immediates equal `PHC_ADJ_MAX_C` at 1, 2, 25, 50, 100, 125, 156.25 and 200 MHz (`receipts/13`). Phases 15b and 34. Suite mutants "whole trim not clamped" and "one unit wider" are caught, as are reviewer mutants RM2 (sign pick) and RM5 (integrator one unit wider) |

The consumer accepts |adj| ≤ `PHC_ADJ_MAX_C`, inclusive (`KL_gptp_txret.sv:434-436`). A trim sitting exactly on the rail is therefore accepted: the parent probe puts 4 pairs on it with 0 refusals. Because `e_sat` also runs on the step arm, a stale or uninitialised integrator can never be written outside the envelope.

**The `S_LOCK` written-before-read invariant.** It holds.

- **One asCapable setter.** The raw write at `gen:1812` is the only writer of flags word 2 that ORs in asCapable. The other writers are the `e_flags` calls at `:849`, `:1567`, `:1617`, `:1819` and `:1842`, and none of them sets bit 2.
- **The verdict word resets.** `pub_flags_r` is reset (`KL_gptp_engine.sv:775`).
- **The bench battery cannot touch it.** The battery at 704 writes scratch 0 to 11 only.
- **Mutation evidence.** The warm-reset phase 28b and the mutant "asCapable's rise keeps the lock" are both caught.

**ROM.**

- **Byte identity.** All four tracked images regenerate byte-identical, and their digests equal the PR table (`receipts/10`).
- **Size.** 996 of 1024 words are real (997 in the seeded images).
- **Only four legs change content.** I placed every base-generator program at the head's addresses and compared word for word. Only BECOME, PDPAIR, SRTO and SERVO change content; every other program only relocates, at 2, 25, 50, 100 and 125 MHz and in both seeded images. Every unowned word is the address filler (`receipts/12`, `receipts/11`).

**Engine tests and mutants.**

- **The suite.** 1207 of 1207 checks pass on each of the three images. The suite's own arm is 27 of 27: the control passes and all 26 mutants are caught (`receipts/30`).
- **The head harness rejects both earlier policies** (`receipts/32`). The base image fails 61 checks: locked, grandmaster change, long slew and envelope. The reviewed image fails 84, including 26 addend pulses outside the envelope.
- **Reviewer mutants.** Seven of my own, RM1 to RM7, are all caught (`receipts/33`).
- **Gates.** `make contract` and `make docs` pass (`receipts/31`).

**Parent impact.** No parent failure remains at this head.

- **`gptp_plane`** at live dev: the head gives 29/29, the base 29/29, and the reviewed control 24/29, which shows the suite discriminates (`receipts/50-52`).
- **`gptp_shadow` `run`** at live dev: the head gives 309/309 (`receipts/53`).
- **The author's +90 us locked-slew probe**, in `gptp_shadow` with the real `KL_gptp_txret`, gives 120 pairs (`receipts/54-55`):
  - the largest |adj| is 1677722, exactly the envelope;
  - 4 pairs sit on it and none beyond;
  - flags stay 13 throughout;
  - 0 PHC-history refusals, 0 lost results.
- **The manager's r2 receipts** pass for the C++ and Python idiom gates, `xvlog_gate --check`, the RTL source lists, the builder and `gptp_shadow` including its mutation arm. The builder's gate 11 is a SKIP (no hardware report on disk), not a pass.

## Prior public review findings, resolved or retained at this head

| Finding | Status at `cbccf226` | Evidence |
|---|---|---|
| R258-1 F1 BLOCKER, the ~320 ppm held slew beyond the consumer envelope, which wedged the plane | RESOLVED | The whole trim and the integrator are clamped to exactly `PHC_ADJ_MAX_C` (`gen:831`, `:839`; `receipts/13`). Slews are bounded to 100 us. The guide states the bound and the held trim (`INTEGRATION.md:230-256`). A donor test drives a slew longer than allowedLostResponses + 1 Pdelay intervals: phase 15b, 48 and 40 pairs, with asCapable held and more than 4 exchanges. That test and the envelope sweep fail on the reviewed image (`receipts/32`). The out-of-envelope mutants are caught. The parent probe with the real `txret` keeps asCapable and loses nothing (`receipts/54-55`) |
| R258-1 F2 MAJOR, the parent suites were not green at the pin | RESOLVED | `gptp_plane` 29/29 and `gptp_shadow` 309/309 at live dev `ede8d48e` with this head (`receipts/50`, `receipts/53`); manager r2 consumer gates PASS. Re-recording the parent ROM digests belongs to the #387 pin bump (pending below) |
| R258-1 S1 SUGGESTION, the `e_sat` docstring overstated its domain | RESOLVED | `gen:707-716` states the exact domain and why both callers stay inside it. The emitted words were checked against that domain |
| R259-1 F1 BLOCKER, the same defect, measured separately | RESOLVED | As R258-1 F1. R259-1's verification asked for "a test failing on the old head for this mechanism"; `receipts/32` shows it |
| R259-1's retention of R258-1 F2 and S1 | RESOLVED | As above |
| R259-1 SUGGESTION, "becoming grandmaster clears the verdict" was unguarded | RESOLVED | `sim_main.cpp:3373`; mutant "becoming grandmaster keeps sync-ok" caught (`receipts/30`) |
| R259-1 SUGGESTION, document bit 3 and `pub_offset_o` during a slew | RESOLVED | `INTEGRATION.md:258-274` |

## Clean-result evidence per lens

```text
[R258] PASS RTL - hdl/ucode/gen_gptp_ucode.py:707-852, :1785-1846, :1603-1631 with hdl/ucpu/KL_gptp_ucpu.sv:185-236, :610-640 and hdl/top/KL_gptp_engine.sv:767-921 - operand widths, signedness and truncation of every new instruction (u64/u32 DIVU with a register or 24-bit immediate divisor, 64-bit zero compare, 32x32 MULS on |offset| <= 100000, 24-bit immediates asserted, the addend's low 32 bits of a value inside +-PHC_ADJ_MAX_C), register clobbers of e_sat, step-before-addend order, the lock cell's write-before-read invariant, and the ROM packing (receipts/10-13); no RTL file changes; the servo's added serial arithmetic reads scratch only and stays within existing handler latency, so the two-bank lifetime (KL_gptp_engine.sv:176-183) is not narrowed for its own event
[R258] PASS Robustness - engine phases 13, 13b, 15b, 18c, 19, 21, 28b, 34 with receipts/20-23, 40, 54-55 - warm reset during a lock, the Sync receipt timeout, asCapable fall and return, mastership and re-adoption, +-T and +-(T + 1 ns) at both thresholds, both envelope rails, a stale integrator on the step arm (clamped), master rates to +-199 ppm without a self-inflicted step, masters outside the envelope (bounded periodic steps, S1), and the real parent consumer through a rail-riding slew with no refusal or loss
```

F1 is not filed under Robustness. Under both readings the failover path is deterministic and bounded: either one counted step pulse, or a slew of at most 100 us that stays inside the envelope. The open question is which of the two the decision requires.

Verified inside the unclean lenses (these stand, but clear nothing while F1 or F2 is open):

- **Conformance.** Every owner rule other than the failover case is met exactly. The acceptance to "keep the parent suites green at the resulting pin" is met at live dev. The issue scope items (the guide, the policy in the microcode, and engine tests that fail when their rule is removed) are present.
- **Tests.** Everything under "Engine tests and mutants" above.
- **Docs.**
  - The guide's pulse semantics, thresholds, rate-envelope expression, held trim and publication-during-slew text match the code.
  - `SOURCE_EVIDENCE.md` and `TEST_DEVELOPER.md` are accurate.
  - The generator docstrings (`:15-27`, `:164`, `:707-716`, `:799-801`, `:1785-1790`, `:1838-1840`) are accurate.
  - No added line carries U+2014 or non-ASCII.
  - The docs gate passes.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #68 body and all comments; owner decision 5794731372 (= #387 5794731090); #387 decision b; REQ-PTP-01/05/08/09; `gen_gptp_ucode.py:333-342, 402-445, 707-852, 1564-1631, 1785-1846`; parent `KL_gptp_txret.sv:115-128, 303-305, 434-436`; failover probe and control (`receipts/40`); parent runs (`receipts/50-55`) | R258-2 | `cbccf226068c107fb30764891c98b8d70c54d775` |
| RTL | CLEAN | `KL_gptp_ucpu.sv:185-236, 610-640`; `KL_gptp_engine.sv:176-183, 767-921`; `gen_gptp_ucode.py:707-852, 1478-1495, 1603-1631, 1785-1846, 1976-2050`; `receipts/10-13` | R258-2 | `cbccf226068c107fb30764891c98b8d70c54d775` |
| Robustness | CLEAN | Engine phases 13, 13b, 15b, 18c, 19, 21, 28b, 34; `receipts/20-23` (models at 2, 100 and 125 MHz), `receipts/33`, `receipts/40`, `receipts/54-55` | R258-2 | `cbccf226068c107fb30764891c98b8d70c54d775` |
| Tests | UNCLEAN (F1) | `tb/verilator/engine/sim_main.cpp` diff (mirror `:622-712`, `expect_policy_pair` `:845-886`, phases 10 to 34), `tb/verilator/engine/mutants.py:180-245`; `receipts/30`, `receipts/32`, `receipts/33`, `receipts/40` | R258-2 | `cbccf226068c107fb30764891c98b8d70c54d775` |
| Docs | UNCLEAN (F1, F2) | `docs/INTEGRATION.md:148-274, 314-330`; `docs/SOURCE_EVIDENCE.md:29-30`; `docs/TEST_DEVELOPER.md:99-100`; generator docstrings; PR #74 title and body; `receipts/31` | R258-2 | `cbccf226068c107fb30764891c98b8d70c54d775` |

## Real limits

- **No hardware, synthesis or physical calibration.** Physical calibration is NOT RUN, and field skips are not hardware proof. The product clock is covered by analysis (the ROM decode at eight clocks and models at 100 and 125 MHz), not by simulation. The engine and parent benches run at 2 MHz.
- **Hosted evidence.** The donor repository has no workflows. At this head there are 0 check runs, 0 statuses and 0 workflow runs (`receipts/60`), so no hosted job was executed or skipped.
- **Parent runs used fetched files, not a checkout.** Only the files each suite reads were fetched from live dev `ede8d48e`, each checked against its tree's blob id. `gptp-processor` was an export of the donor revision, not a registered gitlink, and verilog-axis `axis_fifo.v` came from its pin `48ff7a7e`. I ran only the `gptp_plane` and `gptp_shadow` `run` targets. The parent mutation arms, the builder and the idiom, xvlog and source-list gates are the manager's r2 receipts, not re-run here. `milan_dp` (the gPTP-ON leg), `clkvalid` and `media_grid_align` were run by nobody in this round.
- **The parent probe exits after its loop.** It shows the trim, flags and refusals through a slew. It does not grade `gptp_shadow`'s reconstruction law under that slew; the author's continue probe reports 308/309 for that bench shape.
- **Donor suites I did not re-run:** ucpu, parser, gaskets, tsngen, bench and lint, and the gaskets and tsngen mutation arms. The manager's full donor `make -j8` at this head covers them (exit 0; 768, 268, 81, 288 and 5 checks).
- **What the models are.** The servo figures in S1 and `receipts/20-23` come from a reviewer model of the documented rule with an idealised plant, not from RTL. The RTL points they overlap (±140 ppm, ±90 us) agree with the suite and the parent probe.
- **Deviations, disclosed.**
  - The suites' own Makefiles and `mutants.py` pass Verilator `--build -j 0`. The engine run, its mutation arm and the three `gptp_plane` runs therefore compiled on all 16 host cores for short periods, above the 8-job limit. Later runs were capped at 8 CPUs.
  - The suite's own mutation arm staged its temporary tree in the system temporary directory, outside the packet scratch. It removed itself, and I verified it gone.
  - No run touched the review clone, which is at the exact head bytes, modes and index with no gitlinks (`receipts/90`).
- **Path placeholders.** Home and storage path prefixes in the receipts are replaced by `$HOME` and `$DATA`; the receipts are otherwise raw.

## Pending manager duties

- **F1:** obtain and record the owner's ruling on #68 and #387, covering the failover through a receipt timeout and the return from mastership, then route the resulting correction.
- **F2:** retitle PR #74 before merge.
- **Parent adoption (#387):**
  - Re-record the parent's per-configuration ROM digests at the pin bump.
  - Consider a 20 to 100 us case, because phase 4 of `gptp_plane` and `gptp_shadow` no longer tells the two thresholds apart.
  - Re-derive the `gptp_shadow` reconstruction-law tolerance if a slew case is added to that bench.
  - Run the `milan_dp` gPTP-ON leg and `gptp_plane` in the consumer gate set; `gptp_plane` is outside the r2 list.
- **Merge turn:** build and gate the final current-dev candidate (source base `c1b61743`, live dev `ede8d48e` or later). Own hosted and act acceptance.
- **Review:** a second independent positive review (R259-2) is still required.

## Receipts and reproduction

Every publishable file is listed in `MANIFEST.sha256`. Put the pinned wrapper directory first on `PATH`. Scripts take explicit arguments.

- **ROM:**
  - `scripts/rom_regen_check.sh <clone> <out>`
  - `scripts/rom_leg_differential.py <base gen> <head gen> <clk> [--cease-ms N --seq-seed N --sync-seq-seed N]`
  - `scripts/rom_clamp_decode.py <gen> <clk>...`
- **Engine:**
  - `scripts/run_engine_focus.sh <clone> <rev> <work> <receipt> both`
  - `scripts/reviewer_mutants.py <head gen> <built harness> <work>`
  - `scripts/probe_failover.py <exported tree>` (a copy's `sim_main.cpp` only)
- **Models:** `scripts/servo_envelope_model.py <clk>`
- **Parent:**
  - `scripts/parent_gptp_plane.sh <clone> <rev> <parent rev> <work> <receipt>`
  - `scripts/parent_gptp_shadow_probe.sh <clone> <rev> <parent rev> <work> <receipt> [patch]`, with the author's public `probe-locked-slew-plus90us.patch` copied as `scripts/probe-locked-slew-plus90us.author.patch`
- **Integrity:** `scripts/clone_integrity.sh <clone> <commit> <tree>`

R258-2 FINISHED
