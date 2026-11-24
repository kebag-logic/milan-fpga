[R915] NEGATIVE - exact head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21

# R915-2: internal cleared-context delta re-review of PR #995 (Closes #994)

Head `f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21`, tree `90eef089759111d73b0316ded772250ee95a9735`, base `dev-soft-core` (train head `300da99b`). This round covers the delta from the round-1 head `bbfdb674`: the merge `3a8bdbf0` and the commits `d616b1c6` and `f97e49fe`.

## Verdict in one paragraph

The round-1 MAJOR is fixed at its cause. `tb/verilator/gptp_shadow` now runs three new phases through the slice's transport and the real `timestamp_counter`. They pass at the head, 408/408. With the gitlink at `1616fc8f` (my round-1 control) they fail 16 named checks. With each donor defect restored alone, every assertion the campaign and the PR name fails. The two new campaign controls are armed, and each is caught by its named check. #997 exists and is linked. Images, gitlinks and the ROM are byte-identical to round 1.

One new MINOR keeps the verdict NEGATIVE. Phase 20 claims the first master Announce leaves "only with transmit credit". It cannot fail when the Announce leg ignores the credit, because it withholds credit only through the seal, and the seal's departure fence enforces the same wire behaviour (F1). Three wording residues and five suggestions follow.

## Reconstruction

- **Contract.** AGENTS.md, CONTRIBUTING.md and docs/README were read as before. #994's frozen body has acceptance 1 to 3 (every pin site names `1213ac5b`; the consumer suites and the milan_dp gptp/gptp-lat legs pass; both routes fit at the #818 floor). It has no comments. #818: the best of three directives, or a single route marked as the shipping selection, meets WNS >= +0.030 ns and WHS >= 0 at every corner. Also read: `docs/integration/BUILDING.md:620-627, 772-778`.
- **Delta** (`receipts/published/images-unchanged.txt` lists the paths):
  - `3a8bdbf0` merges `2509db68`. That commit's tree `3b1a7562` equals `300da99b`'s. `git merge-tree --write-tree bbfdb674 2509db68` gives `eb8282df`, which is `3a8bdbf0`'s tree and `bbfdb674`'s. The merge changes no file.
  - `bbfdb674..f97e49fe` touches eight paths. Five are in `tb/verilator/gptp_shadow` (sim_main.cpp, gptp_shadow_wrap.sv, mutants.py, test_mutant_lifecycle.py, README.md). Three are Markdown: CHANGELOG.md, docs/guides/gptp/TEST_DEVELOPER.md, docs/reference/SUBMODULES.md.
- **Evidence packet.** `review-evidence/gptppin-r1` at `2fcbd468` has 245 MANIFEST.json entries. All 245 published hashes match, none is missing and none is unlisted (`receipts/published/evidence-manifest-verify.txt`). Nine entries are path-redacted, with rewritten hashes declared. The archive commit is not cryptographically signed. Its integrity rests on the manifest hashes. The author-r2 receipts, REVIEW-READY.md and PR-BODY.md were read by section.
- **Toolchain.** Scoped Verilator 5.050 (`--version`: `Verilator 5.050 2026-07-01 rev v5.050`), `MAKEFLAGS=--no-print-directory`. Every probe ran in a disposable shared clone at the head (`scripts/probe_setup.py`), on a host at load 160 to 207 on 32 CPUs.

## Executions (all mine, at f97e49fe; raw logs in `receipts/published/`)

| Case (`make -C tb/verilator/gptp_shadow run`) | Edit (diff in `probe-diffs/`) | Result |
|---|---|---|
| `head` control | none | 408 checks: 408 PASS, 0 FAIL, rc 0 |
| `oldpin` (my round-1 control) | `gptp-processor` checked out at `1616fc8f` | 391 PASS, 16 FAIL of 407, rc 2. It fails every #107 rate, counter-advance and TLV check in all four arms, plus the #106 at-once, race and both credit checks |
| `p106-beat` (old 2 ms first-Announce arm, END at SELF) | generator: `prog_self` ends in END; `prog_become` arms `RG_TMR\|3` with 2 ms | 403 PASS, 4 FAIL of 407, rc 2: "#106: the first master Announce leaves at once", "#106 race: one master Announce reaches the lane before the re-election", "#106 credit: two master Announces once the credit returns", "#106 credit: the withheld Announce leaves 1 s after the instant". The first Announce ends 4,184 clocks after the instant (285 at the head), and the withheld one 2,004,099 clocks after (2,000,103 at the head) |
| `p107-gate` (word 3 applied only during a slew) | engine: `if (phc_slew_active_o)` around the word-3 addend write | 404 PASS, 4 FAIL of 408, rc 2: "#107 settled +100 ppm: the mastership's PHC rate is this oscillator's, 0" (got 0x345a), its "real counter advances 8 ns a clock", and both again at -100 ppm (0xffffcb86) |
| `p107-est` (variant: BECOME writes the retained estimate, not rate 0) | generator: word-3 low word is `0 - integrator` | 396 PASS, 12 FAIL of 408, rc 2. All four arms fail rate 0 and the 8 ns advance, and the TLV checks fail |
| `p106-nocredit` (Announce leg without its credit gate) | generator: `e_credit_gate` removed from `prog_leg_anntx` | **408 PASS, 0 FAIL, rc 0.** The probe took effect: its ROM has 1,010 real words, not 1,013, and both phases' first Announces end 6 clocks earlier (279 / 2,000,097). This is F1 |

| Other gate at the head | Result |
|---|---|
| Campaign, `mutants.py`'s own `main()` on the two new controls (`scripts/campaign_slice.py`) | `[ ok ] first_master_announce_waits_for_a_beat: caught by "#106 race: one master Announce reaches the lane before the re-election"`; `[ ok ] word3_applies_only_during_a_slew: caught by "#107 settled +100 ppm: the mastership's PHC rate is this oscillator's, 0"`; controls 2, failures 0, rc 0 |
| `make lifecycle` | `mutant lifecycle: PASS (normal/repeat, eleven named defects, ...)`, rc 0 (`shadow-lifecycle-2.log`). My first attempt used `make -s`, rc 2 (`shadow-lifecycle.log`): the inherited silent flag hides the recipe echo that `ownership()` greps for. The cause is my invocation, not the delta (S4) |
| `gptp_tables` `run limits` (builds the changed wrapper) | `== gptp_tables: checks: 36   failures: 0 ==`, rc 0 |
| `tsn_fuzz` `build` (builds the changed wrapper) | rc 0 |
| Docs gates (`doc-gates-head.txt`) | check_doc_style OK (25), check_gptp_docs OK (8 pages), check_submodule_docs OK (6 exact gitlinks), docs_inventory OK, both diagram `--check` OK, `git diff --check 2509db68 HEAD` clean |
| Images (`images-unchanged.txt`) | 285 png/svg/drawio blobs and 6 gitlinks are identical between `bbfdb674` and the head. The independently regenerated default `gptp_ucode.hex` is `4eb21cef…`, equal to the `rom_digests.tsv` row. No path changed since round 1 is a synthesis or firmware input |

Check-count reconciliation: the delta adds 82 `expect` executions (phase 18: 53, phase 19: 16, phase 20: 13) and removes none. 326 + 82 = 408.

**Consumer gates whose inputs the delta does not touch.** These are `gptp_plane` with phc-step, `gptp_txts` and the milan_dp `gptp`/`gptp-lat` legs. None reads a changed path: only `gptp_tables`, `tsn_fuzz` and `gptp_shadow` build the wrapper. My round-1 executions of them at `bbfdb674` therefore stand. I also spot-checked the author's head receipts:
- `gptp_plane`: 31/31.
- phc-step: 62 checks and 8 arms. The 8 are clean, the no-cease control and six planted defects, split 4 + 4 across two windows. I counted them in `phc_step.py:58-90`.
- `gptp_txts`: 13 controls.
- `gptp_tables`: 26 controls.
- milan_dp: 212/212 each, `[CA]` 0xF822436A and 0xF8FE436A.
- lint: 89 <= 89.

The author's hosted runs at this head were mostly queued when I read them. Only `bdd-conformance` had completed (success).

## Findings

### R915-2-F1: MINOR. Lenses: Tests, Robustness. Phase 20 cannot fail for an Announce leg that ignores the transmit credit.

- **Where:** `tb/verilator/gptp_shadow/sim_main.cpp:2760-2765` (the claim "the first master Announce leaves at once only with transmit credit"), `:2795` (check "#106 credit: no master Announce while the credit is withheld"); README.md row 20; `docs/reference/SUBMODULES.md:1047`; the PR's phase table row 20.
- **Authority and evidence:**
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect".
  - R916-1-F1 asks for the "transmit-credit behavior" to be graded.
  - The engine's credit is `~credit_hold_i & <reserve free>` (`hdl/ieee8021as/gptp_plane/KL_gptp_txticket.sv:259`), and `credit_hold_o = seal_r` (`KL_gptp_txret.sv:758`).
  - Phase 20 withholds credit only by the seal. The seal also holds the departure fence (`KL_gptp_shadow.sv:935-968`: `tx_tvalid_o` masked in `FN_HELD`). An Announce sent without credit is therefore held or discarded by the plane, and the 1 s re-arm (placed ahead of the gates) sends the next one at the same instant.
  - Measured: `p106-nocredit` (the gate removed; ROM 1,010 real words) passes 408/408, including both credit checks.
  - Phase 20 does discriminate the old 2 ms beat (`p106-beat` fails both credit timing checks). So it grades the retry's origin, not the credit gate.
- **Impact:** a later pin or generator change that drops or bypasses ANNTX's credit gate stays green on the platform. The other credit-withholding cause, the ticket reserve, has no fence behind it, and there a credit-less Announce would reach the MAC. The phase names credit as the cause of a result the fence produces.
- **Required outcome:** one of these.
  - Withhold the credit by a path the fence does not also enforce (for example the ticket reserve), so that a credit-less master Announce reaches the lane and a named check fails. Show it red with the ANNTX credit gate removed (a campaign control or a published probe).
  - Or restate phase 20's claim and check names (sim_main.cpp:2760-2765, :2795, README row 20, SUBMODULES.md:1047, the PR row) as "a sealed takeover's master Announce is held and re-sent one announce interval later". Then record the ANNTX credit gate as not separately observable in this suite, with its anchor, in `NOT_SEPARATELY_OBSERVABLE`.
- **Verification:** for the first option, `p106-nocredit` (in `probe-diffs/`) turns a named phase-20 check red at the fix head and the head passes. For the second, the campaign prints the new `[note]` line and the claims match.

### R915-2-R1: RESIDUE. Lens: Docs. The selection rule's sentences are out of order.

- **Where:** `docs/reference/SUBMODULES.md:984-990`.
- **Evidence:** the rule's meaning matches #818 (the first directive ships if it meets the floor, as a single shipping route; otherwise the best worst-corner WNS of three ships). But "At 1x1 the first missed, as on the base." (986) now sits between the rule's two halves, so "Otherwise all three are routed." (988) reads as following the 1x1 instance. The order came from my own round-1 exact fix, which replaced lines 984 and 988 in place. The table and the selection are right.
- **Exact fix:** order lines 984-990 as "An image meeting the floor on the first directive ships. / Otherwise all three are routed. / The best worst-corner WNS ships (#818). / At 1x1 the first missed, as on the base. / So all three were routed there." Each sentence is one paragraph, as now. `check_doc_style.py` passes with it (`receipts/published/residue-fix-style-check.txt`).

### R915-2-R2: RESIDUE. Lens: Docs. The new phase numbers collide with an existing phase 18.

- **Where:** `sim_main.cpp:2258` ("// ---- 18: the PHC trajectory…", existing) against `:2368` ("// ---- 18-20"), `:2587` "(phase 18)", `:2661` "(phase 19)" and `:2760` "(phase 20)". Also README.md rows 18-20 and lines 93-94, `SUBMODULES.md:1037, 1043, 1047`, and the PR phase table and its text.
- **Evidence:** two different phases are both "18". Labels only; no check or figure depends on them.
- **Exact fix:** renumber the new phases 19, 20 and 21 at every site above (or renumber the trajectory phase and say so).

### R915-2-R3: RESIDUE. Lens: Docs. "starts there" has the wrong antecedent.

- **Where:** `CHANGELOG.md:71`, "The 1 s cadence starts there (802.1AS-2011 Figure 10-15)."
- **Evidence:** it follows "Before, an Announce at the timeout instant could pre-empt it.", so "there" reads as the timeout instant. The cadence counts from the first master Announce, which leaves 285 clocks after the instant.
- **Exact fix:** "The cadence counts from that Announce (802.1AS-2011 Figure 10-15)." It passes the style gate; the "1 s" wording gives 11 words and fails (`residue-fix-style-check.txt`).

### R915-2-S1: SUGGESTION. The slewing arm's TLV has the opposite sign.

- In the slewing -100 ppm arm, the TLV frequency change is -3,235,644. The settled -100 ppm arm's is +3,517,186.
- This follows from the donor servo. One 1,473 ns pair moves the integrator by about -25,000 units (`gen_gptp_ucode.py:1134-1141`: I += T/4), and #107 defines the TLV as the negated estimate. The phase grades it only as present, by design (the PR says so).
- Record the observed sign in the README or the record. Consider a donor issue on scaledLastGmFreqChange after a phase transient, since 802.1AS means it as the frequency change against the departed grandmaster.

### R915-2-S2: SUGGESTION. The race arm's Announce arrives just after the instant.

- In the race arm, GMID's Announce is sent 634 clocks after the published instant (5,999,366 against 6,000,000) and re-elects at +1,281. The fix's master Announce ended at +285.
- So the arm grades an Announce arriving within the old 2 ms beat. That is the defect, and the arm catches it. It does not grade one already queued when BECOME runs.
- An arm sending it a few hundred clocks before the instant, within the deadline's millisecond, would cover the queued order too. "Phase 19 queues an Announce at the receipt-timeout instant" (`SUBMODULES.md:1043`) is right only at millisecond resolution.

### R915-2-S3: SUGGESTION. The suite's runtime needs a hosted measurement.

- The PR says the default target "stays well inside" the 1,800 s suite timeout. On this host, at load about 190 on 32 CPUs, one build plus run took 160 to 194 s, and two campaign controls took 390 s (`walltimes.txt`). Twelve runs would then exceed 1,800 s here.
- Hosted runners are faster, but the margin is unmeasured. Replace "well inside" with the hosted figure once measured, and update `scripts/suite_shards.py` (393 s).

### R915-2-S4: SUGGESTION. `ownership()` breaks under an inherited `make -s`.

- `test_mutant_lifecycle.py:345-357` (`ownership()`, not in the delta) fails under an inherited `make -s`, because the inner make stops echoing its recipe.
- Pinning `MAKEFLAGS` in the probe environment would make it invocation-independent.

### R915-2-S5: SUGGESTION. File the disclosed `credit_never_withheld` naming defect.

- `credit_never_withheld`'s expected check name matches nothing. The PR discloses this.
- At the head it is caught only by the new phases' quiet-start guards, so those phases never run under it.
- Open the separate Issue the PR suggests. A reserve-credit phase written for F1 could supply the missing check.

## Prior public findings at this head

I read the round-1 findings after my own pass over the diff and the probes above.

- **R915-1-F1 (MAJOR, Tests, Robustness): RESOLVED at its cause.** Phases 18 and 19 meet both clauses of the required outcome: rate 0 and no step after a nonzero-trim takeover, and the master Announce before a re-election at the instant. Each fails with the gitlink at `1616fc8f` (`oldpin`: 16 FAIL), which is the verification I named.
- **R916-1-F1 (MAJOR): resolved except one clause, which I retain under F1.** The clause is "transmit-credit behavior", whose gate phase 20 cannot detect. Everything else is met:
  - the first master Announce before the queued re-election, with its cadence;
  - rate 0 and the 8 ns-a-clock counter advance with no step;
  - settled arms at both signs, a slewing arm at -100 ppm only (disclosed), and a repeated mastership with no slave rate.
  - R916's two defects turn the assertions red (the author's receipts, and my `p106-beat` and `p107-gate`).
- **R915-1-F2 (MINOR): RESOLVED.** #997 is open. It records the -100 ppm AECP silence, its reproduction at `1616fc8f` and `1213ac5b`, and its donor-review source. The PR's known limitations and `SUBMODULES.md` link it.
- **R915-1-R1 (RESIDUE): applied as I wrote it.** The meaning matches #818. The ordering it produced is R915-2-R1.
- **R915-1-R2 (RESIDUE): RESOLVED.** The PR body names the order ExtraPostPlacementOpt, AltSpreadLogic_high, ExtraTimingOpt.
- **R915-1-R3 (RESIDUE): applied, reworded.** The edition is now cited. The new antecedent issue is R915-2-R3.
- **R915-1-S1: done.** The PR explains the 1x1 "ruling floors NOT met" line as #870's WHS gate.
- **R916-1-R1 (RESIDUE): RESOLVED.** "the six later commits" is correct: `git log --first-parent 973f2f20..HEAD` lists 39e9c9d2, 8c5a51e1, bbfdb674, 3a8bdbf0, d616b1c6 and f97e49fe.

## Clean-lens lines

- **[R915] PASS Conformance** — #994 AC1-3 at f97e49fe: check_submodule_docs "6 exact gitlinks", check_gptp_docs "8 current pages"; `rom_digests.tsv` row against my regeneration `4eb21cef…`; images-unchanged.txt (no synthesis input since round 1, so round 1's route verdict stands); the new phases' 802.1AS reading (10.1.2.1 rate 0 at mastership; 2011 Figure 10-15 first Announce and cadence) against `sim_main.cpp:2368-2819` and the probe outcomes; the selection rule against #818 and BUILDING.md:620-627.
- **[R915] PASS RTL** — The delta has no product RTL. `gptp_shadow_wrap.sv:205-212, 303, 414` adds two observation outputs (the slice's `phc_slew_active_o`, previously open, and `step_we_w`, the counter's adjtime strobe), driving nothing back. `gptp_tables` (`run limits`) and `tsn_fuzz` (`build`) build it with both outputs unconnected (rc 0). The donor RTL and the gitlink are identical to round 1's (R915-1 RTL CLEAN), and the delta changes nothing it depends on.
- **[R915] PASS Docs** (R1-R3 are residue only) — CHANGELOG.md:65-86, TEST_DEVELOPER.md:42, SUBMODULES.md:980-1062 and gptp_shadow README.md:35-37, 88-94, 142 checked against sim_main.cpp and the probe logs; the PR body against the packet's PR-BODY.md and my executions; docs gates (doc-gates-head.txt).

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #994 AC1-3; pin-site gates; ROM regeneration; image/gitlink identity; #818 and BUILDING.md; new phases against 802.1AS-2020 10.1.2.1 and 2011 Figure 10-15 | R915-2 | `f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21` |
| RTL | CLEAN | `gptp_shadow_wrap.sv` taps; gptp_tables and tsn_fuzz builds; donor RTL unchanged since R915-1 | R915-2 | `f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21` |
| Robustness | UNCLEAN (F1) | Takeover from settled, slewing and no-rate slaves; the receipt-timeout race; credit withheld by the seal; harness hold-release reorder (`sim_main.cpp:1957-1960`, matching 1714-1720) | R915-2 | `f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21` |
| Tests | UNCLEAN (F1) | 408-check run; six probes including the old pin; the two new controls through `mutants.py main()`; lifecycle; check-count reconciliation; author receipts | R915-2 | `f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21` |
| Docs | CLEAN (R1-R3 residue) | CHANGELOG, TEST_DEVELOPER, SUBMODULES #994 record, gptp_shadow README, PR body; docs gates | R915-2 | `f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21` |

## Real limits

- No manager source bank ran at this head, and I claim none. Source-head execution is the author's published receipts plus my focused runs above. I did not run the full parent, PP, gPTP, Yosys or builder banks, Docker/act or any hosted job.
- I re-ran the gptp_shadow campaign only for the two new controls. The other nine rest on the author's three slices at `d616b1c6`, whose campaign inputs equal the head's.
- Not re-run by me at the head, because their inputs are unchanged since my round-1 runs at `bbfdb674`: `gptp_plane`, phc-step, `gptp_txts`, milan_dp `gptp`/`gptp-lat`, and the `tsn_fuzz` field campaigns.
- Routes, physical calibration and the board are NOT RUN. Field skips are not hardware proof.
- Runtimes were measured on a heavily oversubscribed host.

## Pending manager duties

- Carry R915-2-R1 to R3 to the residue checklist.
- Confirm the exact-head hosted `rtl-fast`, `verilator-suites` and `yosys-portability` results (queued when read), and the `gptp_shadow` shard time against the 1,800 s timeout (S3).
- Validate the current-dev merge candidate (builder and native banks) at the merge turn.
- After F1 is fixed, a re-review at the new head covering Tests and Robustness, and every lens whose artifacts the fix touches.

R915-2 FINISHED
