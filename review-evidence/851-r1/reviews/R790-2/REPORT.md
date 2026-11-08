[R790] POSITIVE - exact head dafd49c1f9b79d3cc29534a9ab43d98360079d2b

External independent review, round R790-2, of issue #851 / PR #852. The PR adopts protocol-processor main `044cb25f` (processor PR #215, processor #214: one vector per value per MRPDU), lab fix F7.

- Exact head: `dafd49c1f9b79d3cc29534a9ab43d98360079d2b`, tree `01483285bef47c5ec3cb8fe61ded32337eee38d2`. It matches the PR's `headRefOid`.
- Merge base: dev `0a75aa77`.
- This round is a delta review against my round 1 report at `2d939d2d` (R790-1, NEGATIVE on F1).
- All five lenses were applied: Conformance, RTL, Robustness, Tests, Docs.

**Verdict.** Every round 1 finding from both reviewers is resolved at this head, at its cause. This round found no BLOCKER, MAJOR, MINOR or RESIDUE. Four SUGGESTIONs follow, and none affects coverage.

## What was reviewed

Context was reconstructed in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. The issue #851 body (frozen acceptance) and the author's round 2 TAKEN and REVIEW READY comments.
3. The PR #852 body.
4. `git diff 0a75aa77..dafd49c1` (20 files) and `git diff 2d939d2d..dafd49c1`, plus the four round 2 commits `e44a4d20` (the merge), `bb9f0a06`, `bc80b3d3` and `dafd49c1`.
5. The author's round 2 packet at evidence commit `0976305c` (`review-evidence/851-r1/author-r2`).
6. The exact-head hosted check runs.

Prior public findings (R789-1 and R790-1) were read only after my own pass over the diff.

## Delta checks

### 1. The merge `e44a4d20` keeps both adoptions, and every figure came from its recorder or generator

- **Parents.** The merge is `--no-ff` with parents `2d939d2d` and `0a75aa77`, and there is no rebase.
- **Gitlinks.** The index carries gPTP `1616fc8f` (#843) and processor `044cb25f` (#851). The pin table names both, and `check_submodule_docs.py` exits 0 (my run, `receipts/gate-submodule-docs.log`).
- **Nothing of dev's was lost.** `git diff 0a75aa77 e44a4d20` touches only the 15 files round 1 itself changed, so no dev-only change was dropped. In the conflicted prose, the dev lines replaced at the merge are the single-valued "current record" lines. `dafd49c1` then rewrote them for the merged tree. At the head, dev's #843 paragraphs, its record-history entry, its route table and its #843 section on the #234 page are all present.
- **Baseline JSON.**
  - `receipts/record-e44a4d20/baseline-merge-e44a4d20.json` is byte-identical to `git show e44a4d20:syn/ooc/pp_resource_baseline.json`.
  - `baseline-dev-0a75aa77.json` is byte-identical to dev's file.
  - The recorder output `baseline-recorded.json` differs from the head file only in the three `measured` notes. No `tolerance`, `floor` or `ceiling` key moved between dev and the head (field-by-field diff).
- **Boundary diagram.** `submodule_boundaries.gen.py --check` exits 0 (my run).
- **ROM ledger.** The `044cb25f` rows equal the `92100657` rows. I regenerated `ucode.hex` (`49a993be...`) and `ltn_rom.hex` (`23cc67ee...`) from the `044cb25f` processor tree through the milan_dp recipe, and both match the ledger rows.
- **Docs inventory and audit.** `docs_inventory.py --check` exits 0 (my run).

### 2. R789-F1 = R790-F1: timing paths now come from `report_timing`, and the excerpt check works

- **How the paths are taken.** `author-r2/scripts/paths.sh` runs `report_timing -max_paths 1 -nworst 1 -sort_by slack` on the routed checkpoint at each corner, with the corner set-up taken from the platform declaration.
- **The refusal check.** `collect_paths.py` exits 1 unless each excerpt's slack equals that corner's WNS or WHS in the route's own signoff summary.
- **All eight summaries pass.**
  - Three directives at `e44a4d20`: `paths-e44a4d20/{aslh,eppo,eto}`.
  - Five round 1 checkpoints: `paths-round1/*`.
- **Committed claims match the receipts.** Each path claim on the #234 page (`docs/findings/234_PP_SHADOW_AREA_BASELINE.md:146-151`), the area budget (`docs/design/AREA_BUDGET.md:235-236`), the pin page (`docs/reference/SUBMODULES.md:834-842`) and the PR body equals `paths-e44a4d20/aslh/summary.md`:
  - setup: `uop_e_r_reg[imm][1]` to `deb_cnt_r_reg[10]/R`, 37 levels, 20.000 ns requirement, 19.258 ns (6.316 logic, 12.942 route), slack 0.210 = WNS;
  - hold: `frame_cid_r_reg[34]` to `evq_pd_ctx_r_reg_0_3_114_119`, 0.036 = WHS at Fast.
- **The other two directives match.** EPPO is the SoC write buffer to `storage_17`, 13 levels, 10 ns. ETO is `desc_base_r_reg[5]` to `deb_cnt_r_reg[25]/R`, 34 levels.
- **Round 1's path claims were right.** `paths-round1/recipe-eto-a566d4f9` shows 29 levels, `ctr_pend_r_reg[0]`, 19.439 ns with 14.237 ns of routing, and hold `cap_l_r_reg[18]` at 0.036. `ship-eppo-2d939d2d` shows 36 levels, AECP to D3, at 0.044. That is exactly the verification my F1 asked for.
- **The #841 daily-route figure is gone.** No "+246 LUTs" and no "daily ExtraPostPlacementOpt" remain anywhere in `docs/` or `CHANGELOG.md` (grep).

### 3. R789-F2 = R790-S2: the adoption's share is stated on both bases

- **Dev `1eb5289d` base.** `f2-routes/dev-1eb5289d/gate-check.log` is byte-identical (sha256 `c9cb09c6...`) to `review-evidence/843-r1/author-r2/receipts/route-dev/gate-check.log` at the public evidence commit `425a829e`, fetched by me. It reads ETO 52,973 / 54,595 / 15,817 at +0.234 / +0.033. Round 1's `gate-route-1x1.log` reads ETO 53,050 / 54,729 / 15,831 at +0.258 / +0.036. The share is therefore +77 LUT, +134 FF, +14 slices, +0.024 / +0.003 ns.
- **Dev `0a75aa77` base.** `check-dev-route-1x1.log`, the gate against dev's own record, reads +207 LUT, +83 FF, -5 SLICE, DSP 0, WNS -0.032, WHS +0.024, RESULT PASS.
- **The base claim holds.** "From dev `0a75aa77` only the processor gitlink moves a synthesis input" is true: `git diff --name-only 0a75aa77 e44a4d20` lists docs, the baseline JSON, the ROM ledger and the gitlink. `git diff --name-only a6d7cdf3 0a75aa77` lists docs, the baseline JSON and a testbench oracle only.
- **Sub-block arithmetic.** I re-derived each row on the #234 page (`:115-128`), on the pin page (`SUBMODULES.md:854-855`) and in the area budget from the JSON on both sides, and all match. The encoder is +118 / +99 on the route, +78 / +75 on ooc-1x1 and +105 / +71 on ooc-8x8. `milan_datapath` is 44,831 LUT (`route-e44a4d20/aslh/baseline_hierarchy.rpt:114`), and the wrapper is 25,184 (`:180`).

### 4. The stale count is fixed

`docs/design/AREA_BUDGET.md:133` now reads "All these measurements use the same recipe identity and policy." No "All nine" or "All ten" remains in the area pages.

### 5. R790-S1: `[ONEVEC]` is implemented, and both broken encoders fail it

I reviewed the grader in `tb/verilator/milan_dp/sim_crf_licence.cpp:158-175, 702, 783-877, 1457` against the MRPDU layout:

- the ProtocolVersion octet at 14;
- the per-Message AttributeType and AttributeLength;
- the MSRP AttributeListLength bounding each Message;
- the MVRP AttributeList ending at its own EndMark;
- the 13-bit NumberOfValues;
- ThreePackedEvents decoded as /36, /6 %6 and %6;
- FourPackedEvents decoded MSB-first, with 0 (Ignore) skipped;
- value expansion by +1 on the StreamID Unique ID, on SRclassID and SRclassPriority, and on the VID;
- keys `{application, AttributeType, value}`.

The non-vacuity check requires MRPDUs of both applications. The campaign arm in `crflic_mutants.py:114-122, 196-224, 254-258` plants `sr_hit_w = 1'b0` in a copy of the processor `hdl/` and builds with `PP_DIR`, which the Makefile uses as the hdl prefix (`Makefile:43, :161`).

My runs at the head use the pinned Verilator 5.050 (wrapper reports `rev v5.050`) in a disposable copy (`receipts/onevec-probes/`, script `scripts/probe_onevec.sh`):

| Run | Result |
|---|---|
| Clean leg at `044cb25f` | rc 0, `checks: 430 failures: 0`; `[ONEVEC]` reads 285 MSRP and 184 MVRP MRPDUs, 631 values, and 7 MRPDUs with two vectors of one AttributeType |
| `92100657` encoder (the only processor `hdl/` difference between the pins) | rc 1, the only failure being `no DUT MRPDU carries one attribute value in two VectorAttributes ... got=4 exp=0`: MVRP VID 2 three times and the Domain `0x6030002` once, the two processor #214 symptoms |
| Full `crflic_mutants.py` campaign | rc 0, 11 of 11, the never-merges encoder caught (`receipts/crflic-mutants-dafd49c1.txt`) |

### 6. The combined route: F1, F2, F3 and F7, three directives

- **Route figures.** `route-e44a4d20/route-figures.md` (each report hashed) and `check-dev-route-1x1.log` agree with every page and with the PR body:
  - AltSpreadLogic_high: 53,428 / 54,837 / 15,829 (21 free), Slow +0.210 / +0.069, Fast +1.520 / +0.036.
  - ExtraPostPlacementOpt: +0.112, 2 free.
  - ExtraTimingOpt: +0.018 at Slow, under the +0.030 floor, which the pages disclose.
- **Gate checks.** `check` against dev's record gives rc 0 on all three endpoints: route +207 of 500, ooc-1x1 +203 of 250, ooc-8x8 +184 of 316. After `record --write`, `check` gives rc 0 on all three, and `check-baseline` gives rc 0. My own `check-baseline` run at the head also gives rc 0.
- **Synthesis inputs after `e44a4d20`.** `git diff --name-only e44a4d20 dafd49c1` lists docs, testbench files and the baseline JSON only, so the measured image is the head's.
- **SDK loss.**
  - The firmware groups cited in HANDOFF and the PR (`gates-dafd49c1/fw0..fw3`) are timestamped 10:55 to 11:38 CET, after the 10:32 to 10:38 deletion window.
  - `fw0/fw_rv32_sdk_selftest.log` shows `SDK verified` (archive `d42680e9...`, GCC 14.3.0) under the lane's gate HOME.
  - The runs that failed during the loss are only under `receipts/superseded/`. HANDOFF, INDEX, the PR body and the issue cite them only as superseded.
- **Sweep receipts.** `sweep-dafd49c1/shard-{0..3}`: each `spec__results.json` names `head` `dafd49c1...`. The tallies are 15 + 17 + 17 + 16 = 65 suites, 0 failed, 0 timed out, and 361,195 + 1,525,512 + 284,230 + 21,575 = 2,192,512 checks with 0 failures. The docs.yml table reads "65 steps ran, 31 not run with a reason, 0 bad".
- **Evidence packet integrity.** All 753 `author-r2/` files hash to `MANIFEST.json`'s `published_sha256`. None is missing and none is unlisted; 18 entries are masked tails, each with a raw digest (`receipts/evidence-manifest-verify.txt`). The packet is integrity-listed, not cryptographically signed: commit `0976305c` has no signature.

### Other gates I ran at the head, in a disposable copy

All exit 0 (`receipts/gates-rc.txt`): `pp_resource_gate.py check-baseline`, `docs_inventory.py --check`, `check_submodule_docs.py`, `submodule_boundaries.gen.py --check`, `git diff --check 0a75aa77 HEAD`, `check_cpp_idiom.py` and `check_py_idiom.py`.

## Prior findings at this head

| Finding | Round 1 severity / lens | State at `dafd49c1` | Evidence |
|---|---|---|---|
| R790-F1 = R789-F1 | MINOR / RTL, Docs | RESOLVED. Every committed path comes from `report_timing` with a slack-equals-WNS/WHS check, round 1's receipt was corrected, and the #841 figure was removed | Delta check 2 above |
| R789-F2 = R790-S2 | MINOR / Docs (R789); SUGGESTION (R790) | RESOLVED. The share is stated on both bases with receipts, and the "no route exists" sentences are gone | Delta check 3 above |
| R789-S1 = R790-RS1 | SUGGESTION / RESIDUE | RESOLVED (`AREA_BUDGET.md:133`) | Delta check 4 above |
| R790-S1 | SUGGESTION / Tests | IMPLEMENTED: the `[ONEVEC]` check plus its planted control | Delta check 5 above |

## Findings this round

### S1 - SUGGESTION - Tests, Robustness - two `[ONEVEC]` grader branches have no input in this run

- **Where:** `tb/verilator/milan_dp/sim_crf_licence.cpp:825-833`.
- **Evidence:** `receipts/onevec-probes/run_g1.log`, `run_g2.log` (diffs `g1.diff`, `g2.diff`).
  - With the value increment removed (`kk = 0`), the clean leg false-flags exactly one MRPDU: a two-value Talker Advertise vector, events Lv Lv. So the Talker expansion is exercised once.
  - The Domain and MVRP expansion branches never see NumberOfValues > 1 on this shape, which has one domain and one VID.
  - With the Listener Ignore skip removed, the leg still passes, and the value count stays 631. So no Ignore FourPackedEvent occurs in the run.
- **Impact:** None on this adoption. Those two branches are correct by reading but have no input that would expose a slip in them.
- **Optional outcome:** a small table-driven self-test of `check_one_vector` on hand-built MRPDUs: a multi-value Domain, a VID range, a Listener vector with Ignore, and an overlap at FirstValue + k. Or a note in the README that those branches have no input on this leg.

### S2 - SUGGESTION - Tests, Robustness - "walks to its EndMark" does not require the MRPDU-level EndMark

- **Where:** `sim_crf_licence.cpp:794`, the outer loop condition.
- **Evidence:** the walk stops when fewer than two octets remain, with `ok` still true. An MRPDU whose last Message ends at the frame end, or one dangling octet before it, is therefore not counted as malformed. The MVRP AttributeList EndMark and the MSRP AttributeListLength bounds are enforced.
- **Impact:** None for the doubled-value check. The auxiliary check's name is a little stronger than what it tests.
- **Optional outcome:** do one of these:
  - require `f[off] == 0 && f[off+1] == 0` at loop exit (or accept end-of-frame explicitly and say so);
  - rename the check "every DUT MRPDU parses to its end".

### S3 - SUGGESTION - Docs - adoption sections on the pin page keep their own present tense

- **Where:** `docs/reference/SUBMODULES.md:712-716` ("The gate's fourteenth record holds this route. Against it, `check` and `check-baseline` exit 0. The standalone records stay #845's.") and `:599`.
- **Evidence:** the fifteenth record now holds the route and the standalone records. Line 712 comes from dev `0a75aa77`, unchanged by this delta. Line 599 has stayed in present tense since #843, so this is the page's existing convention, not residue introduced by this PR. The area budget's equivalent sentence was put in the past tense by `dafd49c1` (`AREA_BUDGET.md:129`).
- **Optional outcome:** "held", "exited 0" and "stayed", here or in a later page-wide pass.

### S4 - SUGGESTION - evidence packet, not repository - receipt scripts carry host-specific paths

- **Where:** `review-evidence/851-r1/author-r2/scripts/paths.sh` hardcodes the slot-wrapper location under the operator's home directory and a lane scratch clone.
- **Impact:** A cold reader cannot re-run the extraction as published. The excerpts and the refusal logic in `collect_paths.py` can still be checked without re-running it.
- **Optional outcome:** take both locations as arguments or environment variables in future packets.

**RESIDUE: none.** The new source comments in `sim_crf_licence.cpp`, `crflic_mutants.py` and `Makefile` state behaviour with issue and clause IDs (#851, processor #214, 802.1Q-2022 clauses). None names a bench lane label, lane name, review round, reviewer ID or comment ID. I found no wording defect in the PR body or the issue comments.

## Lens coverage

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #851 acceptance: sweep 65/65, firmware self-test, builder, behave, docs gates, inventory and route fit with WNS floor, against HANDOFF, the sweep `spec__results.json`, `docs-yml-table.md`, `check-dev-route-1x1.log` and the route figures. The `[ONEVEC]` layout and increments against 802.1Q-2022 10.8.1.2, 35.2.2.6, 11.2.3.1.9, 35.2.2.8 a), 35.2.2.9 and 11.2.3.1.7, as cited consistently with processor `docs/architecture/10_srp_engine.md:120-149` | R790-2 | `dafd49c1f9b79d3cc29534a9ab43d98360079d2b` |
| RTL | CLEAN | Gitlinks in the index. `git diff --name-only e44a4d20 dafd49c1` and `0a75aa77 e44a4d20` (only the processor gitlink moves a synthesis input). Processor `hdl/` difference `92100657..044cb25f` (only `KL_srp_encoder.sv`). `paths-e44a4d20/*/summary.md` and the Slow_0C setup reports. `route-e44a4d20/aslh/baseline_hierarchy.rpt:114,180`. Baseline JSON on both sides | R790-2 | `dafd49c1f9b79d3cc29534a9ab43d98360079d2b` |
| Robustness | CLEAN | `sim_crf_licence.cpp:783-877` bounds handling (truncated Message, AttributeListLength overrun, AttributeLength below identity width, missing MVRP EndMark). The `crflic_mutants.py:201` pattern-count refusal and the compile-failure refusal. Gate `tolerance`, `floor` and `ceiling` unchanged. ExtraTimingOpt below the floor is disclosed, and the selected route margin is 0.180 ns. S1 and S2 are optional | R790-2 | `dafd49c1f9b79d3cc29534a9ab43d98360079d2b` |
| Tests | CLEAN | My `receipts/onevec-probes/run_{clean,old,g1,g2}.log`, `receipts/crflic-mutants-dafd49c1.txt` (11/11), `receipts/gates-rc.txt`, the author's `onevec/*` and `gates-dafd49c1/camp/*`, and the four sweep shards | R790-2 | `dafd49c1f9b79d3cc29534a9ab43d98360079d2b` |
| Docs | CLEAN | `docs/reference/SUBMODULES.md:719-858`, `docs/design/AREA_BUDGET.md:13,126-159,195-237,255-256,663-667`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:14-177`, `CHANGELOG.md:58-91`, `docs/design/MARK_II_AREA_PLAN.md:59,939-940`, `docs/findings/README.md:25`, `docs/testing/TESTING.md:357`, `tb/verilator/milan_dp/README.md:87,532,601`, the PR body, and every figure re-derived from receipts. S3 is optional | R790-2 | `dafd49c1f9b79d3cc29534a9ab43d98360079d2b` |

## Real limits

- **No manager source bank ran at this head, and none is claimed.** Source-head execution evidence is the author's published receipts plus my focused probes above. I ran no full sweep, firmware, builder, behave, docs.yml or Vivado bank.
- **The route is not independently re-run.** Its figures and paths are checked against the author's published, hashed reports and the gate logs. The routed checkpoint and the full timing reports are published only as hashes.
- **Clause text was not re-read against the standard document this round.** The citations are consistent with the processor's reviewed architecture docs and with round 1.
- **Physical calibration NOT RUN.** No hardware or bench was used, and field skips are not hardware proof.
- **Hosted CI at the exact head is red for an infrastructure reason** (`receipts/hosted-checks-dafd49c1.txt`).
  - The first failure is `elaborate-gates-3`, step "Install the pinned sv2v release": `curl: (22) The requested URL returned error: 504`.
  - Fail-fast then cancelled the Verilator and Yosys shards. `verilator-suites`, `yosys-portability`, `docs-check` and the Union jobs report failure from that cascade.
  - No hosted job executed the suites, so this is neither evidence for the head nor against it.
- **Probe housekeeping.**
  - `crflic_mutants.py` creates its work directory under the system temp directory. It removed it on exit, and none remains.
  - A duplicate launch of that campaign was stopped before it produced a verdict. Only the single complete run is reported.
- **The review clone is unchanged.** HEAD and tree are as above, the status is empty, index and tree modes and blobs are identical (1,478 entries), the worktree equals HEAD, and the six gitlinks are as committed (`receipts/clone-integrity.txt`).

## Pending manager duties

- Re-run the hosted exact-head gates. `verilator-suites` and `yosys-portability` have no executed result at `dafd49c1`.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn. The source base is `0a75aa77`, and live dev is `0a75aa774b89ac89351700f63dd8cbb89694af6c`.
- Run post-merge containment.
- Decide whether to carry S1 to S4 forward. All are optional.

R790-2 FINISHED
