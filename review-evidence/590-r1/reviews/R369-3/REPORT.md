[R369] POSITIVE - exact head 93262f2512054166ae753eda24d76c99f2ea6714

# R369-3 external independent review: PR #609 (#590, #592, #599), round 3

- Round: R369-3, external reviewer, cleared context. Delta focus `c64f8cd8..93262f25` (`26a26e1f3` firmware guard, link marker and tests; `69d833735` receipt and docs refresh; `93262f251` builder host fixture). All five lenses were applied at the exact head.
- Exact head `93262f2512054166ae753eda24d76c99f2ea6714`, tree `439a972bb34677e0bb9b25965ef53cbd8c6bb564`. Source base `8bc97021f28fb7f729418d3a00851c84ea0b50fd`. Live dev at review time `7a7582f03ce5ba7863a90ac342c21be18d90db0b`. Processor pin `16be6768f710e79450aace277abacd6c2c3336e5`.
- Scope sources:
  - AGENTS.md, CONTRIBUTING.md (sections 2, 3, 6), docs/README.md.
  - #590 body; round-3 assignment 5865679172; round-2 assignment 5862495507; round-3 TAKEN 5865703318 and REVIEW READY 5869359958.
  - #592 and #599 bodies; the PR #609 body, including its Round 3 section.
  - Public evidence branch `590-review-evidence` at `ba9e924e`: author packet `author-r3/`, `native-evidence/`, `native-evidence-raw/` and the archive `MANIFEST.json`. The archive's `reviews/` tree was excluded from extraction and not read.
- My round-2 packet was used as read-only input.
- I read the prior public R368-2 findings (5865670438) only after this verdict and ledger were drafted. I did not read the concurrent R368-3 round.
- **Overall result:** every round-3 required item holds at this head: N1, F4 = N2, F5 and F6. The taken suggestions S5 to S9 also hold. I re-ran my own probes and mutants against each. No BLOCKER, MAJOR or MINOR finding is open. Two new SUGGESTIONs are recorded, and they do not affect coverage.

## Findings

None at BLOCKER, MAJOR or MINOR severity.

## Suggestions (do not affect coverage)

### S11 - SUGGESTION - Docs, Robustness - PHY link publication now also requires writer admission, and the PHY paragraph does not say so

- **Where:**
  - `sw/firmware/milan_baremetal/milan_baremetal.c:926-930`: the `nvm_started` early return precedes `phy_link_tick(now)`.
  - `docs/integration/BAREMETAL_FIRMWARE.md:1939`: "Firmware also publishes PHY state through the existing MDIO window."
- **Evidence:**
  - On a shape mismatch the fabric is still configured and the entity is still advertised (`milan_init`, `:1641-1647`). Round 3 adds that MAC_STATUS is also never published, so it keeps its reset value (`link_up=1`, build-time speed).
  - That is the #599 flat-link state, confined to this startup state.
  - The executor disclosed it in REVIEW READY 5869359958 and in the PR body, but not on the authoritative page.
  - For the identity mismatch, not touching a foreign fabric is the right behaviour.
- **Why SUGGESTION:** `nvm_shape_consistent()` (`:562-575`) compares one build's generated tables with its own generated sizes, so a shipped image can reach this state only through a generator defect. The boot line announces it.
- **Option:** one sentence on the PHY paragraph, or a PHY opportunity that does not depend on `nvm_started` in the shape-mismatch case.

### S12 - SUGGESTION - Tests - the per-line oracle's `queued-short` extension has no portable control

- **Where:** `tb/verilator/fw_service_budget/run.py:353` now fires for `queued-builtins` and `queued-short`. `dispatch_controls()` (`:470-489`) uses `queued-builtins` only.
- **Evidence:** in `receipts/dispatch-control-mutants.log`, the mutant that narrows the oracle back to `queued-builtins` passes both `dispatch_controls()` and `service_controls()`.
- **Mitigation:** the target `remove-dispatch` control on `queued-short` would fail under that mutant, because its verdict now requires a per-line finding. The kept native receipt shows 350 per-line findings (`receipts/f6-regrade.log`). The coverage exists natively but not portably.
- **Option:** one `queued-short` row in `dispatch_controls()`.

### Retained, not taken (unchanged at this head)

- R369-1 S1: a single NAK or undiscovered PHY republishes link down on each opportunity (`milan_baremetal.c:887-911`). The new S8 test confirms the down publication on a register-5 NAK, which is the documented behaviour.
- R369-1 S3: the builder literal 4.
- R369-1 S4: there is no `CHANGELOG.md` entry. No stale capture figure remains in `CHANGELOG.md` (`receipts/stale-figure-scan.log`).
- R369-2 S10: `next - i >= 3u` is behaviourally equivalent on every shipped shape. This is unchanged (`receipts/edge-residue-probe.log`).

## Verification of the round-3 items

### 1. R368-2 N1: resolved

- **Code:**
  - `nvm_started` (`milan_baremetal.c:419`) is set only at `:1449`, after the shape check (`:1445-1448`). `milan_init` returns on an identity mismatch (`:1636-1639`) before `nvm_boot`.
  - `nvm_heartbeat_tick` (`:922-939`) returns before `gettime_ns`, the PHY tick or the strobe unless the writer was admitted.
  - It is the only `NVM_STROBE_HB` writer (`:936`). No `nvm_csr_write` addresses word 4.
  - The dispatch hook (`:943-946`), the Milan handlers, the walk yields (`:476`, `:639`, both also gated on `nvm_ready`) and the idle service all go through it.
- **Retained rules:**
  - The retired-writer rule (`:932`) is unchanged.
  - Tag-mismatch heartbeating is unchanged. That is the documented UNRESOLVED 8 (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1799-1807`), and N1 excluded it explicitly.
  - Item 8's sentence "on a SHAPE mismatch ... nothing heartbeats" is true again at this head.
- **My probe** (`scripts/disabled_writer_probe.py`, `receipts/disabled-writer-probe.log`) is independent of the committed test:
  - It plants the identity mismatch in the host CSR model (`ID_MAGIC ^ 1`) and the shape mismatch through the generated header (`MILAN_NVM_IMAGE_MAX 16`). The firmware source is unmodified.
  - It drives 28 console lines: empty, whitespace, unknown and built-in names, every Milan command, and bad-argument forms. It runs them with 0 ms and with 300 ms of idle time after each line.
  - On all five shapes and in both states, `hb`, `backed`, `stale`, `arms`, `starts`, `acks` and `reloads` are all 0. The live control heartbeats (`hb=35 backed=1`).
  - Three firmware mutants are each killed in the state they target: the guard removed (both states), admission moved above the shape check, and admission set before the identity return.
  - Observation, not a finding: `milan_nvm wipe` still erases both slots under a rejected writer (`erases=4`). This is the pre-existing operator behaviour at `8bc97021` and does not involve the backend.
- **Committed test** `sw/firmware/nvm_hosttest/test_disabled_writer.py`:
  - `test_nvm_firmware.py --self-test` rc 0 (`receipts/host-selftest.log`).
  - Both states pass `hb=0 backed=0 stale=0` over 18 cases on each of five shapes, Arty included.
  - "disabled-writer mutant: caught in both states". Each state prints FAIL under the unguarded hook.

### 2. N2 = R369-2 F4: resolved

- Section 18 (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1591-1629`) states:
  - measured commit `26a26e1f`, tree `1ced48e2` (equal to `git rev-parse 26a26e1f3^{tree}`) and firmware `89c0360e...`;
  - all six maxima and minima with floor ratios;
  - 13.23352 ms, a margin of 11.26648 ms to 24.5 ms (`:1611-1613`), and 11.06894 ms gained (`:1615`).
- Section 20 item 6 (`:1768-1786`) repeats the maxima and both margins.
- I recomputed every table row and ratio from `measurements.json` (`receipts/stale-figure-scan.log`). All six rows match.
- The only remaining old figure is `:1614`, labelled "historical". The inverted 100 MHz traffic claim is removed.
- The PR body's top summary gives the same margins. Its round-2 section is headed as superseded.

### 3. R369-2 F5: resolved

- `BAREMETAL_FIRMWARE.md:1912-1914` and `397_SERVICE_BUDGET.md:202-204` both say "A built-in body can lapse backing after about 1,750 ms. The 2,000 ms deadline includes up to 250 ms beforehand."
- This matches `nvm_heartbeat_tick`'s 250 ms rate limit and T-NVM-WRITER-ALIVE.

### 4. R369-2 F6: resolved

My portable regrade is `scripts/f6_regrade.py`, with output in `receipts/f6-regrade.log` (rc 0).

- **Archive manifest:** all 224 published `author-r3/` files match the archive `MANIFEST.json` published hashes.
- **Native manifest (`native-artifacts.json`, 135 entries):**
  - 62 match as stored.
  - 23 `.gz` entries are not in the archive. Their uncompressed copies under `native-evidence-raw/` match `raw_size` and `raw_sha256`.
  - 50 build logs and spec files differ only by publication path redaction. For each, the archive manifest records `path_redacted` with `original_sha256` equal to the native manifest hash.
- **Service receipts (15):**
  - Each raw simulator log hashes to its receipt's `log_sha256`.
  - Each receipt's `input_hashes` equal this head's `run.inputs()`: firmware, patches, configs and measurement code.
  - `build_hashes` equal the kept spec's.
  - The head `grade()` and `service_findings()` recompute rows, liveness, PHY and heartbeat exactly. `report_verdict()` prints the same line as each kept `--regrade` log.
- **Positive arms:** `queued-builtins` on 1x1 and 8x8 gives 1051 of 1051 lines ticked, `unbacked_cycles=0` and 0 findings. All twelve positive plans pass, with a largest heartbeat gap of 322.47884 ms.
- **Controls:**
  - `remove-dispatch` on `queued-builtins`: 1051 named per-line findings plus "continuous backing lost", gap 8238.99253 ms.
  - The same control on `queued-short`: 350 per-line findings.
  - Target `late-sample`: the named "PHY initial gigabit negotiation was not published".
  - `no-publish`: its named PASS line with the failing raw log.
- **Captures:** all 96 rows regrade to the committed `measurements.json`. The byte-only control passes `grade_byte_only`, with a minimum of 24.30310 ms against 13.23352 ms (1.83648x, bound 1.5x) and its baseline hash bound.
- **Limit:** a literal `run.py --regrade` needs the build directory (`native/Vsim`, BIOS), which is not retained. My regrade therefore re-checks everything except the build-binary hashes, which are consistent between spec and receipt but cannot be re-hashed.

### 5. Taken suggestions

- **S5 (link guard): holds.**
  - Patch 0006 (sha256 `f1d23563...`) now defines a strong `bios_dispatch_hook_required()`. `nvm_boot` calls it at `:1444`, on the path `milan_init` reaches through the kept `.bios_init` table.
  - 0006 applies cleanly after 0004 to pristine pinned LiteX `a1e1c365` files, reverse-checks, and equals the shared install's `main.c` (`receipts/patch-0006-apply.log`).
  - `scripts/link_guard_probe.sh` (`receipts/link-guard-probe.log`) uses the product link shape: `-ffunction-sections`, `--gc-sections` and whole-archive. A BIOS without the marker is refused by name, and one with it links and runs.
  - The same probe shows that a reference only in unreached code would be garbage-collected silently. The guard therefore relies on the call staying on the init path, which is true at this head.
  - The host test's stripped-marker link is refused (`host-selftest.log`). `BAREMETAL_FIRMWARE.md:1897-1898` and the patches README note the dependency.
- **S6: holds.** The `apply.sh:6-13` header lists 0006. `test_builder.py` says "four patches", which matches 0002, 0004, 0005 and 0006, and "historical six".
- **S7: holds.**
  - The `report_verdict('remove-dispatch')` path requires the named per-line finding (`run.py:549-556`).
  - `dispatch_controls()` adds 4 checks. The self-test reports 47 grading and 14 flash checks (`receipts/service-selftest.log`).
  - My mutants (`receipts/dispatch-control-mutants.log`) kill three of four planted defects: oracle removed, verdict requirement removed, and over-eager oracle. The fourth is S12.
- **S8: holds.** A register-5 NAK after good BMSR and BMCR reads must publish 0 (`phy_host.c:154-161`). The committed `ack-ignored` mutant is caught. My round-2 `ack-ignored` mutant, which survived in round 2, is now killed (`receipts/mdio-mutants.log`).
- **S9: holds.**
  - `397_SERVICE_BUDGET.md:276` links the phase probe at `a1c4d79f`. That blob equals my round-1/2 probe byte for byte (sha256 `06ac49d5...`).
  - `:173-175` explains the N/A rows.
- **R368-2 T1 to T4:** also addressed. T1 is confirmed below. T2 is the `apply.sh` header and the README list. T3 is the "informational provenance" sentence at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1599`. T4 is the N/A rows.

### 6. Capture binding: holds

- `check_nvm_capture.py` rc 0 at head (`receipts/check_nvm_capture.log`).
- `product_firmware_sha256` equals `sha256(milan_baremetal.c)` at head, and `tree` equals `26a26e1f3^{tree}`. The only later commits touch docs, the receipt and a builder fixture.
- All six `harness_sha256` values equal the head files. `bios_dispatch_patch_sha256` equals the head 0006 patch.
- `check_receipt` refuses the round-2 digest and a one-digit change (`receipts/capture-digest-mutant.log`).
- 8x8 at 50 MHz: 13.23352 ms against 24.5 ms. No STOP condition applies.

### 7. No RTL change: holds

- `c64f8cd8..93262f25` touches no `hdl`, `configs`, processor, `milan_soc.py` or constraint file.
- Against the merge base with live dev, the lane touches none either. All four gitlinks equal live dev's.
- The processor-pin difference from `8bc97021` enters through the dev merge `42f7f4fe7` (`499b15f97` is in live dev).

### Regression re-runs of my earlier probes

These probes were copied unchanged from my round-2 packet:

- MDIO phase: under `PHASE=1` the probe reads BMSR `0x796d`, PHYID1 `0x001c` and `link_status=13`. The old convention fails.
- MDIO mutants: one-turnaround, three-turnaround, `ack-ignored`, fifteen-data and write-opcode are all killed. The settle-free sample passes, as an equivalent.
- Edge mutants on five shapes: `>= 1u`, `>= 2u`, no-edge-guard and ownership-ignoring copies are all caught by the named finding. The byte-only copy is equivalent.
- Built-in oracle probe: the per-line finding now fires for both queued plans.
- Weak and strong hook linkage: unchanged.

## Prior public findings: disposition at this head

These were read after my own pass.

| Finding | Disposition |
| --- | --- |
| R368-2 N1 (MINOR) | Resolved. See item 1. |
| R368-2 N2 = R369-2 F4 (MINOR) | Resolved. See item 2. |
| R369-2 F5 (MINOR) | Resolved. See item 3. |
| R369-2 F6 (MINOR) | Resolved. See item 4, with the stated `--regrade` limit. |
| R369-2 S5 to S9 (taken) | Verified. See item 5. S7's `queued-short` extension leaves S12. |
| R368-2 T1 (prototype) | Resolved. The prototypes are at `milan_baremetal.c:356-357`. `-Wmissing-prototypes -Wstrict-prototypes` gives 0 warnings (`receipts/prototype-warnings.log`). |
| R368-2 T2, T3, T4 | Resolved. See item 5. |
| R369-2 S10, R369-1 S1/S3/S4 | Not taken. Retained as suggestions. |
| Earlier rounds (R368-1 F1 to F3, S1, S2; R369-1 F1, F2) | Resolved in round 2. The regression re-runs above still hold. |

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Round-3 assignment items 1-4 and S5-S9 against `milan_baremetal.c:419,922-946,1443-1449,1636-1639`; #590 acceptance 1-4 via 15 regraded native receipts (`f6-regrade.log`); #592 acceptance 2 via `measurements.json`, `check_nvm_capture.log` and `capture-digest-mutant.log`; #599 via `probe_mdio_phase-head.out` and `mdio-mutants.log`; UNRESOLVED 8 (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1799-1807`) | R369-3 | `93262f2512054166ae753eda24d76c99f2ea6714` |
| RTL | CLEAN | `git diff c64f8cd8..93262f25` and the diff against the live-dev merge base: no `hdl`, `configs`, processor, `milan_soc.py` or constraint path; four gitlinks equal live dev `7a7582f0` (`verify-head-bytes.log`); the firmware-to-fabric strobe contract (single HB writer `:936`, no word-4 `nvm_csr_write`); BIOS C patch 0006 against pinned `main.c` (`patch-0006-apply.log`) | R369-3 | `93262f2512054166ae753eda24d76c99f2ea6714` |
| Robustness | CLEAN (S11 optional) | Rejected identity and shape startup under 28 console-line classes with and without idle time on 5 shapes (`disabled-writer-probe.log`); tag-mismatch and retired paths against `:932` and UNRESOLVED 8; missing-0006 link under gc-sections (`link-guard-probe.log`); mid-negotiation NAK (`phy_host.c:154-161`); wipe under a rejected writer (pre-existing) | R369-3 | `93262f2512054166ae753eda24d76c99f2ea6714` |
| Tests | CLEAN (S12 optional) | `test_nvm_firmware.py --self-test` rc 0, including `test_disabled_writer.py` and its guard mutant, the link guard, and PHY `ack-ignored` (`host-selftest.log`); `run.py --self-test` 47+14 (`service-selftest.log`); reviewer mutants `disabled-writer-probe.log`, `dispatch-control-mutants.log`, `mdio-mutants.log`, `edge-mutants.log`, `edge-residue-probe.log`, `capture-digest-mutant.log`; `ci_scope.py --selftest` rc 0; focused builder gate 35 rc 0 (`gate35-focused.log`) | R369-3 | `93262f2512054166ae753eda24d76c99f2ea6714` |
| Docs | CLEAN (S11 optional) | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1591-1629,1768-1786` recomputed against `measurements.json` (`stale-figure-scan.log`); `BAREMETAL_FIRMWARE.md:1896-1916`; `397_SERVICE_BUDGET.md` round-3 diff (`:173-175,190-204,276`); `nvm_hosttest/README.md`; patches README and `apply.sh`; the PR body Round 3 section; `docs_check`, `check_doc_paths`, `check_doc_style`, `check_archive`, `check_em_dash --base 8bc97021`, `gen_toc --check` and `git diff --check 8bc97021 HEAD` all rc 0 | R369-3 | `93262f2512054166ae753eda24d76c99f2ea6714` |

## Receipts (listed in MANIFEST.sha256)

- **New scripts:**
  - `scripts/disabled_writer_probe.py`
  - `scripts/f6_regrade.py`
  - `scripts/dispatch_control_mutants.py`
  - `scripts/link_guard_probe.sh`
- **Scripts copied unchanged from R369-2:**
  - `probe_mdio_phase.py`, `probe_mdio_phase.c`
  - `mdio_mutants.py`, `edge_mutants.py`, `edge_residue_probe.py`
  - `builtin_oracle_probe.py`, `weak_link_probe.sh`
  - `verify_head_bytes.py`
  - The last line of `builtin_oracle_probe.py` is a text heuristic that predates S7. Its round-3 output is superseded by `dispatch-control-mutants.log`.
- **Receipts:**
  - Every file under `receipts/`.
  - `verify-head-bytes.log`: HEAD, tree, 946 file blobs and modes and 4 gitlinks match the exact head. Porcelain including ignored files is empty in the superproject and all three required submodules, and each submodule is at its pin.
  - The `__pycache__` directories this session created were removed before that check.

## Real limits

- **No native product-CPU simulation was run by me.** Target-side claims rest on the published native logs and receipts. I regraded those logs with the head code. The build binaries are not retained, so their hashes are consistent but not re-hashable. The scoped Verilator was not needed and was not used.
- **Builder banks were not run** (outside allowance). Only focused gate 35 was run, because it exercises the new host-fixture marker.
- **LiteX:** patch applicability was checked on pinned files extracted read-only into this packet's scratch area. The shared LiteX tree was only read.
- **Hosted CI:** at 12:22Z the exact head had no workflow runs, no check runs and no statuses (`hosted-checks-snapshot.txt`). There is no hosted evidence to inspect for this head.
- **Physical:** calibration NOT RUN, and field skips are not hardware proof. The MDIO phase on silicon and the switch cycles are #599 acceptance 4, after merge.
- **Scratch installs:** the two Markdown gates needing the pinned renderer ran from a disposable environment under this packet's scratch area. Nothing shared was installed.

## Pending manager duties

- Hosted and local-replica acceptance at the exact head. No hosted run existed when this review was written.
- The final current-dev candidate build and merge validation (source base `8bc97021`, live dev `7a7582f0`), and post-merge containment.
- The concurrent internal review (R368-3) stays independent. Merging needs two positive reviews and the full completion bar.
- #599 acceptance 4 on the bench. The bench LiteX environment must carry the round-3 patch 0006, or the firmware will fail to link by design.
- Optional S11 and S12.
- Evidence packaging note: `native-artifacts.json` names 23 `.gz` stored paths that the archive carries only uncompressed. The raw bindings verify.

R369-3 FINISHED
