[R320] NEGATIVE - exact head c9bbb03cc3d4da9c6ee28996b91addbb081efa7e

# R320-1: issue #443 / PR #561, internal independent review

- Role: internal cleared-context reviewer; executor [A298].
- Exact head `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e`, tree `0aea0092d7ff41f528d9296c92b401efb2427a38`.
- Source base `0755923d983218ca6ca9db6891a558cbe6425b8d`; diff: 12 files, +323/-9, one commit.
- Scope reconstructed from:
  - the issue #443 body;
  - manager decision 5789749713 (item 4: rail and underrun events are counters/CSR state only, no
    `STREAM_INTERRUPTED`);
  - assignment 5826079535 (items 1, 2, 3, 5), takeover 5826110194 and review-ready 5826384396;
  - REQ-CSR-01/02/05;
  - `REGISTER_MAP.md` verdict legend, STRM_SEL row, debug group and Notes;
  - `REGISTER_MAP_CLASSES.md`;
  - the `KL_render_setpoint.sv` tap contract;
  - the published evidence tree `07043a66.../review-evidence/443-r1`.
- All five lenses applied. Verdict NEGATIVE: three MINOR findings remain open (F1-F3).
  - What reproduces: the functional RTL, the milan_dp and milan_dp_render proof, the controls, and the
    cell counts.
  - What stays open: a stale executable CSR-bench contract, the ABI version ordinal, and the group index.

## What was verified (independent reproduction at exact head)

| Claim | Evidence (this packet or tree) | Result |
|---|---|---|
| `0x8DC` was free in the right group | base 0x8C8 section ("`0x8DC` to `0x8F4` remain unmapped"); head `REGISTER_MAP.md:1819-1820`; `milan_csr.sv:922,2389-2395,2561`; not in `is_plain_rw` (`milan_csr.sv:2005-2038`) | Claimed from the debug group's own stated free span. Decode, live read and RO write-ignore are consistent. |
| Field layout comes from the real tap widths | `KL_render_setpoint.sv:199-213` (`fill_o` 8 per stream, `prefill_o`/`converged_o` 1 per stream, `rails_o` 16); saturation at `:664`; depth 2..7 check at `:236-237`; `milan_datapath.sv:6141` (depth 5, 32 rows); packing at `:6162-6166` | Widths are equal, with no truncation. Fill is bounded, rails saturate, and both flags are levels. Resets match `REGISTER_MAP.md:1952-1958` (`prefill_r` resets to 1, `:555`). |
| One clock, no CDC | stage at `milan_datapath.sv:6178` on `axis_clk`/`axis_resetn`; `milan_csr` instance `aclk(axis_clk)`/`aresetn(axis_resetn)` | Single domain. REQ-CSR-02 holds: the fields are one word sampled in one cycle. |
| Selector semantics and reset | STRM_SEL row `REGISTER_MAP.md:1521` (reset `0`); 0x8DC text `:1948-1950`; `milan_csr.sv:1583` | Stated. Graded by the first reset read: probe `csr_selector_reset_idx1` is caught. |
| Structural zero with the stage absent | absent-stage control in `receipts/render-csr-controls.log` | 31/31 while ingress is accepted; zero at reset and while fed. |
| AXI-Lite reads equal the taps across fill, prefill, convergence and a rail, with a negative control and a failing mutant | `receipts/render-csr-controls.log`; `receipts/aclk-default-head.log` | Clean run 62/0. The wrong-fill mutant exits 1 at `RENDER-CSR: filling mirrors taps` (got 0x100, expected 0x106); the campaign exits 0. The default leg passes 188/0, with 45 RENDER-CSR lines. |
| Two-listener selection | `receipts/milan-dp-render-multi-clean.log` | 64/0 |
| Reviewer mutants | `scripts/render_csr_probes.py`; `receipts/render-csr-probes.log` | Caught at named checks: direction ignored; index aliased to 0 (both legs); window term dropped; selector reset moved; prefill/converged swapped; rails fed from underruns. Survived, as expected: rails upper byte zeroed (see S2). |
| Yosys cell counts vs base | `receipts/yosys-{base,head}-top-{milan_csr,milan_datapath}.result` and logs | Both equal the published numbers exactly: `milan_csr` 70,355 -> 70,466 and `milan_datapath` 1,633,435 -> 1,631,783. Generic `synth`; no physical claim. |
| The four pointers and the two pages | `git grep '#390'` on the four files leaves only `milan_datapath.sv:1192,2585` (the SLIP pair, correct); `TIME_SYNC.md:273-281`; `AAF_LATENCY_TAPS.md:95-100` | Met |
| No `STREAM_INTERRUPTED` wiring | the only consumers of `rsp_rails_w` and `rsp_underruns_w` are the packing and the taps (`milan_datapath.sv:6157-6204`); the diff names the event in docs only | Met |
| No single-port assumption | the word is keyed by listener index through the existing selector; rails are stage-global, not tied to a port | Met |
| Docs gates | `receipts/doc-gates.rc`: `gen_toc --verify-anchors` (170 cross-page fragment links reproduced, including both new `#0x8dc-----render-setpoint-state` links), `--check`, `--selftest`, `docs_check`, doc style, doc paths, em dash vs base, module matrix | All rc 0 |

## Findings

### F1 MINOR - Tests, Docs, Conformance - `tb/verilator/csr/sim_main.cpp:1221-1223` - the CSR bench still asserts that 0x8DC is unmapped

- Authority/evidence: REQ-CSR-01 acceptance ("`REGISTER_MAP.md` matches RTL decode and the CSR bench
  exercises every implemented group").
  - At this head the bench prints `[ok] 0x8DC above the slip pair is unmapped, reads 0`
    (`receipts/csr-bench-head.log:335`, 371/0).
  - It passes only because the bench leaves the new `i_render_status` input undriven.
  - A copy of `milan_csr.sv` with the whole `A_RENDER_STAT` decode removed also passes 371/0, printing
    the same line (`receipts/csr-bench-nodecode-probe.log`).
  - The SLIP pair beside it is graded with driven inputs (`sim_main.cpp:1238-1260`).
- Impact: an executed regression publishes a contract that the register map now contradicts.
  - The CSR plane's unit bench cannot see this word. These defects would all stay green there: a lost
    decode or window term, a wrong index or direction gate at `N_LISTENERS_P > 2`, or writes that are
    no longer ignored.
  - Only the heavier integration legs cover the word.
  - The next reader of the bench is told that 0x8DC is free.
- Required outcome: the bench stops calling 0x8DC unmapped and grades `RENDER_STAT` through a driven
  `i_render_status`, as it does the SLIP pair. Grade:
  - a selected listener word read back;
  - talker and out-of-range selections reading zero;
  - writes ignored;
  - at least one nonzero index on a multi-listener elaboration (for example `obj_win`, `N_LISTENERS_P=4`).
- Verification: the bench passes at the new head. The no-decode copy of `milan_csr.sv` then fails a
  named RENDER_STAT check; `receipts/csr-bench-nodecode-probe.log` records the recipe.

### F2 MINOR - Conformance, RTL, Docs - `hdl/common/csr/milan_csr.sv:196`, `docs/reference/REGISTER_MAP.md:2260-2261` - an additive ABI word without a VERSION minor step or a recorded exemption

- Authority/evidence: `REGISTER_MAP.md:2260-2261` says: "The map is versioned by `VERSION`; additive
  changes bump minor".
  - The page calls itself the stable ABI, and every `VERSION minor >=` feature gate keys on the minor
    (`:381`).
  - The adjacent group row keys the SLIP pair on "minor >= `0x0058`" (`:241`).
  - `0x005E` stepped the minor for one added address (#358, `milan_csr.sv:152-157`).
  - This head decodes a new word and leaves `VERSION = 0x0002_0060`.
  - Precedent is not uniform: `f86e4ddff` added `0x7E8`/`0x7EC` without a step. That is why this is
    MINOR and not higher. The written rule still says what it says, and neither the PR nor the issue
    records an exemption.
- Impact: the base image is also `0x0002_0060`, contains the stage, and reads `0` at `0x8DC`.
  - The new text says a zero there means "no source, never a measured healthy stage"
    (`REGISTER_MAP.md:1968-1973`), and tells the reader to "check the elaborated build".
  - On an image built before this merge, no register tells a present stage from "no stage".
  - The firmware version that controllers receive is derived from `VERSION`, so it does not move either.
  - REQ-CSR-05 asks for unsupported function to be explicit rather than a plausible zero.
- Required outcome: one of two, recorded publicly:
  - (a) Step the VERSION minor. Add a changelog entry, use a coordinated number, and update the `0x004`
    row and the class row to match.
  - (b) Record a manager decision that exempts this addition. The 0x8DC section then states how software
    identifies a gateware that decodes the word.
- Verification:
  - Route (a): `milan_csr.sv` VERSION and the VERSION references in `REGISTER_MAP.md` and
    `REGISTER_MAP_CLASSES.md` agree at the new head. The entity-shape gate stays green
    (`scripts/check_entity_shape.py`, which already runs in the builder and static banks).
  - Route (b): the decision link is present in the 0x8DC section.

### F3 MINOR - Docs - `docs/reference/REGISTER_MAP.md:241-242` - the Register groups index omits 0x8DC

- Authority/evidence: the `## Register groups` table (`:210-244`) lists every decoded group, including
  the one-address groups `0x7F0` and `0x8F8`. `0x8DC` has a Contents entry (`:203`) and a section
  (`:1940-1980`), but no row between `0x8D4` and `0x8F8`.
- Impact: a reader who scans the group index, the page's top-level map, does not find the new word.
  REQ-CSR-01 asks the page to match the RTL decode.
- Required outcome: a `0x8DC` row that states the group: render setpoint state, RO live, the selected
  listener plus global rails, structural zero without the stage.
- Verification: the docs gates stay green (`gen_toc --check` and `--verify-anchors`, `docs_check`, doc
  style).

### Suggestions (optional; they do not affect coverage)

- S1 (Tests): `STRM_SEL[9]` "does not change this word's selection" (`REGISTER_MAP.md:1950`) is graded
  only with index 0 (`sim_aclk.cpp:406`, `0x200`), so "ignores [9]" and "[9] forces listener 0" read the
  same. Writing `0x201` in the two-listener leg would separate them.
- S2 (Tests): only width review proves the rail field's upper byte.
  - Probe `dp_rails_upper_byte_zero` survives because no leg reaches 256 rails.
  - A driven-input CSR bench check (F1) covers the CSR half.
  - The datapath packing remains a static review item.
- S3 (Docs): the 0x8DC text could repeat the STRM_SEL row's caveats about the shared selector.
  - Selecting a listener to read this word invalidates the window's ACMP/SRP snapshots
    (`REGISTER_MAP.md:1521`).
  - Another task that moves SEL changes what 0x8DC reports.
- S4 (Docs, disclosure): `AAF_LATENCY_TAPS.md:94-95` also changes "the TDM frame pin, which no build
  clocks" to "clocked on the shipping TDM8 shape".
  - The new statement is true: `TIME_SYNC.md:217` says "SHIPPED on the AX7101 1x1 TDM8 shape (#447)".
  - The change is outside the stated scope, and neither the PR body nor the handoff lists it. Name it in
    the PR.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | issue #443 body and decisions 5789749713/5826079535; REQ-CSR-01/02/05; `REGISTER_MAP.md:151-162,381,1521,1812-1820,1940-1980,2260`; `REGISTER_MAP_CLASSES.md:41-46,107`; the four pointer sites; `STREAM_INTERRUPTED` absent | R320-1 | `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e` |
| RTL | UNCLEAN (F2) | `milan_csr.sv:196,437,922,1064-1065,1583,2005-2038,2389-2395,2549-2590`; `milan_datapath.sv:1202,2347-2365,2588,6141-6205`; `KL_render_setpoint.sv:199-213,550-685`; generic synthesis of both tops at base and head | R320-1 | `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e` |
| Robustness | CLEAN | reset during activity (`reset again` after a rail); RVALID/RDATA held under 32-cycle backpressure; talker and out-of-range selection; RO write ignored; absent stage while ingress runs; selector reset (probe); saturation and bounded fill (static); bind flush does not clear rails (`KL_render_setpoint.sv:621-628,648-665`); `receipts/render-csr-controls.log`; `receipts/render-csr-probes.log` | R320-1 | `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e` |
| Tests | UNCLEAN (F1) | `sim_aclk.cpp:357-438,1353-1368,1639-1706`; `render_csr_controls.py`; `sim_tdm8_render.cpp:3277-3294`; `tb/verilator/csr/sim_main.cpp:1216-1260`; reproduced runs and 8 reviewer mutants (`receipts/`) | R320-1 | `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e` |
| Docs | UNCLEAN (F1, F2, F3) | `REGISTER_MAP.md` (Contents `:203`, groups `:210-244`, `:1812-1820`, `:1940-1980`, Notes `:2260`); `REGISTER_MAP_CLASSES.md:107`; `TIME_SYNC.md:269-281`; `AAF_LATENCY_TAPS.md:92-102`; `tb/verilator/milan_dp/README.md:793-814`; docs gates (`receipts/doc-gates.rc`) | R320-1 | `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e` |

## Limits

- Physical calibration NOT RUN. The field skips (builder gate 11, the physical gPTP context) are not
  hardware proof. This round makes no silicon claim for the word.
- Not run by this round:
  - the full `milan_dp` default sweep;
  - the full `milan_dp_render` suite;
  - the builder;
  - the static and RTL-lint banks.

  For those, this round relies on the manager's published source bank. The focused runs listed above
  were executed.
- The `milan_datapath` cell decrease (-1,652) is reproduced exactly, but nothing beyond generic mapping
  explains it. No physical area or timing claim is made or accepted.
- Simulator: the scoped 5.050 wrapper, identity recorded in `receipts/tool-identity.txt`. The author used
  5.052.
- Hosted contexts at the exact head, read-only, from `receipts/hosted-check-runs.tsv`:
  - at capture time, `Verilator shard 4/5` was still in progress;
  - `Physical gPTP` was skipped, not executed;
  - every other listed context had completed with success.

  The manager owns hosted and act acceptance.
- After the probes, the clone was restored and checked:
  - tracked blobs and modes of the touched files: `receipts/blob-verify.txt`;
  - index hash, submodule gitlinks and zero untracked/ignored entries: `receipts/post-probe-state.txt`,
    identical to `receipts/pre-probe-state.txt`.

## Pending manager duties

- Hosted acceptance at the exact head: `verilator-suites` completion and `yosys-portability`; act
  replication.
- The final candidate against live dev `c533b4818df8b3f581df76aa0d1c6d5f55d20449` (source base
  `0755923d`), with candidate-merge validation and post-merge containment.
- A decision on F2 if the executor takes the exemption route.
- Re-review of the fix head: Conformance, RTL, Tests and Docs again, plus Robustness if the fix touches
  its artifacts.

## Cross-reference to other public review findings

PENDING: this section is filled only after this verdict and ledger were written.

R320-1 FINISHED
