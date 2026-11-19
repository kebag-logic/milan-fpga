[A801] REVIEW READY
Commit: 0d1eb8e4c5821e9431097950882659f2083d96ba (`951-redeclare`, on the flip train's head `0839453f`, PR #945; for `dev-soft-core`)

Changed:
- `sw/firmware/ctrl/srp/srp_mbx.c`: a withdrawn Talker's changed destination now waits two of the longest LeaveAll periods. Each is 1.5 x LeaveAllTime (IEEE 802.1Q-2018 10.7.4.3; Milan v1.2 Table 4.3), plus the JoinTime and THE TRANSMIT's term as they were (#665's ruling of 2026-11-19, item 2).
  - LeaveAllTime is named once (`SRP_LEAVEALL_CS`, 1000 cs), and both the participants' configuration and the hold-off read it. `SRP_LEAVEALL_LONGEST_CS` is 1.5 times it. `SRP_REDECLARE_CS` is 3,023 cs at 1x1/1if, 3,027 at 8x8/1if and 3,030 at two interfaces (2,023, 2,027 and 2,030 before).
  - A compile-time check refuses a hold-off past `held_cs`'s 16 bits. It adds no code: the images are byte-identical with and without it.
- Tests: `srp_talker.cpp`'s horizon is stated from the clauses, 2 x (10 s + 5 s), and its two hold-off tests are renamed `...WaitsTwoLongestLeaveAllPeriods` and `...AfterTheLatestLeave`. The composed MAAP conflict test (`SrpGate.F895ARangeLost...`) holds the source at 29 s and declares it by 31 s.
- Plants: two new ones put back the old value (`talker-hold-off-two-leavealltime-periods`, and `...-after-a-conflict` on the composed test). The one-LeaveAll and drop-a-term plants are restated on the new terms, and three LeaveTime plants' needle names `SRP_LEAVEALL_CS`.
- Docs: `srp/README.md`, `MAILBOX_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md` section 13 and `ctrl_service_budget/README.md`. No bound, mailbox contract, RTL or lwSRP change.

Validation (every gate at the code head `4224df63`; the commit after it is docs only. The images and the CPU legs were built at `e5dee83b`, and `4224df63`'s 20 images are byte-identical to them):
- Firmware gate, `test_ctrl_firmware.py --require-rv32 --self-test`, 4 shards: PASS. The suites give 74 verdicts, none failed. The control campaign catches 825 of 825, and the AECP and SRP campaigns 366 and 513 `[ok]` lines, none escaped. That includes 106 `[ok] talker-` lines, the 53 Talker plants at 1x1/1if and 8x8/2if.
- The old value put back fails by name at both points: `ChangedDestinationWaitsTwoLongestLeaveAllPeriods` (the changed destination declared at 20,630 ms of model time, where the Leave's time plus 30 s is 30,570), `...AfterTheLatestLeave`, `DestinationChangeWhileValidWithdrawsTheOld`, `ResetKeepsAnUnchangedSourceAndHoldsAMovedOne`, and the composed conflict test at 8x8/2if.
- `fw_coverage.py --selftest` and `--check`: PASS (40 files).
- Twin, twin-plants, twin-maps and twin-maps-plants: PASS, 0 findings, every plant refused.
- Docs workflow steps: PASS, 104 of 104 at `0d1eb8e4`, tracked files unchanged after them. The candidate's own `act_ci.py` self-test is not run: AGENTS.md runs it only inside the CI job. Installs are skipped, and the two builder legs run apart. Both end-station builder legs: PASS, each with one NOT RUN arm that the tree itself declares. Leg 0's first run shared a clone with the docs steps and was refused at its end, while `check_entity_shape.py --self-test` held a planted control in `tb/verilator/csr/Makefile`; on its own clone it passes.
- Image diff, base `0839453f` against this head, at 20 images (the platform's 4, the size fixture's 4, the CPU budget harness's 12). The base's budget images equal the train's recorded hashes, 12 of 12.
  - In every image, `srp_mbx.o` is the only linked input that differs. In it, `li a3,2023` becomes `lui a3,0x1; addi a3,a3,-1073` (likewise 3,027 and 3,030), 4 bytes more in `declare_sources`.
  - Each image was linked again with its relocations kept, and its loadable bytes equal the built image's. With every address field named by its symbol, head and base differ in those three lines alone.
- Release (all-fabric) image: byte-identical. `bios.bin`, `bios.elf`, the ROM and RAM init files and the archive's member are equal, and so is the gateware outside its date comment.
- CPU rows: they carry. No code path changes, but the hot code after `declare_sources` fetches 4 bytes later, so the legs were measured on both images at 1x1/1if and 8x8/1if. These were the `valid-destinations` arm (the legs the hold-off reaches) and arm A's `srp`, `backlog-owed`, `datapath-events` and `aecp` (and `aecp-largest-notice` at 1x1/1if).
  - Every leg exits 0, with no STATED line and no pass over the share. None of the 156 probes changes its verdict, and each image has only arm A's seven `backlog-owed` misses.
  - Arm A's figures move by at most 0.171 ms, on a 20 ms row. In the `valid-destinations` arm at 8x8/1if, rows that wait on a timer's phase move further: `srp.talker_loss` goes from 184.154 to 177.088 ms, of 220. A control image, built in scratch only, has the base's value with one `nop` after its store, so it has the head's placement. It gives 176.954 ms there, and every declaration row of that group equals the head's to the microsecond. Its `srp-talker` follows the head too: 34,434 passes against the head's 34,431 and the base's 33,619, the same count each second, and every row the head's. So the rows follow the code's placement, not the value.
  - `flip_grade.py --check` (either point), `load_grade.py --check` and `shape_costs.py --check` print the same output on both trees.

Acceptance criteria:
- The constant is derived from two longest LeaveAll periods plus the existing terms, about 30.2 s at one interface, never a mirrored literal: met (`srp_mbx.c:32-46`, `:526-527`).
- An image diff limited to that value, and the Talker tests, mutants and docs restated: met (above).
- The reference device's delay after a conflict: not measured. It needs bench access, which this change did not have.

Open risks/questions:
- Milan v1.2 Table 4.3 states LeaveAll with a +/-0.5 s tolerance. The ruling takes 1.5 x LeaveAllTime without it, and this change follows the ruling. A peer at the tolerance's edge makes two periods 31 s.
- The CPU rows were measured on a subset of the groups, not every group; the measured figures move a little, and no verdict moves.
- Not run here: the full suite sweep and act; the hosted gates and act follow the push.
