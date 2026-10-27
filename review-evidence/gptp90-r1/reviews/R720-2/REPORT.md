[R720] POSITIVE - exact head 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e

# R720-2 external independent review: FPGA-gPTP PR #92 (issues #89, #90, #91)

- Head `4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e`, tree `f7731898626419ec3bdb9a025077c39992d00b75`. Source base main `55680bff`. Previously reviewed head `d27a1654` (R719-1 and R720-1).
- Scope was rebuilt from public sources:
  - the issue bodies of #89, #90 and #91;
  - the assignments on #90 (6434675577) and #89 (6434676256), with their scope merge;
  - the round-2 assignment on #90 (6442857175);
  - the PR #92 body at this head;
  - `git diff 55680bff..4d8fb902`, and the round-2 delta `d27a1654..4d8fb902` (three commits);
  - the public evidence packet, milan-fpga `004088f6` `review-evidence/gptp90-r1` (author-r2).
- Token-economy rule: code the delta does not touch keeps its R720-1 lens verdict. The delta itself was judged from scratch, and so was every prior finding, at its cause. My independent pass over the delta was finished before I read the R719-1 and R720-1 findings.
- Verdict: no open BLOCKER, MAJOR or MINOR finding, so the verdict is POSITIVE. Two RESIDUE items and three SUGGESTIONs are listed below. Every prior MINOR finding is resolved at this head.

## What the round-2 delta does (verified)

- **`prog_leg_srto`** (`hdl/ucode/gen_gptp_ucode.py:2138-2170`). Every slot-4 expiry writes `SRTO_PASSED_C` (`0xFF<<16`, `:504`) to scratch 46, whatever the role.
  - It then branches to BECGATE only when `((flags & PRESENT) - PRESENT) | (S_BESTPV >> 40)` compares below `SRTO_PASSED_C`.
  - The microCPU's CMP is a 32-bit unsigned compare (`hdl/ucpu/KL_gptp_ucpu.sv:200-204`). With no elected peer, the low word is `0xFFFFFFFF`, which never compares below. With an elected peer, the value is `{p1, clockClass, clockAccuracy}`, which is below `0xFF0000` exactly when p1 < 255.
  - So the leg ages exactly an elected peer whose grandmaster gives gmPresent, and only marks a master or a port of a priority1 255 grandmaster.
- **`prog_rx_announce`** (`:1091-1101`). The aged check now sits after qualifyAnnounce, so an unqualified Announce reaches nothing.
  - It compares the Announce's `{p1, class, accuracy}` (`bank8 << 16 >> 40`) against the cell. With the cell at 0, nothing compares below it. With the mark set, a p1 < 255 Announce goes to BECGATE, which keeps or makes the plane master, and a p1 = 255 Announce goes on to BTCA.
  - This matches Figure 10-13 (Cor1): the updated information becomes CURRENT, and it ages at once when syncReceiptTimeoutTime has passed and the new gmPresent is TRUE.
- **`prog_become`** (`:1885-1888`) no longer disarms timer slots 4 and 5. FUTO (`:2172-2177`) only voids `S_SYNCTS`, so a master keeps its sync-ok (#84).
  - The master-role Follow_Up pairing (`:915-936`) still needs `S_SYNCTS`. So a Follow_Up later than 125 ms pairs with nothing in either role (11.2.13).
- **`prog_rx_sync`** (`:868-873`). The asCapable gate is rewritten inline (AND, CMP 0, BRS_Z out). For the single-bit mask this is equivalent to `e_flag_gate(FL_ASCAP_C, FL_ASCAP_C)` (`:739-746`), and it saves one word.
- **Mark lifecycle.** The mark is cleared by SRWATCH (`:1048`) and by the asCapable rise (`:2115`). No other writer exists (`grep S_SRTO`).
- **Images and ROM.** All four tracked images regenerate byte-identically with each consumer's own arguments (`receipts/regen/regen-compare.txt`).
  - Shipping images use 1,021 of 1,024 words. The seeded images (`--seq-seed`, `--sync-seq-seed`) use 1,022, and the `--p1 255` image uses 1,021. `FUTO@254`.
  - These figures match `docs/MANAGER.md:103-117` and the PR body.
- **Boundary.** No `.sv`, Makefile, port, parameter or register-map change. The repository has no submodule gitlinks.

## Findings

### R1: RESIDUE. "ages" should be "marks" for a master-role expiry
- **Lenses:** Docs.
- **Where:** `docs/INTEGRATION.md:607`, "So an expiry found in the master role ages too."
- **Authority/evidence:**
  - A master-role expiry has no received information to age. `prog_leg_srto` only marks the port (`gen_gptp_ucode.py:2138-2170`).
  - The PR body ("A master is only marked") and `docs/HDL_DEVELOPER.md` ("Every expiry marks the port aged") say so.
- **Impact:** wording only. The lines that follow describe the behaviour correctly, and no figure, test or claim changes.
- **Exact fix:** "So an expiry found in the master role marks the port aged too."
- **Verification:** `make docs` rc 0.

### R2: RESIDUE. A reflow left one 97-column comment line
- **Lenses:** Tests (comment formatting only).
- **Where:** `tb/verilator/engine/sim_main.cpp:5525`, "// its adoption can start the watch. Then GMS's Sync fails in each shape of the issue while its".
- **Impact:** formatting of a comment only. No code or check changes.
- **Exact fix:** rewrap the phase-39 comment block (lines 5523-5530) to the file's 80-column comment width.
- **Verification:** `awk 'length>90' tb/verilator/engine/sim_main.cpp` no longer prints line 5525, and the engine suite still builds.

### S1: SUGGESTION. The gmPresent boundary at priority1 254 is unchecked
- **Lenses:** Tests.
- **Where:** `hdl/ucode/gen_gptp_ucode.py:504` (`SRTO_PASSED_C = 0xFF << 16`). Phase 41 (`sim_main.cpp`, `age_only_while_a_grandmaster_is_present`) uses only priority1 1 and 255.
- **Evidence:** reviewer probe OWN2 (`receipts/mutants/OWN2_the_gmPresent_threshold_is_priority1_254.txt`) moves the threshold to `0xFE << 16`, so a priority1 254 grandmaster is treated as gmPresent FALSE. It survives the whole suite: 1,862/1,862, the shipping pass plus the priority1 255 pass.
  - The code is correct by inspection, so this is a gap in test strength, not a defect.
- **Suggestion:** add one priority1 254 Announce on the aged port to phase 41, expecting it to be aged, so the boundary has a control.

### S2: SUGGESTION. The rewritten Sync asCapable gate has no control or recorded reason
- **Lenses:** Tests.
- **Where:** `hdl/ucode/gen_gptp_ucode.py:868-873`.
- **Evidence:** reviewer probe OWN4 deletes the gate's branch, so Sync is parked on an incapable port. It survives (1,862/1,862, `receipts/mutants/OWN4_a_Sync_is_taken_on_an_incapable_port.txt`).
  - By inspection the gate is defence in depth. The Follow_Up handler's role gate (`:899-906`) admits only asCapable roles, so an incapable port pairs nothing.
- **Suggestion:** record it beside the "lapse hook's asCapable term" note in `tb/verilator/engine/mutants.py:38`, as that file does for other unreachable arms.

### S3: SUGGESTION (retained from R720-1 F3). No shape has a second responder sending its own Follow_Up
- **Lenses:** Tests.
- **Where:** the harness `PD_DUAL` shape. Unchanged by the round-2 delta.
- **Status:** still open as a suggestion. The behaviour is correct by inspection, as recorded at R720-1.

## Prior public findings at this head

| Finding | Status | Evidence at this head |
|---|---|---|
| R720-1 F1 (MINOR): Sync ageing ignores gmPresent | **Resolved** | The SRTO leg compares the elected vector against `SRTO_PASSED_C`, and the Announce path asks the same question (see above). Named phase-41 checks exist. Controls "sync receipt ageing ignores gmPresent", "an aged port refuses a priority1 255 grandmaster" and "an aged Announce is dropped rather than aged" are each caught here on their named checks (`receipts/mutants/summary.tsv`). The author's unchanged rerun of my p255 probe at this head stays slave (`flags=5`, gm `…0101`) for all 6 s, against `flags=e` at `d27a1654`. |
| R720-1 F2 (RESIDUE): dangling "it" | **Resolved** | `docs/TEST_DEVELOPER.md` now reads "Clears sync-ok on every handover to a peer." |
| R720-1 F3 (SUGGESTION) | Retained as S3 | Not verdict-bearing. |
| R719-1 F1 (MINOR): a master-role expiry is forgotten | **Resolved** | Every expiry marks the port. Phase 40 has the named check "#89 a lone pair heard as master: a later Announce elects nothing" plus its control "…inside its watch elects". The control "only an expiry that ages a slave marks the port" is caught here on all three named checks. The author's unchanged rerun of the R719-1 probe at this head gives 0 of 3 late re-elections, and the control round still re-elects (124 ms). |
| R719-1 F2 (MINOR): BECOME drops the parked Sync's Follow_Up watch | **Resolved** | BECOME keeps slots 4 and 5. Controls "mastership stops the Follow_Up watch", "mastership voids the parked Sync" and "mastership stops the Sync receipt watch" are caught here on their named phase-40 checks. The probe's parked line now reads `elected_by_next_announce=0`. |
| R719-1 F3 (MINOR): parent docs keep the retired counts and a stale figure | **Resolved in the companion patch** | Patch sha256 `b53944d52a51323b267b0a91dbfd6bd1aeaabcacf26d31b246b19318d56a1b7a`, verified against the published `.sha256`. It changes `GPTP_PLANE.md` fourth→fifth and third→fourth, and both `TESTING.md` and `milan_dp/README.md` to 17.992742740 s / 899,637,137 cycles. That is exactly the patched head run's `simulated_duration_seconds` line (`consumer-head/final-b/01.log`). Landing it remains a merge-turn duty. |
| R719-1 R1 (RESIDUE) | **Resolved** | Same fix as R720-1 F2. |
| R719-1 S1 (gmPresent) | Superseded | Fixed through R720-1 F1. |
| R719-1 S2, S3 (other reviewer's suggestions) | Still applicable as suggestions | The delta does not change them: the wrong-sequenceId reset in WAITING_FOR_PDELAY_RESP, and the own-port Sync filter while master. Not verdict-bearing. |

No PR reviews or line comments exist (`pulls/92/reviews` and `pulls/92/comments` both return 0).

## Lens evidence

- **Conformance.**
  - The delta was walked against 802.1AS-2011 + Cor1/Cor2:
    - 10.3.11 / Figure 10-13: CURRENT→AGED on `currentTime >= syncReceiptTimeoutTime && gmPresent`;
    - Figure 10-4 (Cor1, no parent condition), so any Sync on an asCapable port moves the time and nothing else does;
    - gmPresent TRUE iff the grandmaster's priority1 < 255 (10.2.3.13, 10.3.12.1.4 g);
    - 11.2.13 followUpReceiptTimeout.
  - Each round-2 assignment item, 1-3 and 5-6, is met. Item 4 is met in the patch (see the prior-findings table).
  - The #90 and #91 legs are untouched by the delta and keep their R720-1 verdict. Their controls are caught again here: fourth, sixth, first, re-arm and third-response.
- **RTL (microcode).**
  - The compare semantics come from `KL_gptp_ucpu.sv:197-205` (32-bit unsigned, `sub_w[32]`), and the 64-bit logical SHR from the alu64 datapath.
  - Bit placement was checked: `bank8 = {utc16, p1, cq32, p2}` gives, after `<<16`, p1 at bits 63:56, and `>>40` gives `{p1, class, acc}`. `S_BESTPV` uses the same layout.
  - The inline Sync gate is equivalent to the macro it replaces. Timer slots 4/5 and the FUTO leg are safe in the master role. Images regenerate identically, and the ROM figures were verified.
- **Robustness.**
  - The mark's writers and readers were enumerated: set by SRTO; cleared by SRWATCH and the asCapable rise; read by the Announce path.
  - An expiry while incapable sets the mark, which the rise clears.
  - Master-role sync-ok is preserved: FUTO touches only `S_SYNCTS`.
  - The no-oscillation behaviour is bounded to one election per usable pair that the next Announce falls inside.
  - A priority1 255 domain without Sync is never aged.
  - My own controls OWN1 (the rise keeps the mark) and OWN3 (a master pair keeps the mark) are both caught.
- **Tests.**
  - The engine suite was re-executed at this head with pinned Verilator 5.050 (wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`): 1,805/1,805 on each of the three image passes and 57/57 on the priority1 255 pass, rc 0 (`receipts/engine-run.log`). The base receipt shows 1,703 and 53, matching the PR body.
  - The receipt-rule arm (26 controls, including all 7 round-2 additions) was re-executed in parallel through the tree's own `run_mutant()`. The unmutated control passes, and 26/26 are caught, each on every check it names (`receipts/mutants/summary.tsv`).
  - The arm totals 98 controls with no duplicate names (91 at `d27a1654`). The full 98-control arm rests on the author receipt `repo-gates-head/04b-engine-mutants` rc 0.
  - Earlier R720-1 probes R3 and R7 now report NOT-CAUGHT in the author's rerun. Their patterns target code the delta removed. R3 is re-planted against the new leg as R3' and caught, and my OWN1/OWN3 cover the same properties.
  - The phase-40 and phase-41 timing arithmetic was checked against the 2 MHz harness clock: 339 ms park, takeover 36 ms later, Follow_Up at 200 ms and 60 ms, Announce 624 ms and 124 ms after the pair. The `-1` sentinel fails both expectations.
- **Docs.**
  - The delta was read in HDL_DEVELOPER, INTEGRATION, MANAGER, SOURCE_EVIDENCE and TEST_DEVELOPER, in the generator header and comments, and in the PR body.
  - The figures in MANAGER (1,021 words, three free, `FUTO@254`) match the packer.
  - The SOURCE_EVIDENCE `#L984` anchor resolves to `def prog_leg_slew`.
  - Comment rule: added lines in the delta carry no lane labels, lane names, review rounds, reviewer IDs or comment IDs (grep over `git diff 55680bff..HEAD` added lines).
  - Only R1 and R2 remain.

## Ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 10.3.11/Fig 10-13, Fig 10-4 (Cor1), 10.2.3.13/10.3.12.1.4 g, 11.2.13, 11.2.15.3/Fig 11-8; legs SRTO, RX Announce/Sync/Follow_Up, BECOME, BECGATE, SRWATCH, FUTO, PDPAIR rise; companion patch | R720-2 | 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e |
| RTL | CLEAN | Generator delta; µCPU CMP/SHR semantics; four images regenerated identical; ROM 1,021/1,022; no HDL or port change | R720-2 (HDL unchanged since R720-1) | 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e |
| Robustness | CLEAN | Aged-mark lifecycle, master-role watches, sync-ok in the master role, p1 255 domain, OWN1/OWN3 controls | R720-2 | 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e |
| Tests | CLEAN (R2 residue; S1-S3 suggestions) | sim_main.cpp phases 21/27/39/40/41 delta; receipt_mutants.py; engine suite re-run; 26 receipt controls re-run; 4 reviewer controls; author reruns of R719-1/R720-1 probes | R720-2 | 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e |
| Docs | CLEAN (R1 residue) | Five guides, generator docstrings/comments, PR body, comment-rule scan, companion patch doc hunks | R720-2 | 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e |

## Execution evidence and integrity

- **Evidence packet.** milan-fpga `004088f6` `review-evidence/gptp90-r1` has 454 manifest entries. All of them match their `published_sha256`, with no missing or unlisted files and 2 path-redacted entries (`receipts/evidence-manifest-verify.txt`).
  - Neither the packet commit nor the head commit carries a cryptographic signature (GitHub verification `unsigned`). Integrity rests on the manifest hashes.
- **Author gates at this head.** `repo-gates-head/DONE.json` records rc 0 for all 13 gates: contract, ucpu, parser, engine run, engine mutants, gaskets, tsngen, bench test, lint, docs, diagrams-check, OOC self-test and `make`. Every record has `head_unchanged: true`.
- **Parent consumer gates.** The consumer receipts (`consumer-head/final-a|b|c`) are rc 0 on parent snapshot `b42a52a2` with gitlink `4d8fb902`. They are author receipts and were not re-executed here.
- **Hosted evidence.** None exists at this head: the combined status is `pending` with 0 contexts and 0 check runs, and the repository has no workflow. No hosted job executed, and none was skipped.
- **Clone.** The clone matches the exact head after all probes:
  - tree and index tree are both `f7731898…`;
  - `status --ignored` is empty, and `diff-index` and `diff` are both rc 0;
  - there are no gitlinks (`receipts/clone-integrity.txt`).
  - All probes ran in a disposable `git archive` copy under `scratch/`.

## Real limits

- The normative texts of 802.1AS-2011, Cor1/Cor2 and Milan v1.2 were not available in this session. Clause content comes from the issue and assignment text and from the cited clause structure.
- Physical calibration was NOT RUN, and nothing ran on hardware. This is simulation only, and field skips are not hardware proof.
- Not re-executed here, so these rest on author receipts:
  - the full 98-control mutation arm (I re-ran the 26 receipt-rule controls);
  - the parser, gasket, tsngen and bench suites;
  - `make`;
  - every parent consumer gate (milan_dp `gptp`/`gptp-lat`, `milan_dp_gptp`, gptp_plane, gm_steps, idiom gates, builder, tsn_fuzz `ptp`).
- No manager source bank runs at this exact head, and none is claimed.

## Pending manager duties

- Merge-turn current-dev candidate on live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`: builder and native banks, and the parent consumer list including the `milan_dp` `gptp`/`gptp-lat` legs, with the companion patch `b53944d5…` and the donor deep-link pin updates at the gitlink bump.
- Hosted/act acceptance.
- Carry R1 and R2 to the residue checklist.
- #89, #90 and #91 stay open until the parent companion lands, as the PR body states.

## Receipts (listed in MANIFEST.sha256)

- `receipts/engine-run.log` (the home-directory prefix of the tool path is redacted to `<home>`), `engine-run.rc`, `verilator-identity.txt`.
- `receipts/mutants/` (summary.tsv plus one verdict file per control), `mutants-probe.log`, `mutants-probe.rc`.
- `receipts/regen/` (regen-compare.txt plus generator logs), `evidence-manifest-verify.txt`, `clone-integrity.txt`.
- `scripts/probe_mutants.py` (parallel driver plus OWN1-OWN4), `scripts/verify_evidence_manifest.py`.

R720-2 FINISHED
