# [A699] processor #203 handoff: AECP REBOOT and reboot_req_o

Status: REVIEW READY at head `1be824f`. The implementation, tests, mutants and docs are committed.
Every gate and campaign listed below finished with rc 0, and every planted arm was KILLED. The
scratch-parent consumer gate passes with `reboot_req_o` left unconnected. The STOP condition was
not met. Not pushed and no PR opened; PR-BODY.md is ready for one.

## Base and head

- Repository: processor (protocol-processor-control-plane-avb-milan), branch `203-aecp-reboot`
  (`git remote get-url origin` checked before the first commit).
- Base: main `f65c8ff7c673aaa8e2ea8da654f081ddb13588d8` (HEAD before the first commit, checked).
- **Head: `1be824fccbda5d3341737f5fe033d60edd27af57`**, tree `ab055c2107ab5ce1ead0f1fa6cfce10ae0956c12`.
  Not pushed. Nine commits, one-line subjects, no body, no trailers (`receipts/records/processor-records.txt`):

| Commit | Subject |
|---|---|
| `d7a24de` | Answer AECP REBOOT of ENTITY 0 SUCCESS, notify the other controllers, send ENTITY_DEPARTING, then hold reboot_req_o (issue #203) |
| `1fde6ea` | Count REBOOT's F06.14 row in the AECP gate's repeated-row plant (issue #203) |
| `6c04588` | Split RBT6 into the scenario, the wire grading and the after-acceptance checks, one declarator per line (issue #203) |
| `061a9ec` | Re-cut six mutation patches whose context the REBOOT change moved, each planting the same defect (issue #203) |
| `5fd298c` | Keep the d3 enable arm on the restore term alone now that ADP's enable also falls for a REBOOT (issue #203) |
| `2f27767` | Tell the operator what a controller's REBOOT does on the wire (issue #203) |
| `1df890d` | Wrap the A5b paragraph's REBOOT sentence in tb/pp_top/README.md (issue #203) |
| `c82bb1a` | Say which head counted the REBOOT arms in tb/pp_top/README.md (issue #203) |
| `1be824f` | Say in tb/aecp_cmds/README.md that the sweep resets the engine after an accepted REBOOT (issue #203) |

- `git diff --stat f65c8ff7 1be824f`: 50 files, +1,210 -108. `hdl/` is unchanged after `d7a24de`; every
  commit after `5fd298c` touches only `docs/guides/operator.md`, `tb/pp_top/README.md` and
  `tb/aecp_cmds/README.md`. `git diff --check` clean; lane tree clean, ignored files included.
- Top-level change: exactly one new output, `reboot_req_o`. No parameter, no register-map change
  (side-port map untouched; `make check` `params` gate: top 29, guide 29, diagram 29).

## Assignment

- Issue #203 and issuecomment-6493855055. Integrator side: milan-fpga #787 (reset wiring), #396.
- TAKEN posted: issuecomment-6493882095.
- REVIEW READY posted with head `1be824f`: issuecomment-6502031159. These two are the lane's only
  posts.

## Design decisions (recorded)

- Figure number: IEEE 1722.1-2021 puts REBOOT in Figure 7-68 (7-75 is AUTH_ADD_KEY); the issue's
  "Figure 7-75" is cited as 7-68 throughout.
- ENTITY_DEPARTING clause: Milan v1.2 5.2 is only the chapter overview; the requirement is Milan
  5.6.3.3 (SHUTDOWN event), Table 5.51, 5.6.3.5.8 (WAITING) and 5.6.3.5.11 (DELAY), DOWN ignores
  it. IEEE: 6.2.1 introduces the Advertising Entity/Interface machines; the send is 6.2.4.1.3
  doTerminate and 6.2.5.2.2 txEntityDeparting (Figure 6-3); 6.2.6 is the receiving controller's
  Discovery machine (rcvdDeparting, Figure 6-4).
- Notification: 7.4.43 "On success this command also sends an unsolicited notification", 7.5.2
  lists REBOOT, Milan 5.4.5.2 shall. Implemented as class 9 (the {type, index} body of
  START/STOP_STREAMING's notification) with REBOOT's opcode in the job's first argument.
- ENTITY_ACQUIRED is unreachable: ACQUIRE_ENTITY never succeeds (Milan 5.4.2.1). RBT5 shows it.
- reboot_req_o: a held level until rst_n (the assignment's recommendation).
- Acceptance point: the SUCCESS response's TX grant. From it: the engine takes no command
  (txn_ready_o and A_IDLE), the top discards every frame that starts on rx_* after it.
- Sequence: response last byte -> notification round done and no unsolicited frame in flight ->
  ADP enable falls (SHUTDOWN) -> ADP has nothing left to build/queue/send -> reboot_req_o.
- No wait for persistence: documented; the integrator gates its reset on
  `(|nvm_unflushed_o) | d3_unflushed_o`.
- Hazard class: CFG_BARRIER, global key (lock-protected, ends service).

## Changes (file:line at head, clause)

| # | File:line | Change | Clause / item |
|---|---|---|---|
| 1 | `hdl/top/protocol_processor_top.sv:842` | the one new top-level port `reboot_req_o`, documented as a held level, 0 from reset, until `rst_n` | #203 "reboot_req_o (pulse or level, stated)"; assignment recommendation |
| 2 | `hdl/top/protocol_processor_top.sv:1350` (`rx_reboot_gate`) | from the engine's acceptance, a frame that starts on `rx_*` is discarded whole (admission decided at its first byte) | #203 "accepts no further command" |
| 3 | `hdl/top/protocol_processor_top.sv:1718` | classifier: REBOOT (0x002A) is `CFG_BARRIER`, global key, with SET_CONFIGURATION | IEEE 7.4.43.2 (lock-protected), F03.7 |
| 4 | `hdl/top/protocol_processor_top.sv:2020` | ADP's effective enable also falls for good from RB_DOWN: Milan's SHUTDOWN, so ENTITY_DEPARTING where advertising | Milan v1.2 5.6.3.3, 5.6.3.5.8, 5.6.3.5.11, Table 5.51; IEEE 6.2.4.1.3, 6.2.5.2.2 |
| 5 | `hdl/top/protocol_processor_top.sv:4879`, `:4892`, `:4913` | the REBOOT sequence: RB_RESP (the response's last byte), RB_NTF (notification round done, no unsolicited frame in flight), RB_DOWN/RB_DEP (DEPARTING built, queued and sent), RB_REQ (`reboot_req_o`, held) | #203 "the request follows the transmit-done of that response"; "before the request, send ENTITY_DEPARTING" |
| 6 | `hdl/aecp/KL_aecp_engine.sv:838`, `:1437`, `:1617` | `OP_REBOOT_C`, the `rboot_w`/`rboot_r` discriminator, REBOOT joins the `{type @24, index @26}` shape | IEEE 7.4.43.1, Figure 7-68 |
| 7 | `hdl/aecp/KL_aecp_engine.sv:3654` | A_PLD-exit route: cdl < 16 -> E_RBOOTBAD (BAD_ARGUMENTS), type != ENTITY -> E_RBOOTNS (NOT_SUPPORTED), else E_RBOOT | IEEE 7.4.43.1; Table 7-141 |
| 8 | `hdl/aecp/KL_aecp_engine.sv:3969`, `:2682`, `:2860`, `:391` | acceptance at the SUCCESS response's TX grant (`rbt_hold_r`, `reboot_o`); no command taken after it (`txn_ready_o`, A_IDLE) | #203 "no further command" |
| 9 | `hdl/aecp/KL_aecp_engine.sv:1481` | class 9's unsolicited job answers under REBOOT when its first argument is 0x002A | IEEE 7.4.43, 7.5.2; Milan 5.4.5.1, 5.4.5.2 |
| 10 | `hdl/aecp/ucode/gen_ucode.py:270`, `:2351` | E_RBOOT (locate = index check -> NO_SUCH_DESCRIPTOR; CHECK_LOCK -> ENTITY_LOCKED; SUCCESS; NOTIFY_ENQ 9), E_RBOOTNS, E_RBOOTBAD, all `{type, index}` at cdl 16 | IEEE 7.4.43.1, 7.4.43.2 |
| 11 | `hdl/aecp/KL_aecp_notify.sv:1213` | `cmd_busy_o`: command notification queued or its round running | sequence input |
| 12 | `hdl/adp/KL_adp_engine.sv:957` | `tx_busy_o`: a queued ADPDU not yet handed to txreq | sequence input |
| 13 | `hdl/aecp/ucode/aecp_commands.json:400` | the command model's REBOOT row (status set, CFG_BARRIER, lock, class 9 notification, entries) | #203 "the AECP command model" |
| 14 | `docs/architecture/06_aecp_engine.md:279` (generated F06.14), `:914` (F06.9), `:1044` (§6.11), `:1465` (§8.1) | REBOOT row, lock-protected set, the REBOOT section (routes, notification, acceptance, sequence, clause map), realized inventory | #203 docs |
| 15 | `docs/00_MILAN_COMPLIANCE_REVIEW.md:305`, `:555`, `:576` | GAP-13 disposition, REQ-FWX-001, F00.2 GAP-13 row | #203 "REQ-FWX-001, GAP-13, compliance review entry" |
| 16 | `docs/architecture/02_interfaces.md:133`, `:581` | reset rule 6 and F02.10 `reboot_req` (held level) | #203 "stated in the interface documents" |
| 17 | `docs/guides/integrator.md:31`, `:588`, `:697` | reset table, status table, bring-up step 7 | same |
| 18 | `docs/architecture/03_packet_engine.md:242`, `docs/architecture/04_adp_engine.md:166`, `docs/diagrams/21-integration-faces.svg` | CFG_BARRIER members; the effective enable; the contract figure gains the port and its tie-off exception | consistency |
| 19 | `tb/pp_top/sim_main.cpp:12332` (`RebootPhase`, section RBT), `:3409` (M9 gains 0x002A), A5b drops 0x002A | every status, the notification, the order on the wire, the held level, no command after | #203 "tests for every status" |
| 20 | `tb/pp_top/aecp_dispatch_mutants.py`, `tb/pp_top/aecp_dispatch_mutations/rbt-*.patch` (17), `tb/pp_top/Makefile` (`reboot`) | the REBOOT arms; `a5b-reboot-success-arm` retired | #203 "the mutant that raises the request before the response is sent" = `rbt-request-at-acceptance` |
| 21 | `tb/aecp_cmds/sim_main.cpp:221`, `:473`, `decode.json` (regenerated by `make record`) | the sweep resets the engine after an accepted REBOOT; the class-9 job swept with 0x002A | the decode record |
| 22 | `scripts/aecp_gate/plants.py:571`; `tb/pp_top/d3_mutants.py`; six re-cut patches (`tb/pp_top/mutations/{acmp-waits-for-aecp,dl-kill-tied-off,hz-setcfg-not-barrier,hz-stub-restored}`, `tb/adp_engine/mutations/{if-egress-collapsed,if-top-ingress-live}`) | test assets that quote moved lines, each planting the same defect | consistency |

## New checks, planted mutants and failing words

New section RBT in `tb/pp_top/sim_main.cpp` (`make -C tb/pp_top reboot`, `--reboot-only`; the default
build runs it after AD): 79 checks, 0 failures. A fresh processor per SUCCESS; every frame the MAC
takes is logged with the clock of its last byte (`H::tx_log`), and `reboot_req_o`'s first 1 and any
later 0 are tracked in `H::step`.

| Check (label prefix) | What it grades |
|---|---|
| RBT1 | cdl 12 and cdl 14: `BAD_ARGUMENTS`, `{0, 0}` at cdl 16, byte-exact; not accepted; no notification; still served |
| RBT2 | MEMORY_OBJECT 0, AUDIO_UNIT 0, CONFIGURATION 0: `NOT_SUPPORTED` echoing `{type, 0}` at cdl 16 |
| RBT3 | ENTITY 1, ENTITY 0x7FFF: `NO_SUCH_DESCRIPTOR` at cdl 16 |
| RBT4, RBT4b, RBT4c | under another controller's lock: ENTITY 0 `ENTITY_LOCKED`; MEMORY_OBJECT 0 still `NOT_SUPPORTED`; ENTITY 1 still `NO_SUCH_DESCRIPTOR` (the stated order) |
| RBT5 | ACQUIRE_ENTITY is `NOT_SUPPORTED`, so `ENTITY_ACQUIRED` cannot arise |
| RBT6 | the lock holder's REBOOT with three registered controllers: SUCCESS byte-exact; notification (u = 1, entry seq 1) to each other controller, none to the requester; one ENTITY_DEPARTING byte-exact; order response < notifications < DEPARTING < `reboot_req_o`; held to the end; the command queued behind it never served; AEM, ACMP and ADP commands after it unanswered |
| RBT7 | not advertising, nothing registered: the MAC holds the response's last byte 30 ms, the engine has accepted, `reboot_req_o` stays 0; released, it rises after the response |
| RBT8 | not advertising, one controller, padded command (cdl 20): SUCCESS at cdl 16, the notification (seq 0), no DEPARTING, request after both |

Also: M9 sweeps 0x002A on every non-AEM message type (the `aem_w` guard of the new arm); A5b no longer
lists REBOOT; tb/aecp_cmds records REBOOT's three programs and the class-9 job's 0x002A.

Planted arms (`tb/pp_top/aecp_dispatch_mutants.py`, target `reboot`), each KILLED by its named check at
the head, with the count of failing checks:

| Arm | Plant | Named failing words | Failing checks |
|---|---|---|---|
| `rbt-request-at-acceptance` (the assignment's "request before the response is sent") | RB_RUN goes straight to RB_REQ | `RBT7 reboot_req_o stays 0 while the MAC holds the SUCCESS response's last byte` | 12 |
| `rbt-response-unwatched` | RB_RESP leaves without the response's last byte | same | 3 |
| `rbt-notifications-unwatched` | RB_NTF without `ntfy_cmd_busy_w` | `RBT6 reboot_req_o rises after both notifications left` | 4 |
| `rbt-notification-flight-unwatched` | RB_NTF without `tx_fly_uns_r` | `RBT8 reboot_req_o rises after the response and the notification left` | 2 |
| `rbt-no-shutdown` | `rbt_adp_off_w = 1'b0` | `RBT6 one ENTITY_DEPARTING` | 2 |
| `rbt-departing-unwatched` | RB_DEP unconditional | `RBT6 ENTITY_DEPARTING leaves after the notifications and before reboot_req_o` | 3 |
| `rbt-departing-flight-unwatched` | RB_DEP without `tx_fly_adp_r` | same | 3 |
| `rbt-request-pulse` | RB_REQ returns to RB_RUN | `RBT6 reboot_req_o is held from its rise to the end of the run` | 2 |
| `rbt-rx-gate-dropped` | `rx_take_w = rx_valid_i` | `RBT6 an ACMP command after the acceptance gets no answer` | 1 |
| `rbt-engine-hold-dropped` | hold removed from `txn_ready_o` and A_IDLE | `RBT6 the command queued behind the REBOOT is never served` | 1 |
| `rbt-accept-any-status` | acceptance on any REBOOT response | `RBT1 REBOOT of 0 payload bytes (cdl 12): BAD_ARGUMENTS: the REBOOT is not accepted and reboot_req_o stays 0` | 33 |
| `rbt-short-gate-dropped` | cdl-16 floor removed | `RBT1 REBOOT of 0 payload bytes (cdl 12): BAD_ARGUMENTS: byte-exact at cdl 16` | 35 |
| `rbt-type-gate-dropped` | ENTITY gate removed | `RBT2 REBOOT of MEMORY_OBJECT 0: NOT_SUPPORTED: byte-exact at cdl 16` | 27 |
| `rbt-index-unchecked` | E_RBOOT + 1 (BR_STATUS) -> NOP | `RBT3 REBOOT of ENTITY 1: NO_SUCH_DESCRIPTOR: byte-exact at cdl 16` | 20 |
| `rbt-lock-unchecked` | E_RBOOT + 2 (CHECK_LOCK) -> NOP | `RBT4 REBOOT of ENTITY 0 under another controller's lock: ENTITY_LOCKED: byte-exact at cdl 16` | 13 |
| `rbt-notify-dropped` | E_RBOOT + 4 (NOTIFY_ENQ) -> NOP | `RBT6 the REBOOT notification reaches every other registered controller` | 4 |
| `rbt-notification-type` | class-9 job's REBOOT command_type dropped | same | 4 |

Retired: `a5b-reboot-success-arm` (issue #74: a REBOOT SUCCESS arm), because SUCCESS is now the answer.

## Gates run

Each in a disposable clone of the stated head; every rc is the command's own status. Heads after
`5fd298c` change only `docs/guides/operator.md`, `tb/pp_top/README.md` and `tb/aecp_cmds/README.md`
(`git diff --stat 5fd298c <head>`), so results at `5fd298c` stand for them.

| Gate | Head | Result |
|---|---|---|
| `make check` (PATH with the mermaid CLI) | `1be824f` | rc 0; every gate OK (aecp commands 32 commands, F06.14 42 rows; self-test 231 of 231) |
| `bash scripts/run_suites.sh` with `REQ_TAG_LOG` | `1be824f` | rc 0; 1,030,845 checks, 0 failing; pp_top 10,984 (RBT 79), aecp_cmds 181 |
| `python3 scripts/check-req-tags.py --suites suites.txt --evidence req-tags.txt` | `1be824f` | rc 0; 259 evidence lines, 14 suites (REQ-FWX-001: 9) |
| `make -C tb/pp_top reboot` (section RBT alone) | `1be824f` | rc 0; 79 checks, 0 failures |
| `bash scripts/run_suites.sh` (early, informational) | `1fde6ea` | rc 0; 1,030,845 checks, 0 failing; pp_top 10,984 |
| `bash scripts/lint_hdl.sh` (Verilator 5.052, and the parent's pinned 5.050) | `5fd298c` | rc 0 both; 41 modules |
| `./syn/yosys/run.sh` (sv2v + yosys, every top) | `5fd298c` | rc 0; `protocol_processor_top` and `KL_aecp_engine` (Xilinx) OK |
| `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4` | `5fd298c` | rc 0; 93 checks, 0 FAIL |
| `python3 aecp_dispatch_mutants.py --jobs 2` | `5fd298c` | rc 0; 91 checks: 5 controls PASS, 86 arms KILLED (17 new); every count equals its README cell; 1,445 s |
| `python3 aecp_mutants.py --jobs 2` | `5fd298c` | rc 0; 67 checks PASS (the four re-cut arms KILLED) |
| `make -C tb/aecp_cmds mutants` | `061a9ec` | rc 0; 17 of 17 detected, golden and restored PASS |
| `make -C tb/adp_engine mutants JOBS=2` | `061a9ec` | rc 0; 62 checks PASS (the two re-cut arms KILLED) |
| `d3_mutants.py --jobs 2` (two parts: 29 arms, then `--only` the other 81) | `5fd298c` | rc 0; 110 of 110 KILLED (29 + 81, no overlap, union = the driver's 110 labels: `d3-5fd298c/UNION.txt`), goldens PASS in both parts (part 1 stopped by me before the 2 h task limit, its 29 verdicts kept) |
| `notify_mutants.py --jobs 1` | `5fd298c` | rc 0; 137 of 137 KILLED, goldens PASS |
| `ctr_mutants.py --jobs 1` | `5fd298c` | rc 0; 18 checks: 18 PASS, 0 FAIL; 450 s |
| `acmp_mutants.py` (part 1 `--jobs 1`: 30 arms; part 2 `--jobs 2 --only` the other 71) | `5fd298c` | 101 of 101 KILLED (30 + 71, no overlap, union = the driver's 101 `name@suite` labels: `acmp-5fd298c/UNION.txt`); the 8 goldens PASS in both parts; part 2 rc 0 ("71 of 71 KILLED by their named checks; goldens PASS"). Part 1 stopped by me before the 2 h task limit, so it has no rc of its own; its 30 verdicts kept |
| `gsi_mutants.py --jobs 1` | `5fd298c` | rc 0; "GSI mutations: 30 detected by named checks; golden and restored PASS"; 2,171 s |
| `name_wr_mutant.py` | `5fd298c` | rc 0; "Name-write mutation: decode killed; golden and restored PASS" |
| `make -C tb/elab_guards mutants` | `5fd298c` | rc 0; control PASS, "elab guard mutants: 160 of 160 killed"; 869 s |

`061a9ec..5fd298c` changes only `tb/pp_top/d3_mutants.py`, which neither the aecp_cmds nor the adp_engine
campaign reads.

## Scratch-parent consumer gate

Scratch parent: a committed local clone of milan-fpga dev `1e80128f` (push URL disabled, never pushed),
submodules from local repositories. Final head **`ab0b9185`**, gitlink protocol-processor `1be824f`,
gPTP `f97c1803` (`receipts/records/parent-records.txt`). `reboot_req_o` is left unconnected.

| Parent commit | Content |
|---|---|
| `d48fdeb4` | gitlink -> `1fde6ea` (first probe; only the gitlink changed) |
| `ec54c287` | gitlink -> `5fd298c` |
| `65e7503c` | KL_pp_shadow names the port open: `.reboot_req_o (),  // ... open until milan-fpga #787 wires the reset` |
| `fc9648e3` | `./syn/yosys/ooc.sh --record-rom-digests` rows for `5fd298c` (ucode `49a993be...`, ltn unchanged) -- **the swept pin** |
| `fd02ed11` | REBOOT in the parent's served inventories: `tests/steps/aecp_engine_steps.py` SERVED, `docs/reference/milan_feature_status.json` and its four fact documents, the five "thirty" counts |
| `6fff40d7` | gitlink -> `1be824f` |
| `2ca58ec0` | ROM digest rows for `1be824f` (same digests as `5fd298c`) |
| `ab0b9185` | `docs/reference/SUBMODULES.md` pin row and `submodule_boundaries.gen.py`'s regenerated diagram |

Findings (each a required step of the adoption, milan-fpga #787 or its pin PR; receipts in
`receipts/parent/findings/`):

1. **Pin missing at KL_pp_shadow's instance** (only the gitlink changed, `d48fdeb4`):
   `scripts/lint_rtl.py --check` fails, hdl/milan 3 > ratchet 2, the new violation
   `KL_pp_shadow.sv:1235:5: PINMISSING Instance has missing pin: 'reboot_req_o'`. The explicit open
   connection with a rationale passes lint and port contracts (`1b-open-port-trial`).
2. **behave**: `features/aecp_response_contract.feature:359` fails, "the engine decodes 0x002a but this
   suite's SERVED inventory does not list them". Fixed by the SERVED row (SUCCESS at cdl 16 for the
   sweep's ENTITY-0 shape).
3. **Feature ledger**: with that row, `check_feature_status.py` wants REBOOT in
   `milan_feature_status.json`, its four fact documents and the "thirty" served counts.
4. **Pin documentation**: any pin bump fails `check_submodule_docs.py` and
   `submodule_boundaries.gen.py --check` until SUBMODULES.md and the diagram are regenerated.

| Consumer gate | Parent head | Result |
|---|---|---|
| Full sweep, `native-shards.py pp203-a699-parent <spec> <out> 4` (four 4-CPU shards of one picked range: capture_coherence's mutation arm builds one model per CPU of its affinity, and 16 per shard is what ran a prior lane out of memory) | `fc9648e3` (pin `5fd298c`) | rc 0 all four: 14 + 17 + 17 + 16 suites; 1,575,325 + 14,364 + 251,927 + 350,078 checks; 0 in-suite failures; 81 min wall |
| `scripts/suite_tally.py <four log dirs> --expect-suite-root tb/verilator` | same | rc 0; 64 suites, each once; **2,191,694 checks, 0 in-suite failures** (`milan_dp`, `pp_shadow`, `nvm_cosim`, `capture_coherence` among them) |
| 20 static gates: port contracts (+selftest), wire accountability, SV/C++/Python idiom (+selftests), RTL source lists (+selftest), `pp_srcs.py --check --selftest`, hygiene (+selftest), TODO ownership (+selftest), doc paths, `lint_rtl.py --check` and `--self-test`, entity shape self-test | `ab0b9185` | all rc 0 |
| behave (495 scenarios), `syn/yosys/run.sh --mode elaborate` of `milan_datapath`, `KL_pp_shadow`, `KL_gptp_shadow`, `xvlog_gate.py --check` | `ab0b9185` | all rc 0 (xvlog 0 findings == ratchet) |
| `check_feature_status.py` (+self-test), `docs_check.py`, `check_doc_style.py`, `check_em_dash.py --base 1e80128f` under the pinned renderer | `ab0b9185` | all rc 0 |
| `submodule_boundaries.gen.py --check` (+selftest), `DOC_MAP.gen.py --check` (+selftest), `gen_module_matrix.py --check`, `check_submodule_docs.py`, `check_diagram_pngs.py`, `check_solution_docs.py`, `check_sh_idiom.py`, `check_soc_sources.py` | `ab0b9185` | all rc 0 |
| `./syn/yosys/ooc.sh --record-rom-digests` | at each pin | rc 0 |
| OOC area `./syn/yosys/ooc.sh KL_pp_shadow` (own units, picked ranges) | `fd02ed11` vs dev `1e80128f` | rc 0 both. Head 61,878 LUT / 4,332 LUTRAM / 28,343 FF / 15 RAMB36 / 4 RAMB18 / 10 DSP / 2,432 CARRY4; base 61,979 / 4,332 / 28,334 / 15 / 4 / 10 / 2,428: **-101 LUT, +9 FF, +4 CARRY4** |

The sweep ran at `fc9648e3`; what follows it (`git diff --stat fc9648e3 ab0b9185`) is the gitlink to
`1be824f`, whose processor diff from `5fd298c` is three README/guide files, the parent's behave steps
and documents, the ROM ledger rows and the regenerated diagram. No Verilator suite compiles or reads
any of them. Area risk for the integrator: milan-fpga's AREA_BUDGET records 16 of 15,850 slices left on
the shipping route; yosys shows this change neutral (-101 LUT, +9 FF), but a Vivado route at adoption is
the deciding measurement (not run here: no route beside the sweeps).

## STOP check

Not met; no STOP posted.

- Top level: `git diff f65c8ff7 1be824f -- hdl/top/protocol_processor_top.sv` adds one port,
  `reboot_req_o` (the authorised one). No other port changes, and no parameter is added, removed
  or given a new default (`make check` `params`: top 29, guide 29, diagram 29, the same as base).
- Register map: none. The side-port map, CSR offsets and their documents are unchanged.
- New module ports below the top: `KL_aecp_engine.reboot_o`, `KL_aecp_notify.cmd_busy_o` and
  `KL_adp_engine.tx_busy_o`. All three are internal and connected only inside
  `protocol_processor_top` and the unit benches, so none of them reaches the parent.
  The parent instantiates only the top (`KL_pp_shadow`), and its single required edit is the
  open `.reboot_req_o ()`.

## Acceptance items

| Item (issue #203 / assignment) | Met by |
|---|---|
| REBOOT of ENTITY 0: SUCCESS, echoing the command | changes 6-10; RBT6 and RBT8 byte-exact |
| another descriptor type: NOT_SUPPORTED | change 7; RBT2 (and RBT4b under a lock) |
| non-zero index: NO_SUCH_DESCRIPTOR | change 10; RBT3 (and RBT4c under a lock) |
| short command: BAD_ARGUMENTS | change 7; RBT1 at cdl 12 and 14 |
| another controller holds the entity: ENTITY_LOCKED / ENTITY_ACQUIRED | change 10 (CHECK_LOCK); RBT4. ENTITY_ACQUIRED cannot arise, because ACQUIRE_ENTITY is NOT_SUPPORTED (Milan 5.4.2.1); RBT5 shows it |
| ENTITY_DEPARTING before the request if advertising, clause cited | change 4; Milan v1.2 5.6.3.3, 5.6.3.5.8, 5.6.3.5.11, Table 5.51; IEEE 6.2.4.1.3, 6.2.5.2.2 (6.2.1 and 6.2.6 placed in "Design decisions"); RBT6 (one DEPARTING, before the request), RBT8 (not advertising: none) |
| `reboot_req_o` only after the SUCCESS response's transmit-done | change 5; RBT6 order, RBT7 (MAC holds the last byte 30 ms: request stays 0); arm `rbt-request-at-acceptance` KILLED |
| no further command accepted after it | changes 2 and 8; RBT6 (queued command never served; AEM, ACMP and ADP unanswered); arms `rbt-rx-gate-dropped`, `rbt-engine-hold-dropped` KILLED |
| pulse or level stated in the interface documents | change 16 (02 reset rule 6, F02.10: held level), change 17, port comment (change 1) |
| REQ-FWX-001, GAP-13, the AECP command model, the compliance review entry | changes 13-15 |
| tests for every status, plus the mutant that raises the request before the response | section RBT (79 checks); 17 `rbt-*` arms, all KILLED |
| parent consumer gate with the port left unconnected | "Scratch-parent consumer gate" above |
| only `reboot_req_o` added at the top | "STOP check" above |

Every acceptance item is met, so PR-BODY.md carries "Closes #203".

## Not done (by the assignment's rules)

No push, no PR, no merge or rebase, and no edits to any issue or PR comment. On #203 the only
posts are TAKEN and REVIEW READY. No hardware or bench access, no flashing and no Vivado route.
The scratch parent's push URL is disabled and it was never pushed. Sub-agents were not used.

## Receipts

Everything cited is under `receipts/`. Each directory has an `INDEX.md` listing every file in it and
below it, with bytes and a truncated sha256, generated from the files present. Host paths are
replaced by placeholders (`<work>` a disposable clone, `<runs>`, `<parent>`, `<lane>`, `<home>`,
`<tmp>`). A file over 200 KB, or a binary, is not copied. It is listed with its size and full
sha256 in a `RAW-RECORDS.txt` beside the copies.

| Directory | Holds |
|---|---|
| `records/` | `processor-records.txt` (origin check, base, head, tree, commit list, diff stat), `parent-records.txt` (scratch parent commits, gitlinks, push URL) |
| `processor/head-1be824f/` | `make check`, `run_suites` (`suites.txt`), the executed `check-req-tags` and its evidence, section RBT alone |
| `processor/early-1fde6ea/` | the early `run_suites` |
| `processor/portability-5fd298c/` | `lint_hdl.sh` under 5.052 and 5.050, `syn/yosys/run.sh`, elab guards (yosys) |
| `campaigns/<driver>-<head>/` | one per campaign in "Gates run": command, log, rc and per-arm output. `d3-5fd298c/UNION.txt` and `acmp-5fd298c/UNION.txt` reconcile each two-part campaign against the driver's own arm list |
| `campaigns/rbt-arms-first-run-6c04588-tree/` | the first run of the 17 `rbt-*` arms, alone |
| `parent/sweep-fc9648e3/`, `parent/full-tally/` | the four shard logs and the tally |
| `parent/static-ab0b9185/`, `parent/docs-generators-ab0b9185/` | the static, behave, elaboration, xvlog, feature and documentation gates |
| `parent/rom-digests/`, `parent/ooc-area/` | `ooc.sh --record-rom-digests` at each pin; OOC area of head and base |
| `parent/findings/` | the four adoption findings, each with its failing run and its passing trial |
