[R401] POSITIVE - exact head 921fff59d6e1243284e477f7a368173018420d35

# R401-3: independent external delta review of processor PR #135 (lane C2, MAAP; issues #66, #67, #68), round 3

- Exact head `921fff59d6e1243284e477f7a368173018420d35`, tree `dc1d52a75724f6ab29f4831d7498dece23202ca8`, verified in a detached clone (HEAD, tree, index tree, worktree bytes and modes; `receipts/clone-integrity.txt`).
- Scope: three commits on the round-2 head `053f979b`: the merge `c842670` of processor `main` `b2db3a97` (PRs #132 and #133), `f7b67ce` (R400-2-F1) and `921fff5` (R400-2-S1), plus the PR body (R400-2-F2). Assignment: #66 comment 5903309279.
- **Verdict: POSITIVE.** No MINOR, MAJOR or BLOCKER is open. All five lenses are CLEAN. I record one new SUGGESTION (R401-3-S1, line re-flow). R400-2-F1 and R400-2-F2 are resolved, R400-2-S1 is taken, and every earlier suggestion is resolved or explicitly retained.
- Not judged here: the composition with processor `main` `0451d83d` (PR #136, lane C3). That merge is round 4.

## 1. What was reconstructed, in order

1. Contribution guidance. The processor tree has no `AGENTS.md` or `CONTRIBUTING.md`, so I read `README.md` (gates: `run_suites.sh`, `lint_hdl.sh`, `make check`, `gen_matrix.py --check`) and `docs/README.md` (ID registries, single-source rules, citation rules, "`make check` before commit").
2. Issue #66: its body and acceptance (the fit clamp), and every comment. These cover the lane plan 5884446021 (#66, #67 and #68, the gates), round 2 5887951933, the STOP 5890736650, the ruling 5890772857 (option 2: a frame requested before the fall may drain, and no PDU is generated after the fall), and the round-3 assignment 5903309279.
3. PR #135: the body at this head, and the manager comments (review starts, and the round-2 banks 5893938585).
4. Authorities, as the ruling and the code cite them:
   - IEEE 1722-2016 Annex B: Table B.7 (the Release! and PortOperational! rows), B.3.1 c) and e), B.3.2, B.3.5.2, B.3.5.9, footnotes a and c, Table B.9, B.2.3;
   - `docs/architecture/11_maap_engine.md` §6, REQ-MAAP-007 in `docs/00_MILAN_COMPLIANCE_REVIEW.md`, and the `KL_pp_maap.sv` banner.
5. The diff: `git diff b2db3a97..921fff59` (42 files), each round-3 commit on its own, and `git show --remerge-diff c842670` for the three conflict resolutions.
6. Public executable evidence at milan-fpga `1afebd22` `review-evidence/ppC2-r1`: the round-3 author packet `author-r3` (tool identity, merge totals and arms, the f1 and s1 campaigns, the final d3, SRP and suite summaries). R400-2's published `tx-set-omits-*.patch` files were read only for the byte-identity check, after my own pass.
7. Prior public review findings: R400-1, R401-1, R400-2 and R401-2. I read them only after my own pass over the diff, and resolve them in section 5.

## 2. Evidence I produced (all in the foreground, Verilator builds capped at 8 jobs)

Tool: Verilator 5.050 through the wrapper `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`. The brief's path is absent (section 7). This wrapper's sha256 is `905795b9…e92f`, it wraps `verilator_bin` sha256 `44898b22…bfdd`, and it reports `5.050 2026-07-01`. The same identity is recorded in the round-2 reviewer receipts. g++ 16.2.1, Python 3.14.7. See `receipts/tool-identity.txt`. Every build ran in a `git archive` copy of the exact head under `scratch/`. `scripts/run_focused.sh` lists the commands.

| What | Result | Receipt |
|---|---|---|
| `tb/maap` | rc 0, 196/196. U29 prints 20 falls, each "a fresh walk" | `receipts/head/maap-run.log` |
| `tb/rx_validator` | rc 0, 497/497 (main's F28 and this lane's F29) | `receipts/head/rx_validator-run.log` |
| `tb/pp_top` default (`make run`, both builds) | rc 0, 7,893/7,893 (7,873 default + 20 fixture). The default runs MP, from `Suite::run` (`sim_main.cpp:8940`), and D3 (133) | `receipts/head/pp_top-run.log` |
| pp_top focused modes | `--maap-internal-only` 34, `--d3-only` 133, `--dr3a` rc 0, `--gsi-internal-only` 6,182, `--name-writes-only` 85: all rc 0 | `receipts/head/pp_top--*.log` |
| Suites main changed (#132, #133) | acmp_nvm 360, desc_mem_guard 78, dyn_state 118, srp_encoder 581, srp_stream_fsms 1,219, srp_top 2,200: all rc 0, with counts equal to the author's totals | `receipts/head/*-run.log` |
| `make -C tb/maap mutants` equivalent (`mutants.py`) | rc 0, `32 checks: 32 PASS`. 3 controls and 29/29 arms KILLED. The five `tx-set-omits-*` arms are each KILLED on U29, with exactly the omitted state absorbed in all three entries | `receipts/campaign.txt`, `receipts/campaign/` |
| Ledger against logs (`scripts/check_ledger.py`) | 29 ledger rows in `tb/maap/README.md`, 0 mismatches ("N FAIL of M" equals each arm log's tally). The U29 notes in the ival, post, tx-path and off rows match the logs (2, 10, 15 and 20 of 20) | `receipts/ledger-check.txt` |
| #132's `validator_admits_held_aecp` (`d3_mutants.py --only`) | golden PASS, KILLED | `receipts/d3-validator-arm.txt` |
| Validator patch re-anchor | Its planted `+`/`-` lines are identical before (`053f979b`) and after the merge, and it applies cleanly at the head (`@@ -274`) | (command in section 3 (1)) |
| Reviewer probes (`scripts/own_probes.py`, patches in `mutations/`) | 5 of 5 KILLED, U29 named in each (table below) | `receipts/own-probes.txt`, `receipts/own-probes/` |
| Round-1 RTL (`b03d36f2` `KL_pp_maap.sv`) under the head bench | U29 absorbs 20 of 20. INITIAL, claim and fresh-walk checks each fail 20 of 20 | `receipts/own-probes/round1-rtl-head-bench-maap.log` |
| R400-2 patch identity | `tx-set-omits-{alloc,gwait,commit}` are byte-identical to R400-2's published patches, and so are `-write` and `-lane` | `receipts/r400-2-patch-identity.txt` |
| Static | `lint_hdl.sh`, `make check` and `gen_matrix.py --check` rc 0. `git diff --check` against `c951a9ff`, `053f979b` and `b2db3a97` rc 0 and empty | `receipts/static/` |
| Hosted, exact head | `docs-gates` success, `portability` success, `suites` still in progress when queried | `receipts/hosted-checks.txt` |

Reviewer probes, each a single edit to `hdl/maap/KL_pp_maap.sv` at the head:

| Probe | Planted defect | Result |
|---|---|---|
| `r401-3-post-ignores-own-fall` | `W_POST` honours only the latch (`if (rel_pend_r)`), so a one-cycle fall first seen in `W_POST` is lost | KILLED: U29 absorbs the 3 `W_POST` falls, and U23 fails too |
| `r401-3-latch-keeps-claim` | the TX latch sets `rel_pend_r` but leaves `pstate_r`, so the claim lives through the drain | KILLED: U29's no-claim check, plus U24 and U25 |
| `r401-3-latch-defend-only` | the latch acts only in DEFEND | KILLED: U29 absorbs the mid-walk PROBE's 5 TX falls, and U24 fails |
| `r401-3-latch-skips-sdefend` | the latch skips an sDefend frame | KILLED: U29 absorbs the sDefend entry's 5 TX falls, plus U24 and U25 |
| `r401-3-ival-announce-only` | `W_IVAL` honours a fall only for the announce draw | KILLED: U29's PROBE `W_IVAL` fall, plus U17c and U28 |

## 3. The round-3 items, judged

**(1) The merge `c842670`** has parents `053f979b` and `b2db3a97`: a merge, not a rebase. The remerge diff shows the three conflicts resolved so that both sides' checks are kept:

- `tb/pp_top/sim_main.cpp:10057-10067`:
  - `--maap-internal-only` sits beside `--d3-only`, and `--dr3a` returns early;
  - each focused mode excludes the others, and the default runs every section;
  - I ran all five modes and the default, and each passes with the counts above.
- `tb/rx_validator/sim_main.cpp`:
  - main's F28 (`held_aecp_frames_are_dropped_at_the_slot_gate`) keeps its name;
  - the lane's section becomes F29a to F29c and runs after F28;
  - `tb/rx_validator/README.md` carries M4 (main) and M5 (the lane) and the 497 tally;
  - main's `docs/architecture/09_verification.md:194` and `tb/pp_top/d3_mutants.py:457` still say F28 correctly, and no stale F28, 453 or "of 33" reference to the lane's section remains (text search).
- Re-anchored campaign patch: the planted edit is unchanged, and it is KILLED in both suites (F29 47 of 497, MP7 4 of 34).
- MP0: main's `boot_to_aecp` check leads `InternalMaapPhase::run`, so MP has 34 checks, and `tb/pp_top/README.md` says so.
- #132's rx_validator arm is still KILLED at the head.
- The author's public receipts show `d3_mutants.py` 83/83 and the SRP campaign 90/90 (coverage 65/65) at this head. I did not rerun those two whole campaigns (section 7).

**(2) R400-2-F1 (`f7b67ce`).**

- What U29 does (`tb/maap/sim_main.cpp:1473-1612`):
  - it lands 20 one-cycle falls (`link_up_i` low for exactly one `step()`), each first seen in a named state;
  - the states are `W_IVAL`, `W_ALLOC`, `W_GWAIT`, `W_WRITE`, `W_COMMIT`, `W_LANE` and `W_POST`, across three entries: a mid-walk PROBE, an sDefend, and a DEFEND re-announce (sDefend has no `W_IVAL`);
  - each fall must give INITIAL, no valid claim until the fresh walk's 4th PROBE, at most the entry's own byte-exact frame drained, and a fresh walk of 4 byte-exact PROBEs of one range, then its ANNOUNCE;
  - the premise check fails if a fall misses its state.
- This meets R400-2-F1's required outcome (`W_ALLOC`, `W_GWAIT` and `W_COMMIT` in a DEFEND entry and in a mid-walk PROBE entry), and goes beyond it.
- The five `tx-set-omits-*` arms are each KILLED on the U29-named checks, and have ledger rows. The alloc, gwait and commit patches are byte-identical to R400-2's.
- The round-1 RTL absorbs 20 of 20.
- My five extra probes show that U29 also discriminates the `W_POST` and `W_IVAL` arcs, the claim withdrawal, and entry-selective latches.
- The Table B.7 semantics U29 asserts (Release! to INITIAL; PortOperational! in INITIAL giving generate_address and ReserveAddress!, then 4 PROBEs and an ANNOUNCE) match the standard and the banner.

**(3) R400-2-F2 (PR body).**

- "What remains (round 1, rewritten in round 3)" now says that both Release! corners are resolved, and states the ruling correctly: no PDU generated after the fall, and a frame requested before the fall may drain (Table B.7, B.3.2, B.3.5.2, footnote c).
- The line references in sections 1 to 3 are refreshed and carry their round-1 values:
  - `KL_pp_maap.sv:613-627` (`:569-577`) is the `W_ADDR` fall exit at the head;
  - `:644` (`:594`) is the fit compare, and `:604` is `W_OFF`'s seed re-arm;
  - the parent tie-off is `hdl/milan/milan_datapath.sv:7769` at dev `ec0cc0c1`, which I read: `.cfg_maap_internal_i (1'b0)`.
- The round-1 tallies and validation are labelled as round 1's.
- The body's round-3 tallies match my runs (maap 196, rx_validator 497, pp_top 7,893, MP 34, campaign 32). Its 1,016,458 equals the author's merge-head per-suite sum of 1,016,453 plus U29's 5.
- I found no statement in the body that contradicts `11` §6 or the ruling.

**(4) R400-2-S1 (`921fff5`).**

- "no new TX slot request … (a request already pending is retried until granted)" now appears:
  - in U28's check (`sim_main.cpp:1451-1454`) and its comment;
  - in U23's check and comment;
  - in `tb/maap/README.md:114,158-165`;
  - in the PR body's Round 2 section.
- The README's explanation matches the RTL: `W_GWAIT` goes back to `W_ALLOC` without a grant (`KL_pp_maap.sv:695-702`), and the unit bench's pool grants at once.
- My campaign log shows the new U28 wording in `idle-serves-a-latched-expiry-first`.

Round 3 changes no file under `hdl/`: `git diff 053f979b 921fff59 -- hdl/maap` is empty, and `git diff b2db3a97 921fff59 -- hdl/` touches only `hdl/maap/KL_pp_maap.sv`.

## 4. Findings

No MINOR, MAJOR or BLOCKER.

### R401-3-S1: SUGGESTION. Lens: Docs

- **Where:**
  - `tb/maap/README.md:165`: 140 characters, joined in `921fff5`;
  - `docs/architecture/11_maap_engine.md:137-138`: 113 characters on `:138`, joined in `f7b67ce`.
- **Authority/evidence:** the surrounding prose in both files wraps at about 80 columns. The two round-3 edits joined their new sentence onto the next line without re-flowing it (`awk 'length>100'` over prose lines finds only these two).
- **Impact:** none on the rendered text or the gates (`make check` rc 0). The source diffs are just harder to read.
- **Suggested outcome:** re-flow both paragraphs when these files are next touched. This fits naturally with R401-2-S3's retained comment re-flow.
- **Verification:** no prose line over 100 characters in either file.

## 5. Prior public review findings, at this head

| Finding | Status at `921fff59` | Basis |
|---|---|---|
| R400-2-F1 (MINOR, Tests) | **Resolved** | Section 3 (2): U29 at the head, 5 arms KILLED on U29, patch identity, and the round-1 RTL absorbing 20 of 20 |
| R400-2-F2 (MINOR, Docs) | **Resolved** | Section 3 (3) |
| R400-2-S1 (SUGGESTION) | **Taken** | Section 3 (4) |
| R401-2-S1 (SUGGESTION) | (b) is taken as R400-2-S1. (a), the timers during a drain, is **retained** with the reason stated in the PR body | The normative `11` §6 and the banner (`:77-78`) state it, so this is not blocking |
| R401-2-S2 (SUGGESTION, a stalled-drain expiry arm) | **Retained**, with the reason stated in the PR body | Not blocking. No surviving mutant is known |
| R401-2-S3 (SUGGESTION) | The "What remains" half is **resolved** (R400-2-F2). The comment re-flow at `KL_pp_maap.sv:619-623` is **retained**, because round 3 changes no `hdl/` file | Not blocking |
| R400-1-S1 and S2 (SUGGESTIONs) | **Retained** (not in the round-3 assignment) | Not blocking |
| R400-1-F1 to F4 and R401-1-F1 (MINORs); R401-1-F2 to F4 (SUGGESTIONs) | **Remain resolved** | Their arms are all KILLED in my head campaign: `ival-sends-after-release`, `post-publishes-after-release`, `tx-path-absorbs-release`, `off-waits-for-an-edge`, `rx-release-returns-to-idle`, `seed-rearmed-on-idle-release-only`, `seed-clamp-off-by-one`, `release-waits-for-draw`, `idle-serves-a-latched-expiry-first`, `teardown-keeps-announce-timer` and `drain-waits-for-the-link` |

## 6. Reviewer-owned lens ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Table B.7 (Release! and PortOperational! rows), B.3.2, B.3.5.2, footnote c and the ruling 5890772857, checked against U29's assertions and `KL_pp_maap.sv:58-79, 581-627, 660-669, 694-744`. #66, #67 and #68 acceptance still met at the merged head (U17, U18, U18b, F29, MP4, MP7; campaign 32/32). REQ-MAAP-007 | R401-3 | 921fff59d6e1243284e477f7a368173018420d35 |
| RTL | CLEAN | No `hdl/` change in round 3. The merged `hdl/` equals `b2db3a97` except `KL_pp_maap.sv`. The Release! latch and the `W_IVAL`, `W_POST` and `W_OFF` arcs were re-read. Lint rc 0. pp_top with main's D3 and AECP-hold RTL next to the internal MAAP engine (MP 34/34, D3 133/133) | R401-3 | 921fff59d6e1243284e477f7a368173018420d35 |
| Robustness | CLEAN | One-cycle falls in 7 states of 3 entries (U29), plus 5 reviewer probes, all KILLED. The unit-bench pool retry wording. The merge's mode exclusivity in `pp_top` `main()`. The campaign driver (controls first; named failure required; a build failure or missing tally never counts). The re-anchored patch refusing drift (`git apply --check`) | R401-3 | 921fff59d6e1243284e477f7a368173018420d35 |
| Tests | CLEAN | `tb/maap/sim_main.cpp` U29 and its premise; `mutants.py` (5 new rows); the 5 new patches (R400-2 identity); campaign 32/32 with every ledger tally reproduced; the round-1 RTL under the head bench (20/20 absorbed); the merged `tb/pp_top` and `tb/rx_validator` benches and every suite main touched; #132's validator arm | R401-3 | 921fff59d6e1243284e477f7a368173018420d35 |
| Docs | CLEAN (S1 is a SUGGESTION) | `tb/maap/README.md` (U28, U29, the ledger, the tallies), `tb/pp_top/README.md` MP, `tb/rx_validator/README.md` (F28/F29, M4/M5), `11_maap_engine.md` §6, the PR body (sections 1 to "What remains", Round 2, Round 3, the parent-visible list, validation), commit messages. `make check` and `gen_matrix --check` rc 0 | R401-3 | 921fff59d6e1243284e477f7a368173018420d35 |

## 7. Real limits

- **Tool path.** The brief's Verilator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator` instead. It reports Verilator 5.050, and its wrapper and `verilator_bin` hashes equal those in the round-2 reviewer tool-identity receipts. The author's round-3 runs used 5.052, and CI pins v5.050.
- **What I did not rerun myself.** The full `run_suites.sh` (the 24 suites neither this round nor main touched), the whole `d3_mutants.py` (83 arms; I ran its rx_validator arm), the SRP campaign (78 arms), `gsi_mutants.py`, `name_wr_mutant.py`, the nvm_port figures, Yosys, and the parent consumer and donor banks. For these I rely on the author's public round-3 receipts (suites 1,016,458/0 failing, d3 83/83, SRP 90/90) and the manager's banks.
- **No public manager bank receipt for this head.** The brief says the manager's source static, builder and native banks passed here. The only manager bank comment on the PR is for `053f979b`, and the evidence tree at `1afebd22` holds the author's receipts only, so I have not inspected a manager receipt for `921fff59`.
- **Hosted checks.** At the time of review, `suites` was still in progress; `docs-gates` and `portability` had succeeded. Hosted and act acceptance belong to the manager.
- **Unit bench only.** U29 and my probes run in the unit bench, where the pool and lane grant at once. The top's pool-contention retry after a fall, and the longer drain window at the top, are reasoned from the source and not simulated.
- **Not in scope.** No hardware, and physical calibration NOT RUN. Field skips are not hardware proof. The C3 composition (`main` `0451d83d`) is not judged.

## 8. Pending manager duties

- Hosted acceptance at `921fff59`: the `suites` job, and act.
- The donor bank and the official parent consumer bank at milan-fpga dev `ec0cc0c1`, with the combined #132 + C1 adaptation. Publish their receipts for this head.
- Decide the retained SUGGESTIONs: R400-1-S1/S2, R401-2-S1(a)/S2/S3 (comment re-flow) and R401-3-S1.
- Round 4: the merge of `main` `0451d83d` (PR #136) with its own delta review. It conflicts in `.gitattributes`, `.github/workflows/hdl.yml` and `tb/pp_top`.
- The pin-adoption lane's parent-visible list: this lane's items, PR #132's consolidated list and C1's section 4.

R401-3 FINISHED
