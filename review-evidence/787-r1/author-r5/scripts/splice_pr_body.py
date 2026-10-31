"""splice_pr_body.py <round-4-body> <status.md> <validate.md> <out>: round 4's PR-BODY.md with this round's Status and
How to validate sections (the latter with its Route timing subsection) replaced whole, the first line and the executor
line naming this round, the contents line and the verification-bar box stating the round's verdict, and one line
under the linked issues that this PR carries PR #826's commits and merges after it. Every other byte is kept.
Refuses unless each anchor appears exactly once."""
import sys
from pathlib import Path

body, status, validate, out = (Path(p) for p in sys.argv[1:5])
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


replace_line("[A700e]\n", "[A700f]\n")
replace_line("- **[Status](#status)** -- STOP at the head below: the merge of dev is clean, the route misses the floor; "
             "`787-reboot-reset` -> `dev`.",
             "- **[Status](#status)** -- Review ready at the head below, carrying PR #826's commits; the route meets "
             "the floor; `787-reboot-reset` -> `dev`.")
replace_between("## Status\n", "## Linked Issue / roles\n", status.read_text())
replace_line("Relates to #396\n",
             "Relates to #396\n\nCarries PR #826 (#814): this PR holds its commits, through the merge of "
             "`814-soc-timing-cut` at `4ee2aa96`, and merges after it.\n")
replace_line("Executor: `[A700e]` (round 4, the merge of dev; `[A700d]` round 3, the route; `[A700c]` round 2; "
             "`[A700]` round 1)",
             "Executor: `[A700f]` (round 5, the merge of PR #826; `[A700e]` round 4, the merge of dev; `[A700d]` "
             "round 3, the route; `[A700c]` round 2; `[A700]` round 1)")
replace_between("## How to validate\n", "## Known limitations / out of scope\n", validate.read_text())
replace_line("- [ ] Required local verification bar passes (route-1x1 set: the #818 gate refuses it at this head, "
             "below the +0.030 ns floor; xvlog, IOB packing and the #607 log check pass)",
             "- [x] Required local verification bar passes (route-1x1 set, xvlog, IOB packing and the #607 log check "
             "included)")
out.write_text(text)
print(f"wrote {out}: {len(text.splitlines())} lines")
