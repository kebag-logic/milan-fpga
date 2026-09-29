[R368] POSITIVE - exact head 4c2a30debb031595b81c5c4bfc53b601a0fec528

# R368-5 internal independent review: issue #590 / PR #609, merge-dev and fixture delta

Exact head `4c2a30debb031595b81c5c4bfc53b601a0fec528`, tree `0a9754d44e40de8c734468be2cedad5ac675d794`.

**Delta reviewed:** `1f039cfe86d5337f5c9b7248696dba1c4bdda67e` (R368-4 POSITIVE) to the exact head. It has three commits:
- merge `9f94b246` (dev `b5c0f69d`, after #395, #595 and #602);
- `d0203aac`, the restart model;
- `4c2a30de`, the cosim-host marker stub.

**Governing public scope:**
- assignment 590#5879349035;
- disposition 590#5879883680, option (a);
- the issue #590 body and its frozen acceptance;
- review start 609#5881271745.

## Verdict summary

This round has no BLOCKER, MAJOR or MINOR finding. All five lenses are covered clean at the exact head.

- **SUGGESTION S1** retains R368-4-S1: provenance lines name the measured head.
- **Observation O1** is the stale `nvm_cosim` count in `tb/verilator/README.md:71`. It was stale on dev before this PR, and this round measured that at dev `b5c0f69d`. It is out of scope here and is not a finding against this PR.

The five verification items:

1. **The merge is correct.**
   - The only conflict is `docs/findings/README.md`. Its resolution keeps every row of both sides, in dev's order, with no duplicate.
   - The four clean merges carry both sides' edits exactly and contradict nothing.
   - The processor gitlink equals dev's `c951a9ff`.
2. **`d0203aac` models `nvm_started` correctly.**
   - `nvm_started` is a zero-initialised file-scope writer static. Only `nvm_boot()` sets it, after the shape check.
   - The restart model now names it. W1 re-arms it through `nvm_boot()`, and W2-W4 stay retired.
3. **`4c2a30de` adds only the stub.**
   - The stub is byte-identical to `nvm_host.c:67-72` and hides no defect.
   - The product link still requires the real patch-0006 symbol.
4. **Own full `nvm_cosim` run: 465/465 checks and 39/39 mutants, rc 0.** The native service and capture evidence is byte-identical to the previous merge head at every graded field. Every moved bound hash is a dev input and equals this head's bytes.
5. **No statement is made stale by the combination.** The Markdown, idiom and source gates pass in the pinned environment.

## Reconstruction

Read in order:

1. `AGENTS.md` and `CONTRIBUTING.md` sections 3, 5 and 6/6.1.
2. `docs/README.md`.
3. The issue #590 body, acceptance 1-4 and the manager decision.
4. The assignment and disposition comments above.
5. The authorities the delta touches:
   - `docs/integration/BAREMETAL_FIRMWARE.md`;
   - `docs/reference/MILAN_COMPLIANCE_MATRIX.md` and `REGISTER_MAP.md`;
   - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` (restart-model text);
   - `docs/findings/397_SERVICE_BUDGET.md`;
   - `sw/litex/patches/0006-bios-dispatch-hook.patch`;
   - `sw/firmware/milan_baremetal/milan_baremetal.c`.
6. `git diff b5c0f69d..4c2a30de` and `git diff 1f039cfe..4c2a30de`, with history.
7. Public evidence on branch `590-review-evidence` at `fd12ca1661d9fa30fbc9d9c796ebb0dc48f6b508`: packets `author-mergedev` (previous merge head) and `author-mergedev2` (this head).

This round's verdict and ledger were drafted before prior public review findings were read. The other reviewer's in-flight round was not read.

## Verification items

### 1. Merge (Conformance, Docs, RTL)

**Reconstruction of the merge** (`scripts/p1_merge_checks.sh`, `receipts/p1_merge_checks.txt`):
- The merge's parents are `1f039cfe` and `b5c0f69d`, and the merge-base is `7a7582f0`.
- `git merge-tree --write-tree` gives automatic tree `5d051cc3`, with one conflicting path, `docs/findings/README.md`.
- The recorded merge differs from the automatic tree in that path only.
- The two fixture commits touch only `tb/verilator/nvm_cosim/{run_cases.py,cosim_host.c}`.

**Findings index** (`docs/findings/README.md:11-19`):
- **Row order at head:** `75_RECONNECT_RESTART_MEASUREMENT`, `COMMERCIAL_TIMING_395`, `397_SERVICE_BUDGET`, `117_GPTP_SILICON_EVIDENCE`, then the five historical/fixed rows. This is dev's order, with dev's new #395 row at dev's position.
- **Nothing is lost or invented:**
  - Every lane row is present byte for byte.
  - No merged row is absent from both sides.
  - No link target is duplicated.
- **Dev's 397 row was correctly superseded.** It is the only dev row not present byte for byte. It equals the merge-base row byte for byte, so only this lane edited it, and the lane's text is the correct resolution.

**Both sides' edits carried** (`scripts/p12_lane_equivalence.sh`, `receipts/p12_lane_equivalence.txt`). For `BAREMETAL_FIRMWARE.md`, `MILAN_COMPLIANCE_MATRIX.md`, `REGISTER_MAP.md`, `test_builder.py` and `findings/README.md`, two comparisons were made:
- the ordered `+/-` line sequence of lane->merge against dev's base->dev edit;
- dev->merge against the lane's base->lane edit.

All ten comparisons are EQUAL. As a negative control, substituting the lane head for the merge makes all ten DIFFERENT (`receipts/p12_control_merge_is_prev.txt`).

**No contradiction across lanes:**
- **`BAREMETAL_FIRMWARE.md`.**
  - #602 changes only the gate-1b census rows at `:1482` (`media_rebase_p_w` has two references) and `:1484` (`mcr_restart_p_w` excludes the PHC-step term).
  - This PR's statements cover the service budget (`:72-77`), the dispatch hook and walk yields (`:1902-1928`), the capture copy (`:1954-1958`) and PHY publication (`:1960-1979`).
  - None of them mentions `mr`, PHC re-base or the restart pulse, and none depends on those nets.
- **`MILAN_COMPLIANCE_MATRIX.md`.**
  - Dev's rows are 5.4.2.15/.16 (`:120`), 5.3.11.1 (`:169`) and 4.4.4.3 (`:206`), on the PHC-only re-base.
  - The lane's row is 7.4.42.2 (`:192`), on the PHY link-status publication.
  - Each row states only its own lane's behaviour.
- **`REGISTER_MAP.md`.**
  - Dev's `mr` paragraph is at `:125-131`, and the lane's PHY paragraph at `:413-418`.
  - They cover different registers and different causes.
  - The lane's anchor into the firmware contract resolves; the `gen_toc --verify-anchors` gate passes.
- **`test_builder.py`: no gate collision.**
  - Dev's hunks cover the gate-1b `media_rebase` census, schema-12 quoted-hex YAML and new gate 36b.
  - The lane's hunks cover the digraph selection count (`:13304`), two patch-count comments (`:23297`, `:23382`) and the gate-35 marker stubs (`:26647`, `:26668`).
  - The hunks are disjoint, and the count comment matches `sw/litex/patches/` (four `.patch` files).
  - The full builder bank at this head is public evidence (`author-mergedev2/builder-gates.json`: present and absent, rc 0, head `4c2a30de`). This round did not run it, because that is out of this round's allowance.

**Gitlinks** (P1): all four gitlinks equal dev's at both the merge and the head.
- `protocol-processor` `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`;
- `gptp-processor` `5dce647a`;
- `third_party/verilog-axis` `48ff7a7e`;
- `external` `efeb541a`.

**Delta attribution** (`scripts/p10_delta_attribution.sh`, `receipts/p10_delta_attribution.txt`):
- Of the paths differing from `1f039cfe`, 46 are byte-equal to dev's copy. The other seven are the five merged files and the two fixture files.
- Of the paths differing from dev, 23 are byte-equal to the R368-4 head.
- No `hdl/`, `syn/`, submodule, `sw/firmware` or `sw/litex` byte differs from both parents.

**Commit form:** both fixture commits have one-line subjects, no body and no trailer, and each is a single-file change (`receipts/p3_stub_mirror.txt`).

### 2. `d0203aac` restart model (Robustness, Tests, Conformance)

**Firmware facts:**
- `milan_baremetal.c:419`: `static int nvm_started;` is a file-scope static in `.bss`, so a CPU-only reset returns it to 0.
- `:926-927`: `nvm_heartbeat_tick()` returns early unless it is set.
- `:1449` is its only assignment. It sits in `nvm_boot()` after the patch-0006 marker call (`:1444`) and the shape check (`:1445-1448`).

**Restart model:**
- `run_cases.py:181` adds `"nvm_started": "0"` to `WRITER_STATICS`.
- `host_restart()` (`:186-210`) refuses unless the writer's `nvm_*` scalar statics equal that set. It then zeroes them, clears the idle hook and calls `nvm_boot()`.
- The PHY statics (`:787-790`) sit under `#ifdef CSR_MILAN_MAC_PHY_MDIO_W_ADDR`. The cosim stubs do not define that, so they are not compiled into this model.

**This round's run** (`receipts/p5_nvm_cosim_full.log`, `receipts/p5_restart_cases.txt`):
- **W1 (1x1) re-attaches and stays live.**
  - It restarts at 2,830 ms and reports "re-attached, the window is not reloaded".
  - It commits seq 2 to slot B with capture 2 acknowledged.
  - At 5,830 ms it still reads `backed=1`, 3 s after the restart, which is past the 2,000 ms liveness deadline.
  - The only heartbeat path is gated on `nvm_started`, which the model zeroed. So `nvm_boot()` re-armed it.
- **W2, W3 and W4 (1x1 and 8x8) stay retired.** Each prints "no window load was accepted in this boot; the writer stays retired until the next reset" and holds `backed=0` to the end, as their cases require. W4 also holds `backed=0` through `end2`.

**Fault probes** (`scripts/p6_probes.sh`, `receipts/p6/`), run in a scratch clone of the exact head at 1x1, each file restored after its probe:

| Probe | Planted defect | Result |
|---|---|---|
| A | Force `nvm_started = 0` after `nvm_boot()` in the restart | W1 `converged@end` FAILS (314 ok, 1 bad). W1 therefore depends on the re-arm. |
| B | Drop `nvm_started` from `WRITER_STATICS` | Refused with "writer statics [...] != restart model [...]". This is the r4-bank failure. |
| C | Remove the cosim-host stub | Host link fails with "undefined reference to `bios_dispatch_hook_required'" at `milan_baremetal.host.c:1443`. This is the defect the statics refusal had hidden. |

### 3. `4c2a30de` marker stub (Conformance, Robustness, Tests)

**The stub mirrors the probe's copy exactly:**
- `cosim_host.c:65-70` is byte-identical to `sw/firmware/nvm_hosttest/nvm_host.c:67-72`: a declaration, a comment and an empty definition (`receipts/p3_stub_mirror.txt`).
- The commit adds six lines and nothing else.
- `cosim_host.c` is compiled only by `tb/verilator/nvm_cosim/run_cases.py:267`, and `scripts/check_cpp_idiom.py:166` names it as a scanned C root.

**The product link still requires the real symbol:**
- `milan_baremetal.c:356` only declares `bios_dispatch_hook_required`. The firmware tree has no definition and no `weak` attribute.
- The strong definition exists only in `sw/litex/patches/0006-bios-dispatch-hook.patch`, and `apply.sh:36` applies that patch.
- **Guards on the missing marker:**
  - The host guard `test_disabled_writer.py:51-60` strips the marker and requires a link failure naming it.
  - The published product cross-link (`author-mergedev2/logs/product-link-missing-marker.log`) fails with `undefined reference to 'bios_dispatch_hook_required'` from `milan_init`, with `collect2` rc 1.
  - Probe C shows the cosim host is under the same guard.
- **Conclusion:** the stub gives the cosim host what the patched BIOS gives the product, and removes no guard.

### 4. Suite and native evidence (Tests, Conformance)

**Own full `nvm_cosim` run:**
- Setup: `make run` with JOBS=8 and POOL=8. It ran in a disposable clone of the exact head, with the three submodules cloned at their gitlinks, Verilator 5.050 (see limits) and the pinned Markdown interpreter.
- `[contract-1x1] 62 case run(s): 315 ok, 0 bad`.
- `[contract-8x8] 27 case run(s): 150 ok, 0 bad`.
- The 2-bit identity aliases on A8 as required.
- `39 of 39 mutant(s) killed by their named check`, including F08 by `converged@end`, F11 by `restart_stays_retired_without_load@restarted` and R06.
- Totals: `nvm_cosim: 465 checks: 465 PASS, 0 FAIL`, `RESULT: PASS`, rc 0.

**Native packets compared** (`scripts/p4_compare_native.py`, `receipts/p4_compare_native.txt`): `author-mergedev` (head `1f039cfe`) against `author-mergedev2` (head `4c2a30de`).
- **79 artifacts are byte-identical.** They cover:
  - every service `.log` and `-raw.log` (16 runs, including `no-publish`, `late-sample` and both `remove-dispatch` controls);
  - every regrade and final-regrade log;
  - every capture `-raw.log`, `.log` and measurement `.json` (six arms and three controls).
- **65 differ, only in build bindings.**
  - The build logs differ by timestamps and work paths.
  - The capture `-sources.json` files differ in exactly `includes[0..1]` and `sources[117]`, which are the work-directory paths.
  - The service receipts and specs differ only under `build_hashes` and `input_hashes`.

**Bound inputs** (`scripts/p4b_bound_inputs.py`, `receipts/p4b_bound_inputs.txt`):
- The moved source keys are the same on every receipt:
  - `hdl/ieee1722/avtp/KL_media_clock_restart.sv` and `hdl/milan/milan_datapath.sv` (#602);
  - the five processor files the re-pin changes (`KL_acmp_talker.sv`, `KL_srp_{encoder,listener_fsm,talker_fsm,top}.sv`);
  - `sw/litex/milan_soc.py`.
- Each new hash equals both this head's bytes and dev's. Each old hash equals the `1f039cfe`/`16be6768` bytes.
- The generated keys that moved are `sim.v`, `Vsim`, `bios.elf` and `csr.h`/`git.h`/`mem.h`/`soc.h`. `bios.bin` is identical.

**Receipts against this head** (`scripts/p4c_receipt_sources.py`, `receipts/p4c_receipt_sources.txt`): every tracked-source hash in all 15 service receipts was checked against this head's bytes, with submodules read at their gitlinks. That is 2,340 hashes, with 0 mismatches. The three `external/` sources cannot be read in this clone, but they did not move between the packets.

**Capture sources:** the capture compiles the five re-pinned processor files (`receipts/p8_capture_sources_vs_pin.txt`). Its measurements are still byte-identical, so the committed capture receipt holds at `c951a9ff`. `scripts/check_nvm_capture.py` returns rc 0 at the head (P9).

### 5. Stale statements and Markdown gates (Docs)

**Searches** over the merged tree for:
- the restart model: `WRITER_STATICS`, "file-scope variable of the writer", `nvm_host_writer_restart`;
- the marker: `bios_dispatch_hook_required`, "link marker", `cosim_host.c`;
- the old pin and measured head: `16be6768`, `26a26e1f`.

**What the searches found:**
- `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:745-747` and `:1736-1739` say the restart "returns every file-scope variable of the writer to its initial value". `d0203aac` makes that true again, where before it the build was refused.
- `397_SERVICE_BUDGET.md:192`, `BAREMETAL_FIRMWARE.md:1903-1904` and `sw/litex/patches/README.md:18` describe the marker. They agree with probe C and with the product cross-link.
- The `16be6768`/`26a26e1f` mentions are dated provenance, or dev's own history (CHANGELOG, `SUBMODULES.md`, `SAVED_STATE_MATERIALIZATION.md`, `rom_digests.tsv`). They are unchanged by this delta. See S1.
- No statement in the merged tree is falsified by the combination.

**Gates** (`scripts/p9_gates.sh`, `receipts/p9/`). All ran with the pinned Markdown interpreter at the exact head, and all returned rc 0:
- `check_em_dash --base b5c0f69d`: 0 findings over 555 added lines in 11 pages, arms 339/339;
- `check_em_dash --selftest`;
- `docs_check`: 0 findings over 174 md and 932 scrubbed files;
- `check_feature_status`;
- `check_doc_style`;
- `gen_toc --check`, and `--verify-anchors` (235 links);
- `check_solution_docs` and `check_submodule_docs`;
- `check_baremetal_only --check`;
- `check_archive`;
- `check_nvm_capture`;
- `git diff --check b5c0f69d HEAD`;
- `check_cpp_idiom`, `check_py_idiom`, `check_hygiene --check` and `measure_test_evidence --check`.

The last four refused in the scratch clone because its submodules are not registered, which is an environment refusal and not a finding. All four passed in the review clone, which was then proved exact (P13).

## Findings

None at BLOCKER, MAJOR or MINOR.

### R368-5-S1 - SUGGESTION - Docs - measured-head provenance lines (retains R368-4-S1)

- **Location:** `docs/findings/397_SERVICE_BUDGET.md:37-43` and `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1613-1616`.
- **Evidence:**
  - Both pages name measured head `26a26e1f` and processor pin `16be6768`. `397_SERVICE_BUDGET.md:41` says later analysis, documentation and receipt commits do not change the compiled inputs.
  - The merges are not of those kinds, but they did change compiled inputs: #602 RTL, five re-pinned processor files and `milan_soc.py`.
  - The figures remain exact. This round's P4 comparison shows every simulation log and measurement byte-identical at `c951a9ff`, and `check_nvm_capture` passes.
  - The lines are true dated provenance, which is the form `docs/findings/README.md` asks findings to keep ("the exact candidate ... raw artifact identity").
- **Classification of the executor's open point 1:** not stale and not a defect.
- **Impact:** a reader of the tree alone cannot see that the figures were reproduced on the merged inputs. The public evidence shows it.
- **Optional outcome:** when these pages are next touched, for example at the candidate re-measure, name the reproducing head.
- **Verification:** reread both lines, and run the docs gate.

### Observation O1 - not attributable to this PR - `tb/verilator/README.md:71` stale `nvm_cosim` count

- **Location:** the inventory row says "469 checks over 90 case runs". The suite grades 465 checks over 89 case runs (62 + 27) at this head.
- **This PR did not cause it.** This round ran the same suite at dev `b5c0f69d`, with the same submodule pins, and got 465/465 over 89 runs and 39/39 mutants, rc 0 (`receipts/p7_nvm_cosim_dev_b5c0f69d.log`).
- This PR changes no case-, check- or mutant-defining file: only one line of `WRITER_STATICS` and the host stub.
- The row was last written by `cc251d68`, and `26482899` (dev, 2026-09-20) changed the case set. `docs/README.md:90` also advises against copied test counts.
- **Classification of the executor's open point 2:** a pre-existing dev documentation defect, outside the frozen scope of #590/#592/#599 (AGENTS.md section 4). It belongs in a new public Issue and does not block this PR.

## Prior public findings: disposition at this head

**Basis for carrying earlier resolutions** (P10, P12):
- Of this lane's changed paths, 23 are byte-identical to the R368-4 head `1f039cfe`.
- The five merged files carry the lane's edits exactly.
- The two fixture commits touch only the `nvm_cosim` harness.

Every resolution confirmed at `1f039cfe` therefore holds on identical bytes.

| Finding | Severity | Status at `4c2a30de` | Evidence |
|---|---|---|---|
| R368-1 F1 = R369-1 F1 (MDIO sample phase) | BLOCKER | RESOLVED, unchanged | `milan_baremetal.c` byte-identical to `1f039cfe` (P10). The `late-sample` control log is byte-identical and still caught (P4). |
| R368-1 F2 = R369-1 F2 (dispatch for every line) | MAJOR / MINOR | RESOLVED, unchanged | patch 0006 and firmware identical (P10). `remove-dispatch` logs byte-identical (P4). |
| R368-1 F3 (record-edge guard test) | MINOR | RESOLVED, unchanged | `nvm_hosttest` byte-identical (P10) |
| R368-2 N1 (disabled-writer heartbeat) | MINOR | RESOLVED, unchanged | `milan_baremetal.c:926-927,1445-1449` identical. The cosim restart now also models the flag (item 2). |
| R368-2 N2 = R369-2 F4 (design page receipt) | MINOR | RESOLVED, unchanged | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` identical. Receipt holds (`check_nvm_capture` rc 0). |
| R369-2 F5 (built-in lapse threshold) | MINOR | RESOLVED, retained through the merge | `BAREMETAL_FIRMWARE.md:1918-1919` lane text carried (P12) |
| R369-2 F6 (native evidence retained) | MINOR | RESOLVED, renewed at this head | item 4 |
| R368-4-S1 | SUGGESTION | RETAINED as R368-5-S1 (optional) | above |
| R368-4-S2 (evidence summary enumeration) | SUGGESTION | TAKEN: the new REVIEW READY names derived binaries and states `bios.bin` identical | `author-mergedev2/REVIEW-READY.md` |
| Earlier SUGGESTIONs (R368-1 to R368-3, R369-1 to R369-3) | SUGGESTION | Unchanged from R368-4's table; optional | identical bytes |

## Lens coverage (clean results with artifacts)

- [R368] PASS Conformance - `docs/findings/README.md:11-19`; `tb/verilator/nvm_cosim/run_cases.py:181`; `tb/verilator/nvm_cosim/cosim_host.c:65-70`; gitlinks; `receipts/p1_merge_checks.txt`, `p3_stub_mirror.txt`, `p5_*`, `p12_*`.
  - Every assignment item is met. Item 1 is the merge and conflict, 2 the one-line restart-model commit with the full suite, 3 no stale statement, 4 the baseline `b5c0f69d`, and 5 the pinned Markdown environment.
  - Disposition (a) is met: the exact `nvm_host.c:67-72` stub in one separate one-line commit.
  - Issue #590 acceptance 1-4 is unchanged in bytes from the POSITIVE head, and its evidence is reproduced byte for byte.
- [R368] PASS RTL - `receipts/p10_delta_attribution.txt` (no `hdl/`, `syn/` or submodule byte beyond dev); `receipts/p1_merge_checks.txt` (all gitlinks equal dev's, `protocol-processor` `c951a9ff`); `receipts/p4b_bound_inputs.txt`.
  - The merge adds no RTL of its own.
  - #602's `KL_media_clock_restart.sv`/`milan_datapath.sv` and the five re-pinned processor files enter unmodified.
  - The lane's service and capture harnesses elaborate them with byte-identical simulation results.
  - This PR's own RTL content is none.
- [R368] PASS Robustness - `sw/firmware/milan_baremetal/milan_baremetal.c:419,926-927,1444-1449`; `run_cases.py:186-210`; `receipts/p5_restart_cases.txt`; `receipts/p6/`.
  - The re-attaching restart (W1) and the three retired restarts (W2-W4) at both shapes behave as the contract requires.
  - A missing re-arm, a statics omission and a missing host marker are each caught.
- [R368] PASS Tests - `receipts/p5_nvm_cosim_full.log` (465/465, 39/39); `p6/` (three probes); `p7_nvm_cosim_dev_b5c0f69d.log`; `p9/summary.txt`; `p4*`.
  - The fixture commits restore the suite and weaken no check. Probes B and C reproduce the two earlier failures, the statics refusal and the host link.
  - Probes A-C show the restart, statics and link checks each fail on their defect.
  - Each checker of this round is shown to discriminate: the P12 control, and the P13 exactness check.
- [R368] PASS Docs - `docs/findings/README.md:11-19`; `docs/integration/BAREMETAL_FIRMWARE.md:72-77,1482-1484,1902-1979`; `docs/reference/MILAN_COMPLIANCE_MATRIX.md:120,169,192,206`; `docs/reference/REGISTER_MAP.md:125-131,413-418`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:745-747,1736-1739`; `receipts/p9/`.
  - Both lanes' authority text is intact and non-contradictory.
  - The restart-model text is true at this head.
  - S1 is optional, and O1 is out of scope.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 5879349035 items 1-5; disposition 5879883680; findings index; restart model; stub; gitlinks; P1, P3, P5, P12 | R368-5 | `4c2a30debb031595b81c5c4bfc53b601a0fec528` |
| RTL | CLEAN | delta attribution P10; gitlinks P1; bound RTL/processor inputs P4b/P4c; capture sources vs re-pin P8 | R368-5 | `4c2a30debb031595b81c5c4bfc53b601a0fec528` |
| Robustness | CLEAN | `milan_baremetal.c:419,926-927,1444-1449`; `run_cases.py:181-210`; W1-W4 at both shapes P5; probes A-C P6 | R368-5 | `4c2a30debb031595b81c5c4bfc53b601a0fec528` |
| Tests | CLEAN | own full `nvm_cosim` 465/465 + 39/39; dev-base run P7; probes P6; native packet comparison P4; gates P9 | R368-5 | `4c2a30debb031595b81c5c4bfc53b601a0fec528` |
| Docs | CLEAN (S1 optional; O1 out of scope) | merged pages and lines above; stale-statement search; em-dash, docs, TOC/anchors, style, feature, solution, submodule, archive, whitespace gates | R368-5 | `4c2a30debb031595b81c5c4bfc53b601a0fec528` |

**Coverage of the lane's own content:** it stays banked by R368-4 at `1f039cfe` for every path byte-identical here. The five merged files carry the lane's edits exactly (P12). The two changed harness files are covered by this round.

## Real limits

- **The assigned pinned Verilator path was absent.** `.../372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host.
  - This round used its own wrapper under scratch, pointing at the same containerised Verilator 5.050 binary that the issue-590 manager rounds' pinned wrapper names. Its `--version` reads `Verilator 5.050 2026-07-01 rev v5.050`, and `verilator_bin` has sha256 `44898b22af4178b45214a0820a04eeac8632ae721ff005e69ef1cf69121bbfdd`. The wrapper lives under scratch.
  - The system default (5.052) was not used.
- **No native service or capture re-run of this round's own.** No LiteX environment or RV32 SDK was used. Native conclusions rest on the two published packets, compared file by file and bound to this head's bytes.
- **The builder bank was not run**, because it is outside this round's allowance. The public evidence records rc 0 at this head.
- **Scratch-clone environment.** The `nvm_cosim` suite, the probes and the dev-base run ran in a disposable clone. There, the submodules are standalone clones at their pins, not registered submodules.
- **The review clone stayed exact.** The four code-quality gates ran in the review clone. A generated `scripts/__pycache__/` was removed afterwards. P13 then proved the clone exact: 956 tracked files by blob, mode and index; no index flags; three initialised gitlinks at their pins and clean. `external` is uninitialised, as at session start.
- **Review-clone refs changed.** The public evidence branch was fetched into the review clone. That changes refs and objects only.
- **Physical calibration NOT RUN. No hardware.** Skipped hosted contexts, such as `Physical gPTP (nightly and manual)`, are not hardware proof.
- **Hosted checks were only snapshotted.** At the time of `receipts/p11_hosted_checks_snapshot.txt`, four hosted jobs were still in progress. Hosted and act acceptance belong to the manager.

## Pending manager duties

- The final current-dev candidate: source base `b5c0f69d`, live dev `eaa88a32` (PR #615 edits `test_builder.py`). Then the composition review, act, the exact-head hosted `verilator-suites`/`yosys-portability` verdicts and the merge authorization.
- Open a new public Issue for O1 (`tb/verilator/README.md:71` `nvm_cosim` count) if the manager agrees.
- Optionally apply S1 at the next touch of the two provenance pages.

R368-5 FINISHED
