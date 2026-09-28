[R368] POSITIVE - exact head 1f039cfe86d5337f5c9b7248696dba1c4bdda67e

# R368-4 internal independent review: issue #590 / PR #609, merge-dev delta

Exact head `1f039cfe86d5337f5c9b7248696dba1c4bdda67e`, tree `9ce926b910ca80772667bb5722eb6ded5e93d223`.
Delta reviewed: `93262f2512054166ae753eda24d76c99f2ea6714` (the head carrying the review bar, R368-3 and R369-3 POSITIVE) to the exact head.
That delta is merge `9e3df3edc025f73278894ff021a2011e46e2575e` (dev `7a7582f03ce5ba7863a90ac342c21be18d90db0b` into `93262f25`) plus the stale-statement commit `1f039cfe`.
Governing public scope: the merge-dev assignment (issue #590 comment 5869849644), the executor STOP (5870577289), the manager disposition, option (a) (5870597087), and the executor REVIEW READY (5872924337).

## Verdict summary

No BLOCKER, MAJOR or MINOR finding. All five lenses are covered clean at the exact head. Two SUGGESTIONs are recorded; they do not affect coverage.

All four assigned verification items hold:

1. **The conflict keeps both lanes' text unchanged.** The only conflict is `docs/integration/BAREMETAL_FIRMWARE.md`. Its resolution keeps both lanes' text unchanged, and the recorded merge differs from the automatic merge in that file only. The clean merges of `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` and `test_builder.py` introduce no contradiction and no gate collision.
2. **`1f039cfe` rewords only statements this PR falsifies.** Both of its rewordings are accurate against the firmware.
3. **The renewed native evidence holds.**
   - All 138 merge-dev artifacts verify against their bound hashes.
   - All 16 service simulation logs and all 9 capture simulation logs are byte-identical to round 3's.
   - All 15 service receipts keep every graded field. Every repo-relative bound hash equals the exact head's bytes.
   - The head's own grader, applied to the published logs, returns the expected verdict on all 15 runs plus the no-publish control.
   - #597's new parameters equal the `protocol_processor_top` defaults (1, 1, 1) on both AX7101 shapes.
4. **The capture re-measure equals the committed receipt.** All six merge-head arms (96 captures) equal the committed receipt rows. `check_nvm_capture.py` returns rc 0 at the head.

## Reconstruction

Read in order:

- `AGENTS.md`, `CONTRIBUTING.md` sections 2-3 and 6.1, and `docs/README.md`;
- the issue #590 body and every public assignment, STOP, disposition and REVIEW READY comment;
- the PR #609 body;
- the authorities the delta touches: `BAREMETAL_FIRMWARE.md`, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` sections 11, 12, 18 and 20, `397_SERVICE_BUDGET.md`, `BOARD_PORTING_AX7101.md`, `REGISTER_MAP.md` MAC_STATUS, `milan_soc.py` and `REQUIREMENTS.md`;
- `git diff 93262f25..1f039cfe`, including the dev side of the merge, and both new commits;
- the public evidence branch `590-review-evidence` at `086597defb8944c16c3aadd6444fe6c5efbb42d4`: the `author-mergedev` packet with `raw/`, and the `author-r3` packet as the round-3 comparison base;
- my own R368-3 packet, read-only.

Prior review findings were read only after this round's independent pass.

## Verification items

### 1. Merge resolution (Conformance, Docs)

- **The recorded merge adds no unexplained change.** `git merge-tree --write-tree 93262f25 7a7582f0` names one conflicting path, `docs/integration/BAREMETAL_FIRMWARE.md`. The recorded merge tree differs from that automatic result in this path only. See `receipts/merge-equivalence.txt`.
- **Both lanes' text survives unchanged, checked mechanically.** `merge_lane_equivalence.py` compares ordered removed/added line sequences. The edit P1->M must equal dev's edit B->P2, and the edit P2->M must equal this lane's edit B->P1.
  - The result is EQUAL for `BAREMETAL_FIRMWARE.md` (8/8 and 5/5 edit blocks), `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` (9/9 and 12/12) and `test_builder.py` (4/4 and 5/5).
  - Planted probes each turn the result DIFFERENT: dropping a D3 DR2c line, reverting DR2a to the provisional wording, and dropping a lane PHY line. The exact merge tree stays EQUAL (`receipts/probe-merge-checker.txt`).
- **Content of the two conflict regions at the head.**
  - Region 1, `BAREMETAL_FIRMWARE.md:1902-1928`: this PR's runtime/dispatch-hook paragraph, with dev's DR2a substitution at `:1926`.
  - Region 2, `:1940-1979`: #610's D3 retry paragraph (`:1940-1952`) followed by this PR's capture paragraph (`:1954-1958`) and PHY paragraph (`:1960-1979`).
  - Nothing contradicts across lanes. The PR's firmware implements no retry bound, and `:1940` states the D3 policy "still requires implementation".
- **`SAVED_STATE_SNAPSHOT_OWNERSHIP.md` has no contradiction.**
  - Dev's D3 text lives at `:1093-1107` (retry policy), sections 11/12, and section 20 items 1, 6 (debounce sentence), 7 and 10.
  - This PR's receipt figures live at `:1609-1650` and `:1790-1806`.
  - The two touch no common fact. Section 20 item 8 (`:1820`) remains true at the head: the TAG-mismatch writer still heartbeats, and the SHAPE path never admits the writer (`milan_baremetal.c:926-927`, `:1445-1449`).
- **`test_builder.py` has no gate collision.** Dev drops the 80 MHz ROM mutation and adds the `test_clock_contract` entry points. This lane changes the digraph selection count, two comments and the gate-35 BIOS marker stubs. The hunks are disjoint. `test_clock_contract.py` returns rc 0 at the head (`receipts/gates/gate-clock-contract.*`).
- **Commit form is correct.** The merge and `1f039cfe` are one-line subjects with empty bodies and no trailers.

### 2. Stale-statement commit (Docs, Conformance)

- `BOARD_PORTING_AX7101.md:104-111` now says the firmware reads Clause-22 link, speed and duplex and writes the CSR, and writes no PHY register.
  - The firmware issues only read frames (`milan_baremetal.c:810-827`, op code `6<<10`). It publishes through `milan_mac_link_status_write` (`:878-912`).
  - Physical acceptance stays on #599. The statement is accurate.
- The `docs/findings/README.md:12` row now names the #590/#592/#599 repairs and the one-hart decision. This matches the `397_SERVICE_BUDGET.md` header.
- **Independent search** (`receipts/stale-statement-search.txt`) covered #590/#592/#599 references, MAC_STATUS/PHY-writer wording, and idle-hook/queued-input/byte-copy wording. It found no other statement this PR falsifies:
  - `394_387_E1_SWITCH_CYCLES.md:187,282` describe the measured image `9e9954e9` ("this build").
  - `SAVED_STATE_FASTCONNECT.md:61,1341` are dated landing descriptions that stay true.
  - `milan_soc.py:1774-1810` says software "CAN" publish.

### 3. Native evidence at the merge head (Tests, Conformance)

- **Packet integrity** (`verify_native_packets.py`, `receipts/native-packets.*`).
  - All 138 merge-dev and 135 round-3 artifacts verify.
  - 50 of each are path-redacted by the publisher. Each of those is accepted only through a `MANIFEST.json` entry binding the original hash to the exact published bytes.
- **Byte comparison with round 3.** 65 paired artifacts are identical. They include every service `-raw.log` and service `.log` (16 runs), every capture `-raw.log`/`.json`/`.log` (6 arms), and the 15 regrade logs.
  - The three capture controls were renamed. Their measurement bytes are identical too: byte-only `-raw.log` equals r3 `-capture.log`, and byte-only `.json` equals r3 `-measurement.json`. The same holds for no-traffic and skip-copy.
  - The differing items are build logs, source-list JSONs, service specs and receipts, and the three control wrapper logs, whose layout changed.
- **Receipts** (`compare_receipts.py`, `receipts/receipt-compare.*`).
  - All 15 service receipts have zero unequal fields outside `build_hashes`/`input_hashes`.
  - `input_hashes` differs only in `sw/litex/milan_soc.py`.
  - `build_hashes` differs in exactly the same set on every receipt:
    - the three merged inputs (`KL_pp_shadow.sv`, `milan_datapath.sv`, `milan_soc.py`);
    - both generated `adp_shape_defaults.svh`;
    - `gateware/sim.v`;
    - `csr.h`, `git.h`, `mem.h` and `soc.h`;
    - the derived `native/Vsim` and `bios/bios.elf`.
  - `bios.bin` is not among them.
  - Every repo-relative key, including submodule sources read at the pinned commits, hashes to the exact head's bytes (0 failures). It also hashes to `26a26e1f`'s bytes for the round-3 receipt.
- **#597 elaborates to the same design.** `protocol_processor_top` defaults at pin `16be6768` are `N_AUDIO_UNIT_P = N_CLK_DOMAIN_P = N_CONTROL_P = 1` (`hdl/top/protocol_processor_top.sv:81-83`). Both AX7101 generated headers state `AEM_N_AUDIO_UNIT_C = AEM_N_CLKDOM_C = AEM_N_CONTROL_C = 1` (`configs/generated/endstation_ax7101_{1x1_tdm8,8x8}/gen/adp_shape_defaults.svh:36-38`). All four gitlinks are unchanged by the merge.
- **Regrade with the head's grader** (`regrade_offline.py`, `receipts/offline-regrade.*`). The head's `run.grade`, `run.service_findings` and `run.report_verdict` were applied to each published raw log. Each log's hash matches `log_sha256`, and every graded field equals the receipt.
  - The 12 positive plans give rc 0 with zero findings. Largest heartbeat gap 322.47884 ms, largest MDIO transaction 0.12457 ms, largest complete poll 0.83375 ms.
  - `remove-dispatch` is caught on both plans: 1051 per-line findings with backing lost on `queued-builtins`, and 350 on `queued-short`.
  - `late-sample` is caught by "PHY initial gigabit negotiation was not published".
  - `no-publish` is caught by its named simulation failure.
  - A planted `unbacked_cycles=7` in a self-consistent copy is refused (`receipts/probe-regrade.txt`).

### 4. Capture re-measure against the committed receipt (Tests, Conformance, Docs)

- **The six arms equal the receipt.** `check_capture_rows.py` (`receipts/capture-rows.*`) finds each arm equal to the receipt measurement field for field, over every field the arm records. The receipt adds identity fields on top.
  - 96 captures pass, with zero mismatches and zero open copies.
  - Each arm compiles 118 sources, including both changed RTL files.
  - The receipt maxima are consistent: 3.88779, 13.23352 and 9.95464 ms.
  - The 8x8 contract margin is 11.26648 ms to 24.5 ms, and the gain over 24.30246 ms is 11.06894 ms. These match `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1629-1633` and the PR body.
  - A planted one-cycle row change is refused.
- **The byte-only control keeps the slower copy cost.** It measures 24.30310 to 24.30446 ms, `minimum_slowdown` 1.83648.
- **The receipt gate passes.** `scripts/check_nvm_capture.py` returns rc 0 at the head, with all four controls detected.

## Findings

None at BLOCKER, MAJOR or MINOR.

### R368-4-S1 - SUGGESTION - Docs - measured-commit provenance lines predate the merge

- **Location:** `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1613-1614` and `docs/findings/397_SERVICE_BUDGET.md:37-43`.
- **Evidence:** Both pages name `26a26e1f` (tree `1ced48e2`) as the measured source. `397_SERVICE_BUDGET.md:41` adds that later analysis, documentation and receipt commits do not change the compiled inputs. The merge is none of those three kinds, but it did change three compiled inputs.
  - The measurements themselves remain exact: the merge-head re-runs are byte-identical, and the pages defer to the evidence packet for the final head.
  - The executor raised this, and the disposition (5870597087, item 3) chose no further change.
- **Impact:** A cold reader of the tree alone cannot see that the figures were reproduced on the merged inputs.
- **Optional outcome:** When these pages are next touched, for example at the candidate re-measure below, name the reproducing head.
- **Verification:** A docs gate and a reread of both lines.

### R368-4-S2 - SUGGESTION - Docs (evidence text only) - the REVIEW READY enumeration of differing bound hashes is incomplete

- **Location:** issue #590 comment 5872924337, "Byte comparison" bullet.
- **Evidence:** The comment lists the three merged inputs, the LiteX timestamp lines and `AEM_N_CONTROL_C`. The receipts also differ in the derived `build/native/Vsim` and `build/software/bios/bios.elf`, and `git.h` is among the headers (`receipts/receipt-compare.txt`).
  - The packet's own `round3-comparison.json` lists every one of these.
  - `bios.bin` and all simulation logs are identical, so no graded result is affected.
- **Optional outcome:** Future evidence summaries name derived binaries as derived.
- **Verification:** None needed. No repository artifact changes.

## Prior public findings: disposition at this head

Twenty-three of this lane's 26 changed paths are byte-identical at `93262f25` and `1f039cfe`. Only `BAREMETAL_FIRMWARE.md`, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` and `test_builder.py` differ, and item 1 proves this lane's edits to them unchanged (`receipts/lane-paths-touched-by-delta.txt`). So every resolution confirmed by R368-3 and R369-3 at `93262f25` carries to this head on identical bytes.

| Finding | Severity | Status at `1f039cfe` | Evidence |
|---|---|---|---|
| R368-1 F1 = R369-1 F1 (MDIO sample phase) | BLOCKER | RESOLVED, unchanged | `milan_baremetal.c:795-807` identical; target `late-sample` still caught (item 3); host PHY mutants caught (`receipts/gates/gate-host-selftest.log`) |
| R368-1 F2 = R369-1 F2 (dispatch for every line) | MAJOR / MINOR | RESOLVED, unchanged | `milan_baremetal.c:941-946`, patch 0006 identical; `remove-dispatch` 1051 and 350 per-line findings (item 3) |
| R368-1 F3 (record-edge guard test) | MINOR | RESOLVED, unchanged | host self-test `edge_cross` caught (`gate-host-selftest.log`) |
| R368-2 N1 (disabled-writer heartbeat) | MINOR | RESOLVED, unchanged | `milan_baremetal.c:926-927,1445-1449`; disabled-writer grade `hb=0 backed=0` on all five shapes and its mutant caught (`gate-host-selftest.log`) |
| R368-2 N2 = R369-2 F4 (design page receipt) | MINOR | RESOLVED, retained through the merge | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1609-1650,1790-1806` equal the lane's text and the receipt (item 4) |
| R369-2 F5 (built-in lapse threshold) | MINOR | RESOLVED, retained through the merge | `BAREMETAL_FIRMWARE.md:1918-1919`, inside the conflict region, unchanged |
| R369-2 F6 (native evidence retained) | MINOR | RESOLVED and renewed at this head | item 3 |
| R368-1 S1/S2, R368-2 T1-T4, R369-2 S5-S9 | SUGGESTION | TAKEN earlier; unchanged | identical bytes |
| R368-3 S1-S3, R369-3 S11/S12, R369-1 S1/S3/S4 | SUGGESTION | RETAINED, not taken; optional | unchanged files |

## Lens coverage (clean results with artifacts)

- [R368] PASS Conformance - `BAREMETAL_FIRMWARE.md:1902-1979`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1093-1107,1609-1650,1790-1830`; `BOARD_PORTING_AX7101.md:104-111`; `milan_baremetal.c:795-946,1443-1449` - The merge-dev assignment rules 1-5 and disposition items 1-3 are met. Issue #590 acceptance 1-4 is unchanged in bytes from the POSITIVE head. The capture STOP bar (8x8 13.23352 ms against 24.5 ms) and the 500 ms heartbeat bound (322.47884 ms) still hold at the merge head.
- [R368] PASS RTL - `hdl/milan/KL_pp_shadow.sv:239,1059-1062`; `hdl/milan/milan_datapath.sv:7427-7429`; `protocol-processor@16be6768:hdl/top/protocol_processor_top.sv:81-83`; the AX7101 `adp_shape_defaults.svh:36-38`; gitlinks.
  - The merge adds no RTL of its own: the automatic merge equals the recorded tree outside the one Markdown page.
  - #597's three parameters equal the processor defaults on both shipped AX7101 shapes, so the lane's harnesses elaborate an equivalent design. Byte-identical simulation logs corroborate this.
  - All pins are unchanged. This PR changes no RTL.
- [R368] PASS Robustness - `receipts/offline-regrade.txt`; `receipts/gates/gate-host-selftest.log`; `milan_baremetal.c:926-933,1445-1449`.
  - Queued built-ins and short queues keep backing with dispatch removed as the only failing case.
  - Device-wait (3 s erase, 5 ms WIP) passes.
  - The disabled-writer shape and identity states stay silent.
  - The PHY loss/recovery cycle reaches both fabric counters once.
  - The long-built-in residual text is retained (`BAREMETAL_FIRMWARE.md:1914-1919`).
- [R368] PASS Tests - `receipts/native-packets.txt`, `receipt-compare.txt`, `offline-regrade.txt`, `capture-rows.txt`, `check_nvm_capture.log`, `gates/*.rc`, `probe-*.txt`.
  - The renewed evidence verifies at the exact head.
  - The host self-test (five shapes and all mutants), the service self-test (47 checks), the CI-scope self-test and the clock-contract test all return rc 0.
  - Each of my own checkers is shown to fail on a planted defect.
- [R368] PASS Docs - `docs/integration/BAREMETAL_FIRMWARE.md`, `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`, `docs/findings/README.md:12`, `docs/integration/BOARD_PORTING_AX7101.md:104-111`, `receipts/stale-statement-search.txt`, `receipts/gates/gate-{docs-check,em-dash,solution-docs,feature-status,diff-check,diff-check-lane}.*`.
  - Both lanes' authority text is intact and non-contradictory.
  - The stale rewordings are accurate, and no other statement is falsified.
  - `check_em_dash --base 7a7582f0` reports 0 findings over 555 added lines, and `docs_check` reports 0 findings. Both used the pinned Markdown environment.
  - `git diff --check` is clean from both `7a7582f0` and `20aa4eab`.
  - S1 and S2 are optional.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merge-dev assignment and disposition; conflict regions `BAREMETAL_FIRMWARE.md:1902-1979`; snapshot sections 11, 12, 18 and 20; stale rewordings; capture and service figures | R368-4 | `1f039cfe86d5337f5c9b7248696dba1c4bdda67e` |
| RTL | CLEAN | evil-merge check; #597 parameters against `protocol_processor_top` defaults; AX7101 generated headers; gitlinks; lane firmware unchanged | R368-4 | `1f039cfe86d5337f5c9b7248696dba1c4bdda67e` |
| Robustness | CLEAN | queued, built-in, device-wait and dispatch-removal regrades; disabled-writer host grade; PHY edge counts; residual text | R368-4 | `1f039cfe86d5337f5c9b7248696dba1c4bdda67e` |
| Tests | CLEAN | 138/135-artifact packet verification; 15 receipt comparisons; head-grader regrade of 15 runs plus no-publish; 6-arm capture equality; focused head gates; checker probes | R368-4 | `1f039cfe86d5337f5c9b7248696dba1c4bdda67e` |
| Docs | CLEAN (S1, S2 optional) | both merged pages; stale commit; stale-statement search; docs, em-dash, solution, feature and whitespace gates | R368-4 | `1f039cfe86d5337f5c9b7248696dba1c4bdda67e` |

R369-3 remains the external POSITIVE at the pre-merge ancestor `93262f25`, whose lane artifacts are byte-identical here, except for the three lane-equivalent merged files.

## Real limits

- **No native re-run of my own.** This host has no LiteX Python environment and no RV32 SDK. The assigned pinned Verilator path (`.../372-manager-candidate1/pinned-tool-bin/verilator`) does not exist, so its identity could not be verified and it was not used.
  - My native conclusions rest on the published packet: hash-verified, compared with round 3 byte for byte, and regraded with the head's grader.
  - Build binding (`run.py --regrade` with its build-hash check) needs the unpublished build directories. I did not repeat it; the executor recorded 15 of 15 rc 0.
- **Derived binaries were compared by hash only.** The published packet cannot show why the `Vsim`, `bios.elf` and generated-header hashes differ. That these are only timestamp/path/derivative differences is inferred: `bios.bin` and every simulation log are identical, and the generated SVH differs by `AEM_N_CONTROL_C`.
- **Capture identity fields were not independently re-derived.** The merge-head packet does not publish the capture build's CPU-netlist, BIOS, instrumented-firmware, gPTP-ROM and configuration hashes. Two facts cover them: the firmware and patch bytes are unchanged, and the capture logs are byte-identical.
- **#597 and #596 were not RTL-reviewed here.** They are dev-side work reviewed on their own PRs. This round checked only that the merge carries them unmodified, and what they mean for this lane's evidence.
- **Physical calibration NOT RUN; no hardware.** Skipped physical contexts (`Physical gPTP (nightly and manual)`: skipped) are not hardware proof. #599 acceptance 4 (the bench switch-cycle rerun, including MDIO phase on silicon) remains the post-merge lane.
- **Not run by this round:** full builder, parent, PP, gPTP and Yosys banks, per the assignment; the manager's source banks passed at this head.
- **Hosted snapshot (`receipts/hosted-check-runs.tsv`, 15:26 UTC).**
  - Completed: 11 success and 1 skipped.
  - Still in progress: 7, including `docs-check` and `elaborate`.
  - Not yet emitted: the `rtl-fast`, `verilator-suites` and `yosys-portability` aggregates.

## Pending manager duties

- Accept the exact-head hosted contexts and the act replica. They were incomplete when this round read them.
- **Build the candidate on live dev `ce550952e47fbd92367f0d9b099345100f7f4215`.** It moves protocol-processor to `c951a9ff` and changes `sw/litex/milan_soc.py`, and both are bound by the service builds and compiled by the capture harness. The capture receipt's `processor_pins` (`16be6768`) and this round's native evidence will then not describe the candidate tree, and `check_nvm_capture.py` does not bind processor pins.
  - Decide re-measure or disposition, as #580's pin move required.
  - If re-measured, resolve R368-4-S1 at the same time.
- Keep the bench LiteX environment on patch 0006 for #599 acceptance 4. Firmware without it fails to link by design.
- Out-of-scope observation for the #70 sweep, not a finding for this PR: the firmware comment `milan_baremetal.c:340` still calls the debounce "the provisional value section 14 leaves open", while dev's merged D3 DR2a text rules it. This PR did not touch that line.

## Receipts and scripts

Every published file is listed in `MANIFEST.sha256`:

- **Scripts:** `merge_lane_equivalence.py`, `verify_native_packets.py`, `compare_receipts.py`, `regrade_offline.py`, `check_capture_rows.py`, `run_focused_gates.sh` (it needs `MD_PY` set to the pinned Markdown interpreter) and `verify_clone_state.sh`.
- **Receipts:** everything under `receipts/`. Local paths are replaced by `$REPO`, `$PACKET`, `$MD_PY`, `$HOME` and `$DATA`.
- **Scratch:** the evidence clone, merge reconstructions and probe copies live under `scratch/` and are not published.

## Post-probe state

`receipts/clone-state.txt` confirms the clone after all probes:

- HEAD `1f039cfe`, tree `9ce926b9`;
- the index equals the HEAD tree (modes, objects, stage 0), with no assume-unchanged or skip-worktree entries;
- every tracked blob re-hashed from disk equals HEAD, and modes match;
- gitlinks protocol-processor `16be6768`, gptp-processor `5dce647a` and verilog-axis `48ff7a7e`, each checked out and clean;
- zero untracked files.

`external` is uninitialised by design. The planted probes ran only in a shared-object scratch clone and a scratch copy of the packet. One `git fetch origin dev` updated a remote-tracking ref only.

R368-4 FINISHED
