[R582] POSITIVE - exact head e52d7525ae0c5c9ac669843432187ddcd9071686

# R582-8: composition review of issue #665 / PR #704 (F-INT PR 1) on the merge-train candidate

- Candidate: `e52d7525ae0c5c9ac669843432187ddcd9071686`, tree `0705eb4a691dcfb8211de9c7da79883cc357b249`.
  - First parent `eb86b843557c6d9300847e3b6e12851604580b69`: the #696 candidate over live dev `cfadd767a7ad47aaee68de655e1066cc000fb8a0`, which carries M2 (#710), M6 (#719) and 711 (#718).
  - Second parent `67c1285b3b28b12a3af4f3f3aae6e92befd5febb`: the PR source head. Merge base `554e61d299ef7ddb5aca6fb9ce0e6a6cd076d8cb`.
  - Live refs checked read-only during the round: dev is still `cfadd767`, and `refs/pull/704/head` is still `67c1285b` (`receipts/ls_remote.txt`).
- Scope: composition acceptance only. The source head has two independent POSITIVE source reviews:
  - R583-6 (comment 6101681004);
  - R582-6 (comment 6101700655).
- Verdict: the composed tree introduces no defect beyond the reviewed sources.
  - No BLOCKER, MAJOR, MINOR or RESIDUE is opened by this round.
  - Two SUGGESTIONs are recorded. S2 is a pre-existing dev condition outside this PR.

## 1. What the composition changes

`scripts/composition_identity.sh` produces `receipts/composition_identity.txt`:

- `git merge-tree --write-tree eb86b843 67c1285b` gives `0705eb4a`, the candidate's tree. The merge is the conflict-free automatic merge, and nobody hand-resolved anything.
- Both sides' change lines survive byte for byte. They are hashed over raw `git diff --no-ext-diff --no-textconv --no-renames` output:
  - the PR's lines, from the merge base to the source and from the predecessor to the candidate, are `9157c58e63625dbb` on both sides;
  - the predecessors' lines, from the merge base to the predecessor and from the source to the candidate, are `dd16f923cae7262d` on both sides.
- The PR changes 63 files and the predecessors change 61. Six files are changed by both, and each side's per-file lines are identical too:

| File | Predecessor change | PR change |
|---|---|---|
| `sw/litex/milan_soc.py` | M2: the CSR AXI-Lite crossing's W/R FIFOs in block RAM (`_cross_csr_bus` `:773-799`); the MAC crossings' framing flags in LUTRAM with registered read words (`_payload_in_block_ram` `:1433`, applied at `:1806-1807`) | `CtrlMailbox` only (`:2636-2703`): 11 unread `o_pub_*` ports on `Instance("KL_mbx")`, and the docstring |
| `docs/design/MAILBOX_SPLIT.md` | 711: lwSRP pin line `:299` | the publication block (`:802-`) and the census |
| `sw/firmware/ctrl/README.md` | 711: pin `:353` and `:355` | the `publish` port, pass bounds `:121-173`, arm `srpcmp` |
| `sw/firmware/ctrl/srp/README.md` | 711: pin links `:76-77` and `:378-380` | publication term `:274-283`, and the section at `:316` |
| `sw/firmware/ctrl/maap/README.md` | 696: draw sweep `:201-204` | `DA_GATE` writer `:111-122`, and the bounds `:137-147` |
| `sw/firmware/ctrl/test/ctrl_arms.py` | 711: `LWSRP_REV` `:360-363` | `arm_srpcmp` `:415-449` |

The semantic interactions, and how this round checked each:

- **Mailbox window against M2's crossings.**
  - `KL_mbx_wb` and `KL_mbx` sit on the CPU's Wishbone bus in `sys` (`milan_soc.py:2675-2703`).
  - Neither the window nor its CSR bank passes through `_cross_csr_bus`, which is the datapath's AXI-Lite CSR bus in `milan_cd`. Neither passes through the MAC crossings either.
  - The PR adds output connections only. The bus handshake, depth and read latency of both paths are each side's own, unchanged code.
  - I elaborated `CtrlMailbox` out of the composed file and lint-bound it to the mailbox RTL with pinned Verilator 5.050 (`scripts/probe_ctrl_mailbox.py`; `receipts/logs/probe_ctrl_mailbox_*.log`, `probe_ctrl_mailbox.v`):
    - rc 0, with no PINMISSING and no UNDRIVEN;
    - 0 width findings on the 11 `pub_*` ports;
    - the 4 remaining WIDTHEXPAND warnings are migen's 1-bit constant ties on pre-existing F0 inputs.
  - M2's own test of the composed file, `test_retained_cdc_storage`, passes (see §2).
- **711's lwSRP pin, `9197193e` to `08ee86e8`.**
  - 711 groups one Message per AttributeType in each MRPDU, and the PR's SRP writers, tests and comparator now run on it.
  - The comparator is order- and grouping-tolerant by construction (802.1Q 10.8.1/.2), and its self-test uses literal fixtures.
  - Every SRP arm, plant and the pin arms pass at `08ee86e8` (see §2).
- **Datapath changes from M6, 696 and M0s.**
  - These are `milan_datapath.sv` (GET_COUNTERS column read; `KL_maap` ports `port_operational_i` and `realtime_ns_i`) and `KL_pp_shadow.sv` (comment only).
  - The PR's publication census elaborates this datapath. On the candidate it finds the same population as at the source: 25 class-D nets, 4 unread, and 39 reads of 21 nets in all six shapes.
- **696's `KL_maap.sv` against the PR's MAAP writer.**
  - The PR changes `maap_mbx.c/h` and not `maap/maap.c`.
  - The MAAP differential, which builds `maap.c` against the composed `KL_maap.sv`, passes.
- **Linked firmware size.** Measured, see S1.
- **Default all-fabric build.**
  - Of the default build's inputs, the composition changes only:
    - `milan_soc.py` inside `CtrlMailbox`, which is reached only under `--ctrl-mailbox`;
    - the additive `endstation_builder.datapath_params`, which only the census and the builder tests call.
  - No shipping build script references a firmware file the PR changes.
  - The builder's real SoC elaborations of every config pass (see §2).

## 2. Gates run on the candidate (all rc 0)

Raw logs, redacted to placeholders, are in `receipts/logs/<name>.log`.

Where each gate ran:

- In the review clone at `e52d7525`.
- Or, where marked †, in a disposable `--shared` checkout of the same commit and tree (`scratch/candcopy`). That checkout has every submodule at its gitlink, and lwSRP comes from a fresh public fetch of `08ee86e8`. It is needed because `aecp_arms.py:39` and `ctrl_srp_image.py:100` read `third_party/lwSRP` regardless of `--lwsrp` (S2).

Pinned and identified tools:

- Verilator 5.050, through `$TOOLS/pinned-verilator-5.050/verilator`, `--version` "5.050 2026-07-01 rev v5.050".
- sv2v v0.0.12, fetched and checked against `rtl-fast.yml`'s sha256 `ff8c9eea...5a00`.
- Yosys 0.66.
- The RV32 SDK, the CI bootlin archive installed and verified by `scripts/ci_rv32_sdk.py`.

| Gate | Result |
|---|---|
| `docs_check.py` | 0 findings, 203 md + 1265 scrubbed files, scrub 23/23 |
| `gen_toc.py --check` / `--verify-anchors` (pinned markdown venv) | 143 pages OK / 484 cross-page fragments reproduced |
| `check_em_dash.py --base eb86b843` / `--selftest` | 0 findings over 679 added lines in 9 pages / 339 arms |
| `ci_events.py --check` / `--selftest` | 1821 contract items across 4 workflows and CI_WORKFLOWS.md / 2530 arms |
| `check_doc_paths`, `check_submodule_docs`, `check_doc_style`, `check_solution_docs` | OK (963 paths; 5 exact gitlinks) |
| `check_baremetal_only.py --check`, `check_soc_sources`, `check_port_contracts`, `check_rtl_source_lists`, `check_wire_accountability`, `pp_srcs.py --check` | OK (0 findings / 1263 files; 43 modules; RESULT PASS) |
| `check_sweep_shape.py --self-test`, `check_deploy_shape.py --self-test`, `check_nvm_capture.py` | OK |
| `gen_mailbox.py --check` / `--crosscheck` / `--selftest` | 0 findings / 0 findings / 0 arms failed |
| `publication_census.py --check --selftest --jobs 6` | 6 shapes, 234 checks, 0 failures; 25 nets, 4 unread, 39 reads of 21; self-test 0 of 120 arms failed; 0 of 31 rules unproven |
| `make -C tb/verilator/mbx all` | WB 402, AXI4-Lite 447, co-sim 32, IF2 404/449/389 checks, 0 failures; 6 of 6 quick plants caught |
| `syn/yosys/run.sh --mode elaborate --no-structural`, tops KL_mbx, KL_mbx_wb, KL_mbx_axil, milan_datapath, KL_pp_shadow, KL_gptp_shadow † | 6/6 PASS |
| `lint_rtl.py --check` † | 90 <= ratchet 90 |
| `sw/builder/test_builder.py --require-elaboration --require-rv32` | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, see limits). Gates 23f (8 elaborations, 8/8 cuts), 23l (7/7), 23m (5 real elaborations against `datapath_params`, 3/3 cuts). No write into the bench LiteX tree (checked with an mtime stamp) |
| `scripts/run_litex_sims.sh` (bench LiteX interpreter) † | 6/6 PASS, including M2's `test_retained_cdc_storage` |
| `test_ctrl_firmware.py --require-rv32 --jobs 4` † | 60 of 60 arms; `srpcmp` 5 controls + 18 plants, none missing; `lwsrp` at `08ee86e8`; `rv32` |
| `fw_coverage.py --check` † | PASS, 30 files at 100 % lines and branches |
| SRP plants as `--self-test` runs them (`scripts/srp_campaigns.py`, lwSRP `08ee86e8`) | 271 of 271 caught (198 at two interfaces incl. 28 publication plants, 73 at one); 0 escaped |
| `aecp_mutants.py` † | 76 of 76 caught |
| lwSRP pin-refusal plants (`scripts/lwsrp_pin_arms.py`) † | 2 of 2 refused (edited source; `9197193e` refused as not the pin) |
| `maap_differential.py` | 12 tests, 0 failures |
| `fw_rv32_selftest.py --require-rv32` | 17 checks PASS |
| Size fixture, `ctrl_srp_image.py --with-aecp`, ax7101_8x8, IF=2 † | candidate ram_span 223,776 B; source head 223,184 B (S1) |

`ctrl_mutants.py`'s 506 plants were not re-run. Their arms (model, port, adp, unit, walk, acmp*, entity, maap*, rv32, reentry) link no lwSRP. Their inputs differ between source and candidate only in `ctrl_arms.py:363` (`LWSRP_REV`), which those arms do not read. The source reviews and the hosted `firmware-unit` at `67c1285b` cover them.

## 3. Findings

```text
[R582] SUGGESTION Docs, Conformance - PR #704 body (Status, "With AECP linked ... 223,184 B, under 224 KB by 816 B"); receipts/size_cand_8x8_if2_aecp.json, receipts/size_src_8x8_if2_aecp.json - R582-8-S1: the composed linked image is 592 B larger than the PR body's figure
Requirement/evidence: Ruling 6088423771 item "Report the firmware size against 224 KB"; F5 ruling 6081705916 (224 KB). One runtime was built from the same sources with -fno-stack-protector, and the same fixture linked both sides with it. The source head reproduces the author's figure exactly (ram_span 223,184 B). The candidate gives 223,776 B: .text +588 B, every other section identical. The growth comes from 711's lwSRP 08ee86e8. The limit still holds (224 B under 224,000; 5,600 B under 229,376).
Impact: none on this merge. The PR body is correct for its stated base 554e61d2. After the merge, dev's margin on the 224,000-byte reading is 224 B, not 816 B, and F-INT PR 2 and later lanes budget against it.
Required change: optional. Record the composed figure (223,776 B, margin 224 B) in the merge record or on the issue.
Verification: ctrl_srp_image.py --with-aecp --config configs/endstation_ax7101_8x8.yaml --interfaces 2 at the merged head.

[R582] SUGGESTION Tests, Docs - sw/firmware/ctrl/test/aecp_arms.py:39; sw/firmware/ctrl/test/ctrl_srp_image.py:100; sw/firmware/ctrl/README.md (lwsrp arm row: "the pinned submodule, or --lwsrp DIR") - R582-8-S2: two lwSRP consumers ignore --lwsrp
Requirement/evidence: Pre-existing in dev (a6e69168 for the F3/F4 merge; 00800490 for F5). Neither this PR nor the composition introduces it. With the submodule uninitialised, test_ctrl_firmware.py --lwsrp DIR and fw_coverage.py --lwsrp DIR refuse with "lwSRP is not its own checkout", because these two read ROOT/third_party/lwSRP (a traced run shows git resolving it to the superproject root: receipts/logs/fw_arms_attempt2.log). CI initialises the submodule and never sees it.
Impact: a documented invocation fails with a misleading message. No gate verdict is affected.
Required change: optional, outside #665 F-INT PR 1. A separate issue can thread the --lwsrp path through, or document that the submodule is required.
Verification: test_ctrl_firmware.py --lwsrp <pinned clone> with third_party/lwSRP uninitialised.
```

## 4. Lens results at the candidate

```text
[R582] PASS Conformance - receipts/composition_identity.txt; sw/firmware/ctrl/test/ctrl_arms.py:360-363 vs srp_wire_compare.py (grouping-tolerant self-test); receipts/logs/srp_campaigns.log (271/271 at lwSRP 08ee86e8); receipts/logs/fw_arms.log (60/60, lwsrp, srpcmp); receipts/logs/maap_differential.log (composed KL_maap.sv vs maap.c); receipts/size_*_8x8_if2_aecp.json (under 224 KB) - composed SRP/MAAP behaviour and budget against rulings 6088423771 and 6081705916; S1 optional
[R582] PASS RTL - sw/litex/milan_soc.py:773-799,1433-1490,1806-1807 (M2) vs :2636-2703 (mailbox window, sys domain, outputs only); receipts/logs/probe_ctrl_mailbox_lint.log; receipts/logs/census_check_selftest.log (composed milan_datapath.sv, 6 shapes); receipts/logs/yosys_elab_mbx_tops.log; receipts/logs/lint_rtl.log; receipts/logs/mbx_make_all.log - no interaction between the mailbox hookup and M2's crossings; the census population is unchanged on the M6/696 datapath
[R582] PASS Robustness - receipts/logs/test_retained_cdc_storage.log (M2 reset in flight, depth, lockstep on the composed file); receipts/logs/srp_campaigns.log (retry, refusal, reset and destroy plants at the new lwSRP); receipts/logs/mbx_make_all.log (reset, strobe, holes, out-of-window); receipts/logs/lwsrp_pin_arms.log - composed failure and refusal paths
[R582] PASS Tests - ctrl_arms.py (both sides) run as receipts/logs/fw_arms.log; fw_coverage_check.log (30 files at 100 %); srp_campaigns.log; aecp_mutants.log (76/76); lwsrp_pin_arms.log; census self-test 0/120 and 0/31; test_builder.log gate 23m 5 elaborations and 3/3 cuts; ci_events selftest - each changed suite runs green on the composed tree, and its plants still fail; S2 optional
[R582] PASS Docs - the five shared pages (table in §1) read against both sides: pin lines, MAAP sweep against the DA_GATE text, arm counts, pass bounds; receipts/logs/docs_check.log, gen_toc_check.log, gen_toc_anchors.log, em_dash_parent.log, doc_paths.log, ci_events_check.log - coherent; no stale figure in a tracked page (no page states a linked-image byte figure)
```

## 5. Earlier public findings on this PR, at this head

These were read after this round's verdict and ledger were recorded (`receipts/verdict_ledger_before_prior_findings.md`).

| Finding | State at `e52d7525` | Why |
|---|---|---|
| R582-1-F1..F3, R583-1-F1..F3, R582-2-F1 = R583-2-F1, R583-2-S2, R582-3-F1..F3, R583-3-F1, R583-3-S1, R582-4-F1, R583-4-F1/F2, R582-4-S1, R582-5-F1/F2, R583-5-F1..F3, R582-5-S1 | Resolved | Both source reviews resolve them at `67c1285b`. The composition changes none of their artifacts except `milan_soc.py` outside `CtrlMailbox`, and pin lines in three firmware pages. Census, bench, srpcmp and firmware plants re-pass here |
| R582-2-R1, R583-5-R1 | Applied (as recorded by R582-6 and R583-6) | Files not changed by the predecessors |
| R582-6-R1, R583-6-R1 (RESIDUE, PR body) | Retained | PR body unchanged; carried by the manager |
| R583-6-R2 (RESIDUE, `tb/verilator/mbx/Makefile` comment) | Retained | File not changed by the predecessors |
| R583-6-S1 (gate 23m's configuration list) | Retained, optional | `test_builder.py` not changed by the predecessors; 23m passes here |
| R583-6-S2 = R582-6-S2 (PR 2 must source `KL_maap`'s address and gate term) | Retained, optional | 696 adds `KL_maap` inputs only; the datapath reads no new `KL_maap` output |
| R582-6-S1 (census and `milan_csr` read-back) | Retained, optional | Census logic unchanged |
| R582-6-S3 (publication ports' crossing for PR 2) | Retained, optional | M2 keeps `KL_mbx` in `sys` and the datapath in `milan_cd`; the substance is unchanged, and only the line numbers move (`milan_soc.py:2682`, `:838`) |
| R582-7 (POSITIVE at `8c8f82f6`, no new items) | Superseded | Earlier candidate; this round re-covers the composition at `e52d7525` |

## 6. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 optional) | Composition: merge identity, SRP at lwSRP `08ee86e8` (arms, 271 plants, srpcmp, pin arms), MAAP differential with 696's `KL_maap`, composed size. PR-only parts (writers, contract, census rules): source reviews | R582-8; source part R583-6 (6101681004), R582-6 (6101700655) | `e52d7525ae0c5c9ac669843432187ddcd9071686`; source part `67c1285b3b28b12a3af4f3f3aae6e92befd5febb` |
| RTL | CLEAN | `milan_soc.py` M2 and the mailbox hookup (probe lint-bind), census over the composed datapath in 6 shapes, Yosys elaboration of 6 tops, lint ratchet, mbx bench. Mailbox RTL internals (unchanged by predecessors): source reviews | R582-8; source part R583-6, R582-6 | as above |
| Robustness | CLEAN | M2 crossing test on the composed file, SRP failure-path plants at the new pin, mbx bench reset/strobe/range paths. PR-only writer and driver refusals: source reviews | R582-8; source part R583-6, R582-6 | as above |
| Tests | CLEAN (S2 optional) | `ctrl_arms.py` run (60/60), coverage ratchet, SRP 271, AECP 76, pin arms 2, census self-test, builder 23m, ci_events self-test, mbx quick plants. `ctrl_mutants` 506 and the 175 RTL plants (inputs unchanged): source reviews and hosted `firmware-unit` at `67c1285b` | R582-8; source part R583-6, R582-6 | as above |
| Docs | CLEAN | The five shared pages read against both sides; docs, TOC, anchor, em-dash, path and CI-contract gates. PR-authored page content: source reviews (their RESIDUE retained, §5) | R582-8; source part R583-6, R582-6 | as above |

`67c1285b` is the candidate's second parent. Everything the source rounds covered and the predecessors did not touch is byte-identical at `e52d7525` (§1).

## 7. Real limits

- **Hardware.**
  - Physical calibration was NOT RUN, and no hardware was used.
  - Desk and field skips are not hardware proof.
- **Hosted runs.**
  - There is no hosted run at `e52d7525`: the commit is not on GitHub.
  - At `67c1285b` all 24 hosted contexts completed, and all succeeded except `Physical gPTP (nightly and manual)`, which was skipped (`receipts/hosted_checks_source_head_67c1285b.tsv`).
  - Hosted and act acceptance belong to the manager.
- **Builder gate 11** did not run: it needs the bench's mf48 build report. Vivado is absent, so `xvlog_gate` did not run either.
- **Default-image byte identity against dev** was not re-exported. The argument is static (§1) plus the builder's real elaborations. The full-export comparison belongs to the manager's candidate bank.
- **Mutation tables not re-run:** `ctrl_mutants` (506) and the full mbx RTL table (175). Their inputs are unchanged (§2).
- **Size figures.** The runtime was built from the bench LiteX tree's Picolibc, compiler-rt and LiteX sources, with `-fno-stack-protector` patched into the disposable copy only.
  - Both installed RV32 compilers instrument stack protection by default, and this compiler-rt's `umoddi3` then needs `__stack_chk_guard`.
  - The absolute figures depend on the runtime. The source head reproduces the published 223,184 B, so the 592 B delta is like for like.
- **Local toolchain.** These differ from CI's:
  - Yosys 0.66 is a distribution build, not CI's source build;
  - host gcc 16.2.1 and GoogleTest 1.18;
  - Python 3.14;
  - the markdown venv carries pycparser 3.1 against the lock's 3.0 (`gen_toc.py` accepted it).
- **Two transient refusals.** Two firmware runs refused before I traced the cause to S2. Their logs are kept as `fw_arms_attempt1/2.log` and `fw_coverage_check_attempt1/2.log` (and `_nosubmodule`). The passing runs are the † runs.
- **Manager's candidate bank.** The bank under `$TMPROOT/665int-candidate-0923` (head `e52d7525`) only had logs through its step 33 when I looked. This round neither claims nor relies on it.

## 8. Pending manager duties

- Complete and link the candidate builder and native banks, including the default-export comparison, and hosted/act acceptance at the merged head.
- Carry R582-6-R1, R583-6-R1 and R583-6-R2 to the residue checklist.
- Decide the optional items: S1/S2/S3 of R582-6, S1/S2 of R583-6, and S1/S2 of this round. S1 is the composed size figure. S2 is a candidate for a separate issue.
- Run post-merge containment (`check_merge_containment.py`) once the branch stops moving.

## 9. Restoration

- After all probes, the review clone is at `e52d7525`, tree `0705eb4a`. Only ignored build outputs were removed; nothing was untracked or ignored at the start.
- The `git ls-files -s` digest is unchanged: `6da207b8...6c7` before and after (`receipts/index_*.sha256`).
- All 1,289 tracked regular entries re-hash to their index blobs with their recorded modes (`receipts/blob_mode_verify.txt`).
- Gitlinks and `git submodule status` are unchanged (`receipts/submodule_status_*.txt`), and the initialised submodules are clean.

R582-8 FINISHED
