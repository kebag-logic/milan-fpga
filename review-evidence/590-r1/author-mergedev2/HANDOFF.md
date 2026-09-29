# Merge-dev round handoff

Status: REVIEW READY at head `4c2a30debb031595b81c5c4bfc53b601a0fec528` (tree `0a9754d44e40de8c734468be2cedad5ac675d794`), local only.
- The manager's disposition of the STOP (option (a)) is applied: one six-line commit adds the probe's `bios_dispatch_hook_required()` stub to `tb/verilator/nvm_cosim/cosim_host.c`. Nothing else changed.
- The full `nvm_cosim` suite passes: rc 0, 465/465 checks, 39/39 mutants killed by their named checks. W1 shows `nvm_boot()` re-arms `nvm_started` after the modelled restart.
- The native service and capture re-run (25 arms, 65 commands) is byte-identical to the previous round's evidence, and hence to round 3's, at dev's processor pin and #602 RTL.
- Every gate is rc 0. No `d0203aac` receipt is reused.
- REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5881242928 (text in `REVIEW-READY.md`).
Role: executor [A430]. Reviewer: [R368] (delta review of the merge and both fixture commits, per the disposition), then the candidate, composition review, act and merge named in the assignment.
Scope: PR #609 (#590, #592, #599). Assignment: #590 comment 5879349035. Disposition of the STOP: #590 comment 5879883680, option (a).
Starting head: `1f039cfe86d5337f5c9b7248696dba1c4bdda67e`, branch `590-592-599-firmware`, remote `https://github.com/kebag-logic/milan-fpga.git`, clean at start.
Dev: `origin/dev` fetched at `b5c0f69d5d11f0ec4bc847a2cfdd13e89e199a8a`. Previous merge base: `7a7582f03ce5ba7863a90ac342c21be18d90db0b`.
Public: TAKEN https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5879363819 (`TAKEN.md`); STOP https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5879875407 (`STOP.md`); REVIEW READY https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5881242928 (`REVIEW-READY.md`).

## Commits

| Commit | Tree | Subject | Change |
| --- | --- | --- | --- |
| `9f94b246bc714e76e52a3dab3d4be4cd7bf3ca67` | `3e431008b8b7acde0a9d2cdb0ae1c14d547ad3a1` | `Merge dev into 590-592-599-firmware` | merge of `b5c0f69d` into `1f039cfe`; no body, no trailers |
| `d0203aac9724653ea0fb4a61d28ad2e42e515e74` | `73d39ccd3f32ce7ae3e6b6cede917b3925efb73f` | `Model nvm_started in the nvm_cosim writer restart` | `tb/verilator/nvm_cosim/run_cases.py`, 1 line (assignment item 2) |
| `4c2a30debb031595b81c5c4bfc53b601a0fec528` | `0a9754d44e40de8c734468be2cedad5ac675d794` | `Stub the patch-0006 link marker in the nvm_cosim host` | `tb/verilator/nvm_cosim/cosim_host.c`, 6 added lines (disposition (a)) |

- Each subject is one line, with no body and no trailer. No commit was amended.
- Processor gitlink `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3` at all three commits, equal to dev's; the pre-merge head had `16be6768f710e79450aace277abacd6c2c3336e5`. The submodule checkout is at `c951a9ff` (`git -C protocol-processor rev-parse --show-toplevel` is the submodule directory).
- No stale-statement commit was needed (see "Stale-statement search").
- Nothing is pushed.

## Merge

- `git merge-tree --write-tree HEAD origin/dev` before the merge reported one conflict, `docs/findings/README.md`. `BAREMETAL_FIRMWARE.md`, `MILAN_COMPLIANCE_MATRIX.md`, `REGISTER_MAP.md` and `sw/builder/test_builder.py` auto-merged.
- `git diff 1f039cfe 9f94b246` has exactly the changed lines of dev's own delta `git diff 7a7582f0 b5c0f69d`: 51 files, +2176/-413.
- `git diff b5c0f69d 9f94b246` has exactly the changed lines of this PR's delta `git diff 7a7582f0 1f039cfe`: 28 files, +2886/-648.
- In both comparisons, only context lines differ: the other side's findings-index row.
- The four patches are over 200 KB, so they are kept outside this packet. `logs/merge-diffs.sha256` binds their sizes and SHA-256.

## Conflict resolution

Rule applied: keep every row from both sides in the index's own ordering, with no duplicates (assignment item 1).

- Dev (#395, PR #605) inserted one row, `COMMERCIAL_TIMING_395.md`, directly after the `75_RECONNECT_RESTART_MEASUREMENT.md` row and before the `397_SERVICE_BUDGET.md` row. It did not change the 397 row.
- This PR changed only the `397_SERVICE_BUDGET.md` row: the previous merge-dev stale-statement commit `1f039cfe` reworded its scope and state.
- Resolution: dev's inserted row at dev's position, then this PR's 397 row. The 397 row appears once.
- Check: the resolved page differs from dev's page only by this PR's 397 row. It differs from the pre-merge page only by dev's inserted row.

### Before (conflict as presented, `docs/findings/README.md:10-18`)

```text
|---|---|---|
| [75_RECONNECT_RESTART_MEASUREMENT.md](75_RECONNECT_RESTART_MEASUREMENT.md) | Two CRF pairs; disconnect, two-second hold, reconnect (#75) | 100 listener and 97 talker restarts measured; three non-restarts tracked by [#608](https://github.com/kebag-logic/milan-fpga/issues/608); initial-bind exception tracked by #606; AAF unmeasured |
<<<<<<< HEAD
| [397_SERVICE_BUDGET.md](397_SERVICE_BUDGET.md) | Product-CPU firmware service intervals at 50 MHz after the #590, #592 and #599 repairs, with external markers (#397) | Simulation measurement under the one-hart decision; future duties, physical torture and bench proof remain open |
=======
| [COMMERCIAL_TIMING_395.md](COMMERCIAL_TIMING_395.md) | AX7101 commercial-grade timing at both fixed speed models for the `9e9954e9` shipping checkpoint (#395 items 1, 2 and 5) | Applied constraints meet the recorded margin; rejected constraints belong to #607; physical temperature and oscillator measurements remain open |
| [397_SERVICE_BUDGET.md](397_SERVICE_BUDGET.md) | Product-CPU firmware service intervals at 50 MHz, using unchanged firmware and external markers (#397) | Simulation measurement; architecture decision and bench proof remain open |
>>>>>>> origin/dev
| [117_GPTP_SILICON_EVIDENCE.md](117_GPTP_SILICON_EVIDENCE.md) | One AX7101 against the reference peer on dev `ede8d48e`: asCapable, cadence, turnaround, GM loss and return over six switch power cycles, publication and `tu` against the wire, controller enumeration (#117) | Current; GM loss and return inside the 5 s bound (worst 1.60 s) |
```

### After (merge commit, `docs/findings/README.md:10-14`)

```text
|---|---|---|
| [75_RECONNECT_RESTART_MEASUREMENT.md](75_RECONNECT_RESTART_MEASUREMENT.md) | Two CRF pairs; disconnect, two-second hold, reconnect (#75) | 100 listener and 97 talker restarts measured; three non-restarts tracked by [#608](https://github.com/kebag-logic/milan-fpga/issues/608); initial-bind exception tracked by #606; AAF unmeasured |
| [COMMERCIAL_TIMING_395.md](COMMERCIAL_TIMING_395.md) | AX7101 commercial-grade timing at both fixed speed models for the `9e9954e9` shipping checkpoint (#395 items 1, 2 and 5) | Applied constraints meet the recorded margin; rejected constraints belong to #607; physical temperature and oscillator measurements remain open |
| [397_SERVICE_BUDGET.md](397_SERVICE_BUDGET.md) | Product-CPU firmware service intervals at 50 MHz after the #590, #592 and #599 repairs, with external markers (#397) | Simulation measurement under the one-hart decision; future duties, physical torture and bench proof remain open |
| [117_GPTP_SILICON_EVIDENCE.md](117_GPTP_SILICON_EVIDENCE.md) | One AX7101 against the reference peer on dev `ede8d48e`: asCapable, cadence, turnaround, GM loss and return over six switch power cycles, publication and `tu` against the wire, controller enumeration (#117) | Current; GM loss and return inside the 5 s bound (worst 1.60 s) |
```

The conflicted page as presented is kept in `logs/findings-README-conflict.md`.

## Clean-merge checks (assignment item 1)

**`docs/integration/BAREMETAL_FIRMWARE.md`.**
- Dev changed two rows of the #602 structural-check table (merged `:1482` and `:1484`): `media_rebase_p_w` now has two references, and `mcr_restart_p_w` excludes the PHC-step term under the #602 ruling.
- This PR's hunks are at `:72-78` (service budget), `:1902-1928` (runtime and dispatch hook), `:1954-1980` (capture copy and PHY publication) and `:1988-1990`.
- None of this PR's added lines mention restart, re-base, PHC, media clock or `mcr`. Dev's rows mention no dispatch, heartbeat, capture or MDIO behaviour.
- The two lanes' statements are disjoint, so neither contradicts the other.

**`docs/reference/MILAN_COMPLIANCE_MATRIX.md` and `docs/reference/REGISTER_MAP.md`.**
- Dev (#602) changed matrix rows 5.4.2.15/.16 (`:120`), 5.3.11.1 (`:169`) and 4.4.4.3 (`:206`), and register-map lines `:127-131`. All concern `mr`, MEDIA_RESET and PHC-only re-base.
- This PR changed matrix row 7.4.42.2 (`:192`) and added register-map lines `:413-418`. Both concern firmware MDIO publication of `link_status` into MAC_STATUS and the fabric LINK_UP/LINK_DOWN counters.
- A merged-file search for `link_status|MAC_STATUS|LINK_UP|LINK_DOWN|mdio|PHY state|straps|until a driver|PHC step|PHC-only|MEDIA_RESET` finds no row that describes the other lane's mechanism.
- Dev's 4.4.4.3 row names "selected-CRF disruption" as an `mr` cause. A real link loss that this PR now publishes can cause such a disruption under CRF selection, which is consistent with that row.

**`sw/builder/test_builder.py`.**
- Dev (#595, #602) adds gate 36b (`_image_contract_cases`, four `test_shipping_image_contract*` functions) and `test_commercial_timing_grade`. It registers them in the main list (`:27819`, `:27893-27894`) and edits gate text in `test_baremetal_profile_contract` and the schema-12 refusal cases.
- This PR changes gate 1b's directive-reader count (`:13304`), two comments (`:23297`, `:23382`) and the gate-35 host fixture's `bios_dispatch_hook_required` declaration and stub (`:26647`, `:26668`).
- The hunks are disjoint. `gate 36b` occurs 0 times at the previous merge base and 0 times at `1f039cfe`, and this PR adds no gate, gate number or main-list entry.
- The merged file has 90 top-level `def test_` names with no duplicate.
- The full builder bank at the new head is the executable check (Gate table).

## Restart model (assignment item 2)

**The ruling's premise holds at this head.**
- `nvm_started` is a file-scope writer static (`milan_baremetal.c:419`, `static int nvm_started;`). It is zero-initialised, so a CPU-only reset returns it to 0.
- Only `nvm_boot()` sets it (`:1449`), after the shape check at `:1445-1448`. Its only reader is `nvm_heartbeat_tick()` (`:926-927`).
- The refusal regex in `run_cases.py:196-197` matches it together with the fourteen statics already modelled.

**Commit `d0203aac`** changes one line (`logs/restart-model.diff`, SHA-256 `3733987c…`). `nvm_started` goes first, in declaration order, and the line is 113 columns, under the 120-column limit of `check_py_idiom`:

```diff
@@ -178,7 +178,7 @@ def host_firmware(text: str, fences: int) -> str:
 
 #: the writer's file-scope state and its initial value: what a CPU-only reset
 #: gives back (the C start-up zeroes .bss and reloads .data)
-WRITER_STATICS = {"nvm_ready": "0", "nvm_retired": "0", "nvm_in_commit": "0", "nvm_seq": "0",
+WRITER_STATICS = {"nvm_started": "0", "nvm_ready": "0", "nvm_retired": "0", "nvm_in_commit": "0", "nvm_seq": "0",
                   "nvm_auth_slot": "NVM_SLOT_NONE", "nvm_verdict_a": "0",
                   "nvm_verdict_b": "0", "nvm_last_verdict": "0", "nvm_commits_ok": "0",
                   "nvm_commits_failed": "0", "nvm_captures_refused": "0",
```

- The refusal at `run_cases.py:199` no longer fires.
- The generated `milan_baremetal.host.c` restart body opens with `nvm_started = 0;`, followed by the other fourteen statics, `set_idle_hook(0);` and `nvm_boot();`.

**What happened at `d0203aac` (the STOP).**
- `make -C tb/verilator/nvm_cosim` returned rc 2 after 16.4 s. Every build that reached the link failed on one symbol, `undefined reference to 'bios_dispatch_hook_required'`, from `nvm_boot()` (`milan_baremetal.c:1444`). Those builds were `contract-1x1`, `contract-8x8`, `idw2-1x1`, `mut-A01` and `mut-F01`.
  - Receipt: `at-d0203aac/receipts/nvm_cosim.json`. Log: `at-d0203aac/logs/nvm_cosim.log`, SHA-256 `0ac2f14c…`.
- Round-3 commit `26a26e1f` added the admission flag and the patch-0006 marker call in `nvm_boot()`. `93262f25` stubbed the marker in the builder's gate-35 fixture (`test_builder.py:26647`, `:26668`), and `sw/firmware/nvm_hosttest/nvm_host.c:67-72` has it. `tb/verilator/nvm_cosim/cosim_host.c`, the host that `run_cases.py:267` compiles into `host.o`, did not.
- At `1f039cfe` the statics refusal exits before any build and so hid the link failure; the failure predates the merge.
- A scratch probe (`$VALIDATION_STORAGE/590-a430/probe/`, the harness copied with only `cosim_host.c` changed; `logs/probe-cosim-host.diff`, SHA-256 `0c104fd4…`) returned rc 0: 465/465 checks, 39/39 mutants (`logs/probe-nvm_cosim.log`, SHA-256 `cfa2cdf0…`; `restart-cases.json`, `probe-evidence/`).

## Cosim-host stub (disposition (a))

**Commit `4c2a30de`** adds the probe's exact stub, a declaration and an empty definition mirroring `sw/firmware/nvm_hosttest/nvm_host.c:67-72`, and nothing else (`logs/cosim-host-stub.diff`, SHA-256 `3572ed22…`):

```diff
diff --git a/tb/verilator/nvm_cosim/cosim_host.c b/tb/verilator/nvm_cosim/cosim_host.c
index d3427c43d..2afa3c6af 100644
--- a/tb/verilator/nvm_cosim/cosim_host.c
+++ b/tb/verilator/nvm_cosim/cosim_host.c
@@ -62,6 +62,12 @@ extern cmd_handler const nvm_host_cmd_milan_nvm;
 extern cmd_handler const nvm_host_cmd_milan_status;
 
 void set_idle_hook(void (*fptr)(void));
+void bios_dispatch_hook_required(void);
+
+/* The host replaces the BIOS, including its patch-0006 link marker. */
+void bios_dispatch_hook_required(void)
+{
+}
 unsigned int crc32(const unsigned char *buffer, unsigned int len);
 
 struct flash_model {
```

- The six added lines equal the added lines of the probe diff, and the committed file is byte-identical to the probe's copy (SHA-256 `2eaf4038…` for both).
- `git diff --check` is clean. `git diff --stat b5c0f69d HEAD -- tb/verilator/nvm_cosim` lists only `cosim_host.c` (+6) and `run_cases.py` (+1/-1): this PR's only `nvm_cosim` changes against dev are the two fixture commits.

## Full `nvm_cosim` suite at `4c2a30de`

`make -C tb/verilator/nvm_cosim` (target `run`: `run_cases.py --shapes 1x1,8x8 --jobs 8 --pool 8`), with the pinned tool wrappers of the manager's r4 bank (Verilator 5.050; the pinned Markdown environment's Python): **rc 0 in 350.2 s**, worktree clean and HEAD unchanged after (`receipts/nvm_cosim-4c2a30de.json`; `logs/nvm_cosim-4c2a30de.log`, SHA-256 `3267d73c…`). `run_cases.py` removes each build directory before it builds, so nothing from the failed `d0203aac` run was reused.

- `building 42 build(s)`: `contract-1x1`, `contract-8x8`, `idw2-1x1` and the 39 mutant builds.
- `[contract-1x1] 62 case run(s): 315 ok, 0 bad, 0 not expressible`; `[contract-8x8] 27 case run(s): 150 ok, 0 bad, 0 not expressible`.
- Identity wrap: A4, A9, B1, C8 (+3 committing changes each) and C2 at `CAP_ID_W_P=2` give "the same report as at 16"; "5 acknowledgement(s) quoted the capture identity 0"; "identity control: a 2-bit identity aliases on A8 as required".
- `39 of 39 mutant(s) killed by their named check`; `nvm_cosim: 465 checks: 465 PASS, 0 FAIL (0 not expressible)`; `RESULT: PASS`.

**Every case run** (directory names under the git-ignored `runs/`; SHA-256 of each stdout in `restart-cases-4c2a30de.json` → `case_runs`):
- `contract-1x1`, 62: A1, A2, A3, A4, A5, A6, A8, A9, A11, A12; B1, B2, B3, B4, B5, B6, B6b, B7, B8, B9, B10; C1, C1a, C1g, C1r, C2, C2e, C2r, C3, C5, C7, C8; D1, D4c, D4d, D4e; E1, E3; F2, F3; R1 and `R_power_cycle` after B1, B2, B4 and B9; U1 to U13; W1 to W4. Plus the five 16-bit `~wrap` references (A4, A9, B1, C2, C8).
- `contract-8x8`, 27: A1, A2, A3; B1, B2, B5, B6, B9; C1, C2; D1; E1; R1 and `R_power_cycle` after B1, B2 and B9; U4, U5, U6, U7, U9, U11, U12, U13; W2, W3, W4.
- `idw2-1x1`, 6: A4, A8, A9, B1, C2 and C8 at 2 identity bits.

**Every mutant and the named check that killed it** (verbatim from the log):

| Mutant | Killed by | Mutant | Killed by |
| --- | --- | --- | --- |
| A01_composite_durable_bit | `pending_drives_no_commit@end` | M08_attestation_ignores_grant | `last_verified_kept@after:0x21` |
| F01_attestation_not_checked | `last_verified_kept@after:0x21` | M09_second_arm_accepted | `concurrent_arm_refused@stray` |
| F02_copies_open_records | `last_verified_kept@end:0x20` | M10_release_forgets_work | `later_record_persists@after:0x20` |
| F03_prefill_from_blank | `last_verified_kept@end:0x20` | M11_dirty_from_accepted_bytes | `converged@end` |
| F04_ack_without_identity | `stable_no_churn` | M12_alarm_not_revoking | `alarm_revokes@end` |
| F05_device_busy_gate_kept | `later_record_persists@abandoned:0x20` | M13_report_not_revoking | `failure_revokes` |
| F06_ack_after_failed_slot | `converged@end` | M14_pending_bit_misses_producer | `no_durable_claim_unmaterialized@end` |
| F07_reload_refusal_ignored | `converged@end` | M15_pending_bit_misses_open_record | `no_durable_claim@gap` |
| F08_restart_reloads_window | `converged@end` | M17_hold_expiry_voids_capture | `slow_copy_attests` |
| F10_retired_writer_keeps_heartbeating | `writer_absent_when_retired@end` | M18_pending_bit_stuck | `converged@end` |
| F11_restart_reattaches_without_load | `restart_stays_retired_without_load@restarted` | M19_arm_edge_grant_not_deferred | `arm_edge_request_deferred:0x20` |
| F12_repeat_ignores_window_live | `window_live_stops_the_repeat@boot` | M20_arm_accepted_while_request_deferred | `hold_bounded_across_captures:0x21` |
| G01_edge_detected_change | `no_durable_claim_unmaterialized@end` | R01_reload_ignores_inflight | `reload_refused_inflight_at_rebase@after:0x20` |
| M01_open_at_erase_completion | `last_verified_kept@end:0x20` | R02_reload_ignores_grant_since_rebase | `last_verified_kept@end:0x20` |
| M02_close_on_any_completion | `never_torn_or_erased@after:0x21` | R03_reload_not_once_per_reset | `held_work_survives_post_boot_reload@reload` |
| M03_close_on_partial_write | `later_record_persists@end:0x21` | R04_rebase_wins_over_same_edge_grant | `grant_wins_over_rebase_edge@after:0x20` |
| M04_ack_ignores_identity | `stale_identity_refused@stray` | R05_boot_load_stays_pending_when_live | `boot_load_closed_when_live@boot` |
| M05_ack_retires_live_work | `ack_retires_only_slot@post_ack:0x20` | R06_revision_b_load_rule | `change_landed_or_reported@end:0x21` |
| M06_hold_does_not_defer | `deferred_until_attestation:0x21` | R07_arm_without_accepted_load | `arm_refused_without_accepted_load@stray` |
| M07_hold_never_expires | `hold_bounded:0x21` | | |

**Same result as the probe.** The log equals the probe's line for line except make's two entry lines and one leaving line (the probe ran `run_cases.py` directly) and the root path. All 207 case-run stdouts (contract, identity-wrap and mutant builds) exist in both trees: 21 are byte-identical and the other 186 differ only in the host's DDR-buffer address printed as `at 0x…` / `-> 0x…`, which moves with address-space randomisation; after replacing those addresses, 0 differ (`extract_restart_cases_head.py`, `logs/extract_restart_cases_head.out`).

### nvm_cosim case table: which cases restart the writer

Four cases call `nvm_host_writer_restart()` (`cosim_cases.cpp:1078-1240`). W4 runs W3 and then rewrites records. `restart-cases-4c2a30de.json` (SHA-256 `5997bde7…`) holds every restart-case run at this head, 35 in all: 7 on contract builds and 28 on mutant builds (W1 on F08; W2, W3 and W4 on F04, F07, F10, F11, F12, M18, R02, R05 and R06). The contract builds' raw stdout is in `head-evidence/`.

| Case | Builds | Writer before restart | After restart | Heartbeats (`hb`) and backing | Checks |
| --- | --- | --- | --- | --- | --- |
| W1 `writer_restart_reattaches` | contract 1x1 | live, committed seq 1, change X2 pending | "writer restarted on a live backend; re-attached, the window is not reloaded" | `hb` 1 at boot (30 ms), 9 at base (2,230 ms), 12 at restart (2,830 ms), 24 at `end` (5,830 ms); `backed=1`, `stale=0` throughout; seq 2 committed to slot B | `restart_reattaches@restarted`, `no_durable_claim@restarted`, `converged@end`: pass. Named mutant F08 killed by `converged@end`. |
| W2 `restart_after_refused_loads` | contract 1x1, 8x8 | disabled: 4 window loads refused | "no window load was accepted in this boot; the writer stays retired until the next reset" | `hb` 0 and `backed=0` at `boot`, `live`, `restarted` and `end` (6,000 ms later) | pass. Named mutants F11 (`restart_stays_retired_without_load@restarted`) and R06 (`change_landed_or_reported@end:0x21`) killed. |
| W3 `write_across_refused_fill_then_restart` | contract 1x1, 8x8 | disabled: 4 loads refused, then window live | stays retired (same line) | `hb` 0, `backed=0` throughout | pass |
| W4 `all_records_rewritten_after_refused_fill` | contract 1x1, 8x8 | as W3 | stays retired | `hb` 0, `backed=0` through `end2` at 9,067 ms (1x1) and 9,153 ms (8x8) | pass |

**`nvm_boot()` re-arms `nvm_started` after the modelled restart.**
- W1 shows it. The modelled restart sets `nvm_started = 0` before calling `nvm_boot()`.
- The firmware's only heartbeat write, `milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_HB)` at `:936`, sits behind `if (!nvm_started) return;` at `:926-927`.
- Twelve heartbeats follow the restart, and `backed` stays 1 for 3,000 ms, longer than the 2,000 ms T-NVM-WRITER-ALIVE. That can happen only if `nvm_boot()` set `nvm_started` again (`:1449`), after the shape check passed. Without the re-arm, backing would lapse and `converged@end` would fail.
- In W2 to W4 the restarted writer is admitted but retired, so the retired-writer rule keeps `hb` at 0. That is these cases' expected result, and it is not evidence either way about `nvm_started`.

## Stale-statement search (assignment item 3)

Result: nothing in the merged tree is falsified by this PR beyond what the previous merge-dev round already reworded or examined. **No stale-statement commit was made.**

Searches at `d0203aac`, excluding `protocol-processor/`, `docs/history/`, other submodules, JSON receipts and the harness's ignored `build/`:

1. The whole tree: `rg -n '#59[029]\b|issues/59[029]\b'`. The hits are the previous round's reviewed set:
   - this PR's own text in `BAREMETAL_FIRMWARE.md:1979`, `BOARD_PORTING_AX7101.md:110`, `397_SERVICE_BUDGET.md:3-9`, the findings index row, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1612`, `REGISTER_MAP.md:418`, `MILAN_COMPLIANCE_MATRIX.md:192` and `tb/verilator/fw_service_budget/README.md:7`;
   - the dated bench record `394_387_E1_SWITCH_CYCLES.md:191,286,302`, which describes the measured `9e9954e9` image and was left unchanged last round.
2. Only the lines dev added since the previous merge base (`git diff -U0 7a7582f0 b5c0f69d`, 2,224 added lines), searched with `link_status|MAC_STATUS|LINK_UP|LINK_DOWN|mdio|unwritten|never writ|nothing .*writes|no publisher|queued (console )?input|dispatch|idle hook|idle_hook|byte[- ]copy|word[- ](wide|copy)|24\.30246|25\.54|capture (copy|headroom)|#590|#592|#599|nvm_heartbeat_tick|service[- ]budget|#397|nvm_started|heartbeat|straps|until a driver|firmware`.
   - Five hits. They concern the AEM image copy and CRC binding (#595) and the timing script, which "never writes a checkpoint or bitstream". None concerns dispatch, heartbeat, capture copy or MDIO publication.
   - Text outside dev's delta was searched by the previous round at `1f039cfe` and is unchanged since.
3. `COMMERCIAL_TIMING_395.md` (dev's new page): `firmware|mdio|cpu|service|heartbeat|console|capture` gives no hit.
4. The restart-model commit: `WRITER_STATICS|writer statics|restart model|nvm_host_writer_restart|file-scope (state|variable)`.
   - No document lists the modelled statics by name.
   - `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:746,1737` say the model returns "every file-scope variable of the writer to its initial value". The commit makes that true again.
5. `REQUIREMENTS.md:352` ("The manager ratifies it using #397 and #75 measurements") was read. It describes a future ratification and is not falsified.

Added at `4c2a30de` for the stub commit:

6. `bios_dispatch_hook_required|cosim_host|patch-0006 (link )?marker` and `(link|dispatch)[- ]marker|marker (symbol|call)|host (fixture|harness)e?s? (stub|suppl|provid)|stubs? the marker` (case-insensitive) over the same tree.
   - No document says the `nvm_cosim` host lacks the marker or that the suite fails.
   - `tb/verilator/nvm_cosim/README.md:50,192` and `run_cases.py:18` describe what `cosim_host.c` models (the flash, the DDR window, the clock and `PP_STAT`). They stay true: the stub is an empty link symbol, not a model.
   - `sw/litex/patches/README.md:18`, `397_SERVICE_BUDGET.md:192`, `BAREMETAL_FIRMWARE.md:1903` and `sw/firmware/nvm_hosttest/README.md:111` describe the marker's purpose and stay true.
7. Suite size statements: `465 checks`, `39 mutants` and similar.
   - `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1243` ("465 checks over 89 case runs") and `:1757` (39 mutants) match this run.
   - **Residual, not this PR's:** `tb/verilator/README.md:71` still says `nvm_cosim` grades "469 checks over 90 case runs". Commit `cc251d68` (2026-09-20) wrote that line, and `26482899` the same day made E3 an ordinary case and the suite 465 checks (`CHANGELOG.md:302-304`). The line is identical at `7a7582f0` and at dev `b5c0f69d`. This PR's two `nvm_cosim` commits change no case or check count (the probe at `d0203aac` plus stub and this head give the same 465 over 89). So it was stale on dev before this lane, and the assignment's item 3 does not cover it. It is reported here for a separate issue; no edit was made.

The previous round's residuals stand as recorded there: `nvm_capture_cpu/sim_main.cpp:42` "byte copy", `litex_pins.txt:30` "six patches" and `milan_datapath.sv:2077`.

## Gate table at `4c2a30de`

Every gate ran at `4c2a30debb031595b81c5c4bfc53b601a0fec528` on the physical `$LANES/590-592-599-firmware` path.
- Output went to log files and was never piped.
- The worktree was clean before and after every runner, and HEAD was unchanged.
- The processor checkout was `c951a9ff`.
- Long runs were started detached, and the session waited on each in the foreground until it exited. Nothing was left running.

**No receipt from `d0203aac` is reused.** The stub cannot reach the builder bank (`test_builder.py` reads no `tb/verilator/nvm_cosim` file; its gate-35 fixture has its own marker stub) or the service harness (`fw_service_budget/run.py:158-179` binds no `nvm_cosim` file). Every gate was re-run anyway, so no argument rests on that. The `d0203aac` receipts and logs are kept under `at-d0203aac/` for comparison.

Receipts:
- `receipts/nvm_cosim-4c2a30de.json` (`run_long.py`);
- `gates.json` (`run_gates.py`);
- `builder-gates.json` (`run_builder.py`, which runs `full-builder-absent.py`, SHA-256 identical to the previous round's copy);
- `probes.json` (`run_probes.py`, `product_link_guard.py`);
- `native-commands.json`, `native-artifacts.json`, `native-regrades.json` and `previous-comparison.json` (see the next section).

Diff-based gates use the merge's dev parent `b5c0f69d` as base (assignment item 4); it is `git merge-base HEAD origin/dev`. Markdown and source gates ran under the pinned Markdown environment (`$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3`). The builder ran under the LiteX environment of the previous rounds.

| Gate | Command | rc | Seconds | Notes |
| --- | --- | --- | --- | --- |
| **`nvm_cosim` full suite** | `make -C tb/verilator/nvm_cosim`, r4 pinned wrappers | **0** | 350 | 465/465 checks, 39/39 mutants by their named check, `RESULT: PASS` (see above). At `d0203aac` this was rc 2 (host link). |
| Full builder bank, compiler present, with firmware census | `sw/builder/test_builder.py --require-elaboration --require-rv32` | 0 | 1,011 | `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11 calibration, report absent, as in every earlier round. Dev's gate 36b, `[timing grade]` and `[clock contract]` checks and the gate-35 host link pass. Log `logs/builder-present-with-firmware-census.log`, SHA-256 `2bb33eec…`. |
| Full builder bank, compilers absent | `full-builder-absent.py` | 0 | 690 | `EXCEPT 2 NOT RUN`, as before; `FULL BUILDER ABSENT PASS`. Log `logs/builder-absent.log`, SHA-256 `5099b5dd…`. |
| Host firmware self-test | `sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 68 | 5 shapes. Disabled-writer, link-guard and PHY mutants are caught. The two `FAIL` lines are the planted admission-guard mutant. |
| Capture receipt | `scripts/check_nvm_capture.py` | 0 | 0.7 | log SHA-256 `9a4196c7…`, as in both earlier rounds |
| Kept native capture oracles | round-3 `verify_packet.py`, read-only | 0 | 0.1 | 135 artifacts, 96 captures, byte-only control |
| #397 harness, portable | `tb/verilator/fw_service_budget/run.py --self-test` | 0 | 0.6 | 47 grading checks |
| CI scope | `scripts/ci_scope.py --selftest` | 0 | 2.6 | |
| Docs gates | `docs_check`, `check_doc_paths`, `check_doc_style`, `check_archive`, `gen_toc --check`, `check_em_dash --base b5c0f69d` | 0 | ≤ 4.5 each | em-dash: 0 findings over 555 added lines in 11 pages, `[b5c0f69d..HEAD]` |
| Source checks | `check_feature_status --self-test`, `pp_srcs --check`, `check_baremetal_only --check`, `check_entity_shape --self-test`, `check_py_idiom`, `check_cpp_idiom`, `check_hygiene --check`, `measure_test_evidence --check` | 0 | ≤ 42 each | `check_cpp_idiom` covers `cosim_host.c` (`check_cpp_idiom.py:166`): 162 units, every count 0 |
| Whitespace | `git diff --check b5c0f69d` | 0 | 0.04 | |
| Reviewer probes, unchanged | phase, disabled writer, built-in oracle, `edge-cross` (expected raw rc 1), product link guard | 0 (graded) | ≤ 36 each | see the note below |

**Byte identity with `d0203aac`.** All 20 `gates.json` logs and all seven probe and link-guard logs are byte-identical to the `d0203aac` logs. The two builder logs differ only in random temporary-directory names (two lines in each) and in elapsed-seconds figures (one line in the compiler-present log, two in the compilers-absent log).

**One probe run was repeated, and why.**
- The first probe run at this head graded `phase-probe` 1: `host build failed … undefined reference to 'milan_mac_phy_mdio_w_write'` (`probes-stale-workdir.json`, `logs/probe-phase-probe-stale-workdir.log`, `logs/run_probes-stale-workdir.out`).
- Cause: the probe reused the previous session's scratch work directory. After its own `make_bench`, the probe writes `<work>/generated/csr.h` with `#define CSR_MILAN_MAC_PHY_MDIO_W_ADDR 1` (`probe_mdio_phase.py`). That file, dated 00:25 from the `d0203aac` run, was still there. `compile_bench` (`test_nvm_firmware.py:206-207`) searches `-I<work>` before the stub directory. So the next `make_bench` compiled the firmware's MDIO path against the probe's header, and `nvm_host.c` does not define those accessors.
- The work directory was moved aside to `$VALIDATION_STORAGE/590-a430/at-d0203aac/probes-reused/`, and `run_probes.py` was run again unchanged into a fresh one. All five graded 0, and every log is byte-identical to the `d0203aac` run, which also had a fresh directory.
- The committed tree plays no part in this. `cosim_host.c` is not compiled by any probe.

## Native service and capture comparison

**Why it was re-run.** The merge moves inputs that the service builds bind and that the capture harness compiles:
- dev's #602 RTL, `hdl/ieee1722/avtp/KL_media_clock_restart.sv` and `hdl/milan/milan_datapath.sv`;
- the processor re-pin `16be6768` → `c951a9ff` (dev `e8bf5e08`), of which five bound sources change: `hdl/acmp/KL_acmp_talker.sv` and `hdl/srp/KL_srp_{encoder,listener_fsm,talker_fsm,top}.sv`;
- `sw/litex/milan_soc.py` (#595).

The service harness therefore refuses the previous round's logs as stale, as designed, and every arm was run fresh at `4c2a30de`. The stub commit changes no input of either harness.

**Runner.** `run_native.py` is the previous round's runner with four changes plus its docstring, shown by `diff` against that copy: the scratch directory (`$VALIDATION_STORAGE/590-a430/native/`, fresh), the expected head, the expected processor pin, and the CPU set, `taskset -c 40-63` (this lane's affinity) instead of `32-63`. `regrade_native.py` differs from the previous round's only in its scratch path; `verify_packet.py` and `audit_rerun.py` are unchanged copies. The CPU set changes wall time only. `run_capture_native.py` is byte-identical to the previous round's (and round 3's).
- Arguments, environment and STOP conditions are round 3's: an 8x8 capture over 24.5 ms, or an MDIO charge over 50 ms.
- 25 arms: 12 positive service plans, target `late-sample`, `remove-dispatch` on `queued-builtins` and `queued-short`, the `no-publish` control, six capture arms, and the `byte-only`, `skip-copy` and `no-traffic` capture controls.
- 65 commands, all rc 0, all at `4c2a30de`: 25 builds, 25 measurements and 15 immediate regrades (`native-commands.json`). Wall time 00:31 to 02:18 CEST (about 6,420 s); command time totals 49,570 s. No STOP condition occurred (`logs/run_native.out`).
- `native-evidence/` holds 138 artifacts: every build log, run log, raw log, receipt and spec. Each is bound by raw and stored SHA-256 and size in `native-artifacts.json`, and gzip-compressed above 200 KB. No binary was copied.

| Step | Command | rc | Result |
| --- | --- | --- | --- |
| Native arms | `run_native.py` | 0 | `ALL NATIVE MEASUREMENTS COMPLETE: 25 arms at 4c2a30de…` |
| All 15 service runs regraded from the retained bytes | `regrade_native.py` | 0 each | `PASS: all 15 retained service runs regraded at 4c2a30de…` (`native-regrades.json`, `logs/final-regrade-*.log`). Every restored log and receipt matched the build's copy. All 15 regrade logs are byte-identical to the previous round's. |
| Retained capture oracles | `verify_packet.py` (this packet's copy, unchanged) | 0 | `PASS: 138 retained native artifacts; 96 captures match the committed receipt; byte-only control` |
| Comparison with the previous round | `compare_previous.py` → `previous-comparison.json` | 0 | below (`logs/compare_previous.out`) |
| Build delta, `service-1x1-all` | `build_delta.py` | 0 | `logs/build-delta-service-1x1-all.log` |
| Packet audit | `audit_rerun.py` → `audit-rerun.json` | 0 | 138 artifacts, 65 commands and 15 regrades re-hashed; one head; no file over 200 KB |
| Capture receipt | `scripts/check_nvm_capture.py` (gate table) | 0 | log SHA-256 `9a4196c7…`, unchanged |

### Result: byte-identical to the previous round, hence to round 3

The baseline is the previous merge-dev round's packet (`590-a422`, run at `1f039cfe` with the processor at `16be6768`). Its native evidence was byte-identical to round 3's. `compare_previous.py` rebuilds both packets from their stored artifacts, checking every stored and raw SHA-256.

- **Service.** All 16 raw simulation logs (the 15 runs and `no-publish`) are byte-identical. In all 15 receipts every graded field is identical: rows, events, heartbeat, liveness, PHY statistics and findings. `no-publish` writes no receipt, by design. Spec fields are identical once build paths are normalised.
- **Capture.** All nine raw capture logs and all eight measurement JSONs are byte-identical: six arms plus the `byte-only` and `no-traffic` controls; `skip-copy` writes none. The source and include lists, 118 sources in each arm, are identical after path normalisation, and they include the seven changed RTL sources. For all six arms, every receipt-bound identity equals the committed receipt, as does every graded field. The identities are the CPU netlist, instrumented firmware, BIOS, gPTP microcode and configuration.
- **Bound hashes.** Every one of the 15 service receipts moves in the same 15 build-hash keys:
  - eight repository inputs, all in the change set `1f039cfe..4c2a30de`: the two #602 RTL files, the five processor sources and `milan_soc.py`. `moved_repository_inputs_outside_change_set` is empty for every run.
  - seven generated files: `sim.v`, `Vsim`, `bios.elf`, `csr.h`, `git.h`, `mem.h` and `soc.h`.

  Among the measurement-input hashes, only `milan_soc.py` moves.
- **Generated files** (`logs/build-delta-service-1x1-all.log`, previous round's `service-1x1-all` build against this one):
  - `csr.h`, `soc.h`, `mem.h`, `git.h` and `sim.v` differ only in LiteX timestamp lines.
  - `sdram_phy.h`, both `adp_shape_defaults.svh` copies, `bios.bin`, `aem_desc.bin` and the three `sim_*.init` files are identical.
  - `bios.elf` differs only in DWARF: after `objcopy --strip-debug` the two are byte-identical.
  - So the #595 `milan_soc.py` change does not alter the simulated SoC. The changed RTL is elaborated, since its hashes are bound, and the simulation output does not move.

**Artifact identity against the dev parent (assignment item 4).**
- Each service receipt binds 134 tracked repository build inputs, and each equals the file at `4c2a30de`. Of those:
  - 126 equal dev parent `b5c0f69d`'s copy, which includes every file dev changed.
  - The other 8 are this PR's own files. Five are changed: `milan_baremetal.c`, `fw_service_budget/build.py`, `fw_service_budget/sim_main.cpp`, `nvm_capture_cpu/firmware.py` and `nvm_capture_cpu/run.py`. Three are added: `0006-bios-dispatch-hook.patch`, `fw_service_budget/phy.hpp` and `phy.py`.
- Of the 22 measurement inputs, 13 equal dev's copy. The other 9 are the same PR-owned files plus `fw_service_budget/run.py`.
- Every one of these PR-owned paths is in `git diff --name-only b5c0f69d HEAD`.
- The three `external/` CPU-netlist entries are generated and untracked. Their hashes did not move.

**Figures at `4c2a30de`, equal to the previous round's and round 3's.** Every graded field is identical, so round 3's derived figures stand.

| Shape | CPU MHz | Traffic | Minimum to maximum ms, 16 captures | 49 ms floor ratio |
| --- | --- | --- | --- | --- |
| 1x1 | 50 | on | 3.87674 to 3.88779 | 12.6036x |
| 1x1 | 50 | off | 3.82856 to 3.84214 | 12.7533x |
| 8x8 | 50 | on | 13.21274 to 13.23352 | 3.7027x |
| 8x8 | 50 | off | 13.04976 to 13.06923 | 3.7493x |
| 8x8 | 100 comparison | on | 9.94138 to 9.95464 | 4.9223x |
| 8x8 | 100 comparison | off | 9.93764 to 9.94094 | 4.9291x |

- Controls: `byte-only` 24.30446 ms maximum, 1.83648x against the 1.5x bound; `skip-copy` and `no-traffic` caught by their named oracles.
- Service: all twelve positive plans pass with `budget findings: 0` and zero service findings. The largest heartbeat gap is 322.47884 ms; the largest MDIO transaction 0.12457 ms; the largest complete poll 0.83375 ms.
- `remove-dispatch` gives 1051 per-line findings on `queued-builtins` and 350 on `queued-short`. Target `late-sample` gives "PHY initial gigabit negotiation was not published", and `no-publish` "missing publication caught by target simulation".
- These equal `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and section 20 item 6, the committed capture receipt and the #397 findings page, so no figure needs an edit.

Receipts (SHA-256 prefix): `native-commands.json` `8adf8a0a…`, `native-artifacts.json` `c44d457e…`, `native-regrades.json` `2fcccca7…`, `previous-comparison.json` `7e812287…`, `audit-rerun.json` `9641ec2e…`. Gate receipts: `receipts/nvm_cosim-4c2a30de.json` `e5f8e694…`, `restart-cases-4c2a30de.json` `5997bde7…`, `gates.json` `646bbaed…`, `builder-gates.json` `d864db5d…`, `probes.json` `8333f673…`.

## Open points

- **Measured-commit and processor-pin lines.**
  - What they say: `397_SERVICE_BUDGET.md:37-41` and `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1613-1616` name the measured commit `26a26e1f` and the processor pin `16be6768`. The committed capture receipt binds `processor_pins` `16be6768` as provenance.
  - Why they are left: they record what was measured, and `check_nvm_capture` does not compare the pin with the tree. The re-run at `c951a9ff` reproduces every figure byte for byte. So, as with the previous round's measured-commit open point, they are not falsified by this PR, and no edit was made.
  - If the pages should name the merge-head reproduction or the new pin, that is a docs-only change for a later ruling.
- **`tb/verilator/README.md:71`** says `nvm_cosim` grades 469 checks over 90 case runs; the suite grades 465 over 89. The statement was stale on dev before this lane (see "Stale-statement search"), so it needs its own issue.
- **Dev has advanced.**
  - The remote-tracking `origin/dev` now reads `eaa88a32eb77adeba9c1c631198c7fb516a11095`: PR #615 (#607), the first PR in the stated merge train. A fetch outside this session moved it at 01:39 CEST; this session ran no fetch.
  - It changes 12 files (`logs/dev-advance-files.txt`), including `sw/builder/test_builder.py` and `sw/litex/milan_soc.py`. The service builds bind `milan_soc.py`. The processor pin is still `c951a9ff`.
  - `git merge-tree --write-tree HEAD origin/dev` is clean, tree `b5038a41dbf936219243f246a7bc324aa384512b` (`logs/merge-tree-eaa88a32.txt`). No merge was made: the assignment puts the candidate stack and composition review after this round.

## Delivery

- Commits `9f94b246` (merge), `d0203aac` (restart model) and `4c2a30de` (cosim-host stub) are local only. Nothing was pushed, and no PR was created, edited or merged.
- No stale-statement commit was needed.
- No RTL, firmware, builder, processor or configuration edit. The branch changes are the conflict resolution, the one-line restart-model commit and the six-line cosim-host stub commit.
- Repository state changed outside the branch:
  - the protocol-processor checkout, now at `c951a9ff`;
  - the `origin/dev` remote-tracking ref: moved to `b5c0f69d` by this round's first-session read-only fetch, then to `eaa88a32` by a fetch outside this session.
- The checkout's git-ignored `tb/verilator/nvm_cosim/build/` and `runs/` hold the `4c2a30de` suite run. The other git-ignored builder outputs are `sw/builder/out/`, `configs/generated/` and `__pycache__/`.
- Scratch outputs outside this packet (`$VALIDATION_STORAGE/590-a430/`):
  - `native/`: the 25 native builds, about 7 GB, not copied;
  - `delta/`: normalised build-delta copies;
  - `logs/`: the suite logs;
  - `builder-*.log`: this head's builder logs, also stored in `logs/`;
  - `probe/`: the first session's scratch probe tree;
  - `at-d0203aac/`: the first session's builder logs and the reused probe work directory;
  - `pinned-tool-bin/`: the tool wrappers;
  - `HANDOFF.stop-session.md`: the STOP session's handoff, for reference.
- Read-only inputs:
  - the previous round's packet (`590-a422`) and its `native/` builds;
  - the round-3 packet (`590-a411`: `verify_packet.py`) and its BIOS objects for the link-guard replay;
  - the reviewers' probe packets.
- Packet files:
  - runners: `run_long.py`, `run_gates.py`, `run_builder.py`, `run_probes.py`, `run_native.py`, `run_capture_native.py`, `regrade_native.py`;
  - checks: `verify_packet.py`, `audit_rerun.py`, `compare_previous.py`, `build_delta.py`, `product_link_guard.py`, `full-builder-absent.py`;
  - extraction: `extract_restart_cases.py`, which reads the probe, and `extract_restart_cases_head.py`, which reads this head's run;
  - receipts: the JSON receipts;
  - evidence directories: `native-evidence/`, `head-evidence/`, `probe-evidence/`, `receipts/`, `logs/`, and `at-d0203aac/` (the `d0203aac` gate receipts and logs);
  - no file is over 200 KB.
- Public:
  - TAKEN https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5879363819 (`TAKEN.md`);
  - STOP https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5879875407 (`STOP.md`);
  - REVIEW READY https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5881242928 (`REVIEW-READY.md`).
