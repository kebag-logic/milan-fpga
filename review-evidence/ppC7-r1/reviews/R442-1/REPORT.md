[R442] NEGATIVE - exact head e2c7d97d158a30e44289a06a33f8ff4c5e289b87

# R442-1 internal independent review: issue #79 / PR #147 (lane C7, counters), closes #44, #78, #79

- Exact head `e2c7d97d158a30e44289a06a33f8ff4c5e289b87`, tree `2334d3020826afef3d61625b3b2f08b008c848e9` (verified, `receipts/clone_integrity.txt`).
- Diff reviewed: `c74711d45a8bbc0d6b38cb49211b26a4a6413e88..e2c7d97d`, 36 files. That is six author commits (b8df34e, 2b2af6c, cbc4816, dce60db, 315cc94, 751e1c0) on 88969246, plus the manager merge of main c74711d4 (#146).
- Authorities used:
  - The acceptance lists of #44, #78 and #79.
  - The owner decision of 2026-09-19 (#44 comment 5740180072, #79 comment 5740180166).
  - The assignment (#79 comment 5962255629).
  - The manager ruling on the GPTP_GM_CHANGED tick (#79 comment 5963704232).
  - IEEE 1722.1-2021 §7.4.42 and its counter tables (Tables 7-150 to 7-159, as the repository numbers them).
  - Milan v1.2 §5.4.2.25, Tables 5.1, 5.4, 5.6, 5.7 and 5.13 to 5.17, and Table 5.22.
- Prior public review findings on PR #147: none. The PR had no reviews and no finding comments when my pass ended, so nothing needed resolving or carrying over.

## Verdict

**NEGATIVE.** The work is substantively right:
- The RTL change is minimal and clean.
- Every suite is green.
- All 13 new mutants are killed by their named checks, with failure counts equal to the README record.
- The tick removal costs nothing that graded anything else.
- The merge is exact.
- Every acceptance item of #44, #78 and #79 is met in substance.

Two MINOR documentation and contract defects stay open:
- **F1:** the integrator guide restates the GPTP_GM_CHANGED rule as a strobe coincidence. That coincidence is not equivalent to a grandmaster identity change.
- **F2:** figures and normative tables in 01, 05 and 06 still name removed adapter ops and an in-processor counter block. The PR's own new sentences in the same documents now contradict them.

Both are cheap text fixes. Neither is only wording: F1 changes a conformance counting rule, and F2 changes figures.

## Findings

### F1 - MINOR - Conformance, Docs - the GPTP_GM_CHANGED rule in the integrator contract is not exact

- **Where:** `docs/guides/integrator.md:485-489`, in the AVB_INTERFACE duty bullet. The text says: "So count the identity change itself, the update for which you raise `gm_change_i` **and** `gsi_asp_chg_i`, never every `gm_change_i`."
- **Authority and evidence:** Milan v1.2 Table 5.1 counts gPTP grandmaster changes, and the manager ruling (#79 comment 5963704232) excludes domain-only changes. The guide's own §6 (`integrator.md:343-348`) and 06 §6.10 (`06_aecp_engine.md:850-855`) say:
  - `gsi_asp_chg_i` is raised for *any* changed PathTrace, a tail-only change included.
  - A grandmaster identity update raises both strobes only "normally".
  - A consumer may publish no path.
  
  So the "both strobes" coincidence is wrong in both directions:
  - An update that changes the domain and the path tail together raises both strobes with no grandmaster change, so it over-counts.
  - An integrator that publishes no PathTrace never raises `gsi_asp_chg_i`, so it under-counts every grandmaster change.
  
  Every other statement of the rule is the exact identity comparison:
  - `integrator.md:466` (table row: "each grandmaster identity you publish on `gm_id_i` that differs from the one in force").
  - `06_aecp_engine.md:612` (F06.15).
  - The harness store (`tb/pp_top/sim_main.cpp:930-937`, `d->gm_id_i != itf.gm_q`).
  - The reference parent (`hdl/milan/milan_datapath.sv:4965` at milan-fpga dev cdf49d1a, `cfg_adp_gptp_gm != gsi_gm_q_r`).
- **Impact:** Lens item (1) asks for an exact `ctr_*` contract for every counter. An integrator who follows the bullet's operational recipe reports a Milan-mandatory AVB_INTERFACE counter (mask `0x20`, block offset 20) wrongly. No check in this repository can catch it, because the harness implements the other rule.
- **Required outcome:** State the rule only as the identity comparison: count when the published `gm_id_i` differs from the identity in force, at the update you publish. Drop the strobe-coincidence appositive, or state explicitly that neither strobe nor their coincidence identifies a grandmaster change.
- **Verification:** Read `integrator.md` §7.1. The bullet must agree with `:466`, F06.15 and `sim_main.cpp:935`. `make check` stays rc 0.

### F2 - MINOR - Docs, Conformance - removed adapter ops and an in-processor counter block remain in 01, 05 and 06 figures and tables

- **Where** (`receipts/stale_names.txt`):
  - `docs/architecture/01_overview.md:222, :238, :251`: F01.3 still draws `ctrs["counters"]` inside the 06 AECP block, fed by `adapters["srp/maap · gptp · avtp · mclk adapters · side-port · nvm port"]` (`adapters --> ctrs`).
  - `01_overview.md:96`: the block table says "Event router | fan-out of adapter/SM events to counters". The PR's own 03 §5 edit now says "No event feeds a counter here".
  - `docs/architecture/05_acmp_engine.md:286`: action legend A8 of F05.3 still performs `avtp.INPUT_DISABLE`.
  - `05_acmp_engine.md:106`: the flowchart still sends "declare/withdraw, configure/enable" to `srp + avtp adapters`. The PR's new 05 §2 text at `:23-26` says "no `avtp` op exists".
  - `docs/architecture/06_aecp_engine.md:469`: the F06.14 SET_CLOCK_SOURCE row still ends `→ mclk.SET_CLOCK_SOURCE →`. The PR's new 06 §2 text at `:25-27` says "no `avtp` or `mclk` op exists". The PR body maps SET_CLOCK_SOURCE to `aecp_clk_src_index_o`.
- **Authority and evidence:**
  - The owner decision (2026-09-19) and #79 acceptance 3: no counter bank in the processor.
  - #44's re-scope (1): remove the in-processor counters contradiction.
  - #78: the gptp/avtp/mclk class-B ops do not exist on the landed top.
  - The PR body states that "01, 03 and 06's stale 'counters subsystem' rows and nodes are corrected" and that "05 (§2, A15, the BIND_RX sequence) ... follow". The tree does not carry that through for the items above.
  - #78 acceptance 1 is strictly scoped to 02, and 02 is clean: all 56 port names in 02 §4.3 to §6 exist on the top (`receipts/port_names_02.txt`). This finding is about the PR's declared consistency sweep and the GAP-04 and GAP-05 dispositions in the rest of the architecture.
- **Impact:** Normative figures (F01.3, F05.3's action legend, the 05 executor flowchart, F06.14) contradict the landed top and the GAP-05 decision, beside new sentences that deny them. A reader is told both that the processor keeps a counters block fed by adapters and that it keeps none, and that `mclk`/`avtp` ops exist and that they don't.
- **Required outcome:**
  - In F01.3, remove the `ctrs` node and the `adapters --> ctrs` edge, or redraw them as the `ctr` read face. Rename the adapters node to the landed faces.
  - Correct `01:96`.
  - Rewrite A8 as dropping the bound view (`acmp_bound_o` falls), as A15 was rewritten.
  - Relabel the 05 flowchart edge to the srp ops plus the bound-view levels.
  - Replace `mclk.SET_CLOCK_SOURCE` in F06.14 with the `aecp_clk_src_index_o` level.
  - Optionally, update the RTL comments `hdl/acmp/KL_pp_acmp_listener.sv:25, :184, :188`, which predate this PR, in the same pass.
- **Verification:** `scripts/stale_names.sh <clone>` reports no `docs/` hit (the optional RTL comments aside). `make check` stays rc 0.

### S1 - SUGGESTION - Docs - a stale GET_COUNTERS paragraph that predates this PR

`06_aecp_engine.md:1136-1146` still says E_GCTRS is "branch-free — 16 µops, no status arm" and that ENTITY answers `counters_valid` 0. The landed program has a locate, a `BR_STATUS` miss arm and a zero-body loop (`hdl/aecp/ucode/gen_ucode.py:823-845`), and ENTITY is refused NOT_SUPPORTED (06 §6.6, `:563-567`). This is outside the diff, so it is not a finding of this PR. Two other small stale phrases could be fixed in the same pass:
- `docs/10_RESOURCE_AND_EFFORT.md:404-406` ("the µCPU serves and latches counters").
- `hdl/top/protocol_processor_top.sv:366-368`, which names only Table 5.6.

### S2 - SUGGESTION - Tests - `ctr_mutants.py` has no `--jobs`

The new driver runs its 14 builds serially (`tb/pp_top/ctr_mutants.py:134-136`, Makefile target `ctr-mutants`). The merged main (#146) gave the eight other drivers `--jobs N` under the owner's wall-time rule. The arms are independent: the reviewer's parallel re-run (`scripts/ctr_mutants_parallel.py`, five at a time) reproduced every verdict and failure count.

## Focus items

1. **The `ctr_*` contract (integrator.md §7.1) against IEEE §7.4.42 and Milan §5.4.2.25.**
   - Ports, the five read-face rules, and the per-type masks and quadlets all match the RTL:
     - AVB_INTERFACE `0x23` at quadlets 0, 1 and 5. The optional `0x04`/`0x08`/`0x10` bits are listed.
     - CLOCK_DOMAIN `0x03`.
     - STREAM_INPUT `0xF3F`, or `0xFFF` with the IEEE-only TIMESTAMP_VALID/NOT_VALID.
     - STREAM_OUTPUT `0x1F` with the Δ9 compacted layout.
   - The RTL evidence for that:
     - Type gate: `KL_aecp_engine.sv:3342-3345`.
     - Locate first: `gen_ucode.py:824-825`.
     - Mask first, then quadlets 0 to 31 in order: `gen_ucode.py:827-831`, `KL_aecp_engine.sv:2173-2177`.
     - Hold semantics: `:2331-2332`.
     - Watchdog: top `DESC_MEM_TMO_CYC_P` into the engine's `MEM_TIMEOUT_CYC_P`, `protocol_processor_top.sv:3694`.
     - Notify slots and window: `KL_aecp_notify.sv:385-392, 491-507, 1033-1039, 1233-1237`.
   - The wrap, reset and observation rules agree with the pre-existing F06.15 and with the reference parent. The parent's `KL_talker_diag_ctx.sv` quotes Milan's "end of every observation interval" text for FRAMES_TX, MEDIA_RESET and TIMESTAMP_UNCERTAIN.
   - The change-strobe rules and the slot set are exact, and the tie-off row is honest.
   - Open: the GPTP_GM_CHANGED bullet (F1).
2. **K9 to K16** (`tb/pp_top/counters_phases.hpp`).
   - Expectations are written from the tables, never read back:
     - Byte-exact bodies with distinct counts 3/2/5 at block offsets 0, 4 and 20 (K11), which meets #44 acceptance 3.
     - The Table 5.1 and 5.7 invariants at every sample (K10, K16).
     - NO_SUCH_DESCRIPTOR without a face read (K12).
     - One push per registered controller with the counts of its moment (K13).
     - Coalesced late push: nothing before 850 ms, one push at 900 ms or later, never replayed (K14).
     - Per-descriptor windows (K15).
   - The precise 1 s bound (999 ms or more) is graded for AVB_INTERFACE 0 and CLOCK_DOMAIN 0 by the existing storm check ST2b (`notify_phases.hpp:1099-1100, 1209-1213`). K14's 900 ms bound is therefore not the only guard.
   - The domain-only arm grades the harness's integrator store. That is correct by design, since the processor no longer counts anything.
   - Reviewer re-run (`receipts/ctr-mutants/summary.txt`): control PASS with 23 checks. All 13 arms KILLED by their named check, with failure counts 9/3/17/8/1/5/6/1/2/5/7/6/10, identical arm by arm (and check by check) to the `tb/pp_top/README.md` record.
   - Two extra reviewer probes were also KILLED:
     - `rv-store-link-down-uncounted`: the store never counts LINK_DOWN. 9 failures, named K10.
     - `rv-notify-ckd-as-avb`: a CLOCK_DOMAIN strobe marks the AVB_INTERFACE slot. Named K16.
3. **Tick removal.**
   - The RTL removes exactly the flop, its reset and its port (`KL_adp_engine.sv`), plus the top's `adp_gm_tick_nc_w`.
   - Lint is 41 of 41 clean.
   - The 39 removed adp_engine checks are P5's tick count plus the per-cell tick check of the 38 non-'C' F04.2 cells (45 cells, 7 'C' cells return early at `tb/adp_engine/sim_main.cpp:1335`). Each removed CHECK read only the tick counter.
   - P5's 4-clock loop became `idle(4)` (`:446`), the same four ticks.
   - The tally fell from 1,367 (base `c74711d`) to 1,328 at head.
   - The adp_engine mutation campaign: 2 controls PASS and 30 of 30 arms KILLED. Each arm's failure count equals the README record, which this PR left unchanged, so no arm's kill depended on the removed checks.
   - Out-of-context cost 0: the author's measurement (`syn/ooc/README.md`), consistent with an unconnected flop already trimmed. I did not re-measure it (see limits).
4. **02 §4.3 to §4.5, §5 and F02.10 (#78).**
   - Each instance carries a landed-shape table. All 56 port names in 02 §4.3 to §6 exist on `protocol_processor_top`, with the stated widths.
   - The gsi word positions in F02.10 match 06 §6.10.
   - No removed op or event is named in 02 (`receipts/stale_names.txt`).
   - #78 acceptance 3 and 4 were met on main by #133 (`tb/srp_top/sim_main.cpp` Q1 to Q4, `:1710-1790`). #29 was closed as a duplicate of #108, which #133 completed.
   - The stale names outside 02 are F2.
5. **Redundancy.** Nothing narrows the path:
   - The face stays keyed by `{descriptor_type, descriptor_index}`, and the guide says one bank per AVB_INTERFACE at its own index.
   - The removed port was per-interface and fed nothing.
   - The single AVB_INTERFACE and CLOCK_DOMAIN notify slots predate this PR and are recorded for processor #69.
6. **The merge.** The 3-way merge recomputed with `git merge-file` is byte-identical to `e2c7d97` for both READMEs, with no conflict. The other 13 main-side and 34 lane-side files equal their sides (`receipts/merge_check.txt`).

## Acceptance, issue by issue

- **#79:**
  1. The decision is recorded in 00 §7 (the F00.2 GAP-05 row) and 00 §5.
  2. Not applicable.
  3. integrator.md §7.1 gives the per-type contract (exactness: F1). REQ-AEM-019 and REQ-NET-004 point at it, and F07.10 is corrected.
  4. 06 §6.6 has no "tracked separately" and describes the landed push.
- **#44:**
  1. The decision is in 02 and 06. The 02 event catalog and 04 §2 no longer list counters (other places: F2).
  2. The guide documents the face and the AVB_INTERFACE duty, and the tick is removed (ruling 5963704232).
  3. K11 meets it.
  4. Not applicable.
- **#78:**
  1. Met for 02.
  2. Met.
  3. and 4. Met on main by #133 / #108.

## Commands run (all waited on in the foreground; pinned simulator 5.050, wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`, `receipts/tool_identity.txt`)

| Run | Result |
|---|---|
| `scripts/sweep_parallel.sh` on a `git archive` of head: the `run_suites.sh` gates plus every `tb/*` suite, 10 at a time | rc 0: gates rc 0, 33 suites, **1,019,111** checks, 0 failing. pp_top 9,191 (K-AVB 23), adp_engine 1,328 (`receipts/sweep-head/`) |
| Base `c74711d`: `tb/adp_engine`, `tb/pp_top` | 1,367 and 9,168, so the deltas are −39 and +23 (`receipts/base-c74711d/`) |
| `scripts/ctr_mutants_parallel.py` (in-tree arms, kill rule and patches; copy built with `-j 3`) | 16 of 16 as required: control, 13 in-tree arms, 2 reviewer probes |
| `tb/adp_engine/mutants.py` | 32 checks: 32 PASS (`receipts/adp-mutants/`) |
| `./scripts/lint_hdl.sh`, `make check`, `gen_matrix.py --check` | rc 0 each: 41 LINT OK; 18 wavedrom, 1,087 links, 115 REQ / 17 GAP, 94 rows 0 untested, 27 parameters (`receipts/gates/`) |
| `scripts/merge_check.sh`, `scripts/port_names_02.py`, `scripts/stale_names.sh` | as above, rc 0 each |
| Hosted check runs at the exact head, read only | portability and docs-gates success (two contexts each); suites in progress when read (`receipts/hosted_check_runs.txt`). No acceptance claimed |

After the probes, the clone was verified untouched at the exact head:
- HEAD and tree are exact, and `git status --ignored` is empty.
- Worktree equals index, which equals HEAD; `write-tree` gives `2334d302…`.
- The mode, blob and path digests of the index and HEAD are equal.
- This tree has no gitlinks and no `.gitmodules`.

All probes ran in disposable copies under `scratch/`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | integrator.md §7.1 against IEEE §7.4.42 and Tables 7-150 to 7-159 and Milan §5.4.2.25 / Tables 5.1, 5.4, 5.6, 5.7, 5.13 to 5.17, 5.22; 00 GAP-04/GAP-05 and the REQ rows; 02 §4.3 to §6 against the top's ports; parent counter sources at cdf49d1a (read only) | R442-1 | e2c7d97d158a30e44289a06a33f8ff4c5e289b87 |
| RTL | CLEAN | `KL_adp_engine.sv` and `protocol_processor_top.sv` diff; the GET_COUNTERS path in `KL_aecp_engine.sv` and `gen_ucode.py`; the `KL_aecp_notify.sv` counter slots and window; lint 41 of 41 | R442-1 | e2c7d97d158a30e44289a06a33f8ff4c5e289b87 |
| Robustness | CLEAN | read-face hold and watchdog, the tie-off row, unslotted strobes ignored, redundancy keying, harness store reset (`sim_main.cpp:1919-1921`), merge exactness | R442-1 | e2c7d97d158a30e44289a06a33f8ff4c5e289b87 |
| Tests | CLEAN | `counters_phases.hpp` K9 to K16, K4c/K4d, the ST2b window bound, `ctr_mutants.py` and its 13 patches (re-run, plus 2 reviewer probes), adp_engine's 39 removed checks and its campaign (re-run), full sweep and base tallies | R442-1 | e2c7d97d158a30e44289a06a33f8ff4c5e289b87 |
| Docs | UNCLEAN (F1, F2) | 00, 01, 02, 03, 04, 05, 06, 07, 08, 09 diffs and their unchanged neighbours; integrator.md §6, §7 and §7.1; both merged READMEs; `syn/ooc/README.md`; PR body claims | R442-1 | e2c7d97d158a30e44289a06a33f8ff4c5e289b87 |

## Real limits

- The specification PDFs are not in the repository. I checked clause and table numbers for consistency with the repository's own earlier citations and with the reference parent, not against the printed standards.
- I did not re-measure the out-of-context synthesis. No synthesis tool was run. The zero delta is taken from the author's record plus the structural argument: the flop fed only an unconnected wire.
- I did not run the donor bank (9) or the parent consumer set (16). I only checked that the two adoption patches (sha256 `67bcd698…` and `aa5a88eb…`, from the public evidence at milan-fpga c0212c4d) touch neither the tick nor the `ctr_*` face, and that the parent's `milan_datapath.sv` names no `gm_changed_tick`.
- The public evidence at c0212c4d holds only the author archive (a manifest of four files). I found no manager bank receipts there or in the issue and PR comments, so I could not inspect the manager's source, static, builder or native bank results.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Run the donor bank (9) and the parent consumer set (16) at this head with `parent-adoption-c4c6` then `c8`, and publish their receipts.
- Build the final current-dev candidate at the merge turn (source base c74711d4, live dev cdf49d1a).
- Hosted and act acceptance: suites were still in progress when read.
- Carry F1 and F2 to the author. Both need only text and figure edits; no RTL or test change is required.

R442-1 FINISHED
