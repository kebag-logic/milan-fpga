[A822] TAKEN
Branch: `pf-973-1` at `dd163e41` (the flip PR #960's reviewed head); PR base `dev-soft-core`, its diff this lane's commits only.
Authoritative references: #973 and its acceptance; #665; the second-hart lane's fix for two harts (`8fc723ee`, `CrossApp.ALinkUpInsideHartZerosPassIsTheFirstUp`, #872), whose idea is ported and whose two-hart plumbing is not; `sw/firmware/ctrl/srp/srp_mbx.c` (`poll`, `on_event`, `srp_mbx_attach`); `sw/firmware/ctrl/loop/ctrl_loop.c` (`service_events`); IEEE 802.1Q-2018 10.7 and 35.2 (MRP and MSRP participants of a port whose operational state changes).
Interpreted scope: on the one-hart split image the loop takes the event ring's LINK records at a pass's start and SRP's poll reads the LINK register later in the same pass. A link that comes up in between is reset by the poll on a level no LINK record has carried, and the LINK record dispatched next pass is then a repeated UP that resets the interface again, so the clean startup participants a first UP keeps are lost. The fix: the loop records the level of the last LINK record it dispatched for each interface (`ctrl_loop_link_up`), and SRP's poll takes an UP only as the loop dispatched it. A DOWN still comes from the register, so a link lost while a full ring holds its record back still fails closed, as the existing tests require. No mailbox contract, RTL, or CPU budget bound change. If the fix needs any of those, I stop and report.
Validation plan:
- a host test of a link raised between the loop's events and SRP's poll, in its own process, at 1x1/1if and 8x8/1if. It must fail at `dd163e41` and pass at the head;
- planted defects in the firmware campaign: the fix reverted, and a double reset through the loop's level;
- the firmware gate (`test_ctrl_firmware.py --require-rv32 --self-test`) in four shards with its plants, and `fw_coverage.py --selftest` and `--check`;
- the two-placement twin and its plants;
- the CPU budget harness at 1x1/1if and 8x8/1if, base against head, every row within its bound, and the table graders;
- the platform images within their ledgers (`plat_ledger.py`) and the image diff;
- the docs workflow steps.
Blockers: none.
