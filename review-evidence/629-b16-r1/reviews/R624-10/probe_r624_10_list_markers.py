#!/usr/bin/env python3
"""R624-10 probe: digits a reader sees that no paragraph, heading or table cell holds.

usage: <pinned-parser python> -I probe_r624_10_list_markers.py <repo> <packet> <scratch> <out.json>

Each case copies the findings page and the findings index into <scratch>/<case>/docs/findings/, applies one
edit that moves no earlier line (a line appended after the page's last line, or a whole line replaced by one),
runs the packet's tools/check_b16_figures.py on the copy with --repo <repo>, and records its exit status, its
summary and each line it names. It also renders the edited page with the pinned renderer
(scripts/gen_toc_renderer.py's cmark-gfm options and extensions) and records the HTML around the edit, so a
reader can see what GitHub would show. An `escape` is a case whose edit puts a number in front of a reader
(a list item's marker) and the check exits 0.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO, PK, SCR, OUT = (Path(a).resolve() for a in sys.argv[1:5])
PAGE = "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
INDEX = "docs/findings/README.md"


def page_lines():
    return (REPO / PAGE).read_text(encoding="utf-8").split("\n")


def find(lines, prefix):
    return next(i for i, x in enumerate(lines) if x.startswith(prefix))


def cases():
    out = []
    base = page_lines()
    end = len(base) - 1 if base[-1] == "" else len(base)

    def append(name, text, detect, note):
        out.append((name, ("append", text), detect, note))

    def replace(name, prefix, new, detect, note):
        out.append((name, ("replace", prefix, new), detect, note))

    append("append_ordered_17_ppm", "\n17. ppm: the peer's offset in B-AAF, against the DUT's TDM clock.\n", True,
           "an ordered list after the page's last line, starting at 17; the item text holds no digit")
    append("append_ordered_paren_17_ppm", "\n17) ppm: the peer's offset in B-AAF, against the DUT's TDM clock.\n",
           True, "the same with a ) delimiter")
    append("append_ordered_131_blocks", "\n131. blocks sat off the floor in B-CRF, not none.\n", True,
           "an ordered list starting at 131, stating a block count no receipt holds")
    append("append_ordered_1_control", "\n1. ppm: a list starting at one, as on the page.\n", True,
           "a list starting at 1, the form the page already uses for its steps")
    append("append_ordered_digit_in_text_control", "\n17. the peer's offset was 17 ppm.\n", True,
           "control: the same list with the figure written in the item's text, which the check reads")
    append("append_bullet_no_digit_control", "\n- a bullet item with no digit.\n", False,
           "control: a bullet list with no digit, which should pass")
    i = find(base, "1. a set of the peer's CLOCK_DOMAIN to its internal source for B-CRF and")
    replace("replace_decision_list_start_7", base[i], "7" + base[i][1:], True,
            "the B16b decision list renumbered to start at 7 (its items then show 7., 8. and 9.)")
    i = find(base, "1. Refuse to start unless the tone plays")
    replace("replace_step_list_start_300", base[i], "300" + base[i][1:], True,
            "the B16c method's step list renumbered to start at 300")
    return out, end


def render(md):
    """The pinned renderer, as scripts/gen_toc_renderer.py configures it: the HTML cmark-gfm emits."""
    sys.path.insert(0, str(REPO / "scripts"))
    import gen_toc_renderer as R  # noqa: E402
    from cmarkgfm import _cmark
    lib = _cmark.lib
    lib.cmark_gfm_core_extensions_ensure_registered()
    o =lib.CMARK_OPT_UNSAFE | lib.CMARK_OPT_FOOTNOTES | lib.CMARK_OPT_GITHUB_PRE_LANG
    p = lib.cmark_parser_new(o)
    for name in R.EXTENSIONS:
        lib.cmark_parser_attach_syntax_extension(p, lib.cmark_find_syntax_extension(name.encode()))
    raw = md.encode()
    lib.cmark_parser_feed(p, raw, len(raw))
    h = lib.cmark_render_html(lib.cmark_parser_finish(p), o, lib.cmark_parser_get_syntax_extensions(p))
    s = _cmark.ffi.string(h).decode()
    lib.cmark_parser_free(p)
    return s


def main():
    results = []
    todo, end = cases()
    for name, edit, detect, note in todo:
        d = SCR / name
        shutil.rmtree(d, ignore_errors=True)
        (d / "docs/findings").mkdir(parents=True)
        shutil.copyfile(REPO / INDEX, d / INDEX)
        text = (REPO / PAGE).read_text(encoding="utf-8")
        if edit[0] == "append":
            new = text + edit[1]
            line = end + 2
        else:
            lines = text.split("\n")
            i = lines.index(edit[1])
            lines[i] = edit[2]
            new = "\n".join(lines)
            line = i + 1
        assert new.count("\n") - text.count("\n") in (0, 2)
        (d / PAGE).write_text(new, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(PK / "tools/check_b16_figures.py"), str(d / PAGE), str(PK),
                            str(d / "rows.tsv"), str(d / "cov.tsv"), "--repo", str(REPO)],
                           capture_output=True, text=True)
        out = r.stdout.splitlines()
        named = [x for x in out[1:] if x.split(" ", 1)[0] in ("BAD", "UNCOVERED", "MARKUP")]
        html = render(new)
        tail = html[-600:] if edit[0] == "append" else ""
        if edit[0] == "replace":
            starts = re.findall(r"<ol start=\"(\d+)\"", html)
            tail = "ol start attributes in the rendered page: " + ", ".join(starts)
        results.append(dict(case=name, note=note, edited_line=line, edit=edit[1] if edit[0] == "append" else edit[2],
                            rc=r.returncode, summary=json.loads(out[0]) if out else None, named=named,
                            stderr_tail=r.stderr[-400:], rendered=tail,
                            reader_sees_unjudged_number=detect and r.returncode == 0 and not named,
                            outcome=("ESCAPE" if detect and r.returncode == 0 else
                                     "DETECTED" if detect else ("PASS" if r.returncode == 0 else "FALSE_REFUSAL"))))
    OUT.write_text(json.dumps(dict(repo_head=subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                                                            capture_output=True, text=True).stdout.strip(),
                                   results=results), indent=1) + "\n")
    for x in results:
        print(x["outcome"], x["case"], "rc", x["rc"], "line", x["edited_line"], "|", "; ".join(x["named"])[:200])


if __name__ == "__main__":
    main()
