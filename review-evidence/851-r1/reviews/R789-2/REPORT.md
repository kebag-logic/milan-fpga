[R789] POSITIVE - exact head dafd49c1f9b79d3cc29534a9ab43d98360079d2b

Round R789-2 is the internal cleared-context review of issue #851 / PR #852 (adopt processor `044cb25f`, lab fix F7). It covers exact head `dafd49c1f9b79d3cc29534a9ab43d98360079d2b` (tree `01483285bef47c5ec3cb8fe61ded32337eee38d2`) on base dev `0a75aa774b89ac89351700f63dd8cbb89694af6c`. It is a delta review against round R789-1 at `2d939d2d`.

All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.

**Verdict: POSITIVE.**
- No BLOCKER, MAJOR or MINOR finding is open.
- Every prior public finding on this PR, from both reviews, is resolved at this head.
- Three RESIDUE items (wording only) and two SUGGESTIONs are recorded below so the author can absorb them in one pass.

## Prior public findings: resolved or retained at this head

| Prior finding | Status at `dafd49c1` |
|---|---|
| R789-F1 = R790-F1 (MINOR, RTL and Docs): timing-path figures had no receipt, and the worst-path receipt showed another path | **Resolved** (see "F1 at its cause") |
| R789-F2 = R790-S2 (MINOR / SUGGESTION, Docs): the adoption's own route share was reported as not measured | **Resolved** (see "F2 at its cause") |
| R789-S1 = R790-RS1 (SUGGESTION / RESIDUE, Docs): the "All nine measurements" stale count | **Resolved**: `docs/design/AREA_BUDGET.md:133` reads "All these measurements use the same recipe identity and policy." |
| R790-S1 (SUGGESTION, Tests): no parent gate notices a doubled vector | **Resolved** (see "Tests at its cause") |

### F1 at its cause

Every committed timing path is now `report_timing` output from the routed checkpoint.
- The excerpts are the worst setup and worst hold path per signoff corner (`author-r2/scripts/paths.sh`: `-max_paths 1 -nworst 1 -sort_by slack`, over every path group).
- `collect_paths.py` exits 1 unless each excerpt's slack equals that corner's WNS or WHS in the route's own Design Timing Summary.
- `receipts/paths-e44a4d20/{aslh,eppo,eto}/summary.md` read PASS on all 8 rows each.
- Each checkpoint hash matches `route-e44a4d20/RAW-RECORDS.txt`:
  - ASLH `7f00e872…`;
  - EPPO `73fa4844…`;
  - ETO `e40872cb…`.
- All 8 signoff-summary hashes match the same file.

The committed text matches the excerpts:
- `234_PP_SHADOW_AREA_BASELINE.md:146-151`, `AREA_BUDGET.md:235-236`, `SUBMODULES.md:834-842` and the PR body all match.
- Setup path: `uop_e_r_reg[imm][1]` to `deb_cnt_r_reg[10]/R`, 37 levels, Requirement 20.000 ns, 19.258 ns (6.316 ns logic, 12.942 ns route).
- Hold path: `frame_cid_r_reg[34]` to `evq_pd_ctx_r_reg_0_3_114_119/RAMA/I`, +0.036 ns at the Fast corners.
- EPPO: SoC write buffer to `storage_17`, 13 levels, 10 ns.
- ETO: `desc_base_r_reg[5]` to `deb_cnt_r_reg[25]`, 34 levels.

Round 1's receipts are corrected:
- `paths-round1/*` re-reports round 1's five checkpoints. All are PASS.
- They confirm round 1's committed figures: ETO 29 levels, `ctr_pend_r_reg[0]` to `hs_r_reg[1]/CE`, 19.439 ns (14.237 ns route); hold `cap_l_r_reg[18]` to `u_tcdc/mem_r_reg_0_7_42_47` +0.036 ns; EPPO 36 levels AECP to D3.
- So round 1's `worst-setup-path.txt` held the wrong path; its pages did not.

The #841 daily-route figure ("+246 LUTs") is gone from every page. The two remaining "#841 and #842" sentences (`AREA_BUDGET.md:659`, `234…:183`) are #843's own record text from dev.

### F2 at its cause

The share is now stated on both bases (`234…:99-111`, `AREA_BUDGET.md:233`, `SUBMODULES.md:813-830`, the PR body).

On dev `1eb5289d`:
- Dev route `f2-routes/dev-1eb5289d/gate-check.log` (copied from public `425a829e`; `chain.log` EXPORT `1eb5289d…`): 52,973 LUT, 54,595 FF, 15,817 slices, +0.234 / +0.033 ns.
- Round 1 route `round1-a566d4f9/gate-route-1x1.log`: 53,050 LUT, 54,729 FF, 15,831 slices, +0.258 / +0.036 ns.
- Share: +77 LUT, +134 FF, +14 slices, +0.024 / +0.003 ns. This is exact.

On dev `0a75aa77`:
- `record-e44a4d20/check-dev-route-1x1.log` (its baseline is byte-equal to dev's JSON by my `cmp`) gives +207 LUT, +83 FF, -5 slices, DSP 0, WNS -0.032 ns, WHS +0.024 ns.

"Only the processor gitlink moves a synthesis input" is verified:
- `git diff --name-only a6d7cdf3 0a75aa77` lists only docs, the baseline JSON and `tb/verilator/fw_service_budget/oracle.json`.
- `git diff --name-only 0a75aa77 e44a4d20` lists docs, the baseline JSON, `syn/yosys/rom_digests.tsv` (a ledger, not a synthesis input) and the processor gitlink.

### Tests at its cause

`[ONEVEC]` (`sim_crf_licence.cpp:158-175`, `:783-877`, `:1457`) grades the rule on the DUT's wire. Two encoders fail it (`onevec/*.log`):
- the planted encoder (`crflic_mutants.py:114-122`, `:196-224`), with got=3;
- the old `92100657` encoder, with got=4.

## Findings

### R789-2-R1 - RESIDUE - Docs - `docs/reference/SUBMODULES.md:813` - imprecise subject

- **Text:** "Dev `0a75aa77` is #843's record."
- **Evidence:** the measured fact (`234_PP_SHADOW_AREA_BASELINE.md:58`) is that #843's record measures dev `0a75aa77`'s synthesis inputs, at `a6d7cdf3`. A dev commit is not a record.
- **Impact:** wording only. No figure or claim changes.
- **Exact fix:** "#843's record, at `a6d7cdf3`, measures dev `0a75aa77`'s synthesis inputs."

### R789-2-R2 - RESIDUE - Docs - stale mutant counts next to the new arm

- **`docs/testing/TESTING.md:357`**, a line this delta edits, still says "the three gate mutants".
  - The campaign at the head runs six gate arms, then two TSpec arms and the encoder arm.
  - Evidence: `gates-dafd49c1/camp/crflic_mutants.log.tail` ("11 checks: 11 PASS").
  - Exact fix: "the six gate mutants".
- **`tb/verilator/milan_dp/Makefile:665-667`** reads "Six additional elaborations … and two more (#774) …". It does not count the ninth elaboration this delta adds.
  - Exact fix: append "and one more (#851, processor #214) builds a copy of the processor whose SRP encoder never merges".
- **Impact:** wording only. No test, and no count a gate reads, changes.

### R789-2-R3 - RESIDUE - Docs - `syn/ooc/pp_resource_baseline.json`, route-1x1 `measured` note

- **Text:** "-5 slices (80)". The neighbouring figures say "(tolerance +500)" and "(+600)".
- **Impact:** record-note wording only. The recorder does not write the field: `baseline-diff-recorded-head.txt` shows only the `measured` notes differing from the recorder's output.
- **Exact fix:** "-5 slices (+80)".

### R789-2-S1 - SUGGESTION - Tests, Robustness - parts of `[ONEVEC]`'s value expansion never run in this leg

- **Evidence:** my disposable probes at the head (`receipts/onevec-probe/`):
  - Clean leg: 430 / 0, `[i] 285 MSRP and 184 MVRP MRPDUs, 631 values`. This equals the author's figures.
  - Increment forced to 0 (`noincr`): one false double, an MSRP Talker Advertise with StreamID `0x0200000000010000`. So the StreamID increment is exercised, once in the whole run.
  - Ignore skip removed (`noignore`): 430 / 0 and the same 631 values. The Listener Ignore branch (`sim_crf_licence.cpp:825`) is never taken.
- **What this means:** a wrong reading of the Domain increment, the MVRP increment or the Ignore handling would not show at this head. The check still catches both real defect shapes: the planted encoder and `92100657`.
- **Optional outcome:**
  - Add a small self-test of `check_one_vector` on hand-built MRPDUs: a multi-value Domain vector, a multi-value MVRP vector and a Listener vector with an Ignore entry.
  - Or state in the README row which branches the run exercises.

### R789-2-S2 - SUGGESTION - Docs - Ignore wording; clause text not reopened by this reviewer

- **Text:** `sim_crf_licence.cpp:166-167` and `tb/verilator/milan_dp/README.md:532` say "A Listener value declared Ignore is not in the MRPDU (35.2.2.7.2 a))".
- **Observation:** an Ignore entry is physically present in the vector, as a FourPackedEvent of 0. What the walk relies on is that the entry carries no Listener declaration.
- **Optional outcome:** the author re-reads 35.2.2.7.2 and either keeps the wording or writes "carries no Listener declaration and is skipped".
- **Classification:** this is a clause claim and I did not open the clause text, so it is a SUGGESTION, not RESIDUE.

**Comment rule:** no new instance. Every source line this delta adds (`git diff 0a75aa77..HEAD -- tb sw scripts hdl syn/yosys`) cites only issue numbers, processor issue numbers and clauses. None carries a bench lane label, lane name, review round, reviewer ID or comment ID.

## Focus checks

### 1. The merge `e44a4d20` keeps both adoptions

- The parents are `2d939d2d` and `0a75aa77`.
- Every file dev changed since the merge base `1eb5289d` is byte-equal to dev in `e44a4d20`, except the twelve conflict and generated files listed in the HANDOFF.
- Every lane file is byte-equal to round 1, except the ten the merge rewrote.
- Two files keep the lane's version whole:
  - `syn/ooc/pp_resource_baseline.json`, then re-recorded;
  - `docs/findings/README.md`, the current-record line, which `dafd49c1` then rewrote.
- Pin table: both gitlinks (gPTP `1616fc8f`, processor `044cb25f`).
- The record list, record history, the #234 page and the Mark II ledger keep #843's and #851's records in order (`AREA_BUDGET.md:121-134`, `:205-237`, `:652-664`; `234…:12-14`, `:51-177`; `MARK_II_AREA_PLAN.md:939-940`).

My reruns at the head (`receipts/quick/`), all rc 0:
- `check_submodule_docs.py`: 6 exact gitlinks;
- `submodule_boundaries.gen.py --check`: OK, decoded PNG;
- `./syn/yosys/ooc.sh --record-rom-digests` plus `git diff --exit-code`: the recorder reproduces the rows;
- `docs_inventory.py --check`: fresh;
- `check-baseline`: 3 endpoints;
- `pp_srcs.py --check`, `docs_check.py`, `check_em_dash.py --base 0a75aa77` (389 added lines, 339/339 arms);
- `check_cpp_idiom.py`, `check_py_idiom.py`, `git diff --check 0a75aa77 HEAD`.

Baseline JSON:
- The committed JSON equals `record-e44a4d20/baseline-recorded.json`, the recorder's output, except the three `measured` notes.
- Against dev's JSON, only figures, scopes, `inputs_sha256` and the `measured` notes move: 204 leaf changes (`baseline-diff-dev-head.txt`).
- No tolerance, floor, ceiling or flow field moved, and the directive stays AltSpreadLogic_high.

### 2-4. F1, F2 and the stale count

All three are resolved, as set out above.

### 5. `[ONEVEC]`

The walk agrees with the MRPDU layout:
- ProtocolVersion 0.
- MSRP Messages carry an AttributeListLength. MVRP Messages end at their AttributeList EndMark.
- The VectorHeader's 13-bit NumberOfValues is read.
- ThreePackedEvents are decoded most significant first (/36, /6 %6, %6). FourPackedEvents are 2 bits per value, the first value in the top bits.
- The identity is {application, AttributeType, value}, matching the processor's `key_f`.

Robustness of the walk:
- Every loop advances, so it cannot hang.
- Every read past the frame is guarded.
- A truncated or malformed MRPDU counts as `malformed` and fails its own check, so the walk fails closed (`:788-850`).

The campaign arm is guarded against drift:
- It refuses unless its pattern occurs exactly once in `KL_srp_encoder.sv`, which is true at `:453`.
- It refuses a mutant that does not compile.
- It plants into a copy of `hdl/` passed by `PP_DIR`. The Makefile derives the processor sources from `PP_DIR` (`Makefile:43`, `:161`).
- Tying `sr_hit_w` to 0 keeps the search but never merges (`:458`, `:464-465`, `:680-681`), so every hand-over appends, as before #214.

Head campaign (`gates-dafd49c1/camp`, head `dafd49c1`): crflic-mutants 11 of 11, gsi-mutants rc 0, unb-mutants rc 0.

### 6. The combined route at `e44a4d20`

- `chain-e44a4d20/clone-1x1.log` and `clone-8x8.log` both read `e44a4d20`, with the gitlinks exact.
- The three directives ran from one export, one route at a time (`chain1.log`). `ooc-8x8` synthesized beside the first route.
- Gate (`check-dev-route-1x1.log`):
  - AltSpreadLogic_high is selected at 0.21 ns, over EPPO 0.112 and ETO 0.018.
  - 53,428 LUT, 54,837 FF, 15,829 slices, RAMB36 74, RAMB18 27, DSP 15.
  - Corners: Slow +0.21 / +0.069 ns, Fast +1.52 / +0.036 ns.
  - Route complete.
  - It passes against dev's record, as do `ooc-1x1` (+203 / +76) and `ooc-8x8` (+184 / +80).
- After `record --write`, `check` exits 0 on all three endpoints and `check-baseline` exits 0.
- ETO misses the +0.03 ns floor at the Slow corners (0.018). The floor binds the selected route (`BUILDING.md:569`, `:579`: "The shipping image is built from that directive").
- 21 slices are left.

### 7. SDK loss and superseded runs

- The first firmware runs ended 10:26-10:51 CET. The shared SDK was deleted at 10:32-10:38.
- Every reported firmware group was re-run from 10:55 (`records/cpu-booking.txt`) on fresh clones at `dafd49c1`.
- Re-run evidence:
  - `fw0/fw_rv32_sdk_selftest.log`: "SDK verified", archive `d42680e9…`, GCC 14.3.0;
  - `fw3/fw_boundary.rc`: 0.
- The superseded `fw_boundary` runs (rc 2, twice) appear only under `superseded/`.
- Neither the PR body nor the REVIEW READY comment cites a superseded run.
- The sweep, started 10:22, is unaffected: no suite Makefile and no line of `run_all_suites.sh` references the RV32 SDK.

### 8. Gates at the head

These are author receipts, `sweep-dafd49c1`.
- Every shard's `spec__results.json` has head `dafd49c1` and base `0a75aa77`.
- Shards: 15 + 17 + 17 + 16 = 65 suites, 0 failed, 0 timed out.
- Checks: 361,195 + 1,525,512 + 284,230 + 21,575 = 2,192,512.
- The crflic leg is an ordinary `milan_dp` sweep case (`Makefile:740`). My own clean run of it at the head gives 430 / 0.
- Firmware shards 0-3, coverage, nvm and the self-tests exit 0, as do both builder legs.
- Evidence packet `0976305c`: 753 of 753 `author-r2` files match `MANIFEST.json`, with 0 mismatches, 0 missing and 0 unlisted (`receipts/evidence-manifest-check.txt`).

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #851 acceptance against the head receipts (sweep 65/65, firmware, builder, behave, docs, route fit and floor). The `[ONEVEC]` walk (`sim_crf_licence.cpp:788-850`) against the MRPDU layout and the processor's `key_f` identity. `BUILDING.md:569,579` against the selected route. The maintainer decision of 2026-11-06 against the JSON diff (`baseline-diff-dev-head.txt`: figures only, and the gate passed). Processor gitlink unchanged since R789-1 | R789-2 | `dafd49c1f9b79d3cc29534a9ab43d98360079d2b` |
| RTL | CLEAN | `git diff 0a75aa77..HEAD` touches no parent `hdl/`. The processor gitlink `044cb25f` and its RTL keep R789-1's verdict; the gPTP gitlink equals dev's. Combined-route timing: `paths-e44a4d20/{aslh,eppo,eto}` excerpts (Requirement 20 / 10 ns, levels, delays), tied to the checkpoint and signoff hashes in `route-e44a4d20/RAW-RECORDS.txt`. Corners, slices and sub-block movements in `check-dev-*.log` | R789-2 | `dafd49c1f9b79d3cc29534a9ab43d98360079d2b` |
| Robustness | CLEAN | `check_one_vector` bounds, termination and fail-closed `malformed` (`sim_crf_licence.cpp:788-850`). The `run_pp_mutant` pattern and compile guards (`crflic_mutants.py:196-224`). Probes `noincr` and `noignore` (S1, optional). The SDK-loss timeline and the isolation of superseded runs (`records/cpu-booking.txt`, `superseded/README.txt`) | R789-2 | `dafd49c1f9b79d3cc29534a9ab43d98360079d2b` |
| Tests | CLEAN | My clean crflic run at the head, 430 / 0 (`onevec-probe/clean.log`). The author's planted encoder (got=3) and `92100657` (got=4) in `onevec/*.log`. Campaign 11/11 at the head (`gates-dafd49c1/camp`). The `noincr` probe fails, so the check discriminates. Sweep shard heads and check sums. The README and TESTING rows name the new arm | R789-2 | `dafd49c1f9b79d3cc29534a9ab43d98360079d2b` |
| Docs | CLEAN (RESIDUE R1-R3 carried; S1 and S2 optional) | `SUBMODULES.md:724-856`, `AREA_BUDGET.md:13,121-159,205-237,652-664`, `234_PP_SHADOW_AREA_BASELINE.md:1-177`, `CHANGELOG.md:11,58-91`, `MARK_II_AREA_PLAN.md:59,939-940`, `findings/README.md:25`, `TESTING.md:357`, `milan_dp/README.md:87,532,601` and the PR body, all against the receipts above. The generated diagram, manifest, audit and ROM ledger through their generators (`receipts/quick/*`, all rc 0) | R789-2 | `dafd49c1f9b79d3cc29534a9ab43d98360079d2b` |

## Method and receipts (this packet)

- **Reading:**
  - issue #851's body and its four comments, the PR body and the PR comments, through the read-only API;
  - my own R789-1 report;
  - R790-1, read only after my own pass over the diff.
  - No private or management material was read.
- **Author evidence:** `review-evidence/851-r1/author-r2` at `0976305c`, extracted with `git archive` into a scratch directory and checked by `scripts/verify_manifest.py`.
- **Scripts:**
  - `scripts/probe_onevec.sh`: the clean, `noincr` and `noignore` probes, in disposable clones at the head, with pinned Verilator 5.050 (rev v5.050, wrapper sha256 `905795b9…e92f`);
  - `scripts/quick_checks.sh`;
  - `scripts/json_diff.py`.
- **Hosted snapshot:** `receipts/hosted/`.
- **Clone integrity** (`receipts/clone-integrity.txt`): the review clone was never written. After the probes:
  - HEAD `dafd49c1`, tree `01483285`, porcelain 0;
  - the index mode/blob/path listing equals HEAD's (sha256 `9a53534a…`);
  - all six gitlinks are exact.
- Local absolute paths in published receipts are replaced by placeholders.

## Real limits

- I reran no Vivado route, full sweep, firmware bank or builder. Route, path, gate, sweep and firmware figures rest on the author's published receipts at the stated commits, and the large reports are published as hashes only.
- I did not reopen the IEEE 802.1Q-2022 clause texts (10.8.1.2, 35.2.2.6-35.2.2.9, 11.2.3.1.7 and 11.2.3.1.9).
  - The `[ONEVEC]` Domain and MVRP increments and its Ignore handling were checked for internal consistency only.
  - My probes show those branches are not exercised in this leg (S1).
- Hosted exact-head evidence at the snapshot (`receipts/hosted/`):
  - The four PR workflows (rtl-fast, elaborate, docs, rtl-full) were cancelled by their fail-fast after `elaborate-gates-3`'s "Install the pinned sv2v release" step got `curl: (22) … error: 504`, an infrastructure download failure.
  - The aggregate jobs (`docs-check`, `elaborate`, the `Union …` jobs, `verilator-suites`, `yosys-portability`) then failed on "dependent job … cancelled".
  - So there is no successful exact-head `rtl-fast`, `verilator-suites` or `yosys-portability` verdict yet. This is not a source defect, and it is not acceptance evidence either way.
- Act at this head: NOT RUN; this role may not run it.
- Physical calibration: NOT RUN. There was no hardware or bench access, and field skips are not hardware proof.
- No manager source bank ran at this exact head, and none is claimed or inferred.

## Pending manager duties

- Re-run the hosted workflows at `dafd49c1` now that the sv2v download has failed once, and confirm exact-head `rtl-fast`, `verilator-suites` and `yosys-portability`. The PR is marked ready, not draft.
- Run act at the final head.
- Build and validate the current-dev merge candidate (builder and native banks) against live dev `0a75aa774b89ac89351700f63dd8cbb89694af6c`, and link its receipts on the PR.
- Carry RESIDUE R1-R3 to the residue checklist.
- Self-test evidence still lives only in the issue's REVIEW READY comment and the PR body. The PR's DoD box "Self-test evidence is posted in a PR comment" is unchecked.
- Keep the external review independent.
- Merge only on explicit maintainer authorization.

R789-2 FINISHED
