[R400] POSITIVE - exact head 921fff59d6e1243284e477f7a368173018420d35

# R400-3: processor PR #135 (lane C2, MAAP), issues #66, #67, #68, round 3

- Exact head `921fff59d6e1243284e477f7a368173018420d35`, tree `dc1d52a75724f6ab29f4831d7498dece23202ca8`. Three commits on the round-2 head `053f979b`: the merge `c842670` (parents `053f979b`, `b2db3a97`), `f7b67ce` (R400-2-F1) and `921fff5` (R400-2-S1). R400-2-F2 is a PR-body change.
- **Verdict: POSITIVE.** No MINOR, MAJOR or BLOCKER is open, and all five lenses are CLEAN. I record one new SUGGESTION (R400-3-S1, Docs). Four earlier suggestions stay retained, as the PR body states.
- **Summary:**
  - The merge keeps both sides' checks. It differs from the mechanical merge only in the three conflicted files and four declared follow-ups.
  - Every focused mode of `tb/pp_top` runs only its own section, and the default run covers every section, including MP (34 checks) and D3 (133).
  - R400-2-F1 is resolved. U29 lands 20 one-cycle falls in the named walker states of three entries. It absorbs all 20 against the round-1 RTL. Each of the five `tx-set-omits-*` arms is KILLED on U29, and all five patches are byte-identical to R400-2's.
  - R400-2-F2 is resolved: "What remains" matches round 2 and the ruling, and every line reference I checked is correct.
  - R400-2-S1 is taken in U23, U28, the README and the PR body.
  - Round 3 changes no file under `hdl/`.

## 1. What was reconstructed, in order

1. **Conventions.** The processor repository has no AGENTS.md or CONTRIBUTING.md at this head. I used `README.md` and `docs/README.md`: the single-source rules, the citation form, and `make check`.
2. **Issue #66 and its public decisions:**
   - the issue body and acceptance list;
   - the lane assignment 5884446021;
   - the round-2 assignment 5887951933;
   - the STOP 5890736650;
   - the ruling 5890772857 (option 2: Table B.7 Release! row, B.3.1 c) and e), B.3.2, B.3.5.2, Table F.23);
   - the round-3 assignment 5903309279;
   - REVIEW READY 5906155816.
3. **Authorities:**
   - `docs/architecture/11_maap_engine.md` §6;
   - REQ-MAAP-001, -005 and -007 in `docs/00_MILAN_COMPLIANCE_REVIEW.md`;
   - the `KL_pp_maap.sv` walker (`:581-850`);
   - main's `docs/architecture/09_verification.md` (F28 = the AECP hold) and `tb/pp_top/d3_mutants.py`.

   IEEE 1722-2016 Annex B was judged through the clause citations in the ruling and in 11 §6. The standard's text is not distributed.
4. **Diff and history:**
   - `git diff b2db3a97..921fff59` (42 files);
   - `git diff 053f979b..921fff59`;
   - each of the three round-3 commits;
   - a recomputed mechanical merge of `053f979b` and `b2db3a97` (`git merge-tree`), compared with `c842670`.
5. **Public evidence** at milan-fpga `1afebd22:review-evidence/ppC2-r1/author-r3`: HANDOFF, the PR body, and the final, merge, f1 and s1 receipts. I also read the PR body and the hosted checks at the exact head.
6. **Prior public findings, read last.** They were read only after my provisional verdict and ledger were written (`receipts/provisional-verdict-ledger.md`, 07:43:17Z): R400-2 (5893604815), R401-2 (5893508851), and the R400-1 and R401-1 items as those two reviews list them. I then verified the byte-identity of R400-2's published patches.

## 2. Evidence I produced

All builds used Verilator **5.050** through `scripts/verilator-j8`, which caps `--build -j` at 8, one run at a time. Every build and run happened in `git archive` copies under the packet's `scratch/`.

| Run | Result | Receipt |
|---|---|---|
| Tool identity | The assigned path `$ASSIGNED_TOOL_DIR/pinned-tool-bin/verilator` is **absent**. I used the shared Verilator source build at tag `v5.050` (commit `848d926e`, `verilator_bin` sha256 `51910d8d…`). | `receipts/tool-identity.txt` |
| Mechanical merge vs `c842670` | `git merge-tree` conflicts in exactly `tb/pp_top/sim_main.cpp`, `tb/rx_validator/sim_main.cpp` and `tb/rx_validator/README.md`. Beyond those, `c842670` differs from the mechanical merge only in `tb/maap/README.md`, `tb/maap/mutants.py`, the re-anchored validator patch and `tb/pp_top/README.md`. | `receipts/merge-tree.txt`, `receipts/merge-resolution-vs-automerge-*.diff` |
| `tb/maap run` | rc 0, **196/196**. U29 prints 20 falls, each "a fresh walk". | `receipts/head-maap-run.log` |
| `tb/maap run` on host Verilator 5.052 (comparison) | rc 0, 196/196. Every scenario line is identical to the 5.050 run. | `receipts/head-maap-run-v5052.log` |
| `tb/rx_validator` | rc 0, **497/497** (main's 437 plus this lane's 60) | `receipts/head-rx_validator-run.log` |
| `tb/pp_top run` (both builds, default and fixture) | rc 0, **7,893/7,893**: default 7,873 (D3 133, NW 85), fixture 20 | `receipts/head-pp_top-run.log` |
| `tb/pp_top` focused modes | `maap-internal` 34/34; `--d3-only` 133/133; `--gsi-internal-only` 6,182/6,182; `--name-writes-only` 85/85; `--dr3a` rc 0 (measurements only, no tally, by design). All rc 0. | `receipts/head-pp_top-*.log`, `*.rc` |
| `tb/srp_top` (C1) | rc 0, **2,200/2,200** | `receipts/head-srp_top-run.log` |
| `make -C tb/maap mutants` | rc 0, **32/32**: 3 controls PASS and **29/29 KILLED**, each on its named check. Every one of the README's 29 ledger tallies ("N FAIL of M") equals this run. | `receipts/maap-mutants.txt`, `receipts/maap-mutants/*`, `receipts/ledger-vs-run.txt` |
| `d3_mutants.py` slice (#132), `--jobs 1` | rc 0. Goldens `pp_top` (`--d3-only`) and `rx_validator` PASS. `validator_admits_held_aecp` (the rx_validator F28 arm) and `dispatch_not_held` are KILLED. | `receipts/d3-mutants-slice.txt`, `receipts/d3-mutants-slice/*` |
| Static gates | `lint_hdl.sh` rc 0; `gen_matrix.py --check` rc 0 (94 rows, 0 untested); `make check` rc 0; `git diff --check` against `c951a9ff`, `053f979b` and `b2db3a97` rc 0 | `receipts/head-static.rc`, `receipts/head-lint_hdl.log`, `receipts/head-make-check.log`, `receipts/head-gen_matrix.log` |
| Head `tb/maap` against the round-1 RTL (`b03d36f` `KL_pp_maap.sv`) | rc 2, 23 FAIL of 187. **U29 absorbs 20 of 20 falls**, with no INITIAL, a claim kept, and no fresh walk. | `receipts/r1rtl-maap-run.log` |
| Reviewer probes (three disposable mutants that the author set does not contain) | Each is **KILLED**, each on U29. `post-ignores-live-fall` (`W_POST` no longer sees a live fall): U29 3/20 absorbed, and U23. `latch-keeps-claim` (the TX latch no longer withdraws the claim): U29 no-claim 10/20, plus U24 and U25. `latch-forgets-release` (the TX latch no longer remembers the Release!): U29 10/20 absorbed, and U24. | `probes/*.patch`, `receipts/probes.txt`, `receipts/probes/*` |
| R400-2 patch identity | `tx-set-omits-{alloc,gwait,commit}` and also `-write` and `-lane` at the head are **byte-identical** to R400-2's published patches. Each sha256 equals R400-2's `MANIFEST.sha256`. | `receipts/r400-2-patch-identity.txt` |
| R400-1 S1's patch re-run at the head | `r400-compare-mac-last-octet-only` still passes `tb/maap` 196/196. The suggestion stays retained. | `receipts/r400-1-s1.txt`, `receipts/r400-1-s1/*` |
| Clone integrity after all probes | HEAD, tree and `git write-tree` all equal `dc1d52a7…`. The worktree and index equal HEAD, with 0 untracked or ignored entries. 357 tracked entries match in bytes and mode. There are 0 gitlinks and no `.gitmodules`, so no submodule gitlinks are required. | `receipts/clone-verify.txt` |
| Hosted checks at the head (snapshot 07:45:49Z, push run 36682734423) | `portability` and `docs-gates` succeeded. `suites` is **in progress**. Its "Lint (zero tolerance) + every suite" step **executed** with success. The SRP campaign is running. The MAAP campaign, traceability and figures steps are **pending, not executed**. "Build Verilator v5.050" was skipped (cache hit). | `receipts/hosted-check-runs.txt` |

## 3. The round-3 items

### (1) The merge of processor main `b2db3a97` (`c842670`)

- **Both sides' checks are kept.**
  - `tb/pp_top/sim_main.cpp:10055-10067`: `--d3-only` and `--dr3a` (main) sit beside `--maap-internal-only` (lane). Each focused mode runs only its own section; I checked the truth table and ran every mode.
  - The default run keeps every section. MP runs inside `Suite::run` (`:8940`), and main's MP0 (`:8497`) is kept, so MP has 34 checks.
- **rx_validator.**
  - Main's F28 (the AECP hold, `held_aecp_frames_are_dropped_at_the_slot_gate`) keeps its name.
  - The lane's maap_version section is renamed F29, with F29a to F29c, and runs after F28.
  - The README gives the tally line `497` and keeps main's M4 row; the lane's row becomes M5.
  - No stale F28 reference to the maap_version section remains in the tree (`git grep`). `09_verification.md:194` and `d3_mutants.py:457` still mean the AECP hold.
- **The re-anchored campaign patch.** Only the hunk header and the trailing context moved (`@@ -274`, next to main's `held_fail_w`). The planted `+/-` lines are byte-identical to the round-2 patch. The arm is KILLED on F29 (47 of 497) and on MP7 (4 of 34).
- **Every #132 and C1 suite still passes.**
  - Only `tb/maap`, `tb/pp_top` and `tb/rx_validator` (and Yosys, which reads `hdl/maap`) consume a file that differs from `b2db3a97`. Every other suite's inputs are byte-identical to main.
  - I ran `pp_top` (every section and mode), `rx_validator`, `srp_top` and a D3 campaign slice.
  - The author's receipts at the head cover the rest: `run_suites.sh` rc 0 with 1,016,458 checks, `srp_top` mutants 90/90 with coverage 65/65, and `d3_mutants.py` 83/83 with goldens PASS. They are consistent with my tallies.

### (2) R400-2-F1 (`f7b67ce`)

- **What U29 does** (`tb/maap/sim_main.cpp:1473-1614`). It starts three entries: a mid-walk PROBE (a probe_timer expiry), an sDefend (an rProbe! in DEFEND), and a DEFEND re-announce. In each entry it lands a fall of exactly one clock edge, first seen in `W_IVAL`, `W_ALLOC`, `W_GWAIT`, `W_WRITE`, `W_COMMIT`, `W_LANE` or `W_POST`. sDefend has no `W_IVAL`, so there are 20 points.
- **The fall is really seen in the named state.** `eng_w` is combinational from `link_up_i` (`KL_pp_maap.sv:334`). The fall is applied for the single edge on which `walker_o` equals the named state, and the latch at `:589-593` samples `w_st_r` on that edge.
- **Each fall must give all of the following:**
  - INITIAL before the fresh walk's first PROBE;
  - no claim from the fall until the fresh walk's fourth PROBE;
  - at most one drained frame, byte-exactly the entry's own;
  - a fresh walk of 4 byte-exact PROBEs of one range, then its ANNOUNCE.

  An absorbed fall cannot pass. A continued PROBE walk has only 3 PROBEs left, and a DEFEND entry sends no PROBE at all.
- **This matches the required outcome and Annex B:** Table B.7 Release!, then PortOperational! in INITIAL (generate_address, ReserveAddress!), with B.3.2 ordering under the ruling.
- **Failing arms:**
  - `tx-set-omits-{alloc,gwait,write,commit,lane}` are each KILLED on U29. In each, 3 of 20 falls are absorbed, one per entry, and INITIAL, no-claim and fresh-walk all fail.
  - `-write` also fails U24, and `-lane` also fails U25, as the ledger says.
  - Against the round-1 RTL, U29 absorbs 20 of 20.
  - My three extra probes are KILLED on U29 too.
- **Ledger rows** for all five arms are in `tb/maap/README.md:261-265`.

### (3) R400-2-F2 (the PR body)

- **"What remains (round 1, rewritten in round 3)"** now states the following:
  - Both corners are resolved.
  - The seed is re-armed on every Release! (`W_OFF`, `KL_pp_maap.sv:604`; U27).
  - A frame still being drawn is dropped whole.
  - A frame whose slot was requested before the fall may drain, and no PDU is generated after the fall. It cites Table B.7, B.3.2, B.3.5.2, footnote c and the ruling.

  This matches the Round 2 section, 11 §6 and the ruling. The body no longer contradicts itself.
- **Line references.** I checked each against the tree:
  - `:613-627` (round 1 `:569-577`), `:644` (round 1 `:594`, base `:587`), `:604` and `:619-623`;
  - the parent's `milan_datapath.sv:7769` at dev `ec0cc0c1` and `:7695` at `13eda870`, both `.cfg_maap_internal_i (1'b0)`.

  Round-1 tallies are labelled as round 1's, and the round-1 validation section is labelled with head `b03d36f`.

### (4) R400-2-S1 (`921fff5`)

"No new TX slot request" (a request already pending is retried until granted) is now in:

- U28's check (`sim_main.cpp:1451-1453`) and its comment;
- U23's check (`:1060`) and its comment (`:993`);
- `tb/maap/README.md:114, 158-164`;
- the PR body's Round 2 section.

The README and the comment add that the unit bench's pool grants at once, so there any request after the fall would be a new one. That matches the RTL retry arc (`KL_pp_maap.sv:695-702`), and U28 still counts every request literally in the unit bench, which is the stronger check.

### Parent-visible list (re-read at the merged head)

- Round 3 changes nothing under `hdl/`. The lane's `hdl/` delta against main is byte-identical to its round-2 delta against its base.
- The list names what the merge brings: #132's consolidated list, C1's section 4, and the manager's combined adaptation.
- Parent-side claims (ratchets, port inventory 176, no parent file pinning these counts) are the manager's to confirm with the parent bank. I did not run any parent command.

## 4. Prior public findings: resolved or retained at this head

| Finding | Status at `921fff59` | Evidence |
|---|---|---|
| R400-2-F1 (MINOR, Tests) | **Resolved** | §3 (2): U29; five arms KILLED on U29, the first three byte-identical to R400-2's patches; 20/20 absorbed on the round-1 RTL; three further reviewer probes KILLED |
| R400-2-F2 (MINOR, Docs) | **Resolved** | §3 (3) |
| R400-2-S1 (SUGGESTION) | **Resolved** (taken) | §3 (4) |
| R400-1 F1 to F4 (MINOR) | **Resolved** (in round 2; still holds) | RTL unchanged since round 2. Their arms (`ival-sends-after-release`, `post-publishes-after-release`, `tx-path-absorbs-release`, `off-waits-for-an-edge`, `rx-release-returns-to-idle`, `seed-rearmed-on-idle-release-only`, `seed-clamp-off-by-one`, `release-waits-for-draw`, `idle-serves-a-latched-expiry-first`, `teardown-keeps-announce-timer`, `drain-waits-for-the-link`) are all KILLED in my campaign run. |
| R400-1 S1 (SUGGESTION, compare_MAC pair with equal low octets) | **Retained** | Not in the round-3 assignment. The published patch still passes `tb/maap` 196/196 (`receipts/r400-1-s1.txt`). |
| R400-1 S2 (SUGGESTION, shared default `/tmp/maap-mutants`) | **Retained** | `tb/maap/Makefile:4` is unchanged. Not in the round-3 assignment. |
| R401-1 F1 (MINOR) and F2 to F4 (SUGGESTION) | **Resolved** (in round 2; still holds) | Same arms, KILLED. `11` §6 and the README name both stalled states. |
| R401-2 S1 | (b) **Resolved** (it is R400-2-S1). (a) **Retained**. | The PR body gives the reason: normative 11 §6 and the banner already scope the timers during a drain. |
| R401-2 S2 (a stalled-drain expiry arm) | **Retained** | Reason stated in the PR body (not in the assignment; no surviving mutant) |
| R401-2 S3 | First half **resolved** (F2). Comment re-flow at `KL_pp_maap.sv:619-623` **retained**. | This round changes no `hdl/` file. |

## 5. Findings

No MINOR, MAJOR or BLOCKER is open.

### R400-3-S1: SUGGESTION. Lens: Docs

- **Where:**
  - `docs/architecture/11_maap_engine.md:137-138` (`f7b67ce`): a 115-column line inside an otherwise wrapped paragraph;
  - `tb/maap/README.md:163-165` (`921fff5`): a wrapped paragraph with one over-long line.
- **Authority:** readability of the normative 11 §6 text. `make check` passes and no gate enforces the width.
- **Impact:** cosmetic. The rendered Markdown is unaffected.
- **Suggested outcome:** re-flow both paragraphs when these files are next touched, together with R401-2 S3's comment re-flow.
- **Verification:** `make check` rc 0 after the re-flow.

## 6. Reviewer ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The ruling 5890772857 (Table B.7 Release!/PortOperational!, B.3.1 c) and e), B.3.2, B.3.5.2, footnote c) against U29's expectations and `KL_pp_maap.sv:581-850`. REQ-MAAP-007 and 11 §6. Issue #66, #67 and #68 acceptance still met (U17, U18, U18b, F29, MP4, MP7, and the campaign's `fit-compare-forced-true`, `seed-clamp-removed`, `validator-maap-version-1-only` and `compare-mac-forward` arms, all KILLED). | R400-3 | 921fff59d6e1243284e477f7a368173018420d35 |
| RTL | CLEAN | No `hdl/` change in round 3. The lane's `hdl/` delta against main is byte-identical to its round-2 delta against `c951a9ff`. `eng_w` is combinational (`:334`), so U29 lands each fall in the named state. `lint_hdl.sh` rc 0. The #132 RTL arrives unchanged through the merge (no `hdl/` edit in the resolution). | R400-3 | 921fff59d6e1243284e477f7a368173018420d35 |
| Robustness | CLEAN | Merge truth table of `tb/pp_top`'s modes; every mode run, rc 0. The campaign driver (controls first, named failures, no kill on a build failure or missing tally). One-cycle falls in 7 states × 3 entries. 5.050 and 5.052 give identical scenario output. Clone integrity after every probe. | R400-3 | 921fff59d6e1243284e477f7a368173018420d35 |
| Tests | CLEAN | `tb/maap` 196, `rx_validator` 497, `pp_top` 7,893 (MP 34, D3 133, NW 85, GSI 6,182), `srp_top` 2,200. MAAP campaign 32/32 with 29/29 KILLED. D3 slice: goldens plus 2/2 KILLED. U29 on the round-1 RTL: 20/20 absorbed. Three reviewer probes KILLED. R400-2 patch byte-identity. Author receipts for `run_suites` (1,016,458), `srp_top` mutants (90/90) and `d3_mutants` (83/83). | R400-3 | 921fff59d6e1243284e477f7a368173018420d35 |
| Docs | CLEAN (R400-3-S1 is a SUGGESTION) | `tb/maap/README.md` (U29 text, S1 wording, 29 ledger rows equal to my run); `tb/rx_validator/README.md` (497, M4 and M5); `tb/pp_top/README.md` (MP0, 34); 11 §6; the PR body ("What remains", line references, Round 3 section, parent-visible list); `make check` rc 0 | R400-3 | 921fff59d6e1243284e477f7a368173018420d35 |

## 7. Real limits

- **Tool path.** The assigned Verilator path was absent. I used a shared Verilator source build at tag `v5.050`, with its identity recorded. The hosted job and the author used the pinned 5.050 and 5.052 respectively, and my comparison run on 5.052 agrees.
- **One build above the cap.** The single 5.052 comparison build (`tb/maap`) used the Makefile's `-j 0` directly, so the build could use up to 16 threads. It compiled 6 C++ files, and it was the only such build.
- **Runs I did not make**, as the brief requires:
  - the full `run_suites.sh`, the SRP campaign, the full D3 campaign (2 of 83 arms run), `gsi_mutants.py` and `name_wr_mutant.py`, Yosys, and the NVM figures;
  - any parent, donor or builder bank.

  For those I rely on the author's round-3 receipts (public evidence), and my own runs agree with them.
- **Manager bank receipts at this head.** I found none in the published evidence tree at `1afebd22` or in comments on #66 and #135. The only manager bank comment is for round 2 (5893938585). The manager's source, static, builder and native banks at this head are taken as the brief states them.
- **Hosted checks.** At my snapshot the `suites` job had not executed its SRP campaign, MAAP campaign, traceability or figures steps.
- **Top-level retry arc.** The pool-contention retry arc (`W_GWAIT` to `W_ALLOC` after a fall) is not reachable in the unit bench, whose pool grants at once. It was judged from the source (`KL_pp_maap.sv:589-593, 695-702`): `rel_pend_r` is cleared only in `W_OFF`.
- **Standard text.** Annex B was judged through clause citations, since the standard's text is not distributed.
- **Hardware.** Physical calibration was NOT RUN and no hardware was involved. Skipped field contexts are not hardware proof.
- **Out of scope.** Processor main has moved to `0451d83d` (PR #136, lane C3), which conflicts in `.gitattributes`, `.github/workflows/hdl.yml` and `tb/pp_top`. That composition was not judged; it is round 4.
- **Path redaction.** Absolute paths in receipts are redacted to `$PACKET`, `$CLONE`, `$TOOLS`, `$ASSIGNED_TOOL_DIR` and `$HOME` before hashing.

## 8. Pending manager duties

- Accept the hosted `suites` job at the exact head once its SRP campaign, MAAP campaign, traceability and figures steps have executed.
- Run and post the donor bank and the parent consumer bank at milan-fpga dev `ec0cc0c1`, with the gitlink at `921fff59` and the combined #132 + C1 adaptation (`author-r3/parent-adaptation-132-c1.patch`) applied.
- Obtain the second independent review. Decide the retained SUGGESTIONs: R400-1 S1 and S2, R401-2 S1(a), S2 and S3's second half, and R400-3-S1.
- Round 4:
  - merge processor main `0451d83d` (PR #136), with its own delta review;
  - at the merge turn, build the final current-dev candidate (source base `b2db3a97`, live dev `ec0cc0c1`).
- Publish `REPORT.md` and the files listed in `MANIFEST.sha256`.

R400-3 FINISHED
