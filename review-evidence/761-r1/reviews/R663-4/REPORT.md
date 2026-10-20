[R663] POSITIVE - exact head f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d

Round R663-4. Internal, cleared-context, independent review of kebag-logic/milan-fpga PR #767 (issues #761 and #762). Tree `c1c7c13bd84fa4d6544783ab82bfe09fa7483c6a`. Source base `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. The previously reviewed head is `d30a208d44d5868cc356e6a8b7abc89b062ca9bd`.

## Verdict

All five lenses were applied to the round-4 delta at this head, and all five are CLEAN. There is no open BLOCKER, MAJOR or MINOR.

R663-3-F1 and R664-3-F1 are resolved. Both were the same MINOR: `[762-DP]` ran on no elaboration of the shipping AX7101 shape. R663-3-R1 is resolved.

This round records:
- two new RESIDUE items, both wording only: R663-4-R1 and R663-4-R2;
- two new SUGGESTION items: R663-4-S1 and R663-4-S2;
- four earlier suggestions, carried forward unchanged.

## Reconstruction

I read the following, in this order:
1. AGENTS.md and CONTRIBUTING.md.
2. The round-4 assignment (#767 comment 6283915359) and the review start (#767 comment 6285155662).
3. The two #762 scope rulings (#762 comments 6260976223 and 6265746720).
4. The entity config `configs/endstation_ax7101_1x1_tdm8.yaml`, `sw/litex/milan_soc.py:664-677,1060-1104` and `sw/litex/build.sh:195,378`.
5. The delta `d30a208d..f3fef856` (`round4.diff`, 3 files, +92/-5).
6. The tb Makefile recipes: `tb/verilator/milan_dp/Makefile:68-76,90-102,236-249,314-331,522-533,567,605-645`.
7. The live PR body (`receipts/pr767-body-live.md`).
8. The posted round-4 REVIEW READY on #761 (comment 6285115002).
9. The author's round-4 receipts in evidence tree `55c754698d494aaa17cf76f96229f9822c123c3a`.

I did not read the lane HANDOFF files. I read the round-3 review findings (R663-3 #767 comment 6283905996, R664-3 #767 comment 6275950683) only after my own pass over the diff and my probes were complete. I read no other round-4 review.

Evidence authentication: I downloaded 44 round-4 receipt blobs. For each one, the git blob hash of the downloaded bytes equals the evidence tree's blob id (`receipts/evidence/author-r4-blobcheck.txt`). The posted REVIEW READY matches the packet copy except for trailing whitespace (`receipts/evidence/review-ready-posted-vs-packet.diff`).

## The delta

- `tb/verilator/milan_dp/sim_nxn.cpp`
  - `:3036` adds the call `stopped_input_law_on_the_shipping_geometry()`. It sits inside `#ifdef DYNMAP_DEFAULT_TB` (`:3031`).
  - `:4564-4621` adds the comment and the function, inside the `#ifdef DYNMAP_DEFAULT_TB` block that opens at `:4326` and closes at `:4622`. The function:
    - prints 22 elaborated parameters;
    - checks `N_STREAMS == 1`;
    - checks `CRF_SNK_IDX_C == N_STREAMS && ADP_LISTENER_SINK_C == N_STREAMS+1`;
    - resets the datapath, sets the entity id and runs the boot restore walk;
    - then runs the existing TRAP-1 bind, the 5.3.8.7 discard section and `[762-DP]`, unchanged.
  - Every added line is under `DYNMAP_DEFAULT_TB`, so the preprocessed source of every other `sim_nxn` leg is unchanged.
- `tb/verilator/milan_dp/dynmap_probes.vlt:24-41` adds `public_flat_rd` for the 22 parameters, as read-only constants.
- `tb/verilator/milan_dp/README.md:82,778-780,1190-1209` changes the `obj_dynmap` row, the section intro and the `[762-DP]` paragraph.
- No RTL file, Makefile, CI command table or generated artifact changed.

## Independent probes

The script is `scripts/dynmap_762dp_probe.sh`. It works on a byte copy of this clone, `.git` included, under the scratch area. It plants one replacement of `milan_datapath.sv:6308` and builds through the Makefile's own `dynmap-build` recipe. That recipe is the `obj_ax1x1` argv on `SHAPE_AX1x1` with `NSTREAMS_TB=1`. The script then runs `./obj_dynmap/Vmilan_dp_dynmap` from the leg directory.

The simulator is Verilator 5.050, through the scoped pinned wrapper (`receipts/simulator-identity.txt`). The four variants ran concurrently, at 4 build jobs each. Summary: `receipts/probe/SUMMARY.txt`.

| Variant (`:6308` `.stopped_i`) | build rc | run rc | checks / failures | Failing checks (complete list) |
|---|---:|---:|---|---|
| clean `acmpl_stopped_v_w[N_STREAMS-1:0]` | 0 | 0 | 199 / 0 | none. 15 `[762-DP]` `[ok]`: the 2 geometry guards and the 13 case checks |
| `'0` (tie-off) | 0 | 1 | 199 / 2 | `[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0` (got 1); `[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0` (got 1) |
| `acmpl_stopped_v_w[N_STREAMS:1]` (the CRF sink's level at N=1) | 0 | 1 | 199 / 2 | the same two |
| `acmpl_bound_v_w[N_STREAMS-1:0]` | 0 | 1 | 199 / 1 | `[762-DP] 4 started gap: STREAM_INTERRUPTED +1` (got 0) |

- The elaborated-parameter lines are byte-identical across all four runs: sha256 `d2094321fbb6f594ec13bbc5332fa7f2a284a663700daf5605f08e908eaf5e6f`. This is the same digest as the author's `r4-shape/same-elaboration.txt`. So all three mutants ran on the elaboration the clean leg ran on.
- In the tie-off run, every check that is not `[762-DP]` carries the same name as in the clean run.
- The clean leg takes 3.53 s wall time (`receipts/probe/clean/run-time.txt`), so the tail adds negligible time to the sweep.
- The Verilator warning classes and counts are identical to the author's clean build receipt: GENUNNAMED 32, PROCASSINIT 24, SYNCASYNCNET 1, VARHIDDEN 4. There are no compiler diagnostics on `sim_nxn.cpp`.

### Elaborated parameters against the entity definition

I regenerated the shipping design argv from the config with the repository's own builder: `python3 -I sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml -o <scratch>`.
- Its `soc_params.json` argv is byte-identical to the author's `r4-shape/sweep_opts_ax7101.OPTS.txt`.
- Its `adp_shape_defaults.svh` equals the tracked `configs/generated/endstation_ax7101_1x1_tdm8/gen` copy on every non-comment line.
- Receipts: `receipts/shape/`.

I mapped that argv through `milan_soc.py`:
- The optional blocks default to present (`:664-677`), and only `--no-i2s-playback` and `--no-render-lpf` prune.
- `AUDIO_IF_WORD_BITS_P` and `AUDIO_IF_FS_HZ_P` are withheld at their defaults of 32 and 48000 (`:1072-1085`). The config's `word_length_bits: 24` is 24 bits in a 32-bclk slot.
- `AUDIO_IF_CLK_HZ_P = 2*8*32*48000 = 24,576,000`.

The logged values then agree with the shipping definition on 19 of 22 parameters: N_STREAMS 1, ADP_TALKER_SRC_C 2, ADP_LISTENER_SINK_C 2, CRF_SNK_IDX_C 1, TALKER_WIRE_CHANS_P 8, AUDIO_IF_SLOTS_P 8, AUDIO_IF_MASTER_P 1, AUDIO_IF_I2S_PAIR_P 0, AUDIO_IF_WORD_BITS_P 32, AUDIO_IF_FS_HZ_P 48000, AUDIO_IF_CLK_HZ_P 24576000, LOOPBACK_P 1, MCSERVO_P 1, LTAP_P 1, MAAP_P 1, I2SPB_P 0, RXFILT_P 1, LPF_P 0, DPROBES_P 1.

The other three are the named verification substitutes:

| Parameter | Leg | Shipping |
|---|---:|---:|
| `MILAN_CLK_FREQ_HZ` | 100,000,000 | 50,000,000 |
| `GPTP_PLANE_EN_P` | 0 | 1 |
| `AUDIO_IF_RENDER_SLOTS_P` | 0 | 8 |

This matches the author's table, and no other parameter differs.

## Findings

### R663-4-R1 RESIDUE: the README's last `[762-DP]` sentence lost its antecedent

- **Lenses:** Docs.
- **Where:** `tb/verilator/milan_dp/README.md:1208-1209`.
- **Why:** The delta inserts "On `obj_dynmap`, sink 1's level is the CRF sink's." between "With that port tied to `'0` or fed sink 1's level, ... each count." and "With it fed the bound level, the gap after START does not count." Now "it" reads as "sink 1's level", but the sentence means the port. This is wording only. The probe confirms the behaviour the sentence describes.
- **Exact fix:** Replace "With it fed the bound level, the gap after START does not count." with "With the port fed the bound level, the gap after START does not count."

### R663-4-R2 RESIDUE: the PR body puts `obj_nxndv` on the Arty 4x4 entity itself

- **Lenses:** Docs.
- **Where:** PR #767 body, Round 3 table, row `336a6f6a`: "`obj_nxn`, `obj_nxndv` and `obj_nxn4c` on the retired Arty 4x4 entity".
- **Why:** `obj_nxndv` elaborates `gen_divergent/gen/adp_shape_defaults.svh` (`Makefile:82,357-358,614`). `gen_divergent_shape.py` generates that header from the Arty 4x4 config and gives input row 1 the 96 kHz base. So the leg runs a generated divergent copy of that entity, not the entity. The "not a shipping shape" conclusion is right, and nothing measured depends on this wording.
- **Exact fix:** "`obj_nxn` and `obj_nxn4c` on the retired Arty 4x4 entity, `obj_nxndv` on a generated divergent copy of it (input row 1 at the 96 kHz base), and `obj_nxn8` on the AX7101 8x8 entity at the default geometry."

### R663-4-S1 SUGGESTION: the `obj_ax1x1` baseline table has no row for the pruned render lane

- **Lenses:** Docs.
- **Where:** `tb/verilator/milan_dp/README.md:121-132`, read against the new `:1196-1198`.
- **Why:** The new paragraph calls "the render lane pruned" an `obj_ax1x1` verification substitute, and the logged `AUDIO_IF_RENDER_SLOTS_P` is 0. The table that lists the `obj_ax1x1` substitutes names the clock and gPTP but not the render lane. "I2S playback / render LPF" there is a different block, and the shipping value of that row is the same as the leg's. The table predates this PR. The substitute is stated in the new paragraph and in the PR body, so this is optional.
- **Suggested change:** Add the row `| Render lane | Pruned (AUDIO_IF_RENDER_SLOTS_P 0; deployment 8); graded in tb/verilator/milan_dp_render |`.

### R663-4-S2 SUGGESTION: the `obj_dynmap` sweep banner names only #658

- **Lenses:** Docs.
- **Where:** `tb/verilator/milan_dp/Makefile:567` (`CASE_OPTIONS_dynmap`) and its copies in `ci/image/command-table.json:2859,5915`.
- **Why:** The leg now ends with `[762-DP]` (#762), and the banner reads "#658 the power-on audio maps, Milan 5.4.2.7 and a restored format". The author kept the banner deliberately, so the CI command table stays unchanged. The README row and section intro already say the leg runs `[762-DP]`.
- **Suggested change:** Optional. If the command table is regenerated for another reason, add "then #762 on a fresh boot" to the banner.

## Prior findings at this head

| Finding | Status at f3fef856 | Evidence |
|---|---|---|
| R663-3-F1 MINOR (Conformance, Robustness, Tests, Docs) | **Resolved** | Part 1, the case on the shipping shape: it runs on `obj_dynmap`, which is `SHAPE_AX1x1` plus the `obj_ax1x1` argv (`Makefile:324-331`). Part 2, the geometry: its parameters are logged and agree with the regenerated entity definition except the three named substitutes. Part 3, the mutants: the clean leg passes, and on the same elaboration the tie-off and the `[N_STREAMS:1]` form each fail named `[762-DP]` checks. The bound-level form also fails its named check. Part 4, the wording: the PR body no longer calls `obj_nxn4c` shipping. The round-3 mutant script's header now reads "endstation_arty_4x4, the retired Arty 4x4 entity at 4 wire channels; not a shipping shape". It is published at `author-r4/receipts/r3-mutants/dp_stopped_mutants.sh` (sha256 `551242c2...`); against the round-3 copy (`b2d85578...`) only the header changes. The round-4 script `dynmap_762dp_mutants.sh` names its shape and the substitutes accurately. |
| R664-3-F1 MINOR (same cause) | **Resolved** | Same evidence. The verification R664-3 required is now met: stopped gap SEQ_NUM_MISMATCH +1 with STREAM_INTERRUPTED +0; stopped silence MEDIA_UNLOCKED +1 with STREAM_INTERRUPTED +0; after START and relock, a gap counts STREAM_INTERRUPTED +1. |
| R663-3-R1 RESIDUE (stale hosted citation) | **Resolved** | Status reads "every check run at `d30a208d` succeeded, with the nightly physical gPTP job skipped". Known limitations reads "it succeeded at `d30a208d`". My query of the hosted check runs at `d30a208d` shows 63 success and 1 skipped, the skipped one being `Physical gPTP (nightly and manual)` (`receipts/hosted/check-runs-d30a208d.tsv`). |
| R663-3-S1 SUGGESTION (only bit 0 of `stopped_i` graded) | Retained, optional | Not assigned and not taken. On the shipping N=1 shape this class of defect cannot occur. |
| R663-2-S1, R663-1-S1, R664-2-S2 SUGGESTION | Retained, optional | The delta touches none of their artifacts. |
| Earlier resolved findings (R663-1-F1..F3, R664-1-F1..F2, R663-2-F1..F3, R664-2-R1) | Resolved, carried | The delta changes no RTL, no engine harness and no CI artifact they depend on. |

## Comment rule

The new source comments are `sim_nxn.cpp:4564-4571` and `dynmap_probes.vlt:24-25`. They state behaviour and reason with #762 and the 5.3.8.7 clause. They name the `[762-DP]`, `[DYNMAP]` and TRAP-1 check tags of the harness's own output. They carry no bench lane label, lane name, review round, reviewer ID or comment ID. No new instance.

Two related observations, neither a new source-comment instance:
- The modified README line `:779` keeps the pre-existing "(comments 5988293154 and 5988843004)". It is documentation prose, re-flowed.
- The existing `dynmap_probes.vlt:10` "(R490-1 F1)" falls under #746.

## Lens results

```text
[R663] PASS Conformance - sim_nxn.cpp:3031-3036,4564-4621; Makefile:68,243-249,324-331; configs/endstation_ax7101_1x1_tdm8.yaml; regenerated soc_params.json argv; #762 rulings 6260976223/6265746720; assignment 6283915359 items 1-3 - the [762-DP] count law runs on the shipping AX7101 1x1 TDM8 elaboration and grades the ruled counts; every assignment item is met
[R663] PASS RTL - hdl/milan/milan_datapath.sv:1633,1656,1721,1756,6307-6308 (unchanged by the delta); dynmap_probes.vlt:24-41 (read-only constants on a verification elaboration); probe/*/elaborated.txt - no RTL change; at N=1 the slice [N_STREAMS-1:0] selects AAF input 0 and [N_STREAMS:1] selects the CRF sink, as the probe shows
[R663] PASS Robustness - probe/{tie0,sink1,bound}; sim_nxn.cpp:4609-4621 fresh reset and restore walk after [DYNMAP] - the configuration-dependent wrong-vector case (the CRF sink adjacent at N=1) is now caught on the shape where it arises; the tail re-boots, so [DYNMAP] state does not leak into the graded counts ([BOOT] walk check passes)
[R663] PASS Tests - receipts/probe/SUMMARY.txt; author r4-mutants and r4-dynmap-mutants receipts (blob-verified; dynmap-mutants 16/16) - the clean leg passes 199/0; each plant fails exactly its named checks on one elaboration (identical parameter digest); the geometry guards keep the sink1 plant meaningful; other legs' preprocessed sources are unchanged
[R663] PASS Docs - tb/verilator/milan_dp/README.md:82,778-780,1190-1209; PR #767 body (receipts/pr767-body-live.md); REVIEW READY 6285115002; r3/r4 mutant script headers - the shapes and substitutes are named accurately; the only remaining defects are wording (R663-4-R1, R663-4-R2)
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sim_nxn.cpp:3031-3036,4564-4621`; `Makefile:68,243-249,324-331`; entity config and regenerated argv; #762 rulings; round-4 assignment | R663-4 | f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d |
| RTL | CLEAN | `milan_datapath.sv:1633,1656,1721,1756,6307-6308`, unchanged since d30a208d (covered clean by R663-3 there); `dynmap_probes.vlt:24-41`; probe elaborations | R663-4 | f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d |
| Robustness | CLEAN | N=1 CRF-sink adjacency; tie0/sink1/bound probes; the fresh boot after `[DYNMAP]` | R663-4 | f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d |
| Tests | CLEAN | `receipts/probe/*`; author `r4-mutants`, `r4-focused`, `r4-dynmap-mutants`, `r4-shape` (blob-verified) | R663-4 | f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d |
| Docs | CLEAN (RESIDUE R663-4-R1/R2 to the checklist) | `README.md:82,121-132,778-780,1190-1209`; PR body; REVIEW READY; mutant script headers | R663-4 | f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d |

## Real limits

- I ran only the `obj_dynmap` leg: clean plus three plants, built from byte copies of this head. I did not re-run the other `milan_dp` legs, avtp_rxmon, crf_rx, `make dynmap-mutants`, the docs gates, the builder bank, Yosys or route-1x1. For the other `sim_nxn` legs, the reason is that every added `sim_nxn.cpp` line sits under `DYNMAP_DEFAULT_TB`. For `dynmap-mutants` I verified the author's receipt (16/16, blob-verified), and I did not execute it myself.
- Hosted CI at `f3fef856` was in progress when I looked (2026-10-20T06:59:00Z): 11 success, 33 queued or in progress, `Physical gPTP` skipped (`receipts/hosted/check-runs-f3fef856-snapshot.tsv`). That is observation only. The `d30a208d` run is complete: 63 success, 1 skipped.
- There is no manager source bank at this head, and I claim none. Physical calibration was NOT RUN. Skipped field and hardware contexts are not hardware proof.
- The clone was restored and verified (`receipts/checkout-integrity.txt`): HEAD, tree and index write-tree are all `c1c7c13b...`; the worktree and index equal HEAD; there are no untracked or ignored files; the six gitlinks are unchanged. The bytecode caches that my builder run created were removed.

## Pending manager duties

- Hosted and act acceptance at exact head `f3fef856`, including `rtl-fast`, `verilator-suites` (whose sweep runs `obj_dynmap`) and `yosys-portability`.
- The current-dev merge-candidate validation, builder and native banks, against live dev `e26f1816e456dc8027924bc2e5d327a8aa6e46db`.
- The second independent positive review.
- Carry R663-4-R1 and R663-4-R2 to the residue checklist.
- Consider new Issues for the author's three disclosed pre-existing items, which this delta leaves unchanged:
  - the "shipping Arty" text for `obj_nxn4c` (README row, `build-nxn4c` comment, `CASE_OPTIONS_nxn4c` banner);
  - the `AX1X1_BUILD` "byte for byte" comment;
  - `dynmap-mutants` not making its listener leg's inputs.

R663-4 FINISHED
