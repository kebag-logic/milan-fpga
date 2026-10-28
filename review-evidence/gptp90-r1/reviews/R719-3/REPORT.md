[R719] POSITIVE - exact head 42f9541e1d80e3d888cee1d16f19e01c0027f1cf

# R719-3 independent review: FPGA-gPTP PR #92 (issues #89, #90, #91)

- **Under review:** Mister-M-alt/FPGA-gPTP PR #92.
  - Head `42f9541e1d80e3d888cee1d16f19e01c0027f1cf`, tree `04516ca122525b64eaa414c03d73999dd401a02a`.
  - Source base: main `55680bff`.
  - Previously reviewed head: `4d8fb902` (R719-2 NEGATIVE, R720-2 POSITIVE).
- **Role:** internal independent reviewer, cleared context, round R719-3. Lenses: Conformance, RTL, Robustness, Tests, Docs.
- **Scope, rebuilt from public sources:**
  - the issue bodies of #89, #90 and #91;
  - the round-1 assignments and scope merge (#89 issuecomment-6434676256 and -6434679304; #90 -6434675577 and -6434679552);
  - the round-2 assignment (#90 -6442857175);
  - the round-3 assignment (#90 -6449128848): option (a) of R719-2 F1, a named phase-42 check with a planted control, R719-2's probe run unchanged, and R719-2 R1 plus R720-2 R1/R2 applied;
  - the PR body at this head;
  - `git diff 55680bff..42f9541e` and the delta since the last review, `4d8fb902..42f9541e` (three commits: e81885b, cfb2f4f, 42f9541);
  - the public author evidence at milan-fpga `8480ed96` `review-evidence/gptp90-r1/author-r3`.
- **Process inputs:** this repository has no AGENTS.md or CONTRIBUTING.md. I used README.md, docs/README.md (truth order: RTL and generated microcode, then tests, then guides) and the four role guides.
- **Token-economy rule:** code the delta does not touch keeps its R719-2 lens verdict. That verdict was clean apart from F1 and R1, which are resolved below. I judged the delta from scratch. I wrote my own verdict and ledger draft (`receipts/own-verdict-written-at.txt`, 2026-10-28T05:03:17Z) before reading any prior review. After that I resolved every prior item at its cause.

## Verdict

POSITIVE. The delta has no open BLOCKER, MAJOR or MINOR finding. The one MINOR from the previous round (R719-2 F1) is resolved at this head. This report lists one RESIDUE item and four SUGGESTIONs. None of them affects the verdict.

## What the delta does (own reading)

- **`prog_leg_srto`** (`hdl/ucode/gen_gptp_ucode.py:2158-2195`). The leg is still 11 words and still has no branch for the new case.
  - **Mark.** It writes the mark `SRTO_PASSED_C = 0xFF << 3` (`:507`) to scratch 46 on every expiry.
  - **Threshold.** It computes `RV = (flags & FL_PRESENT_C) * SRTO_PASSED_C` with `MD MULS`. That is the mark for an elected peer and zero otherwise.
  - **Compare.** It tests the elected vector's bits 63:53, which hold priority1 and clockClass[7:5].
  - **Ageing.** A vector below the threshold branches to BECGATE. That happens exactly when a peer is elected with gmPresent TRUE.
  - **Otherwise.** `MASK RT, R0, RV` computes `flags & ~RV`, and the leg jumps to `PUBFLAGS`. `PUBFLAGS` is PDPAIR's flags write, followed by `COMMIT` and `END`.
- **Announce path** (`:1112`). The aged-Announce compare uses the same 53-bit shift.
- **Assembler.** `Prog.address()` (`:680-689`) and the `LB["PUBFLAGS"]` placeholder resolve the shared tail. The placeholder is filled before pass 2 (`:2360`, `:2394`).
- **Harness.** Phase 42 (`tb/verilator/engine/sim_main.cpp:5757-5799`) runs in the priority1 255 pass. Phase 19's check becomes "#84 takeover: the queued receipt timeout commits after it" (`:3980`).
- **Mutation arm.** Two new controls and one replacement are in `receipt_mutants.py`. Patterns in the existing controls were updated for the rewritten leg.
- **Docs.** The delta touches `HDL_DEVELOPER.md`, `INTEGRATION.md`, `SOURCE_EVIDENCE.md` and `TEST_DEVELOPER.md`.

## Lens evidence (delta)

### Conformance

- **Ageing condition (802.1AS-2011 10.3.11, Figure 10-13 as corrected by Cor1):** CURRENT goes to AGED on `syncReceiptTimeoutTime && gmPresent`. gmPresent is TRUE only when the grandmaster's priority1 is below 255 (10.2.3.13; 10.3.12.1.4 g).
  - I checked the new 11-bit compare exhaustively over all 65,536 (priority1, clockClass) pairs. "Aged" equals "priority1 < 255" in every case, with 0 mismatches (`receipts/pubflags-target.txt`, `scripts/check_pubflags_target.py`).
- **gmPresent FALSE:** the clause ages nothing, and the leg keeps the peer elected.
  - Clearing sync-ok is an implementation verdict, not a variable of the standard. The round-3 assignment asks for it (option (a)).
  - Main's rule did the same for every expiry outside mastership.
  - It does not conflict with the figure.
- **Master role:** the port is marked, and sync-ok is kept (#84).
- **Unchanged by the delta:** #90 (fifth lost response) and #91 (duplicate response goes to RESET). They keep their R719-2 verdict, which was clean.
- **Lens:** CLEAN.

### RTL

- **No RTL file changes.** The delta touches no `.sv` file. There is no port, parameter or register-map change.
- **First shipping use of `MASK`.** `MASK` (`OP_SET_MASKED`) merges `(rd & ~rb) | (ra & rb)` (`hdl/ucpu/KL_gptp_ucpu.sv:205`). With `ra = R0` the result is `rd & ~rb`.
  - R0 reads zero only because the microcode never writes register 0. Existing `WRST ra=0` zero-writes already rely on the same invariant.
  - The hazard logic counts `rd` as a source for every op (`:175-181`), so `MASK` stalls on a pending write to rd.
  - `MD MULS` stalls until `md_done` (`:328`).
- **Bits cleared.** `MASK` clears bits 10:3 of the flags word. The only defined flag bits are 3:0 (`gen:570`), and the generator asserts that the mark's low nibble is exactly `FL_SYNCOK_C` (`gen:2182`). So only sync-ok can fall. asCapable (bit 2) is untouched, so the engine's asCapable-fall hook (`KL_gptp_engine.sv:950`) cannot fire from this leg.
- **Shared tail.** The SRTO leg's final `BR` targets µPC 700. That address is PDPAIR's `WRST RG_PUB|2`, and only `COMMIT` and `END` follow it. The SRTO leg sits at µPC 992 (`receipts/pubflags-target.txt`).
- **ROM.** I regenerated all four tracked images with each consumer's own arguments, and each is byte-identical to the tracked file (`receipts/regen-images.txt`). The shipping image holds 1,021 of 1,024 words. The two seeded images hold 1,022 (`receipts/seeded-images.txt`).
- **Lens:** CLEAN.

### Robustness

- **The fall commits at the expiry.** At head, the commit that carries the sync-ok fall comes from the expiry's own `COMMIT`. Sync stops while the priority1 255 grandmaster keeps announcing, the fall is committed with flags `5`, and the peer stays elected. Cycle values in that log are absolute harness cycles (`receipts/probe-p255-commit-recovery-head.log`).
- **Recovery.** Usable Sync resumed for 1 s re-raises sync-ok (`flags=d`) with the same grandmaster elected. So the unaged clear does not latch, and recovery is automatic.
- **No oscillation.** The author's unchanged rerun of R719-2's probe at head shows `syncok=0` from 1 s to 4 s after Sync stops, with `gm=0000000000000105` elected (`author-r3/receipts/probes/probe_p255_syncok-head.log`).
  - Its script hash `c751da23…7ec10` matches the published R719-2 script.
- **Master expiry.** A master-role expiry now commits an unchanged record once per expiry. The watch is not re-armed without a usable pair, so this adds no periodic commit. The "#84 every master cycle publishes sync-ok" checks pass.
- **Reachable states.** sync-ok is set only by a consumed pair, which needs an elected peer, or by BECOME, which sets the master bit. So the "neither elected nor master" case, where this leg also keeps sync-ok, cannot carry sync-ok.
- **Lens:** CLEAN.

### Tests

- **Own head run.** I ran the engine suite at the exact head with the pinned Verilator 5.050, which I verified (`receipts/verilator-version.txt`). All four passes ran (`receipts/engine-run-head.log`, rc 0):
  - shipping: 1,805/1,805;
  - request-seeded: 1,805/1,805;
  - Sync-seeded: 1,805/1,805;
  - priority1 255: 59/59.
- **Cheap gates.** These ran at head, concurrently, each rc 0 (`receipts/gate-*.{log,rc}`):
  - `make contract`, `make docs` (which includes diagrams-check) and `make lint` (pinned Verilator);
  - the microCPU, tsngen, gaskets and bench `test` suites;
  - the out-of-context clock self-test.
- **Controls rerun on their named checks.** I reran the round-3 controls against the unchanged harness (`receipts/probes.txt`):
  - "a sync receipt timeout that ages nothing keeps sync-ok": caught, priority1 255 pass 58/59, on the phase-42 check;
  - "a consumed pair leaves sync-ok down": caught on "…usable Sync raises sync-ok";
  - "an expiry takes a master's own vector for a peer's": caught, shipping pass, on "#84 takeover: the queued receipt timeout commits after it";
  - the unmutated control passes both passes.
- **Author receipts.** The author's mutation arm at head reports 101/101 (100 controls plus the clean control), rc 0, with each new control caught on its named check (`author-r3/receipts/repo-gates-head/04b-engine-mutants.log:153-171`).
- **Own plants.**
  - "the unaged expiry commits but publishes the flags unmasked": caught on the phase-42 check.
  - "the expiry writes the flags but never commits": caught only in the shipping pass, by phase 19. See S1.
  - Boundary plant: see S2.
- **Lens:** CLEAN. S1 and S2 concern test strength. They are not defects in the shipped behaviour.

### Docs

- **The new guide text matches the code:**
  - `HDL_DEVELOPER.md:199-218`;
  - `INTEGRATION.md:305-307`, `:403`, `:568-570`, `:594`, `:618`, `:646-648`;
  - `TEST_DEVELOPER.md:129`;
  - `SOURCE_EVIDENCE.md:40`.
- **Moved anchor.** The `prog_leg_slew` link moved to `#L998`, which is correct at head.
- **Source comments.** The comments in the delta give issue and clause IDs. They contain no lane label, lane name, review round, reviewer ID or issue-comment ID. Commit hashes that replaced "round 1" follow R719-2 R1's exact fix.
- **Wording.** One wording item remains (R1).
- **Lens:** CLEAN.

## Findings

### R1 - RESIDUE - `MASK` is described without its `ra` term

- **Lenses:** Docs.
- **Location:** `docs/HDL_DEVELOPER.md:214`, "`MASK` does that: rd and not rb."
- **Authority:** `hdl/ucpu/KL_gptp_ucpu.sv:205`: `merged_w = (opd & ~opb) | (opa & opb)`. The leg passes `ra = R0` (`gen:2193`).
- **Impact:** wording only. A reader could take `MASK` to be a plain and-not operation. No code, figure or claim changes.
- **Exact fix:** "`MASK` with ra = R0 does that: rd and not rb."
- **Verification:** `make docs` rc 0.

### Suggestions (no effect on the verdict)

- **S1 (Tests): bound the phase-42 commit.**
  - Phase 42 grades the live `pub_flags_o` only (`sim_main.cpp:5794-5798`), while integrators sample at `pub_commit_o` (`INTEGRATION.md:456`).
  - With the plant "the expiry writes the flags but never commits", the priority1 255 pass still reads 59/59. The fall then reaches a commit only at the next Announce, about 216 ms later (431,346 cycles; `receipts/probe-p255-commit-recovery-nocommit-mutant.log` against `...-head.log`).
  - Because the leg is branch-free, the master path loses its commit too, and phase 19 catches the plant. So the arm as a whole still catches it.
  - Consider also requiring, in phase 42, a commit naming G255 with sync-ok clear within 380 ms of the last pair.
- **S2 (Tests; R720-2 S1 retained, evidence updated): the gmPresent boundary has no control.**
  - The plant `SRTO_PASSED_C = 0xFE << 3` is now refused by the generator assert at `gen:2182`.
  - The plant "both compares shift by 52" treats priority1 127..254 as absent, and it survives: shipping 1,805/1,805 and priority1 255 59/59 (`receipts/boundary-probe.txt`).
  - The code is correct (exhaustive table above). Consider one priority1 254 Announce on the aged port in phase 41.
- **S3 (RTL/Tests): add microCPU vectors for `MASK`.**
  - This is the opcode's first use in shipping microcode, and the microCPU suite has no `SET_MASKED` vector.
  - Engine-level checks do cover it: the phase-42 flags are exactly `5`, and a master keeps sync-ok.
  - Consider adding microCPU vectors for both terms.
- **S4: suggestions carried unchanged, which the delta does not address:**
  - R719-2 S2: the edition note near `INTEGRATION.md:618`;
  - R719-2 S3: an own-port Sync filter;
  - R719-2 S4: Figure 11-8 wrong-sequenceId reset, to be filed as an issue;
  - R719-2 S5 / R720-1 F3 / R720-2 S3: a two-responder Follow_Up shape;
  - R720-2 S2: a recorded reason for the Sync asCapable gate.

## Prior public findings at this head

I resolved each item below after writing my own verdict draft.

| Prior item | State at 42f9541e | Evidence |
|---|---|---|
| R719-2 F1 (MINOR): a slave of a priority1 255 grandmaster keeps sync-ok after its Sync stops | **RESOLVED** (option (a)) | `gen:2186-2194`: an unaged expiry on an elected peer clears sync-ok and commits, and the peer stays elected. The named phase-42 check exists, and its control is caught (own rerun and author log). The R719-2 probe, run unchanged at head with a matching hash, gives `syncok=0` with `gm=…0105`. My own probe confirms the commit and the recovery. |
| R719-2 R1 (RESIDUE): source comments named review rounds | **RESOLVED** | `receipt_mutants.py:60` "the rule at d27a1654…" and `:155` "BECOME as d27a1654 had it…", as prescribed. |
| R720-2 R1 / R719-2 S1 (RESIDUE): "ages" for a master-role expiry | **RESOLVED** | `INTEGRATION.md:618` reads "So a master-role expiry marks the port aged too.", which carries the prescribed meaning. |
| R720-2 R2 / R719-2 S6 (RESIDUE): 97-column comment line | **RESOLVED** | Phase-39 comment rewrapped (`sim_main.cpp:5529-5534`). No added line in the delta exceeds 90 columns. The remaining long lines (`:3734`, `:5983-5997`) predate this PR. |
| R720-2 S1 (SUGGESTION): priority1 254 boundary | Retained as S2 | Evidence updated above. |
| R719-2 S2-S5, R720-2 S2/S3 | Retained in S4 | Suggestions only. |
| R719-1 F1-F3, R720-1 F1-F3 | Remain resolved | Their code is unchanged by this delta except `prog_leg_srto`. Its mark-on-every-expiry write is kept, and the "only an expiry that ages a slave marks the port" control is caught at head (author log `:165`). The companion patch's sha256 `b53944d5…1b7a` is unchanged from round 2. |

## Evidence verification

- **Author packet.** milan-fpga `8480ed96` `review-evidence/gptp90-r1/MANIFEST.json` has sha256 `1bf89606…4e1e`.
  - All 166 `author-r3` files are present, and each published sha256 matches. There are no missing or unlisted files, and no redacted-content entries (`evidence-manifest-check.txt`, `scripts/verify_manifest.py`).
- **Author gate rows at head.** Each row is rc 0 with `head_unchanged` true (`author-r3/receipts/repo-gates-head/rows.txt`, `repo-gates-head-make`):
  - contract, microCPU, parser, engine run (1,805 ×3 and 59), engine mutants (101/101), gaskets, tsngen, bench test, lint, docs, diagrams-check, ooc self-test;
  - the full `make`.
- **Parent consumer runs.** Runs final-a, final-b and final-c are rc 0, every row exit 0. They were made on a parent snapshot of dev `97aab1d0` with the gptp-processor gitlink at `42f9541e`, which `consumer-head/final-a/03.log:3` records.
  - Final-a has 14 rows, including both idiom gates and the milan_dp `gptp`/`gptp-lat` legs.
- **Hosted checks.** The exact head has 0 hosted check runs and 0 commit statuses. No hosted job executed, so no hosted claim is made.
- **Clone restored.** After the probes, HEAD and tree are exact. The index matches the HEAD tree in blob ids and modes, all 108 tracked files hash to their HEAD blobs, the worktree is clean, and the repository has no gitlinks (`receipts/clone-restore-check.txt`).
  - Every probe ran in disposable copies under the packet's `scratch/`.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `gen:2158-2195`, `:1107-1115`, `:497-507`; 802.1AS-2011 10.3.11 / Figure 10-13 (Cor1), 10.2.3.13, 10.3.12.1.4 g; exhaustive compare table | R719-3 (delta); R719-2 for #90/#91 | 42f9541e1d80e3d888cee1d16f19e01c0027f1cf |
| RTL | CLEAN | `KL_gptp_ucpu.sv:168-206,454-551,640-675`; `KL_gptp_engine.sv:934-955,1046`; PUBFLAGS target; four regenerated images | R719-3 | 42f9541e1d80e3d888cee1d16f19e01c0027f1cf |
| Robustness | CLEAN | own commit/recovery probe (head and no-commit plant); author R719-2 probe rerun; master-expiry commit path | R719-3 | 42f9541e1d80e3d888cee1d16f19e01c0027f1cf |
| Tests | CLEAN | own engine run (4 passes), 8 cheap gates, 3 author controls rerun, 3 own plants; author mutation arm 101/101 | R719-3 | 42f9541e1d80e3d888cee1d16f19e01c0027f1cf |
| Docs | CLEAN (R1 residue carried) | HDL_DEVELOPER, INTEGRATION, SOURCE_EVIDENCE, TEST_DEVELOPER deltas; source-comment rule scan of the delta; PR body figures | R719-3 | 42f9541e1d80e3d888cee1d16f19e01c0027f1cf |

## Real limits

- **Mutation arm not rerun.** I did not rerun the full arm (about 2 h serially). I reran 3 author controls and 5 own plants, and relied on the hash-verified author log for the rest.
- **Parent consumer gates not rerun.** That evidence is the author's published receipts. The parent companion patch is not committed anywhere, and its landing is still pending.
- **No manager bank at this head.** No manager source bank ran at this exact head. I claim or infer none.
- **Parts of the full gate set not run by me.** I did not run the parser suite or the full `make`. The author receipts cover both.
- **No synthesis.** The out-of-context synthesis flow was not run (the vendor tool is absent). Only its clock self-test ran.
- **No physical evidence.** Physical calibration was NOT RUN. Field skips are not hardware proof, and no hardware was used.

## Pending manager duties

- Build and validate the current-dev merge candidate. That means source base `55680bff` onto live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`, through the builder and native banks, at the merge turn. Link its receipts on the PR.
- Own hosted/act acceptance. The exact head currently has no hosted runs.
- Land, or sequence, the parent companion change (sha256 `b53944d52a51323b267b0a91dbfd6bd1aeaabcacf26d31b246b19318d56a1b7a`) together with the gitlink bump. Issues #89, #90 and #91 close only after it lands.
- Carry R1 to the residue checklist.
- Collect the second independent review result for this head.

R719-3 FINISHED
