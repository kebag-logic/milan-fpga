"""splice_pr_body.py <current-body> <status.md> <validate.md> <timing.md> <out>: PR #822's current body with this
round's Status, How to validate and Route timing sections replaced whole, the first line and the executor line
naming this round, and the verification-bar box stating the route's verdict. Every other byte is kept. Refuses
unless each anchor appears exactly once."""
import sys
from pathlib import Path

body, status, validate, timing, out = (Path(p) for p in sys.argv[1:6])
text = body.read_text()


def once(needle):
    if text.count(needle) != 1:
        sys.exit(f"anchor not unique: {needle!r} ({text.count(needle)})")
    return text.index(needle)


def replace_between(start, end, new):
    global text
    a, b = once(start), once(end)
    assert a < b, (start, end)
    text = text[:a] + new + text[b:]


def replace_line(old, new):
    global text
    once(old)
    text = text.replace(old, new)


replace_line("[A700d]\n", "[A700e]\n")
replace_line("- **[Status](#status)** -- Review ready at the head below; `787-reboot-reset` -> `dev`.",
             "- **[Status](#status)** -- STOP at the head below: the merge of dev is clean, the route misses the floor; "
             "`787-reboot-reset` -> `dev`.")
replace_between("## Status\n", "## Linked Issue / roles\n", status.read_text())
replace_line("Executor: `[A700d]` (round 3, the route; `[A700c]` round 2; `[A700]` round 1)",
             "Executor: `[A700e]` (round 4, the merge of dev; `[A700d]` round 3, the route; `[A700c]` round 2; "
             "`[A700]` round 1)")
replace_between("## How to validate\n", "### Route timing\n", validate.read_text())
replace_between("### Route timing\n", "## Known limitations / out of scope\n", timing.read_text())
replace_line("- [x] Required local verification bar passes (route-1x1 set, xvlog, IOB packing and the #607 log check "
             "included)",
             "- [ ] Required local verification bar passes (route-1x1 set: the #818 gate refuses it at this head, "
             "below the +0.030 ns floor; xvlog, IOB packing and the #607 log check pass)")
out.write_text(text)
print(f"wrote {out}: {len(text.splitlines())} lines")
