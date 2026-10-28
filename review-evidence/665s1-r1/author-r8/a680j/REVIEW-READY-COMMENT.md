[A680j] REVIEW READY
Commit: `bdad673a7824d84c922d771ff5950e8f69083c27` (three commits on `27c54171`; nothing pushed)
Changed (answering ruling 6461910715, option (c)):
- `tb/verilator/ctrl_service_budget/split_soc.py`: the harness's SoC acknowledges each face commit at the contract's bound.
  - `StimulusMailbox.slowest_ack` pulses `fw_ack_p_i` `FACE_ACK_CYCLES` bus cycles after that interface's `fw_send_o` rises. The bound is the generated constant from `mailbox_model.constants`, 64 in contract 2.3.
  - Every other face input stays idle by name.
  - Before the SoC is built, `ack_deviations` checks the bound against the firmware's `MBX_FACE_ACK_CYCLES`. It also simulates the acknowledgement in migen against `KL_mbx`'s commit rule. The build refuses on any deviation.
- `tb/verilator/ctrl_service_budget/README.md`:
  - the one difference from `CtrlMailbox` and why: a CPU budget needs the slowest acknowledgement the contract allows;
  - what this head boots and measures, and which controls are caught here.
- The PR body states the difference too.
- Everything else done at `27c54171` (F1, F2, W1) is kept.

Validation (all at `bdad673a` unless noted):
- **The build's acknowledgement check:** two planted mutants, the pulse one cycle early and the one-cycle datapath, are each refused by a real build, rc 1, with the deviation named.
- **Real harness builds, to the measurement** (at `0eda061a`; `bdad673a` changes only the README):
  - arm A `aecp`: 25 of 25 probes at 1x1/1if and 39 of 39 at 8x8/2if, 0 refusals, 0 T_svc misses;
  - arm B `aecp-fanout`: 1x1 4 of 14 instances miss (S2: 3); 8x8 22 of 22 miss (S2: 22), 4 over the ceiling (S2: 3);
  - also arm A `aecp-fanout`: verdicts as S2's (1 of 9; 13 of 13).
- **Against [A680i]'s one-cycle probe:** arm A is identical, cycle for cycle. The firmware's first F_STATUS read after a commit comes later than 64 bus cycles. A probe beyond the contract, at 256 bus cycles, adds one read per commit (+170 CPU cycles).
- **Against S2's recorded figures**, the differences S1's firmware explains:
  - the `applied` read: +1 access a command an interface;
  - LOCK_HELD's publication: +12 accesses, +0.21 ms at 1x1;
  - SET_NAME's publication on every interface: +21 accesses at 1x1, +42 on 8x8 if0;
  - arm B's settings publications: +12 to +19 accesses;
  - SET_CONFIGURATION's every-entry publication: +131,573 CPU cycles at 1x1 and +439,826 at 8x8 (below);
  - the rest is phase. S2's one 8x8 arm A miss, `get_configuration.if0`, measures 7.675 ms here (S2: 14.822 ms).
- **Gates, all rc 0:**
  - harness self-test: 89 PASS, 64 mutants caught;
  - R701-7's three probes, unchanged;
  - `test_ctrl_memory.py`;
  - `gen_mailbox.py --check`: 0 findings;
  - the docs workflow: 69 of 69, with the bare-metal scope gate;
  - the docs CI self-tests: 16 of 16;
  - `behave`: 406 scenarios;
  - rtl-fast `firmware-boundary` steps: 2,864 sources, PASS;
  - `ctrl_boundary --only verilator`: PASS;
  - `test_ctrl_nvm.py`: 435 tests;
  - the firmware self-test, four shards in separate units: 61, 528, 137 and 280 plants, 0 escaped;
  - `fw_coverage.py --check`: 100 %;
  - `test_builder.py`: all pass except gate 11, which needs a local Arty build report;
  - the linked images at four points: byte-identical to the merge round's; 57.5 only with the ledgered override;
  - the four-shard Verilator sweep: 64 of 64 suites and 2,191,124 checks, the merge round's counts.
- **The `slow-adp-rx` control** is caught: 24.614 ms.

Acceptance criteria: ruling items 1 to 4 met (evidence above and in the PR body).
Open risks/questions (decisions for the manager, not changed here):
1. **The `as-built` control escapes on this branch**, also at the merge head `0052e62e`.
   - The 1x1 image's start code copies `.data` from 0x197b0 (bit 15 set) first. So #791's decode defect surfaces as a load access fault, cause 5 at pc 0x20, before any fetch above 0x8000.
   - The control requires cause 1 (`run.py:262-264`), so it prints ESCAPED, rc 1.
   - (a) Widen the control to an access fault, cause 1 or 5, or (b) keep cause 1 and make the fixture's first rom access above 0x8000 a fetch.
2. **SET_CONFIGURATION's face publication** (`aecp_face.c` `publish(..., every)`) looks up every stream entry through `aecp_find`, a linear search.
   - In arm B it takes the 1x1 row from 9.233 to 11.660 ms (over T_svc), and the 8x8 if0 row from 19.788 to 26.980 ms (over the 24 ms ceiling).
   - Arm A does not run that command.
   - A firmware follow-up, outside this round.
