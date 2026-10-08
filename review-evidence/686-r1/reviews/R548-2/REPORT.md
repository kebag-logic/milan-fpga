[R548] NEGATIVE - exact head 48f12dc14099a3630a98eb07e9ec790695a72bfb

# R548-2 internal cleared-context review: issue #686 / PR #695, round 2

- Head `48f12dc14099a3630a98eb07e9ec790695a72bfb`, tree `7ed2f048f73734f671ae6eb5e1a008544fa0d0d0`. Source base `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`. Merged dev `291710b180ca9196780a6d17f2517957c9bcb89c`. Live dev at review time `99e4eb6c14462aafa84bb1ac597fd241abc1a240` (not merged here; manager candidate duty).
- Scope: delta `c7b69cd0..48f12dc1`, per assignment comment 6047563934 and REVIEW READY 6050832603. Part A covers `b2e786bb1`, `359c42da7` and `30fce4b0a`. Part B covers merge `e519e31f` and re-record `48f12dc1`.
- Reconstruction order: AGENTS.md and CONTRIBUTING.md, issue #686 body and its six comments, PR #695 body, the delta diff and history, then the published receipts at archive `84add8ed`. Prior public findings (R548-1, R549-1) were read only after my verdict and ledger draft were written to this file.
- No private author material was read, and no concurrent reviewer report. The archive's author narrative (HANDOFF.md) was not read before the verdict.

The verdict is NEGATIVE on one MINOR finding, R548-2-F1 (Conformance, Docs). The RTL fix and the guard check are sound. Every prior finding is resolved at this head. All three resource records regenerate exactly from the published receipts through the head's own gate.

## Findings

### R548-2-F1 - MINOR - Conformance, Docs - the shipping engine is not seeded from the station MAC

**Where:**
- `docs/design/MAAP_FABRIC.md:91-95`: "Both draws come from a free-running 16-bit LFSR seeded from the station MAC ... So the draws are random for every station MAC."
- `docs/design/MAAP_FABRIC.md:129-132`: the B.3.6.1 deviation record, "`KL_maap` uses a 16-bit LFSR seeded from the station MAC alone".
- `docs/design/MAAP_FABRIC.md:167`, under Fabric integration: "Randomness: LFSR seeded from station MAC".

**Evidence:**
- `KL_maap` loads `lfsr_r` only in its reset branch (`hdl/ieee1722/maap/KL_maap.sv:286-292`), from `station_mac_i`.
- In the shipping integration that reset is `axis_resetn` (`hdl/milan/milan_datapath.sv:7066`). `station_mac_i` is `cfg_mac_addr` (`:7069-7071`), the output of `milan_csr` (`:2491`). `milan_csr` sits on the same `axis_resetn` (`:2465-2466`).
- `milan_csr`'s reset branch clears `mac_alo` and `mac_ahi` to 0 (`hdl/common/csr/milan_csr.sv:1553-1556`). Firmware writes the station MAC only after boot (for example `sw/firmware/milan_baremetal/milan_baremetal.c:1591-1592`).
- So whenever the engine's LFSR is seeded, its MAC input is the CSR reset value 0. The seed is `0xACE1 ^ 0 ^ 0 = 0xACE1` on every shipping station, whatever its MAC. Any reset that reseeds the LFSR also clears the MAC registers, so no reset sequence avoids this.
- The station MAC never enters the timer or offset draws in the shipped engine. Draws differ between stations only through the cycle on which each station's enable and sends happen.
- The behaviour predates this PR. The text is new in this PR: `:129-132` came in round 1 and `:91-95` in round 2, answering the zero-seed finding. Neither prior round raised it.

**Impact:**
- The round-2 zero-seed fix is correct for the module and its port contract (see Ledger: RTL), but the zero-fold case cannot occur through `milan_datapath`.
- More important, the B.3.6.1 deviation recorded for the follow-up decision understates it. The shipped engine is not "seeded from the station MAC alone": every station uses the same constant seed. The follow-up decision would be taken on an incorrect description of what ships.
- This is not RESIDUE: correcting it changes a clause deviation claim (B.3.6.1) and a randomness claim tied to item 2 (B.3.4).

**Required outcome:**
- `MAAP_FABRIC.md` states, at `:91-95`, `:129-132` and `:167`, what the shipped engine does. In the `milan_datapath` integration the LFSR seed is sampled during `axis_resetn`, when MAC_ADDR_LO/HI are themselves 0. So every shipping station seeds `0xACE1`, and the station MAC does not enter the draws.
- The module-level statements may stay as module-level statements (seeded from `station_mac_i` at reset).
- The follow-up list carries the seed-timing gap with the B.3.6.1 item: seeding before the MAC is programmed.
- No RTL change is required for #686. Changing when the seed is taken is a follow-up decision.

**Verification:** read the corrected text against `KL_maap.sv:286-292`, `milan_datapath.sv:2465-2466` and `:7066-7071`, and `milan_csr.sv:1553-1556`.

### R548-2-E1 - MINOR - Docs (evidence; owned by the manager's publication, not the head's tree) - receipt MANIFEST fails for four files

**Where:** archive `84add8ed571d376f8a1b39c3c6f71c4e80eed32a`, `review-evidence/686-r1/author-r2/resource-receipts/MANIFEST.sha256`.

**Evidence:**
- `sha256sum -c MANIFEST.sha256` fails for `r1-c7b69cd0/recipe/orchestration/{ooc,route}.sh` and `r2-48f12dc1/recipe/orchestration/{ooc,route}.sh`. The published hashes and the manifest hashes are in `receipts/archive_manifest_check.log`.
- The other 182 files verify, and every file is listed. The published scripts carry host placeholders and a `$VIVADO_LOCK` variable. Whether the originals differed only there cannot be checked from the archive.
- The publication note says only six Vivado logs (host line) and two gz inputs (re-encoding) were altered, and that the MANIFEST covers every file.

**Impact:**
- No record, figure or verdict depends on these four files. They are not record inputs, and the single-thread flow identity is proved by the executed Tcl and the records.
- But the archive's integrity claim is false for them, and a cold reviewer running the documented check gets four failures.

**Required outcome:** either restore the original bytes or re-hash the published bytes, and state the alteration in the archive's README as was done for the logs. No head change is needed.

**Verification:** `sha256sum -c MANIFEST.sha256` exits 0 in a fresh checkout of the archive.

### Suggestions (non-blocking; none affects coverage)

- **R548-2-S1 - SUGGESTION - Tests - the guard check grades one window of a frame on the wire.**
  - [6a] (`tb/verilator/maap/sim_main.cpp:419-441`) injects the PROBE after two beats have left, with `m_axis_tready` low.
  - Two narrower guard defects survive the suite (`receipts/probes.log`):
    - `!(tx_busy_r && tx_beat_r != 3'd0)`: a DEFEND may rewrite a frame that is requested but has no beat accepted yet. That violates AXI-Stream stability under backpressure.
    - `!(tx_busy_r && !m_axis_tready)`: a DEFEND may rewrite a frame while it streams.
  - The removal mutant asked for in round 1 is caught. Extending [6a] to inject at beat 0 under backpressure, and while the frame streams, would close both.
- **R548-2-S2 - SUGGESTION - Tests - the own-empty-range check runs in PROBE only.**
  - `sim_main.cpp:491-497` sets `count_i` 0 while the engine is in PROBE.
  - A defect that makes an empty own range conflict only in ANNOUNCE survives (`own_empty_range_conflicts_in_announce_only`). There it would send a DEFEND with conflict_count 0.
  - Repeating the check in ANNOUNCE, with `defends_o` unchanged, would grade it.
- **R548-1-S2 retained - SUGGESTION - Tests, Robustness - the truncated-PDU gate `rbeat_r >= 3'd5` (`KL_maap.sv:353`) has no check.** It is pre-existing and outside #686, and the PR body lists it for the follow-up.

No RESIDUE item is reported.

## Prior public findings at this head

| Finding | Status at `48f12dc1` | Evidence |
|---|---|---|
| R549-1-F1 = R548-1-F3 (MAJOR, manager ruling): a zero LFSR state for a MAC folding to `0xACE1` | **Resolved** | Reset seed `(mac_seed_w == 0) ? 0xACE1 : mac_seed_w` (`KL_maap.sv:149`, `:292`); `lfsr_r` is written only there and by the step (`:316`). Exhaustive model (`scripts/r548_2_lfsr.py`, `receipts/lfsr_model.log`): the seed is nonzero for all 65,536 folds and unchanged for every fold that was nonzero. The step has one 65,535-state cycle, so zero is unreachable. The draws span exactly 518..581 and 30488..31511 ms. `seed_offset_i` does not touch the LFSR. Harness [11] uses `02:00:00:00:AC:E1` (`sim_main.cpp:58`): 6 of 6 probe intervals and 3 of 3 announce intervals distinct, all strictly in bounds (`receipts/maap_run.log:172-179`). Both zero-seed mutants are caught (`receipts/maap_mutants.log:20-23`), and so are my `guard_compares_wrong_value` and `seed_forced_zero_always`. An equivalent fix with another constant passes, so the check does not pin the constant. `MAAP_FABRIC.md:85` is corrected, but see the new R548-2-F1 on the seed's source. |
| R548-1-F1: in-flight guard on the DEFEND path ungraded | **Resolved** as asked | [6a] (`sim_main.cpp:419-441`); mutant `defend_rewrites_the_frame_on_the_wire` is caught on "PROBE mid-frame: frame on the wire byte-identical". My `defend_guard_removed` is killed. Narrower windows: S1. No RTL change. |
| R548-1-F2: missed fourth PROBE misread | **Resolved** | `MAAP_FABRIC.md:135-140` states PROBEs one to three repeated, the fourth not repeated, the prober's probeCount! ANNOUNCE at once, and settlement by compare_MAC that can move this station. Consistent with Table B.7 probetimer!/probeCount! as frozen in the issue. |
| R549-1-F2 = R548-1-F4: all-fields snapshot claim | **Resolved** | R548-1-F4's text appears in the banner (`KL_maap.sv:222-228`), `MAAP_FABRIC.md:64-69` and the PR body ("requested_count and the source MAC follow `count_i` and `station_mac_i` ..."). |
| R549-1-F3 = R548-1-F5: unconditional pool claim | **Resolved** | `MAAP_FABRIC.md:50-52`; follow-up item `:142-144`; banner `KL_maap.sv:49-57`; `:280-281`; module page `KL_maap.md:5`, `:27`; PR body Known limitations. |
| R549-1-F4: no public receipts for the records | **Resolved** for the records at this head | Independent regeneration of all three, below. Round 1's records are superseded and were not regenerated in this round. Archive integrity: E1. |
| R548-1-S1 (own empty range) | Done; see S2 | `sim_main.cpp:491-497`, mutant `own_empty_range_conflicts` caught |
| R548-1-S3 (supporting labels) | Done | `mutants.py` `SUPPORTING = 0`, excluded from the item guard |
| R548-1-S4 (stale datapath comments) | Done | `milan_datapath.sv:267-286` |
| R548-1-S2 (truncated PDU) | Retained as SUGGESTION | Above |

## Part B: merge and re-record

- **Merge.** `e519e31f` has parents `30fce4b0a` (lane) and `291710b1` (dev), so it is a true `--no-ff` merge. `git merge-tree --write-tree 30fce4b0a 291710b18` reproduces exactly four conflicts: `AREA_BUDGET.md`, `234_PP_SHADOW_AREA_BASELINE.md`, `findings/README.md` and `pp_resource_baseline.json`.
  - The recorded merge differs from that mechanical merge only in those four files, and each of them equals dev's version.
  - The one auto-merged file both sides changed, `sw/firmware/ctrl/maap/README.md`, keeps both sides.
  - `git diff 291710b1 48f12dc1 -- hdl/milan/milan_datapath.sv` has no non-comment line.
- **Re-record.** `48f12dc1` changes only the baseline JSON and three docs. Against F, every tolerance, floor and ceiling is unchanged, and each endpoint's flow identity equals F's, `set_param synth.maxThreads 1` included (`receipts/baseline_policy_diff.log`).
- **Independent regeneration** (`scripts/r548_2_regen.py`, `receipts/regen_*.log`). I did not use the archive's regeneration script or its digest code.
  - Each endpoint's measurement directory was rebuilt from the receipts. The executed Tcl's placeholders were resolved to this clone (read only) and to the copied non-repository inputs.
  - The head's own `pp_resource_gate.record()` then recomputed identity, input digest (re-hashing every repository input from the head's files and pinned submodules), figures and scopes.

  | Endpoint | identity | inputs_sha256 | figures | scopes | equals receipt `record.json` | route status |
  |---|---|---|---|---|---|---|
  | route-1x1 | EQUAL | EQUAL `0c3280d1...` | EQUAL (50,391 LUT / 54,263 FF / 15,788 slices / 74 / 27 / 14, WNS +0.241, WHS +0.029) | EQUAL | yes | complete, 0 errors |
  | ooc-1x1 | EQUAL | EQUAL `9782839e...` | EQUAL (23,179 / 19,779) | EQUAL | yes | n/a |
  | ooc-8x8 | EQUAL | EQUAL `776f4f7f...` | EQUAL (30,135 / 27,380) | EQUAL | yes | n/a |

- **Gate checks** (`receipts/gate_checks.log`). `pp_resource_gate.py check` passes all three endpoints on the rebuilt directories, both against F (dev `291710b1`) and against the head record.
  - Route against F: LUT +434 (tolerance +500), FF -11, SLICE +54 (+80), RAM and DSP 0. WNS +0.241 against floor +0.03, WHS +0.029 against floor 0. Route complete.
  - `check-baseline` passes at the head.
- **Area text.** `AREA_BUDGET.md`'s figures match the route hierarchy report: `milan_datapath` 41,809, `pp_shadow` 23,081, `g_maap.maap_engine` 429 / 279. The arithmetic also checks: 79.48 %, 12,351 over, 62 slices free, 10,730 and 54 %, and a fall of 0.211 ns.
  - The 41-logic-level critical-path sentence cannot be checked from the receipts: only the timing summary is published, with the full report's hash.

## Executed evidence at this head

All runs used the 5.050 simulator, whose identity was verified (`Verilator 5.050 2026-07-01 rev v5.050`). Builds and runs went to unpublished scratch, so the clone was never written.

| Receipt | Result |
|---|---|
| `receipts/maap_run.log` | `KL_maap: 130 checks, 0 failures`, rc 0 |
| `receipts/maap_mutants.log` | `maap mutants: checks: 27 failures: 0` (clean control plus 26 named rejections), rc 0 |
| `receipts/maap_coverage.log` | `KL_maap.sv line 100.0% (169/169)`, gate PASS |
| `receipts/probes.log` (`scripts/r548_2_probes.py`, 12 probes) | Controls pass. Seed, draw, guard-removal and DEFEND-destination defects are killed. Survivors: S1 (two) and S2. A one-bit probe draw is killed by "probe draw reaches its high end". |
| `receipts/lfsr_model.log` | PASS (above) |
| `receipts/yosys_ooc_KL_maap.log` | `KL_maap 515 LUT, 278 FF, 59 CARRY4`, rc 0; against dev 637 / 268 that is -122 / +10, inside +40 / +40 |
| `receipts/gates/maap_differential.log`, `maap_differential_selftest.log.gz` | 12 tests PASS; 16/16 controls caught |
| `receipts/gates/lint_rtl.log` | PASS, 90 <= 90 |
| `receipts/gates/docs_check.log`, `module_matrix.log`, `test_evidence.log` | rc 0 each |
| `receipts/gates/em_dash_*.log`, `gen_toc.log` | **Not judged** (rc 2): the pinned Markdown renderer is not installed here, and shared installs are not allowed. A direct scan of the added lines in `291710b1..48f12dc1` finds no U+2014, and `git diff --check e21c1ca0..48f12dc1` is clean. |
| `receipts/regen_*.log`, `gate_checks.log`, `baseline_policy_diff.log`, `archive_manifest_check.log` | Part B, above |
| `receipts/hosted_snapshot.tsv` | 2026-10-08T02:38Z at the exact head: 15 completed success; 5 in progress (docs-check, elaborate, Verilator shards 1, 2 and 4); Physical gPTP skipped. A skipped or unfinished context is not counted as evidence. |
| `receipts/tree_integrity.log` (`scripts/r548_2_integrity.py`) | PASS. HEAD and tree exact; index equals HEAD's tree; 1,187 tracked files match in bytes and mode; no assume-unchanged or skip-worktree flag; nothing untracked or ignored. Gitlinks protocol-processor `2ad2f845`, gptp-processor `5dce647a` and verilog-axis `48ff7a7e` match and are clean. `external` is not initialised (not a build input). No probe touched the clone, so nothing needed restoring. |

## Ledger (reviewer-owned)

Every lens was applied in this round at the exact head.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R548-2-F1) | Seed and timer draws (`KL_maap.sv:141-149`, `:170-171`, `:292`) against B.3.4.1/B.3.4.2 random T, plus `receipts/lfsr_model.log` and harness [11]. Missed-fourth-PROBE text `MAAP_FABRIC.md:135-140` against Table B.7 probetimer!/probeCount!. Pool text `:50-52` against Table B.9 and both arms of `new_off_w` (`KL_maap.sv:282-283`). B.3.6.1 record `:129-132` against the integration (F1). | R548-2 | 48f12dc14099a3630a98eb07e9ec790695a72bfb |
| RTL | CLEAN | `KL_maap.sv` full file at head: seed mux (`:149`, `:292`); LFSR invertible and maximal (`receipts/lfsr_model.log`); guard `:276-277`; walk `:362-412`. Integration `milan_datapath.sv:7064-7086`, with the diff against dev comment-only. Yosys 515 / 278. In-context 429 / 279 from the route hierarchy. Merge tree against mechanical merge-tree. | R548-2 | 48f12dc14099a3630a98eb07e9ec790695a72bfb |
| Robustness | CLEAN | Zero-seed boundary over all 65,536 folds. Reset re-seed in [11] (`sim_main.cpp:586-622`). Supplied seed isolated from the LFSR. Backpressure mid-frame [6a]. Empty own range (`:491-497`). Disable and re-enable walks. Configuration dependence of the seed in integration (recorded under F1 as a docs and conformance claim; the RTL behaviour is pre-existing and a follow-up item). | R548-2 | 48f12dc14099a3630a98eb07e9ec790695a72bfb |
| Tests | CLEAN (S1, S2 and the retained R548-1-S2 are SUGGESTION) | `tb/verilator/maap/sim_main.cpp` [6a], [8] and [11]; `mutants.py` 26 rows plus control and item guard; 12 independent probes (`receipts/probes.log`); coverage 169/169; differential 12/12 and 16/16. | R548-2 | 48f12dc14099a3630a98eb07e9ec790695a72bfb |
| Docs | UNCLEAN (R548-2-F1; R548-2-E1) | `MAAP_FABRIC.md:50-52`, `:64-69`, `:91-95`, `:129-144`, `:167`, `:188-197`; banner `KL_maap.sv:12-57`, `:222-228`; `KL_maap.md:5`, `:27`; `milan_datapath.sv:267-286`; `AREA_BUDGET.md:99-206`; `234_PP_SHADOW_AREA_BASELINE.md:5`; `findings/README.md:21-22`; PR body; receipt archive README and MANIFEST (E1). | R548-2 | 48f12dc14099a3630a98eb07e9ec790695a72bfb |

## Real limits

- I did not have the standard's text in this round. Clause readings rest on the frozen issue text, the published Annex B contract and the prior rounds' public clause citations. The delta's conformance questions (B.3.4 randomness, the Table B.7 fourth PROBE) need nothing beyond those.
- Not run by me:
  - the five datapath suites, the crflic leg, the RV32 ctrl suite, builder, Yosys portability, the xvlog gate and any Vivado run;
  - the em-dash and TOC gates (renderer missing).
- The datapath suites are unaffected by Part A on this argument: the new seed equals round 1's for every fold that was nonzero, and the integration's reset MAC is 0, which folds to `0xACE1`. The `milan_datapath.sv` change against dev is comments only.
- Round 1's records were not regenerated: they are superseded at this head. The critical-path sentence is unverifiable from the receipts.
- Physical calibration NOT RUN. Simulation, resource results and field skips are not hardware proof.

## Pending manager duties

- Publish this round. Fix E1 (the archive manifest). Route F1 back to the lane.
- When F1 is answered, a re-review must cover Conformance and Docs at the new head. RTL, Robustness and Tests stay banked at this head only if the fix touches nothing in their scope.
- Build and validate the current-dev candidate (`e21c1ca0` source base; live dev `99e4eb6c`, PR #693 GMII capture). The area budget's re-baseline rule applies to that merge result, because #693 changes the shipping export.
- Own hosted and local-replica acceptance at the exact head. Five contexts were still running at the snapshot.
- After merge: acceptance 4, bench MAAP interop with the reference peer. Also file the follow-up deviations from the PR body, including the seed-timing gap in F1.
- Merge requires two independent positive verdicts, no round in flight, and maintainer authorization.

## Reproduce

From the packet directory, with a clone at the head (submodules at their pins) and the archive at `84add8ed` sparse-checked-out to `<archive>`:

```sh
python3 -I scripts/r548_2_lfsr.py
python3 -I scripts/r548_2_probes.py <clone> <scratch>/probes <verilator> --jobs 12
for e in route-1x1 ooc-1x1 ooc-8x8; do
  python3 -I scripts/r548_2_regen.py <clone> <archive>/review-evidence/686-r1/author-r2/resource-receipts/r2-48f12dc1/$e $e <scratch>/regen/$e
done
python3 -B <clone>/syn/ooc/pp_resource_gate.py check <scratch>/regen/route-1x1/meas --endpoint route-1x1 --baseline <F json from 291710b1>
python3 -I scripts/r548_2_integrity.py <clone> 48f12dc14099a3630a98eb07e9ec790695a72bfb 7ed2f048f73734f671ae6eb5e1a008544fa0d0d0
```

Host paths in receipts are replaced by `<clone>`, `<packet>`, `<tools>` and `<home>`. Results and diagnostics are unchanged. `MANIFEST.sha256` lists every publishable file. `scratch/` is not published.

R548-2 FINISHED
