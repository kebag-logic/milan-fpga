# #661 handoff: second processor pin adoption (ead80360)

Executor [A537]. Branch `661-pp-pin-ead80360` from dev `506d91dbeeba585d72d2e80d92fca799c719f8ee`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/661#issuecomment-5986065259
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/661#issuecomment-5986101343

Status: REVIEW READY. Items 1 to 7 complete within the assigned author scope; current head `42f654478c11bd8f2b070969d83140587190f276`.
Item 7 is complete; its final consumer, campaign and documentation tables are below. The initial interruption was external, not a failed gate. The full parent synthesis sweep, lint, BDD, capture, processor documentation/lint and resource instrument controls have passed at this head.
Internal reviewer: [R486]. External reviewer: [R487]. No review verdict is claimed.

## 1. The pin change

- `protocol-processor` gitlink `631eeb342ca1e3fa80e734077a56a943aee76ff1` -> `ead8036035affd53ef4b29979190f2f4f67084c0`
  (commit `4a2f8ae4`). No other processor change.
- Processor top header diff `631eeb34..ead80360`: one added parameter, `NVM_MEM_TMO_CYC_P = CLK_HZ_P` (P2); no port added,
  removed or changed. `KL_pp_shadow` leaves the parameter at its default.
  `protocol-processor/scripts/check-integrator-params.py`: "parameters: top 28, guide 28, diagram 28, OK".

## 2. Patches (item 2)

All four applied cleanly at `4a2f8ae4` with no offset (hunk headers and changed lines identical to the patches). The seven
patch commits together give tree `35a2525f`, equal to `git apply --cached` of the four patches in order on `4a2f8ae4`.

| Patch | sha256 | Commits |
|---|---|---|
| `parent-adoption-c8-bbf704ec.patch` | `3340d2e8e389a52c...` | `6178aa1b` (waiver pass-through + ENDSTATION_BUILDER row 45), `dbd9e246` (gate 36b lint=False) |
| `parent-adoption-p2-p1-1269cdaf.patch` | `d3034e89dba34862...` | `5dd3598d` (P2 regions), `eefffe50` (P1 regions); split by change region, the pair byte-identical to `git apply` |
| `parent-adoption-c10-1269cdaf.patch` | `55e62329f52e352b...` | `399d5976` (tops budget, self-test, CODE_QUALITY), `880a40fc` (xvlog.budget) |
| `parent-adoption-232-241f9184.patch` | `88ee5e9643a453f8...` | `42c63ebc` (xvlog.budget `pd_ix_w`) |

(The hunk table follows in section 8.)

## 3. Amendments (item 3)

- `5546023e`: W13's processor suites cited as `protocol-processor/tb/...` (the p2-p1 patch's row failed `check_doc_paths.py`).
- `d4d77e8a`: FASTCONNECT "Processor recovery" bullet and D3 section 15 item 5: processor #15 and #20 closed by P2.
- `7a33919a`: the duplicate L6/L10 checker `sw/builder/aem_image_checks.py` retired; gate 36b re-pointed to the lint. Its calls are removed from the builder and `sw/litex/milan_soc.py:3314` image emitter; the processor packer already lints both emitted documents. This is the explicitly assigned duplicate-check cleanup, with no SoC interface or firmware change.
- `70ebe851`: REGISTER_MAP `0x644` available_index note (resets after ENTITY_DEPARTING).

## 4. Re-recorded records (item 4)

- `a502f5eb` ROM digests (`ooc.sh --record-rom-digests`): both equal the `631eeb34` rows.
- `8829d9ff` boundary diagram (`submodule_boundaries.gen.py`): `docs/diagrams/submodule_boundaries.drawio`, `.svg`, `.png` and `docs/diagrams/PNG_MANIFEST.json`.
- `df4260fb` SUBMODULES.md pin row, lanes, parent-visible table.
- `34ed57eb` port_docs.budget (`--write-budget`): processor 1,757 -> 1,759 ports; counts unchanged.
- naming.budget (`--write-budget`): byte-identical, 95 recorded.
- `1a169973` two DUT-reader dispositions.
- `7370458c` saved-state materialization and `tb/verilator/pp_shadow/README.md`: the processor writer/walk now carries P1 names; the parent transfer remains separately owned.
- `ca129e38` CHANGELOG adoption entry. The resource record and its authoritative interpretation are covered in item 6.

## 5. Saved-state capture (item 5)

`check_nvm_capture.py` PASS: census and firmware digest equal the receipt. No re-measure. 8x8 maximum 13.86484 ms. The census is 13,210 bytes / 164 records at 8x8 and 3,290 bytes / 54 records at 1x1 TDM8. Product firmware SHA-256: `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`.

## 6. Resource gate (item 6)

All three completed with rc 0 under the host lock, without another heavy build in this lane beside them.
The route at `ca129e3805dbd45d1289325bc0c8bef06d05f6a2` uses 50,318 LUT,
54,214 FF and 15,789 slices (61 free); WNS +0.108 ns, WHS +0.036 ns.
All 100,970 routable nets are fully routed, routing errors 0. It fits and meets the 50 MHz STOP threshold.
The standalone figures are 23,178 LUT / 19,776 FF at 1x1 and 29,853 / 27,370 at 8x8.
Each endpoint saves five RAMB36s against C. Standalone timing is not a route verdict.
The interrupted 8x8 attempt had no completion receipt and was replaced by a fresh run.

`a5c68ac70` records all three endpoints with `syn/ooc/pp_resource_gate.py record --write`.
Only each endpoint's free-text `measured` note was supplied separately; every generated field came from the generator.
Every tolerance, floor and ceiling is byte-for-byte equal as a JSON value to C.
Checks against C and against D all return 0; `check-baseline` returns 0.
The complete per-scope comparison is `area-deltas.tsv` (inclusive scopes must not be added to descendants).
`area-receipts.json` records log/report/checkpoint size and SHA-256 without copying large artifacts.
All six images in each endpoint rehash to the recorded size and digest; no completed log has Synth 8-4445 or 8-7186 diagnostics.
The measured input files are unchanged at the later documentation commits. The recipe omits bitstream generation and retains the external measurement checkpoints for independent inspection.

The authoritative comparison is `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`.
It cites processor PRs #150, #153, #154 and #155, showing the saved-name walker and watchdog costs alongside the notification, SRP and queue reductions.
Notification rows, SRP FIFO payloads, timer-arm queues and listener records map to distributed RAM.
Parallel-read stamps and matcher fields deliberately remain registers. The large payload flop banks are gone.
This satisfies #234 criterion 2; the manager's comment 5974629836 says it was the only remaining criterion.
The 60 percent LUT target remains assigned to #640, with 12,278 LUT still to remove.
The comparison includes predecessor #653's CRF unbind change between C and the assigned dev base; it makes no claim to isolate that predecessor's contribution to outside-wrapper movement.

Resume checks: origin is the required HTTPS repository; the branch is
`661-pp-pin-ead80360`; HEAD descends from `506d91db`. Processor worktree root
verified before its status and head checks; it is clean at `ead80360`.
The existing TAKEN comment was retained without reposting.

## 7. Gates (item 7)

Completed at `42f654478c11bd8f2b070969d83140587190f276`. The final tables and raw receipt indexes follow.
Completed at this head: all 55 parent synthesis tops and both structural gates;
404 BDD scenarios / 1,968 steps; all four LiteX simulations and their driver
self-test; lint, source-list, capture and every resource-instrument control.
The complete parent sweep returned rc 0: 59/59 suites, 2,149,002 checks, zero in-suite failures and zero timeouts. It declares four `tsn_fuzz` skips: two generator-dependent field campaigns and their result-freshness checks. They contribute zero to the total; the two traceability checks still ran, as the suite contract specifies.
The processor sweep returned rc 0: 33 suites, 1,021,627 checks, 0 failing.
The gPTP contract, complete default tests and mutation controls, and lint returned rc 0.
The initial synthesis result used the system ABC revision. The final version audit
found it differed from the bundled revision required by `syn/yosys/README.md`.
The full synthesis and cache controls returned rc 0 with ABC
`5d51a5e420f5de493d07bf61109a977248c86ffb`; their canonical receipts are
`yosys-pinned` and `yosys-cache-pinned`. The independent tally confirms all 55 expected tops, with no errors. The mounted binary digest matches the fresh build; the host binary digest is unchanged before and after.
All three resource endpoint checks were repeated at this committed head and return 0.
`gate-results.json` retains completed gate receipts, including superseded environment attempts. `parent-suite-receipts.json` records all 59 individual suite-log sizes and hashes behind the aggregate.
`docs-results.json` records verbatim workflow commands and their SHA-256;
`docs-steps.tsv` gives the per-step make version, result and log digest.
Every raw log, command, head and rc receipt is outside this packet under `$VALIDATION_STORAGE/661-a537`.
The pinned simulation executable is `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`; host default is not used.
The hosted documentation commands are read directly from `.github/workflows/docs.yml`.
Each step records GNU Make 4.3. Markdown gates use `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`.
Explicit build invocations use `make -j16`; hosted docs command bodies remain verbatim, with two compilation jobs per configurable large simulation build. A private compiler launcher bounds concurrent C++ compiler processes to four across campaigns, preserving `/usr/bin/g++` and every argument; it also bounds submodule recipes that hard-code `-j 0`. No source or test flag is changed.

The two dev controls use an immutable source export of `506d91db`, with processor `631eeb34` and the recorded gPTP/AXIS pins.
No other checkout, branch or worktree was made. Disposable Git indexes reproduce `ls-files` over those exact trees for the unchanged source-list generator; the original indexes are never written.
The base export is under `$VALIDATION_STORAGE/661-a537/base-export` and contains no `.git`. `base-source-proof.json` verifies all 1,800 exported source files against their Git blob IDs, with zero differences.
The exact base/head comparisons reproduce #656 (physical gPTP 139/3) and #657 (render controls 28/32), without changing their tests.


## 8. Every supplied patch hunk

Coordinates name the applied patch tree `35a2525f`, before the required cleanup amendments.
The four C8 test hunks were subsequently replaced or retired with the duplicate checker in `7a33919a`; production packing always keeps the processor lint on.
The P2 W13 row's suite paths were qualified with `protocol-processor/` in `5546023e`.
No patch was hand-ported or offset. The resume independently re-ran this proof; `patch-equivalence.json` records the exact equal trees and every hunk result.

| Patch | Applied file:line | Processor change answered |
|---|---|---|
| c8 | `avdecc/aem_assemble.py:603` | C8: carry lint waivers into the assembled model |
| c8 | `avdecc/aem_specs.py:297` | C8: copy overlay waivers into the specification |
| c8 | `avdecc/gen_aemi_image.py:385` | C8: expose waivers in the packer document |
| c8 | `configs/endstation_ax7101_8x8.yaml:267` | C8: record the shipping 8x8 layout waiver under #584 |
| c8 | `docs/ENDSTATION_BUILDER.md:1040` | C8: document the accepted configuration key |
| c8 | `sw/builder/endstation_builder.py:4430` | C8: retain the key in normalized configuration |
| c8 | `sw/builder/endstation_builder.py:5234` | C8: emit the declared waiver in the overlay |
| c8 | `sw/builder/test_builder.py:28193` | C8: deliberately malformed images bypass packer lint for the old checker |
| c8 | `sw/builder/test_builder.py:28254` | C8: old checker index-walk fixture bypass |
| c8 | `sw/builder/test_builder.py:28268` | C8: old checker cyclic-index fixture bypass |
| c8 | `sw/builder/test_builder.py:28330` | C8: old checker presence fixture bypass |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:11` | P1: parent owns map persistence and rollback |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:385` | P1: stage 3 writer ownership |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:556` | P1: rollback resets processor stores only |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:597` | P1: parent restores empty maps on restore_rb_o |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:843` | P2: bounded manager error while device debt stays quarantined |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1179` | P1: parent restores maps after processor scalar restore |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1241` | P1: rollback responsibilities per owner |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1478` | P2: 1,000 ms owed-event deadline and retained device debt |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1521` | P2: three failed attempts report alarm and clear pending |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1549` | P2: W13 historical horizon and later bounded failure |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1560` | P2: qualify historical never-durable observations |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1851` | P1: map capacity belongs to parent writer |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1865` | P2/P1: release caveat and stage 3 ownership |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1935` | P2: rejected alternatives reference resolved contract |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2235` | P1/P2: authoritative ownership and recovery amendment |
| p2-p1 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2733` | P1: lane 4 uses parent buffers and restore_rb_o |
| c10 | `docs/development/CODE_QUALITY.md:609` | C10: document complete 42-top processor inventory |
| c10 | `scripts/check_rtl_source_lists_selftest.py:371` | C10: source-list controls cover all six new tops |
| c10 | `scripts/processor_yosys_tops.budget:2` | C10: retire six unsupported-top budget rows |
| c10 | `scripts/xvlog.budget:30` | C10: retire removed srp_class_a_prio_w diagnostic |
| 232 | `scripts/xvlog.budget:30` | #232: retire removed notification pd_ix_w diagnostic |

Full patch hashes:

| Patch | Bytes | SHA-256 |
|---|---:|---|
| `parent-adoption-232-241f9184.patch` | 587 | `88ee5e9643a453f8c31dc76e5f8d57e8deec89bcbbf9d4a4a8ca005757b72560` |
| `parent-adoption-c10-1269cdaf.patch` | 7133 | `55e62329f52e352bdd56b6d37bf2877aa952063f43221bb3f1d8583274ea34b9` |
| `parent-adoption-c8-bbf704ec.patch` | 8546 | `3340d2e8e389a52c49c32611c6eb36f55bef4534d30ecafbecad25b9a1b38a4c` |
| `parent-adoption-p2-p1-1269cdaf.patch` | 24711 | `d3034e89dba34862a0c8534472043212fd1f56412a90397997dcce3441613d84` |

## 9. Parent-visible list

The processor range includes eleven merged PRs. Numbers #143, #148 and #151 in the requested interval are issues; PR #156 is not in this pin.
The complete durable lane list is in `docs/reference/SUBMODULES.md`.

| Processor PR | Parent-visible result and adoption |
|---|---|
| #144, C8 | Packer lint is on by default, including L6/L10. Waivers pass from the declared 8x8 config through all parent emitters. Duplicate parent L6/L10 logic is removed; both emitters' named negative and presence tests reach the processor lint. No production lint bypass. |
| #146, #143 | Shared worker pool adds --jobs to eight mutation drivers; existing DUT-reader dispositions remain valid. No parent interface change. |
| #145, P2 | Top gains `NVM_MEM_TMO_CYC_P = CLK_HZ_P`, no port change. The parent keeps the default. Device-owed events count toward the 1,000 ms deadline; manager/port backpressure pauses it. A synthetic error releases the manager but does not erase device debt; only the device terminal or reset permits reuse. The saved-state docs describe alarm after three failed attempts. |
| #147, C7 | `gm_changed_tick_o` is removed from internal ADP. No parent face used it. Existing event-counter masks and wrap behavior remain. |
| #150, P1 | Name records use `0x80 + ordinal`, 72-byte payload, through `DESC_NAME_ENTRIES_P` (39/107 shipped, at most 128). Restore takes longer and emits no live-write pulse. The existing parent's sticky name pending stays until the separately owned materialization transfer. Parent maps remain under #637; no map RTL or firmware is added here. |
| #149, C10 | All 42 processor synthesis tops are supported; source-list controls and budget are updated. The internal NVM port payload ceiling is 65,527 bytes; the parent does not override it. Removed xvlog declaration is banked. |
| #152, #85 | `available_index` resets after departing; REGISTER_MAP 0x644 is corrected. No parent RTL edit. |
| #153, #232 | Notification registry/pending rows move to distributed RAM; removed `pd_ix_w` xvlog finding is banked. Re-baseline records the reduced payload flops. |
| #154, #230 | SRP FIFOs and walk-only fields move to RAM; parallel matcher fields remain registers. No parent interface edit. |
| #157, #81/#84 | GET_DYNAMIC_INFO joins the hazard class that serializes against ACMP stream changes. No parent port change. |
| #155, #639 | Timer-arm rings and listener records map to RAM. Parent re-baseline completes the remaining adoption obligation; test-evidence disposition follows the new arm-queue readers. |

The declared top port count stays 213. Across all processor modules the inventory rises from 1,757 to 1,759 ports:
ADP removes one output; the NVM writer adds `nchg_i`, `nchg_ord_i` and `sb_name_o` internally.
The NVM port adds its timeout parameter, and the writer adds name geometry.
`check-integrator-params.py` verifies 28 parameters in top, guide and integrator diagram 21.
The parent has no duplicate of that processor diagram; its own boundary figure is regenerated from the pin.
ROM bytes, firmware sources and the saved-state census are unchanged.

The port audit also read the parent-visible sections of PRs #140 and #142,
as item 4 requests. They are already contained in the old `631eeb34` pin:
#140's deadline and scoreboard faces are internal to the processor;
#142's merge carries C6's identify parameter/input, already tied off by the
first adoption. No additional parent binding or budget change is owed by either.

## 10. Remaining public actions

The verification table and PR body are complete. The final action is one `[A537] REVIEW READY` publication with this head on #661.
No push, PR creation/edit, merge, hardware operation or bench run is authorized in this lane.
Hosted checks, both independent reviews, merge validation, flashing and the post-merge soak remain with the manager and reviewers.

## Environment replay notes

- Host has no apt-get. The exact diagram-dependency installation script was run successfully in Ubuntu with its native GNU Make 4.3. The host gate uses the required prepared Python environment and its matching diagram packages.
- The existing shared SDK selector has no installer receipt, so the first host installation check refused it. An initial Ubuntu install passed. The canonical replay completed the SDK step and all following docs steps inside a private mount namespace: a fresh writable SDK parent appeared at the workflow's normal selector only within that process tree. HOME and the shared host installation are unchanged. The exact SDK command and the complete builder passed under the same verified prefix.
- The candidate act self-test runs only in a disposable offline job with no host credentials or Docker socket. The first attempted host-built make binary could not load its Guile library in Ubuntu; the replay uses Ubuntu's own GNU Make 4.3 and passes. This is a setup failure, not a self-test verdict.
- The auxiliary processor sweep first saw sv2v 0.0.12, which lowers its fatal guard differently and causes the test's expected $finish diagnostic check to fail. The unchanged guard passes with the processor-compatible sv2v 0.0.13. The complete processor sweep passes with 0.0.13; parent gates remain on their pinned 0.0.12. Verilator remains 5.050 in both.
- The no-Git documentation job runs its exact removal/check commands inside an isolated source archive of the committed head; it never removes the implementation worktree metadata.
- The real vendor syntax check and its live self-test share one acquisition of `/tmp/milan-vivado.lock`. Their queued launcher was changed only after it was stopped and proved to have no started gate or child command; the existing waiting process was retained. The idle outer successor was retired after both finished, avoiding a duplicate self-test and another lock wait.
- Original attempts and retries retain separate logs and rc files. No test or source was changed to resolve these environment differences.
- The system ABC package is `0.0.0.20260511-1`, source revision `c61f1a04e9db42db9cea876c1127bfd8f3eab040`, while the documented Yosys 0.66 bundle pins `5d51a5e420f5de493d07bf61109a977248c86ffb`. The required revision is built from its immutable source archive outside this packet and selected by a private mount namespace over `/usr/bin/abc`. The host installation is unchanged. The full synthesis repeat uses no result-cache options; its cache instrument gets a separate fresh self-test. The channel-map netlist leg invokes `proc; opt; memory; opt -full`, without ABC, so that leg is unaffected by the selector change.
- One processor-compatible sweep printed all 33 PASS rows but its receipt launcher then exited 2: the launcher's file had been edited while its shell waited, invalidating the remaining file offset. That log is retained as `processor-suites-013-unrecorded`, and is not used as a completed gate verdict. The whole sweep was repeated with the stable launcher and returned rc 0; only that completed receipt supplies the final verdict.

## Hosted documentation step results

All 49 shell steps completed with rc 0 at `42f654478c11bd8f2b070969d83140587190f276`.
Every step used GNU Make 4.3. The exact workflow bodies, execution boundaries and log hashes are in `docs-results.json`; the compact ledger is `docs-steps.tsv`.

| Job | Step | Make | rc |
|---|---|---|---:|
| docs-check | Build the validated HDL reference | GNU Make 4.3 | 0 |
| docs-check | Install the python gate dependencies | GNU Make 4.3 | 0 |
| docs-check | Install the pinned Markdown renderer | GNU Make 4.3 | 0 |
| docs-check | Install diagram gate dependencies | GNU Make 4.3 | 0 |
| docs-check | Link health, wording, dead-reference and local-info gate | GNU Make 4.3 | 0 |
| docs-check | Added-line em-dash gate | GNU Make 4.3 | 0 |
| docs-check | Concise audience documentation gate | GNU Make 4.3 | 0 |
| docs-check | Audience diagram no-drift gate | GNU Make 4.3 | 0 |
| docs-check | Product solution source-fact gate | GNU Make 4.3 | 0 |
| docs-check | Verified submodule documentation gate | GNU Make 4.3 | 0 |
| docs-check | HDL timing diagram no-drift gate | GNU Make 4.3 | 0 |
| docs-check | Published diagram PNG gate | GNU Make 4.3 | 0 |
| docs-check | Milan feature-status consistency gate | GNU Make 4.3 | 0 |
| docs-check | Traceability matrix no-drift gate | GNU Make 4.3 | 0 |
| docs-check | Fetch the builder source dependencies | GNU Make 4.3 | 0 |
| docs-check | Imported gPTP documentation gate | GNU Make 4.3 | 0 |
| docs-check | Code-quality measurement self-tests | GNU Make 4.3 | 0 |
| docs-check | Install the pinned sv2v release | GNU Make 4.3 | 0 |
| docs-check | Bare-metal scope gate | GNU Make 4.3 | 0 |
| docs-check | Install and verify the pinned RV32 SDK | GNU Make 4.3 | 0 |
| docs-check | Compiler-absent firmware controls | GNU Make 4.3 | 0 |
| docs-check | End-station builder gates | GNU Make 4.3 | 0 |
| docs-check | NVM record-space gate | GNU Make 4.3 | 0 |
| docs-check | Capture measurement census and clock gate | GNU Make 4.3 | 0 |
| docs-check | Saved-state writer gate | GNU Make 4.3 | 0 |
| docs-check | SoC source-list gate (Vivado would fail 40 min in without this) | GNU Make 4.3 | 0 |
| docs-check | RTL source-list drift gate | GNU Make 4.3 | 0 |
| docs-check | Boundary-unit naming ratchet | GNU Make 4.3 | 0 |
| docs-check | Port contract gate | GNU Make 4.3 | 0 |
| docs-check | Fail-fast ratchet | GNU Make 4.3 | 0 |
| docs-check | TODO ownership gate | GNU Make 4.3 | 0 |
| docs-check | Test-evidence ratchet | GNU Make 4.3 | 0 |
| docs-check | Mechanical hygiene ratchet | GNU Make 4.3 | 0 |
| docs-check | SystemVerilog idiom gate | GNU Make 4.3 | 0 |
| docs-check | C and C++ idiom gate | GNU Make 4.3 | 0 |
| docs-check | Python idiom gate | GNU Make 4.3 | 0 |
| docs-check | Shell idiom gate | GNU Make 4.3 | 0 |
| docs-check | CI event and SHA contract gate | GNU Make 4.3 | 0 |
| docs-check | Local act runner contract gate | GNU Make 4.3 | 0 |
| docs-check | Doc cited-path gate | GNU Make 4.3 | 0 |
| docs-check | Archive integrity gate | GNU Make 4.3 | 0 |
| docs-check | Per-page contents gate | GNU Make 4.3 | 0 |
| docs-check | AEM store generator self-test | GNU Make 4.3 | 0 |
| docs-check | Sweep/build shape gate | GNU Make 4.3 | 0 |
| docs-check | Deploy shape gate | GNU Make 4.3 | 0 |
| docs-check | Entity shape gate | GNU Make 4.3 | 0 |
| wire-accountability | Fetch the engine authority the builder derives from | GNU Make 4.3 | 0 |
| wire-accountability | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | GNU Make 4.3 | 0 |
| docs-check-no-git | Strip git metadata, then run the docs gate | GNU Make 4.3 | 0 |

## Final consumer and campaign results

All head-side commands below validate `42f654478c11bd8f2b070969d83140587190f276`. Markdown commands use the pinned Python environment.
The sweep inherits `MAKEFLAGS=-j16 VERILATOR_JOBS=2`; its source command is `make -C <suite>`.

| # | Consumer command | Evidence | rc |
|---:|---|---|---:|
| 1 | `python3 scripts/check_cpp_idiom.py` | docs-check-38 | 0 |
| 2 | `python3 scripts/check_py_idiom.py` | docs-check-39 | 0 |
| 3 | `python3 scripts/xvlog_gate.py --check` | xvlog-check | 0 |
| 4 | `python3 scripts/check_rtl_source_lists.py` | docs-check-30 | 0 |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | pp-srcs | 0 |
| 6 | `python3 sw/builder/test_builder.py --require-rv32` | docs-check-25; whole, two explicit NOT RUN arms | 0 |
| 7 | `make -C tb/verilator/pp_shadow -j16` | parent sweep / pp_shadow | 0 |
| 8 | `python3 scripts/check_port_contracts.py` | docs-check-32 | 0 |
| 9 | `python3 scripts/measure_naming.py --check` | docs-check-31 | 0 |
| 10 | `python3 scripts/measure_test_evidence.py --check` | docs-check-35 | 0 |
| 11 | `python3 scripts/docs_check.py` | docs-check-07 | 0 |
| 12 | `python3 scripts/lint_rtl.py --check --self-test` | lint | 0 |
| 13 | `make -C tb/verilator/nvm_cosim -j16 lint` | nvm-lint | 0 |
| 14 | `make -C tb/verilator/nvm_cosim -j16 quick` | nvm-quick | 0 |
| 15 | `make -C tb/verilator/milan_dp -j16` | parent sweep / milan_dp | 0 |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | parent sweep / milan_dp_render | 0 |
| 17 | `python3 scripts/check_sh_idiom.py` | docs-check-40 | 0 |

| Additional command | Result | rc |
|---|---|---:|
| `scripts/run_all_suites.sh $VALIDATION_STORAGE/661-a537/parent-suite-logs` | 59/59 suites; complete check accounting below | 0 |
| `bash protocol-processor/scripts/run_suites.sh` | 33/33; 1,021,627 checks, 0 failing; sv2v 0.0.13 | 0 |
| `make -C gptp-processor -j16 contract tb lint` | contract, every default test and mutation arm, lint | 0 |
| `syn/yosys/run.sh --results $VALIDATION_STORAGE/661-a537/yosys-pinned-results` | 55 tops plus tied-input and observer-purity gates; bundled ABC revision | 0 |
| `behave --no-capture -f plain` in `tests` | 404 scenarios / 1,968 steps | 0 |
| `scripts/run_litex_sims.sh --selftest`; `scripts/run_litex_sims.sh $VALIDATION_STORAGE/661-a537/litex-sim-logs` | driver controls and 4/4 simulations | 0 |
| `python3 scripts/check_nvm_capture.py` | census, clocks, timing arms and retained receipt agree | 0 |
| `python3 syn/ooc/pp_resource_gate.py check-baseline`; `check <endpoint-directory> --endpoint <name>` | unchanged policy and all three recorded endpoints | 0 |
| `python3 scripts/xvlog_gate.py --selftest` | planted controls pass; real check was not skipped | 0 |

The remaining instrument commands and their raw rc are individually recorded in `gate-results.json`: source-read-set and Tcl controls, baseline self-tests and mutants, resource self-tests and all 174 mutants, ROM failure controls, synthesis-cache controls, processor docs and processor lint.

Parent aggregate output:

```text
suites: 59   passed: 59   failed: 0   timed out: 0
checks: 2149002   in-suite failures: 0

declared skips (4) -- these ran NOTHING and contribute 0 to the total above:
  SKIPPED  tsn_fuzz: AAF/AVTP field campaign (tsn-gen absent; set TSN_GEN_ROOT to enable)
  SKIPPED  tsn_fuzz: hdl/ieee1722/avtp/doc/TEST_RESULTS.md freshness not checked (AAF/AVTP field campaign (tsn-gen absent; set TSN_GEN_ROOT to enable))
  SKIPPED  tsn_fuzz: gPTP/802.1AS field campaign (tsn-gen absent; set TSN_GEN_ROOT to enable)
  SKIPPED  tsn_fuzz: hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md freshness not checked (gPTP/802.1AS field campaign (tsn-gen absent; set TSN_GEN_ROOT to enable))
logs: $VALIDATION_STORAGE/661-a537/parent-suite-logs
```

The physical campaign returns rc 2 at both base and head, with exactly the same 139 checks / 3 failures from #656. The separately invoked abort-accounting verifier returns rc 0 at both.
The full render campaign returns rc 2 at both, with the same 28 PASS / 4 FAIL outcomes across all 32 controls from #657. `exception-comparison.json` retains both exact verdict lists. No test or threshold was changed.

The whole builder returns rc 0 and names two NOT RUN arms: the GNU Make 4.3 `MAKEFLAGS += -e` mutation has no effect on this make, and the historical board calibration report is not on disk. All assigned image-lint tests and both emitters run and pass.

Queued duplicate physical/render successors from the first launcher were retired only after the original completed receipt was durable. The concurrent replacements have their own completed receipts; an uncompleted duplicate is not counted as evidence.

The real vendor syntax check analysed 73 parent files and 52 pinned-processor files. It returned rc 0 with zero parent findings and the two existing processor findings exactly matching the ratchet (`cancel_hit_w` and `vd_push_w`). The live planted-fault self-test returned rc 0; neither result is a missing-tool skip.
