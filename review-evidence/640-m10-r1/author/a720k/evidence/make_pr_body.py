"""Write PR-BODY.md for [A720k]: the first pass's body, updated for the second pass."""
import subprocess
from pathlib import Path

SRC = Path("$MANAGEMENT/2026-09-23/640-a720j/PR-BODY.md")
OUT = Path("$MANAGEMENT/2026-09-23/640-a720k/PR-BODY.md")
G = Path("$VALIDATION_STORAGE/640-a720k/gates/logs")
LANE = "$LANES/640-mark2-charter"
head = subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
rcs = sorted(G.glob("*.rc"))
bad = [p.stem for p in rcs if p.read_text().strip() != "0"]
s = SRC.read_text(encoding="utf-8")


def rep(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


rep("[A720j]\n", "[A720k]\n")
i = s.index("GREEN, documentation only -- ")
j = s.index("\n", i)
status = (f"GREEN, documentation only -- every run step of the docs workflow exits 0 on a clean clone of head `{head}`, "
          f"including both builder legs ({len(rcs)} recorded steps, all rc 0), and `git diff --check` against the merge base `503bc97c` is clean "
          f"-- `640-charter-followup` -> `dev`." if not bad else
          f"NOT GREEN -- steps not 0: {', '.join(bad)} -- `640-charter-followup` -> `dev`.")
s = s[:i] + status + s[j:]
rep("Executor: `[A720j]`", "Executor: `[A720j]`, then `[A720k]` for the second pass")
rep("Five items, one commit each, all in `docs/design/MARK_II_AREA_PLAN.md` except the last.",
    "Five items, one commit each, all in `docs/design/MARK_II_AREA_PLAN.md` except the last. "
    "A second pass then adds two commits on the same page, from the manager's answer on #640 (issuecomment-6575277828).")
rep("The owner's 2026-11-02 decisions are recorded as D18 to D20. |",
    "The owner's 2026-11-02 decisions are recorded as D18 to D20, linked to the comment on #640 that records them. |")
rep("(owner, 2026-11-02), with the flash layout of `QSPI_FLASHBOOT.md` unchanged. Masters",
    "(owner, 2026-11-02); the image has its own flash slot (D21, below). Masters")
rep("The cause is not established, and the page says it is a measurement, not a diagnosis. That layout has no firmware slot, so where the image sits is open owner decision 4: the bitstream slot leaves 368,312 bytes after the 3,825,992-byte bitstream file; a separate slot changes the layout. |",
    "The cause is not established, and the page says it is a measurement, not a diagnosis. |")
k = s.index("\n## Authoritative references")
s = s[:k] + (
    "\n\nSecond pass:\n\n"
    "| # | Item | What changed |\n"
    "|---|---|---|\n"
    "| 6 | D18 to D20 links | The three decision rows link to issuecomment-6575277828, which records the owner's 2026-11-02 decisions. |\n"
    "| 7 | Firmware flash slot | The manager's decision of 2026-11-02 is recorded as D21: the firmware image gets its own flash slot, sized for the image, in a free erase-aligned range that is neither reserved (`journal`, `user`) nor used. The bitstream and AEM slots keep their offsets and budgets. The image does not go in the bitstream slot's tail, which would tie its offset to the bitstream's size. Open decision 4 and every statement that the layout stays as is are removed: the stage 1 table row and text, the D18 consequence, the stage 1 lane's dependency. The offset and budget are not chosen here: the stage 1 lane states them in `FLASHBOOT_LAYOUT` and the generated layout page. `QSPI_FLASHBOOT.md` still describes the shipping layout, unchanged until stage 1 lands. |\n"
) + s[k:]
rep("The plan links them to #640.", "Recorded on #640 (issuecomment-6575277828).")
rep("- #665: one hart", "- The manager's decision of 2026-11-02 on where the copied firmware sits in flash (#640 issuecomment-6575277828).\n- #665: one hart")
rep("git rev-parse HEAD        # 7aa996e3816a2e68e5d1672d2379a3f97cc304af", f"git rev-parse HEAD        # {head}")
rep("- **The 2026-11-02 owner decisions are not yet posted on #640.** D18 to D20 link to the issue, not a comment.\n", "")
rep("- **Where the copied firmware image sits in flash is open owner decision 4.** The page gives the measured room and the two choices; it chooses neither.\n",
    "- **The firmware slot's offset and budget are not chosen.** D21 fixes where the image goes in principle; the stage 1 lane states the numbers in `FLASHBOOT_LAYOUT`. `QSPI_FLASHBOOT.md` is not edited: it describes the shipping layout.\n")
for bad_word in ("/home/", "/data/", "act_ci"):
    assert bad_word not in s, bad_word
assert all(ord(c) < 128 or c in "µ" for c in s), [c for c in s if ord(c) >= 128 and c != "µ"]
OUT.write_text(s, encoding="utf-8")
print(OUT, len(s.encode()), "bytes; head", head, "; bad", bad)
