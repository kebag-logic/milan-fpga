[A757] TAKEN

Branch: `665-s7-srp-tx`, from `dev-soft-core` `1d6bf555`. The PR will target `dev-soft-core`.

Authoritative references: this issue's acceptance 1 to 7; the plan's section S7; IEEE 802.1Q-2018 10.7.4, 10.7.9, 10.7.11 and Table 10-7, 10.8.1 and 10.8.2; Milan v1.2 Table 4.3 and 4.2.7.2.2; `T_svc` = 20 ms, approved (#665 issuecomment-6495692075); #839 (source address) and #608 (withdrawal after a LeaveAll); lwSRP PR #18 (one Message per AttributeType); `sw/firmware/ctrl/srp/README.md`; `tb/verilator/milan_dp/README.md`, the two-placement simulation.

Interpreted scope: a split-only SRP egress check on the two-placement simulation's split half: `tb_split_top`, the platform firmware on the RTL mailbox, built once and reused for every run.
- Item 1. Every MSRP and MVRP frame the MAC sends is graded for its 10.8.1/10.8.2 form: at most 1,500 octets, one Message per AttributeType, each AttributeList and PDU EndMark, no value declared twice, and a LeaveAll on every AttributeType of its application.
- Item 2. Its source address is the port's MAC from the first frame after reset.
- Item 3. Each participant's JoinTime and LeaveAll spacing at egress is held to 10.7.4 and Table 10-7 (Milan Table 4.3 values), widened by `T_svc`. The egress interval error per timer is measured in µs, with frames per transmit opportunity.
- Item 4. A second run holds the MAC until the SRP TX ring is full. Every MRPDU lwSRP was told was sent must leave the MAC in order, byte for byte, and the adapter must have seen the ring full and kept the frame.
- Item 6. The split leg checks each source's LICENCE bit at the stream gate and the AAF and CRF emission terms, as the all-fabric build's ACTIVE AND admitted reaches them.
- Item 7. Each check gets a planted mutant: the five the issue names, plus one each for items 5 and 6.

No RTL, contract or ring change is planned. A defect found is fixed in its owner's file, or drafted as an lwSRP donor patch.

Validation plan, on a clean clone of the final head, all rc 0:
- every `run:` step of the jobs a pull request to `dev-soft-core` triggers, with a reason for each step that cannot run here;
- the docs workflow's steps;
- the full sweep;
- the firmware self-test (`test_ctrl_firmware.py --require-rv32 --self-test`), `fw_coverage.py --check` and every firmware mutant driver;
- `make twin`, `make twin-plants`, `make split`, `make split-mutants` and the new check with its plants;
- S2's harness at 1x1/1if and 8x8/2if, `test_builder.py --require-rv32`, `cd tests && behave`, and `git diff --check` against the merge base.

Blockers: item 5 needs a licensed split talker. At this base every split source declares Talker Failed from boot: `ctrl_plat.c` `configure_sources` never sets `allocated`, and `srp_mbx.c:170` admits only an allocated source. Ruling issuecomment-6505997821 item 3 defers the adapter entry that takes MAAP's allocation until S2b's `srp_mbx.c` is on `dev-soft-core`, and S2b rewrites that file's TX path. I will build the #608 check, run it with source 0 allocated at SRP creation by a test-only link-time fixture, and publish that fixture. Item 5 stays unmet in the production composition until that entry lands, and the exit will name that line.
