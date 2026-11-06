#!/usr/bin/env python3
"""PR-BODY.md for round 8: the live body (gh pr view 812 --json body) with its assigned corrections and a round 8
section. usage: make_pr_body.py <live body> <round 8 section> <out>. Every edit must match exactly once."""
import sys
from pathlib import Path

live, section, out = map(Path, sys.argv[1:4])
HEAD = 'b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce'
PREV = '37e0393094e62d395edc2798a6a6da2f34badbec'
text = live.read_text()


def sub(old: str, new: str) -> None:
    """One exact edit."""
    global text
    assert text.count(old) == 1, (text.count(old), old)
    text = text.replace(old, new)


sub('[A698h]\n\n## Contents', '[A698i]\n\n## Contents')
sub('its gates and one open question.\n\n## Status',
    'its gates and one open question.\n'
    '- **[Round 7: no silent placeholder image](#round-7-no-silent-placeholder-image)** — The refusal of a link with no '
    'flash map, and the placement controls.\n'
    '- **[Round 8: a flash map without its headers](#round-8-a-flash-map-without-its-headers)** — The refusal of a map '
    'that lacks a generated header, and its checks.\n\n## Status')
sub(f'**REVIEW READY at `{PREV}`. Every gate of the round 7 assignment is rc 0 at this head, on clean clones. See '
    '[Round 7](#round-7-no-silent-placeholder-image) for what changed, and '
    '[Round 6](#round-6-generated-flash-map-in-the-platform-boot) for the current figures, which round 7 does not '
    'move, and one open question on the SDK used for them.**',
    f'**REVIEW READY at `{HEAD}`. Every gate of the round 8 ruling is rc 0 at this head, on clean clones. See '
    '[Round 8](#round-8-a-flash-map-without-its-headers) for what changed, and '
    '[Round 6](#round-6-generated-flash-map-in-the-platform-boot) for the current figures, which rounds 7 and 8 do not '
    'move, and one open question on the SDK used for them.**')
sub('Executor: `[A698g]` (round 1: `[A698]`, round 2: `[A698b]`, round 3: `[A698c]`, round 4: `[A698d]`, round 5: '
    '`[A698e]`, round 6: `[A698f]`, `[A698g]`)',
    'Executor: `[A698i]` (round 1: `[A698]`, round 2: `[A698b]`, round 3: `[A698c]`, round 4: `[A698d]`, round 5: '
    '`[A698e]`, round 6: `[A698f]`, `[A698g]`, round 7: `[A698h]`)')
# How to validate now expects this head's 40 checks, so the checkout above it must be this head (R737-4-R1)
sub('git checkout 7643aef613c5b87a246544f57d23ad9f1bf8311e\n', f'git checkout {HEAD}\n')
sub('`ctrl_image_selftest.py` prints `ctrl_image self-test: 37 checks PASS`.',
    '`ctrl_image_selftest.py` prints `ctrl_image self-test: 40 checks PASS`.')
# the ruling's fourth statement
sub('A link of the split platform image without a map is refused by name, since round 7, so `ctrl_plat_image.py` links '
    'no image on the stand-ins.',
    'A link of the split platform image without a map is refused by name, since round 7, and so is one with a map that '
    'lacks `generated/csr.h` or `generated/mem.h`, since round 8, so an image `ctrl_plat_image.py` links takes no header '
    'of the stand-ins. The refusal reads that both headers are there, not what they say.')
text = text.rstrip('\n') + '\n\n' + section.read_text().rstrip('\n') + '\n'
out.write_text(text)
