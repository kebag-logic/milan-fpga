#!/usr/bin/env python3
"""R624-9: does the figures check read text that follows an extended (bare) autolink?

usage: <parser python> probe_r624_9_autolink.py <check_b16_figures.py> <packet root> <repo at the head> <scratch> <out.json>

Each case appends a phrase to the END of one covered line (no line moves) in copies of the findings page and
the findings index taken from <repo>, runs the check on the copies with --repo <repo>, and records its exit
status and the UNCOVERED / MARKUP / BAD lines it prints. Every case adds the measurement "7 ppm", so the
check must exit 1 and name 7. A case where it exits 0 is an ESCAPE. Offline; documents only.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

CHECK, PACKET, REPO, SCRATCH, OUT = sys.argv[1:6]
REPO, SCRATCH = Path(REPO), Path(SCRATCH)
PAGE = (REPO / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md").read_text(encoding="utf-8").split("\n")
INDEX = (REPO / "docs/findings/README.md").read_text(encoding="utf-8").split("\n")


def find(lines, prefix):
    return next(i for i, x in enumerate(lines) if x.startswith(prefix))


INTRO = find(PAGE, "In lane B16, the operator tried the reference peer's own loopback") + 1  # second covered line
SECTION_PARA = find(PAGE, "The loopback did not form. The peer's listener, bound to its own talker,")
SECTION_PARA_2 = SECTION_PARA + 1  # a line inside that paragraph, not its first
ROW = find(INDEX, "| [629_MEDIA_CLOCK_FOLLOWING_BENCH.md]")
TABLE = find(PAGE, "| Restore | Done | See [B16: bench as left](#b16-bench-as-left) |")


def at_end_of_line(lines, i, phrase):
    out = list(lines)
    out[i] = out[i] + phrase
    return out


def before_last_bar(lines, i, phrase):
    out = list(lines)
    assert out[i].endswith(" |")
    out[i] = out[i][:-2] + phrase + " |"
    return out


CASES = [  # (name, which document, line index, how, phrase, expected: "detect" or "pass")
    ("unchanged", None, None, None, None, "pass"),
    ("intro_email_autolink_then_7ppm", "page", INTRO, at_end_of_line, " Write to x@example.com 7 ppm.", "detect"),
    ("intro_email_autolink_then_7ppm_no_space_word", "page", INTRO, at_end_of_line, " x@example.com, 7 ppm.", "detect"),
    ("intro_www_autolink_then_7ppm", "page", INTRO, at_end_of_line, " See www.example.com 7 ppm.", "detect"),
    ("intro_url_autolink_then_7ppm", "page", INTRO, at_end_of_line, " See https://example.com 7 ppm.", "detect"),
    ("intro_7ppm_alone", "page", INTRO, at_end_of_line, " It ran 7 ppm.", "detect"),
    ("section_para_first_line_email_then_7ppm", "page", SECTION_PARA, at_end_of_line, " x@example.com 7 ppm.", "detect"),
    ("section_para_later_line_email_then_7ppm", "page", SECTION_PARA_2, at_end_of_line, " x@example.com 7 ppm.", "detect"),
    ("section_table_cell_email_then_7ppm", "page", TABLE, before_last_bar, " x@example.com 7 ppm.", "detect"),
    ("index_row_email_then_7ppm", "index", ROW, before_last_bar, "; write to x@example.com 7 ppm.", "detect"),
    ("index_row_www_then_7ppm", "index", ROW, before_last_bar, "; see www.example.com 7 ppm.", "detect"),
    ("index_row_7ppm_alone", "index", ROW, before_last_bar, "; it ran 7 ppm.", "detect"),
    ("intro_mailto_autolink_then_7ppm", "page", INTRO, at_end_of_line, " Write mailto:x@example.com 7 ppm.", "detect"),
    ("intro_email_then_figure_on_next_word_run", "page", INTRO, at_end_of_line, " x@example.com: 7 ppm, 26 s, -3 dB.", "detect"),
    ("intro_and_index_email_then_7ppm", "both", (INTRO, ROW), None, (" Write to x@example.com 7 ppm.", "; write to x@example.com 7 ppm."), "detect"),
]

results = []
for name, which, i, how, phrase, expect in CASES:
    d = SCRATCH / name
    d.mkdir(parents=True, exist_ok=True)
    page, index = PAGE, INDEX
    if which == "page":
        page = how(PAGE, i, phrase)
    elif which == "index":
        index = how(INDEX, i, phrase)
    elif which == "both":
        page = at_end_of_line(PAGE, i[0], phrase[0])
        index = before_last_bar(INDEX, i[1], phrase[1])
    (d / "629_MEDIA_CLOCK_FOLLOWING_BENCH.md").write_text("\n".join(page), encoding="utf-8")
    (d / "README.md").write_text("\n".join(index), encoding="utf-8")
    p = subprocess.run([sys.executable, "-I", "-B", CHECK, str(d / "629_MEDIA_CLOCK_FOLLOWING_BENCH.md"), PACKET,
                        str(d / "rows.tsv"), str(d / "coverage.tsv"), "--repo", str(REPO)],
                       capture_output=True, text=True)
    named = [x for x in p.stdout.splitlines() if re.match(r"(UNCOVERED|MARKUP|BAD) ", x)]
    names_7 = any(re.match(r"UNCOVERED \S+ 7 ", x) for x in named)
    if expect == "pass":
        verdict = "OK" if p.returncode == 0 and not named else "UNEXPECTED"
    else:
        verdict = "DETECTED" if p.returncode == 1 and names_7 else ("ESCAPE" if p.returncode == 0 else "FAILED_OTHERWISE")
    results.append(dict(case=name, document=which, line=None if i is None else ([x + 1 for x in i] if isinstance(i, tuple) else i + 1), phrase=phrase, expect=expect,
                        exit=p.returncode, verdict=verdict, named=[x[:220] for x in named][:6],
                        summary=(p.stdout.splitlines() or [""])[0][:400], stderr=p.stderr[-400:]))
    print(name, p.returncode, verdict, named[:2])
Path(OUT).write_text(json.dumps(dict(check=CHECK, results=results), indent=1) + "\n")
sys.exit(0)
