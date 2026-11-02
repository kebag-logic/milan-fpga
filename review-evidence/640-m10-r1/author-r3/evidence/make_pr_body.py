"""Build round 3's PR-BODY.md from round 2's. Usage: python3 -I make_pr_body.py <r2 body> <out> <head> <steps>"""
import sys
from pathlib import Path

src, out, head, steps = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
t = Path(src).read_text(encoding="utf-8")


def sub(a, b):
    global t
    assert t.count(a) == 1, a[:70]
    t = t.replace(a, b)


sub("[A720l]\n", "[A720m]\n")
sub("- **[Round 2](#round-2)** -- The answers to R765-1 and R766-1, one commit each.\n",
    "- **[Round 2](#round-2)** -- The answers to R765-1 and R766-1, one commit each.\n"
    "- **[Round 3](#round-3)** -- The answer to R766-2-F1, one commit.\n")
sub("clean clone of head `30eb4834e0d258668a7bdfece187f9d7d9fccd0b`, including both builder legs (55 recorded steps, all rc 0)",
    f"clean clone of head `{head}`, including both builder legs ({steps} recorded steps, all rc 0)")
sub("then `[A720l]` for round 2\n", "then `[A720l]` for round 2, then `[A720m]` for round 3\n")
sub("## Authoritative references\n", """## Round 3

R765-2 (issuecomment-6579373754) was POSITIVE. R766-2 (issuecomment-6579449561) was NEGATIVE on one MINOR, R766-2-F1: the plan still disagreed about which lane removes the BIOS memory, and about what takes its place. One page changes: `docs/design/MARK_II_AREA_PLAN.md`.

| # | Findings | What changed |
|---|---|---|
| 13 | R766-2-F1 | The BIOS ROM and SRAM rows say the switch-over removes the BIOS and its integrated ROM and SRAM, and that `ctrl_memory`'s `rom` and `sram` banks hold those regions (and `rom` the reset entry) until stage 3, then first-party Block RAM. From stage 1 the boot loader fills `rom` from the flash copy (D18). "Nothing in its place" and "the split build builds none" are gone. Lane 2's scope reads "Drop DDR3 (lane 1 already drops the BIOS memory); a boot loader filling `rom` from the firmware's QSPI flash copy (D18); ..." and no longer drops the BIOS ROM. The note under the stage table says the stage 1 row keeps the owner's words, that the switch-over removes the BIOS and its ROM and SRAM, that `ctrl_memory`'s banks hold them until stage 3, and that stage 1 drops DDR3 and fills `rom` from flash. |

Every other statement of who removes the BIOS memory already agreed and is unchanged: the basis row's disposition ("the switch-over and LiteX stages 1 to 3"), D19's scope line and decision row, the Block RAM ledger ("all 47 are gone once LiteX stage 3 ends"), the basis description of the LiteX top, M8a-1's row and text in the plan and in `AREA_BUDGET.md` ("the split builds neither BIOS memory"), and `MAILBOX_SPLIT.md`'s switch description ("builds no BIOS ROM or BIOS SRAM, and builds `rom` and `sram` block RAM from that image"). The stage table's stage 1 cells keep the owner's stage name; the note above reconciles them, as R766-2 read it.

Suggestions not taken this round: R766-2-S1 (T_svc = 20 ms as an approved owner decision, and a 256-byte row under it), R766-2-S2 (naming the probe board) and R766-2-S3 (`MilanMAC`'s first-party glue in the Ethernet fate). The round was limited to F1; each stays open for a later change.

## Authoritative references
""")
sub("- PR #835's round 1 reviews: R765-1 (issuecomment-6577388726) and R766-1 (issuecomment-6577608536).\n",
    "- PR #835's round 1 reviews: R765-1 (issuecomment-6577388726) and R766-1 (issuecomment-6577608536).\n"
    "- PR #835's round 2 reviews: R765-2 (issuecomment-6579373754) and R766-2 (issuecomment-6579449561).\n"
    "- `sw/litex/ctrl_memory.py` (`ROM` and `RAM` regions) and `sw/litex/milan_soc.py` (`add_ctrl_memory`, the `--ctrl-mailbox` build switch).\n")
sub("git rev-parse HEAD        # 30eb4834e0d258668a7bdfece187f9d7d9fccd0b", f"git rev-parse HEAD        # {head}")
Path(out).write_text(t, encoding="utf-8")
