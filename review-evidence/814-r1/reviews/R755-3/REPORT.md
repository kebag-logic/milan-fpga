[R755] POSITIVE - exact head 7f4d7eeaa1773099f72edb3830bd9f8ab2b5c22c

Round R755-3, issue #814 / PR #826. This is a composition-acceptance review of the merge-train candidate `7f4d7eeaa1773099f72edb3830bd9f8ab2b5c22c` (tree `c5ae659753edc70b7c52d1035964d9833f8e6e06`). Its parents are live dev `02ca829ad821f4233ab66f59978c65d3c3c9de70` and PR head `4ee2aa9654196a00876dedade4b2e987c9c06e64`.

**Verdict.** The composed tree introduces no defect beyond the reviewed sources. No BLOCKER, MAJOR or MINOR is open. There are no new findings. The two source reviews' open SUGGESTIONs and RESIDUEs are retained unchanged, because their bytes are identical at this head.

## 1. Composition

- **The merge itself.** `git merge-tree --write-tree 02ca829ad 4ee2aa965` gives tree `c5ae6597…`, which is the candidate's own tree. So the candidate is git's clean merge, with no hand resolution. The merge base is `1e80128f`, the PR's source base. Receipt: `receipts/composition.log`.
- **Predecessors since the PR's base, in live dev:**
  - PR #816 (#70): the volatile set and its firmware;
  - PR #821 (#817): the servo reset synchroniser cut;
  - PR #813 (FPGA-gPTP #94, the #806 adoption).
- **Files changed by both this PR and a predecessor:** three.

| File | Predecessor change | PR change | Interaction |
|---|---|---|---|
| `sw/litex/milan_soc.py` | #821: the `add_servo_reset_constraints` import (`:67-68`), `_CRG.milan_pll_clk` (`:279-281`), the servo constraint call in `MilanSoC.__init__` (`:3253-3256`) | `ResetInserter` import; `AXIReadyStage`, `RegisteredRefresher`, `add_staged_sdram`, `SPIPHYStage`, `stage_spi_phy`, `MilanSoC.add_spi_flash`; the `add_staged_sdram` call (`:3174`) | Disjoint hunks. Of 43 top-level units and `MilanSoC` methods, only `_CRG`, `MilanSoC` and `MilanSoC.__init__` differ from the PR head, and only by #821's hunks. Every entry point the new test calls is byte-identical to the PR head. Every name imported from `clock_constraints` exists at the candidate. The servo Tcl finds its two flops by `NAME =~ "*mmcm_servo/psrst_sync_r_reg*"` (`sw/litex/clock_constraints.tcl:29-33`), which no #814 cell matches. Receipt: `receipts/entrypoint_identity.log` (rc 0). |
| `docs/litex/CLOCK_DOMAINS.md` | #821: the servo row (`:237`) and the constraint bullets (`:384-386`) | The `AXIReadyStage` bullets (`:277-282`) | Separate sections, and no count or table is shared. "Only the servo's reset synchronizer input is cut" is about constraints, and #814 adds no constraint. |
| `docs/testing/TESTING.md` | #816: the dynmap mutant row (66 controls, `[VOLATILE]`) | The `test_soc_timing_cuts.py` paragraph (`:722-755`) | Separate sections. The LiteX inventory has 8 members at the candidate. `docs/testing/CI_WORKFLOWS.md:2681` ("all seven simulations") is a dated 2026-10-14 measurement record, not a current count. |

- **Shared registries and pins checked for coupling:**
  - `ci/image/exec-audit.json`: only the PR changed it (its stand-in digest). `scripts/run_litex_sims.sh --selftest` passes at the candidate.
  - `ci/image/command-table.json`: only predecessors changed it, and only firmware and test entries. See limit 6.
  - `scripts/port_docs.budget`: changed by a predecessor. `check_port_contracts.py` passes at the candidate.
  - `tb/verilator/nvm_capture_cpu/measurements.json`: re-measured by #816 at the #70 firmware. `check_nvm_capture.py` passes at the candidate. See limit 3.
  - `docs/design/AREA_BUDGET.md`: changed by #813. This PR does not touch it. See limit 2.
  - Workflow definitions: identical at the PR head and the candidate, and equal to the manifest's `definitions` hashes.
  - LiteX pins, patches and `third_party`: unchanged by the predecessors.
  - Submodule gitlinks: the candidate's six equal dev's (`receipts/gitlinks-head.txt`).

## 2. Gates run on the candidate

`scripts/composition_gates.sh <clone> <out> 02ca829ad821f4233ab66f59978c65d3c3c9de70` ran 26 gates, with the pinned Markdown renderer from `tools/markdown/requirements.txt` in a private environment. All 26 returned rc 0. Logs and rc files are in `receipts/gates/`.

- **Docs gates:** `docs_check.py` (0 findings, 210 md files), `check_feature_status.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_gptp_docs.py`, `check_solution_docs.py`, `check_submodule_docs.py`, `check_archive.py`.
- **Em-dash gate:** `check_em_dash.py --base 02ca829a` gave 0 findings over 41 added lines in 2 pages, with 339/339 arms.
- **TOC gates:** `gen_toc.py --verify-anchors` reproduced 542 cross-page links, and `gen_toc.py --check` passed.
- **Record and source gates:** `check_nvm_capture.py`, `check_nvm_record_space.py`, `check_soc_sources.py`, `check_rtl_source_lists.py`, `check_port_contracts.py`.
- **Measures and idiom checks:** `measure_naming.py --check`, `measure_fail_fast.py --check`, `measure_test_evidence.py --check`, `check_hygiene.py --check`, `check_todo_ownership.py`, `check_py_idiom.py`, `check_sh_idiom.py`.
- **CI gates:** `ci_events.py --check`, `ci_gate_workflows.py --check`, `scripts/run_litex_sims.sh --selftest`.

## 3. Signed local CI packet

Packet: `review-evidence/814-r1/local-ci/4ee2aa96` at `471be138`. Copies and the verification log are in `receipts/local-ci/`.

1. **Signing key.** `allowed_signers` holds one key, principal `milan-local-ci`, namespace `milan-local-ci`. Its fingerprint is `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`, the required key.
2. **Signature.** `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` printed "Good signature", rc 0. `manifest.json` has sha256 `2586312b262868369a10851b496d48306090a6c53c25b722086a2610a747f65d`, as stated.
3. **Subject and coverage.**
   - The subject is PR 826, candidate `7f4d7eea…`, candidate parent `02ca829a…`, candidate tree `c5ae6597…`, head `4ee2aa96…` and head tree `ec3c136a…`. All of these match this clone.
   - The result is `success`. act exited 0 and both banks exited 0 (`manager-builder` with 48 commands, `full-native` with 5).
   - All 47 coverage entries are `ok: true`. The only one not run by act is `rtl/physical-gptp`, with a named reason: it runs on schedule and dispatch only, and it is not hardware evidence.

**Hosted contexts at the PR head:** 67 success and 1 skipped (`Physical gPTP (nightly and manual)`). `verilator-suites`, `yosys-portability`, `rtl-fast`, `elaborate` and the docs checks executed. Hosted acceptance is the manager's.

## 4. Prior public findings, judged at this head

Both source reviews at `4ee2aa96` (issuecomment-6537580432 and issuecomment-6537646057) recorded every round-1 MINOR as RESOLVED. These are R755-1 F-1/F-2 and R756-1 F-1/F-2. The resolving code (`RegisteredRefresher`, both stall-arm stages) and the test are byte-identical at the candidate (`receipts/entrypoint_identity.log`). So they stay RESOLVED.

The open optional items are retained unchanged. The candidate does not touch any of them.

| ID (source round) | Severity | Lenses | Location at this head | Status at this head |
|---|---|---|---|---|
| S-2 (R755-2) | SUGGESTION | Tests | `sw/litex/test_soc_timing_cuts.py:736`, `docs/testing/TESTING.md:751-752` | Retained. D7 plants aw and ar together; an ar-only plant is optional. |
| S-3 (R755-2) | SUGGESTION | Tests, Conformance | `sw/litex/test_soc_timing_cuts.py:251-277` | Retained. There is no structural check that a stage's VALID never waits on its READY. |
| S-4 (R755-2) = S-A (R756-2) | SUGGESTION | Tests, Robustness | `sw/litex/test_soc_timing_cuts.py:944-979`, `scripts/run_litex_sims.sh:110` (`TMO` 900 s) | Retained. The member's wall time is about 590 s CPU, and over 900 s wall on a loaded host. The test, the LiteX pins and the aggregate limit are unchanged by the composition. |
| S-B (R756-2) | SUGGESTION | Tests, Robustness | `sw/litex/test_soc_timing_cuts.py:530-549`, `:712-736` | Retained. Each stall arm runs one seed. |
| S-C (R756-2) | SUGGESTION | Conformance | LiteDRAM `modules.py` `MT41J256M16`, `ns_to_cycles` at pin `f9b75e03` | Retained. The tREFI round-up predates the PR. |
| R-1 (R755-2, R756-2) | RESIDUE | Docs | `docs/testing/TESTING.md:746` | Retained. Exact fix: re-wrap `at reset, which issues no ZQCS there, must fail that arm. Then each stage's output is stalled` so that `Then each stage's output is stalled` starts the next line, matching the paragraph's wrap. |
| R-2 (R756-2) | RESIDUE | Docs | `sw/litex/milan_soc.py:2451` (`:2447` at the PR head) | Retained. Exact fix: drop "again" from "so an idle controller would never issue ZQCS again". |

## 5. New findings

None at any severity.

The comment-rule scan found no new instance in the reviewed delta. I scanned the added lines of `git diff 02ca829ad..7f4d7eeaa -- sw scripts ci docs` for lane labels, review rounds, reviewer IDs and comment IDs. `F0`-`F4` in `test_soc_timing_cuts.py` are check IDs in the test's own output, not lane labels. Issue references and `dev 1e80128f` are permitted.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | **Composition touches it:** the predecessors change the integrated image (#813 gPTP RTL, #821 constraints, #816 firmware). Examined: issue #814 acceptance; rulings issuecomment-6522621984, -6525285974 (record rule: each adoption is judged on its own route set; the record is re-recorded once after the last release merge) and -6527475726; `AREA_BUDGET.md:140-146` at the candidate; capture `SUMMARY.md` at `fdae2980` against `measurements.json` `maxima` at the candidate; `check_nvm_capture.py` rc 0; entry-point identity. Open optional items: S-3 and S-C, retained. | R755-3 (composition); the source by R755-2 and R756-2 | 7f4d7eeaa1773099f72edb3830bd9f8ab2b5c22c (source: 4ee2aa9654196a00876dedade4b2e987c9c06e64) |
| RTL | CLEAN | **Composition touches it:** `milan_soc.py` `MilanSoC.__init__` and `_CRG`. Examined: `milan_soc.py:67-68, 279-281, 2332-2530, 3161-3256, 3696-3716`; `clock_constraints.py:44-48`; `clock_constraints.tcl:27-33`; `receipts/entrypoint_identity.log` (stages and hooks identical to the source head); `git merge-tree` equality | R755-3 (composition); the stages by R755-2 and R756-2 | 7f4d7eeaa1773099f72edb3830bd9f8ab2b5c22c |
| Robustness | CLEAN | **Composition does not touch it.** The stage code, the test, the LiteX pins and the aggregate limit are identical to the source head (`receipts/entrypoint_identity.log`, `git diff --quiet 4ee2aa96 7f4d7eea -- sw/litex/test_soc_timing_cuts.py scripts/run_litex_sims.sh`). So it is covered by R755-2 and R756-2. Open optional items: S-4/S-A and S-B, retained. | R755-2, R756-2 (source); identity confirmed R755-3 | 4ee2aa9654196a00876dedade4b2e987c9c06e64, unchanged in scope at 7f4d7eeaa1773099f72edb3830bd9f8ab2b5c22c |
| Tests | CLEAN | **Composition touches the inventory and audit registries.** Examined: `run_litex_sims.sh` INVENTORY (8 members) and `--selftest` rc 0 at the candidate; `exec-audit.json` and `command-table.json` disjoint; the signed manifest (act at the head, banks at the candidate, 47/47 ok); hosted 67 success / 1 named skip. Open optional items: S-2, S-4 and S-B, retained. | R755-3 (composition); the test by R755-2 and R756-2 | 7f4d7eeaa1773099f72edb3830bd9f8ab2b5c22c |
| Docs | CLEAN | **Composition touches it:** `CLOCK_DOMAINS.md` and `TESTING.md` are both shared. Examined: the composed regions in §1; 26 gates rc 0 (`receipts/gates/`), including `docs_check`, `check_em_dash --base 02ca829a`, `gen_toc --verify-anchors` and `--check`, and `check_port_contracts`; the comment-rule scan of the delta. R-1 and R-2 are RESIDUE only. | R755-3 (composition); the source by R755-2 and R756-2 | 7f4d7eeaa1773099f72edb3830bd9f8ab2b5c22c |

## 7. Real limits

1. **No source bank at this exact head.** The execution evidence is the manager's signed packet (banks on this candidate, act on the PR head) and the authors' published receipts. I re-ran no suite sweep, builder bank, LiteX aggregate member or Yosys bank. The pinned LiteX environment was not installed here, so `test_soc_timing_cuts.py` was not executed on the candidate. Instead, its entry points were shown byte-identical to the source head. The manifest's bank commands are recorded only as argv digests, so I cannot name which candidate-bank commands ran the LiteX aggregate.
2. **The composed shipping image has not been routed in any evidence I examined.**
   - The PR's route set was taken at `0d4a899f` on base `1e80128f`. The candidate also carries #813 (the #806 route placed 15,823 slices, 27 free, `AREA_BUDGET.md:143`), #821 and #816.
   - The PR adds about +320 FF and +31 slices against the record.
   - Under the record rule (issuecomment-6525285974), this is not a finding against this PR. The manager's release-integration routes own the composed slice fit and WNS.
   - The issue body's "Then #806 and #787 each merge dev and re-route" is superseded by the rulings: #806's PR #813 merged first, under #818.
3. **The capture has not been measured at #70 firmware plus the flash stage.**
   - The source measured the stage at `8b28ebaf`: worst 13.85922 ms at 8x8/50 MHz, against 13.86328 ms committed then.
   - #816 re-measured without the stage at the #70 firmware: 13.86052 ms.
   - The stage's measured effect is within 0.005 ms, against a 10.6 ms margin to 24.5 ms. So the composed margin is not expected to move materially, but it is unmeasured.
4. **Physical calibration NOT RUN.** The flash stage has not been on hardware. The `Physical gPTP` skip is not hardware evidence.
5. **The record still holds the +0.440 ns route.** Re-recording is a post-release dev duty under the record rule.
6. **Observation, not a finding.** The `ci/image/command-table.json` reviewed-digest entries do not match the candidate:
   - `scripts/run_litex_sims.sh` is pinned at `91299632…`, while the file is `73d8119f…` at the PR head and the candidate;
   - `sw/litex/milan_soc.py` is pinned at `105961e5…`, which matches neither dev, the merge base nor the candidate.
   - The table is read by the CI image build (`ci/image/build.py`), not by a PR gate.
   - The `milan_soc.py` mismatch already exists on dev, and no predecessor touched either entry. So this is not a composition effect.

## 8. Pending manager duties

- Build and validate the final current-dev merge candidate at the merge turn, if dev moves past `02ca829a`, and link its receipts on the PR.
- Own hosted and act acceptance, and the release-integration routes (composed slice fit and WNS), and the post-release re-record.
- Carry R-1 and R-2 to the residue checklist.
- Merge only with explicit maintainer authorization.

## 9. Clone integrity

No probe edited a tracked file. After the gates, `git diff-index --quiet HEAD` was clean and `git status --porcelain` was empty. The Python caches the gates generated were removed. HEAD is `7f4d7eeaa1773099f72edb3830bd9f8ab2b5c22c`, and the index gitlinks equal the head's six (`receipts/gitlinks-worktree.txt` = `receipts/gitlinks-head.txt`).

R755-3 FINISHED
