[A793] REVIEW READY
Commit: `7cfb8a04` on `936-stream-notice` (base dev-soft-core `70f4056f`; 9 commits, `d3c528fc` to `7cfb8a04`)
Changed:
- **The notice is obliged.** Milan v1.2 5.4.5.2 and Table 5.22 list a Stream Output's MSRP Talker declaration state, failure code and bridge ID, Stream ID, destination MAC and VLAN ID among GET_STREAM_INFO's unsolicited triggers. IEEE 1722.1-2021 7.5.2 ties Talker Advertisements and Failures to GET_STREAM_INFO notices. The release processor raises one at each declare and withdraw (`protocol_processor_top.sv:3679-3684`).
- `srp_mbx.c` `declare_sources`, after TALKER_DECL is published, records each source whose declaration changed against what its STREAM_OUTPUT last showed. That covers declared or withdrawn, the type swapped Advertise/Failed (once lwSRP makes the swap), and another VID (an adopted Domain's). A reset that declares an unchanged source records nothing.
- The SRP delivery takes the record into `ctrl_app.srp_noticed`, and an attach clears it. The AECP bridge raises `aecp_changed(STREAM_OUTPUT n, STREAM_INFO)` for each recorded source, so AECP's existing notice path and pacing send it to every registered controller (Milan v1.2 5.4.5.1).
- Tests: `Talker.DeclarationAndWithdrawalAreNoticed`, `TypeSwapIsNoticed`, `AdoptedDomainVidIsNoticed`, `ResetNoticesNothingUnchanged`; `SrpGate.F936AProbeAndItsExpiryEachNoticeTheSource`; `App.SrpDeclarationChangeIsItsStreamOutputsNotice`.
- Plants, each caught by its test's words: 12 `talker-notice-*` (both SRP campaigns) and 4 `app-output-notice-*`.
- Twin: `stream-output-0-notices` deleted, since the split now sends the fabric's four notices of STREAM_OUTPUT 0 at the same changes to the same controllers. One byte group still differs and is held by the exact owed row `stream-output-0-dest-mac` (finding below). New capture plant `output-notice-dropped`; `vanished-owed` re-aimed.
- Ledger: `ctrl_plat` +64 B at the two-interface points. The size fixture's `8x8-two-interfaces` entry goes 59.0 -> 59.5 RAMB36 by the owner's loose block-RAM decision (#665 issuecomment-6892332745): the harness's every-port and valid-destinations arm images need 127,132 and 126,992 B of rom, 156 and 16 B past 59.0.
- No RTL, mailbox-contract or CPU-budget-bound change.
Validation (each on a fresh clean clone; workflow jobs replayed step by step, every `run:` step rc 0 or not run for a stated reason, which here are only tool installs present on the host and hosted step recorders):
- At `7cfb8a04`:
  - docs `wire-accountability`, `docs-check-no-git`, `docs-gates-0/1/2`, `docs-check`: PASS (61 steps).
  - rtl-fast `firmware-unit`: PASS, `fw_coverage.py --check` 39 files.
  - elaborate's builder legs (both, `--require-elaboration --require-rv32`): PASS. The LiteX aggregate passes 8 of 8, `test_ctrl_memory` included.
  - twin: 1 finding, `split-talker-failed`, PR #935's stale row. Twin plants: the 20 plants other than `srp-plus-k` (PR #935's stale words) refused in both runs, 40 of 40.
  - Release image byte-identical to the base (`bios.bin` 1x1 `860d4771`, 8x8 `d8851b6d`).
  - `plat_ledger.py` PASS. Every split platform (24) and fixture (6) image hash equals `b496c99e`'s; product ROM banks unchanged.
- At `b496c99e` (`7cfb8a04` adds only the ledger's figures in `SPLIT_CONTROL_MEMORY.md` and an unread reason string in `ctrl_memory.py`; no image changes, by hash):
  - `firmware-srp-mutants`: 445 caught, none escaped. `firmware-aecp-mutants`: 303 caught. `firmware-control-mutants`: 716 of 716 caught.
  - `firmware-boundary`, `firmware-verilator`, `split-cdc`: PASS.
  - `verilator-shards` 1, 4, 6, 10, 17 of 19 (the shards that build the split firmware: `milan_dp__0..3`, `mbx`): 28 suites, 763,945 checks, 0 failed.
- Scratch merge with PR #935's `37255683` (not pushed): twin 0 findings, all 22 plants refused (44 of 44).
- CPU service-budget harness on the final image (arm A built at `77c1aad7`, its `ctrl_app.elf` equal to `7cfb8a04`'s by hash; the variant arms on `b496c99e`), CPU 100 MHz on sys:
  - Arm A at 1x1/1if (96 groups): 0 refusals, 0 of 130,941 passes over the 2 ms share, no `STATED` line.
  - Arm A at 8x8/1if (95 groups): 0 refusals, 0 of 263,828 passes over the share. Its `STATED` lines report the costs this point takes past the 1x1/1if stated ones, as the harness README says it does. The base's `backlog-owed` group reports the same two ACMP kinds.
  - Both points' only budget misses are the base's seven held-egress rows. The egress ledger at 8x8/1if PASSes them, 0.136 to 0.314 ms inside.
  - Notice rows: `answering-later` at most 8.301 ms (1x1/1if) and 8.246 ms (8x8/1if) against 20 ms. `answering-every-port` 1x1/1if: 192 notices at most 27.073 ms against 140 ms.
  - `valid-destinations`: every Talker declare/withdraw row within 220 ms at both points (at most 189.423 ms). At 8x8/1if the arm's `STATED` reports include the tier-2 slice and build-one passes, as at the base, and, new here, 21 THE RETRY rounds of one refused attempt (below).
Acceptance criteria:
- Decided by the specs: obliged (above). Met.
- Sent from where SRP changes the declaration, within AECP's notice bounds: `declare_sources` records it; AECP's notice path and pacing send it. Met.
- A unit test and a planted defect cover it: the six tests and 16 plants above, all caught by name. Met.
- The twin row is deleted with its evidence: `stream-output-0-notices` deleted; STREAM_OUTPUT 0's notices now match but for `stream_dest_mac`, which is held by its own row with the plants above. Met.
- The CPU service-budget harness shows the notice rows within their bounds: every notice row is within its bound at both points, and so is every other row except the base's seven held-egress rows, which the ledger grades (PASS). Met. The first three open questions below concern held-egress rows, stated costs and a harness row, not the notice rows' bounds.
Open risks/questions:
- Held-egress rows at 1x1/1if: the seven measure 0.132 to 0.151 ms more than the base's, from 62.905 to 63.041 ms for `backlog.owed.if0`; the service behind the 60 ms hold grows 3.6 to 8.7 %. 1x1/1if has no ledger (`egress_ledger.py` refuses it), so by #936 issuecomment-6938589620 they stay the base's recorded misses. At 8x8/1if the change is -0.006 to +0.066 ms, inside the ledger. Whether 1x1's growth needs a figure is the owner's call. Table in the PR body.
- New `STATED` reports at 8x8/1if in `valid-destinations`: 21 THE RETRY rounds of one refused attempt, 11,922 to 12,537 CPU cycles against the one-interface stated 11,900. The base's same arm has none; its longest round is 2,174. Each is a new STREAM_OUTPUT notice's GET_STREAM_INFO attempt, refused because this arm's fixture leaves the gather window unanswered, and retried at AECP's backoff. At 1x1/1if the same rounds are at most 9,015, within 11,900. 8x8/1if reports costs past the one-interface ones by design; whether its round needs its own figure is for #894 (the 8x8 owner).
- No harness group registers a controller while its Talker declares, so no row times the new STREAM_OUTPUT notice itself. Its record's cost is inside the SRP rows, and it is sent by AECP's notice path, which the `answering-*` rows time. A dedicated row would be a harness change outside #936.
- Finding for a new issue (RTL, no owner): on the split, a declaring STREAM_OUTPUT's GET_STREAM_INFO answer carries `stream_dest_mac` 0 with STREAM_DEST_MAC_VALID set (Milan v1.2 5.4.2.10.2). The datapath answers from the fabric MAAP engine's address, which the split does not build (`milan_datapath.sv:6424`, `:6625`, `:8731`, `:8760-8761`). Seen on the same face: no MSRP failure fields, no REGISTERING, the declaring bit is the DA gate, and there is no Listener-registration notice. The PR body has the twin's bytes and lines.
- Lane conflicts:
  - PR #935: text conflicts in the twin's `Makefile`, `README.md` and `twin_compare.py`. The resolution keeps this PR's dest-MAC row, #935's deletion of `split-talker-failed` and both new plants; its twin is clean, above.
  - PR #932: text conflicts in the memory ledger; whichever lands second re-measures.
  - PR #914: merges cleanly as text.
