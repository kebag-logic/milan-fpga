#!/usr/bin/env python3
"""PR-BODY.md for round 7: the live body (gh pr view 812 --json body) with its assigned corrections and a round 7
section. usage: make_pr_body.py <live body> <round 7 section> <out>. Every edit must match exactly once."""
import sys
from pathlib import Path

live, section, out = map(Path, sys.argv[1:4])
HEAD = '37e0393094e62d395edc2798a6a6da2f34badbec'
text = live.read_text()


def sub(old: str, new: str) -> None:
    """One exact edit."""
    global text
    assert text.count(old) == 1, (text.count(old), old)
    text = text.replace(old, new)


sub('[A698g]\n\n## Contents', '[A698h]\n\n## Contents')
sub('**REVIEW READY at `7643aef613c5b87a246544f57d23ad9f1bf8311e`. Every gate and run of the round 6 assignment is rc 0 '
    'at this head, on clean clones. See [Round 6](#round-6-generated-flash-map-in-the-platform-boot); it carries the '
    'current figures and one open question on the SDK used for them.**',
    f'**REVIEW READY at `{HEAD}`. Every gate of the round 7 assignment is rc 0 at this head, on clean clones. See '
    '[Round 7](#round-7-no-silent-placeholder-image) for what changed, and '
    '[Round 6](#round-6-generated-flash-map-in-the-platform-boot) for the current figures, which round 7 does not '
    'move, and one open question on the SDK used for them.**')
# R738-4 F2: the current writer's figure and the claim that its measurement is unchanged
sub("- The current flash writer's capture: at most 13.863 ms at 8x8, with the CPU at 50 MHz and the bus at 100 MHz, under "
    "its 24.5 ms (round 2's measurement; that writer and its harness are unchanged since).",
    "- The current flash writer's capture: at most 13.861 ms at 8x8 (13.86052 in "
    "`tb/verilator/nvm_capture_cpu/measurements.json`; the merge of `dev-soft-core` `a68536fa` brought that receipt, and "
    "round 2 had measured 13.863 ms), with the CPU at 50 MHz and the bus at 100 MHz, under its 24.5 ms.")
sub("- `nvm_store_boot`'s CPU time on the split CPU at 50 MHz: 100.5 ms valid, 165.1 torn, and 10.1 absent or "
    "wrong-version at 1x1; 488.5, 745.1 and 34.9 ms at 8x8.",
    "- `nvm_store_boot`'s CPU time on the split CPU at 50 MHz: 101.0 ms valid, 166.0 torn, and 10.1 absent or "
    "wrong-version at 1x1; 490.4, 748.7 and 34.9 ms at 8x8.")
sub('11,062 + 263.7 a byte at 1x1, and 16,500 + 205.5 at 8x8.', '11,066 + 265.8 a byte at 1x1, and 16,533 + 205.6 at 8x8.')
# item 4: what is true of the no-map path
sub("**On \"no F1 placeholder in any split image\".** Both links the boot simulation makes use the generated map. "
    "`ctrl_plat_image.py` still accepts no map, for one caller: the boundary gate's compile (`ctrl_runs.py`), which is "
    "given absent runtime archives and stops at its link by design, so it produces no image.",
    "**On \"no F1 placeholder in any split image\".** Both links the boot simulation makes use the generated map. A link "
    "of the split platform image without a map is refused by name, since round 7, so `ctrl_plat_image.py` links no image "
    "on the stand-ins. Only the boundary gate's compile (`ctrl_runs.py`) takes no map: it is given absent runtime "
    "archives, so it compiles and stops at its link, and produces no ELF. The size fixture is a separate builder and is "
    "not a booted image; see [Round 7](#round-7-no-silent-placeholder-image).")
# R738-4 F3: the PR text matches what is in the tree
sub("| `boot_soc.build`'s placement guard | `spiflash_master_cs` expected four bytes off, in a scratch map | `the boot SoC "
    "does not place the flash port's devices as the split SoC does`; with the guard removed, the same export succeeds, "
    "so the defect escapes |",
    "| `boot_soc.build`'s placement guard | `spiflash_master_cs` expected four bytes off, in a scratch map | `the boot SoC "
    "does not place the flash port's devices as the split SoC does`; with the guard removed, the same export succeeds, "
    "so the defect escapes. A probe at this round; round 7 commits it, as `run.py --placement-controls` |")
sub('python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-plants --self-test\n',
    'python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-1x1 --placement-controls\n'
    'python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-plants --self-test\n'
    'python3 -B sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32\n')
sub('its self-test prints `6 of 6 native controls as required; 2 of 2 plants caught`.\n- Every other command exits 0.',
    'its self-test prints `6 of 6 native controls as required; 2 of 2 plants caught; 0 placement controls wrong`.\n'
    '- `--placement-controls` prints `ctrl_split_boot placement controls: 8 of 8 as required`, and '
    '`ctrl_image_selftest.py` prints `ctrl_image self-test: 37 checks PASS`.\n'
    '- Every other command exits 0.')
sub('- The mailbox\'s address is still the fixture\'s placeholder. The target platform firmware (S3) owns it.\n',
    '- The mailbox\'s address is still the fixture\'s placeholder. The target platform firmware (S3) owns it.\n'
    '- The placement controls need the product LiteX tree, as the boot does, so no hosted job runs them. The refusal of '
    'a link with no map is a control of `ctrl_image_selftest.py`, which the hosted firmware boundary job runs.\n')
text = text.rstrip('\n') + '\n\n' + section.read_text().rstrip('\n') + '\n'
out.write_text(text)
