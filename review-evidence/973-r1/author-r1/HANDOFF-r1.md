# HANDOFF r1 — #973 ([A822]) — a link-up inside a loop pass on the one-hart split image

STATUS (20:36 CET 2026-11-22): **REVIEW READY** at `9a71daa9`. Every gate passes at `862fd41c`, and the docs steps
at the final head `9a71daa9` (section 5). The reproduction fails at the test's commit and passes at the head (section
4). ETA: none, round done. No unit or process of this lane is left running.
Posted: `[A822] TAKEN` issuecomment-7081155903 (TAKEN-comment.md) and `[A822] REVIEW READY`
issuecomment-7084516073 (REVIEW-READY.md). Nothing pushed; no PR opened (PR-BODY.md is the manager's).

**Change of approach during the round (section 3).** The first fix (`8b76887e`) recorded the level in the loop
(`ctrl_loop_link_up`). The platform ledger then refused the 8x8/1if image: +104 B of ROM moved it from 58 to 58.5
RAMB36, past its ledgered 58. The base sat 56 B under that half-tile. The fix now keeps the level in SRP's interface
(`link_carried`), set by SRP's own LINK sink. It is the level of the last LINK the loop dispatched, the "or
equivalent" form, and it costs +8 to +24 B of ROM. The loop and the coverage ratchet are back to the base.

Branch `pf-973-1` at `dd163e41` (PR #960's reviewed head), PR base `dev-soft-core`. Commits, in order:
- `406c4a89` the host test first. It fails at that commit (section 4);
- `8b76887e` the first fix in the loop, with plants;
- `7a0f6d81` docs;
- `ef516e6e` the gate's arm list names the new suite;
- `fe2fe9b9` the loop header in the coverage ratchet;
- `79436c25` the level carried in SRP instead; the loop and the ratchet back to the base; seven plants;
- `862fd41c` the README names the carried level;
- `9a71daa9` the plants' docstring within the Python idiom ratchet's 120 columns.

## 1. Task and authority
- #973, which relates to #665, #970 and #972.
- The idea is ported from the second-hart lane's `8fc723ee` (#872) and its host test
  `CrossApp.ALinkUpInsideHartZerosPassIsTheFirstUp`. The two-hart plumbing is not ported.
- IEEE 802.1Q-2018 10.7 and 35.2: the MRP and MSRP participants of a port whose operational state changes.

## 2. Cause (from the code, reproduced in section 4)
- The loop takes the event ring's records at the start of an ordinary pass (`ctrl_loop.c`, `service_events`). Then
  come the channels' records and then the polls, SRP's among them.
- SRP's poll read the LINK register (`srp_mbx.c`, `poll`, `links[n] = mbx_link_up(n)`). If it differed from the level
  SRP held, the poll called `reset_interface` and set `link_seen`.
- A link that comes up after the pass's events and before SRP's poll reads up in the register. No LINK record has
  been dispatched for it yet: the poster posted it after the loop's take.
- So the poll reset the interface. The LINK UP dispatched next pass then found `link_seen` set. That is a repeated UP,
  which `on_event` treats as coalesced down/up edges, so it reset the interface a second time.
- A first UP (`link_seen` false) normally only calls `hold`, which keeps the clean startup participants. Here they
  were destroyed. A later UP reset the interface twice.
- The one-hart CPU budget harness hides it: there, the link always moves at a pass boundary (#872's report).

## 3. Changes at the head (file:line, reason)
- `sw/firmware/ctrl/srp/srp_mbx.h:66-68`: `bool link_carried` in `struct srp_interface`. It is the level the last
  LINK the loop dispatched carried; attach gives it the register's level.
- `sw/firmware/ctrl/srp/srp_mbx.c:1233`, `on_event`: each LINK sets it, beside `link`.
- `srp_mbx.c:1474`, `srp_mbx_attach`: it starts at the level attach reads, as `link` does.
- `srp_mbx.c:1279-1287`, `poll`: `links[n] = mbx_link_up(n) && m->ifs[n].link_carried`.
  - A DOWN is still taken from the register. So a link lost while a full ring holds its record still fails closed at
    once (`Srp.LinkLevelLossAndFirstDownEventAreFailClosed`).
  - An UP is taken only while the last LINK carried one. A register that rose after the pass's events changes
    nothing until its LINK comes, and that LINK is then a first UP.
  - An UP whose DOWN record a held ring cancelled is still recovered from the register, since the last LINK carried
    an UP (`Srp.CancelledLinkRecordRecoversFromLevelAndFencesOldReceive`).
  - A reattach to a link already up keeps it without another record
    (`Srp.ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord`).
  - It is still one register read per interface (`Srp.PollTermsAreMeasuredSeparatelyThroughRealCallbacks`).
  - `link` implies `link_carried` everywhere `link` is set (attach, `on_event`, the poll), so this is the first
    fix's `mbx_link_up(n) && (link || ctrl_loop_link_up(loop, n))` with SRP's sink as the record.
  - One difference from a record in the loop: a LINK that SRP's sink drops on a re-entry (`enter`, counted in
    `reentries`, asserted in debug builds) is not carried. A dropped DOWN still comes from the register; a dropped UP
    waits for the next LINK.
  - Why not the two-hart form, `links[n] = ctrl_loop_link_up(m->loop, n)`. On two harts the loop also reads the
    register after the ring each pass and dispatches a LINK for a moved level, so its level follows a DOWN at once.
    The one-hart loop has no such read, and this lane changes no LINK dispatch, so the DOWN must come from the
    register (plant `link-pass-down-waits-for-its-record`).
- `sw/firmware/ctrl/test/srp_link_pass.cpp` (new): the host test, section 4.
- `sw/firmware/ctrl/test/srp_fixture.hpp:57-77`: `Srp::SetUp` is now `boot(true, nullptr)`. `boot(link_up, ahead)`
  can boot with the links down and bind a test's own sink and poll before SRP's. Other suites are unchanged.
- `sw/firmware/ctrl/test/srp_arms.py:117-124`: `link_pass_arms`, the suite at 1x1/1if and 8x8/1if, each its own build
  and process. `test_ctrl_firmware.py:212` runs them in the suites phase, and `:78-83` names them.
- `sw/firmware/ctrl/test/srp_link_mutants.py` (new): seven plants (section 4). `srp_mutants.py:18,960` adds them to
  the table. `test_ctrl_firmware.py:234,240` selects them in the 1x1/1if and 8x8/1if campaigns; the 1x1/2if campaign
  runs the whole table.
- `srp_mutants.py:838-841`: the existing `srp-poll-extra-read` plant's site is the changed line, so its texts follow
  it. The plant is the same: one extra bus read in the poll.
- `sw/firmware/ctrl/srp/README.md:114-119` and `CHANGELOG.md:11,61-66`: the rule.
- No RTL, mailbox contract, loop, CPU budget bound or CPU budget harness file changed.

## 4. Reproduction and new checks
The host test `srp_link_pass.cpp` boots SRP on the real loop and the mailbox model with every link down. It moves
interface 0's link at one phase of a pass:
- `BeforeAPass`;
- `InTheEvents`, from a sink ahead of SRP's on the pass's first event, a TICK;
- `AfterTheEventsBeforeSrpsPoll`, from a poll ahead of SRP's: the race;
- `AfterSrpsPoll`, from a poll after SRP's.

It counts interface 0's resets by its LICENCE publication writes: `reset_interface` writes it once, and nothing else
does here. Each test checks:
- the first UP resets nothing and keeps the startup participants;
- its declarations leave interface 0;
- a DOWN between passes resets once;
- the next UP at the same phase resets once.
In the race phase it also checks that the pass that moved the link leaves SRP at the level it held.

| Test | `406c4a89` (base firmware) | Head |
|---|---|---|
| 1x1/1if `AfterTheEventsBeforeSrpsPoll` | FAIL: first UP 2 resets, startup participants lost; later UP 2 resets | PASS |
| 8x8/1if `AfterTheEventsBeforeSrpsPoll` | FAIL: the same | PASS |
| the other three phases, both shapes | PASS | PASS |

Receipts: `receipts/repro/`. The 8x8/2if build of the suite passes at the head too.

Plants (`srp_link_mutants.py`). Each was caught in the 1x1/1if, 8x8/1if and 1x1/2if campaigns during development;
the gate's SRP shard at the head is section 5.

| Plant | Caught by | Failing words |
|---|---|---|
| `link-pass-poll-takes-the-register` (the fix reverted) | `SrpLinkPass.AfterTheEventsBeforeSrpsPoll` | "a first UP resets nothing" |
| `link-pass-attach-carries-an-up` (a double reset at the first UP) | `SrpLinkPass.AfterTheEventsBeforeSrpsPoll` | "SRP's poll reset the interface on a level no LINK had carried" |
| `link-pass-carried-stays-up` (a double reset at a later UP) | `SrpLinkPass.AfterTheEventsBeforeSrpsPoll` | "a later UP resets the interface once" |
| `link-pass-first-up-resets` (`on_event` resets a first UP) | `SrpLinkPass.BeforeAPass` | "a first UP keeps the startup participants" |
| `link-pass-carried-never-recorded` | `SrpLinkPass.BeforeAPass` | "a first UP resets nothing" |
| `link-pass-attach-carries-nothing` | `Srp.ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord` | "Value of: talker" |
| `link-pass-down-waits-for-its-record` (the two-hart form whole) | `Srp.LinkLevelLossAndFirstDownEventAreFailClosed` | "adapter.ifs[0].active[0]" |
| `srp-poll-extra-read` (existing, site moved) | `Srp.PollTermsAreMeasuredSeparatelyThroughRealCallbacks` | "one link read per interface" |

## 5. Gate table
Every gate ran at `862fd41c`, except the docs steps, which ran at the final head `9a71daa9`. `9a71daa9` only rewraps
one test module's docstring within 120 columns (`receipts/change/after-gate-head.txt`): no firmware source, image
input, test or plant. The first fix's results are in section 7.

| Gate | Result |
|---|---|
| Firmware gate, 4 shards (`test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`) | PASS each. Suites 77 of 77 verdicts, the two new arms among them; control campaign 826 of 826; AECP campaign 385 `[ok]`; SRP campaigns 564 `[ok]` (the base's 543 plus the 7 plants in each of 3 campaigns); 0 escaped |
| Shard inventory self-test (`test_ctrl_firmware_shards.py`) | PASS: 1866 invocations, each in exactly one shard ([90, 827, 386, 563]) |
| `fw_coverage.py --selftest`, `--check --jobs 4` | PASS, PASS (40 files; `srp_mbx.c` 803/803 lines, 100 % after exclusions) |
| Twin, twin-plants, twin-maps, twin-maps-plants | PASS each: 0 findings; the 16 split and capture plants each refused, the 3 maps plants caught. Frame counts equal another lane's run on the same base (split MSRP 96, MVRP 92) |
| Platform images at every ledger point (`plat_ledger.py`), base and head | PASS both. RAMB36 45 / 46 / 58 / 63 at both; ROM +16 / +24 / +8 / +16 B (1x1-if1, 1x1-if2, 8x8-if1, 8x8-if2); SRAM unchanged. The size fixture's four images link (rc 0) |
| Image diff, platform and size-fixture images (8 pairs) | `srp_mbx.o` at every point: `poll` +12 or +16 B, `on_event` +4, `srp_mbx_attach` +4, `reset_interface` and `open_interface` -4 each. At 8x8, `ctrl_plat.o`, `ctrl_app_aecp.o` and `ctrl_app_srp.o` (and the fixture's `ctrl_aecp_image.o`) differ only in offsets into the grown SRP interface; their sizes are unchanged |
| CPU budget legs, 10 groups (srp, adp-link, maap, control, backlog, aecp, aecp-fanout, acmp-cmd, datapath-events, fixture), base vs head | 1x1/1if: 0 refusals, 0 budget misses each side; 88 of 88 probes paired; 0 verdicts changed; largest difference -0.438 ms against 20 ms. 8x8/1if: the same; 86 of 86 paired; largest -0.146 ms. No pass over THE SHARE on either side. The ordinary passes run 2 instructions more, a LINK's pass 3 |
| CPU rows: `flip_grade --check --point 1x1/1if`, `--point 8x8/1if`, `load_grade --check`, `shape_costs --check` | PASS, byte-identical at base and head. 1x1/1if: load 0.511 (ceiling 0.70), last queued notice 127.31 ms (130), ACMP 29.06 ms (30), txL 47.88 ms (49). 8x8/1if: load 0.744 (0.75), THE TRANSMIT's figure 77 ms held against 76.81 |
| SRP join intervals on the harness | 1x1/1if 187.938 to 190.006 ms; 8x8/1if 188.162 to 189.943 ms; against 181 to 239 |
| Split boot simulation 1x1, 8x8, `--self-test` (`ctrl_split_boot/run.py`) | PASS, PASS: ready at 27.973 and 67.224 ms (another lane's run on this base: 27.952 / 67.223 ms); self-test 6 of 6 native controls, 6 of 6 plants caught; tracked files unchanged |
| Docs workflow steps (`docs.yml`'s gate commands) | PASS at `9a71daa9`: 104 of 104, tracked files unchanged. At `862fd41c` 103 of 104: the Python idiom ratchet refused a 121-column docstring line in `srp_link_mutants.py`, which `9a71daa9` rewraps |
| Builder legs 0 and 1 (`ci_builder_legs.py run`) | PASS and PASS, each with the one NOT RUN arm the tree declares: leg 0 the MAKEFLAGS note, leg 1 gate 11's build tree, which is not on this host |

Not run:
- The full Verilator sweep (`native-shards.py`): no RTL, testbench or harness file changed, and the round's gate list
  does not name it.
- Vivado: no RTL change, and the RAMB36 counts are unchanged.
- The candidate's `act_ci.py` self-test: AGENTS.md runs it only inside the CI job.
- The CPU harness's other 89 groups at 1x1 and 88 at 8x8-1if, among them the 72 `backlog-adp@` variants and the save
  groups. The change is in SRP's poll, its LINK sink and its attach, which the 10 groups exercise. Each of those 10
  groups' passes moved by 2 or 3 instructions.

## 6. Receipts
`receipts/` with `INDEX.md` generated from the files present.

## 7. Notes
- Scratch: `/data-2/milan/tmp/973-a822`; clones under `clones/`. Units are `milan-973-a822-*`, each on a range booked
  through `cpu_ranges.py pick`. Shards 0 and 2, coverage and the docs steps ran inside the session unit while every
  range was booked. Its memory stayed under 4 GB.
- Two other lanes' units started on ranges my CPU legs had booked (a booking race at 17:12 and 17:15). The legs'
  figures are simulated cycles, so only their wall time moved.
- The first fix's gate results (`7a0f6d81`; coverage at `fe2fe9b9`), superseded:
  - firmware gate four shards: PASS (77 suite verdicts, control 826 of 826, AECP 385, SRP 558 `[ok]`);
  - coverage: PASS once the loop header was recorded;
  - twin and its plants: PASS, 0 findings;
  - CPU legs: 0 misses at both points;
  - docs steps: 104 of 104;
  - `plat_ledger`: FAIL at 8x8-if1, 58.5 RAMB36 against 58. That failure is why the fix moved to SRP.

## 8. Open questions / recommendations
1. A DOWN inside a pass still resets twice: the poll takes it from the register (fail closed), and the LINK DOWN
   record resets again. Both happen before the participants are rebuilt, so nothing clean is lost; the rebuild waits
   one more pass. This lane leaves it as it was, since #973's acceptance is the link-up.
2. The second-hart lane (#872, `opt-hart2-3`) changes the same poll line under `CTRL_HARTS == 2`
   (`ctrl_loop_link_up`). Its loop's level stays its own. On a merge, its `#if` can keep its form there and this one
   on one hart. Alternatively, both harts can take `link_carried`, set by the LINK its loop dispatches to SRP.
3. The 8x8/1if platform image now has 48 B of ROM below its next half-tile (139,216 of 139,264). The next firmware
   change at 8x8/1if is likely to need recorded BRAM debt or a cut.

## 9. Posting
- `[A822] TAKEN`: #973 issuecomment-7081155903.
- `[A822] REVIEW READY`: #973 issuecomment-7084516073 (the text is REVIEW-READY.md).
- Nothing else posted; no existing comment edited. Nothing pushed. The PR body is PR-BODY.md (base `dev-soft-core`,
  `Closes #973`, `Relates to #665`), for the manager to open.

REVIEW READY 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7
