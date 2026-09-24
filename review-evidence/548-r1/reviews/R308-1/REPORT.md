[R308] NEGATIVE - exact head e41703b2948ef53e5cb0dd01a1e13c5632637615

# R308-1: internal independent review of issue #548 / PR #556

- Exact head: `e41703b2948ef53e5cb0dd01a1e13c5632637615`, tree `4dd0f8cb28230a5a8d2e51e5e19ce25a0a24af23`, one commit on base `573f0052a0e4412e81f0845438fcec2086ce5d55`.
- Role: internal reviewer, cleared context, own detached clone. The executor is [A279].
- Scope authority: the #548 issue body (frozen acceptance 1-3) and manager decision issuecomment-5821224656 (STRUCTURAL ZERO; the count is not restored; scope items 1-6).
- Prior public review findings on PR #556: none. There are no PR reviews, no inline comments and no reviewer findings on the issue or the PR at this head, so none are retained or resolved. The other reviewer's report was not read.

## Verdict summary

The pinned zero is correct and well tested. The register map row, paragraph and group gloss use the page's own STRUCTURAL ZERO legend and name the processor monitor. The #117 page no longer infers presence or eviction from the word. RTL changes are comment-only. The new AXI-Lite check sits after the probe, retry and eviction, and it fails, alone, under three independent nonzero mutants.

One MINOR finding keeps acceptance 2 from being fully met. `milan_csr.sv` still carries two comment blocks, which the PR did not touch, that describe `CTLR_DIAG` as a "RO live" set of three wrapping tallies. So the RTL still does not fully agree with the register map. Once those two blocks are corrected, the pinned zero plus the documentation would meet acceptance 2.

## Findings

### R308-1-F1: MINOR (Conformance, RTL, Docs): the CSR decode table and read mux still document `CTLR_DIAG` as a live count

- **Where:** `hdl/common/csr/milan_csr.sv:761-763` and `hdl/common/csr/milan_csr.sv:2395-2399` at `e41703b2`. Both blocks are byte-identical to base `573f0052` (`receipts/reference-sweep.txt`).
  - `:761-763` reads: "gh #59 departing-controller detection (Milan v1.2 §5.4.5.3). RO live, one word: {evictions[31:24], CONTROLLER_AVAILABLE replies seen[23:12], CONTROLLER_AVAILABLE probes sent[11:0]}. All three wrap."
  - `:2395-2399` reads: "probes sent / replies seen / controllers shed. All three climb together on a healthy bench ... a climbing eviction count with a static reply count is a controller that died without deregistering".
- **Authority/evidence:**
  - Issue #548 acceptance 2 says: "Make the RTL, REGISTER_MAP and any page that reads it agree".
  - The manager decision's scope item 4 covers any other current artifact that reads 0x6F4 as a live count.
  - The PR corrected the same statement at `milan_csr.sv:309-312`, `milan_datapath.sv:1500-1502` and `:3204-3205`, but it left these two. At this head the decode-table entry for the address and the read-mux arm that serves it are the only places in the tree that still call the word live. The builder treats the decode table as the RTL's own statement of the CSR map (`sw/builder/test_builder.py:2708`).
  - These `//!` lines are not rendered into the generated HDL reference: a multi-declarator `localparam` takes its description from the statement's first line (`scripts/gen_hdl_reference_comments.py:138-145`). So the stale text is source-only. That is why this is MINOR rather than MAJOR.
- **Impact:** Someone working from the RTL reads that 0x6F4 carries live probe, reply and eviction tallies and how to interpret them. This is the same misreading #548 exists to remove, now in the file the register map calls normative. It contradicts `REGISTER_MAP.md:1244` and `:1248-1257` and the corrected port comment 450 lines earlier in the same file.
- **Required outcome:** Both blocks agree with the decision. They either state STRUCTURAL ZERO or point to the `:309` comment. Neither claims a live, wrapping or climbing count. The existing reserved-word note for 0x6F8/0x6FC stays intact. No functional RTL change.
- **Verification:**
  - `scripts/rtl_comment_free_identity.py <repo> 573f0052a0e4412e81f0845438fcec2086ce5d55 <new head> hdl/common/csr/milan_csr.sv hdl/milan/milan_datapath.sv` still prints `IDENTICAL`.
  - A sweep of `CTLR_DIAG|0x6F4|ctlr_diag` outside `docs/history` finds no live-count wording.
  - The reviewer re-covers Conformance, RTL and Docs at the new head. The notify leg need not be rerun for a comment-only change, but the Tests lens must confirm the change is comment-only.

### R308-1-S1: SUGGESTION (Tests, Robustness): a zero-expected AXI read cannot tell a zero from a timed-out read

- **Where:** `tb/verilator/milan_dp/sim_nxn.cpp:612-626` (`axi_read`), used by the new check at `:1596-1597`.
- **Evidence:** `axi_read` initialises `v = 0` and returns it when `rvalid` never asserts within `kAxiGuardCycles`. It also ignores `rresp`. A hung or erroring read path would therefore satisfy `ck(..., axi_read(0x6F4), 0)`.
- **Mitigation already present:** Reviewer mutant m2 changes only the CSR read-mux arm. It read back `0x80000000` at that exact point, so the AXI-Lite path does deliver `live_mux` data there at this head.
- **Optional change:** Have the zero-pinning read also assert that `rvalid` was observed with an OKAY response. This is optional and does not affect coverage.

### R308-1-S2: SUGGESTION (Docs): the row drops the old field layout that sibling STRUCTURAL ZERO rows keep

- **Where:** `docs/reference/REGISTER_MAP.md:1244`.
- **Evidence:** Sibling rows keep a "Was: ..." layout for old decoders, for example `ACMPL_DBG` at `:1241`, `BDBG0..2` at `:951-953` and `AECP_STAT1` at `:1063`. The 0x6F4 row names the deleted counters but not their `[31:24]/[23:12]/[11:0]` positions.
- **Optional change:** Keep the old layout as "Was: ..." so an old decoder can be recognised.

### Out-of-scope observation (not a finding against this PR; recommend a new Issue)

`hdl/common/csr/milan_csr.sv:758` still labels `A_ACMPL_DBG` (0x6E8) "RO live: listener walker forensics". `REGISTER_MAP.md:1241` and the TOC gloss at `:188` call that word STRUCTURAL ZERO. #548 is scoped to 0x6F4, so this belongs in its own Issue.

## Lens results (artifact evidence at `e41703b2`)

```text
[R308] MINOR Conformance: hdl/common/csr/milan_csr.sv:761-763, :2395-2399. Acceptance 2 is not fully met; see R308-1-F1.
[R308] MINOR RTL: hdl/common/csr/milan_csr.sv:761-763, :2395-2399. The module's own decode and read-mux documentation contradicts the tied-zero contract; see R308-1-F1.
[R308] MINOR Docs: hdl/common/csr/milan_csr.sv:761-763, :2395-2399. In-source documentation contradicts REGISTER_MAP.md:1244/1248-1257; see R308-1-F1.
[R308] PASS Robustness: hdl/milan/milan_datapath.sv:3206, hdl/common/csr/milan_csr.sv:2400. The tie is an unconditional constant, independent of shape, config, reset and traffic. The read arm is unchanged. The comment-free RTL is identical to base, so no reset, backpressure or config path changed. The zero holds after probe, retry and eviction (receipts/clean-run.log:137-148).
[R308] PASS Tests: tb/verilator/milan_dp/sim_nxn.cpp:1594-1597 and receipts/notify-probe-verdict.txt. The clean leg gives 147 checks and 0 failures. Three mutants (datapath tie 0x01001001, CSR read-mux MSB only, datapath tie 1) each exit 1 with exactly this check failing.
```

What was checked under each lens:

### Conformance

- Acceptance 1: the decision is recorded (issuecomment-5821224656), and the implementation follows STRUCTURAL ZERO without restoring the count.
- Acceptance 2:
  - Register map row `REGISTER_MAP.md:1244`, paragraph `:1248-1257` and group TOC gloss `:188`: each uses the legend at `:101`, "The source of this word is deleted and has no replacement ... Never read it as a measurement".
  - The paragraph names `KL_aecp_notify` and `KL_aecp_ca_originator`. Both exist at gitlink `09f9bf38` and carry the 5.4.5.3 monitor (`KL_aecp_notify.sv:91-94`, `KL_aecp_ca_originator.sv:6`).
  - The processor top exports no monitor count (`protocol_processor_top.sv` outputs, `receipts/reference-sweep.txt`), so "no replacement source" is true.
  - #117 page (`117_GPTP_SILICON_EVIDENCE.md:468-474`, `:524`): keeps the wire facts (registration 13:10:47.0, deregistration 13:11:26.5, both SUCCESS), states the word is STRUCTURAL ZERO, and no longer infers presence or eviction.
  - Remaining gap: R308-1-F1.
- Scope items 1-5 were checked as above. For item 6, `sw/builder/test_builder.py` and `docs/history/` are untouched (`git diff --stat` shows 5 files; `receipts/reference-sweep.txt`).

### RTL

- `receipts/rtl_comment_free_identity.txt`: comment-free `milan_csr.sv` and `milan_datapath.sv` are byte-identical to `573f0052` (sha256 `2c885e5a...` and `f302c0ef...` on both sides).
- The stripper detects a real change (`receipts/stripper-control.txt`). No non-comment line changed in `hdl/`.
- The new comments at `milan_csr.sv:309-312` and `milan_datapath.sv:1500-1502` and `:3204-3205` are accurate.
- Gap: R308-1-F1.

### Robustness

- Nothing functional changed (RTL identity above).
- The zero is a constant assign with no state, reset or configuration dependence.
- The check reads after controller traffic, including an eviction.
- No robustness regression is possible from comment and documentation edits. The one test-side vacuity risk is recorded as S1 (SUGGESTION).

### Tests

- The new check sits after the probe, retry, deregistration and never-probed-A checks (`sim_nxn.cpp:1559-1593`). It reads through the real AXI-Lite slave (`axi_read`, `:612`).
- Clean run: probe at 35791 ms, retry at 36041 ms, DEREGISTER at 36292 ms, then `CTLR_DIAG = 0x0`. Result: 147 checks, 0 failures (`receipts/clean-run.log`).
- Mutants, own build recipe from `make -n run` (`receipts/recipe-dryrun.log`) with the pinned simulator:
  - m1: author's arm reproduced independently, `got=0x1001001`.
  - m2: reviewer arm at a different injection point (CSR read mux), `got=0x80000000`.
  - m3: reviewer arm with the smallest nonzero value, `got=0x1`.
  - Each gives 147 checks and 1 failure, and it is exactly this check (`receipts/*-run.log`, `receipts/notify-probe-verdict.txt`).
- The check can fail for the defect it claims to detect, and no other check moves.

### Docs

- REGISTER_MAP and #117 wording were checked as above.
- Gates rerun at head (`receipts/docs-gates.log`):
  - `docs_check.py` in Git and no-Git inventory modes: rc 0.
  - `check_doc_style.py`: rc 0.
  - `check_doc_paths.py`: rc 0.
  - `check_cpp_idiom.py`: rc 0.
  - `git diff --check` over the range: rc 0.
  - `gen_toc.py --check` and `check_em_dash.py --base 573f0052`: rc 2 on the host, which lacks the pinned renderer. Both return rc 0 in a disposable scratch environment installed from `tools/markdown/requirements.txt` with `--require-hashes`.
- The anchor `#how-to-read-this-page-now-three-verdicts-and-why-the-distinction-matters` resolves to `REGISTER_MAP.md:92`.
- Gap: R308-1-F1.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R308-1-F1 open) | #548 body and decision comment; REGISTER_MAP.md:92-103,188,1244,1248-1257; 117_GPTP_SILICON_EVIDENCE.md:468-474,524; milan_csr.sv:309-312,761-766,2395-2400; processor `KL_aecp_notify.sv`, `KL_aecp_ca_originator.sv`, `protocol_processor_top.sv` at 09f9bf38 | R308-1 | e41703b2948ef53e5cb0dd01a1e13c5632637615 |
| RTL | UNCLEAN (R308-1-F1 open) | comment-free identity of milan_csr.sv and milan_datapath.sv versus 573f0052; milan_datapath.sv:1500-1503,2535,3204-3206; milan_csr.sv:309-313,761-766,2395-2400 | R308-1 | e41703b2948ef53e5cb0dd01a1e13c5632637615 |
| Robustness | CLEAN | milan_datapath.sv:3206; milan_csr.sv:2400; receipts/clean-run.log:137-148 | R308-1 | e41703b2948ef53e5cb0dd01a1e13c5632637615 |
| Tests | CLEAN | sim_nxn.cpp:612-626,1559-1597; receipts/clean-run.log; m1/m2/m3 run logs; notify-probe-verdict.txt | R308-1 | e41703b2948ef53e5cb0dd01a1e13c5632637615 |
| Docs | UNCLEAN (R308-1-F1 open) | REGISTER_MAP.md; 117_GPTP_SILICON_EVIDENCE.md; milan_csr.sv comments; receipts/docs-gates.log | R308-1 | e41703b2948ef53e5cb0dd01a1e13c5632637615 |

A fix for F1 changes `milan_csr.sv` comments. That touches the scope of Conformance, RTL and Docs, and the RTL-identity part of Tests. Those lenses must be re-covered at the new head. Robustness stays banked only if the new head's comment-free RTL is still identical to `573f0052`.

## Real limits

- Physical calibration and hardware were NOT RUN. Field skips are not hardware proof. The #117 page is judged as documentation only; no bench data was re-examined.
- The full parent, PP, gPTP, Yosys and builder banks, the default `make -C tb/verilator/milan_dp` sweep, and the act/hosted replicas were not run by this reviewer, as the brief does not allow them. Only the timed notification leg (`obj_notify`) was built and run, at head and under three mutants, with the pinned simulator (Verilator 5.050 wrapper sha256 `905795b9...`, `--version` "5.050 2026-07-01 rev v5.050"). The author ran a different local simulator release; the leg results agree.
- The public evidence tree at `ae967643` contains the author's packet only (33 entries, all `author/`). No separate manager bank receipts were found there or in issue or PR comments. This verdict does not rely on the manager's bank results.
- Hosted snapshot at this head (`receipts/hosted-check-runs-snapshot.txt`):
  - `rtl-fast`, docs, lint, elaboration, BDD and Yosys shards: success.
  - Verilator shards 1/5 and 4/5: still in progress.
  - Physical gPTP: skipped.
  - Hosted acceptance is the manager's.
- Receipts had host paths replaced by `$CLONE`, `$PACKET`, `$PINNED_SIM` and `$SIM_ROOT` after the run. The pass/fail judgement was computed before redaction.
- Probe hygiene: the build prerequisites (`ltn_rom.hex`, `ucode.hex`) and interpreter caches generated in the clone were removed. `receipts/restore-verification.txt` confirms:
  - HEAD and tree are exact.
  - `status --porcelain --ignored` is empty.
  - The index equals the HEAD tree (mode and blob per path).
  - 882 worktree blobs rehash equal with 0 mismatches, and executable bits match the modes.
  - The gitlinks for `external` (uninitialised), `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` match HEAD and are clean.

## Pending manager duties

- Route R308-1-F1 to the executor. A comment-only fix is expected, and it needs a re-review at the new head covering Conformance, RTL, Docs and the Tests identity check.
- Decide whether to file a separate Issue for the stale `A_ACMPL_DBG` "RO live" comment at `milan_csr.sv:758`.
- Exact-head hosted acceptance, including the two Verilator shards still in progress, and the act replica.
- The final current-dev candidate merge build and validation. Source base and live dev are both `573f0052`.
- Merge requires two independent POSITIVE verdicts and a reviewer-accepted ledger at the merge head.

R308-1 FINISHED
