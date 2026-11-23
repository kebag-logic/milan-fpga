[R909] NEGATIVE - exact head 2e278379c1ae9ea09063b3e3cb183d0e8a3f0929

# R909-1: internal independent review of PR #987 (issue #979)

- Head `2e278379c1ae9ea09063b3e3cb183d0e8a3f0929`, tree `3ae715044d525c20cffba94f4cabb2c3370803b2`.
- Reviewed range `3cda030c17..2e278379` (six commits on #975's reviewed head; #975 itself not re-reviewed).
- Cleared-context session. Inputs: AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #979 body and its four comments (including the option-B ruling, issuecomment-7096503041), the PR body, the diff and history, the cited RTL and builder sources, and the public author packet `review-evidence/loopbram-r1` at `6500a01b`.
- Every lens below was applied at this exact head. The verdict is NEGATIVE: one BLOCKER, two MAJOR and four MINOR findings are open.

## Verdict summary

At the two tracked shapes the mapped-copy design works as specified, and the sample-exact wire harness is real evidence. I reproduced it at both shapes: 79,587 checks / 468 packets at 8x8 and 76,017 / 447 at 1x1. The control and all seven planted defects reproduce their verdicts. Disabled builder artifacts and descriptor images are byte-identical to the base. The enabled descriptors are mono with port widths `[9,8,8,8,8,8,8,7]`. The routes and the S14 debt record match the claims.

Four things block approval:

1. The PR breaks two existing regression campaigns. The author's render-queue receipt cannot have come from this source.
2. The disabled image is not shown not to grow. The repository's own synthesiser keeps 57 loopback-only flops in the disabled capture crossbar.
3. No executed test covers the option inside `milan_datapath`. That leaves the map-writer invalidations, multi-page GET_AUDIO_MAP and the full-width walk untested.
4. Four smaller robustness and test gaps remain open.

## Findings

### F1 - BLOCKER - Tests, Docs - two existing mutation campaigns disarmed at this head; author queue receipt not from this source

- **Where:**
  - `tb/verilator/render_queue/mutants.py:103-105` is anchored on `if (flush_i[s]) begin`. The head changed that line to `if (flush_w[s]) begin` at `hdl/ieee1722/aaf/KL_render_queue.sv:1024`.
  - `tb/verilator/milan_dp/render_mutants.py:102-106` ("a PHC step resets the stage") is anchored on `) render_queue (\n    .clk_i (axis_clk), .rst_n (axis_resetn),`. The head inserted the `input_*` connections ahead of `.clk_i` at `hdl/milan/milan_datapath.sv:8479-8486`.
- **Evidence:**
  - `receipts/run-render_queue-all.txt`: `make -C tb/verilator/render_queue all` at this head exits 2. The output is `[FAIL] mutation 'a bind wipe ignored': its pattern(s) appear [0] time(s) ... fix the pattern, do not delete the arm` and `28 checks: 27 PASS, 1 FAIL`.
  - `receipts/anchor-counts.txt` uses each campaign's own `count(pattern) != 1` refusal. Both arms count 1 at base `3cda030c` and 0 at head.
  - `make -C tb/verilator/milan_dp run` ends with `python3 render_mutants.py` (`tb/verilator/milan_dp/Makefile:795`). That script prints `[FAIL]` for a zero-count anchor and returns 1 (`render_mutants.py:365-372`), so the main datapath suite cannot pass at this head. I did not run that suite in full; the refusal predicate is shown directly.
  - The author receipt `regressions--queue.log:106,123` shows that arm caught and 28/28. But the author's own `source_identity.json` hash for `KL_render_queue.sv` (`361493...bfd`) is this head's file, which does not contain the anchor. That receipt was produced from an earlier source.
  - REVIEW-READY's "render queue including 28 mutants" PASS claim is therefore false at this head.
- **Impact:**
  - Two planted controls of the shipping presentation stage stop mutating anything: the bind wipe, and the stage reset on a PHC step.
  - Two existing gates go red.
  - The published evidence over-states what was run.
- **Required outcome:**
  - Re-anchor both arms to the head's RTL, keeping the behaviour each arm plants. Do not delete either arm.
  - Re-run `make -C tb/verilator/render_queue all` and the `milan_dp` render-mutants arm at the new head.
  - Publish receipts produced from the exact head, and correct the REVIEW-READY claim.
- **Verification:** `scripts/anchor_counts.py` reports `ANCHORS INTACT 0`. Both campaigns exit 0 with every arm caught.

### F2 - MAJOR - Conformance, RTL, Tests - disabled image growth not excluded; disabled capture leaf grows under the repository synthesiser

- **Where:**
  - `hdl/ieee1722/aaf/KL_chan_map_capture.sv:931`: the state enum is widened to 3 bits whatever `INPUT_LOOPBACK_P` is.
  - `:1374-1387, 1453-1457`: `input_left_r`, `input_right_r`, `input_right_addr_r` and both selects are written in `CM_STEP_S` whatever `INPUT_LOOPBACK_P` is. They are read only in `CM_INPUT_L_S` and `CM_INPUT_R_S`, which the disabled build never enters.
- **Authority:**
  - Issue #979 acceptance: "with it off, the 1x1/1if and 8x8/1if images do not change".
  - Owner rule: the images at 1x1 and 8x8 must not grow.
- **Evidence:**
  - `receipts/leaf-off-incontext.txt` (`scripts/leaf_off_incontext.sh`): a flattened xc7 synthesis with all parameters at default and the head's new ports stripped as the disabled datapath leaves them. In `KL_chan_map_capture`:
    - FF goes from 3961 to 4018, +57. The extra flops are `input_left_r` x24, `input_right_r` x24, `input_right_addr_r` x6, two selects and `st_r[2]`.
    - LUT goes from 4339 to 4702, +363, while MUXF7/8 falls from 1103 to 763.
  - In `KL_render_queue` the disabled result is unchanged: FF equal, LUT -5.
  - The author identity scope explicitly excludes gateware ("FPGA configuration bitstreams ... are outside this identity claim"). Every routed measurement is of the enabled image. No disabled-image utilisation against the base exists.
  - Whether the vendor flow prunes the unreachable states is unmeasured.
- **Impact:** both shipping default images may carry dead loopback logic, in breach of the frozen acceptance criterion and the no-growth rule. Today's evidence cannot rule this out.
- **Required outcome:** either one of these:
  - make the disabled RTL structurally free of the option: generate-gate the extra states, the holding registers and their writes on `INPUT_LOOPBACK_P`; or
  - publish disabled 1x1/1if and 8x8/1if synthesised or routed utilisation equal to the base.
- **Verification:**
  - `scripts/leaf_off_incontext.sh` shows zero FF and LUT delta for both leaves.
  - Disabled-image utilisation equals the base at both shapes.

### F3 - MAJOR - Tests, Conformance - the enabled option is never executed inside `milan_datapath`

- **Evidence:**
  - `tb/verilator/input_loopback` is the only harness that sets `INPUT_LOOPBACK_P` (search of `tb/`). Its wrapper `loopback_wrap.sv`:
    - drives `invalidate_i` and `map_i` directly;
    - feeds the render event instant and the capture close instant from one stamp;
    - instantiates the capture crossbar with `N_SLOTS_P(4)` and one talker. So 8 destinations are transmitted per window, and no walk ever reads all 63 bucket-6 destinations at once.
  - These enabled-only datapath paths have no executed check:
    - the four `input_loop_invalidate_r` writers and the `!dom_live_w` term: `milan_datapath.sv:5201, 5285, 5334, 5344, 8481`;
    - the factory loopback image, `:5016-5021`;
    - the `cmap_walk_ns_w` / `dom_ns_w` pairing, `:1552, 8485, 8500`;
    - the bucket-6 output templates, `avdecc/aem_specs.py:183-187`, through the real capture map;
    - AECP ADD/REMOVE/GET_AUDIO_MAP on the new keys, including `map_index` 1. No shipping configuration has `ADP_DMAP_IN_PNMAPS_C` above 1 (`configs/generated/*/gen/adp_shape_defaults.svh:85`), so multi-page input maps have never been simulated. This is Milan v1.2 5.4.2.26-28 and IEEE 1722.1-2021 7.4.44-46 at the enabled configurations.
    - the 32-slot walk with two extra cycles per slot, and its `TLK_WALK_CYC_C` term (`:1700-1702`).
  - The design document this PR adds requires this coverage. It says "Every mapping writer must feed that logical view. Include accepted edits, boot defaults, restore, rollback, and format clipping", "Cover reset, bind loss, format clipping, and buffer-fill edits", "Run ... the relevant mapping/restore regressions", and "Implementation must meet every validation and measurement obligation above".
  - The harness README defers command acceptance to "the existing datapath render suites", but those run with the option off.
- **Impact:**
  - A defect in any of these paths ships undetected in the enabled image. Examples: a dropped invalidation pulse, or a page-2 GET_AUDIO_MAP indexing error.
  - The issue's end-to-end criterion ("received audio re-transmitted by a talker through the input mapping; mapping changes ... covered") is met only at module level.
- **Required outcome:**
  - Add an enabled-image datapath test, using a generated enabled shape at both sizes. It drives received AAF through AECP ADD, REMOVE and GET_AUDIO_MAP, with `map_index` 0 and 1 on 8x8 port 0 and 1x1 port 0. It transmits through the real capture map at full slot count, with all destinations at once.
  - Add at least one planted removal of a datapath invalidation pulse that must fail.
- **Verification:** the new test passes clean and fails its named check under the plant.

### F4 - MINOR - Tests, Robustness, Docs - five guard plants survive the scoreboard (four documented guards plus the current-frame age check)

- **Evidence:** `receipts/probes-summary.txt`. Each plant below passes the unchanged scoreboard (79,587 checks, 0 failures) at 8x8:
  - `no_flush_term8`: `invalidate_w` without `|flush_i`;
  - `no_claim8`: the one-shot claim removed;
  - `no_expiry8`: period expiry removed;
  - `no_backlog8`: the `sn_r != n_r` gate removed;
  - `no_age8`: the age gate removed.
- **Why the bind-flush step does not test bind loss:** the harness pulses `invalidate_i` together with `flush_i` (`sim_main.cpp:196-198`), which masks the bind-loss term. In the datapath, bind loss reaches the queue only through `flush_i` (`strtbl_bind_fall_w`), and `input_invalidate_i` does not carry it.
- **Claims these plants contradict:**
  - The harness README claims coverage of "bind flush" and "prolonged absence across tag wraps".
  - `hdl/ieee1722/aaf/README-parameters.md` claims "A second walk cannot replay that page".
- **Impact:** these never-stale guarantees are asserted but not load-bearing in any test.
- **Required outcome:** either one of these:
  - add scenarios that fail when each guard is removed: bind loss without map invalidation, a repeated capture instant or duplicate walk, and a stalled or backlogged schedule; or
  - record these guards as untested defence in depth in the README and the design document.
- **Verification:** re-run `scripts/probes.py`. Each guard plant either fails, or is listed as untested.

### F5 - MINOR - RTL, Robustness - the four-page window silently requires an out-lead of at most two frames

- **Where:** `hdl/ieee1722/aaf/KL_render_queue.sv:783-905`. Pages are indexed by `cons_w[1:0]`, expire two frames after their frame, and are reused at event n+4.
- **Evidence:**
  - Probes `lead3_8` and `lead3_1` fail with permanent silence (`got=000000`) from the first audio frame. `lead2_8` passes.
  - `RENDER_LEAD_C` is derived from interface timing (`milan_datapath.sv:8420`): 2 at 1x1 TDM8, 1 at 8x8 TDM32.
  - `g_input_loop_shape` (`:8461`) checks only the key count.
  - The builder's `_validate_input_loopback` checks only stream counts, physical counts and map mode.
- **Impact:** an enabled shape whose out-lead derives to 3 or more elaborates and routes, but loops back silence.
- **Required outcome:** an elaboration guard relating page count and expiry to `KMIN_C`, or a page count derived from it, plus a negative elaboration check.
- **Verification:** lead 3 refuses at elaboration, or passes the wire scoreboard.

### F6 - MINOR - RTL, Robustness, Tests - the ±3-cycle capture-instant window is underived and its margin untested

- **Where:** `hdl/ieee1722/aaf/KL_render_queue.sv:799`. The justification at `:818` is one sentence: "Clock-domain synchronizers and PHC sampling bound the stamp tolerance."
- **Evidence:**
  - Probes `drift_p60_8` and `drift_m60_8` pass, and `drift_p70_8` fails (5,588 failures), at the wrapper's 63 ns window. The datapath's 100 MHz clock gives ±30 ns.
  - `tol_zero8` fails, so ns rounding is exercised. Nothing exercises a realistic offset.
- **Error terms the window must absorb:**
  - The page tag is `ev_ns + (K+1) x Ps` at the nominal rate, while the walk instant is a PHC sample at the frame-close marker.
  - Each stamp carries up to one datapath cycle of quantisation, and the marker crosses a clock domain.
  - A media clock not syntonised to the PHC (INTERNAL) adds `(K+1) x Ps x e`: 6.25 ns per 100 ppm at K = 2.
  - Pages are 20.8 µs apart, so a window far wider than 30 ns would still be unambiguous.
- **Impact:** intermittent loopback silence under rate offset or marker jitter, with an unknown margin.
- **Required outcome:** derive the window from those terms (or widen it), document the derivation, and test with a rate offset and jitter near the bound.
- **Verification:** a scoreboard run with a ppm ramp passes inside the documented bound and fails outside it.

### F7 - MINOR - Docs, RTL - module contract banners are stale for the enabled option

- **`KL_chan_map_capture.sv:334-348` (WALK BUDGET):** the formula and figures omit the two extra cycles per slot when the option is on. The enabled 8x8 walk is 1 + 33 + 32 x 28 = 930 cycles. No test measures the enabled walk.
- **`KL_render_queue.sv:53-73` (READ, CONSUMED ROWS):** these do not describe the copy interval between the reads and the scrub.
- **`:125-130` (HOLD):** this says "their rows keep their frame numbers". With the option on, two missing domain periods flush every stream instead.
- **`:132-135` (FLUSH):** this omits that flush.
- **Required outcome:** banners that state the enabled behaviour.
- **Verification:** documentation diff.

### R1 - RESIDUE - Docs - `docs/design/INPUT_MAPPED_LOOPBACK.md:7`

`Author: [A826]. Date: 2026-11-23.` puts a session label in an authoritative design document. Exact fix: replace the line with `Date: 2026-11-23.`

### R2 - RESIDUE - Docs - off-tree pointer

`docs/design/INPUT_MAPPED_LOOPBACK.md:3` and `tb/verilator/input_loopback/README.md:31` point to "the review packet", which is not in the tree. Exact fix: replace "the review packet" with a link to PR #987 (`https://github.com/kebag-logic/milan-fpga/pull/987`).

### R3 - RESIDUE - Docs - `docs/ENDSTATION_BUILDER.md:1115`

Row 16g is placed ahead of rows 16f and 16e. Exact fix: move the row after 16e.

### S1 - SUGGESTION - Docs - PR body and REVIEW-READY

The text says "no ... product guard changed". State explicitly that split-placement builds now apply only layout 3's NAME capacity, and no longer the all-fabric 128-record bound (`sw/builder/endstation_builder.py:2833-2835`). The fabric backend is absent from the split image, so the change is sound. It is a guard change all the same.

## Public review findings at this head

I read these only after writing the verdict and ledger above. At the start of this round no review findings were published. The concurrent external round R910-1 published a NEGATIVE verdict at this same head during this round. Its two items are reconciled here:

- **R910-1-F1 (MAJOR, Tests): enabled command-to-audio integration untested. RETAINED** at this head as my F3. I also attribute it to Conformance, because Milan 5.4.2.26-28 behaviour at the enabled configurations, including multi-page GET_AUDIO_MAP, has no executed evidence.
  - Its full-width leaf probe (607,488 checks / 3,551 packets) answers the leaf-level concurrency part of F3.
  - It does not answer the datapath part, which still requires all 63 destinations with all streams at once in the real datapath.
- **R910-1-R1 (RESIDUE, Docs): `docs/design/INPUT_MAPPED_LOOPBACK.md:107` "The current queued lane has not been remeasured." RETAINED.** It sits beside the fresh legacy-capture leaf comparison in REVIEW-READY.
  - Exact fix, adjusted for R2 above so that it does not point off-tree: replace the sentence with "Fresh leaf measurements are recorded on PR #987."

One statement in R910-1 differs from this round's executed evidence. It lists the render-queue regression as passing with 28 detected plants, citing the author log. At this head that campaign exits 2 with 27/28 (F1). R910-1 read the author receipt and did not re-run the campaign.

## Checks that held (artifact-specific)

| Check | Result | Artifact |
|---|---|---|
| Wire harness, both shapes, pinned simulator 5.050 | PASS: 79,587 / 468 (8x8), 76,017 / 447 (1x1) | `receipts/probes-summary.txt` (`clean8`, `clean1`) |
| Author's seven plants plus control, unchanged `mutants.py` | control PASS; all 7 fail `COPY_SAMPLE` | `receipts/author-mutants-rerun.{json,txt}` |
| Extra plants at 1x1 and capture-side plants | `wrong_bank1`, `wrong_latency1`, `cap_right_ignored8` and `cap_left_addr8` all fail | `receipts/probes-summary.txt` |
| Disabled builder identity, base vs head (12 artifacts incl. `aecp_aem_rom.svh`, `soc_params.json`, `nvm_split.json`; descriptor image) | IDENTICAL at both shapes; the enabled control differs in 11 artifacts | `receipts/identity-compare.txt`, `identity-{base,head}.json` |
| Disabled render queue leaf | FF equal; LUT -5 (mapping noise) | `receipts/leaf-off-incontext.txt` |
| Enabled descriptors: AUDIO_CLUSTER channel_count, port widths, number_of_maps | all 1; `[9,8,8,8,8,8,8,7]` + 1x1 `[16]`; 0 (dynamic) | `receipts/descriptors.txt` |
| Builder contract test | PASS | `receipts/run-builder-test_input_loopback.txt` |
| Capture lockstep regression `chmap_capture run` | exit 0 | `receipts/run-chmap_capture.txt` |
| Default-off datapath regressions `capture_coherence run dp`, `milan_dp_render run ship8` | both exit 0; ship8_render 130 checks and five leg defects caught | `receipts/run-capture_coherence-dp.txt`, `receipts/run-milan_dp_render-ship8.txt` |
| Lint ratchet, pinned simulator | 89 <= 89 PASS | `receipts/run-lint.txt` |
| Documentation and privacy gate | 0 findings | `receipts/run-docs_check.txt` |
| Routes (author receipts) | 1x1 AltSpreadLogic_high +0.290 / +0.036 and 8x8 ExtraPostPlacementOpt +0.233 / +0.025; 4 corners each; 0 failing endpoints; 0 routing errors | `review-evidence/loopbram-r1/author/receipts/route-summary.json` |
| S14 debt (author receipts) | enabled 8x8 70.5 tiles, product allocation REFUSED; enabled 1x1 46.5 within 56 | `.../firmware-memory.json` |
| Source comments in the delta | no lane labels, rounds, reviewer IDs or comment IDs | `git diff 3cda030c17..2e278379` added lines |

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2, F3) | issue #979 acceptance and the option-B ruling; `milan_datapath.sv` input image, map writers and GET_AUDIO_MAP page walk; enabled descriptor ROMs; builder identity | R909-1 | 2e278379c1ae9ea09063b3e3cb183d0e8a3f0929 |
| RTL | UNCLEAN (F2, F5, F6, F7) | `KL_render_queue.sv` 597-905, 1021-1042; `KL_chan_map_capture.sv` 928-1496; `milan_datapath.sv` 1480-1580, 1700-1702, 5003-5350, 8457-8490; `KL_media_domain_event.sv` | R909-1 | 2e278379c1ae9ea09063b3e3cb183d0e8a3f0929 |
| Robustness | UNCLEAN (F4, F5, F6) | 18 probes in `receipts/probes-summary.txt`; reset, clock-loss, bind-flush, lead and drift paths | R909-1 | 2e278379c1ae9ea09063b3e3cb183d0e8a3f0929 |
| Tests | UNCLEAN (F1, F2, F3, F4, F6) | `tb/verilator/input_loopback/*`, render_queue and milan_dp mutation tables, re-run of the author plants, probes | R909-1 | 2e278379c1ae9ea09063b3e3cb183d0e8a3f0929 |
| Docs | UNCLEAN (F1, F4, F7) + RESIDUE R1-R3 | `docs/design/INPUT_MAPPED_LOOPBACK.md`, both `README-parameters.md`, `docs/ENDSTATION_BUILDER.md` row 16g, `docs/testing/TESTING.md`, module banners, REVIEW-READY / PR body | R909-1 | 2e278379c1ae9ea09063b3e3cb183d0e8a3f0929 |

## Real limits

- **Not run in full:** the `milan_dp` suite. F1's datapath half rests on that campaign's refusal predicate applied to its own table.
- **Not run by me:**
  - any vendor synthesis or route, so F2's vendor-flow outcome is unmeasured;
  - the firmware link or ROM comparison. Firmware sources are untouched by the delta, and its builder inputs are byte-identical when the option is off.
  - the full builder union, portability synthesis bank (`syn/yosys/run.sh`), the front-end parse gate, or hosted or act jobs.
- **Leaf comparison scope:** the in-context comparison is an approximation that strips port status from the flattened leaf. It is not a datapath synthesis.
- **Owner bounds (loads 0.70/0.75, last notice 140 ms, ACMP 30 ms, txL 49 ms, THE SHARE 2 ms):** the default image is untouched, because no firmware source changed and the default builder inputs are identical. No firmware path changed for the enabled image. Its owner bounds are not stated, and the enabled 8x8 image is refused by the allocator anyway.
- **Hardware:** physical calibration was not run. Field skips are not hardware proof.

## Pending manager duties

- Current-dev merge-candidate validation (live dev `e275d795`) and hosted/act acceptance.
- **Evidence-packet hygiene, outside this head:** one published file name in `review-evidence/loopbram-r1/author/receipts/` embeds a vendor-tool temporary directory containing a host name (`route--endstation_ax7101_8x8--gateware--.Xil--<vendor-tool>-<pid>-<host>--realtime--alinx_ax7101.tcl`). Some receipts carry a `$MANAGEMENT/...` path. Review against the privacy rule.
- Carry R1-R3 to the residue checklist.

R909-1 FINISHED
