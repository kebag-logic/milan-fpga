"""Round 30's PR-BODY.md: round 29's body with round 30's status, section, validation and limits. usage: prbody30.py"""
from pathlib import Path

S = Path('/data-2/milan/tmp/665s2b-a683zo')
O = Path('$MANAGEMENT/2026-09-23/665s2b-a683zo')
t = Path('$MANAGEMENT/2026-09-23/665s2b-a683zn/PR-BODY.md').read_text()
r30 = (S / 'pr-round30.md').read_text()


def rep(a: str, b: str) -> None:
    """Replace the one occurrence of a."""
    global t
    assert t.count(a) == 1, (t.count(a), a[:80])
    t = t.replace(a, b)


def insert_after(marker: str, text: str) -> None:
    """Insert text right after the one occurrence of marker."""
    global t
    assert t.count(marker) == 1, marker
    i = t.index(marker) + len(marker)
    t = t[:i] + text + t[i:]


rep('[A683zn]\n', '[A683zo]\n')
i = t.index('- **[Status](#status)**')
j = t.index('\n', i)
t = t[:i] + ("- **[Status](#status)** — STOP at the head below: round 30, items 1 to 3 of the ruling on round 29 and the "
             "merge of the TSN stack pin move's round 4 head. The composed size fixture's 8x8/2if image plans 58.5 RAMB36 "
             "against its 58.0, so the re-grade waits for a decision. The platform's image is ledgered at 60.0 and gated "
             "at every point; the SRP record cut's control is held to this image's own record; the rule windows, the "
             "load gate's column binding and driver test T7 are in.") + t[j:]
i = t.index('## Status\n')
j = t.index('## Linked Issue / roles')
t = t[:i] + (S / 'pr-status30.md').read_text() + t[j:]
rep('Executor: `[A683zn]`', 'Executor: `[A683zo]`')
rep('### Round 29\n', r30 + '\n### Round 29 (at `b2d39235`)\n')
rep('### The re-grade on the composed image\n', '### The re-grade on the composed image (round 29, at `2cc852fa`)\n')
rep('### What holds at this head\n', "### What held at round 29's head (`b2d39235`)\n")
rep('git checkout b2d39235ab9bba85d7e560b5f5f78fb4be528960\n', 'git checkout 187eeed89235d5ab7ce68bcd4953c7ef118e9245\n')
insert_after('## Authoritative references\n\n',
             '- The ruling on round 29 (#665 issuecomment-6828629878); the owner decision of 2026-11-12 (#665 '
             'issuecomment-6824896581); R711-8 (#810 issuecomment-6828561870) and R712-8 (#810 '
             "issuecomment-6828619213); PR #892's round 4 REVIEW READY (#665 issuecomment-6829628610).\n")
insert_after('## How to validate\n\n', (S / 'pr-validate30.md').read_text())
insert_after('## Known limitations / out of scope\n\n', (S / 'pr-limits30.md').read_text())
i = t.index('## Definition of Done\n')
t = t[:i] + (S / 'pr-dod30.md').read_text()
(O / 'PR-BODY.md').write_text(t)
print(len(t), 'bytes')
