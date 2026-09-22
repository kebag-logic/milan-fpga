[R239] NEGATIVE - exact head 60c5225fe5f93209bf313c51b7a722f25f9aaa7d

Round R239-1, cleared-context internal review of kebag-logic/milan-fpga issue #372 / PR #518.
Head `60c5225fe5f93209bf313c51b7a722f25f9aaa7d`, tree `64182178131d03f157fe1a4ec767edee618bc6ff`
(merge of dev `52711029f374650dc93830d5ea28e81cb5c8f410` and author commit
`5bbf2953ea747403217aeeda020df6a6e5ff27f9`). Review start: PR #518 comment 5779353250.

Verdict basis: no BLOCKER and no MAJOR. The checker, bind, direct harness, campaign and
Makefile integration are correct at this head, and Conformance, RTL, Robustness and Tests are
covered clean. Docs is NOT clean: three MINOR findings (F1-F3) are open, so section 7's
all-lenses-clean bar is not met at this head. The required changes are text-only corrections.

## 1. What was read, in order

1. AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md (REQ-VER-01/02/04 and the
   `ptp_ts_top` scope note).
2. Issue #372 body and every comment. Settled contract: comment 5776353888 ([A10] READY
   SCOPE / IMPLEMENTATION DECISION). Later public comments: A170 TAKEN / REVIEW READY and the
   A10 validation comments.
3. PR #518 metadata, body, two commits, and the two A10 comments (5779340870, 5779353250).
4. The diff `52711029..60c5225f` (12 files, +2256/-7), and the product RTL it binds:
   `hdl/common/axis_mux_rr_2in_1out.sv`, `hdl/ieee8021as/ptp_timestamp/ptp_ts_top.sv:403-425`.
5. Harness plumbing: `tb/common/verilator_harness.hpp`, `scripts/suite_tally.py`,
   `scripts/run_all_suites.sh`, `scripts/suite_shards.py`.
6. The public manager packet at `eb069041/review-evidence/372-r1/candidate1`, at ledger level.

Not read: the author lane directory, any private author material, and the R240 report.

## 2. Identity checks

- `git rev-parse HEAD` = `60c5225f...`, tree `64182178...`; parents `52711029` and `5bbf2953`.
- The issue patch is byte-identical in both histories: `git diff 52711029 60c5225f` and
  `git diff 88e9276b 5bbf2953` both hash to sha256 `ef503064...1b186c`.
- The intervening dev merge touched 6 paths, disjoint from the PR's 12.
- No path under `hdl/`, `third_party/`, `syn/`, `sw/`, `protocol-processor`, `gptp-processor`
  changes. All four gitlinks are identical at base and head.
- `git diff --check 52711029 60c5225f` exits 0 (`raw/diff-check.txt`). This is my own
  invocation of the corrected endpoint pair, independent of the manager's corrected row.

## 3. Pinned tool identity (independent)

- Scoped selector `<pinned>` (sha256 `905795b9...`) execs `<layer>/usr/bin/verilator`
  with `VERILATOR_ROOT=<layer>/usr/share/verilator`. `--version`:
  `Verilator 5.050 2026-07-01 rev v5.050`. PATH `verilator` is 5.052 and was not used.
- Chain: the cached `verilator-5.050-1-x86_64.pkg.tar.zst` has a good `gpgv` signature
  (key B5971F2C5C10A9A08C60030F786C63F330D7CB92). The host and layer archives are identical
  (sha256 `3dea7f43...`). The archive `.MTREE` equals the layer's local-db mtree
  (sha256 `350cb0c0...`).
- 123 of 123 regular files match that mtree. 4 man pages are absent and are not build inputs.
- `usr/bin/verilator_bin` sha256 `44898b22...` equals the manager's recorded binary hash.
- `usr/share/verilator/bin/verilator_bin` execs `$RealBin/../../../bin/verilator_bin`, the
  layer binary, not the host one.
- Receipts: `raw/tool-identity.txt`, `raw/tool-mtree.txt`, `raw/tool-package-chain.txt`.

## 4. Findings

### F1

[R239] MINOR Docs - docs/testing/ASSERTIONS.md:85-86 and :154-157 - reset and past-state tool semantics are misstated

Requirement/evidence: The settled contract requires the guide to document reset and past
state. The page says each tool fact "was measured" (lines 6-8, 67-68). Two statements are
contradicted by measurement on the pinned tool:
(a) Line 85-86: "An attempt that starts during reset ... neither fails nor passes."
In `raw/probe-reset-R1.log`, s0 is offered and stalled at reset edge 9. At the first
running edge 10, the pass actions of `u_s0_stimulus` and `u_m_dut`
`ap_tvalid_held_until_handshake` run with flag 0: a vacuous pass.
The generated model shows why (`raw/model-w8/Vaxis_mux_rr_2in_1out___024root__0.cpp`,
sha256 `674d69b5...`). The antecedent register is
`_Vpast_2_1 = sampled(rst_n) & sampled(stalled_w)` (lines 660-662). The consequent edge is
gated by `if (rst_n)`, and the pass action runs whenever the check does not fail
(lines 393-404). So an attempt that completes in reset is abandoned. An attempt that starts
in reset passes vacuously.
(b) Lines 154-157: at the first edge the "previous" value is "the variable's initial value".
`raw/pastprobe-run.log` contradicts this. `one` is declared `= 1'b1` and never changes, yet
at the first edge `$past(one) == 1'b1` fails and `$stable(one)` fails.
`raw/xprobe-run-plain.log` agrees. The previous value is the past register's 0, whatever the
variable's initial value.
Impact: The guide is the reusable how-to for future checkers (acceptance criterion 3). Two
failure paths follow from these statements:
- A witness flag written without `rst_n` inside `$past(...)`, trusting (a), reports
  non-vacuous checks that the tool treated as vacuous. That is false coverage.
- A property without `disable iff`, like `ap_reset_releases_owner`, that uses
  `$past`/`$stable` on a signal initialised non-zero fails at the first edge, contrary to (b).
The checker in this PR is not affected: its flags fold `rst_n`, and its harness holds reset
first.
Required change: Line 85-86 must state the measured behaviour: an attempt completing on a
reset edge is skipped; an attempt starting on a reset edge passes vacuously (pass action
runs, flag 0). The Witnesses section should state why `rst_n` must be inside the flag's
`$past`. Lines 154-157 must say the first-edge previous value is 0 regardless of the
variable's initial value.
Verification: Re-read the corrected lines against `raw/probe-reset-R1.log` and
`raw/pastprobe-run.log`, or rerun `scripts/probes/probe_reset.cpp` (case R1, `+trace`) and
`scripts/probes/pastprobe.sv` on the pinned 5.050. Rerun the docs gates. The lens stays
Docs; no other lens is attributable, because checker and harness behaviour are correct.

### F2

[R239] MINOR Docs - docs/testing/TESTING.md:443, tb/verilator/README.md:51, tb/verilator/ptp_ts/mux_sva_main.cpp:15-19 - witness grading is overstated

Requirement/evidence: TESTING.md:443 says "each property's non-vacuous witness count must
match the harness's own port count". tb/verilator/README.md:51 says the witnesses "must match
the harness's port counts". The harness header (mux_sva_main.cpp:15-19) says that where
internal state is involved "the port-visible events that imply it are a floor". The harness
applies three bounds (mux_sva_main.cpp:925-966; docs/testing/ASSERTIONS.md:184-188 states
them correctly):
- 15 of 21 pairs must be equal.
- 2 have a floor (`ap_owner_held_until_tlast_handshake`, `ap_grant_only_to_requester`).
- 4 immediate laws need only both counts above zero, not a floor.
Measured in `raw/focused-witness-and-tallies.txt`:
- w8: `ap_owner_held_until_tlast_handshake` 787 vs 379 (at least);
  `ai_grants_mutually_exclusive` 1514 vs 677 (both above zero).
- w64: `ai_tvalid_forwarded` 1689 vs 754 (both above zero).
Impact: The testing index and the suite README are where a reader judges what a suite
proves. Both claim equality for all 21 pairs. The harness header claims a floor for the
immediate laws. Both state a stronger check than the one that runs.
Required change: The three summaries must state the bound actually applied (equal / floor /
presence, 15/2/4), or defer to ASSERTIONS.md's precise statement.
Verification: Compare the corrected text with `grade_witnesses()` and the printed witness
table of `make mux-sva`. A commit touching `mux_sva_main.cpp` changes a Tests- and
Robustness-scope artifact, so those lenses must be re-covered at that head (section 7).

### F3

[R239] MINOR Docs - docs/testing/ASSERTIONS.md:278-280 - the no-formal limitation carries unmeasured claims about formal tools

Requirement/evidence: The settled contract requires stating that the evidence does not
establish a formal proof, and the review brief requires the no-formal limitation to match
executable behaviour. Lines 278-280 add two claims that nothing in this PR or repository
measured:
- "The properties avoid unsupported constructs."
- "a formal flow would compile out the DPI witness calls and turn the stimulus instances into
  assumptions."
The page's own rule (lines 6-8, 67-68) is that every tool behaviour stated was measured.
No formal front-end ran. A formal tool proves `assert property` as an assertion; it does not
convert the `u_s*_stimulus` asserts into assumptions by itself. Unconstrained inputs would
make those stimulus properties fail.
Impact: A reader can take the checker as formal-ready. The contract excluded formal, and
the evidence does not support that.
Required change: Keep "Only simulation ran" and "no formal tool has read them". Remove the
construct-support and flow-behaviour claims, or mark them as untested future work. Example:
a formal use would first have to recast the stimulus instances as assumptions.
Verification: Re-read lines 278-280. Rerun `check_em_dash.py --base`, `docs_check.py` and
`gen_toc.py --check`. Docs only.

### Suggestions (optional; they do not affect lens coverage)

[R239] SUGGESTION Tests - tb/verilator/ptp_ts/mux_sva_main.cpp:104-109,123 - the w8 shape cannot see TKEEP forwarding defects
At TDATA_WIDTH 8 every valid beat carries TKEEP=1, which the harness documents. A scratch
mutant `m_tkeep = '1;` in STREAM_0 passes all 8 scenarios at w8: no property fires and no
harness check fails (`raw/extra-mutants.txt`). The w64 shape covers TKEEP
(`mutant-tkeep_hidden_while_stalled-w64`, `mutant-tkeep_from_other_source-w64`). No
document claims w8 TKEEP reach. A TKEEP=0 null-byte TLAST beat at w8 would give the 1-bit
shape reach, if wanted.

[R239] SUGGESTION Robustness - tb/verilator/ptp_ts/sva_campaign.py:535 - `--only` deletes every retained campaign log
`shutil.rmtree(WORK)` runs for `--only` too. Reproducing one row, as ASSERTIONS.md:244-245
suggests, discards the raw per-row logs that ASSERTIONS.md:255-257 says are kept.

[R239] SUGGESTION Robustness - tb/verilator/ptp_ts/mux_sva_main.cpp:530-534,628-635 - an empty `+seed=` is accepted silently
`+seed=` with no value falls back to the default seed and exits 0
(`raw/robustness-plusargs-seeds.txt`). Every other malformed plusarg tried exits 2.

## 5. Clean lenses (same fields as a finding)

[R239] PASS Conformance - issue #372 comment 5776353888; tb/common/sva/axis_stream_source_sva.sv:63-89; tb/common/sva/axis_mux_rr_2in_1out_sva.sv:109-187; tb/common/sva/axis_mux_rr_2in_1out_bind.sv:31-58; tb/verilator/ptp_ts/Makefile:44-94; raw/focused-ptp_ts.log - every in-scope item of the settled contract, and the three acceptance criteria, checked at this head
- Stalled TVALID is held, and TDATA/TKEEP/TLAST are stable until the handshake (IHI0051A 2.2
  as the contract cites it). This is enforced on s0, s1 and m, with stimulus/DUT ownership
  carried in the instance names.
- Grant mutual exclusion, legal state, grant only to a requester, ownership held to the TLAST
  handshake, release after TLAST, and reset release are each a named property.
- Four immediate laws cover forwarding.
- The checker is bound by module name to the unmodified mux.
- Integration is in the existing `ptp_ts` default target (`all: run mux-sva sva-campaign`).
  There is no workflow, global flag, shard or budget change. Shard ownership is a hash of the
  unchanged suite name (`scripts/suite_shards.py:70-81`).
- AC1 is met: the bound SVA passes at w8/w64, 170/171 checks.
- AC2 is met: 62/62 campaign rows, plus my 7/7 extra mutants.
- AC3 is met in substance: the guide covers every required topic; its accuracy defects are
  F1/F3 under Docs.
- Product RTL, firmware and PP/gPTP pins are unchanged (section 2).

[R239] PASS RTL - raw/model-w8/Vaxis_mux_rr_2in_1out___024root__0.cpp:107-194,364-404,644-711,915-944; raw/model-w8/Vaxis_mux_rr_2in_1out__Syms__Slow.cpp; raw/probe-reset-R1/R2/R3.log; hdl/common/axis_mux_rr_2in_1out.sv (blob unchanged) - the elaborated binding and reset/sampling behaviour of the real bound instance, checked against the checker's intent
- Binding is real. Checker scopes exist as `TOP.axis_mux_rr_2in_1out.u_sva{,.u_s0_stimulus,.u_s1_stimulus,.u_m_dut}`.
  The bind's owner flags read the mux's own register `axis_mux_rr_2in_1out__DOT__state`
  (lines 366-369).
- `disable iff (!rst_n) a |=> b` lowers to `if (rst_n) check(!$past(rst_n&&a) || b)`.
  Probes R1-R3 confirm there is no spurious failure for:
  - a 1-edge reset while stalled, with TVALID still high on the reset edge;
  - a 2-edge reset while stalled;
  - a reset on a TLAST handshake edge.
- Sampling is sound. `_sample` copies state and ports at the start of each `eval()`. With the
  harness's settle-then-clock order, properties see the same pre-edge values as the DUT flops
  and the harness's `observe()`. A presented fault fires on that same edge: fault after the
  stall at cycle 5, failure at `[6000]` (`raw/probe-default-errlimit.log`).
- The immediate laws are evaluated on current values at every combinational settle. They
  are invariants of every settled state.
- Scope is a single clock and one module; widths 8/64 are checked, and width 12 is refused
  by `gen_guard_tdata_width`.
- The only product instance, `ptp_ts_top.axis_tx_rx_ts_switch_rr` (64-bit), stays unbound.
  The docs state this.

[R239] PASS Robustness - raw/probe-reset-*.log; raw/robustness-plusargs-seeds.txt; raw/variant-summary.txt and raw/variant-*-build.log; tb/verilator/ptp_ts/sva_campaign.py:289-300,385-388,438-480 - malformed input, reset during activity, backpressure, configuration-dependent and lost-coverage paths
- Malformed plusargs exit 2 (`+scenario=bogus`, `+stimulus_fault=s2_...`, `s0_flip`,
  `+seed=12x`).
- 40 extra seeds per width pass with 0 failures, including random resets.
- Reset edge cases R1-R3 are clean.
- Lost coverage is refused rather than reported as zero:
  - `--no-assert` and the mistyped bind (which builds with 0 diagnostics under `-Wall`);
  - a bind omitted entirely (my variant: 4 scope failures, exit 1, fault not detected);
  - swapped ports (witness failure) and the unused path.
- A width-truncating bind connection fails the `-Wall` build (`%Error: Exiting due to 1
  warning(s)`). An instance-path bind is a syntax error.
- Detection needs exit 3 plus the named path. Compile failures, watchdogs and other exits are
  not detections.

[R239] PASS Tests - raw/focused-ptp_ts.log; raw/focused-campaign-rows.txt; raw/extra-mutants.txt; raw/focused-verdict.txt; raw/focused-tally/tally.txt; tb/verilator/ptp_ts/mux_sva_main.cpp:348-418,925-977 - defect sensitivity, independence, attribution and expected-failure separation
- Every one of the 21 (instance, property) pairs is failed, by its own name, by at least one
  campaign row.
- My 7 extra mutants on other branches, ports and widths are each caught by the named
  property. A scratch mutant must build, and the pattern must match exactly once.
- The scoreboard reads only ports. The round-robin inversion is caught by the scoreboard with
  no property firing.
- 170 checks = 4 scope + 8 reset + 120 packet-intact + 16 scenario-close + 1 alternation
  + 21 witness. 171 is the same with 121 packets.
- 62 campaign rows = 2 clean + 16 stimulus + 14 mutant + 1 scoreboard + 1 elaboration
  + 28 coverage.
- The original `ptp_ts` count is 92. `sim_main.cpp` blob `aefba00b` and the run recipe,
  VFLAGS and SRCS are unchanged.
- The suite log has 0 `Assertion failed`, 0 `[FAIL]` and 0 `SVA-STOP` lines. Expected
  failures stay in 38 row directories.
- `suite_tally --verdict` exits 0. The tally is 495 checks in 4 tallies, owned by `ptp_ts`.
- Witness counts are reproducible: w64 `u_m_dut` 228/228, `u_s0_stimulus` 625/625.

Docs (not clean, see F1-F3). Checked clean within Docs:
- 11 docs-workflow gates at the head, invoked as `docs.yml` does, exit 0 (`raw/static/summary.txt`).
- `check_em_dash --base 52711029`: 0 findings over 292 added lines.
- The index rows link correctly.
- ASSERTIONS.md's other tool facts match measurement:
  - default-on since 5.038 (upstream v5.050 `Changes` line 875, in the 5.038 section);
  - `--no-assert` removes the scopes;
  - bind is by module name only;
  - a mistyped bind is silent;
  - the failure line format;
  - `Verilog $stop`, then exit 1 at the default limit;
  - pass actions run on vacuous edges;
  - `$past` works inside a pass action;
  - `cover` needs `--coverage-user`;
  - `assume` prints the same line;
  - two-state X reads as 0;
  - 5.050 is the workflow pin.
- The first run of the static subset refused 5 gates (exit 2) because the scratch clone had
  no processor submodules. After initialising them from the review clone's local checkouts,
  all 11 exit 0. The rerun overwrote the refusal logs.

## 6. Reviewer-owned ledger

| Lens | Covering round | Head | State |
|---|---|---|---|
| Conformance | R239-1 | 60c5225fe5f93209bf313c51b7a722f25f9aaa7d | covered clean |
| RTL | R239-1 | 60c5225fe5f93209bf313c51b7a722f25f9aaa7d | covered clean |
| Robustness | R239-1 | 60c5225fe5f93209bf313c51b7a722f25f9aaa7d | covered clean (2 optional SUGGESTIONs) |
| Tests | R239-1 | 60c5225fe5f93209bf313c51b7a722f25f9aaa7d | covered clean (1 optional SUGGESTION) |
| Docs | R239-1 | 60c5225fe5f93209bf313c51b7a722f25f9aaa7d | NOT clean: F1, F2, F3 (MINOR) open |

The clean rows hold only while no later commit touches an artifact in that lens's scope.
A fix confined to ASSERTIONS.md, TESTING.md and tb/verilator/README.md needs Docs re-covered.
A fix that also edits `mux_sva_main.cpp` needs Tests and Robustness re-covered at that head.
Moving a finding to another Issue does not resolve it.

## 7. Evidence I did not produce, and pending gates

- **Manager packet (`eb069041/.../candidate1`).** I inspected it at ledger level only.
  - Identities (`candidate.json`) match section 2.
  - Five native commands exit 0 at `60c5225f`. The parent sweep shows 55/55 suites and
    2,118,667 checks. Behave ran 14 features, 316 scenarios and 1515 steps, 0 skipped.
  - The 4 declared `tsn_fuzz` field-campaign skips contribute 0 checks.
  - The packet's `ptp_ts.log` shows the same 92/170/171/62 and 62 `[PASS]` rows.
  - `manager-builder-final` is a composed ledger, exit 0. Only command index 43 is the
    corrected whitespace invocation; the stale raw rows are not that check.
  - Builder calibration gate 11 is NOT RUN; it is not hardware evidence.
  - I did not rerun the full native parent, Yosys, processor or builder banks.
- **Hosted checks at `60c5225f`, captured 2026-09-22T18:03:37+02:00** (`raw/hosted-check-runs.tsv`).
  - `rtl-fast`, `elaborate`, `docs-check`, `docs-check-no-git` and `wire-accountability`
    completed with success.
  - `verilator-suites` and `yosys-portability` were not yet emitted; Verilator shard 4/5 was
    still in progress.
  - The worker that owns `ptp_ts` is shard 2/5 (`raw/ptp_ts-shard-owner.txt`). It completed
    on Verilator 5.050 with `PASS ptp_ts`, 10/10 suites and 1,522,826 checks
    (`raw/hosted-verilator-shard2.log`). That is one worker's result, not the aggregate.
  - `Physical gPTP (nightly and manual)` was skipped.
- **Pending.**
  - The trusted act replica result. I did not run act or the candidate's act_ci.
  - Both hosted aggregates.
  - R240's external round, which I have not read.
  - Final current-dev candidate validation. Dev had advanced to `483a133e` at publication, and
    this candidate was built against `52711029`.
  - Merge authorization, containment and Done/closure.

## 8. Integrity of the review clone

`raw/clone-integrity.txt`: INTEGRITY PASS.
- HEAD and tree are exact.
- The index equals the tree, 861/861 records.
- There are 0 assume-unchanged or skip-worktree entries.
- 857/857 worktree blobs match, with kind and mode.
- There are 0 untracked or ignored paths.
- `third_party/verilog-axis` (214), `protocol-processor` (222) and `gptp-processor` (103) are
  checked out at their gitlinks, every file byte-proven, clean.
- All builds, probes and mutants ran in scratch only.

## 9. Local path placeholders (for neutralization)

`<clone>` = $VALIDATION_STORAGE/reviews/r239-372-r1;
`<scratch>` = $VALIDATION_STORAGE/r239-372-r1-work (export `src/`, `probes/`, `gitclone/`);
`<report>` = $WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r1-r239;
`<pinned>` = $VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator;
`<layer>` = the on-disk image layer `.../containers/storage/overlay/9517af57.../diff`.
Scripts: `scripts/README.md`. Receipt hashes: `raw/MANIFEST.sha256`.

R239-1 FINISHED - report `REPORT.md`, verdict [R239] NEGATIVE - exact head 60c5225fe5f93209bf313c51b7a722f25f9aaa7d
