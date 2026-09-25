[R320] POSITIVE - exact head 5beebb7c7edd908d08be34e52286c9eee441f5b3

# R320-2: issue #443 / PR #561, internal independent delta review

- Role: internal cleared-context reviewer; round-2 executor [A301]; assignment: issue comment 5826779078.
- Exact head `5beebb7c7edd908d08be34e52286c9eee441f5b3`, tree `f1210ce331ebf00f39187ca02021f85d66b4ee2c`.
- Source base `0755923d983218ca6ca9db6891a558cbe6425b8d`. Round-1 head `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e`.
- Delta `c9bbb03c..5beebb7c`: one commit, 10 files, +110/-17. The commit is one line with no trailers.
  - Changed: `CHANGELOG.md`, `docs/reference/REGISTER_MAP.md`, `docs/testing/TESTING.md`,
    `scripts/measure_test_evidence.py`, `tb/verilator/csr/sim_main.cpp`, `tb/verilator/csr/sim_win.cpp`,
    `tb/verilator/milan_dp/{Makefile,README.md,render_csr_controls.py,sim_aclk.cpp}`.
  - No RTL change. The blobs of `milan_csr.sv` (`4a194ada`), `milan_datapath.sv` (`10a21957`) and
    `KL_render_setpoint.sv` (`e66b427d`) are identical at both heads. The four gitlinks are unchanged too
    (`receipts/delta-scope.txt`).
- Scope reconstructed from:
  - AGENTS.md and CONTRIBUTING.md;
  - the issue #443 body;
  - decision 5789749713 (item 4: counters/CSR state only, no `STREAM_INTERRUPTED`);
  - assignment 5826079535 (items 1, 2, 3, 5);
  - round-2 assignment 5826779078 (items 1-5, including the VERSION decision);
  - review-ready 5826943017;
  - REQ-CSR-01/02/05 and the `REGISTER_MAP.md` legend and claim rule;
  - the full diff `0755923d..5beebb7c`, and the delta above hunk by hunk.
- Verdict POSITIVE. All five lenses were applied at this head. Every round-1 finding of this reviewer (F1-F3) is
  closed with executable or textual evidence. So are the concurrent-round items retained at round 1 (X2, X3).
  No new MINOR or higher finding. One SUGGESTION carries over (S2, residual).

## Round-1 findings: closure at this head

| Round-1 item | Status | Evidence at `5beebb7c` |
|---|---|---|
| F1 (Tests, Docs, Conformance): CSR bench asserted `0x8DC` unmapped and never drove `i_render_status` | CLOSED | The bench no longer calls `0x8DC` unmapped. The neighbours stay graded unmapped: `0x8E0` and `0x8F4` (`tb/verilator/csr/sim_main.cpp:1224-1225`). A driven `render_status_word()` (`:1429-1449`) grades five things: the absent-source tie reading 0; the `0x100` prefill reset word; all 32 bits of a selected word (`0xA5C30216`); writes ignored; and talker and out-of-range selections reading 0. It also grades full-width saturated rails (`0xFFFF0100`). The N=4 leg (`sim_win.cpp:700-718`) grades each of the four listener indices. Bench runs: 380/0, 380/0, 115/0, 38/0 and 380/0 (`receipts/csr-bench-head.log`). My round-1 no-decode recipe (the `A_RENDER_STAT` case arm and its window term removed) now **fails**, rc 2, at `RENDER_STAT driven prefill reset word got=0x0 exp=0x100` and three more `RENDER_STAT` checks (`receipts/csr-probe-nodecode.log`). Round 1 recorded a pass of 371/0. Five more CSR-bench mutants are all caught at named `RENDER_STAT` checks (`receipts/csr-bench-probes-{1,2}.log`): direction ignored, index aliased to 0, bit 9 forcing listener 0, upper rail byte zeroed, and window term dropped. |
| F2 (Conformance, RTL, Docs): additive word without a VERSION step or recorded exemption | CLOSED by route (b) | The manager decision is recorded in item 4 of comment 5826779078: follow current practice. VERSION stays `0x0002_0060` (`milan_csr.sv:196`, unchanged blob), and the release step owns the minor bump. `CHANGELOG.md:31-39` has the `Unreleased - render setpoint state` entry, which names `RENDER_STAT` at `0x8DC` and states that VERSION remains `0x0002_0060` and the release step owns the bump. It links the decision comment; I checked that the link resolves to 5826779078. It matches the existing deferral at `CHANGELOG.md:133-135` (`GPTP_DROPE[31:16]`, "VERSION is unchanged; the release step owns the bump"). The 0x8DC section says how to identify the addition, as route (b) required (`REGISTER_MAP.md:1945-1948`): "Before that bump, VERSION alone cannot identify this addition. Verify the build's source revision includes #443's register decode." The entry has a Contents line (`CHANGELOG.md:11`), and `gen_toc --check` and `--verify-anchors` pass. |
| F3 (Docs): the Register groups index omitted `0x8DC` | CLOSED | `REGISTER_MAP.md:242` has a row between `0x8D4` and `0x8F8`. It names `RENDER_STAT` and says: RO live, selected-listener state and global rails, structural zero without the stage, VERSION minor stays `0x0060`, and the release step owns the bump. That is consistent with F2's route and the CHANGELOG entry. No text source still calls `0x8DC` free. The only remaining unmapped statement is `REGISTER_MAP.md:1821`, "`0x8E0` to `0x8F4` remain unmapped", which the bench now grades at both ends. |
| X2 (Tests), was S1: `STRM_SEL[9]` "does not change this word's selection" was not graded | CLOSED | `sim_aclk.cpp:404-409` grades `0x300` reading 0 (`RENDER-CSR: bit 9 preserves talker rejection`) and `0x200` mirroring the taps. `sim_win.cpp:704-715` grades `0x200|s` for s = 0..3 against distinct words (`RENDER_STAT bit 9 preserves the listener index`) and `0x303` reading 0. My unchanged round-1 probe `csr_lsn0_window_semantics` changed outcome. Round 1: SURVIVED. This head: caught, rc 1, at `RENDER-CSR: bit 9 preserves talker rejection got=65550 exp=0` (`receipts/render-csr-probes-r1-b.log`; the script's "unexpected" label is the change being verified). On the N=4 CSR bench the same mutant fails `bit 9 preserves the listener index` three times (`receipts/csr-probe-lsn0_window_semantics.log`). The campaign now plants it too (`render_csr_controls.py:54-66`), and it fails that named check (`receipts/render-csr-controls.log`). |
| X3 (Tests, Docs): the explicit campaign was missing from `TESTING.md` | CLOSED | `docs/testing/TESTING.md:265` lists `render_csr_controls.py`, `make -C tb/verilator/milan_dp render-csr-controls`, and who runs it. The named identifiers exist, for example `render_status_w` at `milan_datapath.sv:1202,2588,6163`. |
| S3 (Docs, suggestion): shared-selector caveats | Taken | `REGISTER_MAP.md:1957-1961`. The claim that a selector write invalidates the ACMP/SRP snapshots is true in RTL: `sel_wr_w` clears `srp_fresh_r` and `acmp_fresh_r` (`milan_csr.sv:2838,3030,3081`). |
| S4 (Docs, suggestion): disclose the TDM frame-pin sentence change | Taken | PR body, first paragraph: "The latency page also corrects its TDM frame-pin statement". |
| S2 (Tests, suggestion): upper rail byte proven only by width review | Partly taken; residual SUGGESTION | The CSR half is now graded: `upper_rails_zeroed` is caught (`receipts/csr-probe-upper_rails_zeroed.log`). The datapath packing half still survives the integration legs, and my unchanged round-1 probe `dp_rails_upper_byte_zero` SURVIVED again (`receipts/render-csr-probes-r1-b.log`). The packing `{rsp_rails_w, 6'd0, ...}` at `milan_datapath.sv:6163-6166` is width-exact by static review. |

## Delta review (hunks not covered above)

- `tb/verilator/milan_dp/Makefile:107-108,196`: `CSR_SRC ?=` defaults to the tracked `milan_csr.sv`. It is used
  only in `SRCS`. Every other reference to `milan_csr` in the Makefile is a comment, so the default elaboration
  is unchanged.
- `render_csr_controls.py`: it requires the selector anchor exactly once and writes the mutant into a temporary
  directory. Its tally is now `1 + len(cases)` = 4. The absent-stage and wrong-fill cases are unchanged.
- `scripts/measure_test_evidence.py:614-618`: the new DUT-source-reader disposition describes the campaign
  accurately. `--check` passes the ratchet, and `--selftest` passes 101/101.
- `tb/verilator/milan_dp/README.md`: the control table gains the bit-9 row, and the text now says three extra
  elaborations. Both match the campaign.

## Reproduced at this head (scoped simulator 5.050, at most 8 jobs, disposable copy of the clone)

| Run | Result | Receipt |
|---|---|---|
| `tb/verilator/csr`: all five executables, `-j 8` | 380/0, 380/0, 115/0, 38/0, 380/0; rc 0 | `receipts/csr-bench-head.log`, `.rc` |
| CSR-bench mutants (6) | 6/6 caught at named `RENDER_STAT` checks | `receipts/csr-bench-probes-{1,2}.log`, `receipts/csr-probe-*.log` |
| `make -C tb/verilator/milan_dp aclk` | `media_aclk: 189 checks, 0 failures` (round 1: 188), 46 `RENDER-CSR` lines; rc 0 | `receipts/aclk-default-head.log`, `.rc` |
| `make -C tb/verilator/milan_dp render-csr-controls` | clean 63/0; wrong-fill caught at `RENDER-CSR: filling mirrors taps` (got 256, exp 262); bit-9 caught at `RENDER-CSR: bit 9 preserves talker rejection` (got 65550, exp 0); absent stage 32/0; `4 checks, 0 failures`; rc 0 | `receipts/render-csr-controls.log`, `.rc` |
| Round-1 probe script, unchanged (sha256 `e6acfa7a...`, same as the round-1 packet) | 9 of 10 outcomes as at round 1. The 10th is `csr_lsn0_window_semantics`, which moves from SURVIVED to caught (the X2 closure). `csr_lsn0_window_semantics_multi` still survives the two-listener render leg, which does not write bit 9. The N=4 CSR bench grades that instead. | `receipts/render-csr-probes-r1-{a,b}.log` |
| Two-listener `milan_dp_render` clean leg (`tdm8render-multi-build`) | 64/0 | `receipts/milan-dp-render-multi-clean.log`, `.rc` |
| Doc and evidence gates: `gen_toc --verify-anchors` (170 links), `--check`, `--selftest` (1501/1501); `docs_check`; doc style; doc paths; `check_em_dash --base 0755923d` (0 findings over 109 added lines); `gen_module_matrix --check`; `measure_test_evidence --check` and `--selftest`; `git diff --check` | all rc 0 | `receipts/doc-gates.rc` and one `.log` each |

## Findings

No finding at MINOR or higher is open at this head.

- S2-residual, SUGGESTION, Tests: `hdl/milan/milan_datapath.sv:6163-6166`. No integration leg reaches 256
  rails, so a datapath packing that dropped `rsp_rails_w[15:8]` would stay green. The CSR half is now graded.
  - Optional outcome: a rail-count force, or a check at the datapath port, that sets bit 8 or higher.
  - Verification: `dp_rails_upper_byte_zero` in `scripts/render_csr_probes.py` would then be caught.
  - This does not affect coverage.

## Reviewer-owned completion ledger

A lens covered clean at R320-1 counts only if nothing in its scope changed since that head. Every lens was
re-applied here at the exact head.

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #443 acceptance items 1, 2, 3 and 5, and decisions 5789749713/5826779078. REQ-CSR-01: the bench now exercises the decoded word (`sim_main.cpp:1429-1449`; no-decode probe caught). The VERSION deferral is recorded (`CHANGELOG.md:31-39`, `REGISTER_MAP.md:1945-1948`), with no `STREAM_INTERRUPTED` wiring. No RTL change since R320-1, where decode, selection and structural zero were reproduced (`receipts/delta-scope.txt`). | R320-2 | `5beebb7c7edd908d08be34e52286c9eee441f5b3` |
| RTL | CLEAN | `milan_csr.sv:196,922,1761-1765,2389-2395,2561,2838,3030,3081`; `milan_datapath.sv:1202,2588,6163-6166`. The blobs are identical to R320-1's head, and the RTL was re-checked for the new doc claims (`sel_wr_w` snapshot invalidation). The VERSION parameter is left at `0x0002_0060` under the recorded decision, which closes F2's RTL attribution. | R320-2 | `5beebb7c7edd908d08be34e52286c9eee441f5b3` |
| Robustness | CLEAN | Absent-source tie and restore (`sim_main.cpp:325,1432,1446-1447`); writes ignored at N=1 and N=4; talker, out-of-range and bit-9 talker selections; full-width saturated rails; RVALID/RDATA held under backpressure and reset after a rail (`receipts/aclk-default-head.log`); absent stage while ingress runs, 32/0 (`receipts/render-csr-controls.log`). | R320-2 | `5beebb7c7edd908d08be34e52286c9eee441f5b3` |
| Tests | CLEAN (S2-residual is a SUGGESTION) | `tb/verilator/csr/sim_main.cpp:1221-1225,1429-1449,1499`; `sim_win.cpp:700-718,743`; `sim_aclk.cpp:401-413`; `render_csr_controls.py`; `Makefile:107-108,196`; `measure_test_evidence.py:614-618`. Reproduced runs, 6 new CSR-bench mutants and the unchanged 10-case round-1 probe set (`receipts/`). Each new check fails for the defect it names. | R320-2 | `5beebb7c7edd908d08be34e52286c9eee441f5b3` |
| Docs | CLEAN | `REGISTER_MAP.md:242,1821,1940-1961`; `CHANGELOG.md:11,31-39`; `TESTING.md:265`; `tb/verilator/milan_dp/README.md:793-814`; PR body; the doc gates (`receipts/doc-gates.rc`). | R320-2 | `5beebb7c7edd908d08be34e52286c9eee441f5b3` |

## Limits

- Physical calibration NOT RUN. Field skips (builder gate 11, the physical gPTP context) are not hardware
  proof. This round makes no silicon claim.
- Not run by this round: the full `milan_dp` default sweep, the full `milan_dp_render` suite, the builder,
  the static/RTL-lint banks, the synthesis banks and Yosys. RTL is unchanged since R320-1, which reproduced
  the cell counts. For the banks, this round relies on the manager's source static, builder and native banks
  that the review assignment reports as passing. I found no separate manager bank artifact in the evidence
  tree at `8cf594dd` (its `author-r2/` and `reviews/` subtrees only), so I name that reliance and do not
  claim to have verified it.
- The author ran the simulator at 5.052. This round used the scoped 5.050 wrapper (`receipts/tool-identity.txt`).
  The renderer-dependent doc gates ran from a private hash-locked environment under the scratch area.
- Hosted contexts at the exact head, read-only (`receipts/hosted-check-runs.tsv`, captured
  2026-09-25T05:20:07Z):
  - `Verilator shard 4/5` was in progress;
  - `Physical gPTP` was skipped, not executed;
  - every other listed context had completed with success.

  The manager owns hosted and act acceptance.
- Integrity: every build ran in a disposable copy under the scratch area. Afterwards:
  - the review clone's 885 tracked blobs and modes match the index;
  - HEAD, the tree, the index hash, the four submodule gitlinks and the zero untracked/ignored count equal
    the pre-probe state (`receipts/pre-probe-state.txt`, `receipts/post-probe-state.txt`,
    `receipts/blob-verify.txt`);
  - the scratch copy's tracked files are unmodified.

## Pending manager duties

- Hosted acceptance at the exact head (`Verilator shard 4/5` completion, `verilator-suites`,
  `yosys-portability`) and act replication.
- The final candidate against live dev `c533b4818df8b3f581df76aa0d1c6d5f55d20449` (source base `0755923d`),
  with candidate-merge validation and post-merge containment.
- The second (external) positive review. Merge only with explicit maintainer authorization.
- The release step that owns the VERSION minor bump for `RENDER_STAT`.

## Cross-reference to prior public review findings

- Order of work:
  - The verdict, the round-1 closure table and the ledger above were written first. They are frozen as
    `receipts/REPORT-pre-crossref.md` (sha256 in `receipts/REPORT-pre-crossref.sha256`).
  - Only then did I read the other prior public review on this PR: R321-1, issue comment 5826662478 at
    `c9bbb03c`.
  - There are no PR reviews and no inline comments. No R321-2 report was read.
- Each R321-1 item is resolved or retained at this head:

| R321-1 item | Status at `5beebb7c` | Basis |
|---|---|---|
| F1 MINOR (Tests, Docs): the CSR bench asserts `0x8DC` unmapped | RESOLVED | Same defect as R320-1 F1; see the closure table. R321's own verification was dropping the `(rd_addr_q == A_RENDER_STAT)` term. That is my `window_term_dropped`, caught at four `RENDER_STAT` checks (`receipts/csr-probe-window_term_dropped.log`). |
| F2 MINOR (Tests): `STRM_SEL[9]` not graded | RESOLVED | R321's mutant `strm_lsn0_r ? (s == 0) : (...)` is textually identical to my `csr_lsn0_window_semantics` and the campaign's `bit9_window_selection`. It fails by name on the aclk leg (`RENDER-CSR: bit 9 preserves talker rejection`) and on the N=4 CSR bench (`RENDER_STAT bit 9 preserves the listener index`). It still survives the two-listener render leg, which does not write bit 9. The required outcome was "some leg", so that is met. |
| F3 MINOR (Tests, Docs): campaign missing from `TESTING.md` | RESOLVED | `TESTING.md:265`. |
| F4 MINOR (Conformance, Docs): no VERSION bump and no recorded deferral | RESOLVED | The deferral is recorded (comment 5826779078, `CHANGELOG.md:31-39`, `REGISTER_MAP.md:1945-1948`), in the current-practice form R321 cited. |
| F5 MINOR (Docs): the group index lacks `0x8DC` | RESOLVED | `REGISTER_MAP.md:242`, with a minor note consistent with F4. |
| S1 (Docs): reset assumption and shared-selector caveat | Taken | `REGISTER_MAP.md:1957-1961`; the RTL claim was checked (`milan_csr.sv:2838,3030,3081`). |
| S2 (Docs): one sentence on the unexplained `milan_datapath` decrease | Taken | The PR body says: "The decrease is unattributed; these counts make no physical area or timing claim. Round 2 changes no RTL." |

- Effect on this report: none. The verdict, the findings and the ledger stand as frozen. R321-1 records RTL
  and Robustness CLEAN at `c9bbb03c`; this round re-covers both at `5beebb7c`.

R320-2 FINISHED
