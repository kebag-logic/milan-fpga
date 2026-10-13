#!/usr/bin/env python3
"""R624-10 probe: this review's own forms against round 10's two rules (no position; digit conservation).

usage: <pinned-parser python> -I probe_r624_10_own_forms.py <repo> <packet> <scratch> <out.json>

Each case edits a copy of the findings page or the index row without moving a line (text appended to a line,
or one line appended after the page's last), runs the packet's check with --repo <repo>, and records its exit
status and the lines it names. `expect` is what a check that judges every digit a reader sees should do:
`detect` (exit 1) or `pass` (exit 0). `stated` marks a form the page already lists as a limit.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO, PK, SCR, OUT = (Path(a).resolve() for a in sys.argv[1:5])
PAGE, INDEX = "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md", "docs/findings/README.md"
SEC_P = "The loopback did not form. The peer's listener, bound to its own talker,"  # line 2301
ROW = "| Restore | Done | See [B16: bench as left](#b16-bench-as-left) |"           # line 2324

CASES = [
    # (name, target, how, text, expect, stated)
    ("section_entity_digit_before_unit", "page", ("line_end", SEC_P), " See &#55; ppm.", "detect", False),
    ("section_entity_hex_digit_before_unit", "page", ("line_end", SEC_P), " See &#x37; ppm.", "detect", False),
    ("section_half_entity_before_unit", "page", ("line_end", SEC_P), " See &half; ppm.", "detect", False),
    ("section_strike_text_with_figure", "page", ("line_end", SEC_P), " See ~~7 ppm~~.", "detect", False),
    ("section_link_text_figure_resolving_target", "page", ("line_end", SEC_P), " See [7 ppm](#b16-limits).",
     "detect", False),
    ("cell_ordered_list_like_text", "page", ("cell_end", ROW), " 7. ppm", "detect", False),
    ("cell_entity_before_unit", "page", ("cell_end", ROW), " &#55; ppm", "detect", False),
    ("index_half_entity_before_covered_part", "index", ("index_before", "Lane B16, `5603c353`:"), "&half; ",
     "pass", False),
    ("index_entity_digit_in_covered_part", "index", ("index_cell_end", None), "; &#55; ppm", "detect", False),
    ("append_nested_ordered_in_bullet", "page", ("append", None), "\n- Lock times:\n  17. ppm, the peer's offset.\n",
     "detect", True),
    ("append_quoted_ordered", "page", ("append", None), "\n> 17. ppm, the peer's offset.\n", "detect", True),
    ("append_emoji_keycap_shortcode", "page", ("append", None), "\nThe offset was :seven: ppm.\n", "detect", True),
]


def main():
    res = []
    for name, target, (how, anchor), text, expect, stated in CASES:
        d = SCR / name
        shutil.rmtree(d, ignore_errors=True)
        (d / "docs/findings").mkdir(parents=True)
        page = (REPO / PAGE).read_text(encoding="utf-8")
        index = (REPO / INDEX).read_text(encoding="utf-8")
        if target == "page":
            ls = page.split("\n")
            if how == "append":
                new = page + text
                line = len(ls) + (1 if page.endswith("\n") else 0) + 1
            else:
                i = ls.index(anchor)
                ls[i] = ls[i] + text if how == "line_end" else ls[i][:-1].rstrip() + text + " |"
                new, line = "\n".join(ls), i + 1
            assert new.count("\n") - page.count("\n") in (0, text.count("\n"))
            page = new
            where = f"629_MEDIA_CLOCK_FOLLOWING_BENCH.md:{line}"
        else:
            ls = index.split("\n")
            i = next(k for k, x in enumerate(ls) if x.startswith("| [629_MEDIA_CLOCK_FOLLOWING_BENCH.md]"))
            if how == "index_before":
                ls[i] = ls[i].replace(anchor, text + anchor, 1)
            else:
                ls[i] = ls[i][:-1].rstrip() + text + " |"
            index = "\n".join(ls)
            where = f"README.md:{i + 1}"
        (d / PAGE).write_text(page, encoding="utf-8")
        (d / INDEX).write_text(index, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(PK / "tools/check_b16_figures.py"), str(d / PAGE), str(PK),
                            str(d / "rows.tsv"), str(d / "cov.tsv"), "--repo", str(REPO), "--show", "200"],
                           capture_output=True, text=True)
        named = [x for x in r.stdout.splitlines()[1:] if x.split(" ", 1)[0] in ("UNCOVERED", "MARKUP")]
        bad = sum(1 for x in r.stdout.splitlines()[1:] if x.startswith("BAD"))
        got = "detect" if r.returncode == 1 else "pass" if r.returncode == 0 else f"rc {r.returncode}"
        res.append(dict(case=name, edited=where, text=text, expect=expect, stated_limit=stated, rc=r.returncode,
                        named=named, bad_rows=bad, stderr_tail=r.stderr[-300:],
                        outcome="MET" if got == expect else ("STATED LIMIT" if stated else "NOT MET")))
        print(res[-1]["outcome"], name, "rc", r.returncode, where, "|", "; ".join(n[:110] for n in named[:2]))
    OUT.write_text(json.dumps(dict(results=res), indent=1) + "\n")


if __name__ == "__main__":
    main()
