[A822] REVIEW READY
Commit: 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7 (branch `pf-973-1` on `dd163e41`, PR base `dev-soft-core`)

Changed:
- `sw/firmware/ctrl/srp/srp_mbx.c` and `srp_mbx.h`: each interface carries `link_carried`, the level of the last
  LINK the loop dispatched; attach gives it the register's level.
- SRP's poll now reads `links[n] = mbx_link_up(n) && m->ifs[n].link_carried`.
  - A DOWN is still taken from the LINK register, so a link lost while a full ring holds its record fails closed.
  - An UP is taken only while the last LINK carried one. A link that comes up after a pass's events is therefore
    still SRP's first UP: it resets nothing and keeps the clean startup participants. A later UP resets once.
- `sw/firmware/ctrl/test/srp_link_pass.cpp` (new): the host test. The link moves at four phases of a pass; the test
  runs in a process of its own at 1x1/1if and 8x8/1if (`srp_arms.link_pass_arms`).
- `srp_fixture.hpp`: `boot(link_up, ahead)`.
- `srp_link_mutants.py` (new): seven plants. The existing `srp-poll-extra-read` follows its moved site.
- The SRP README and the changelog.
- No RTL, mailbox contract, loop, CPU budget bound or harness file changed.
- A first version recorded the level in the loop (`ctrl_loop_link_up`). It put the 8x8/1if platform image at 58.5
  RAMB36, past its ledgered 58, so the level moved into SRP's interface. Those commits stay in the history.

Validation (at `862fd41c`; `9a71daa9` only rewraps a test module's docstring; the docs steps ran at `9a71daa9`):
- the test at its own commit `406c4a89`, on the base firmware: `SrpLinkPass.AfterTheEventsBeforeSrpsPoll` FAILS at
  both shapes. The first UP resets twice and loses the startup participants; a later UP resets twice. The other
  three phases pass. At the head all four pass at 1x1/1if, 8x8/1if and 8x8/2if;
- `test_ctrl_firmware.py --require-rv32 --self-test`, 4 shards: PASS. Suites 77 of 77; control 826 of 826; AECP 385
  `[ok]`; SRP 564 `[ok]`; 0 escaped;
- the seven plants are caught in the 1x1/1if, 8x8/1if and 1x1/2if campaigns, each by its named test's own words;
- `fw_coverage.py --selftest` and `--check`: PASS;
- twin, twin-plants, twin-maps, twin-maps-plants: PASS, 0 findings, every plant refused;
- `plat_ledger.py` at every point: PASS at base and head. RAMB36 45 / 46 / 58 / 63 unchanged; ROM +16 / +24 / +8 /
  +16 B; SRAM unchanged. The image diff is `srp_mbx.o`'s code, plus offset-only changes at 8x8;
- CPU budget harness, 10 groups at 1x1/1if and 8x8/1if, base against head: 0 refusals and 0 budget misses each
  side; 88 and 86 probes paired; 0 verdicts changed; largest difference 0.438 ms against 20 ms;
- `flip_grade --check --point 1x1/1if` and `--point 8x8/1if`, `load_grade --check`, `shape_costs --check`: PASS,
  byte-identical to the base. 1x1/1if: load 0.511, last queued notice 127.31 ms, ACMP 29.06 ms, txL 47.88 ms.
  8x8/1if: load 0.744;
- split boot simulation: 1x1 and 8x8 PASS; self-test 6 of 6 native controls and 6 of 6 plants;
- docs workflow steps: 104 of 104; builder legs 0 and 1: PASS, each with its declared NOT RUN arm.

Acceptance criteria:
- A link-up at any phase of a pass resets SRP's interface once, keeping the startup participants: met. A first UP
  resets nothing and keeps them; a later UP resets once; at each of the four phases, both shapes.
- The host test of that ordering fails before the fix and passes after, at 1x1/1if and 8x8/1if, with a planted
  defect: met (seven plants).
- The CPU budget rows unchanged within their bounds: met. The graders are byte-identical, and the measured legs
  change no verdict.
- The images within their ledgers: met at every point.

Open risks/questions:
- A DOWN inside a pass still resets twice (register, then its record), before any rebuild; out of #973's scope.
- A LINK that SRP's sink drops on a re-entry (counted, asserted in debug builds) is not carried; a dropped UP waits
  for the next LINK.
- The 8x8/1if platform image is 48 B of ROM below its next half-tile.
- The second-hart lane (#872) changes the same poll line on two harts; that lane owns the merge of the two.
