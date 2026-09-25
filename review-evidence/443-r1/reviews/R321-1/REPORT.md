[R321] NEGATIVE - exact head c9bbb03cc3d4da9c6ee28996b91addbb081efa7e

# R321-1: external review of PR #561 (issue #443)

- Head `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e`, tree `0aea0092d7ff41f528d9296c92b401efb2427a38`.
- Source base `0755923d983218ca6ca9db6891a558cbe6425b8d`, the single commit `c9bbb03cc`, executor [A298].
- Scope reconstructed from the issue body, the item-4 decision (comment 5789749713) and the assignment (comment 5826079535). The assignment covers items 1, 2, 3 and 5. Item 4 is decided: counters and CSR state only, no STREAM_INTERRUPTED.
- There were no prior review findings on the PR at this head: 0 reviews, 0 inline comments, and only the two review-start comments.

## Verdict summary

The frozen acceptance items are met, and the new word and its tests are good.

- `RENDER_STAT` at `0x8DC` mirrors the stage's taps exactly and preserves their widths.
- The integration proof catches six of the seven reviewer mutants I planted, and it catches each one by name.
- I reproduced both Yosys counts exactly at base and at head.

I found five MINOR findings, and they leave Conformance, Tests and Docs unclean:

- A standalone bench still asserts that `0x8DC` is unmapped.
- A documented selector rule is not graded.
- The new explicit campaign is missing from the testing page's list.
- The additive ABI change carries neither a `VERSION` bump nor a recorded deferral.
- The register-group index has no row for the word.

Under this round's rule any open MINOR makes the verdict NEGATIVE. RTL and Robustness are CLEAN.

## Findings

### F1 MINOR (Tests, Docs): the standalone CSR bench still asserts that 0x8DC is unmapped

- **Where:** `tb/verilator/csr/sim_main.cpp:1221-1223`. It reads `ck("0x8DC above the slip pair is unmapped, reads 0", axi_read(0x8DC), 0)`.
- **Evidence:** At head, `milan_csr.sv:2389-2395` and `:2561` decode `0x8DC` as `RENDER_STAT`. The bench never drives the new `i_render_status` port. At head it still prints `[ok] 0x8DC above the slip pair is unmapped, reads 0 = 0x0` and ends 371/371 PASS (`receipts/csr-bench-run.log:335`).
- **Impact:** A gating suite now publishes a false contract statement. The check passes only because the input floats at zero, so it cannot detect a broken `RENDER_STAT` decode. For comparison, #390 drove the slip inputs in this same bench (`:1236-1258`).
- **Required outcome:** No check in the tree claims that `0x8DC` is unmapped. The bench either grades the word with a driven `i_render_status`, or states honestly what a tied-zero input proves.
- **Verification:** Rebuild and run `tb/verilator/csr`. The label is gone or corrected. If the input is driven, dropping the `(rd_addr_q == A_RENDER_STAT)` term fails the check.

### F2 MINOR (Tests): the documented STRM_SEL[9] semantic is not graded

- **Where:** The claim is at `docs/reference/REGISTER_MAP.md:1950`: "`STRM_SEL[9]` does not change this word's selection". The only check is `tb/verilator/milan_dp/sim_aclk.cpp:406-407`, the `0x200` "listener-0 row override" read at index 0.
- **Evidence:** For the `0x800` window, bit 9 forces sink 0 and ignores `[8]`/`[3:0]` (`REGISTER_MAP.md:1521`). A mutant that gives `RENDER_STAT` that window meaning is `if (strm_lsn0_r ? (s == 0) : (...))` at `milan_csr.sv:2392`. It **survives** both the aclk leg (62/62) and the two-listener leg (64/64). See `receipts/probe-row-select.jsonl` and `receipts/probes/probe-csr_row_select_as_window_*.log`. The assignment asks that selector semantics be stated and graded.
- **Impact:** The one place where this word deliberately departs from the window's rule is unprotected. A later change that aligns the two would go unnoticed.
- **Required outcome:** Some leg grades bit 9 with a non-zero listener index, or with the talker direction, such that the window-semantics mutant fails a named check.
- **Verification:** Plant the mutant above. It must fail by name.

### F3 MINOR (Tests, Docs): the new explicit control campaign is missing from the testing page's list

- **Where:** `docs/testing/TESTING.md:256-267`. Line 258 reads "this page keeps the list of such targets". The new target is at `tb/verilator/milan_dp/Makefile:407-409`, and `tb/verilator/milan_dp/README.md:812` says its two elaborations "stay outside the default sweep's deadline".
- **Evidence:** The table lists `tdm8render-mutants`, `crflic-mutants` and `gmstep-mutants`, each with who must run it. `render-csr-controls` is absent, and no gate runs the absent-stage control or the wrong-fill mutant.
- **Impact:** The absent-stage control and the mutant from acceptance item 2 have no owner after merge. A later change to `render_status_w`, the `A_RENDER_STAT` decode or the stage's taps is not required to re-run them.
- **Required outcome:** The list names the target and the changes whose authors and reviewers must run it.
- **Verification:** The row is present, and the docs gates pass.

### F4 MINOR (Conformance, Docs): an additive CSR change with no VERSION bump and no recorded deferral

- **Where:** The rule is `docs/reference/REGISTER_MAP.md:2260-2261`: "additive changes bump minor". See also `:264-266`, where a new CSR field "would be a CSR contract change owing a `VERSION` bump". At head `VERSION` is still `0x0002_0060` (`hdl/common/csr/milan_csr.sv:196`). `CHANGELOG.md` has no entry for the change.
- **Evidence:** The project's current practice is an `Unreleased` CHANGELOG entry saying "VERSION is unchanged; the release step owns the bump" (`CHANGELOG.md:86,104,124`, for example #360's `GPTP_DROPE[31:16]`). This PR records neither that entry nor a bump, and the issue and PR never mention VERSION.
- **Impact:** Gateware with and without `RENDER_STAT` would report the same VERSION. Feature gates key on the minor (`REGISTER_MAP.md:357`), so software cannot gate on the word, and nothing tells the release step that a minor is owed.
- **Required outcome:** Either bump the minor, or record the deferral publicly the way current practice does. That means an `Unreleased` CHANGELOG entry naming `RENDER_STAT`, or an equivalent recorded decision.
- **Verification:** The entry or the bump is present at the new head, and the docs gates pass.

### F5 MINOR (Docs): the register-group index has no 0x8DC row

- **Where:** `docs/reference/REGISTER_MAP.md:210-244`. The rows jump from `0x8D4` (`:241`) to `0x8F8` (`:242`).
- **Evidence:** The PR claims `0x8DC` as its own section (`:1940`) and adds a contents entry (`:203`). Every other claimed group has an index row, including the slip pair with its `minor >=` note.
- **Impact:** Read by base address, the index places `0x8DC` inside the slip-counter group.
- **Required outcome:** Add a `0x8DC` row that names `RENDER_STAT`. Include a minor note once F4 settles one.
- **Verification:** The row is present, and `gen_toc --check`/`--verify-anchors` pass.

### Suggestions (do not affect coverage)

- **S1 (Docs):** At `REGISTER_MAP.md:1946-1950`, say that the `0x00000100` reset assumes STRM_SEL at its reset (listener 0). Also say that selecting another listener moves the shared STRM_SEL, which invalidates the window's ACMP/SRP snapshots (`:1521`). A diagnostic reader should restore it.
- **S2 (Docs):** The PR records the `milan_datapath` change (-1,652 cells, reproduced exactly) without comment. One sentence would help: generic synthesis, no area claim, the decrease is not attributed. The author's Yosys receipts do not record which commit each run synthesized. My reproduction pins both.

## Independent evidence (reviewer-run, this head)

| Check | Result | Receipt |
|---|---|---|
| Yosys `milan_csr` base / head | 70,355 / 70,466 (+111), exact match to the PR | `receipts/yosys-csr-{base,head}.log` |
| Yosys `milan_datapath` base / head | 1,633,435 / 1,631,783 (-1,652), exact match to the PR | `receipts/yosys-dp-{base,head}.log`, `receipts/yosys/` |
| `make -C tb/verilator/milan_dp render-csr-controls` | rc 0. Clean 62/62. Wrong-fill caught at `RENDER-CSR: filling mirrors taps` (got 256, exp 262). Absent stage 31/31 | `receipts/render-csr-controls.log` |
| Reviewer mutants (aclk leg `--render-csr-only`) | rails sourced from underruns: CAUGHT. prefill/converged swapped: CAUGHT. direction ignored: CAUGHT. bit 9 zeroes: CAUGHT. read-window term dropped: CAUGHT. Clean: PASS | `receipts/probe-mutants.jsonl`, `receipts/probes/` |
| Reviewer mutants (two-listener leg) | Every index aliased to listener 0: CAUGHT (`RENDER-CSR-MULTI: flushed listener 1 has empty prefill`). Clean 64/64 | same |
| Bit-9 window-semantics mutant | SURVIVED both legs (F2) | `receipts/probe-row-select.jsonl` |
| Standalone CSR bench | 371/371, with the stale "unmapped" check at line 335 (F1) | `receipts/csr-bench-run.log` |
| Author default-sweep aclk chunk (public) | 188/188, RENDER-CSR checks present (reset, filling, converged, rail) | public evidence `sweep-chunk-1790307224815958860.log` |
| `gen_toc --check`, `--verify-anchors`, `--selftest`, `docs_check`, doc style, doc paths, em-dash vs base | all rc 0. 170 cross-page anchors reproduced, including the new `#0x8dc-----render-setpoint-state` links | `receipts/docs-*.log` |
| lint_rtl `--check`, SV/C++/Python idiom, port contracts, RTL source lists, test evidence, `git diff --check` | all rc 0. Lint 90 <= ratchet 90 | `receipts/static-*.log` |
| Four pointers / STREAM_INTERRUPTED | No pointer names #390. The two remaining `#390` mentions in `milan_datapath.sv` (`:1192`, `:2585`) are the SLIP pair's own. No hdl hunk touches an interrupt | `receipts/pointers-and-interrupt.txt` |

Tools: Verilator 5.050, run through the pinned wrapper, whose identity I checked. Yosys 0.66 and sv2v v0.0.13. `reproduce.sh` and `probe_mutants.py` re-run all of the above from a clean exact-head clone.

## Lens results

These lines cover what was examined at the exact head, including the lenses left unclean by the findings above.

- [R321] UNCLEAN Conformance: F4. **Examined and met:**
  - Item 1: `0x8DC` sits in the formerly unmapped `0x8DC-0x8F4` span, and the page's own sentence is updated (`REGISTER_MAP.md:1819-1820`). The layout follows the real tap widths:
    - `fill_o` is 8 bits (`KL_render_setpoint.sv:199,682`), and `DEPTH_LOG2_P<=7` bounds it at 128.
    - `prefill_o` and `converged_o` are levels.
    - `rails_o` is 16 bits and saturates (`:664`).
    - The resets are prefill=1 and the rest 0 (`:553-559,653`).
    - Legend-consistent STRUCTURAL ZERO wording is at `:1968-1973`, and the class row is at `REGISTER_MAP_CLASSES.md:107`.
  - Item 2: see Tests.
  - Item 3: all four pointers now name #443, and both pages say what the word carries (`TIME_SYNC.md:273-281`, `AAF_LATENCY_TAPS.md:96-100`).
  - Item 5: the counts are reproduced.
  - Item 4 decision: no STREAM_INTERRUPTED wiring, and both pages say so.
  - No single-port assumption: the word is per listener index, and the rails are global.
- [R321] PASS RTL. **Examined:**
  - `milan_csr.sv:434-437` (port), `:922` (address), `:2389-2395` (the selected-listener mux, zero for talker or out of range), `:2561` (read-window carve-out), `:1761-1763` (STRM_SEL storage), and `:2567-2590` (two-stage read registers with RDATA held).
  - `milan_datapath.sv:1202` (declared before use), `:2352` (`N_LISTENERS_P = N_STREAMS`), `:2375-2376` (CSR on `axis_clk`/`axis_resetn`, the same domain as the stage), `:2588`, and `:6162-6166` (packing in the documented order).
  - No CDC: one clock and one reset. No truncation. Not in `is_plain_rw`, so writes are inert.
  - Cell deltas reproduced. The lint ratchet is unchanged.
- [R321] PASS Robustness. **Examined** through the aclk and multi legs, plus mutants, against the RTL above:
  - Talker, out-of-range and index-2 selections read 0.
  - Reset during activity returns `0x100`.
  - R-channel backpressure holds RVALID and the sampled word for 32 cycles.
  - Writes are ignored.
  - With the stage absent, active ingress still reads 0.
  - A bind flush empties listener 1 while the global rails stay.
  - A rail clears convergence.
  - The bit-9 behaviour is correct in the RTL; only its grading is missing (F2).
  - F1's floating input is a test defect, not an RTL one.
- [R321] UNCLEAN Tests: F1, F2, F3. **Examined and sound:**
  - `sim_aclk.cpp:359-443`: the expected word is built independently on the capture edge, with exact equality.
  - `:1353-1367` covers the prefill, filling and converged phases, and `:1639-1651` and `:1694` place the checks in both the short and the default runs.
  - `render_csr_controls.py`, the named wrong-fill mutant and the absent-stage control.
  - `sim_tdm8_render.cpp:3274-3294`, the unequal two-listener states.
  - Six of seven reviewer mutants caught. The seventh, the bit-9 mutant, survived both legs.
- [R321] UNCLEAN Docs: F1, F3, F4, F5. **Examined and accurate:**
  - `REGISTER_MAP.md:203,1819-1820,1940-1980`, `REGISTER_MAP_CLASSES.md:107`, `TIME_SYNC.md:272-281`, `AAF_LATENCY_TAPS.md:95-100` and `milan_dp/README.md:793-814`.
  - All docs gates pass.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F4) | issue #443 items 1-5 and decision 5789749713; `REGISTER_MAP.md` legend, Notes, `0x8C8`/`0x8DC`/`0x800` sections; `REGISTER_MAP_CLASSES.md:107`; the four pointers; `CHANGELOG.md`; the Yosys reproduction | R321-1 | `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e` |
| RTL | CLEAN | `milan_csr.sv:196,434-437,922,1761-1763,2389-2395,2561,2567-2590`; `milan_datapath.sv:1202,2352,2375-2376,2588,6162-6166`; `KL_render_setpoint.sv:199-214,540-690`; the Yosys base and head pair; lint | R321-1 | `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e` |
| Robustness | CLEAN | aclk leg (`--render-csr-only`, `--render-csr-absent`), the two-listener leg, ten probe runs across the selection, reset, backpressure, write, flush and absent-stage paths | R321-1 | `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e` |
| Tests | UNCLEAN (F1, F2, F3) | `sim_aclk.cpp`, `render_csr_controls.py`, `sim_tdm8_render.cpp:3274-3294`, `tb/verilator/csr/sim_main.cpp:1215-1258`, `TESTING.md:256-267`, the reviewer mutation receipts | R321-1 | `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e` |
| Docs | UNCLEAN (F1, F3, F4, F5) | `REGISTER_MAP.md`, `REGISTER_MAP_CLASSES.md`, `TIME_SYNC.md`, `AAF_LATENCY_TAPS.md`, `milan_dp/README.md`, `TESTING.md`, `CHANGELOG.md`, the docs gate receipts | R321-1 | `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e` |

## Real limits

- I did not run the full parent, PP, gPTP, Yosys, builder or `milan_dp` default banks. For the default sweep I rely on the author's public chunk receipts and the manager's statement. The runs I did are the focused ones listed above.
- The `milan_dp` probes cover the 1x1 aclk shape and the two-listener TDM8 shape only. No 8x8 elaboration was exercised through `RENDER_STAT`.
- Physical calibration was NOT RUN. No hardware was touched, and no field or skip result is hardware proof. Builder gate 11 is NOT RUN, per the author.
- Hosted checks at this head: 17 success, 1 skipped (`Physical gPTP (nightly and manual)`), and 2 still in progress (`Verilator shard 1/5`, `4/5`) when I read them (`receipts/hosted-check-runs.tsv`). They are not accepted here.
- This clone was never edited. Every probe ran in disposable copies. After the probes, 885 tracked blobs hash equal to the index, and the index, the modes and the four gitlinks are unchanged (`receipts/integrity-{before,after}.txt`). The pinned-tool path is redacted in two logs (`receipts/REDACTIONS.txt`).

## Pending manager duties

- Hosted and act acceptance at the exact head, including the two in-progress Verilator shards.
- The candidate-merge build on current dev `c533b4818df8b3f581df76aa0d1c6d5f55d20449`, then post-merge containment.
- After fixes, re-review at the new head. F1-F5 must be resolved in the tree. Moving them to new Issues does not resolve them.

R321-1 FINISHED
