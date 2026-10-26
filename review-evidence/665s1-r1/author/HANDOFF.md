STATUS: REVIEW READY (round 3, executor [A680c]): head `44d95625bde2c46d7070c090fc29ed0ba85ab64a`, every gate rc 0

# #665 lane S1 ([A680c]): the processor's other faces, census and contract 2.3

- Branch `665-s1-faces`, from `dev-soft-core` `e76a755a` (`origin` is `kebag-logic/milan-fpga`;
  `git merge-base HEAD origin/dev-soft-core` is `e76a755afc0536453161e3cd33f6f4d2dcd7641f`).
- Round 2's seven commits (`05d0b575`..`bd3f5d94`) stand unrewritten; round 3 adds eight (15 one-line
  commits on `e76a755a`; 54 files, +8,155 / -229). Nothing pushed.
- Assignment 6409739310; rulings 6410169666 (round 1) and 6412739248 (round 3, overrides both);
  decisions 6409738976; branch policy 6409455089; owner clarification 6410301079.
- TAKEN: #665 comment 6412971991; REVIEW READY: 6416542628.
- Round-2 handoff: `../665s1-a680b/HANDOFF.md` (changes, checks and plants of rounds 1 and 2);
  round-1 handoff: `../665s1-a680/HANDOFF.md` (the 217-port table, probes).

## Round-3 work list (ruling 6412739248)

- [x] TAKEN posted (6412971991)
- [x] 1. The 8x8 two-interface point ledgered at 57 RAMB36 in `SPLIT_CONTROL_MEMORY.md` section 5, owed to S14
- [x] 1. Named planner override for that point alone; the default and the SoC build keep refusing; tests and plants
- [x] 1. The other three points plan 37.0, 40.5 and 50.0 RAMB36, within 56
- [x] 2. PR body states the shared `-fno-stack-protector` runtime
- [x] 3. Whole firmware self-test (four shards), `test_builder.py --require-rv32`, `cd tests && behave`
- [x] 3. Four-shard sweep at `44d95625`: 64 of 64 suites, 2,191,124 checks, 0 failures
- [x] 3. `KL_mbx` OOC under the host lock: 5,515 LUT, 7,632 FF, 1 RAMB36, 10 RAMB18 (base repeats 3,585 / 4,114 / 1 / 10)
- [x] 3. All-fabric export, five shipped configs: normalised digest identical, base and head
- [x] REVIEW READY posted (6416542628)

## Round-3 changes (file:line, reason)

`80aa0372`, the ledgered override (ruling 6412739248 item 1: an explicit, named override used only by
that point's measurement; the default build path stays refusing):
- `sw/litex/ctrl_memory.py:94` the `budget` rule's text names the ledgered point and the override's
  misuse; `:166` `Plan.budget` and `Plan.ledgered` (the summary adds `ledgered` and `ledgered_tiles` only
  when set, so the default summary is unchanged); `:188` `Ledgered`, `:204` `LEDGERED`, the one point
  `8x8-two-interfaces` at 57.0 RAMB36, owed to S14, recognised by the image's own symbols (`nvm_stage`
  13,264 B, the shape; the size fixture's `image_allocation[MBX_N_IF]`, 16 B, two interfaces); `:210`
  `ledgered_tiles` refuses an unknown name and any image without both symbols at their sizes; `:337`
  `plan(..., ledgered=None)` holds every image to 56 unless named; `:415` `plan --ledgered-point`.
  `milan_soc.add_ctrl_memory` is unchanged and names none, so every SoC build stays refused past 56.
- `sw/firmware/ctrl/test/ctrl_srp_image.py:109` `--ledgered-point` (split layout only, `:121`), passed to
  the plan at `:199`: the measurement of that point links through this script, which plans the image.
- `sw/litex/test_ctrl_memory.py:186` `Layout.interfaces` writes `image_allocation`; `:196` `LEDGER_NAME`,
  `OVER_ONE` (the point at 57.0) and `OTHER_POINTS`; `:304` ten `budget` refusal rows (no override; the SoC
  build's `add_ctrl_memory`; 57.5; the override on the three other points and on an image without the
  table; on another point within the budget; two unknown names); `:324` `ledger_arms` (the ledger holds
  the one ruled point; the override plans 57.0 and says so in its summary; a default plan names no point;
  `plan --ledgered-point` accepts its point and refuses the four others).
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 3: the rule row, the override paragraph, what the test plants.

`cd7a0e39` and `c9abfc2d`: `SPLIT_CONTROL_MEMORY.md` section 5, the ledger (four points, base against the
head's firmware `308852d1`, the 8x8 two-interface point over by 1 tile and owed to S14, the flip's rule);
section 6, the reproduce commands name the override. `c9abfc2d` moves the figures to the event decode fix
(16 B more `rom` at each point, the same tiles).

`7464b876`: `docs/design/MAILBOX_SPLIT.md` "Measured area", the `KL_mbx` OOC with the face block.

`b6e35903`, a round-2 defect found by the whole firmware self-test (shard 1 at `7464b876`: 526 of 527,
`unknown-event-decoded-as-tick` ESCAPED):
- `sw/firmware/ctrl/mbx/mbx.c:479` `event_decode`'s last branch names `AVB_INFO_CHANGED`,
  `AS_PATH_CHANGED` and `AMAP_LIVE_WRITE`. Round 2 made it a catch-all `else`, so an event of a type the
  contract does not define was decoded as a counted face event (`count`, `now_ms`); the driver's rule (D9)
  is that such an event is taken with no field decoded, as the base did.
- `sw/firmware/ctrl/test/test_unit_driver.cpp:110` D9 fills words 1 to 3 and requires every field of
  `mbx_event` to stay 0, the face events' included (it read five before).
- `sw/firmware/ctrl/test/ctrl_mutants.py:349` `unknown-event-decoded-as-tick` re-pointed (its edit no
  longer compiled against the new chain, which the campaign counted as ESCAPED); `:353` a new defect,
  `unknown-event-decoded-as-a-face-count`, which is round 2's catch-all.

`b48db8fa`: `sw/litex/ctrl_memory_elf.py` (new) holds the memory test's ELF32 writer and byte edits,
moved from `test_ctrl_memory.py` with no change but reading `RAM`'s origin from `ctrl_memory`, which the override's arms had taken to 1,049 lines, over the
1,000-line module limit (`check_py_idiom.py`: "long module 11 > ratchet 10"); it is now 985.

`308852d1`: `sw/firmware/ctrl/test/ctrl_configs.py:179` lists round 2's `sw/mailbox/census_ports.py` in
`OUTSIDE`. It names the firmware's tree in its text and compiles nothing, so the TSN stack boundary gate
(`ctrl_boundary.py --require-rv32 --selftest`, an `rtl-fast` job) refused it as an unregistered builder.

`44d95625`, a round-2 bench defect found by the full `make mutants`:
`tb/verilator/mbx/suite_face.hpp:708` `check_face_timing` idled `held - 1u` cycles; when a defect keeps the
request from opening, `held` is 0 and that is 2^32 - 1 cycles, so the arm `wb-address-shifted` never
finished and the campaign, which has no per-arm timeout, never ended. It now idles 0 then; T0 has failed.

## New checks, planted mutants, failing words

- Override (probe `probes/ledger_mutants.py`, through `test_ctrl_memory`'s own `mutated` and
  `mutant_arms`, control first): 11 of 11 caught (`receipts/ledger-mutants-at-80aa0372.txt`, again at `b48db8fa` in `ledger-mutants-b48db8fa.txt`). E.g. "the override
  applies to every image" caught by "`plan --ledgered-point 8x8-two-interfaces` accepts its point and
  refuses ... (exit codes [0, 0, 0, 0, 0])"; "the SoC build takes the override" by "add_ctrl_memory
  builds the image: raised Refusal"; "a second point in the ledger" by "an override the ledger does not
  hold, on the image of the point it names: accepted"; "a second point added to LEDGERED" by "the
  ledger holds the one ruled point". A first run, before `80aa0372` was committed, caught 9 of 10: "a
  second point in the ledger" lived, because the unknown-name arm used the two-interface image, which
  that point refuses anyway; the arm on the image of the point the name claims was added before the
  commit. Not added to the tree's `MUTANTS`: `docs/testing/TESTING.md:753`
  counts those (forty-four), and that file is in a release lane's file map.
- D9 (probe `probes/d9_mutants_only.py` over `ctrl_mutants.campaign`): 2 of 2 caught, each by
  "D9 an event of a type the contract does not define is taken with no field decoded"; in the whole
  campaign (shard 1) 528 of 528.
- The bench fix: the full `make mutants` finishing, `wb-address-shifted` caught (see the gate table).

## Gate table

Final head `44d95625`. A gate run at an earlier head counts for it only where no later commit touched
anything the gate reads; the column says so.

| Gate | Head | Result | Receipt (`receipts/`) |
|---|---|---|---|
| `make -C tb/verilator/mbx` (Wishbone, AXI4-Lite, cosim, `run-if2`, quick plants; pinned Verilator 5.050) | `44d95625` | rc 0: 523, 568, 32; at two interfaces 530, 575, model 488; 7 of 7 | `gates/mbx-make.txt` |
| `make -C tb/verilator/mbx mutants` | `44d95625` | rc 0: four positive controls, 199 of 199 caught, 606 s | `gates/mbx-mutants.txt` |
| `gen_mailbox.py --check --crosscheck`; `--selftest` | `44d95625` | rc 0, 0 findings; rc 0, 0 arms failed | `gates/gen-mailbox-*.txt` |
| `publication_census.py --check --selftest --jobs 4` (pinned sv2v 0.0.12) | `7464b876`; nothing it reads changed after | rc 0 in 992 s locally (round 2: 14:48.8; hosted estimate within 27 min) | `gates/census.txt` |
| `test_ctrl_firmware.py --require-rv32 --self-test`, its four exhaustive shards | `44d95625` | rc 0 each; shard 1: 528 of 528 mutants caught | `fw/final-44d95625/shard-*.txt` |
| `fw_coverage.py --check` | `44d95625` | rc 0, 31 files at 100 %; `mbx.c` 302/302 lines, 150/150 branches | `gates/fw-coverage-check.txt` |
| `aecp_mutants.py --output` (whole) | `b48db8fa`; nothing it reads changed after | rc 0, 96 of 96 | `gates/aecp-mutants.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --without verilator`; `--only verilator` | `44d95625` | rc 0 PASS (1,179 s); rc 0 PASS (671 s) | `gates/ctrl-boundary-*.txt` |
| `test_builder.py --require-rv32` | `b48db8fa`; nothing it reads changed after | rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN": gate 11 needs a local Arty build report this host lacks | `gates/test-builder.txt` |
| `cd tests && behave --no-capture -f plain` | `b48db8fa`; nothing it reads changed after | rc 0: 14 features, 406 scenarios, 1,977 steps | `gates/behave.txt` |
| `test_ctrl_memory.py` (LiteX interpreter) | `c9abfc2d`; the later commit touches only the bench | rc 0, 0 failures | `gates/test-ctrl-memory.txt` |
| override plants (`probes/ledger_mutants.py`) | `b48db8fa` | 11 of 11 | `ledger-mutants-b48db8fa.txt` |
| `lint_rtl.py --check`; `xvlog_gate.py --check` (host lock); Yosys on `KL_mbx`, `KL_mbx_wb`, `KL_mbx_axil` | `44d95625` | rc 0 (89 <= 89); rc 0 (0 findings); rc 0 | `gates/lint-rtl.txt`, `gates/xvlog-gate.txt`, `gates/yosys-mailbox-tops.txt` |
| docs gates (`probes/docs_gates.sh`: the docs workflow's 69 commands) | `44d95625` | 0 failed | `gates/docs-gates.txt` |
| linked images, four points, base `e76a755a` against the final firmware (`308852d1`, unchanged after) | `308852d1` | 37.0, 40.5, 50.0 within 56; 8x8 two interfaces 57.0 by its override, refused without it (exit 2); the override refused on the other three (exit 2) | `linked-images-final.txt`, `images-final/` |
| `KL_mbx` OOC (Vivado 2026.1, host lock), RTL unchanged since `bd3f5d94` | `bd3f5d94` and base | head 5,515 LUT, 7,632 FF, 1/10, WNS +0.123 ns, 12,761 nets routed; base 3,585, 4,114, 1/10, +0.151 ns | `ooc/` |
| all-fabric export, five shipped configs (Arty at 100 MHz, as `MAILBOX_SPLIT.md` "Default build" records), base against `7464b876`; `milan_soc.py` and `hdl/` unchanged after | `7464b876` | normalised digest identical per config, as between two base runs; 3,856 of 3,876 files byte-identical, the other 20 by run stamps, archive member times, the hierarchy comment's order and the log's interleaving | `export/` |
| four-shard Verilator sweep (`native-shards.py`, pinned Verilator 5.050 and sv2v 0.0.12) | `44d95625` | rc 0 each: shards 0 to 3 pass 15, 17, 16 and 16 suites (64), 250,913 + 1,536,446 + 380,086 + 23,679 = 2,191,124 checks, 0 in-suite failures, 0 timed out; declared skips only `tsn_fuzz`'s two field campaigns (tsn-gen not installed) | `sweep/sweep-44d95625/` |

## Process notes

- The first firmware self-test ran at `7464b876`; shard 1 found the D9 escape fixed in `b6e35903`.
- The first export run was given a mistyped head SHA; its base exports are kept as a base-against-base
  control.
- `make mutants` was started three times. The first was stopped for the `mbx.c` edit; it left 7.2 GB in
  a tmpfs `/tmp` directory (removed) and one simulation of `wb-address-shifted` running for 49 minutes
  (stopped). The second hung on the same arm (the bench defect fixed in `44d95625`) and was stopped by
  its process group. Its scratch, 33 GB under this lane's `TMPDIR` on `/data`, filled that disk to 100 %
  for some minutes around 13:20 CET before it was removed; anything else writing to `/data` then may have
  failed. The third runs with its scratch on the root filesystem, removed after.
- The sweep was launched four times: at `b48db8fa` (three shards failed the preflight
  `test_suite_cancellation.py`, "CLEANUP FAILED: owned descendants remain", and passed it on the next
  launch: host timing), at `308852d1` and `c9abfc2d` (each stopped for a later commit), and at
  `44d95625`. The launch at `c9abfc2d` reused CPUs 16-31, which another unit had booked in the minute
  after they were freed; it was moved to 80-95 within about two minutes and then stopped.
- CPU ranges: no four free ranges were available, so each launch split the free 16-CPU ranges into four
  4- or 8-CPU shards (`-j4` each), checked against every unit's affinity after each launch; the two
  minutes at `c9abfc2d` above are the only overlap.

## Receipts

See `receipts/INDEX.md` (generated from the files present).
