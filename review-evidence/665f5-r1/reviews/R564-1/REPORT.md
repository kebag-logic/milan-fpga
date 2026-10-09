[R564] NEGATIVE - exact head 1e68d1b62ef2facdf0e8dbad28a202297d433c61

# R564-1: internal independent review of PR #700 (issue #665, lane F5, AECP on the bare-metal core)

- Reviewed head: `1e68d1b62ef2facdf0e8dbad28a202297d433c61`, tree `ba72813fa634b7df0d9b937a144e427c6dd63ab6`, 19 commits on dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
- Scope reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue #665 body, assignment 6081266905, budget ruling 6081705916, directives 6009661573 and 6030870481, REVIEW READY 6084993566, issues #637 and #653, docs/reference/FR_NFR.md (NFR-SCOUT-02/03/08, sections 3.4.1 and 3.4.2), docs/design/MAILBOX_SPLIT.md, IEEE 1722.1-2021 clauses 6.2.2.15, 7.2, 7.4, 7.5, 9.2, 9.3 and 9.7.4, and Milan v1.2 5.3 and 5.4.
- Prior public review findings on PR #700: there are none at this head. The PR carries only the two review-start comments, so there is nothing to resolve or retain.
- Verdict: NEGATIVE. Five MINOR findings are open (F1 to F5). Every lens carries at least one of them, so no lens is covered clean in this round.

## Findings

### F1 MINOR - READ_DESCRIPTOR refuses ENTITY/CONFIGURATION reads whose configuration_index is not 0, and echoes the received index
- Lenses: Conformance, Robustness, Tests.
- Where: `sw/firmware/ctrl/aecp/aecp_commands.c:81-90` copies the index into the response and refuses `cfg >= configurations` before the lookup. `sw/firmware/ctrl/test/test_aecp.cpp:530` asserts BAD_ARGUMENTS for an ENTITY read with configuration_index 1, which pins the deviation.
- Authority / evidence: IEEE 1722.1-2021 7.4.5.1 says "For the ENTITY or CONFIGURATION descriptors, this field is ignored on receipt", and 7.4.5.2 says it is "set to zero (0) on transmit". Reviewer probe P1 (`probes/probe_tests.cpp`, receipt `receipts/probe-run.log`): ENTITY and CONFIGURATION reads with configuration_index 0x0001 and 0xffff return status 7 (BAD_ARGUMENTS) with an 8-byte body, and the response carries the received index. All five shapes have exactly one configuration (`receipts/descriptor-census.txt`), so every non-zero index is refused.
- Impact: a controller that sends a non-zero index, which the entity must ignore, cannot read the ENTITY or CONFIGURATION descriptor. Enumeration fails on a clause the core must tolerate.
- Required outcome: for ENTITY and CONFIGURATION, ignore the received configuration_index, serve the descriptor, and transmit 0 in the response. The unit test asserts the clause instead of the refusal. Any resulting wire difference against the fabric is recorded by clause.
- Verification: probe P1 passes, and a planted defect that restores the refusal is caught by the named test.

### F2 MINOR - SET_STREAM_INFO refuses the IEEE-ignored SAVED_STATE / STREAMING_WAIT flags and a command with no sub-command
- Lenses: Conformance, Robustness, Tests.
- Where: `sw/firmware/ctrl/aecp/aecp_commands.c:296-298` answers NOT_SUPPORTED whenever `flags != 0x20000000`. `sw/firmware/ctrl/test/test_aecp.cpp:706` asserts NOT_SUPPORTED for flags 0.
- Authority / evidence: IEEE 1722.1-2021 7.4.15.1 says "since SAVED_STATE and STREAMING_WAIT are not settable, they are ignored in the command". Milan v1.2 5.4.2.9 refuses only "unsupported sub-commands" (the XXX_VALID flags), and says a successful response sets MSRP_ACC_LAT_VALID "to the same value as in the command", so a command without that flag can succeed. Probe P2: flags 0x20000000 returns SUCCESS, while 0x00000000, 0x20000004 and 0x20000008 return status 11 (NOT_SUPPORTED). The fabric makes the same documented choice (`protocol-processor/hdl/aecp/KL_aecp_engine.sv:799-801`), so the core reproduces the fabric rather than the clause.
- Impact: a conforming controller that echoes SAVED_STATE or STREAMING_WAIT from a GET_STREAM_INFO response, or sends a no-op SET, has its presentation-time offset refused.
- Required outcome: ignore SAVED_STATE and STREAMING_WAIT in the command, answer SUCCESS to a command carrying no XXX_VALID sub-command, and keep NOT_SUPPORTED for an unsupported sub-command. Record the resulting difference against the fabric by clause.
- Verification: probe P2 passes, and the existing refusal cases for other VALID flags and for STREAM_INPUT still hold.

### F3 MINOR - Non-AEM, non-MVU AECP commands are silently dropped; IEEE 9.7.4 requires every HDCP_APM_COMMAND to be acknowledged, and the fabric answers them
- Lenses: Conformance, Robustness, Tests, Docs.
- Where:
  - `sw/firmware/ctrl/aecp/aecp.c:258-261` counts message types other than 0 and 6 as `ignored` and sends no response.
  - `sw/firmware/ctrl/test/test_aecp.cpp:1022-1024` asserts silence for message_type 2.
  - `sw/firmware/ctrl/test/aecp_wire_oracle.py:10-12`: the COMMANDS census covers only AEM codes and MVU.
  - `sw/firmware/ctrl/aecp/README.md:24-25` says "Other commands return NOT_IMPLEMENTED", and the PR body says "No other difference is accepted".
- Authority / evidence: IEEE 1722.1-2021 9.7.4 says "Each HDCP_APM_COMMAND AECPDU received shall be acknowledged by the ATDECC Entity. If the ATDECC Entity does not support HDCP IIA ..., it transmits an HDCP_APM_RESPONSE AECPDU with the status field set to NOT_IMPLEMENTED." Probe P3: message types 2, 4, 8 and 14 addressed to the entity produce no response (`ignored` increments by 1 each). The reference fabric answers every such type with NOT_IMPLEMENTED (`KL_aecp_engine.sv:1245-1275` and `:1743-1760`). This is therefore a wire difference that the differential never exercised and the difference ledger does not record.
- Impact: the core breaks a normative "shall". A controller's HDCP, ADDRESS_ACCESS or AV/C transaction to the Mark II core times out where the shipping fabric answers. The README and PR claim of a complete difference ledger is not true.
- Required outcome: answer at least HDCP_APM_COMMAND with HDCP_APM_RESPONSE / NOT_IMPLEMENTED per 9.7.4, and decide the other command message types by clause. The test asserts the decided behaviour. The differential or the contract records every remaining wire difference by clause, and the README and PR text match.
- Verification: the HDCP case of probe P3 passes, and the wire census either includes the non-AEM message types or the ledger records them.

### F4 MINOR - READ_DESCRIPTOR(ENTITY) serves the image's constant available_index instead of ADP's current value
- Lenses: Conformance, RTL, Tests.
- Where:
  - `sw/firmware/ctrl/aecp/aecp_commands.c:94` copies the stored ENTITY bytes.
  - `sw/firmware/ctrl/aecp/aecp.h:78-97` has no port through which the ADP owner's available_index can reach the core.
  - `sw/firmware/ctrl/test/test_aecp.cpp:528` and `sw/firmware/ctrl/test/aecp_wire_oracle.py:95` assert the image bytes, which pins the constant.
- Authority / evidence: IEEE 1722.1-2021 7.2.1, Table 7-1 offset 36, says "available_index: The available index of the ATDECC Entity. This is the same as the available_index field in ATDECC Discovery Protocol. See 6.2.2.15". Clause 6.2.2.15 increments it after every ENTITY_AVAILABLE. Probe P5: the core serves 0, the image constant, while the firmware ADP owner (`sw/firmware/ctrl/adp/adp.h:171`) advances its own counter. The fabric serves the same constant (there is no available_index source in `protocol-processor/hdl/aecp/`). The deviation is shared, but the standards oracle still rejects it.
- Impact: after the first advertisement the descriptor and ADP disagree. A controller that uses the descriptor field to correlate availability cycles is misled.
- Required outcome: the ENTITY descriptor's available_index equals ADP's current value at read time, for example through an observation port from the ADP owner in the composed application, with a test that advances ADP and then reads the descriptor. The alternative is a recorded owner or standards disposition of the clause.
- Verification: a test that sends N advertisements and then reads READ_DESCRIPTOR(ENTITY) sees N at offset 36, and a planted defect that serves the image byte is caught.

### F5 MINOR - One persistently unavailable observation starves every later descriptor's notifications and keeps the core permanently busy
- Lenses: Conformance, RTL, Robustness, Tests.
- Where: in `sw/firmware/ctrl/aecp/aecp.c:422-449`, `asynchronous()` scans descriptors in image order and returns `true` at the first pending event whose snapshot fails, without moving past it. `sw/firmware/ctrl/test/test_aecp.cpp:873-885` covers only the failing descriptor itself.
- Authority / evidence: Milan v1.2 5.4.5.2 and Table 5.22 require each listed notification to be sent "when the state of the entity changes". NFR-SCOUT-03 and FR_NFR 3.4.1 measure notification service from the occurrence. Probe P6: with only the STREAM_INPUT counters unavailable, the pending AVB_INTERFACE and CLOCK_DOMAIN counter notifications are never sent (0 of 1 each), and `aecp_poll` reports busy on 100 of 100 passes across a 5 s advance. This input is within the port contract: the README (`sw/firmware/ctrl/aecp/README.md:38-39`) says read ports may "explicitly report its absence", and the size fixture itself uses unavailable observers.
- Impact: a single missing or failed physical observer silently suppresses unrelated Table 5.22 notifications indefinitely (gPTP grandmaster, AS path, clock-domain and stream counters), and keeps the event loop busy.
- Required outcome: a failing snapshot is retried without blocking other descriptors' eligible events and without an unbounded busy loop. Tests prove the independence and the bounded retry.
- Verification: probe P6 passes, and a planted defect that restores the head-of-line blocking is caught by a named test.

## Suggestions (non-blocking)

- S1 (Conformance): NOT_IMPLEMENTED replies echo the command body. In probe P4, GET_ASSOCIATION_ID, GET_VIDEO_FORMAT and GET_VIDEO_MAP are answered with control_data_length 12. IEEE 1722.1-2021 9.3.5.3.3 asks for "a correctly sized response", and the fabric makes the same echo choice. Size the responses of known commands once processor #73's single command model supplies the table.
- S2 (Conformance, RTL): `aecp_name_offset()` (`aecp_commands.c:139-147`) treats VIDEO_MAP (24) and SENSOR_MAP (25) as named at offset 4, where IEEE 7.2.20 and 7.2.21 place `mappings_offset`. It also omits PTP_PORT (40), which carries `object_name` at offset 4 (7.2.36). No current shape reaches this. Correct it so the portable core cannot overwrite map structure if such a descriptor is ever generated.
- S3 (Conformance): a REGISTER_UNSOLICITED_NOTIFICATION with TIME_LIMITED set (IEEE 7.4.37.2) is accepted as a permanent registration and answered with flags 0. Either honour the 300 s timeout and its DEREGISTER notification, or record the clause disposition in the AECP contract.

## Residue (wording only)

- RES1: `docs/design/MAILBOX_SPLIT.md:568` reads "The AECP notification that will key on that port lands in F5." Exact fix: "The opt-in F5 bridge (`sw/firmware/ctrl/app/ctrl_app_aecp.c`) keys AECP notifications on that port."

## Assignment items at this head

| Item | Result | Evidence |
|---|---|---|
| (1) portable core behind `*_mbx.c` | Met | Core units include only `aecp*.h`, `wire.h` and `<string.h>`. Image parsing is in `aecp_image.c`, mailbox access in `aecp_mbx.c`, persistence in `aecp_nvm.c` and composition in `ctrl_app_aecp.c`. No intrinsics or heap |
| (2) READ_DESCRIPTOR for every descriptor type | Met except F1 and F4 | The core test reads all 42 shipping descriptors byte-exact, and each wire ingress reads 42. Every shape loads, and the largest descriptor is 452 B, below the 1472 B response limit (`receipts/descriptor-census.txt`) |
| (3) Milan 5.4 mandatory set, others NOT_IMPLEMENTED | Not met: F2, F3; see also S1 | Field layouts were checked against IEEE 7.4.1-7.4.46 and 7.4.76 and Milan 5.4.2.1-5.4.4.3: ACQUIRE NOT_SUPPORTED, LOCK, ENTITY_AVAILABLE flags, configuration, names including group_name at offset 180, format/rate/clock offsets, STREAM_INFO 84- and 56-byte forms with Table 5.9/5.11 flags, IDENTIFY control, START/STOP on Stream Inputs only, registration, AVB info, AS path, counters, audio maps and partitions, the GET_DYNAMIC_INFO list, MVU GET_MILAN_INFO and SUID |
| (4) notifications, #653, #637 | Met except F5 | 17 notification types are graded on the wire. The #653 order holds through the cross-channel commit-order merge (`docs/design/MAILBOX_SPLIT.md:132-140`) and `App.MediaUnlockedNoticeCannotPassAnOwedUnbindResponse`. The #637 restore, refusal and rollback are covered in the `Nvm.*` tests, including a real store power cycle |
| (5) per-interface state, processor #69 | Met | `registry[interface]` and per-interface MAC and egress. The two-interface wire run against `c9f74b6866a63dd3c0e4534724bfc07a86ad142b` passes 256 observations |
| (6) 100 % ratchet, no new exclusion, plant per check | Met | The 8 new production files are at raw 100 % lines and branches. Only `coverage.ratchet` changed under `sw/firmware/gtest/`. All 66 tests are named by plants, and 59/59 plants are caught |
| (7) wire differential by clause | Not met: F3 (unexercised, unrecorded difference); F1, F2 and F4 would each add a clause-recorded difference | Both the one- and two-interface runs pass with the four recorded differences. Only three refusal probes are compared on the wire |
| (8) latency vs 240 ms and T_svc | Met (desk bounds) | Reproduced maxima: 9.0061 ms (deferred START failure guard), 2.0069 ms (1 ms TX stall), 1.1573 ms (two-interface full fanout) and 1.0789 ms (one-interface fanout). All are below 10 ms and 240 ms with the stated 100 ns per access and 1 ms CPU allowances |
| (9) linked image, tiles, BSS consumers | Reported; not re-linked here | `size-matrix.json` is internally consistent. Spans 139072/151728/192240/219744 B equal the section sums plus 18 B of alignment. Nominal tiles, ceil(span/4608), are 31/33/42/48; with 32-bit packing, ceil(span/4096), they are 34/38/47/54. Largest shape at two interfaces is below 224 KB. The five largest BSS consumers are listed with reduction options |
| (10) no RTL, default and shipping image unchanged | Met | The diff touches only `sw/firmware/ctrl/**`, `sw/firmware/gtest/coverage.ratchet` and `docs/README.md`. No `hdl/`, `syn/`, `configs/`, builder or mailbox-contract file changes. `gen_mailbox.py --check` reports 0 findings |
| Processor #73 owed change stated | Met | `sw/firmware/ctrl/aecp/README.md:26-28` and the PR body's limitations |

## Executed evidence (reviewer, at the exact head; receipts in `receipts/`)

All runs used a disposable scratch clone of the review clone at the head, with lwSRP `9197193e`, processor `2ad2f845`, and a separate processor checkout at `c9f74b68` for the two-interface reference. The scoped simulator reports `Verilator 5.050 2026-07-01 rev v5.050`.

| Gate | Result |
|---|---|
| `test_ctrl_firmware.py --jobs 4` (normal bank: all arms including AECP at one and two interfaces, five image arms, the debug guard and the RV32I freestanding build) | rc 0, PASS; AECP composed arm 62/62 at each interface count |
| `fw_coverage.py --check --lwsrp third_party/lwSRP` | rc 0, PASS (30 files); the eight AECP files are at raw 100 % |
| `aecp_mutants.py --shard 0 2` and `--shard 1 2` | rc 0 each; 30/30 and 29/29 caught |
| `aecp_wire.py`, one interface (pin `2ad2f845`) | rc 0; 123 observations, 6 oracle controls |
| `aecp_wire.py`, two interfaces (`c9f74b68`) | rc 0; 256 observations, 6 controls per ingress |
| `make -C tb/verilator/mbx` (scoped 5.050) | rc 0; mbx mutants 5 of 5 caught |
| `gen_mailbox.py --check` | rc 0; 0 findings |
| `aecp_arms.py --app --asan` at one and two interfaces | rc 0; 62/62 each |
| `aecp_arms.py --mailbox --filter 'Latency.*'` at one and two interfaces | rc 0; maxima as in item (8) |
| Docs and code-quality subset: 21 commands, including docs_check, the em-dash check against the base, doc style, DOC_MAP, gen_toc check and anchors, module matrix, feature status, naming, port contracts, fail-fast, test evidence, hygiene, C++/Python/shell idiom, doc paths and ci_events | all rc 0. The nine code-quality gates first refused in the scratch clone because its submodules were unregistered, then returned rc 0 after registration |
| Reviewer probes P1-P6 (`scripts/run_probes.sh`) | P1, P2, P3 and P6 fail as described in F1, F2, F3 and F5; P4 and P5 are informational |
| Review clone integrity after all work | 1263 tracked blobs are byte-identical to HEAD, the index equals the HEAD tree, and the gitlinks are unchanged (`receipts/clone-integrity.txt`) |

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4, F5) | `aecp.c`, `aecp_commands.c`, `aecp_maps.c`, `aecp_mbx.c` and `ctrl_app_aecp.c` against IEEE 1722.1-2021 6.2.2.15, 7.2, 7.4.1-7.4.46, 7.4.76, 7.5.2, 9.2, 9.3 and 9.7.4, and Milan v1.2 5.3 and 5.4.1-5.4.5; probes P1-P6; wire verdicts | R564-1 | `1e68d1b62ef2facdf0e8dbad28a202297d433c61` |
| RTL (architecture, contracts, widths, error paths, backpressure) | UNCLEAN (F4, F5) | the port contract in `aecp.h:78-97`; buffer bounds in `aecp_rx`, `mvu`, `dynamic` and the map commands (all within 1514 B); timer arming, deferred START, completion cookies, cross-channel commit order; per-interface keying | R564-1 | `1e68d1b62ef2facdf0e8dbad28a202297d433c61` |
| Robustness | UNCLEAN (F1, F2, F3, F5) | malformed and truncated framing, foreign target, wrong interface, busy hold-off via `ctrl_loop_set_rx_ready`, full rings, unavailable observations, saved-state refusal and rollback, ASAN arms | R564-1 | `1e68d1b62ef2facdf0e8dbad28a202297d433c61` |
| Tests | UNCLEAN (F1, F2, F3, F4, F5) | `test_aecp.cpp`, `test_aecp_image.cpp`, `test_aecp_debug.cpp`, `aecp_mutants.py` (59 plants; all 66 tests named), `aecp_wire*.{py,cpp,hpp}`, the coverage ratchet; executed bank, coverage, mutants, wire, latency and ASAN runs | R564-1 | `1e68d1b62ef2facdf0e8dbad28a202297d433c61` |
| Docs | UNCLEAN (F3) | `sw/firmware/ctrl/aecp/README.md`, `sw/firmware/ctrl/README.md`, `docs/README.md`, the PR body, the author's REVIEW READY and the public packet; docs gates executed | R564-1 | `1e68d1b62ef2facdf0e8dbad28a202297d433c61` |

## Real limits of this round

- The linked RV32 images were not re-linked, because the runtime archives and runtime source roots were not reproduced here. Item (9) is judged on the published `size-matrix.json` for internal consistency and against the ruling, not on a reviewer link.
- This reviewer did not run:
  - the builder bank;
  - the saved-state bank (`test_ctrl_nvm.py`);
  - the inherited control, SRP and saved-state mutation tables (471/169/68/109);
  - the firmware bank's `--self-test`;
  - act;
  - hosted acceptance;
  - any hardware or physical calibration. Calibration is NOT RUN, and skips are not hardware proof.
- The differential compares only success paths plus three refusal probes. All other refusal bodies are graded by unit tests alone. The probes run on the host only.
- The latency results are desk bounds with explicit access and CPU allowances. Target timing, wire departure and complete call-chain stack depth are not established.

## Pending manager duties

- Hosted CI at the head: the snapshot (`receipts/hosted-checks-snapshot.txt`) showed 12 pass, 7 pending (Verilator shards 0/1/2/4, docs-check, firmware-unit, elaborate) and 1 skipped (physical gPTP, which runs only on schedule). Acceptance remains the manager's.
- Candidate merge validation (builder 48, native 5) and act on the current-dev candidate at the merge turn.
- Owner visibility: with 32-bit data packing, the largest shape at two interfaces needs 54 RAMB36 tiles, against the roughly 50 set aside in ruling 6081705916 (the nominal count at 4.5 KB per tile is 48). Routed proof is owed before the default flip. FR_NFR 3.4.1 also states that T_svc = 10 ms still awaits owner approval.
- Processor #73 adoption remains owed. F2 and the S1 response sizing touch the same command table.
- Carry RES1 to the residue checklist.

R564-1 FINISHED
