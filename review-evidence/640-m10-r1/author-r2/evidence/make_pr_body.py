"""Build PR-BODY.md: the live round 1 body with round 2's changes. Usage: make_pr_body.py <live> <out> <head> <steps>"""
import sys
live, out, head, steps = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
s = open(live, encoding="utf-8").read().rstrip("\n") + "\n"


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)


rep("[A720k]\n", "[A720l]\n")
rep("- **[Description](#description)** -- What changed and why.\n",
    "- **[Description](#description)** -- What changed and why.\n"
    "- **[Round 2](#round-2)** -- The answers to R765-1 and R766-1, one commit each.\n")
rep("on a clean clone of head `3f8ed303e01285f1bad0641f4ebc05764f162467`, including both builder legs (54 recorded steps, all rc 0)",
    f"on a clean clone of head `{head}`, including both builder legs ({steps} recorded steps, all rc 0)")
rep("Their readers pass at the head: `pp_resource_gate.py check-baseline` (\"baseline PASS: 3 endpoints\") and the `ctrl_service_bounds` arm (47 checks, 0 failures). Neither reads a changed line.",
    "Their readers pass at the head: `pp_resource_gate.py check-baseline` (\"baseline PASS: 3 endpoints\") and the `ctrl_service_bounds` arm. Neither reads a changed line.")
rep("Executor: `[A720j]`, then `[A720k]` for the second pass",
    "Executor: `[A720j]`, then `[A720k]` for the second pass, then `[A720l]` for round 2")
rep("Masters use the SoC bus, never the CPU's DMA port: the stage 1 probe measured that route hanging (3 reads issued, none answered; 311 of 311 on the SoC bus).",
    "Masters use the SoC bus, never the CPU's DMA port: the stage 1 probe measured that route hanging (3 reads issued, none answered). With the masters on the SoC bus the entity advertised and all 33 descriptors read back byte-identical.")
rep("One pass fits the 2.0 ms per-pass share, in which 24 characters can arrive, so the buffer is 32 bytes (covers 2.778 ms).",
    "While every pass fits the 2.0 ms per-pass share, 24 characters can arrive between polls, so the buffer is 32 bytes (covers 2.778 ms); round 2 states that this share is unmerged S2b work.")

round2 = """
## Round 2

Both round 1 reviews were NEGATIVE with MINOR findings only: R765-1 (issuecomment-6577388726) and R766-1 (issuecomment-6577608536). Each finding is answered once, under every ID that raised it. Two pages change: `docs/design/MARK_II_AREA_PLAN.md` and one line of `docs/design/MAILBOX_SPLIT.md`.

| # | Findings | What changed |
|---|---|---|
| 8 | R765-1-F1, F2, F3; R766-1-F1 | The census is re-derived from `sw/litex/milan_soc.py` and the basis build's SoC hierarchy, CSR map and placed hierarchy, not from the first pass's table. New rows: the 200 MHz `idelay` clock and the `IDELAYCTRL`, which Ethernet keeps past stage 1 and whose clock drives the audio MMCM's `PSCLK` (the fate keeps today's clock for it; an `IDELAYCTRL` stays only if the stage 2 MAC uses an `IDELAYE2`, since all 32 in the basis are DDR3's); `MilanMAC`'s `link_status` CSR (REQ-MAC-03; a first-party register) and `loopback` CSR (removed: nothing writes it); the split build's `ctrl_memory` banks and decoder (first-party Block RAM at stage 3) and `ctrl_mbx`'s event manager, CSR bank and tick. The BIOS ROM and SRAM move to the switch-over, where the split build already drops them, and their fates no longer name a LiteX block. The Ethernet row's PHY reset pin keeps its power-on pulse and the reboot controller's hold. DDR3's row gains the CPU memory port's crossing and the `sys4x` clocks. Three cross-references follow: a note under the stage table, the basis row's disposition and the Block RAM ledger's line. Coverage was checked mechanically: every node of the SoC hierarchy, every CSR register and every placed child of the CPU wrapper maps to exactly one row with a stage and a fate, and the same check against the round 1 page fails on the nine objects the findings named. |
| 9 | R765-1-F5; R766-1-F2 | The page states that the 2.0 ms share and T_svc = 20 ms come from #665's S2b work (PR #810, not merged), and that dev's `FR_NFR.md` still proposes 10 ms. Under 10 ms, with no per-pass share, 116 characters complete within the gap and the buffer would be 128 bytes. The 32-byte result is marked conditional on the share and is re-derived if the share changes; at 32x32 #665 estimates passes over the share, where the loss rule applies. The census UART row and D20's consequence say the same. |
| 10 | R765-1-F4; R766-1-F3 | "311 of 311 reads were answered" is removed: no public source carries it. The page keeps the measured hang and adds what the cited probe comment shows for the SoC bus route: the entity advertised and all 33 descriptors read back byte-identical. |
| 11 | R766-1-R1 | `MAILBOX_SPLIT.md:151` now reads "Its sources also include fabric timer expiries, tagged by arm." The residue's exact text was 11 words; "with their arm" became "by arm" to meet the 10-word limit, as round 1 did for its residue. |
| 12 | R765-1-S1; R766-1-S1 | The split CPU's netlist identifier, which no public source records, is dropped; the cited #665 comment stays the source of 3,948 and 3,543. |

Suggestions not taken: R765-1-S2 (which CPU figure the start uses: the lever 4 figures recomputed clean in both reviews, and the CPU's clock moves with the S2b work); R765-1-S3 (the image behind the console-loss figure: the public probe comment does not name it, so naming it would add an unsourced fact); R766-1-S2 (recasting lever 4's "Why" cell and lane 7 needs the owner, whose text it is); R766-1-S3 (the probe's AX7101 area figure includes the failing DMA route and was not re-routed, so it does not measure stage 1 as planned).
"""
rep("\n## Authoritative references\n", round2 + "\n## Authoritative references\n")
rep("The full docs workflow, both builder legs included, is in the author's evidence.",
    "The full docs workflow, both builder legs included, is in the author's evidence; so are the census coverage check and its basis excerpts.")
rep("- #495: the #828 residue (issuecomment-6573412222).\n",
    "- #495: the #828 residue (issuecomment-6573412222).\n"
    "- PR #835's round 1 reviews: R765-1 (issuecomment-6577388726) and R766-1 (issuecomment-6577608536).\n"
    "- PR #810, the S2b lane, open and not merged.\n")
rep("git rev-parse HEAD        # 3f8ed303e01285f1bad0641f4ebc05764f162467",
    f"git rev-parse HEAD        # {head}")
rep("- **The console buffer rests on the 2.0 ms per-pass share,** which the S2b lane (PR #810) carries and dev does not yet publish. At 32x32 the S2b estimates exceed the share; console loss is then accepted by rule.",
    "- **The console buffer rests on the 2.0 ms per-pass share,** which the S2b lane (PR #810) carries and dev does not yet publish; the page now says so, and gives 128 bytes under dev's proposed 10 ms. At 32x32 the S2b estimates exceed the share; console loss is then accepted by rule.\n"
    "- **The census is checked against the basis build's records,** which stay outside the repository. The author's evidence carries the SoC hierarchy, the CSR map, the placed hierarchy's top rows and the coverage check, with the digests of the full reports.\n"
    "- **Two census fates keep today's behaviour rather than choose a new one:** the audio MMCM's `PSCLK` stays the 200 MHz clock, and the PHY reset pin keeps its power-on pulse and the reboot hold. Changing either is a later lane's measured decision.")
open(out, "w", encoding="utf-8").write(s)
