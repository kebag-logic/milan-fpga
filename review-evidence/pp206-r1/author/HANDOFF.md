# [A691] processor #206 — HANDOFF

**Status: REVIEW READY at head `9abb41f`.** Every gate the assignment names returned rc 0: the processor-top
suite with the new cases (within the full processor sweep), the mutant arm killed by the driver, `make check`,
and the parent consumer gate on a scratch clone of milan-fpga dev `97aab1d0` with this head as the gitlink and the
#202 wiring patch (sha256 `ff5068d2…1275`) applied. milan_dp's `[GSI]` checks did not regress: the same 461 checks
and 234 `[GSI]` lines at base and head, and the parent's `[GSI]` campaign kills all 11 of its mutants.
No top-level port, parameter or register-map change, so no STOP.

TAKEN: issue #206 issuecomment-6434935803 (2026-10-27). REVIEW READY with the head: issuecomment-6437442827.
Assignment: issue #206 issuecomment-6434829865.
Session 1 was stopped by its unit's memory cap (not by a gate) after the commit and the processor gates;
session 2 ran the parent gate in separate units and finished it. Void runs: `receipts/records/VOID.md`.

## 1. Records

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked before the commit) |
| Branch | `206-gsi-settled-gate` (local; not pushed) |
| Base (processor main) | `097a79875f20c27f0a5987a193c165c5086f3cf5`, tree `e496f4f6faa5d95dbf531f743ecd0dc7a3f72f4a` |
| Head | `9abb41f9f539fde8d940ff23b4b594f46658a46a`, tree `ac9a94c068f955e63a4d20c6fe7cbd8d6edd2e65` |
| Commit | `9abb41f` Report an input's stream_id, destination MAC and VLAN and their flags in GET_STREAM_INFO only while it is PROBING_COMPLETED (issue #206) |
| Top-level ports, parameters, register map | unchanged (`receipts/records/base-head-records.txt`) |
| Lane tree | clean, ignored files included (`git status --porcelain --ignored` empty) |

## 2. Changes (file:line at head, clause)

| # | File:line | Change | Clause |
|---|---|---|---|
| 1 | `hdl/top/protocol_processor_top.sv:3532`, `:3554-3564` | `gsi_settled_w`: an in-range index whose committed status `gsi_status_w[7:5]` (from `lstn_gsi_status_r`) is `PB_COMPLETED_C`, the test selector 6 used inline | Milan v1.2 5.3.8.5 (probing or settled), 5.3.8.6 Table 5.5 value 3; IEEE 1722.1-2021 7.4.16.2 |
| 2 | `hdl/top/protocol_processor_top.sv:3573-3574` | selector 6 reads the same wire; behaviour unchanged | Milan v1.2 Table 5.9 (stream_vlan_id) |
| 3 | `hdl/top/protocol_processor_top.sv:3578-3588` | while unsettled: selector 0 `& ~0x52000000`, selector 2 = 0, selector 4 `[63:16]` = 0 (failure-code byte still the SRP registrar's) | Milan v1.2 5.4.2.10.1, Table 5.9 |
| 4 | `docs/architecture/06_aecp_engine.md:384-393`, `:395-397`, `:460-461`, `:479-480`, `:491-493` | §6.2 and the F06.12/F06.13 rows: the three fields and flags pass only while settled | issue #206 acceptance item 3 |
| 5 | `docs/architecture/02_interfaces.md:430`, `docs/guides/integrator.md:600-609`, `docs/00_MILAN_COMPLIANCE_REVIEW.md:435` (REQ-AEM-010) | the same rule where the integrator's words are described | issue #206 acceptance item 3 |
| 6 | `tb/pp_top/README.md:494-515`, `:576-581` | section GI's settled-gate steps and the six arms | — |

Selectors 0, 2 and 4 still raise the external request and honour `gsi_wait_i`; while settled they pass unchanged.

## 3. New checks, planted mutants and failing words

New checks: `tb/pp_top/gsi_internal.hpp:606-742` (`settled_gate()`, section GI, 119 checks), with the harness
integrator mode `H::gsi_fold_identity` (`tb/pp_top/sim_main.cpp:1287-1303`, `:2054-2059`): selectors 2 and 4
answered from the published binding view, the three flags claimed in every flags word. Sink 0's steps, each
status change's unsolicited response and the solicited read, checked byte-exact and by name (the three flags,
stream_id, stream_dest_mac, stream_vlan_id, pbsta/acmpsta), with binding-view premise checks:

| Acceptance case (issue #206) | Steps | Expected |
|---|---|---|
| bound and probing before the first answer | PROBING (the bind's push), PROBING-SENT (after its PROBE_TX) | flags clear, fields zero |
| settled | SETTLED, SETTLED-AGAIN | the integrator's flags, the binding view's stream_id and MAC, the stored VLAN |
| back in PROBING_PASSIVE after a timeout with a stale ID | PASSIVE-STALE: talker departs (settled sink only notes it), T-ACMP-NOTK; premise: view still names the settled stream | flags clear, fields zero |
| unbound | RESET, UNBOUND (after UNBIND_RX) | flags clear, fields zero |
| (extra) the same timeout with the talker discovered | REPROBE, REPROBE-SENT: probing again, view still names the stream | flags clear, fields zero |

The shared expected-body helper (`tb/pp_top/sim_main.cpp:5415-5423`) clears the three flags and zeroes stream_id
and the destination MAC in every expected STREAM_INPUT body below PROBING_COMPLETED, so the GI, G and D3
expectations grade the same rule on the fixed integrator words.

Planted mutants (`tb/pp_top/gsi_mutants.py:106-132`; each killed by the driver with its named check;
`receipts/campaigns/gsi-results.json`, `receipts/campaigns/gsi-new-arms/`):

| Arm | Plant | Named failing words | FAIL lines (GI GATE) |
|---|---|---|---|
| `settled-gate-removed` (the defect as reported: pass-through restored) | `if (!gsi_settled_w)` → `if (1'b0)` | `GI GATE PASSIVE-STALE solicited: stream_id sink 0 is zero` | 82 (32) |
| `settled-gate-flags-passed` | selector 0 mask → `gsi_data_i` | `GI GATE PASSIVE-STALE solicited: STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID clear for sink 0` | 22 (22) |
| `settled-gate-sid-passed` | selector 2 zero → `gsi_data_i` | `GI GATE PASSIVE-STALE solicited: stream_id sink 0 is zero` | 60 (10) |
| `settled-gate-dmac-passed` | selector 4 `[63:16]` zero → `gsi_data_i[63:16]` | `GI GATE PASSIVE-STALE solicited: stream_dest_mac sink 0 is zero` | 60 (10) |
| `settled-gate-closed` | `if (!gsi_settled_w)` → `if (1'b1)` | `GI GATE SETTLED solicited: stream_id sink 0 is the settled stream's` | 829 (16) |
| `settled-means-bound` | `== PB_COMPLETED_C` → `!= 3'd0` | `GI GATE PROBING solicited: STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID clear for sink 0` | 71 (31) |

Base cross-check: the head's tests on the base RTL (`hdl/` replaced by `097a7987`'s, verified equal) fail
82 lines, 32 `GI GATE`, the same as `settled-gate-removed` (`receipts/processor/base-097a7987/`).

## 4. Processor gates (head `9abb41f`, disposable clones; every `.rc` is the command's own status)

| Gate | Result | Receipt |
|---|---|---|
| full sweep `bash scripts/run_suites.sh` with `REQ_TAG_LOG` (includes the processor-top suite) | rc 0; 1,030,712 checks, 0 failing; pp_top 10,872 (10,753 at the #202 record + 119) | `receipts/processor/sweep-9abb41f/` |
| `python3 scripts/check-req-tags.py --suites … --evidence …` | rc 0; 247 tags (+1), 247 evidence lines | same |
| `python3 tb/pp_top/gsi_mutants.py --jobs 4` | rc 0; 29 of 29 killed by their named checks (the 6 new arms included); golden and restored PASS | `receipts/campaigns/gsi.*`, `receipts/campaigns/gsi-results.json` |
| `python3 tb/pp_top/acmp_mutants.py --only gsi_vlan_external parent_vlan_shifted stored_vlan_truncated retry_probe_status_cleared` (arms on the selector 6 line this change rewrote) | rc 0; 5 of 5 killed; goldens PASS | `receipts/campaigns/acmp_vlan.*` |
| `make check` | rc 0 | `receipts/processor/head-9abb41f/` |
| `bash scripts/lint_hdl.sh` | rc 0; 41 modules LINT OK | same |
| base GI (`097a7987`, `make -C tb/pp_top gsi-internal`) | rc 0; 6,254 checks (head: 6,373) | `receipts/processor/base-097a7987/` |
| head tests on the base RTL | sim rc 1 (make 2); 82 FAIL lines, 32 `GI GATE` | same |

## 5. Scratch parent consumer gate

Scratch parent `pp206-parent`, a local clone of milan-fpga dev `97aab1d0` (push URL invalid, never pushed;
`receipts/records/parent-state.txt`):

| Commit | Content |
|---|---|
| `c3139895` | dev + the #202 wiring patch (sha256 `ff5068d295872d1f872b89890ff76f9bb1d3fd0738ad650282dbe45d9e171275`, 70,091 bytes) + processor `097a7987` (base) |
| `c7d5887d` | gitlink → `9abb41f` (one line) |
| `764d1253` | `./syn/yosys/ooc.sh --record-rom-digests` rows for `9abb41f` (equal to the `ed211803` rows) — **the gated pin** |
| `8f72c7e4` (base tree `pp206-parent-base`) | `c3139895` + the digest rows for `097a7987`, for the base area run only |

How it ran (session 2): every heavy part in its own unit, never in the lane's unit; MemoryMax 13G each (the
four shard units that `native-shards.py` starts at 10G were raised with `systemctl --user set-property --runtime`);
CPU ranges as `cpu_ranges.py` reported them free, plus the lane's own range. The full default sweep ran as
`native-shards.py pp206-a691-parentb <spec> <out> 4 …` with `VERILATOR_JOBS=4` in the spec's env prefix
(`receipts/records/parent-full-native-vj4.json`). Shard 2 of 4 was stopped twice by its 13G limit in
`capture_coherence`: the suite's default target (`all: run dp mutants` under `-j4`) starts its mutation arm beside
the datapath build, and the arm runs one model build per CPU of the unit (16 here, 4 on the hosted runner). In
its place: `capture_coherence` in the parent's own CI piece form (`scripts/ci_suite_pieces.py run capture_coherence__k`,
k = 0..3, under a 4-CPU affinity as on the hosted runner, then `ci_suite_pieces.py union`), and shard 2's other 15
suites each through `run_all_suites.sh`'s own per-suite step (`timeout 1800 make -C tb/verilator/<suite>`, then
`suite_tally.py --verdict`). The tally over all of it checks the inventory: every suite exactly once.

| Consumer gate (pin `764d1253`, processor `9abb41f`) | Result | Receipt (`receipts/parent/`) |
|---|---|---|
| static: `lint_rtl.py --check --self-test`, port contracts (+selftest), wire accountability (+self-test), SV idiom (+selftest), C++ idiom, RTL source lists (+selftest), behave (406 scenarios), yosys elaboration of `milan_datapath`/`KL_pp_shadow`/`KL_gptp_shadow`, the parser gate (`xvlog_gate.py --check`) | all rc 0 | `static-764d1253/` |
| ROM digests `./syn/yosys/ooc.sh --record-rom-digests` (at `c7d5887d`, producing `764d1253`) | rc 0; same contents as the `ed211803` rows | same |
| sweep shard 0/4 (15 suites incl. `milan_dp`) | rc 0; 15 passed; 251,015 checks, 0 failures | `parent-sweep-shards-b/shard-0/` |
| sweep shard 1/4 (17 suites incl. `pp_shadow`, `milan_dp_mclk`, `milan_dp_gm_steps`) | rc 0; 17 passed; 1,536,446 checks | `parent-sweep-shards-b/shard-1/` |
| sweep shard 3/4 (16 suites incl. `maap`, `mbx`) | rc 0; 16 passed; 23,086 checks | `parent-sweep-shards-b/shard-3/` |
| shard 2/4, 15 suites (incl. `milan_dp_render`) | each rc 0, verdict clean | `parent-shard2-rest/` |
| shard 2/4, `capture_coherence` in CI piece form | 4 pieces rc 0, verdicts rc 0; union rc 0: "43 cases exactly once; original tally passed" | `parent-shard2-capture-pieces/` |
| **full tally** `suite_tally.py <all five log dirs> --expect-suite-root tb/verilator` | **rc 0; 64 suites, no MISSING/UNEXPECTED/DUPLICATE; 2,190,635 checks, 0 in-suite failures**; 4 declared skips (`tsn_fuzz`: its external generator is absent on the test machine) | `parent-full-tally/` |
| consumer counts against the #202 consumer gate | `milan_dp` 13,685, `pp_shadow` 2,187, `maap` 251, `milan_dp_render` 347, `capture_coherence` 43 cases: identical | same |
| **milan_dp `[GSI]` leg** `make -C tb/verilator/milan_dp notify` + verdict, base `c3139895` vs head `764d1253` | rc 0 both; 461 checks, 0 failures both; the 234 `[GSI]` lines identical | `gsi-base-c3139895/`, `gsi-head-764d1253/` |
| **milan_dp `[GSI]` campaign** `make -C tb/verilator/milan_dp gsi-mutants` | rc 0; 11 of 11 mutants caught by their named checks; clean control PASS (1,765 s) | `parent-gsimut/` |
| out-of-context `./syn/yosys/ooc.sh KL_pp_shadow` | rc 0; 61,883 LUT, 4,332 LUTRAM, 28,346 FF, 15 RAMB36, 4 RAMB18, 10 DSP, 2,428 CARRY4 | `parent-ooc/` |
| same at the base (`8f72c7e4`) | rc 0; 61,219 LUT, 4,332 LUTRAM, 28,334 FF, same BRAM/DSP/CARRY4 (the #202 figures): this change costs +664 LUT (+1.1%), +12 FF | `parent-ooc-base/` |

The parent's `[GSI]` arms quote processor lines verbatim (`PP_SEL4`, `PP_SEL5`, `PP_SEL7`, `PP_INTERNAL`,
`PP_SINK`, the event lines); this change leaves each of them in place exactly once, which the campaign's plant step
enforces. The arm "the failure-code byte is left to the parent" passes `gsi_data_i` whole in selector 4; the gate
still zeroes `[63:16]` while unsettled, and the arm is still caught by its named check.

## 6. Completion

Required: done exactly (§2; the same test selector 6 uses). Acceptance: (1) the four cases — §3; (2) a mutant
restoring the pass-through is caught — `settled-gate-removed`, plus five narrower arms; (3) the docs row for
GET_STREAM_INFO is updated — §2 rows 4-5; (4) the parent consumer gates pass — §5; milan-fpga's own `[GSI]` cases
and its `gsi_mutants.py` entry for the new gate land with the pin adoption (milan-fpga #790), as the issue says.

No push, PR creation or edit, merge, rebase, sub-agent, hardware or bench access, flashing, or top-level
interface change. Nothing was posted on issue #206 but TAKEN and REVIEW READY.

Resources: session 2's lane unit stayed under 1.1 GB; the parent work ran in units of MemoryMax 13G (shard peaks
5.9, 3.7, 4.6 GB; capture 3.9 GB; the `[GSI]` campaign 3.3 GB); host MemAvailable stayed above 48 GB.

## 7. Receipts

`INDEX.md` here and in every `receipts/**/` directory is generated from the files present
(`index.py`). Host paths in receipts are normalized (`<home>`, `<data>`, `<work>`, `<parent>`, …); a record over
190 KB is kept as its size, sha256 and tail (`*.excerpt.txt`), and every raw record is listed with its size and
sha256 in the directory's `RAW-RECORDS.csv`.

| Receipt | What it holds |
|---|---|
| `receipts/processor/` | the head sweep and req-tags, `make check`, lint, base GI, the head tests on the base RTL |
| `receipts/campaigns/` | `gsi_mutants.py` (29 arms) and the ACMP VLAN arms, with each new arm's failure list |
| `receipts/parent/` | the consumer gate (§5) and the void runs (`void/`) |
| `receipts/records/` | base and head records, the scratch parent's state, the sweep spec, `VOID.md` |
