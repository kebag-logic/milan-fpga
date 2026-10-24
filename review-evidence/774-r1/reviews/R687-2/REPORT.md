[R687] POSITIVE - exact head 01fc54756f1ffb0a3aa836681215e8321ee7e86c

# R687-2: internal cleared-context review of PR #778 (issue #774), round 2

- **Head under review:** `01fc54756f1ffb0a3aa836681215e8321ee7e86c`, tree `7d8822f99d37284635fc34101123477e0c89846c`. This is also the PR's current head on GitHub.
- **Source base and live dev:** `a032c6d6e3775f145349d5a495c1e1ad12294936`.
- **Delta reviewed:** `git diff 5f0d5bf9..01fc5475`, the five round-2 commits on the head R687-1 reviewed. There was no rebase or amend. The commits are:
  - `bf95d757`: `KL_crf_tx.sv` cast form.
  - `53cd0d38`: SRP-10 and Q-10 wording; regenerated matrix and README-tests.
  - `0d4b4620`: command-table re-pin and `Vmilan_dp_tspec8` command.
  - `2a0085dd`: command-table build forms.
  - `01fc5475`: firmware page count.
- **Whole-PR context:** `git diff a032c6d6..01fc5475` (20 files) was re-read wherever the delta depends on it. The PR changes no submodule gitlink (0 `160000` entries in the raw diff).
- **Reconstructed from:**
  - AGENTS.md and CONTRIBUTING.md.
  - The issue #774 body.
  - The round-2 assignment (issuecomment-6382693550), R687-1 (issuecomment-6382684028), the R688-1 stop note (issuecomment-6382962829), and the round-2 REVIEW READY (issuecomment-6385545886).
  - The PR #778 body.
  - The author's packet at evidence commit `4484c29c` (`review-evidence/774-r1/author-r2`).
  - Hosted check runs at the exact head.
- **Not read:** any other reviewer's round-2 report. The R688-1 stop note carries no findings.

**Verdict: POSITIVE.**
- Every R687-1 finding is resolved at its cause at this head: F1 BLOCKER, F2 MINOR, F3 MINOR and R1 RESIDUE.
- The delta adds no BLOCKER, MAJOR or MINOR.
- All five lenses are covered clean at this head.
- Three SUGGESTIONs are recorded. They are optional and do not affect coverage.

## Prior findings at this head

### R687-1-F1 (BLOCKER; Tests, RTL): RESOLVED

**The RTL change** is at `hdl/ieee1722/crf/KL_crf_tx.sv:235`: `localparam int CRF_PDU_C = CRF_HDR_C + 32'(CRF_DLEN_C);`, replacing `int'(...)`.
- **Same value:** 20 + 8 = 28.
- **Same width:** 32 bits.
- **No new literal:** `CRF_DLEN_C` stays `16'd8` at `:227`, and `FRAME_BYTES = ETH_HDR_C + CRF_PDU_C + 18` at `:241` = 60.
- **Signedness:** the size cast gives an unsigned 32-bit operand where `int'` gave a signed one. The sum is assigned to an `int` localparam, so the value stays 28. `16'(CRF_PDU_C + 1)` = 29 is unchanged.

**The scenario and step are unchanged:** `git diff a032c6d6..01fc5475 -- tests` is empty. The resolver at `tests/steps/crf_class_a_steps.py:72` strips `\d+'(`, which is the form the RTL now uses.

**Executed by me at this head:**
- `cd tests && behave --no-capture -f plain`: rc 0, "406 scenarios passed, 0 failed", 1977 steps (`receipts/bdd/behave-head.log`, `.rc`).
- `bdd_frame_bytes_probe.py` (R687-1's script, sha256 `c0eb117d...`, matching the author's `reviewer-probes.sha256`):
  - At this head: `CRF_PDU_C = 28` and `FRAME_BYTES = 60`, rc 0 (`receipts/bdd/frame_bytes_probe_head.log`).
  - Across dev, `5f0d5bf9` and this head: dev 60, `5f0d5bf9` "no localparam int found", head 60 (`receipts/bdd/frame_bytes_probe.log`). That run's rc 1 comes from the old head only.
- **Falsification** (`scripts/scenario48_fault_probe.sh`, on a disposable copy; `receipts/bdd/scenario48_fault_probe.log`). The unchanged scenario `features/crf_sr_class_a.feature:48` fails "FRAME_BYTES is not 60" for both planted faults:
  - `CRF_DLEN_C = 16'd12`;
  - `CRF_PDU_C + 4`.

  The copy was restored with 0 dirty files afterwards. The author's own 6-fault receipt agrees (`author-r2/receipts/round2/bdd/frame_mutants.log`, 6/6), including the round-1 `int'(...)` form and a non-arithmetic `$bits(...)`.
- **Legs, built from clean copies with the verified Verilator 5.050** (`receipts/legs/`):
  - `make crflic`: 427 checks, 0 failures. `[TSPEC]` gives AAF 217 and CRF 29, and both equal the emitted AVTPDU + 1.
  - `make tspec8`: 61 checks, 0 failures, with eight AAF sources at 217 and CRF at 29.

**Hosted at the exact head** (`receipts/hosted/head-check-runs.tsv`, snapshot time in the file's first line): `bdd-conformance` is completed/success (check run 120901308509), as are `changes` and `verilator-lint`. The other contexts were still queued or in progress at the snapshot.

### R687-1-F2 (MINOR; Docs): RESOLVED

- **The fix:** `docs/traceability/ieee8021q.md:154` (SRP-10) now cites "(Milan 4.3.3.2 Table 4.4)". It carries no version token.
- **This matches the document's convention.** Its other Milan citations are `Milan 4.2.7.1.1`, `4.2.7.1.2` and `4.3.3.2`, plus one pre-existing `Milan v1.2 4.3.2` in a row that names no module. Line 14 also links the document's evaluation to the Milan v1.2 audit.
- **`matrix_clause_probe.py`** (`receipts/docs/matrix_clause_probe.log`):
  - Dev keeps `['35.2.2.8.4', '802.3']`.
  - This head keeps `['35.2.2.8.4', '802.3', '4.3.3.2']`. The tokens in order are `35.2.2.8.4`, `802.3`, `4.3.3.2` and `4.4`, and no `1.2` is among them.
- **The regenerated rows** are at `docs/traceability/MODULE_MATRIX.md:67,98,173` and the three README-tests files:
  - `KL_aaf_packetizer` and `KL_crf_tx`: `35.2.2.8.4, 4.3.3.2, 802.3`.
  - `milan_datapath`: `34.4, 35.2.2.8.4, 35.2.7, 4.3.3.2`.

  A scan of every clause cell for a bare `1.x` token finds none at this head or at dev (`receipts/docs/matrix_version_token_scan.log`).
- **One display change:** `milan_datapath`'s four-entry display cap (`gen_module_matrix.py:422,443`) now shows `4.3.3.2` where dev showed `802.1`. A real clause displaces a standard name inside the display cap; the full clause set is unchanged in kind. This is not a defect.
- **`gen_module_matrix.py --check`:** rc 0, "traceability generator controls: 7/7", "up to date (79 modules, 0 untested)" (`receipts/gates/gen_module_matrix_check.log`).

### R687-1-F3 (MINOR; Tests): RESOLVED

All of the following is in `ci/image/command-table.json` at this head:
- **The re-pin:** `scripts["tb/verilator/milan_dp/crflic_mutants.py"]` is class "reviewed non-installing" with sha256 `baec486a...0015d2`, which equals `sha256sum` of the file at this head. The file is unchanged since R687-1 re-reviewed its class.
- **The new command:** `commands["Vmilan_dp_tspec8"]` is `{"class":"non-installing","executables":["./obj_tspec8/Vmilan_dp_tspec8","Vmilan_dp_tspec8"],"patterns":[[]]}`. It has the same shape as `Vmilan_dp_crflic`.
- **The build forms:**
  - The `obj_crflic` form now carries `-DWIRE_CHANS_TB=8`. This matches `tb/verilator/milan_dp/Makefile:309`, which this PR changed.
  - A new `obj_tspec8` form exists. `scripts/tspec8_pattern_probe.py` (`receipts/inventory/tspec8_pattern_probe.log`) shows it differs from the crflic form only by the shape: the 8x8 include dir, `obj_tspec8 -GN_STREAMS=8`, a `<runtime>` CFLAGS (the recipe's `$(shell ...)`), and the output name.

**`inventory_walk.py`** used the checksum-pinned shfmt v3.11.0 (sha256 `1904ec6b...`, size 2916536, both matching `ci/image/sources.lock.json`), run on disposable copies of this head and of dev:
- Both walks give the identical 12-step refusal sequence, all on dev drift. It runs from `sw/builder/endstation_builder.py` through `tb/verilator/avtp_rxmon/lockstep_mutants.py`, and stops at the undeclared `tb/verilator/avtp_rxmon/format_mutants.py` (`receipts/inventory/walk-head.log`, `walk-dev.log`).
- No refusal names `crflic_mutants.py`, `Vmilan_dp_tspec8` or `Vmilan_dp_crflic`.
- The author's walks at `a032c6d6`, `0d4b4620` and `2a0085dd` give the same sequence.

**What the walk cannot reach** are the Verilator patterns behind the first undeclared refusal. For those I checked the author's learn comparison at `2a0085dd` (`author-r2/receipts/round2/inventory/milan_dp-learn-compare.txt`, `milan_dp-pattern-residue.txt`). `command-table.json` is unchanged from `2a0085dd` to this head; only `sw/firmware/ctrl/README.md` changes.
- The crflic and tspec8 patterns differ from the Makefile by exactly the three source-list differences that dev's own crflic and dynmap patterns already have: `KL_render_setpoint` to `KL_render_queue`, plus `KL_media_if_latency_pkg`, `KL_media_domain_event` and `KL_mtt_round`.
- Nothing this PR introduces is left unrecorded. See pending manager duties.

### R687-1-R1 (RESIDUE): RESOLVED

`docs/traceability/ieee8021q.md:103` (Q-10) now carries R687-1's exact wording, byte for byte: "MaxFrameSize still derives from real frame geometry in [`milan_datapath`](../../hdl/milan/milan_datapath.sv), one slot per source: each AAF talker's channel count and the CRF output's PDU shape (#774), passed as `cfg_tspec_max_frame_i`." `gen_module_matrix.py --check` passes.

### R687-1-S1 (SUGGESTION; Tests): RETAINED, optional, not taken

The per-AAF-talker slot index is still unobservable at the graded shapes, because every talker in an elaboration has the same width. The round-2 delta does not touch it. The frozen acceptance (the talker-0 control fails on both shapes) is met, as the author's `crflic-mutants` receipt confirms (see the Tests lens).

## New findings in the round-2 delta

There are no BLOCKER, MAJOR, MINOR or RESIDUE findings.

### S2 SUGGESTION - Tests, Robustness - `tb/verilator/milan_dp/Makefile:904` - `make clean` does not remove `obj_tspec8`

- **Evidence:** the `clean` recipe lists `obj_crflic` and every other leg's Mdir, but not `TSPEC8_MDIR` (`obj_tspec8`, `:321`). This PR introduced `obj_tspec8`, in round 1.
- **Impact:** small.
  - The directory is git-ignored (`.gitignore:98`).
  - `run` and `run-tspec8` always build before they execute.
  - But `make clean && make exec-tspec8` runs a stale binary instead of failing the way `exec-crflic` does after `clean`.
- **Optional outcome:** add `obj_tspec8` to `clean`.
- **Verification:** run `make clean` after a `tspec8` build; no `obj_tspec8` remains.

### S3 SUGGESTION - Docs - `docs/traceability/gen_module_matrix.py:239,252` - the generator still accepts a dotted version string as a clause

- **Evidence:** F2 was fixed by rewording the row, which the assignment allowed. `clause_re` still matches the `1.2` in a token such as "v1.2". The next traceability row that cites "Milan v1.2 <clause>" next to a backticked module will therefore put `1.2` back into the matrix. The 7 existing generator controls do not cover this.
- **Optional outcome:** have the generator skip a `v`-prefixed version token, and add a generator control for it.
- **Verification:** `gen_module_matrix.py --check` reports 8/8 controls, and a planted "v1.2" row adds no `1.2`.

### Delta hygiene (no finding)

- The 13 non-table added lines and all table lines contain no em dash, no lane or bench label, no review round, no reviewer ID and no comment ID (`receipts/hygiene/delta-added-line-scan.log`). The only regex hits are `gptp_plane` paths.
- The new `KL_crf_tx.sv:231-233` comment states the behaviour (a size cast widening `crf_data_length`) and its reason, with the issue ID.

## Lens results at this head

**[R687] PASS Conformance**
- **Examined:** `hdl/ieee1722/crf/KL_crf_tx.sv:227,235,241,249`; `docs/traceability/ieee8021q.md:103,154`; `receipts/legs/crflic-head.log:562-575` and `tspec8-head.log:510-553`.
- **Checked against:** issue #774 AC1-AC4, Milan Table 4.4 as cited in-tree (AAF 24*N + 24 + 1; CRF 28 + 1), and IEEE 802.1Q 35.2.2.8.4 a).
- **Result:** the delta changes only the cast form of `CRF_PDU_C`. The leg runs at this head reproduce CRF 29 = emitted AVTPDU + 1 on the 1x1 shape, and 8 x 217 plus 29 on the 8x8 shape.
- **Netlist unchanged:** the Yosys cell counts (`KL_crf_tx` 2,687; `milan_datapath` 1,778,782) and the route figures are identical to round 1 (author receipts at `2a0085dd`).
- **Carried:** code the delta does not touch keeps R687-1's clean Conformance result. That covers the AC1 per-source port and AC2 per-slot derivation in `milan_datapath.sv` and `KL_pp_shadow.sv`.

**[R687] PASS RTL**
- **Examined:** `hdl/ieee1722/crf/KL_crf_tx.sv:221-249` (width, signedness and value of `CRF_PDU_C`, `FRAME_BYTES`, `NUM_BEATS`, `LAST_KEEP` and `tspec_max_frame_o`), and `receipts/gates/lint_rtl_check.log`.
- **Lint:** "LINT GATE: PASS (89 violation(s) <= ratchet 89)", at this head, run by me.
- **Route** (author receipt, `2a0085dd`, design-identical to this head): route-1x1 against the eleventh record is `RESULT: PASS`. SLICE goes 15,835 to 15,831 (-4), WNS is 0.281 ns, WHS 0.009 ns, and routing is complete. The +5-slice STOP is not met.
- **Result:** F1's RTL attribution is closed. No other RTL changed in the delta.

**[R687] PASS Robustness**
- **Examined:**
  - `KL_crf_tx.sv:235` as the only RTL delta;
  - the two planted frame-size faults (`receipts/bdd/scenario48_fault_probe.log`);
  - `ci/image/command-table.json`, the build-form diff (`receipts/inventory/tspec8_pattern_probe.log`);
  - `tb/verilator/milan_dp/Makefile:303-331,562-572,800-807,903-904`.
- **Result:**
  - A value-identical cast change cannot alter shape-dependent or reset behaviour.
  - The frame-size regression again reads the real arithmetic and refuses both a grown data length and a grown PDU.
  - The `run` path builds every ordinary case before it executes. S2 is the only gap, and it is optional.
- **Carried:** the round-1 per-source path keeps R687-1's clean Robustness result (no-CRF shapes, widths, clocking, 10 caught planted faults).

**[R687] PASS Tests**
- **Run by me at this head:**
  - behave 406/406;
  - the frame-bytes probe, 60;
  - the scenario-48 falsification, 2/2 caught;
  - `obj_crflic` 427/0 and `obj_tspec8` 61/0;
  - `test_sim_pool.py` 17/17;
  - the inventory walks, head identical to dev;
  - the tspec8 pattern probe.
- **Author receipts checked:**
  - The `crflic-mutants` verdicts: 10/10. Both unmutated legs pass, and talker 0's TSpec on every slot is caught on the 1x1 and on the 8x8 (`author-r2/receipts/round2/crflic_mutants/crflic-mutants-verdicts.txt`, rc 0).
  - The full sweep at `0d4b4620`: four shards, every exit 0. Summing the shard tallies gives 64/64 suites passed and 2,189,325 checks with 0 in-suite failures (`author-r2/receipts/round2/sweep/shard-*/spec-01.log`).
  - The rtl-fast native replica at `01fc5475`: every job success, `bdd-conformance` included. Its `receipts.json` shows head = head_after = `01fc5475` and no tracked changes.
- **Carry:** `0d4b4620..01fc5475` touches only `command-table.json`, which no workflow, Makefile or `run_all_suites.sh` reads (my grep), and the firmware page. So the sweep at `0d4b4620` carries.
- **Result:** F1 and F3 are closed.

**[R687] PASS Docs**
- **Examined:**
  - `docs/traceability/ieee8021q.md:103,154`;
  - `docs/traceability/MODULE_MATRIX.md:67,98,173`;
  - `hdl/ieee1722/aaf/README-tests.md`, `hdl/ieee1722/crf/README-tests.md`, `hdl/milan/README-tests.md`;
  - `sw/firmware/ctrl/README.md:253`;
  - the CHANGELOG #774 entry and the PR body (round-2 table and carry statement).
- **Gates run by me:** `docs_check.py` reports 0 findings across 210 md files. `gen_module_matrix.py --check` passes with 7/7 controls.
- **Firmware page count:** "167 pin controls" matches the self-test. In the replica's `firmware-boundary` log, `ctrl_boundary` reports "167 pin and 4 figure controls, 0 misbehaved". The figure control refuses 168 ("gives the pin controls as 168, where the self-test has 167"). The two new controls are `make build-tspec8` and `make run-tspec8`, each with the stack poisoned (`author-r2/receipts/round2/rtl-fast/logs/firmware-boundary.9.log:265,276,316,330`).
- **Docs gates** (author receipt at `01fc5475`, GNU Make 4.3): 44 steps, 0 failed. The 2 skips are by rule (local act runner contract, and the no-git step, whose pair is run separately with rc 0).
- **Result:** F2 and R1 are closed. S3 is optional.

## Ledger (reviewer-owned)

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_crf_tx.sv:227-249`; `ieee8021q.md:103,154`; `legs/crflic-head.log` (427/0), `legs/tspec8-head.log` (61/0); author Yosys/route receipts at `2a0085dd`; carried R687-1 per-source path | R687-2 | `01fc54756f1ffb0a3aa836681215e8321ee7e86c` |
| RTL | CLEAN | `KL_crf_tx.sv:221-249`; `gates/lint_rtl_check.log` (89 <= 89); author route-1x1 PASS (-4 slices) at design-identical `2a0085dd` | R687-2 | `01fc54756f1ffb0a3aa836681215e8321ee7e86c` |
| Robustness | CLEAN | `KL_crf_tx.sv:235`; `bdd/scenario48_fault_probe.log`; `inventory/tspec8_pattern_probe.log`; `milan_dp/Makefile:303-331,562-572,800-807,903-904`; carried R687-1 probes | R687-2 | `01fc54756f1ffb0a3aa836681215e8321ee7e86c` |
| Tests | CLEAN | `bdd/behave-head.log` (406/406); `bdd/frame_bytes_probe_head.log`; `inventory/walk-head.log` vs `walk-dev.log`; `gates/test_sim_pool.log`; author `crflic-mutants` 10/10, sweep 64/64, rtl-fast replica; hosted `bdd-conformance` success | R687-2 | `01fc54756f1ffb0a3aa836681215e8321ee7e86c` |
| Docs | CLEAN | `ieee8021q.md:103,154`; `MODULE_MATRIX.md:67,98,173` + 3 README-tests; `docs/matrix_clause_probe.log`; `docs/matrix_version_token_scan.log`; `gates/gen_module_matrix_check.log`; `gates/docs_check.log`; `sw/firmware/ctrl/README.md:253` vs replica `firmware-boundary.9.log`; author docs gates 44/0 | R687-2 | `01fc54756f1ffb0a3aa836681215e8321ee7e86c` |

## Real limits

- **No standards texts.** The Milan, IEEE 802.1Q-2018 and IEEE 1722-2016 texts were not available. Table 4.4's rows and the clause numbers were checked against the issue, the in-tree citations and the processor's SRP documents, as in R687-1.
- **Not re-run here, by rule.** The full sweep, Yosys, the Vivado resource gate, the rtl-fast job bodies, the docs-gate bank and `crflic-mutants` were not re-run. Their results are the author's published receipts.
  - Those receipts are integrity-checked against the packet's `MANIFEST.json`: 822/822 digests match, with none missing or unlisted (`receipts/evidence-manifest-verify.log`). The evidence commit `4484c29c` is unsigned, so integrity rests on those digests, not on a signature.
  - The Yosys `run.log` does not name its head. Its attribution to `2a0085dd` comes from the author's HANDOFF table.
- **Native replica, not act.** The rtl-fast evidence is the author's native replica, not act. Hosted contexts at this head were mostly still queued or running at my snapshot. Only `changes`, `verilator-lint`, `bdd-conformance` and `full-ci-gate` had succeeded, and `Physical gPTP` was skipped.
- **The inventory walk ends at an undeclared script.** The walk stops at dev's undeclared `format_mutants.py` (step 11). Beyond it, the build-form claim rests on the author's learn comparison and my pattern diff.
  - R687-1's published walk showed a different two-step dev sequence (`endstation_builder.py`, then undeclared `avdecc/gen_aemi_image.py`). My walk and the author's agree with each other on 12 steps.
  - The refusal order therefore appears environment-dependent. That does not change the conclusion, because head and dev refuse identically in every walk.
- **Simulation only.** No bench and no hardware were used. Physical calibration was NOT RUN, and field skips (the `tsn_fuzz` tsn-gen campaigns in the sweep) are not hardware proof.
- **No manager source bank.** No manager source bank ran at this head, and none is claimed or inferred.

## Pending manager duties

- Hosted and act acceptance at this exact head. Most hosted contexts were still in flight at my snapshot.
- Current-dev candidate merge validation (builder and native banks) at the merge turn, against live dev `a032c6d6`.
- `tool-inventory.json` regeneration, which dev's pre-existing drift still blocks. That drift is the 12-step walk sequence and the stale `milan_dp` Verilator source lists.
  - When those lists are re-learned, include this PR's `Vmilan_dp_crflic` and `Vmilan_dp_tspec8` forms.
  - They carry the same stale source list as dev's forms (`KL_render_setpoint` and the three missing CRF files).
- The second independent review (R688-2) and the full completion bar.
- Optional items for the author or a follow-up: S1, S2 and S3.

## Receipts

Every published file is listed in `MANIFEST.sha256`:
- **`scripts/`:**
  - R687-1's `bdd_frame_bytes_probe.py`, `inventory_walk.py` and `matrix_clause_probe.py`, unchanged;
  - `verify_evidence_manifest.py`, `tspec8_pattern_probe.py`, `scenario48_fault_probe.sh` and `run_r2_probes.sh`.
- **`receipts/bdd`:** behave at head, the frame-bytes probes, the scenario-48 falsification.
- **`receipts/legs`:** `obj_crflic` and `obj_tspec8` build and run at head, with host paths redacted.
- **`receipts/gates`:** lint, `gen_module_matrix --check`, `docs_check`, `test_sim_pool`.
- **`receipts/docs`:** the matrix clause probe and the version-token scan.
- **`receipts/inventory`:** the head and dev walks, and the tspec8 pattern probe.
- **`receipts/hosted`:** the check-run snapshot at the exact head.
- **`receipts/hygiene`:** the delta added-line scan.
- **`receipts/evidence-manifest-verify.log`:** the author-packet digest check.
- **`receipts/restore/clone-state.txt`:** the clone state after the probes.
  - HEAD and tree are as above, and `write-tree` equals the tree.
  - The worktree and index are clean, with no ignored entries.
  - The index (mode, blob, path) equals the HEAD tree across 1447 entries.
  - The five checked-out gitlinks match HEAD and are clean; `external` is not checked out, as at the start.
  - The PR changes no gitlink.

R687-2 FINISHED
