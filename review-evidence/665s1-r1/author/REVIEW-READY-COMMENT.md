[A680c] REVIEW READY
Commit: 44d95625bde2c46d7070c090fc29ed0ba85ab64a (`665-s1-faces`, local, not pushed: 15 one-line commits on `dev-soft-core` `e76a755a`, round 2's seven unrewritten)

Changed in round 3 (ruling 6412739248):
- `sw/litex/ctrl_memory.py`: `plan` still refuses any image past 56 RAMB36. One named override, `LEDGERED["8x8-two-interfaces"]` at 57.0 and owed to S14, applies only to an image carrying that point's own symbols: `nvm_stage` at 13,264 B and the size fixture's two-interface `image_allocation`. It is refused on any other image. `ctrl_memory.py plan --ledgered-point` and `ctrl_srp_image.py --ledgered-point` are its only callers; the SoC build names none.
- `test_ctrl_memory.py` plans the point at 57.0 and refuses it in three cases: without the override, through `add_ctrl_memory`, and at 57.5. It refuses the override on the 1x1 images (one and two interfaces), on the 8x8 image with one interface, on an image without the table, and for unknown names. 11 planted defects of the override, 11 caught.
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 ledgers the four points at this firmware: 37.0, 40.5 and 50.0, within 56; 8x8 with two interfaces 57.0, over by 1 tile and owed to S14.
- Three round-2 defects, found by the gates round 2 did not run, are fixed:
  - `mbx.c` decoded an undefined event type as a counted face event. D9 is strengthened and a new defect plants the old catch-all; the whole campaign catches 528 of 528.
  - `suite_face.hpp` T0 idled 2^32 - 1 cycles when a request never opened, so `make mutants` never ended. It now catches 199 of 199.
  - `census_ports.py` was missing from the TSN stack boundary's `OUTSIDE` table.
- `docs/design/MAILBOX_SPLIT.md`: `KL_mbx` out of context with the face block.

Validation: all rc 0 at this head unless a head is named, and nothing a gate reads changed after the head named.
- `make -C tb/verilator/mbx`: 523, 568, 32; at two interfaces 530, 575, model 488. `make -C tb/verilator/mbx mutants`: 199 of 199.
- `gen_mailbox.py --check --crosscheck` and `--selftest`. `publication_census.py --check --selftest --jobs 4` (`7464b876`): 138 arms, 43 rules, 992 s locally.
- `test_ctrl_firmware.py --require-rv32 --self-test`, all four shards. `fw_coverage.py --check`: 31 files at 100 %. `aecp_mutants.py` (`b48db8fa`): 96 of 96. `ctrl_boundary.py --require-rv32 --selftest`, both legs.
- `test_builder.py --require-rv32` (`b48db8fa`): every gate passes; gate 11 did not run, as it needs a local Arty build report. `cd tests && behave` (`b48db8fa`): 406 scenarios. `test_ctrl_memory.py` (`c9abfc2d`).
- `lint_rtl.py --check`, `xvlog_gate.py --check`, Yosys on the three mailbox tops, and the docs gates (69 commands).
- The four-shard Verilator sweep: 64 of 64 suites, 2,191,124 checks, 0 failures. `tsn_fuzz` declares its field campaigns skipped, as tsn-gen is absent.
- `KL_mbx` out of context, under the host lock: 3,585 -> 5,515 LUT and 4,114 -> 7,632 FF; 1 RAMB36 and 10 RAMB18 unchanged; WNS +0.123 ns.
- The all-fabric export, five shipped configs, base against `7464b876`: the normalised digest is identical per config. 3,856 of 3,876 files are byte-identical. The other 20 differ only as two base runs do: run stamps, archive member times, the hierarchy comment's order and the log's interleaving.

Acceptance criteria: met under ruling 6412739248, with the 8x8 two-interface point ledgered at 57 RAMB36 and owed to S14; the flip still needs 56 or fewer at every point. The images were measured with one shared `-fno-stack-protector` runtime for base and head; S3 owns the target runtime. VERSION is untouched, and there is no `milan_datapath.sv`, `.github/` or CI-generator edit.

Open risks/questions:
- `docs/testing/TESTING.md:753` counts the memory test's in-tree mutants (forty-four). The override's plants run as a probe because that file is in a release lane's file map; adding them in-tree is owed with that count.
- The image figures are planned; none was mapped out of context.
