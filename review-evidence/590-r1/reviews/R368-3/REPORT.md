[R368] POSITIVE - exact head 93262f2512054166ae753eda24d76c99f2ea6714

# R368-3 internal independent review: issue #590 / PR #609 (with #592 and #599 simulation scope)

- Head reviewed: `93262f2512054166ae753eda24d76c99f2ea6714`, tree `439a972bb34677e0bb9b25965ef53cbd8c6bb564`, in a clean detached clone.
- Delta reviewed: `c64f8cd8..93262f25`, three commits:
  - `26a26e1f` guards disabled writers and adds the BIOS dispatch marker;
  - `69d83373` refreshes the capture and service evidence;
  - `93262f25` supplies the marker in the builder's gate-35 host fixture.
- Whole lane re-read where the delta interacts with it (`git diff 8bc97021..93262f25`).
- Round: R368-3. My round-2 findings (R368-2 N1, N2 and suggestions T1-T4) are resolved below.
- The other reviewer's round-2 report (R369-2) was read only after this verdict, the findings and the ledger were written. Its disposition is in its own section at the end.
- Authorities read:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - Issue #590: the round-3 assignment 5865679172, [A411] TAKEN 5865703318 and REVIEW READY 5869359958, and the manager's review start 5869385389.
  - The #599 body (acceptance 1-5).
  - `docs/design/SAVED_STATE_FASTCONNECT.md` section 9 (`nvm_backed`).
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` sections 18 and 20.
  - `docs/reference/REGISTER_MAP.md` MAC_STATUS.
  - `sw/litex/milan_soc.py` `link_status` resets.
  - The pinned LiteX `a1e1c3652ec2f1346ebaea7663d2867f393ae2c4`: `bios/main.c`, `bios/init.h`, `bios/linker.ld`, `bios/Makefile` and `common.mak`.
- Public evidence:
  - The round-3 author packet on `590-review-evidence` at `a9a45bdc`/`ba9e924e` (`review-evidence/590-r1/review-evidence/590-r1/author-r3/`), with the archive `MANIFEST.json` that records original and published SHA-256 per file.
  - Only the author packet and the archive manifest were extracted; no other reviewer's report was read before the verdict.

## Verdict summary

POSITIVE. Every round-3 required item and every taken suggestion is met at this head, and each one is checked below by my own execution. No BLOCKER, MAJOR or MINOR is open. Three SUGGESTIONs are optional.

1. **N1 is resolved.**
   - The firmware now has a startup admission flag, `nvm_started`:
     - it is set only after the shape check (`milan_baremetal.c:1449`);
     - it is never set on the identity-mismatch return (`:1636-1638`).
   - `nvm_heartbeat_tick()` returns before reading time, polling the PHY or writing `PP_NVM_STAT` unless the writer was admitted (`:922-940`). It is the only heartbeat-strobe writer.
   - I ran my round-2 `disabled_writer_probe.py` unchanged. The head now shows `hb=0 backed=0 stale=0` in both states, after one line, after two lines and after 2500 ms. The healthy arms are unchanged (`hb=1 backed=1`).
   - The committed `test_disabled_writer.py` caught all of the following on the 1x1 shape:
     - the actual round-2 firmware (36 findings, both states);
     - the guard moved into the hook only (caught through `milan_nvm wipe`, both states);
     - admission set before the shape check (shape state);
     - admission set at the top of `milan_init` (both states).
2. **N2 (= R369-2 F4) is resolved.**
   - Section 18 and section 20 item 6 of `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` state the receipt's commit, tree, firmware digest and processor pin.
   - They also state all six minima and maxima, the floor ratios, the 8x8 margin (11.26648 ms to 24.5 ms) and the margin gained (11.06894 ms).
   - Every figure equals my recomputation from `measurements.json`. The only remaining 24.30246 ms is labelled historical (`:1614`).
   - The PR body's summary and round-3 margin sentences match the receipt.
3. **F5 is resolved.** Both pages state that a built-in body can lapse backing after about 1,750 ms, net of the 250 ms rate-limit phase (`BAREMETAL_FIRMWARE.md:1912-1914`, `397_SERVICE_BUDGET.md:202-204`). This matches the hook and the rate limit (`:931-939`).
4. **F6 is resolved.**
   - All 135 artifacts in the author's `native-artifacts.json` verify: 62 byte-exact, 50 through the archive's recorded path-redaction chain, and 23 `.gz` entries through their published uncompressed replacements.
   - Every one of the 15 kept service runs:
     - binds its raw log (`log_sha256` and `raw_log`);
     - carries `input_hashes` equal to head `inputs()`;
     - regrades with head code to identical rows and findings and a passing verdict.
   - All 96 captures regrade to the committed receipt. The byte-only control passes at 1.83648x.
5. **Taken suggestions S5-S9 and my T1-T4 are all in place.**
   - The S5 link guard fails by name. I checked this in the host test and in an RV32 replay of the LiteX `.bios_init` KEEP, `--whole-archive` and `--gc-sections` recipe.
   - Patch 0006 applies to and reverses on the pinned LiteX.
6. **The capture receipt binds the head firmware.** Its digest `89c0360e…` equals `sha256(milan_baremetal.c)`, and `check_nvm_capture` passes. Its tree `1ced48e2` is the tree of `26a26e1f`, and nothing measured changed after that commit.
7. **There is no RTL change** (no `hdl/` path, and no gitlink change in the delta).

## Round-2 findings (R368-2): resolution at this head

| ID | Round-2 severity | Status at `93262f25` | Evidence |
| --- | --- | --- | --- |
| N1 | MINOR | RESOLVED | `milan_baremetal.c:418-419,922-940,1443-1449,1633-1638`; `test_disabled_writer.py:1-61`; `test_nvm_firmware.py:620-636`; `receipts/disabled_writer_probe_r2_unchanged.log`; `receipts/disabled_test_mutants.log`; `receipts/test_nvm_firmware_selftest.log` |
| N2 | MINOR | RESOLVED | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1591-1631,1768-1786`; `measurements.json` maxima and measurements; `receipts/kept_evidence_regrade.log` (the capture rows); `receipts/pr609_body.txt` lines 10 and 77 |
| T1 | SUGGESTION | TAKEN | `milan_baremetal.c:356-357` declares `bios_dispatch_hook_required` and `command_dispatch_hook` |
| T2 | SUGGESTION | TAKEN | `apply.sh:10` lists 0006 in apply order; `patches/README.md` has no stray blank line |
| T3 | SUGGESTION | TAKEN (stated informational) | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1599`; the field equals `sha256(0006-bios-dispatch-hook.patch)` = `f1d23563…` (`receipts/litex_patch_check.log`) |
| T4 | SUGGESTION | TAKEN | `397_SERVICE_BUDGET.md` duty tables show empty and unknown lines as N/A; `:173-175` explain N/A |

### N1 in detail

- **The guard.**
  - `phy_link_tick` has exactly one caller, `nvm_heartbeat_tick` (`:930`), and the strobe write `NVM_STROBE_HB` has exactly one site (`:936`). The guard at `:926-927` therefore covers the dispatch hook (`:943-946`), the walk and page yields (`:476-477,639-640,1022,1061`), `nvm_service` (`:1309`) and the `milan_nvm wipe` tick (`:1771`).
  - Other `PP_NVM_STAT` strobes (ARM, ATTEST, START, ACK, RELEASE, RELOAD) are reachable only through `nvm_boot` after admission, or through `nvm_commit`. `milan_nvm commit` refuses unless `nvm_ready` is set (`:1759-1762`).
  - The retired and tag-mismatch paths are unchanged, as the finding required.
- **The committed test** (`test_disabled_writer.py`):
  - It plants each rejected state on all five shapes, Arty included.
  - It requires the firmware's own message, so the precondition is proven reached.
  - It sends nine lines twice each: empty, unknown, and every Milan command including commit, wipe and the three time commands. The host bench now dispatches those commands (`nvm_host.c:652-657`).
  - It requires `hb`, `backed` and `stale` to be 0 at 0 ms and at 2500 ms.
  - Its `--self-test` mutant removes the guard and must fail both states.
  - My four independent mutants above (`scripts/disabled_test_mutants.py`) show the grade can fail for the defects it claims. That includes a Milan-command path the hook alone does not reach.
- **The consequence the executor declared publicly** (PR body round-3 section): a rejected startup performs no PHY poll. This is recorded as optional suggestion R368-3-S1 below. The shape-mismatch branch is a run-time check of compile-time constants (`nvm_shape_consistent`, `:562-575`), and all five shipped shapes pass it in the host gate.

### N2 in detail

- Recomputed from `measurements.json` (each row has 16 captures):

  | Shape | CPU MHz | Traffic | Minimum ms | Maximum ms | 49 ms / maximum |
  | --- | --- | --- | --- | --- | --- |
  | 1x1 | 50 | ON | 3.87674 | 3.88779 | 12.6036x |
  | 1x1 | 50 | OFF | 3.82856 | 3.84214 | 12.7533x |
  | 8x8 | 50 | ON | 13.21274 | 13.23352 | 3.7027x |
  | 8x8 | 50 | OFF | 13.04976 | 13.06923 | 3.7493x |
  | 8x8 | 100 | ON | 9.94138 | 9.95464 | 4.9223x |
  | 8x8 | 100 | OFF | 9.93764 | 9.94094 | 4.9291x |

- 24.5 − 13.23352 = 11.26648 ms. 24.30246 − 13.23352 = 11.06894 ms. The page states exactly these.
- The superseded traffic-arm sentences, including the inverted 100 MHz claim, are removed and replaced by a scenario-scoped statement.
- A repository-wide search finds no other stale capture figure outside the labelled historical line.

## Taken suggestions (from the round-3 assignment): verification

| Item | Status | Evidence |
| --- | --- | --- |
| S5 link-time guard for patch 0006 | MET | See the notes below this table. |
| S6 `apply.sh` header and "six patches" text | MET | `apply.sh:6-13` lists all four in SERIES order. `test_builder.py:23296` says "four patches". `:23381` says "historical six". |
| S7 `remove-dispatch` requires the named per-line finding, plus a portable control | MET | See the notes below this table. |
| S8 NAK part-way through the negotiation reads | MET | `phy_host.c:22,60,154-161` NAKs register 5 after BMSR and BMCR succeed, and requires publication 0 then recovery to 11. The committed `ack-ignored` mutant (`test_phy_firmware.py:32-36`) is caught (`receipts/test_nvm_firmware_selftest.log`). |
| S9 phase-probe locator and N/A rows | MET | `397_SERVICE_BUDGET.md:276` links the public probe at `a1c4d79f`; `:173-175` explain N/A. |

S5 details:
- `0006-bios-dispatch-hook.patch` defines a strong `bios_dispatch_hook_required()`, and `nvm_boot` calls it (`milan_baremetal.c:1443-1444`).
- The committed `check_link_guard` strips the marker and requires a named link failure. It passes on all five shapes.
- The patch applies exactly to and reverses on pinned LiteX `a1e1c365`, stacked after 0004 (`receipts/litex_patch_check.log`).
- In the pinned LiteX, `define_init_func` places the pointer in `.bios_init` and `linker.ld` KEEPs it. `milan_init` and `nvm_boot` therefore survive `--gc-sections`, and so does the marker reference.
- My RV32 replay of that link shape (`scripts/link_guard_rv32_probe.sh`): with the marker present, rc 0 and the strong `T command_dispatch_hook` wins over the weak default. Without it, rc 1 with "undefined reference to `bios_dispatch_hook_required`".
- `BAREMETAL_FIRMWARE.md:1897-1898` and `397_SERVICE_BUDGET.md:192-193` state the dependency.

S7 details:
- `run.py:552-555` requires both "continuous backing lost" and a `console line lacks a dispatch opportunity:` finding.
- `dispatch_controls` (`:470-489`) adds four portable controls, and `--self-test` reports 47 grading and 14 flash checks (`receipts/fw_service_selftest.log`).
- The per-line check now also covers `queued-short` (`:353`).
- On the real kept logs (`receipts/per_line_oracle_probe.log`), planting one missing tick at the first, middle or last console row of `queued-builtins` or `queued-short`, on either shape, yields exactly that one named finding, and the `none` verdict refuses.

## New findings (R368-3)

None at BLOCKER, MAJOR or MINOR.

## Suggestions (optional; do not affect coverage)

### R368-3-S1: a rejected shape startup also leaves MAC_STATUS unpublished; the authoritative pages do not say so

- **Lenses:** Robustness, Docs.
- **Where:**
  - In the firmware:
    - `milan_baremetal.c:926-930`: the admission guard precedes `phy_link_tick`, its only caller.
    - `:1445-1448`: the shape return.
    - `:1553`: the idle hook is installed only on admitted paths.
  - `REGISTER_MAP.md:412` says "Bare-metal firmware publishes PHY state".
  - `milan_soc.py:1783-1795`: the `link_status` resets are link up, gigabit, full duplex.
- **Evidence:** the fabric is configured and the entity is still advertised after a shape rejection (`milan_init`, `:1640-1646`). In that state MAC_STATUS stays at the reset default, and the link counters and `is_1g` never follow the real link.
  - The executor states the consequence in the PR body.
  - The branch cannot be reached on any shipped shape, because the check is a run-time comparison of compile-time constants and all five shapes pass it.
  - Before round 3, this state already had no idle service. PHY polling happened only on console lines.
  - On the identity path, leaving the SoC untouched is the stated intent.
- **Suggested outcome:** either state in `BAREMETAL_FIRMWARE.md` or `REGISTER_MAP.md` that a rejected startup publishes no PHY state, or decouple the PHY poll from writer admission on the shape path.

### R368-3-S2: the per-line dispatch oracle covers only `queued-short` and `queued-builtins`

- **Lenses:** Tests.
- **Where:** `tb/verilator/fw_service_budget/run.py:353`.
- **Evidence:** `queued-input` also suppresses idle service between queued lines. On the kept 8x8 `queued-input` log, a planted missing tick yields no finding (`receipts/per_line_oracle_probe.log`, contrast rows). Continuous-backing and heartbeat-gap checks still cover that plan, and the documented claim is scoped to the queued built-in plan, so this is not a defect.
- **Suggested outcome:** optionally apply the per-line check to `queued-input` too.

### R368-3-S3: the patch-migration recipe names only 0005, and 0006's text changed this round

- **Lenses:** Docs.
- **Where:** `sw/litex/patches/README.md:33-44`.
- **Evidence:** a LiteX tree patched with the round-2 0006 text can neither reverse nor re-apply the new text. `apply.sh` then stops at 0006, correctly and fail-closed. The generic sentence covers this case, but the commands are 0005-specific. The executor lists the bench tree as an open risk for #599 acceptance 4.
- **Suggested outcome:** add the 0006 case to the recipe or to the #599 bench runbook.

## Lens coverage and clean-result evidence

```text
[R368] PASS Conformance — milan_baremetal.c:418-419,922-946,1443-1449,1633-1638; SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1591-1631,1768-1786; measurements.json; author-r3 native-artifacts.json — round-3 items 1-4, S5-S9 and T1-T4 checked against assignment 5865679172, section 9 nvm_backed, #599 acceptance 1-5, and receipt digest = sha256(milan_baremetal.c) at 93262f25
[R368] PASS RTL — git diff c64f8cd8..93262f25 (no hdl/ path, gitlinks 16be6768/5dce647a/48ff7a7e unchanged); milan_soc.py:1783-1795 link_status resets; pinned LiteX bios/linker.ld .bios_init KEEP — no RTL change; the firmware-to-fabric identity contract ("fabric remains disabled") now holds with zero PP_NVM_STAT writes after an identity mismatch
[R368] PASS Robustness — milan_baremetal.c:562-575,926-940,1304-1311,1753-1780 — disabled, retired and tag-mismatch paths; all nine console-line classes in both rejected states; link with and without the marker; long built-in lapse bound; edge residues (all 2) on every shipped shape; S1 is optional
[R368] PASS Tests — test_disabled_writer.py; test_nvm_firmware.py --self-test; test_phy_firmware.py (4 mutants); fw_service_budget/run.py --self-test (47/14); check_nvm_capture.py (7 controls); builder gate 35 focused — all rc 0 at head, plus 4 disabled-test mutants, 3 edge mutants, MDIO phase 8 arms, per-line oracle on kept logs, and 15 kept service regrades + 96 captures
[R368] PASS Docs — BAREMETAL_FIRMWARE.md:1894-1920; 397_SERVICE_BUDGET.md (delta); SAVED_STATE_SNAPSHOT_OWNERSHIP.md sections 18 and 20.6; nvm_hosttest/README.md; patches/README.md and apply.sh; PR body — each figure checked against the receipt and kept logs; check_doc_paths and check_doc_style rc 0; git diff --check rc 0; S1 and S3 are optional
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Round-3 assignment items 1-4, S5-S9, T1-T4; #599 acceptance; section 9 contract; firmware guard; capture receipt and design page; kept native evidence | R368-3 | `93262f2512054166ae753eda24d76c99f2ea6714` |
| RTL | CLEAN | Delta has no `hdl/` or gitlink change; `link_status` CSR resets; identity contract; pinned LiteX link and init sections | R368-3 | `93262f2512054166ae753eda24d76c99f2ea6714` |
| Robustness | CLEAN | Rejected, retired and tag-mismatch writer paths under all console-line classes; link guard with and without the marker; lapse bound; record-edge residues | R368-3 | `93262f2512054166ae753eda24d76c99f2ea6714` |
| Tests | CLEAN | Host NVM self-test (disabled grade, link guard, PHY mutants); capture gate; service self-test; focused gate 35; mutation, oracle and regrade probes | R368-3 | `93262f2512054166ae753eda24d76c99f2ea6714` |
| Docs | CLEAN | Snapshot-ownership sections 18 and 20.6; BAREMETAL_FIRMWARE; #397 findings; host-test, patch README and apply.sh; PR body; doc path and style gates | R368-3 | `93262f2512054166ae753eda24d76c99f2ea6714` |

Every lens was applied at `93262f25`, which is the merge-candidate source head. No lens is banked from an earlier head.

## Real limits

- **No product-CPU simulation was run in this review.**
  - The scoped Verilator path named in the assignment (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host, so its identity could not be verified and it was not used.
  - The native `queued-builtins`, `remove-dispatch`, `late-sample`, `no-publish`, byte-only and capture arms were therefore not re-simulated.
  - I verified their kept raw logs byte-for-byte against the author manifest (through the archive's redaction record) and regraded them with head code. One check was not possible: `run.py --regrade`'s own build-hash check needs the native build directories, which are not published. My probe performs every other step of `--regrade`.
- **The native runs executed at `26a26e1f`.** Their recorded `input_hashes` equal head `inputs()`. Between `26a26e1f` and the head, only the docs, `measurements.json` and the builder fixture changed.
- **The S5 product link replay is the author's** (`product-link-guard.json`, which uses the real product BIOS objects). My RV32 probe reproduces the linker mechanism with a synthetic BIOS, not the product objects.
- **Two docs gates were NOT RUN.** `gen_toc --check` and `check_em_dash` need the pinned Markdown renderer, which is not installed here; nothing was installed.
- **No builder bank was run** (not permitted). Only gate 35, which the fixture edit touches, was run in isolation.
- **Physical calibration was not run.** Field skips and simulation are not hardware proof. The MDIO phase on silicon is #599 acceptance 4, the post-merge bench lane.

## Pending manager duties

- **Hosted acceptance at the exact head.**
  - At 12:07Z (`receipts/hosted_check_runs.txt`), `93262f25` had no check runs, no status contexts and no workflow runs.
  - GitHub reports the PR as `mergeable=CONFLICTING` against live dev `7a7582f0`, and that blocks the pull-request workflows.
  - No hosted evidence exists yet for this head. None was inspected, and none is claimed.
- **The final current-dev candidate** (source base `8bc97021`, live dev `7a7582f0`, merge base `20aa4eabf`). A local, read-only `git merge-tree` shows:
  - a content conflict in `docs/integration/BAREMETAL_FIRMWARE.md`;
  - auto-merges in `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` and `test_builder.py`.

  Dev also changed `sw/litex/milan_soc.py` since the merge base. That file is a `fw_service_budget` `inputs()` member and an input to the capture SoC, so the candidate must re-establish the capture and service bindings. It must also keep the section 18 and section 20.6 figures equal to the receipt after the merge.
- **Local act replication.**
- **The external review ([R369]).**
- **The #599 physical re-run after merge.** The bench LiteX tree must carry the round-3 0006 text (see S3), or the firmware fails to link, by design.

## Findings of the other reviewer's round 2 (R369-2): resolution at this head

I read [R369-2](https://github.com/kebag-logic/milan-fpga/pull/609#issuecomment-5865621116) only after the verdict, the findings above and the ledger were written. Nothing in it changes them. I have not read the external reviewer's current-round report.

| R369-2 item | Severity | Status at `93262f25` | Evidence |
| --- | --- | --- | --- |
| F4 design authority states the replaced receipt | MINOR | RESOLVED | See the notes below this table. |
| F5 long built-in lapse threshold | MINOR | RESOLVED | `BAREMETAL_FIRMWARE.md:1912-1914` and `397_SERVICE_BUDGET.md:202-204` state about 1,750 ms of body, net of the 250 ms phase. This is consistent with `milan_baremetal.c:931-939` and the 2,000 ms T-NVM-WRITER-ALIVE. |
| F6 native evidence not retained | MINOR | RESOLVED | See the notes below this table. |
| S5 link-time guard | SUGGESTION | TAKEN | See "Taken suggestions" above. |
| S6 stale series records | SUGGESTION | TAKEN | See "Taken suggestions" above. |
| S7 per-line oracle pinned portably | SUGGESTION | TAKEN | See "Taken suggestions" above. |
| S8 NAK part-way through negotiation | SUGGESTION | TAKEN | See "Taken suggestions" above. |
| S9 locator and N/A rows | SUGGESTION | TAKEN | See "Taken suggestions" above. |
| S10 off-by-one edge mutant is equivalent | Note | NO CHANGE NEEDED; still accurate | `receipts/edge_residues.log`: every selectable edge on every shipped shape has residue 2. `receipts/mutant2_edge-cross-3.log` survives, as in round 2. |
| R369-1 S1 PHY error hold | SUGGESTION | NOT TAKEN; retained as optional | `phy_link_tick` (`milan_baremetal.c:878-912`) is unchanged in this round. |
| R369-1 S3 builder literal 4 | SUGGESTION | NOT TAKEN; retained as optional | The only builder edits this round are two comments and the gate-35 fixture marker. |
| R369-1 S4 CHANGELOG | SUGGESTION | NOT TAKEN; retained as optional | `CHANGELOG.md:36-49` (the #580 entry) describes that pin's re-measure in historical terms. The lane has no entry, and CONTRIBUTING does not require one. |

F4 details:
- Its own verification command returns only `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1614`, which is labelled historical (`receipts/r369_2_f4_check.log`).
- The section figures equal `measurements.json` (my N2 table above).
- The PR body's margin sentences match the receipt.

F6 details:
- The round-3 packet retains raw logs, JSON receipts and specs for:
  - the `queued-builtins` positive arm on both shapes;
  - `remove-dispatch` on both queued plans;
  - target `late-sample` and `no-publish`;
  - the byte-only, skip-copy and no-traffic controls;
  - all positive plans.
- The packet binds them in `native-artifacts.json`, and all 135 entries verify through the archive manifest.
- Each of the 15 service logs, regraded with head code, prints its named PASS line and reproduces its rows and findings. The author's `run.py --regrade` runs are in `final-target-gates.json` and `native-evidence-raw/regrade-*.log`.
- Limit: the build-hash step of `--regrade` cannot be repeated without the unpublished build directories.

## Receipts and probes (listed in MANIFEST.sha256)

- **Probes** (`scripts/`):
  - `disabled_writer_probe.py`, the round-2 probe run unchanged → `receipts/disabled_writer_probe_r2_unchanged.log`.
  - `disabled_test_mutants.py` → `receipts/disabled_test_mutants.log`.
  - `link_guard_rv32_probe.sh` → `receipts/link_guard_rv32_probe.log`.
  - `kept_evidence_regrade.py` → `receipts/kept_evidence_regrade.log`.
  - `per_line_oracle_probe.py` → `receipts/per_line_oracle_probe.log`.
  - `mdio_phase_probe.py` with `mdio_peer_probe.c` → `receipts/mdio_phase_probe.log`.
  - `edge_residues.py` → `receipts/edge_residues.log`.
  - `host_mutant2.py` → `receipts/mutant2_*.log`.
  - `host_mutant_r1.py`, the round-1 probe unchanged → `receipts/mutant_r1probe_edge_cross.log`.
- **Committed gates:**
  - `receipts/test_nvm_firmware_selftest.log`;
  - `receipts/fw_service_selftest.log`;
  - `receipts/check_nvm_capture.log`;
  - `receipts/builder_gate35_focused.log`;
  - `receipts/doc_checks.log`.
- **Other receipts:**
  - `receipts/litex_patch_check.log`;
  - `receipts/r369_2_f4_check.log`;
  - `receipts/pr609_body.txt`;
  - `receipts/hosted_check_runs.txt`;
  - `receipts/clean_state.txt`.

## Post-probe state

- `receipts/clean_state.txt`:
  - HEAD `93262f25…`, tree `439a972b…`; the index writes the same tree.
  - Every tracked blob rehashes to its index entry.
  - No mode, blob, path or gitlink difference.
  - Porcelain is empty, including ignored files, after I removed 17 ignored `__pycache__` files created by the probes.
  - `protocol-processor 16be6768`, `gptp-processor 5dce647a` and `third_party/verilog-axis 48ff7a7e` are at their gitlinks and clean; `external` is uninitialized, as at clone time.
- All probes and mutants ran from temporary copies or `scratch/`.
- No source edit, commit, push or GitHub write was made.

R368-3 FINISHED
