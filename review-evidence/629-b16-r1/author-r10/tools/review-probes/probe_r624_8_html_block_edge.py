#!/usr/bin/env python3
"""R624-8 probe: raw HTML blocks that open on an uncovered line and close on a covered one, and controls.

usage: probe_r624_8_html_block_edge.py <parser python> <check_b16_figures.py> <packet root> <repo> <workdir> <out.json>
Each case edits a copy of docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md (and README.md) in <workdir>, by
replacing whole lines so that no line moves, runs the check on it and records its exit code and every
MARKUP and UNCOVERED line it prints. A case that adds a figure no row claims must exit 1 to be detected."""
import concurrent.futures as cf
import json
import shutil
import subprocess
import sys
from pathlib import Path

PY, CHECK, PACKET, REPO, WORK, OUT = sys.argv[1:7]
PAGE = Path(REPO) / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
INDEX = Path(REPO) / "docs/findings/README.md"
SEC = "## Dev 5603c353, 2026-10-12: lane B16"
INTRO = "In lane B16, the operator tried the reference peer's own loopback"
TOC = "- **[Dev 5603c353, 2026-10-12: lane B16]"


def at(lines, prefix):
    return next(i for i, x in enumerate(lines) if x.startswith(prefix))


def edit(lines, i, new):
    lines[i] = new


def heading_pre(l, fig):
    i = at(l, SEC)
    assert l[i - 1] == ""
    edit(l, i - 1, "<pre>")
    edit(l, i, l[i] + fig + "</pre>")


def intro_pre(l, fig):
    i = at(l, INTRO)
    edit(l, i - 1, "<pre>")
    edit(l, i, l[i] + fig + "</pre>")


def toc_pre(l, fig):
    i = at(l, TOC)
    edit(l, i - 1, "<pre>")
    edit(l, i, l[i] + fig + "</pre>")


def intro_pre_close_second_line(l, fig):
    i = at(l, INTRO)
    edit(l, i - 1, "<pre>")
    edit(l, i + 1, l[i + 1] + fig + "</pre>")


def intro_div(l, fig):
    i = at(l, INTRO)
    edit(l, i - 1, "<div>")
    edit(l, i, l[i] + fig)


def emoji_shortcode(l, fig):
    i = at(l, "| Attribution | No loss in the network or the DUT |")
    edit(l, i, l[i].replace("Every stage at the path's floor.", "Every stage at the path's floor. CLOCK_DOMAIN 7:smile:ppm."))


def heading_comment(l, fig):
    i = at(l, SEC)
    edit(l, i - 1, "<!--")
    edit(l, i, l[i] + fig + " -->")


def inside_pre_one_line(l, fig):
    i = at(l, SEC)
    j = next(k for k in range(i + 1, len(l)) if l[k] == "")
    edit(l, j, "<pre>" + fig.strip() + "</pre>")


def inside_pre_two_lines(l, fig):
    i = at(l, SEC)
    j = next(k for k in range(i + 2, len(l)) if l[k] == "" and l[k + 1] == "" and l[k + 2] != "")
    edit(l, j, "<pre>")
    edit(l, j + 1, fig.strip() + "</pre>")


def link_title(l, fig):
    i = at(l, "| Attribution | No loss in the network or the DUT |")
    edit(l, i, l[i].replace("](#b16c-attribution)", '](#b16c-attribution "' + fig.strip() + '")'))


def heading_plain(l, fig):
    i = at(l, SEC)
    edit(l, i, l[i] + fig)


FIG = " THD+N -90 dB"
CASES = [
    ("unchanged", None, False),
    ("heading_plain_figure", heading_plain, True),
    ("heading_pre_from_line_above_no_figure", lambda l, f: heading_pre(l, ""), False),
    ("heading_pre_from_line_above_with_figure", heading_pre, True),
    ("intro_pre_from_line_above_with_figure", intro_pre, True),
    ("contents_pre_from_line_above_with_figure", toc_pre, True),
    ("intro_pre_closed_on_second_covered_line_with_figure", intro_pre_close_second_line, True),
    ("intro_div_from_line_above_with_figure", intro_div, True),
    ("heading_comment_from_line_above_with_figure", heading_comment, False),
    ("emoji_shortcode_between_identifier_and_unit", emoji_shortcode, False),
    ("inside_section_pre_one_line_with_figure", inside_pre_one_line, True),
    ("inside_section_pre_two_lines_with_figure", inside_pre_two_lines, True),
    ("link_title_with_figure", link_title, False),
]


def run(case):
    name, fn, adds_visible = case
    d = Path(WORK) / name / "docs/findings"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    lines = PAGE.read_text(encoding="utf-8").split("\n")
    if fn:
        fn(lines, FIG)
    (d / PAGE.name).write_text("\n".join(lines), encoding="utf-8")
    shutil.copyfile(INDEX, d / "README.md")
    p = subprocess.run([PY, "-I", CHECK, str(d / PAGE.name), PACKET, str(d / "rows.tsv"), str(d / "cov.tsv"),
                        "--repo", REPO, "--show", "1000"], capture_output=True, text=True)
    out = p.stdout.splitlines()
    return dict(case=name, adds_visible_unclaimed_figure=adds_visible, rc=p.returncode,
                summary=json.loads(out[0]) if out and out[0].startswith("{") else None,
                markup=[x for x in out if x.startswith("MARKUP")],
                uncovered=[x[:200] for x in out if x.startswith("UNCOVERED")],
                bad_rows=[x[:200] for x in out if x.startswith("BAD")][:10],
                stderr=p.stderr[-2000:],
                verdict=("DETECTED" if p.returncode == 1 else "ESCAPED") if adds_visible else
                ("PASS" if p.returncode == 0 else "FAIL"))


with cf.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(run, CASES))
Path(OUT).write_text(json.dumps(res, indent=1) + "\n")
for r in res:
    print(r["case"], "rc", r["rc"], r["verdict"], r["markup"][:2], r["uncovered"][:2], r["bad_rows"][:1])
