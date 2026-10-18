[R650] POSITIVE - exact head 334e9fe64dfff5568be58a0dc9aeb302959b3b58

# R650-3 internal independent review: FPGA-gPTP PR #83 (issue #82), round 3

- Repository: Mister-M-alt/FPGA-gPTP, PR #83, base `main`.
- Exact head `334e9fe64dfff5568be58a0dc9aeb302959b3b58`, tree `fdb142e8ffb1a8f68158feaf00d486f6f5e3c3e2`. The PR's headRefOid matches.
- Delta reviewed: three commits on `8f3c376d` (`784da3f`, `85d267a`, `334e9fe`). Source base for the whole PR: `b9ade3a63d1b2292d75eb9b1809647e6439542a0`.
- Assignment: PR comment 6254393722 (round 3). Review start: 6255592831.
- Evidence: kebag-logic/milan-fpga `6f640b75f3ce16dd015ab8bd6363db1ea9ddffac`, `review-evidence/gptp82-r1/author-r3`.

## Verdict summary

Every round-3 item holds at this head. No MINOR, MAJOR or BLOCKER is open.

1. **R650-2-F1 is closed.**
   - Phase 36 now takes the capability fall while sync-ok is set. The fall commit has flags `0x9`.
   - The drop commit's whole flags word is graded exactly: `0x1` in the default image, `0x0` in the priority1-255 image.
   - A port that regains asCapable with no further Announces commits mastership with thisClock and {thisClock}. Observed: 2,000,682 cycles (1.0 s) after the rise. Bound: 3 s.
   - `drop_keeps_flags` and `held_no_rearm` each fail their named checks. This holds in the published arm and in my own run at this head.
2. **R650-2-F2 is closed by making the behaviour conform.**
   - flags bit 0 = µcode bit 0 OR a configuration-time capability bit (ROM word 1022, bit 32, set when priority1 < 255). So every self publication of a priority1-248 image carries gmPresent: reset, the asCapable drop, the Announce-silence departure, and mastership.
   - Each of these is graded and has planted controls. The PR body's "Known limits" and `docs/INTEGRATION.md` are corrected.
3. **R650-2-R1 is closed.** The exact comment text is at `hdl/top/KL_gptp_engine.sv:708-712`.
4. **No port or parameter change reaches the parent.** The comment-stripped header is identical at `8f3c376d` and this head. The author's four-revision port digests all equal `ccf818c7…`. The parent reads only flags bits 3 and 2 (`milan_datapath.sv:2040-2041` at e9cbb676).
5. **The published author-r3 packet verifies.** Both shipped verifiers report 312 files, 312 rows, 0 mismatches, rc 0. All 313 MANIFEST.json published hashes match. No host paths remain.
6. **R651-2-F1** (the manager's redaction broke the verifier) **is closed on author-r3.**

Open items: one RESIDUE (wording only) and five SUGGESTIONs, listed under Findings. Three round-2 suggestions are retained unchanged.

## Reconstruction order and authorities

- The repository has no AGENTS.md or CONTRIBUTING.md. The applicable sources are:
  - `docs/README.md`, whose truth order is RTL and µcode, then tests, then current guides, then history.
  - `docs/INTEGRATION.md`, `HDL_DEVELOPER.md`, `TEST_DEVELOPER.md` and `SOURCE_EVIDENCE.md`.
- Frozen acceptance:
  - Issue #82 body: 10.3.13.2.4 b) and i). Done when: thisClock and {thisClock} from reset, a boot-state case with a mutant, and the parent consumer gates.
  - Issue assignment 6249575055.
  - Round-2 assignment 6251117177.
  - Round-3 assignment 6254393722: the F1 items, the F2 ruling to make it conform, the R1 text, and STOP on any parent-visible change.
- Authorities:
  - IEEE 802.1AS-2020: 10.3.13.2.4 (updtStatesTree: gmPriority, gmPresent, pathTrace) and 10.3.12 (PortAnnounceInformation: BEGIN, DISABLED, AGED).
  - The round-3 ruling's "10.3.12 sets gmPresent" names the 2011 PortRoleSelection location. The code cites the 2020 location, 10.3.13.2.4 g), which matches the issue's own numbering.
  - Parent consumer: `hdl/milan/milan_datapath.sv` at e9cbb676.
- I made my independent pass over `git diff 8f3c376d..334e9fe6`, the PR-wide diff stat from `b9ade3a6`, and the receipts. Only after that did I read the prior public findings (R650-2 6254388777, R651-2 6254290649).

## Assignment items, checked against the head

### 1. R650-2-F1: drop flags word and regain-without-Announces

**Harness.** In `tb/verilator/engine/sim_main.cpp:4927-5015` (phase 36), D sends a Sync and Follow_Up pair every 125 ms (`d_sync`) and an Announce every second while Pdelay is off. So sync-ok is inside its 375 ms timeout when asCapable falls.
- Published head log: `INFO … the fall commits flags 9, thisClock follows 1970 cycles later with flags 1`. In the priority1-255 pass, the second value is `flags 0`.

**Drop commit.** `expect("#82 Pdelay loss: the drop commit's flags are gmPresent alone", self->flags, self_present)` (`:4971`) is an exact match on the whole word. It requires presence to come only from the engine's capability bit, and sync-ok, master and asCapable to be clear.

**Regain.** After the rise, `wait_flags(FL_AMGM…)` runs (`:4987`) and then three checks:
- `master in 3 s`: the first ASCAP commit to the first AMGM commit, at most 6,004,000 cycles.
- `that mastership names thisClock, {thisClock}`.
- `that mastership commit has gmPresent` (`:5002-5008`).

Observed: 2,000,682 cycles. The rise commit and the mastership commit are therefore distinct, and the bound is not vacuous at this head.

**Controls** (`tb/verilator/engine/mutants.py:429-441`):
- `the asCapable drop keeps the flags word` deletes only the BECGATE `WRST ra=0, RG_PUB|2` before `BR SELF`. This is the R650-2 `drop_keeps_flags` text.
- `an incapable port's receipt watch is not re-armed` deletes the two-line 3000 ms re-arm (`gen_gptp_ucode.py:1703-1704`). This is the R650-2 `held_no_rearm` text.
- Published head arm, shards 16 and 17:
  - The first control fails `#82 Pdelay loss: the drop commit's flags are gmPresent alone` (got 9, expected 1) and its p1-255 twin (got 9, expected 0).
  - The second fails `master in 3 s`, `that mastership names thisClock, {thisClock}` and the p1-255 `master in 3 s`.

**My independent run** (`scripts/probe_r650_2_mutants.sh`, `receipts/probe-r650-2-mutants.txt`, `receipts/probe/`): one engine build from `git archive` of the exact head with the pinned simulator 5.050, both passes per variant.

| variant | default pass | priority1-255 pass |
|---|---|---|
| clean | 1642/1642, rc 0 | 46/46, rc 0 |
| drop_keeps_flags | 1 FAIL: the drop commit's flags (got 9, expected 1), rc 1 | 1 FAIL: the same check (got 9, expected 0), rc 1 |
| held_no_rearm | 3 FAIL: master in 3 s; that mastership names thisClock, {thisClock}; that mastership commit has gmPresent; rc 1 | the same 3 FAIL, rc 1 |

Result: **closed**.

### 2. R650-2-F2: gmPresent in every self publication

**RTL.**
- `hdl/top/KL_gptp_engine.sv:172-175`: `rom_gm_capable_w = cid_img_r[ROM_CID_HI_C][32]`.
- `:1028-1031`: `pub_flags_o = {pub_flags_r[31:1], pub_flags_r[0] | rom_gm_capable_w}`.
- `rom_clock_id_w` still takes only `[31:0]` of each word (`:170-171`), so bit 32 cannot contaminate thisClock or S_CID.
- `st_rd_mux_w` word 2 (`:775`) returns the raw `pub_flags_r`, so µcode decisions are unchanged.
- The asCapable hook (`:938`) and the slew-qualification hook (`:931`) read bits 2 and 3 only.

**Generator.**
- `hdl/ucode/gen_gptp_ucode.py:2199-2201` sets bit 32 when `RUNTIME["p1"] < 255`.
- `:1730-1731`: BECOME no longer ORs FL_PRESENT, so µcode bit 0 means only "a peer is elected".

**Every reader of µcode bit 0.** I checked each reader against the new meaning (master no longer sets PRESENT):
- The Sync and Follow_Up gates (`:794-795`, `:816-817`) want PRESENT|ASCAP with AMGM clear. A master was already excluded by AMGM.
- BECGATE (`:1692-1716`) leaves early on AMGM before testing PRESENT.
- They_win (`:1658`) sets PRESENT on adoption.
- The fall and timeout masks (`:1488`, `:1537`, `:1964`, `:1987`) only preserve bits.
- No reader inferred "master" from PRESENT.

**Conformance.**
- 10.3.13.2.4 g) sets gmPresent from gmPriority's priority1 < 255. gmPriority is never worse than the systemPriorityVector, whose priority1 is 248. So a priority1-248 instance always has gmPresent TRUE, and the constant OR is exact.
- With priority1 255, a self publication carries gmPresent FALSE. This is new and correct for mastership: at base, BECOME set it.
- An elected peer whose own priority1 is 255 still sets it. This is disclosed as a known limit and unchanged from base.

**Grading.** Default pass:
- `cold release: every cycle to the first beat has gmPresent` (`sim_main.cpp:1242`)
- `cold release: that commit's flags are gmPresent alone` (`:1256`)
- `warm reset: its flags are gmPresent alone` (`:4881`)
- `peer leaves: the mastership commit has gmPresent` (`:4909`, the Announce-silence departure)
- `Pdelay loss: the drop commit's flags are gmPresent alone` (`:4971`)
- `Pdelay loss: that mastership commit has gmPresent` (`:5007`)
- phase 3 `master flags`, now `self_present|AMGM|ASCAP`

The priority1-255 pass (`:245-258`) runs boot, the first mastership and phase 36 with the expected value 0.

**Controls.**
- `the published flags leave gmPresent to the microcode`, an RTL mutant: fails all six default checks.
- `the image does not mark thisClock grandmaster-capable`: fails all six.
- `the capability mark ignores priority1`: fails four p1-255 checks.
- `mastership sets the microcode's presence bit`: fails the p1-255 mastership check.
- All are in the published 58/58 arm.

**Against older revisions** (published controls): the head harness fails exactly 4 default checks plus 2 p1-255 checks against `8f3c376d`, and 20 plus 13 against base `b9ade3a6`. This matches the PR body.

**Text.**
- PR body "Known limits" no longer carries the R650-2 sentence. Its gmPresent paragraph matches the RTL.
- `docs/INTEGRATION.md:494-508` adds "Grandmaster presence", and `:534-536` corrects the drop's flags.
- The BECGATE comment (`gen_gptp_ucode.py:1707-1711`) is aligned.

Result: **closed**.

### 3. R650-2-R1

`KL_gptp_engine.sv:708-712` reads: "Every reset loads the self publication, thisClock and {thisClock}, and invalidates the best record below, so only a newly received Announce competes with the local vector (#82);". This is the exact text required. **Closed.**

### 4. No port or parameter change seen by the parent

- `receipts/spot-checks.txt`: the comment-stripped `module KL_gptp_engine … );` header is identical at `8f3c376d` and the head (50 lines, sha256 `23b9be0d…`).
- The author's `receipts/r3/iface/ports-sha256.txt` has four revisions, including e4869fd0 (the parent pin) and 334e9fe6, all `ccf818c7…`.
- The delta adds no port and no parameter. Its RTL hunks are a wire, a comment, and the `pub_flags_o` assign.
- Consumer impact: bit 0 is now constant 1 for a default image. Parent dev e9cbb676 reads only bits 3 and 2. The `gptp_pub_flags_w` consumers are `:2040` and `:2041`; `:7604` is the port binding and `:7675` the plane-off tie-off (`receipts/identity-and-hosted.txt`).
- The parent ROM ledger needs the new digest row. The author's local parent commit adds it (`receipts/r3/parent/pin-commit.diff`, `syn/yosys/rom_digests.tsv`).

### 5. Published author-r3 packet

- `receipts/r3/scripts/verify_receipts.py` reads only the "## In this directory" table. On the published copy it reports 312 files, 312 index rows, 0 mismatches, rc 0 (`receipts/verify-author-r3.txt`).
- The round-2 `receipts/scripts/verify_receipts.py` gives the same result on the same copy (`receipts/verify-author-r3-with-r2-script.txt`). The scratch-only files are now a bullet list under their own headings, outside any table either script parses.
- MANIFEST.json: 313 author-r3 entries, 313 files present, 0 published-hash mismatches, 0 unlisted, 0 missing (`receipts/manifest-json-author-r3.txt`).
- No `/home`, `/srv`, `/data` or `/mnt` prefix remains anywhere in author-r3.

**Round-3 gate receipts** (all at `gates/head/HEAD` = 334e9fe6, `gates/base/HEAD` = b9ade3a6):
- Every head `.rc` is 0: contract, lint, docs, ucpu, parser, engine, 18 engine-mutant shards, gaskets, tsngen, bench, clean.
- Engine: 1642/1642 on three images, plus 46/46 for the priority1-255 pass. The arm has 58 controls caught, 25 of them naming #82 checks.

**Parent consumer gates**, at local parent `c7c60bae` (dev e9cbb676 plus two never-pushed commits, gitlink 334e9fe6, push remote disabled):
- rc 0: gptp_shadow 309, lifecycle, gptp_shadow-mutants (controls 9, failures 0), gptp_tables 36 (controls 26, failures 0), gptp_txts and its mutants, gptp_plane run and phc-step, gmstep, `milan_dp` `gptp` 182/182 and `gptp-lat` 182/182, lint_rtl, port_contracts and selftest, wire_acc, docs, builder clock contract, yosys-ci3, ooc-tcam, tsn_fuzz-ptp.
- rc 2: `milan_dp-gptp-dev-tests`, dev's unmodified test, at 179/182. The 3 failures assert GM 0 before any peer and a CLKV mask without the discontinuity holdover, which is exactly the boot state #82 removes. The PR body discloses this and keeps "Refs #82" for that reason.

**Other checks.**
- R651-2-F1: closed (see the prior-findings table).
- My regeneration of all four committed ROM copies from the head generator, each with its own Makefile arguments, matches byte for byte. Word 1022 is `000102A1B2FF` (default) and `000002A1B2FF` (priority1 255). The image uses 1013 of 1024 words, as the PR says.

## Findings

### R650-3-R1 - RESIDUE - Docs - the reset section states the flags value unconditionally

- **Where:** `docs/INTEGRATION.md:480`: "Flags carry gmPresent alone."
- **Evidence:** in an image with priority1 255, reset publishes flags `0x0` (graded: `p1 255 #82 cold release: that commit's flags are gmPresent alone`, expected 0). The same page states this correctly at `:508`. Only this sentence omits the condition.
- **Impact:** wording only. It changes no measurement, test, code or conformance claim.
- **Exact fix:** replace it with "Flags carry gmPresent alone, or nothing with priority1 255."

### R650-3-S1 - SUGGESTION - Conformance, Tests - restored capability could grant mastership at once, not after the running receipt watch

- **Where:**
  - `gen_gptp_ucode.py:1703-1704` (BECGATE re-arm while incapable) and `_pdpost_verdict` `:1951-1958` (the asCapable rise).
  - `sim_main.cpp:5002-5003`: a 3 s bound.
- **Authority:** in 802.1AS-2020 10.3.12, the DISABLED state exits to AGED as soon as the port is enabled and asCapable. AGED sets reselect, so updtStatesTree selects MasterPort when no port holds better information, without waiting for announceReceiptTimeout.
- **Context:** the round-3 assignment set "within one receipt interval", following my R650-2-F1 text. That text cited the receipt-timeout aging path, which applies to received information that times out, not to a disabled port becoming capable again. The head meets the assigned bound: 1.0 s observed, 3 s at most.
  - GM and path are thisClock and {thisClock} throughout.
  - Only the master bit and the start of Sync/Announce transmission lag.
  - This behaviour was introduced in round 2, and the delta does not change it, so it does not reopen acceptance.
- **Suggestion:** on the rise, with no peer elected, arm slot 2 with delta 1, as the fall hook does, so that BECGATE runs BECOME at once. Then tighten the check to a few milliseconds, or record a follow-up issue.

### R650-3-S2 - SUGGESTION - Tests - assert the phase-36 preconditions directly

- **Where:** `sim_main.cpp:4956-4972` and `:4985-5008`.
- **Evidence:**
  - "Sync-ok is set at the fall" appears only in an INFO line. It is enforced indirectly: the arm requires `drop_keeps_flags` to fail the default-pass drop check, and that check fails only when sync-ok was set (0x9 against 0x1).
  - Likewise, `master in 3 s` would pass vacuously if the asCapable rise and the mastership ever shared one commit (`rose == master`). The held control still guards the presence of mastership.
- **Suggestion:**
  - Add `expect("#82 Pdelay loss: sync-ok is set at the fall", fell ? fell->flags & FL_SYNCOK : 0, FL_SYNCOK)`.
  - Require `rose != master`.
  - The PR table's "sync-ok is set at the fall" would then name a real check.

### R650-3-S3 - SUGGESTION - Tests, Docs - state exactly which phases the priority1-255 pass covers

- **Where:** PR body, "Round 3": "each is graded with planted controls in both the default and the priority1-255 images".
- **Evidence:** the p1-255 pass runs boot, the first mastership and phase 36 (`sim_main.cpp:245-258`). It does not run the warm reset or phase 35's departure of an elected peer through Announce silence. Its mastership checks do grade the same BECOME publication, reached through Announce silence. The source header comment (`:161-165`) is already exact.
- **Suggestion:** mirror the header in the PR text: "the priority1-255 pass grades the cold release, the asCapable drop and the Announce-silence mastership".

### R650-3-S4 - SUGGESTION - RTL - the bench presence LED is now steadily lit

- **Where:** `bench/arty/bench_arty_top.sv:344`: `led_o[3] = pub_flags_w[0]`.
- **Evidence:** for any image with priority1 below 255, bit 0 is now constant 1, so the LED no longer shows "a peer is elected or this plane is master". No document claims a meaning for this LED. The UART label "bit0 gm_present" (`bench_uart_report.sv:16`) stays accurate.
- **Suggestion:** if a visual election indicator is wanted, drive the LED from the master bit or a GM-differs-from-thisClock comparison, or note the change in the bench comment.

### R650-3-S5 - SUGGESTION - evidence provenance (manager) - MANIFEST.json does not record the pre-redaction digests for author-r2 or author-r3

- **Where:** `review-evidence/gptp82-r1/MANIFEST.json` at `6f640b75`.
- **Evidence:**
  - All 313 author-r3 entries (and all 132 author-r2 entries) have `path_redacted: false` and `original_sha256 == published_sha256`.
  - Yet about 50 author-r3 files contain the manager's placeholders (`<home>`, `<data>`, `<slots>`, `<host>`), and the RECEIPTS.md header says the manager redacted and re-hashed them.
  - The round-1 `author/` and the review directories do record `path_redacted: true` with distinct digests.
  - Verification of the published copy is unaffected.
- **Suggestion:** record the author's pre-redaction digests and `path_redacted: true` for the files changed, or document that author-rN entries are post-redaction.

### Retained suggestions (unchanged code; the author did not take them this round)

- **R650-2-S1:** the parser's loop check still waits for the init leg on a cold start (`KL_gptp_engine.sv:157`, `:186`, `:857-860`). thisClock is known from reset (`rom_clock_id_w`).
- **R650-2-S2:** the asCapable hook (`:938-942`) shares the timer-arm registers with the hardware boot arms (`:869-877`). This is unreachable today. A comment or a simulation assertion that the hook never fires while `!boot_done_r` would make that explicit.
- **R651-2-S2:** the configuration example `docs/INTEGRATION.md:552` uses `--mac 02:a1:b2:c3:d4:e5`, which the parser rejects. The fix is `--mac 0x02A1B2C3D4E5`.

## Prior public findings: resolved or retained at this head

| Finding | Status | Cause-level evidence at 334e9fe6 |
|---|---|---|
| R650-2-F1, drop flags and regain path ungraded | **Closed** | Phase 36 takes the fall at flags 0x9 and grades the drop word exactly. Regain mastership is graded. Both controls fail by name in the published arm (shards 16 and 17) and in my run (`receipts/probe/`). |
| R650-2-F2, gmPresent filed as an unchanged limit | **Closed (conformed)** | `pub_flags_o` bit 0 is µcode bit 0 OR the ROM capability bit. Six default and four p1-255 checks, with four controls. PR "Known limits" and INTEGRATION corrected. |
| R650-2-R1, best-record comment | **Closed** | `KL_gptp_engine.sv:708-712` has the exact text. |
| R650-2-S1, S2 | Retained as suggestions | Code unchanged (see above). |
| R651-2-F1, verifier fails on the redacted scratch rows | **Closed on author-r3** | Both verifier versions pass on the published copy: 312/312, rc 0. The scratch files sit outside the verified table, in non-table form. |
| R651-2-S1, base ROM-layout helper | Closed | `receipts/r3/rom/layout-base.txt` completes; the round-2 copy keeps its historical traceback. |
| R651-2-S2, configuration example | Retained as a suggestion | `docs/INTEGRATION.md:552` unchanged. |
| R650-1-* and R651-1-*, closed in round 2 | Remain closed | The delta touches none of their causes. The cold, warm and departure checks and their controls still pass and fail as required in the round-3 head arm. |

## Lens summaries

**Conformance: CLEAN.**
- gmPresent now follows 10.3.13.2.4 g) for every self publication: reset (cold and warm), the asCapable drop (10.3.12 DISABLED), the Announce-silence departure (AGED), and mastership.
- With priority1 255, self publications clear it.
- Each departure still publishes thisClock and {thisClock} (b, i).
- The restored-capability latency is within the assigned bound. The stricter reading of the clause is recorded as S1.
- Limit: the clause text was not re-read in this session. The citations agree with the issue's numbering and the assignment's ruling.

**RTL: CLEAN.**
- The delta is one wire from a configuration-time ROM bit and one OR on an output assign.
- No port or parameter change. µcode reads stay raw. Bit 32 is isolated from thisClock. The output is stable across commits.
- Lint rc 0. The parent's yosys-ci3 and ooc-tcam are rc 0 with the gitlink at this head.
- Bench side effect recorded as S4.

**Robustness: CLEAN.**
- Every µcode reader of PRESENT was re-audited against its new meaning; none depended on master implying PRESENT.
- The fourth pass writes only to a gitignored `p1run/`, and `make clean` removes it.
- The arm builds both images from each mutated generator, merges the tallies, and turns an aborted pass into an abort verdict rather than a catch. A p1-prefixed check can be satisfied only by p1 output, and a default check only by default output (`failing()`).

**Tests: CLEAN.**
- 1642 checks on each of three images, plus 46 in the priority1-255 pass. 58/58 controls, 25 naming #82 checks, confirmed in the published arm.
- My exact-head run reproduces the clean tallies and both R650-2 controls.
- Harness-on-old-revision controls: 4+2 against round 2, 20+13 against base.
- Suggestions S2 and S3.

**Docs: CLEAN.**
- INTEGRATION, HDL_DEVELOPER and TEST_DEVELOPER describe the new bit, its ROM mark and its scope.
- All re-pointed SOURCE_EVIDENCE anchors land on the named constructs (`:177`, `:257`, `:369`, `:375`, `:411`, `:431`, `:458`, `:993`, `:998`, `gen:890`).
- The PR body matches the packet draft.
- No new source comment shows lane labels, lane names, rounds, reviewer IDs or comment IDs.
- One RESIDUE (R1).

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_gptp_engine.sv:160-175, 700-712, 920-945, 1025-1031`; `gen_gptp_ucode.py` BECGATE, BECOME, the flags readers, `build()` ROM marks; 10.3.13.2.4 b/g/i and 10.3.12 against them; PR "Known limits" | R650-3 | 334e9fe64dfff5568be58a0dc9aeb302959b3b58 |
| RTL | CLEAN | RTL delta; header comparison with 8f3c376d; four-revision port digests; regenerated ROM copies; parent flags consumers at e9cbb676; lint, yosys-ci3 and ooc receipts | R650-3 | 334e9fe64dfff5568be58a0dc9aeb302959b3b58 |
| Robustness | CLEAN | every µcode PRESENT reader; `mutants.py` stage, run_harness and failing(); Makefile fourth pass and clean; `.gitignore` | R650-3 | 334e9fe64dfff5568be58a0dc9aeb302959b3b58 |
| Tests | CLEAN | `sim_main.cpp` phase 36, the boot and warm-reset checks, the p1 pass; the 58-control head arm; controls against older revisions; my clean and two-control run at the exact head; parent consumer gate receipts | R650-3 | 334e9fe64dfff5568be58a0dc9aeb302959b3b58 |
| Docs | CLEAN (RESIDUE R1 carried) | INTEGRATION, HDL_DEVELOPER, TEST_DEVELOPER and SOURCE_EVIDENCE deltas and anchors; PR body and packet draft; comment-rule scan of the added source lines | R650-3 | 334e9fe64dfff5568be58a0dc9aeb302959b3b58 |

## Reviewer execution (exact head, scratch copies only)

- `scripts/spot_checks.sh` regenerates the ROM images, prints word 1022 for both images, and compares the module header (`receipts/spot-checks.txt`).
- `scripts/probe_r650_2_mutants.sh` builds once from `git archive` of the head with the pinned simulator 5.050 (identity printed in `receipts/identity-and-hosted.txt`). It runs clean, drop_keeps_flags and held_no_rearm, each in the default and priority1-255 passes, six runs in parallel, about 48 s of wall time (`receipts/probe-r650-2-mutants.txt`, `receipts/probe/`).
- I ran both published verifiers, with isolated interpreters, from outside the evidence directory, on a sparse checkout of `6f640b75` (`receipts/verify-author-r3*.txt`), plus a MANIFEST.json check (`receipts/manifest-json-author-r3.txt`).
- Clone integrity after all work (`receipts/clone-integrity.txt`):
  - HEAD and index tree are both `fdb142e8…`.
  - The worktree equals HEAD.
  - `git status --porcelain --ignored` is empty.
  - This repository tracks no gitlinks.
  - No probe wrote into the clone.

## Real limits

- No manager source bank runs at this exact head. Source-head execution evidence is the author's published gate receipts plus my focused engine run. I do not claim or infer a manager bank.
- Hosted CI: 0 check runs and 0 statuses at 334e9fe6, so there is no hosted evidence. The manager owns hosted and act acceptance.
- I did not re-run the full repository gates, the full mutation arm, or the parent consumer gates. I relied on the published receipts after verifying the packet.
- Not run by the author: the nightly physical gPTP job. By the author's own reading, its mid-run reset check needs the same update. Also not run: the full `milan_dp` sweep and the media-clock suites.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- I did not re-read the 802.1AS-2020 clause text in this session (see the Conformance lens).

## Pending manager duties

- At the merge turn, build and validate the current-dev merge candidate (builder and native banks; source base b9ade3a6, live dev e9cbb676) and link its receipts.
- The parent pin bump must carry:
  - the `milan_dp` gptp and gptp-lat test update, and the dev-test expectations of GM 0 at boot;
  - the eight docs re-points and the ROM-ledger row for 334e9fe6;
  - the nightly physical job's mid-run-reset expectation.
  Until then, #82's parent done-condition is not met, which is why the PR says "Refs".
- Carry R650-3-R1 to the residue checklist.
- Decide on S1 (immediate mastership on restored capability) as a follow-up, and on S5 (MANIFEST.json provenance for author-rN).
- Hosted and act acceptance at the merge candidate.

R650-3 FINISHED
