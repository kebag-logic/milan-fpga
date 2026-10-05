[R491] NEGATIVE - exact head fb4953bd61b0f6ca61ab067081e766fe37f96076

Round R491-1, external independent review of issue #658 / PR #670. Tree: `e07c63993b62098d0d475d9baa6d937b82bd1846`. Source base: `e617275074e370cec342af99b929e2588fc8d43f`.

All five lenses were applied independently. One MINOR documentation finding remains open. No functional RTL defect was demonstrated. The negative verdict follows the rule that an open MINOR leaves its lens unclean.

## Scope and authorities

Reconstruction followed AGENTS.md, CONTRIBUTING.md, docs/README.md, the public issue body and scope decisions, requirements and interfaces, the complete source diff and nine-commit history, then published executable evidence. No private lane material or another reviewer's report informed this verdict or ledger.

The [stage-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/658#issuecomment-5988843004) supersedes item 2 of the [initial ruling](https://github.com/kebag-logic/milan-fpga/issues/658#issuecomment-5988293154): identity defaults and boot clipping are required; runtime adaptation-driven pruning is withdrawn. Milan v1.2 5.4.2.7 and the unchanged SET_STREAM_FORMAT program retain BAD_ARGUMENTS when a mapping would be orphaned. IEEE 1722.1-2021 7.4.44-7.4.46 govern the map command faces. Local authorities examined include REQUIREMENTS.md sections 1, 3 and 8; SAVED_STATE_MATERIALIZATION.md sections 1, 5.2, 6.2 and 8.4; ENDSTATION_BUILDER.md D7/D8; CHANNEL_MAP_64.md sections 4-6; REGISTER_MAP.md 0x900; and the pinned processor's edit-face contract.

## Findings

### R491-1-F1 - MINOR - Docs

**Artifact:** `docs/design/SAVED_STATE_MATERIALIZATION.md:1200-1203`, especially line 1202.

**Authority/evidence:** The new paragraph says map records `0x60`-`0x7F` stay erased "until a controller edits a map." At this head an accepted controller edit does not materialize those records either. The same document at lines 172-177 says the live-write pulse becomes sticky pending and no slot holds these changes. `hdl/milan/KL_pp_shadow.sv:970-982` implements that pending path. The pinned `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv:97-109` enumerates only scalar records through `0x50 + STREAM_OUTPUT` and reserves channel maps for a later stage. The stage-2 ruling leaves map persistence in #70.

**Impact:** The authoritative restore section incorrectly presents a controller edit as the point when map records cease being erased. A reader can infer map persistence after the first edit, although this head only reports unmaterialized pending work. This changes a persistence-support claim, so it is not a wording-only RESIDUE.

**Required outcome:** Keep the boot clip distinct from the pending trigger and the future record writer. Replace the sentence beginning "The clip is not a live map write" with: "The clip raises neither `amap_edit_live_wr_p` nor map-persistence work. Controller edits raise sticky live-map pending; records `0x60` to `0x7F` remain unmaterialized in stages 1 and 2. Stage 3 supplies their writer."

**Verification:** Re-read the correction against section 1 and the pinned writer inventory; run applicable documentation gates and re-review Docs at the corrected head. No persistence implementation is requested in this lane.

### R491-1-S1 - SUGGESTION - RTL

**Artifact:** `hdl/milan/milan_datapath.sv:4358`, `:4550-4582`; processor `KL_aecp_engine.sv:2589`, `:3209-3220`, `:3281-3302`; `gen_ucode.py:2023-2027`.

**Authority/evidence:** [#640](https://github.com/kebag-logic/milan-fpga/issues/640) retains the LUT target. The shipping shape has eight boot keys and drains nine clocks after its window closes. Even an already queued valid zero-record ADD first copies eight payload bytes plus two command bytes before dispatching its edit program, which then checks lock and descriptor before phase 0. The independent queued-command probe measured phase 0 at clock 182 after window closure, with identical results when the edit wait input was tied low in a disposable copy. Both runs passed 156 checks. The static ten-byte lower bound, rather than that particular measured latency, supports considering a shipping-shape specialization.

**Impact:** There may be avoidable area in making the processor's edit wait path live on this small shape. The published comparison attributes +189 LUT to the processor instance, but does not measure this isolated alternative. Fresh synthesis was unavailable here, so a materially cheaper equivalent has not been established; this remains optional.

**Suggested outcome:** Measure a specialization tying edit wait low only where the documented minimum dispatch latency exceeds the complete sweep and drain. Preserve CSR exclusion, clipping, the writer and larger-shape arbitration. Do not extrapolate the eight-key argument to 64 keys or future map restore.

**Verification:** Exact-shape before/after synthesis, queued-at-release control, six planted controls and relevant multiport regressions. Receipts: `queued-head-run.log`, `queued-wait-low-run.log`. Reproducer: `scripts/wait_path_probe.py`, following `scripts/boot_boundary_probe.py`.

## Lens results

**[R491] PASS Conformance - `hdl/milan/milan_datapath.sv:4440-4548`, `:4629-4632`, `:5018-5042`; processor `gen_ucode.py:2172-2194`.** Identity construction uses generated dynamic-port masks, cluster bases/counts, channel bounds and each row's declared format. Input keys carry stream/channel; output ownership and exact cluster offsets identify the same identity mapping. Shipping GETs expose eight mappings per direction. During boot, live valid format rows clip the default; invalid rows select their own defaults. The supported/survives verdict and BAD_ARGUMENTS program are unchanged. REMOVE 4..7 permits narrowing; widening retains four mappings. No runtime automatic add/prune was introduced. F1 concerns the persistence explanation, not implemented protocol behavior.

**[R491] PASS RTL - `hdl/milan/milan_datapath.sv:4550-4605`, `:4639-4767`, `:1256-1264`, `:6783-6794`; processor `KL_aecp_engine.sv:451-476`, `:2334-2339`.** One cursor drives both existing AECP RAM write legs. A final sweep starts at key zero after COMPLETE/DEFAULTS or CLOSED, followed by a drain clock for the registered write pulse. CSR writes are excluded at both RAM muxes and both protocol stores. The edit face holds fallible phases; phase 5 and finish remain non-stalling and cannot precede a completed phase 0. Busy falls monotonically until reset. No new clock domain, leaf interface, parameter, CSR field or processor pin is introduced. Additional shipping state is three cursor bits and three window/drain flags. S1 remains optional pending isolated area measurement.

**[R491] PASS Robustness - `hdl/milan/milan_datapath.sv:4510-4582`; processor `KL_aecp_nvm_writer.sv:764-800`, `:1084`; `protocol_processor_top.sv:2768-2777`; `receipts/boot-probe-run.log`.** D3 ownership prevents command acceptance and controller registration during clipping; CLOSED keeps AECP held. The last format application precedes the terminal, and the parent updates the clipped image on the window-closing edge too. Invalidating the staged output row restores the full image. Reset restarts stores and writer. The additional probe checks every sampled edge during attempted CSR clears, post-release CSR persistence, a subsequent controller ADD, and two real restore drains: 153 checks pass. Generated shapes were inspected for zero input clusters, static outputs, 4x4 partitions and 8x8 output ownership. These are static boundary checks plus published regression evidence, not a fresh exhaustive bank.

**[R491] PASS Tests - `tb/verilator/milan_dp/sim_nxn.cpp:3893-4276`, `:5394-5443`, `:6614-6668`, `:6803-6835`, `:7871-7894`; `milan_dp_render/sim_tdm8_render.cpp:1831-1893`, `:2791-2835`, `:4080`; `capture_coherence/sim_dp.cpp:258`; `pp_shadow/sim_main.cpp:1464-1480`, `:1529`.** Empty-start scenarios establish and check their preconditions. Existing malformed/atomicity, format-family, divergent-row, output-map, pending and render-law assertions remain. The render route oracle comes from ruled identity and accepted commands, not RAM readback. Power-on media checks issue no map commands. Six planted defects fail their named checks; all three clean controls pass. Output narrowing is explicitly a staged-row test, not evidence of product-legal narrower output SET.

**[R491] Docs applied, UNCLEAN - `docs/design/SAVED_STATE_MATERIALIZATION.md:188`, `:595-605`, `:1195-1203`; `docs/ENDSTATION_BUILDER.md:624-643`, `:729-770`; `docs/reference/REGISTER_MAP.md:2157-2163`.** Reset/rollback name clipped identity; D7 explains REMOVE before narrowing and no refill on widening; D8 separates the unused builder image from gateware identity. CSR hold, its counter limitation and stage 3's takeover are explicit. F1 remains open.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Identity/clip functions; map faces; format verdict and SET program; ruling; focused leg | R491-1 | fb4953bd61b0f6ca61ab067081e766fe37f96076 |
| RTL | CLEAN | Boot walk/slot/write muxes, commit arbitration, phase contract; area reports; probes | R491-1 | fb4953bd61b0f6ca61ab067081e766fe37f96076 |
| Robustness | CLEAN | D3 terminal/ownership; generated bounds; rollback; held/released CSR and queued edit | R491-1 | fb4953bd61b0f6ca61ab067081e766fe37f96076 |
| Tests | CLEAN | Changed harnesses, build/pool wiring, mutation driver; six mutants and three clean controls | R491-1 | fb4953bd61b0f6ca61ab067081e766fe37f96076 |
| Docs | UNCLEAN | D3 sections 1/5.2/8.4; D7/D8; channel-map/register/walkthrough docs; inventory and PR body. F1 open | No clean covering round; applied R491-1 | fb4953bd61b0f6ca61ab067081e766fe37f96076 |

## Executed evidence

Portable commands, with SOURCE pointing to the disposable exact-head checkout and PACKET to this packet:

```sh
python3 scripts/audit_bytes.py SOURCE
python3 scripts/focused_campaign.py SOURCE PACKET --verilator PINNED_EXECUTABLE --phase clean --jobs 3
python3 scripts/focused_campaign.py SOURCE PACKET --verilator PINNED_EXECUTABLE --phase mutants --jobs 3
python3 scripts/boot_boundary_probe.py SOURCE PACKET --verilator PINNED_EXECUTABLE
python3 scripts/wait_path_probe.py SOURCE PACKET --verilator PINNED_EXECUTABLE --jobs 2
```

The requested compiler's 5.050 identity was verified before use. Foreground supervisors joined every child. Independent builds ran concurrently, using `make -j16` with four compilation workers per campaign child (three children maximum), or two for the boundary probe. Disposable trees and temporary directories stayed under scratch.

| Local run | Checks | Failures | Result |
|---|---:|---:|---|
| Dynamic-map clean control | 142 | 0 | PASS |
| Listener clean control | 258 | 0 | PASS |
| Talker clean control, quick datapath leg | 134 | 0 | PASS |
| Boot/CSR boundary probe | 153 | 0 | PASS |
| Queued minimum edit, published RTL | 156 | 0 | PASS |
| Queued minimum edit, wait-low disposable control | 156 | 0 | PASS |
| Empty identity mutant | 142 | 39 | Named defect caught |
| Missing input restore clip | 142 | 5 | Named defect caught |
| Missing output clip | 142 | 1 | Named defect caught |
| Missing crossbar writer | 142 | 12 | Named defect caught |
| Empty identity under listener check | 256 | 8 | Named defect caught |
| Empty identity under talker check | 134 | 20 | Named defect caught |

Every build/run has a raw log and exit-code receipt. Compilation failure, crash or unexplained nonzero exit did not count as a caught defect. `clean-summary.json` and `mutants-summary.json` record adjudication.

The [published executable packet](https://github.com/kebag-logic/milan-fpga/tree/d445cbd4d2dadfa01fbefc36bec82d9ffde5695f/review-evidence/658-r1) was examined after the independent diff pass. Selected receipts match its published SHA-256 manifest. Its sweep tally reports 2,149,203 checks, zero failures and four explicit field-campaign/freshness skips. These are implementation/management source receipts, not banks rerun here. The manager's reported source static/builder and native-bank passes are separate from final current-dev candidate validation.

Published area reports substantiate 43,634 to 43,769 LUT (+135) and 48,764 to 48,770 FF (+6) after opt_design, with unchanged LUTRAM, BRAM and DSP. This is OOC shipping 1x1 evidence, not routed image utilization or timing. The zero-cost stage-1 reset-image estimate does not describe the complete writer, clip and arbitration. One shared cursor and reused write legs avoid duplicate leaf reset/restore machinery. The +189 LUT processor-instance attribution and other cross-boundary changes are not additive independent savings. No fresh synthesis saving or hardware calibration is claimed.

## Limits and pending manager duties

- Prior-public-finding reconciliation was completed after this independent verdict and ledger were written. The paginated PR conversation contained only the two manager review-start notices; submitted reviews and inline review comments were empty. There were no prior public findings to resolve or retain. Receipts: `pr-comments.json`, `pr-reviews.json`, `pr-inline-comments.json`.
- The exact-head hosted snapshot records successful rtl-fast, its executed lint/elaboration jobs, four synthesis shards, wire-accountability and docs-check-no-git. Other jobs were still running; exhaustive aggregate acceptance was not claimed. The nightly physical context was skipped. The manager owns hosted/local-replica acceptance.
- Merge-tree against `fa450d301805881ad713b67521477bf042ddadfd` is clean, yielding `bf00f45c65da7bbbfece2449bd2e0970298f595e`. This proves only textual merging. The manager must validate the final candidate against live dev, including #645's overlapping datapath work when applicable.
- Resolve F1 and obtain reviewer acceptance of Docs at the corrected head. Revisit other lenses if their artifacts change. The independent internal review and final completion ledger remain pending manager duties.
- Physical calibration was NOT RUN. The nightly physical-named leg is simulation; field skips and digital passes are not hardware proof. Post-flash power-on read, physical release evidence, merge authorization, containment, issue closure and project completion remain with the manager.
- No source fixes, commits, pushes, GitHub writes, merges, author contact, full banks, container/hardware runs or other-checkout edits occurred. Exact tracked blob bytes, modes, index entries and all three required gitlinks are checked directly. Scratch holds disposable probes and is excluded from publication.

R491-1 FINISHED
