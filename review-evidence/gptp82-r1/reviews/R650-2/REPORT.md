[R650] NEGATIVE - exact head 8f3c376d1e07d2f1417889ae2ac590c71b8cb910

# R650-2 internal independent review: FPGA-gPTP PR #83 (issue #82), round 2

- Exact head `8f3c376d1e07d2f1417889ae2ac590c71b8cb910`, tree `359e2e2518117b70fd1efd4287ecf2888a61d102`. Source base `b9ade3a63d1b2292d75eb9b1809647e6439542a0`. Delta reviewed since the round-1 head `85373de0`: three commits, `f29094c`, `ff62370` and `8f3c376`.
- Parent reference: dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`, with the gPTP pin at `e4869fd0`.
- Assignment: [round-2 assignment](https://github.com/Mister-M-alt/FPGA-gPTP/pull/83#issuecomment-6251117177). Review start: [comment 6254193304](https://github.com/Mister-M-alt/FPGA-gPTP/pull/83#issuecomment-6254193304).
- Evidence: [milan-fpga `476262d7` review-evidence/gptp82-r1/author-r2](https://github.com/kebag-logic/milan-fpga/tree/476262d73e7181b2d9eda360a774427bd07527a3/review-evidence/gptp82-r1).

## Verdict summary

The three round-1 behaviour faults are fixed at their cause, and every prior finding is closed (see the table below):

- **Cold start.** thisClock is now ROM data. Reset loads the self tuple, and the boot commit fires on the first edge after release.
- **Capability loss.** An asCapable fall expires the Announce receipt watch, and BECGATE then drops the elected peer through SELF.
- **Warm reset.** The best record now has reset-backed validity, and the raw path is reset.

What I checked myself at this head:

- The suite passes 1634/1634 on all three images.
- Four of the published controls fail exactly the checks they name.
- Parameter and port declarations are identical at e4869fd0, b9ade3a6, 85373de0 and the head.
- The published receipt index matches its directory exactly.
- The parent mutant arms ran to completion against a committed local gitlink, with no refusal.

The verdict is NEGATIVE on one MINOR test gap and one MINOR conformance-scoping statement. Both concern the new asCapable departure path:

- **F1.** The drop commit clears the presence and sync flags, and the parent consumes the sync flag. A planted control that keeps those flags survives the whole suite. A second control, which removes the watch re-arm that restores mastership after capability returns, also survives.
- **F2.** The PR files "gm_present stays 0 ... after a dropped peer" as a known limit "unchanged by this PR". This PR creates that state. The other departure path, Announce silence, publishes gm_present 1.

One RESIDUE (a source comment) and two SUGGESTIONs follow.

## Reconstruction order and authorities

1. **Repository rules.** There is no tracked `AGENTS.md` or `CONTRIBUTING.md`. I read `docs/README.md`, which sets the truth order (RTL and microcode, then tests, then guides), and the current role guides.
2. **Scope.** Issue #82 body: done when the engine publishes thisClock and {thisClock} from reset, a boot case with a planted mutant exists, and the parent consumer gates pass. Assignment comment (A10): three cases with mutants, the parent gates on dev e9cbb676, and STOP on any interface or parameter change. The round-2 assignment adds items 1 to 7. There are no maintainer scope decisions narrowing any of these.
3. **Requirements.** The IEEE 802.1AS-2020 clauses named in the assignment:
   - 10.3.13.2.4 b), i): with no port vector, thisClock is the grandmaster and the path is {thisClock}.
   - 10.3.9.23: pathTrace.
   - 10.3.11: PortAnnounceInformation, receipt timeout.
   - 10.3.12: PortStateSelection, including BEGIN and DISABLED, and gmPresent.
   - 10.7.3.2: announceReceiptTimeout.

   I did not have the final-edition standard text in hand. Clause obligations below rest on the frozen acceptance and the assignment's citations.
4. **Interface authority.** The parent consumes the engine at `hdl/milan/milan_datapath.sv:1503-1515`, and only bits 3 (sync_ok) and 2 (asCapable) of the published flags at `:2040-2041`. The shadow captures the bank on commit (`KL_gptp_shadow.sv:737-750`). Both read at e9cbb676.
5. **Diff and history.** I read `git diff b9ade3a6..8f3c376d` and the round-2 delta `85373de0..8f3c376d`. Files: RTL `KL_gptp_engine.sv`, generator `gen_gptp_ucode.py`, four regenerated images, `mutants.py`, `sim_main.cpp`, and five guides.
6. **Evidence.** The `author-r2/` packet, its RECEIPTS.md index and the MANIFEST.json published hashes. The PR body.
7. **Prior findings.** I read the R650-1 and R651-1 findings only after my own verdict and ledger were written and hashed: `receipts/independent-verdict-before-prior-findings.md`, sha256 `4708d7aa96b9c735226207ce79a2cb78a61a1f6b897614250598e28c516c58da`.

## Assignment items, checked against the head

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | Self tuple published and committed at reset release; thisClock loaded at reset from ROM data; release-to-first-timer interval graded, with a mutant | **Met** | See below |
| 2 | A peer whose port is not asCapable, or whose Announce receipt timed out, stops contributing; both paths tested, with mutants | **Met**, with the F1 gap on side effects | See below |
| 3 | Warm reset clears the retained vector and path; a better absent peer and a worse present peer elect the present one; with a mutant | **Met** | See below |
| 4 | Boot-commit uniqueness and the warm-reset path tail graded | **Met** | See below |
| 5 | Parent gates, including the `gptp_shadow` mutants and `gptp_tables`, run to completion against a committed local parent snapshot, without bypassing the guard | **Met** | See below |
| 6 | No port or parameter change seen by the parent; the ROM digest and ledger row change is expected | **Met** | See below |
| R1 | Round-1 residue applied to the PR body | **Met** | The PR body Interface section carries the exact fix text |

**Item 1: cold start.**

- `hdl/top/KL_gptp_engine.sv:157-171`: thisClock is read from ROM words 1022 and 1023 of `UCODE_HEX_P`.
- `:814`, `:820-821`: reset loads GM thisClock, count 1 and a zero tail.
- `:849-850`: the boot commit is the first edge after release.
- `gen_gptp_ucode.py:2184-2189` places the two data words. `:2161-2162` keeps the packer out of them.
- Grading: `sim_main.cpp:549-555` grades every cycle from release to the first beat, and `:1196-1214` grades the commit.
- My run: "cold release graded for 2400605 cycles", 1634/1634 (`receipts/probes/engine-run-head.log`).
- Controls: "reset leaves the grandmaster zero", "words read swapped", "reset leaves the path empty" and "waits for the timer bootstrap" are all caught in the published shards. My word-15 probe trips the new S_CID/ROM assertion at `:855-856` (`receipts/probes/word15_zero.log`).
- No interface change was needed (item 6).

**Item 2: departure.**

- The engine hook at `:933-937` arms slot 2 at 1 ms whenever a flags write clears bit 2.
- I traced all three handlers that clear asCapable (`gen_gptp_ucode.py:1476`, `:1525`, `:1950`). None of them writes timer slot 2 after the flags write. The only other slot-2 writers are init-once, BTCA `same_gm` and BECOME.
- The Announce handler is gated on asCapable (`:939`), so an incapable port cannot re-arm the watch.
- BECGATE (`:1670-1703`): a master ends; a capable port goes to BECOME; an incapable port re-arms the watch and, if a peer is present, writes flags 0 and goes to SELF.
- Tests: phase 35 covers Announce silence with Pdelay answering (`sim_main.cpp:4859-4872`). Phase 36 covers Pdelay loss with Announces continuing (`:4875-4926`).
- My run: thisClock was committed 1970 cycles (0.985 ms at 2 MHz) after the fall.
- Controls:
  - My `hook_delta_3000` probe fails all three Pdelay-loss checks.
  - The published "an asCapable fall leaves the receipt watch running", "an incapable receipt timeout keeps the elected peer" and "an incapable port's Announces still compete" controls are caught.
  - My `drop_via_become` probe is caught by four existing slew checks, so the "no mastership PHC transition" claim is guarded.
- The gaps on flags and on recovery to mastership are F1.

**Item 3: warm reset.**

- `KL_gptp_engine.sv:252-262`, `:759-762`, `:839-841`, `:909-915`: an unwritten best record reads all ones, the worst vector.
- I traced BTCA (`gen_gptp_ucode.py:1585-1640`) against an all-ones record. The source compare and the pv, id and steps compares all `take` for any Announce that passes qualifyAnnounce, because stepsRemoved ≥ 255 is rejected first. So the RTL comment "any received Announce displaces" holds.
- The path is reset at `:821`.
- Phase 35: B (priority1 2) wins over the absent A (priority1 0) with its own path. C (priority1 250) leaves thisClock.
- My independent runs of "a warm reset keeps the retained best record" and "an unwritten best record reads as the best vector" fail exactly their named checks (`m1.log`, `m2.log`).
- The phase-35 comment at `sim_main.cpp:4794-4805` is corrected.

**Item 4: boot commit and tail.**

- Graded by "one commit before the first beat", "one commit in the first 2 ms", "first edge after release", "its path is {thisClock} with a zero tail", and the run-wide invariant at `:4929-4937`.
- My independent runs of "the boot commit fires twice" (`m3.log`) and "reset keeps the elected tail" (`m4.log`) fail their named checks.
- The published "never retires" control is caught.

**Item 5: parent gates.**

- The parent commit is local and its push remote is disabled (`parent/remotes.txt`).
- Commits: `e54c7c21` pins the gitlink, re-points the docs and adds the ledger row. `3d0cae2b` updates the milan_dp test.
- `pgates/head/GITLINK` shows ` 8f3c376d` with no index or worktree prefix.
- No `REFUSED` line appears in any head parent-gate log.
- Results: `gptp_shadow-mutants` controls 9, failures 0, RESULT PASS. `gptp_tables` controls 26, failures 0, PASS. Shadow 309/309. Lifecycle PASS.
- milan_dp `gptp` and `gptp-lat` are 182/182, with the updated test. The dev test fails 3 of 182 at head; the updated test fails 2 at base.
- The base arms are also recorded.

**Item 6: interface.**

- My own extractor (`scripts/ports.sh`) strips comments and whitespace from the module header. It gives an identical sha256, `946e8389198024398bc7a66de35e0af305b5885ba8f9acdb69931ce44da7bb70`, at e4869fd0, b9ade3a6, 85373de0 and 8f3c376d (`receipts/ports-*.txt`). This matches the author's iface receipts: 1366 bytes, identical at the four revisions.
- The default image regenerated at head has sha256 `00826e9be6b0aeaa6fef58e7f46b48508626661d96aef317a0d6ce67ac5fe5ae`. That equals the committed `tb/verilator/ucpu` and `syn/ooc/work` copies and the new parent ledger row. The engine-suite image also regenerates byte-exact (`44e48258...`).

## Findings

### F1 - MINOR - Tests, Robustness - two consumer-visible effects of the new asCapable departure path are not graded

- **Where:**
  - `hdl/ucode/gen_gptp_ucode.py:1691-1692`: the incapable branch re-arms the receipt watch.
  - `:1699`: the drop writes flags 0 before `BR SELF`.
  - `tb/verilator/engine/sim_main.cpp:4875-4926`: phase 36 checks GM, path, the 2 ms bound, incapable-port Announces, and the post-recovery election of E. It never inspects the drop commit's flags, and it never lets the port regain asCapable without Announces.
  - Claimed in `docs/INTEGRATION.md:516` ("Its commit also clears the presence and sync flags.") and `:524` ("Without Announces, the receipt watch then grants mastership.").
  - Claimed in the PR body, "What a consumer sees differently": "a commit within about 1 ms names thisClock and clears the presence and sync flags".
- **Authority:**
  - Assignment item 2: publication returns to thisClock; both departure paths are tested with planted mutants.
  - 802.1AS-2020 10.3.12: an asCapable port that receives no better Announce becomes master after 10.7.3.2 announceReceiptTimeout.
  - The parent consumes flag bit 3 as `fabric_sync_ok_i` (`milan_datapath.sv:2040` at e9cbb676).
- **Evidence.** These are reviewer probes on scratch copies of the head, using `scripts/probe_mutant.py` and `scripts/flags_probe.sh`.
  - `drop_keeps_flags` deletes only the `WRST ra=0, RG_PUB|2` at `:1699`. The engine suite still passes 1634/1634, rc 0 (`receipts/probes/drop_keeps_flags.log`).
  - A printf-only harness copy reads the flags at the phase-36 commits (`receipts/probes/flags-clean.log`, `flags-drop_keeps_flags.log`):
    - The fall commit has flags `0x1` with GM D.
    - At head, the thisClock commit has flags `0x0`.
    - Under the control, the thisClock commit has flags `0x1`: gm_present with GM thisClock and no master bit. All 1634 checks still pass.
  - Sync-ok is already 0 when asCapable falls in phase 36, so "clears the sync flag" is never exercised either way.
  - `held_no_rearm` deletes the BECGATE re-arm at `:1691-1692`. The suite passes 1634/1634 (`receipts/probes/held_no_rearm.log`). With that defect, a port that is dropped and later regains asCapable while its peer has stopped announcing never becomes master.
- **Impact:**
  - A regression that leaves sync-ok set after the drop would reach the parent's `fabric_sync_ok_i`, paired with a self grandmaster that is not master, for up to the 375 ms sync receipt timeout. No check in this repository would fail.
  - A regression in the recovery path would leave the plane non-master on a capable link with no grandmaster on the wire, again with no check failing.
  - Both behaviours are correct at this head. Only their protection is missing.
- **Required outcome:**
  - In phase 36 or a sibling phase, take the capability fall while sync-ok is set. Grade that the drop commit carries the intended flags word: presence, sync-ok and master clear.
  - Grade that, after the drop, a port that regains asCapable with no further Announces commits mastership with thisClock and {thisClock} within one receipt interval.
  - Add each probe above as a planted control naming its check.
- **Verification:** `drop_keeps_flags` and `held_no_rearm`, as in `scripts/probe_mutant.py`, each fail their new named check. The suite stays 1634+N on all three images.

### F2 - MINOR - Conformance, Docs - the PR files a gmPresent state this change introduces as a pre-existing, unchanged limit

- **Where:**
  - PR #83 body, "Known limits, unchanged by this PR": "gm_present stays 0 at boot and after a dropped peer."
  - Code: the BECGATE drop writes flags 0 (`gen_gptp_ucode.py:1699`), with the comment at `:1696-1698`: "Drop it: no grandmaster is selected and sync is not ok, as after a reset". SELF then publishes thisClock as the grandmaster.
  - BECOME, the Announce-silence departure, sets PRESENT|AMGM (`:1717`).
- **Authority:**
  - 802.1AS-2020 10.3.12, as cited in the assignment, sets gmPresent from gmPriority's priority1 being below 255. thisClock's priority1 is 248 (`gen_gptp_ucode.py:419`, `P1_C`).
  - Assignment item 2 introduced the drop path in this round.
- **Evidence:**
  - At base `b9ade3a6` there is no dropped-peer state. The only departure is BECOME, which publishes PRESENT 1.
  - At this head, the asCapable drop newly publishes GM thisClock with PRESENT 0 (`flags-clean.log`, self flags `0x0`).
  - The Announce-silence departure still publishes PRESENT 1. Phase 35's mastership commit carries FL_AMGM, set together with FL_PRESENT.
  - So the PR's sentence is wrong in two ways. The state is new, not unchanged. And it holds after one of the two departures, not after "a dropped peer" in general.
  - At boot the flag value is unchanged, but it now pairs with a nonzero self GM instead of GM 0.
  - No tracked issue or scope decision records this.
- **Impact:**
  - The parent datapath does not consume bit 0 today, so the consumer impact is small. However, the PR's conformance-limit disclosure misstates what this change introduces.
  - The same self publication carries a different presence bit depending on which departure produced it.
- **Required outcome:** one of the following.
  - Publish PRESENT consistently with the self tuple (reset and the SELF drop), per 10.3.12 gmPresent, with a check.
  - Or keep the behaviour and correct the PR body. State that the asCapable drop is new in this PR and publishes gm_present 0 with GM thisClock, while the Announce-silence departure publishes 1, and that boot now pairs thisClock with gm_present 0. Link a tracked follow-up issue or a recorded scope decision. Align the `:1696-1698` comment.
- **Verification:** the PR body and the tracked issue or decision link exist, or a graded check on the presence bit of both departures and the boot commit passes.

### R1 - RESIDUE - Docs - RTL comment says the best record "returns to the local vector" at reset

- **Where:** `hdl/top/KL_gptp_engine.sv:704-706`, "Every reset loads the self publication, thisClock and {thisClock}, as the best record below returns to the local vector (#82)".
- **Evidence:** reset does not write the local vector into the best record. It invalidates the record, which then reads as the worst vector (`:252-262`, `:759-762`, `:839-841`). The behaviour, tests and the comment at `:252-258` are correct. Only this sentence is imprecise.
- **Exact fix:** "Every reset loads the self publication, thisClock and {thisClock}, and invalidates the best record below, so only a newly received Announce competes with the local vector (#82);"

### S1 - SUGGESTION - RTL - the parser's loop check still waits for the init leg on a cold start

- **Where:** `KL_gptp_engine.sv:156-157`, `:181-182`, `:889-894`. `local_clock_valid_r` becomes 1 only when the init leg writes S_CID, about 1.2 s after a cold release. Until then, the parser refuses over-cap Announces that carry this identity ("pre-init deep Announce", `sim_main.cpp:1153-1167`).
- **Suggestion:** thisClock is now known from configuration (`rom_clock_id_w`). The parser could take it, valid from reset, and the S_CID mirror and its assertion would then be redundant. This is not required by #82: RX handlers are guarded until init, so nothing is elected in that window.

### S2 - SUGGESTION - Robustness - the asCapable hook shares the timer-arm registers with the hardware boot arms

- **Where:** `KL_gptp_engine.sv:864-876` (boot arms at counts 254 and 255) and `:933-937` (hook), in the same `always_ff`.
- **Analysis:** the comment at `:931-932` explains why no µcode timer write can collide with the hook. The boot arms are another writer. A collision is unreachable today, because `pub_flags_r` resets to 0 and asCapable needs two Pdelay exchanges, far longer than 256 cycles.
- **Suggestion:** extend the comment, or add a simulation-only assertion that the hook never fires while `!boot_done_r`.

## Prior public findings: resolved or retained at this head

| Finding | Status | Cause-level evidence at 8f3c376d |
|---|---|---|
| R650-1-F1 / R651-1-F1, cold start 1.2 s zero window | **Closed** | ROM thisClock and reset-loaded tuple (`:157-171`, `:814-821`); first-edge commit (`:849-850`). Cycle grading passes on my run. The four published cold controls are caught. The R651 cold probe re-run at head: `r651/head/probe-cold.log`, rc 0, `release_delta=0`. At the round-1 head: rc 1. |
| R651-1-F2, capability loss | **Closed**; F1 here is a new, narrower test gap on side effects | The hook (`:933-937`) and BECGATE drop (`gen:1694-1700`). Phase 36 is graded. My hook probe fails it. `r651/head/probe-gone.log`, rc 0: GM thisClock, count 1, flags 0 after 7 s. |
| R651-1-F3 / R650-1-F2, warm reset resurrects the retained winner | **Closed** | Validity bits and path reset. Phase 35 B-over-absent-A is graded. `m1` and `m2` are caught on my runs. `INTEGRATION.md:468/494` and the phase-35 comment are corrected. `r651/head/probe-warm.log`, rc 0, successor B. |
| R650-1-F3, boot-commit uniqueness and warm tail ungraded | **Closed** | The checks listed under item 4. `m3`, `m4` and the published "never retires" control are caught. |
| R651-1-F4, parent mutant arms refused | **Closed** | Committed local gitlink `e54c7c21`; no `REFUSED`; shadow 9/0, tables 26/0, both RESULT PASS. |
| R650-1-F4, receipt index named an unpublished `iface/` | **Closed** | `iface/` is published. My `scripts/verify_index.py` finds 131 files and 131 in-directory rows, 0 mismatched, 0 unlisted, plus 3 out-of-tree scratch rows. All 132 `author-r2/` MANIFEST.json published hashes match, including RECEIPTS.md itself as recomputed after redaction (`receipts/verify-author-r2-index.txt`). |
| R650-1-R1, "byte-identical" wording | **Closed** | The PR body uses the exact fix text. |
| R650-1-S1, idle guard and cancel branch ungraded | **Closed** (moot) | Both guards are removed. The commit is unconditional at the first edge, and no handler can run before it. |
| R650-1-S2, zero-GM sentinel | **Closed** | Raw GM is thisClock from reset. GM 0 is now only a canonical-zero output gate (`:1027-1029`) and no longer substitutes thisClock. |

## Lens summaries

- **Conformance: UNCLEAN (F2).**
  - 10.3.13.2.4 b), i) hold from reset release and after both departures.
  - 10.3.12 BEGIN: no retained vector competes. 10.3.12 DISABLED: an incapable port's vector is dropped and its Announces are refused.
  - 10.3.11 and 10.7.3.2: Announce silence on a capable port still ages the peer out to mastership.
  - The gmPresent scoping statement is F2.
- **RTL: CLEAN.**
  - The ROM copy reads two constant words. The author's synthesis proxy reports it folds to constants and keeps LUTRAM single-port (RAM64X1S, RAM32M, RAM64M and RAMB18 counts unchanged).
  - The validity mux keeps the read address equal to the write address.
  - The hook cannot share a cycle with a µcode timer write.
  - No multiply-driven state remains (the `pub_path` initial block and its lint waiver are removed).
  - My `make lint` with the scoped simulator is rc 0 with no warnings.
- **Robustness: CLEAN** for the three faults. F1 carries the recovery-path test gap under Tests and Robustness, but the behaviour is correct at head. I checked:
  - warm reset mid-handler;
  - reset held long, where outputs show thisClock and there is no commit;
  - asCapable falls as master, which BECGATE ends harmlessly;
  - asCapable falls with no peer, where the watch is re-armed and nothing is published;
  - repeated Pdelay-lost writes with bit 2 already clear, which leave the hook idle;
  - an all-ones Announce against an invalid record.
- **Tests: UNCLEAN (F1).**
  - 19 #82 controls. All 52 arm controls are present as caught across the 8 published shards, each with a passing clean control.
  - Reproduced: 1634×3, and four controls independently.
  - Two surviving reviewer controls (F1).
- **Docs: UNCLEAN (F2).**
  - Guides match the head: ROM 1,013/1,024 with 11 free words, `FUTO@125`, word 15, the reset and departure sections.
  - Source-evidence anchors pass: `make docs` reports 20 exact and 0 findings.
  - The PR-body known-limit line is F2. R1 is residue only.
  - The comment rule holds: no lane labels, review rounds, reviewer IDs or comment IDs appear in added source lines (scan of `git diff b9ade3a6..HEAD -- hdl tb scripts`).

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | Issue #82 body and the A10 assignments; 802.1AS-2020 10.3.13.2.4 b) i), 10.3.9.23, 10.3.11, 10.3.12, 10.7.3.2 as cited; reset, BTCA, BECGATE, BECOME and SELF; parent flag consumption | R650-2 | 8f3c376d1e07d2f1417889ae2ac590c71b8cb910 |
| RTL | CLEAN | `KL_gptp_engine.sv` delta (ROM copy, reset tuple, boot commit, validity mux, hook, output gate); generator packing and data words; lint rc 0; author synthesis-proxy stats | R650-2 | 8f3c376d1e07d2f1417889ae2ac590c71b8cb910 |
| Robustness | CLEAN | Hook and timer-writer interaction; asCapable-clearing handlers; Announce gate; all-ones record against BTCA; warm and cold reset paths; probes `hook_delta_3000`, `drop_via_become`, `word15_zero` | R650-2 | 8f3c376d1e07d2f1417889ae2ac590c71b8cb910 |
| Tests | UNCLEAN (F1) | `sim_main.cpp` phases 1d, 35, 36 and the invariant; `mutants.py` 52 controls and 8 published shards; my 1634×3 run; independent `m1`-`m4`; surviving `drop_keeps_flags` and `held_no_rearm` | R650-2 | 8f3c376d1e07d2f1417889ae2ac590c71b8cb910 |
| Docs | UNCLEAN (F2) | Five guides delta; `make docs contract` rc 0; source-evidence anchors; PR body; author-r2 RECEIPTS index and manifest; comment-rule scan | R650-2 | 8f3c376d1e07d2f1417889ae2ac590c71b8cb910 |

## Reviewer execution (exact head, scratch copies only)

- **Scoped simulator.** Wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`, Verilator 5.050 rev v5.050 (`receipts/identity-and-hosted.txt`).
- **Engine suite.** 1634/1634 on each of the three images, rc 0 (`receipts/probes/engine-run-head.log`).
- **Controls taken verbatim from the head `mutants.py`.**

  | Control | Failed checks | Receipt |
  |---|---|---|
  | warm reset keeps the retained best record | 3 named | `m1.log` |
  | unwritten best reads best | 11, including both named | `m2.log` |
  | boot commit fires twice | 2 named | `m3.log` |
  | reset keeps the elected tail | 2 named | `m4.log` |

- **Reviewer probes.**

  | Probe | Result | Receipt |
  |---|---|---|
  | `hook_delta_3000` | caught, 3 FAIL | `hook_delta_3000.log` |
  | `drop_via_become` | caught by 4 slew checks | `drop_via_become.log` |
  | `word15_zero` | caught by assertion | `word15_zero.log` |
  | `drop_keeps_flags` | **survived** | `drop_keeps_flags.log` |
  | `held_no_rearm` | **survived** | `held_no_rearm.log` |
  | flags read at the drop commit | head `0x0`, control `0x1` | `flags-*.log` |

- **Gates.** `make docs contract` rc 0. `make lint` rc 0 (`receipts/probes/docs-contract-head.log`, `lint-head.log`).
- **Interface.** Header extract identical across four revisions.
- **Receipts.** Published index and manifest verified.
- **Note on the probe script.** `scripts/probe_mutant.py` gained the `held_no_rearm` entry and the `m:` mode after the first four probes ran. Their code paths are unchanged.
- **Clone integrity.** After all probes: HEAD and tree match; the index equals the HEAD tree (107 entries); every tracked file's bytes and mode equal its blob; `git status --porcelain --ignored` is empty. This repository has no submodule gitlinks (`receipts/clone-integrity.txt`). The clone was never written; every probe ran on `git archive` copies under `scratch/`.

## Real limits

- I did not have the final-edition 802.1AS-2020 text. Clause readings follow the assignment's citations.
- **Packet signature.** The evidence commit `476262d7` is unsigned. Integrity rests on the manifest's published hashes and the RECEIPTS index, both of which I verified. The three large synthesis logs live only in author scratch, recorded by hash, and I did not see them.
- **Parent evidence.** Parent gate results are the author's executions on a local, never-pushed parent. I did not re-run any parent gate.
- **Mutant arm.** The 52-control arm was credited from the published shard logs. I re-ran 4 controls, not the arm.
- **Not run.**
  - The full parent, PP, gPTP, Yosys and builder banks.
  - Vivado OOC: the MANAGER.md resource tables are not re-measured for this change.
  - The nightly physical gPTP job. The handoff notes that its mid-run-reset GM check will need the same update.
  - The full milan_dp sweep and the media-clock suites.
- **No manager bank.** There is no manager source bank at this head, and none is claimed or inferred.
- **Hosted checks.** Zero check runs, and a pending combined status with no contexts. No hosted job is credited.
- **Hardware.** Physical calibration NOT RUN. Field skips and simulated field campaigns are not hardware proof.

## Pending manager duties

- After F1 and F2 are resolved and two independent reviews are positive, build the current-dev merge candidate from source base b9ade3a6 against live dev e9cbb676. Bump the gptp-processor pin together with:
  - the eight gPTP doc re-points;
  - the `syn/yosys/rom_digests.tsv` row for 8f3c376d (`00826e9b...`);
  - the milan_dp `sim_gptp.cpp` update, which expects thisClock and masks the CLKV discontinuity bit 3 that the boot GM edge arms;
  - the corresponding nightly `sim_ax1x1gptp.cpp` reset expectation.
- Run the builder and native banks and link their receipts on the PR.
- Confirm that no parent flow feeds the engine a ROM image from an older generator. The engine now takes thisClock from words 1022 and 1023 of `UCODE_HEX_P`.
- Own hosted and act acceptance.
- Carry R1 to the residue checklist.
- #82 stays open ("Refs") until the parent consumer change lands, per the PR body.

R650-2 FINISHED
