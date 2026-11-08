[R789] NEGATIVE - exact head 2d939d2dcb9664c08f7d2dc7b584987a1e0c0f8a

Round R789-1, internal cleared-context review of issue #851 / PR #852 (adopt processor `044cb25f`), tree `42c092d1a9ec53f3655aa3e3605105a14e79ee7b`, on dev `1eb5289db8fc9d139ce90cad2e380b4515793806`. All five lenses were applied: Conformance, RTL, Robustness, Tests, Docs.

Verdict: NEGATIVE. There are two open MINOR findings, both about evidence and record content. No defect was found in the adopted RTL, the gitlink, the gate records or the consumer gates.

Prior public review findings on this PR: none. Before this round the PR thread holds only the two review-start comments, so nothing is carried over.

## Findings

### F1 - MINOR - Docs, RTL - committed timing-path and daily-route figures have no public receipt, and the receipt named for the worst path shows a different path

- **Where:**
  - `docs/design/AREA_BUDGET.md:211-212`
  - `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:127-130`
  - `docs/reference/SUBMODULES.md:721-725`
  - The PR body: "The worst setup path is inside the processor's AECP block (microcode CPU to the D3 debounce counter, 36 logic levels, 20 ns clock)".
  - The #841 daily-route delta "+246 LUTs and +10 FFs" at `docs/design/AREA_BUDGET.md:209`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:95` and the PR body.
- **Evidence:**
  - These pages commit measured figures for the selected ExtraTimingOpt route:
    - 29 logic levels;
    - `u_notify/ctr_pend_r_reg[0]` to `u_nvm_shadow/hs_r_reg[1]`;
    - 19.439 ns data delay, of which 5.202 ns is logic and 14.237 ns is routing;
    - the worst hold path `cap_l_r_reg[18]` to `u_tcdc/mem_r_reg_0_7_42_47`.
  - They also commit an ExtraPostPlacementOpt worst path (AECP microcode CPU to `u_d3`, 36 levels).
  - None of the 703 files in `review-evidence/851-r1` at `2dd97058` contains any of these paths or delays. The search is in `receipts/figure-crosscheck.txt` and the method is below.
  - `author/receipts/route-2d939d2d/worst-setup-path.txt` and `route-a566d4f9/worst-setup-path.txt` both show a `clk200_p` path at +3.609 ns slack with 0 logic levels. That is not the +0.044 ns WNS path its name claims.
  - The routed timing reports are published as hashes only ("not copied"). `gate/eto/large.sha256` lists only the baseline log.
  - The #841 figure traces to no receipt, repository page or public comment.
- **Impact:** These pages argue that the WNS fall is not the adoption's ("outside the encoder this pin changes"). A cold reviewer cannot check that argument, which is a timing-effect claim, or the committed delays. The one published receipt for the worst path contradicts the pages.
- **Required outcome:**
  - Publish the worst setup and hold paths (report_timing excerpts, slow and fast corners) for the selected ExtraTimingOpt route and the ExtraPostPlacementOpt shipping route at the measured commit. Tie each to the hash of its not-copied report.
  - Correct the worst-path extraction.
  - Publish or cite the source of the #841 daily-route delta.
  - Any figure that cannot be backed is removed or marked unmeasured.
- **Verification:** The next round opens the excerpts and matches the levels, the endpoints and both delays to the pages.

### F2 - MINOR - Docs - the record says the adoption's own route share cannot be measured, but public evidence measures it

- **Where:** `docs/design/AREA_BUDGET.md:208`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:94` and the PR body's Known limitations. All three say "No route of dev `1eb5289d` exists on this recipe, so this adoption's own share of the route growth is not measured".
- **Evidence:**
  - PR #846's round-2 receipts, `review-evidence/843-r1/author-r2/receipts/route-dev` at evidence commit `425a829e46033442e9093825b4dbb8d69f4fab9c`, routed dev `1eb5289db8fc9d139ce90cad2e380b4515793806` on this recipe (`chain.log`: `EXPORT 1eb5289d...`).
  - ExtraTimingOpt was selected there: 52,973 LUT, 54,595 FF, 15,817 slices, +0.234 / +0.033 ns, gate rc 0.
  - Against this PR's selected route (53,050 LUT, 54,729 FF, 15,831 slices, +0.258 / +0.036 ns), the adoption's share is +77 LUT, +134 FF, +14 slices, WNS +0.024 ns and WHS +0.003 ns.
  - So the receipts **agree** with the manager's figures (+77 LUT, +14 slices) for judgement call 2.
  - The statement was true when `405f1587` was committed (21:21Z). Dev's route chain completed at 21:48Z, so the statement is stale at this head.
  - Earlier records do state the adoption's share against dev when one exists (`AREA_BUDGET.md:187`, `:612`).
- **Impact:** The record withholds a measurement that exists and states that it does not. This is a measurement-status claim, not wording alone.
- **Required outcome:** At the planned post-#846 sync and re-measure, the record states the adoption's share against the measured dev route on this recipe and cites its receipt. The "no route exists" claim goes. Nothing beyond the planned re-measure is required.
- **Verification:** The next round diffs the two pages and the PR body against the dev-route receipt.

### S1 - SUGGESTION - Docs - a stale count that predates this PR

- `docs/design/AREA_BUDGET.md:129` reads "All nine measurements use the same recipe identity and policy". The page now lists fourteen records.
- The line predates this delta: it was unchanged by the twelfth and thirteenth records. It is optional here and could become its own issue.

RESIDUE: none. This PR changes no parent source comment. The baseline JSON `measured` notes carry the decision's comment URL exactly as the preceding record's notes already did (3 instances at dev `1eb5289d`). They are record data, not source comments.

## Focus checks

1. **The gitlink and the processor change.**
   - The index holds `160000 044cb25f4ed2187bd238490650e73d5d189855d1 0 protocol-processor` (`receipts/clone-integrity.txt`).
   - Public processor `main` is exactly `044cb25f`, and it is processor PR #215's merge commit (MERGED 2026-11-07T17:19:52Z). Its parents are `92100657` and `7feeccea`, and its tree `60300bb0` equals `7feeccea`'s.
   - From `92100657` to `044cb25f` the only processor HDL change is `hdl/srp/KL_srp_encoder.sv` (+146/-12). The only non-test, non-doc change outside it is `tb/srp_top/mutants.py`. No port or parameter changed; only the `ev_ready_o` comment changed.
   - The RTL matches the PR body:
     - `key_f` is {app, AttributeType, FirstValue[0:8)}, or the VID for MVRP.
     - `merge_ev_f`: New or Lv replaces; a join keeps a pending New; an s replaces only an s.
     - `merge_fp_f`: the Listener declaration type follows the newer event unless that event was a non-replacing s.
     - The search goes through the existing read port, one clock per entry.
   - The parent pages repeat processor `docs/architecture/10_srp_engine.md:131-165` faithfully, including the five-clock drain and the "third entry" slip.
2. **Consumer gates at this head.**
   - Author receipts: all four sweep shards ran at `2d939d2d` with rc 0 (`spec__results.json` `head` field). The `milan_dp` tail is green.
   - Also rc 0 at the head: the campaigns crflic-mutants (10 checks PASS), gsi-mutants and unb-mutants; the firmware shards, including the SRP mutation shard; behave (14 features, 508 scenarios, 2,330 steps); the builder in both legs; the rtl-fast steps; `check_cpp_idiom`; the xvlog gate; the ROM-digest check.
   - My independent run in a disposable clone at this head: the `milan_dp` `crflic` leg (`receipts/crflic`), 427 checks and 0 failures. That leg parses the DUT's own MSRP MRPDUs: "every DUT LeaveAll flagged all four MSRP attribute types" and each Talker Advertise TSpec.
   - The SRP wire comparisons pass.
3. **The route.**
   - Shipping route (ExtraPostPlacementOpt) at the head (`route-2d939d2d`, clone head `2d939d2d`, tree `42c092d1`): 53,033 LUT, 54,729 FF, 15,792 of 15,850 slices, 87.5 BRAM tiles, 13 DSP, 0 routing errors. Corners:
     - Slow 0/85 C: WNS +0.044, WHS +0.066;
     - Fast 0/85 C: WNS +1.408, WHS +0.035.
   - This equals the `a566d4f9` run figure for figure.
   - Gate route set (`gate-route-1x1.log`): ExtraTimingOpt selected at +0.258 ns. Corners:
     - Slow: WNS +0.258, WHS +0.102;
     - Fast: WNS +1.375, WHS +0.036.
   - Every corner of the selected route meets WNS >= +0.03 ns and WHS >= 0 (BUILDING.md section 5). The one-directive shipping route also meets the floors at every corner. AltSpreadLogic_high misses the floor at +0.028 ns, and the docs disclose this.
   - Post-route LUTs match the PR: 53,050, 53,033 and 53,082. The placement report reads 1 more for ETO and ASLH, and the PR consistently uses the post-route figure.
   - The gate refused `route-1x1` only (+521 of +500). It is re-recorded, and `check` and `check-baseline` exit 0 afterwards.
   - The JSON structural diff (method below) shows only figures, scopes, `inputs_sha256` and `measured` notes moved. No tolerance, floor or ceiling moved. This follows the maintainer decision of 2026-11-06.
   - Processor #214 originates in a conformance-run capture, so it is a lab fix as that decision requires.
4. **Judgement call 1 (re-record all three endpoints) is accepted by the manager.** The standalone endpoints were measured at this pin, not copied:
   - They have their own Vivado runs (`gate/chain1.log` DONE ooc rc=0 at 20:35Z; `chain8.log` DONE ooc8 rc=0 at 19:47Z).
   - Their own utilisation and hierarchy reports: 25,199 / 21,010 and 37,048 / 32,116, encoder 1,561 / 1,573 LUT.
   - New `inputs_sha256` values, and gate deltas against the thirteenth record.
5. **Judgement call 2:** the receipts agree. The share is +77 LUT and +14 slices; see F2.
6. **Act at this head:** NOT RUN; open, as instructed.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gitlink record; processor main and PR #215 merge, parents and tree; `KL_srp_encoder.sv` delta (`key_f`, `merge_ev_f`, `merge_fp_f`, `value_search`) against the PR body, `SUBMODULES.md:635-790`, `INTEGRATION_GUIDE.md:89-110` and processor `10_srp_engine.md:119-165`; issue #851 acceptance against the receipts for the sweep, firmware, builder, behave, docs and route; maintainer decision 6689114981 against the JSON diff | R789-1 | `2d939d2dcb9664c08f7d2dc7b584987a1e0c0f8a` |
| RTL | UNCLEAN (F1) | encoder search and merge datapath and read-port mux; ports and parameters unchanged; `KL_pp_shadow` and `milan_datapath` unchanged; ROM rows (`rom_digests.tsv:9-10` = `:55-56`); route and gate corners, slices and sub-block deltas (`gate-route-1x1.log`, `eto/eppo/aslh` reports); dev-route share; the critical-path claims could not be verified (F1) | R789-1 | `2d939d2dcb9664c08f7d2dc7b584987a1e0c0f8a` |
| Robustness | CLEAN | `value_search` reset, restart when the offered event changes, accept on hit or last; full-table hold and drain-overtake paths; processor `tb/srp_encoder` at the pin 1,604/1,604 with planted no-merge (68 FAIL) and join-displaces-New (5 FAIL) mutants (`receipts/encoder`); parent `crflic` LeaveAll and TSpec wire leg 427/0 at the head (`receipts/crflic`); the 8x8 standalone endpoint within its gate | R789-1 | `2d939d2dcb9664c08f7d2dc7b584987a1e0c0f8a` |
| Tests | CLEAN | encoder suite discriminates both planted defects; sweep shards 0-3 at the head rc 0 (`sweep-2d939d2d/shard-*/spec__results.json`); crflic, gsi and unb campaigns and firmware shards rc 0 at the head (`gates-2d939d2d`); behave totals; no parent doubled-vector check, disclosed and graded in the processor (PV1-PV20, OV0-OV10) | R789-1 | `2d939d2dcb9664c08f7d2dc7b584987a1e0c0f8a` |
| Docs | UNCLEAN (F1, F2) | `CHANGELOG.md`, `INTEGRATION_GUIDE.md`, `SUBMODULES.md`, `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md`, the #234 finding page, findings README, `DOCUMENTATION_AUDIT.md`, the diagram and manifest; checks rerun by this reviewer (`receipts/quick`), all rc 0: `check_submodule_docs`, `docs_inventory --check`, `check_em_dash --base 1eb5289d` (372 added lines, 339/339 arms), `docs_check`, `check-baseline`, `pp_srcs --check`, the ROM recorder reproducing the committed rows, `git diff --check` | R789-1 | `2d939d2dcb9664c08f7d2dc7b584987a1e0c0f8a` |

## Method and receipts

- **Reading:** the public issue, PR, maintainer decision and processor issue #214 were read through the read-only API.
- **Author evidence:** `review-evidence/851-r1` at `2dd97058` was sparse-cloned and checked against its MANIFEST.json (703 entries, 0 hash mismatches; `receipts/evidence-manifest-check.txt`).
- **Dev route:** `route-dev` at `425a829e` was read through git object reads.
- **Figure extraction:** `scripts/crosscheck_figures.sh` reproduces the figure extraction (`receipts/figure-crosscheck.txt`).
- **The F1 search** covered all 703 evidence files:
  - exact strings: the path endpoints (`ctr_pend_r`, `hs_r_reg`, `cap_l_r`, `u_tcdc`, `u_notify`, `nvm_shadow`), the delays (`19.439`, `14.237`) and the daily-route revisions (`+246`, `3f6bef88`, `cc204c6f`);
  - pattern: `Logic Levels: +(29|36)`;
  - hits only in hierarchy reports, synthesis log tails, campaign logs and the published HANDOFF.md, none of them a timing path.
- **JSON structural diff:** `syn/ooc/pp_resource_baseline.json` at `1eb5289d` against the head, walked field by field.
- **Probes:** run in a disposable local clone at the head with the pinned submodules. Scripts are in `scripts/`:
  - `probe_encoder.sh` (processor encoder suite and two planted mutations);
  - `run_crflic.sh`;
  - `quick_checks.sh`.
  - Verilator identity: 5.050 rev v5.050, wrapper sha256 `905795b9...e92f`.
- **Clone integrity:** the review clone was never modified. HEAD, tree, index and gitlinks were verified after the probes (`receipts/clone-integrity.txt`: porcelain 0, index tree `42c092d1`, six gitlinks exact).
- **Hosted snapshot:** `receipts/hosted/check-runs-2d939d2d.txt`.
- **Redaction:** local absolute paths in published receipts are replaced with placeholders.

## Real limits

- No Vivado route, full sweep, firmware bank or builder was rerun by this reviewer. Route, gate and sweep figures rest on the author's published receipts at the stated commits; for the route this means the hash-only large reports plus the published excerpts.
- The IEEE 802.1Q-2022 and Milan v1.2 clause texts were not reopened. The clause citations were checked for consistency against the processor's architecture document and the repository's traceability pages.
- In particular, whether a Talker Advertise and a Talker Failed for one StreamID may share an MRPDU was not judged against 35.2. The identity keeps them distinct by AttributeType.
- The processor RTL was read as a delta and exercised through its own encoder suite and two mutants. This is not a full independent processor review, which belongs to the processor lane.
- The author's `fw_rv32_sdk_selftest.symlinked-path` leg exits 1 with "SDK provenance mismatch" on a symlinked destination. The canonical leg exits 0 with 25 tests. No SDK script changes in this PR.
- Act at this head: NOT RUN.
- Hosted exact-head evidence at the snapshot:
  - completed success: `changes`, `bdd-conformance`, `docs-check-no-git`, `elaborate-gates-2/3`, `wire-accountability`, `full-ci-gate`;
  - skipped: the physical gPTP context;
  - queued or in progress: the Verilator shards, the firmware jobs, `verilator-lint`, the docs gates and the Yosys preparation.
  - This is not acceptance evidence. The manager owns hosted and act acceptance.
- Physical calibration NOT RUN. No hardware or bench access. Field skips are not hardware proof.
- No manager source bank ran at this exact head, and none is claimed or inferred.

## Pending manager duties

- Sequence #846 first, then sync this lane and re-measure. The re-measure is where F2 closes.
- F1 needs published timing-path excerpts or removed figures.
- Run act at the final head.
- Confirm hosted exact-head `rtl-fast`, `verilator-suites` and `yosys-portability`.
- Build and validate the current-dev merge candidate (builder and native banks) and link its receipts on the PR.
- Self-test evidence currently lives in the issue's REVIEW READY comment and the PR body. CONTRIBUTING asks for a PR comment, and the PR's own DoD box is unchecked.
- The external review (R790) stays independent.
- Merge only on explicit maintainer authorization.

R789-1 FINISHED
