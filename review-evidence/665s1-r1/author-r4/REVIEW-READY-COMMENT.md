[A680d] REVIEW READY
Commit: `d33a5adc60cd93b34be41dfacf94daaec9d059c2` (branch `665-s1-faces`, on round 3's `44d95625`, from `dev-soft-core` `e76a755a`; PR #795)

Changed (round 4, six commits on `44d95625`; answering R701-3 6417591484 and R702-3 6417635453 under the round-4 assignment 6417644908):
- **F1, no promise of an unapplied value.** I chose the defer path by clause: a defined failure status within the deadline, not IN_PROGRESS. The project keeps its no-IN_PROGRESS policy and IEEE 1722.1-2021 9.3.2.6's 240 ms deadline (`docs/reference/FR_NFR.md`, the AECP rows). The core has a new `aecp.h` port, `applied`, false while an interface owes a publication or holds a commit not yet acknowledged (`aecp_face.c`). The core asks it at three points:
  - **After a command that changed state** (`aecp.c:348`). False there, the command answers ENTITY_MISBEHAVING within the service bound and notifies no one. That is the status the core already gives a datapath that misses its bound.
  - **Before LOCK_ENTITY, SET_CONFIGURATION, SET_STREAM_FORMAT, SET_STREAM_INFO, SET_NAME, SET_SAMPLING_RATE, SET_CLOCK_SOURCE, SET_CONTROL and ADD_/REMOVE_AUDIO_MAPPINGS** (`aecp.c:339`). False there, the command answers ENTITY_MISBEHAVING, echoing its data, before it changes anything. So no second value joins the owed one.
  - **At a lock expiry** (`aecp.c:462`). False there, no unlock notification leaves.

  Reads, registrations and other notifications continue, so service stays bounded. The held value reaches the datapath when it acknowledges, and a read meanwhile reports it. Once the poll has published the interface whole, changes are taken again. `ctrl_app_open_aecp` opens AECP only once every interface has acknowledged the initial publication (`aecp_face_open` returns that).
- **Tests.**
  - `Face.ALateCommitIsOwedAndPublishedAgainWhole` now checks ordering: refusal, no notification, nothing written, then recovery with commit and acknowledgement before the response.
  - New: `Face.APartialAcknowledgementFailsTheChangeUntilEveryInterfaceTakesIt`, `Face.AMissingAcknowledgementRefusesEveryChangeAndNotifiesNothing` (ten refusals and the timed-out command within the service bound; lock expiry), `AppFaceUnacknowledged.AecpOpensOnlyOnceTheInitialPublicationIsAcknowledged`, `Core.AChangeThePlatformHasNotAppliedPromisesNothing` (the core on a mock port).
  - All run at one and two interfaces. Twelve new planted defects, each caught by its own words (108 of 108 in the AECP campaign).
- **Docs.**
  - `MAILBOX_SPLIT.md`: the writer's ordering, the failure path and its clause; the verification rows at this head, with the census at 138 arms and 43 rules, the bench's common checks (523 at one interface, 530 at two) and the AXI4-Lite build's own 45, the model's 488 of 530, the face block's bench row, the AECP face's host-test row, and seven quick plants.
  - `aecp_face.h`, `aecp.h`, the aecp and ctrl READMEs, and the architecture sentence.
  - R702-3 F2: "the firmware's saved-state store" in `mailbox.yaml`, regenerated through `gen_mailbox.py --write`. Only that phrase moved, in `KL_mbx_pkg.sv`, `mbx_contract.h` and `MAILBOX_CONTRACT.md`.
  - Both residue lists, comment-only. For "T0 has failed" I took R702-3's wording, "the timing check has failed".
- **Memory ledger** (`SPLIT_CONTROL_MEMORY.md` section 5, base `e76a755a`, one runtime): 37.0 / 40.5 / 50.5 / 57.0 RAMB36. The path adds 392 to 400 B of `rom` and 16 B of `sram`. The 8x8 one-interface point moves from 50.0 to 50.5, within 56. The 8x8 two-interface point stays at 57.0 under its override, with 104 B of `rom` left before 57.5. It is still refused without the override, and the override is still refused at the other three points.

Probes (both byte-identical to the reviewers' manifests):
- **R701-3 `response_probe.py`.** Applied to a copy of the test directory, the named test passes at one and two interfaces at this firmware. At `44d95625` it fails with 255 against 0, as R701-3 recorded. Its anchor line is kept verbatim in the reworked test, now after recovery.
- **R702-3 `probe_ack.py`.** Its assertion "successful response must not promise an unwritten F value" holds (`response_status=10 core_identify=255 mailbox_identify=255`). Its test still fails, only at the fixture's default status check in its two `receive(24, ...)` calls: "status for command 24", expected 0, actual 10. The probe expects SUCCESS from both commands sent while the acknowledgement is withheld, which item 1 forbids. Its script exits 1 because it exits 0 only on observing the defect. At `44d95625` the assertion fails and the script exits 0.

Validation (round 4; each gate ran at `d33a5adc` or at an ancestor that differs only in what the gate does not read; receipts and the gate table are with the manager's handoff):
- `make -C tb/verilator/mbx` (pinned Verilator 5.050): rc 0. 523 Wishbone, 568 AXI4-Lite, 32 cosim; at two interfaces 530, 575, model 488; quick plants 7 of 7.
- `make -C tb/verilator/mbx mutants`: rc 0, 199 of 199.
- `gen_mailbox.py --check --crosscheck` and `--selftest`: rc 0, 0 findings.
- `publication_census.py --check --selftest --jobs 4`: rc 0. 217 ports per shape (C 25, F 28, R 34, E 6, M 14, G 110); 138 arms and all 43 rules in 949 s locally.
- `test_ctrl_firmware.py --require-rv32 --self-test`, four shards: rc 0 each. Shard 1 catches 528 of 528; shard 2's AECP campaign 108 of 108.
- `aecp_mutants.py` (whole, four shards): 108 of 108.
- `aecp_arms.py --app` at one and two interfaces: 93 of 93 each.
- `fw_coverage.py --check`: rc 0, 31 files at 100 %. `aecp.c` 372/372 lines and 318/318 branches; `aecp_face.c` 172/172 and 148/148.
- `ctrl_boundary.py --require-rv32 --selftest --without verilator` and `--only verilator` (pinned Verilator): rc 0 each, PASS (1,082 s and 648 s).
- `test_builder.py --require-rv32`: rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11 needs a local Arty build report).
- `test_ctrl_memory.py`: rc 0. `cd tests && behave`: rc 0, 406 scenarios.
- `lint_rtl.py --check`: rc 0, 89 against a ratchet of 89. `xvlog_gate.py --check` (host lock): rc 0. Yosys on `KL_mbx`, `KL_mbx_wb` and `KL_mbx_axil`: rc 0, cells 420,989, 5 and 136, as at the measured OOC head, so the OOC figures stand.
- Docs gates (the docs workflow's 69 commands): 69 of 69 rc 0 at `d33a5adc`.
- All-fabric export of the five shipped configs at base `e76a755a` and head `989c9f53` (`milan_soc.py` and `hdl/` unchanged after): normalised digest identical per config, and `compare_same.py` clean.
- Four-shard Verilator sweep at `a6519873` (pinned Verilator 5.050, sv2v 0.0.12): rc 0 each. 64 of 64 suites, 2,191,124 checks, 0 failures, 0 timed out. The only declared skips are `tsn_fuzz`'s field campaigns without tsn-gen.

Acceptance criteria:
- **Round 4, items 1 to 3:** met, with the R702-3 probe exactly as stated above.
- **Round 3, standing:** met. The census, contract 2.3 additive (minor 3), the BRAM ledger (S14 owes the 8x8 two-interface tile), and the all-fabric export digest-identical.
- **#665:** stays open.

Open risks/questions:
- 104 B of `rom` remain at the 8x8 two-interface point before it would plan 57.5, which the override refuses.
- While a commit is held, a read reports the value the held block carries, and every state-changing command is refused, including those whose values the face does not carry.
- A release or change applied by a late acknowledgement is not notified afterwards.
- These are documented in `MAILBOX_SPLIT.md` "The firmware's writer".
