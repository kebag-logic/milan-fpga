#!/usr/bin/env python3
"""R624-7: Markdown (not HTML) constructs that render no visible character, placed between an identifier's
digit and a unit, against lane B16's round-7 figures check. Documents only, offline; edits copies only.

usage: <renderer python> -I probe_r624_7_markdown_escapes.py <repo at head> <author-r7 packet> <work dir> <out.json>

Each form is appended to the B16c attribution row (R625-6's insertion point); a form may also append a
definition block at the page's end (no line moves). For each form: the check's exit status and what it
names at the row's line, and the text a reader sees for the row (cmark-gfm, GitHub's options, text nodes
only). A form ESCAPES when the reader sees a digit run directly before a unit and the check exits 0.
"""
import json, re, subprocess, sys
from pathlib import Path
import cmarkgfm, html5lib
from cmarkgfm.cmark import Options

repo, packet, work, out = (Path(a).resolve() for a in sys.argv[1:5])
page = repo / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
orig = page.read_text(encoding="utf-8")
needle = "| Attribution | No loss in the network or the DUT | Every stage at the path's floor."
assert orig.count(needle) == 1
line = orig[:orig.index(needle)].count("\n") + 1
FORMS = {  # name: (inline form, definition appended at the page's end)
    "unchanged": ("", ""),
    "plain_control": (" CLOCK_DOMAIN 7 ppm.", ""),
    "full_stop_stated_limit": (" CLOCK_DOMAIN 7. ppm.", ""),
    "image_empty_alt_bang": (" CLOCK_DOMAIN 7![](x.png) ppm.", ""),
    "image_empty_alt_bang_glued": (" CLOCK_DOMAIN 7![](x.png)ppm.", ""),
    "image_alt_and": (" CLOCK_DOMAIN 7 ![and](x.png) ppm.", ""),
    "empty_link_title_and": (' CLOCK_DOMAIN 7[](#b16c-attribution "and") ppm.', ""),
    "label_link_title_and": (' [CLOCK_DOMAIN 7](#b16c-attribution "and") ppm.', ""),
    "empty_full_reference_and": (" CLOCK_DOMAIN 7[][and] ppm.", "\n[and]: #b16c-attribution\n"),
    "empty_full_reference_stop": (" CLOCK_DOMAIN 7[][.] ppm.", "\n[.]: #b16c-attribution\n"),
    "footnote_ref_and": (" CLOCK_DOMAIN 7[^and] ppm.", "\n[^and]: See the attribution.\n"),
    "pointy_destination_space_and": (" CLOCK_DOMAIN 7[](< and>) ppm.", ""),
    "image_title_and": (' CLOCK_DOMAIN 7![](x.png "and") ppm.', ""),
    "image_full_stop_alt": (" CLOCK_DOMAIN 7![.](x.png) ppm.", ""),
    "image_after_channel_index_db": (" Channel 2![](x.png) dB.", ""),
    "image_after_round_index_ms": (" Round 7![](x.png) ms.", ""),
    "image_after_identifier_furlongs": (" CLOCK_DOMAIN 7![](x.png) furlongs.", ""),
}


def visible(e):
    return (e.text or "") + "".join((visible(c) if isinstance(c.tag, str) else "") + (c.tail or "") for c in e)


res = []
for name, (form, tail) in FORMS.items():
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    text = orig.replace(needle, needle + form) + (("\n" if not orig.endswith("\n") else "") + tail if tail else "")
    assert text.count("\n") - orig.count("\n") == tail.count("\n") + (0 if orig.endswith("\n") or not tail else 1)
    (d / page.name).write_text(text, encoding="utf-8")
    (d / "README.md").write_bytes((page.parent / "README.md").read_bytes())
    p = subprocess.run([sys.executable, "-I", str(packet / "tools/check_b16_figures.py"), str(d / page.name), str(packet),
                        str(d / "rows.tsv"), str(d / "cov.tsv"), "--repo", str(repo)], capture_output=True, text=True,
                       timeout=300)
    row = text.splitlines()[line - 1]
    h = cmarkgfm.github_flavored_markdown_to_html(text, options=Options.CMARK_OPT_UNSAFE)
    v = visible(html5lib.parseFragment(h))
    s = v.find("Every stage at the path's floor.")
    seen = " ".join(v[s:s + 120].split())
    shows_measurement = bool(re.search(r"\d\s*(ppm|dB|ms|furlongs)\b", seen))
    named = [x for x in p.stdout.splitlines() if x.startswith(("UNCOVERED", "MARKUP", "BAD"))]
    res.append(dict(name=name, form=form, appended=tail, rc=p.returncode, summary=p.stdout.splitlines()[0],
                    named_at_or_near_line=[x[:240] for x in named][:6], reader_sees=seen,
                    reader_sees_digit_before_unit=shows_measurement,
                    escapes=bool(shows_measurement and p.returncode == 0),
                    rendered_fragment=cmarkgfm.github_flavored_markdown_to_html(form.strip(), options=Options.CMARK_OPT_UNSAFE)))
    print(name, "rc", p.returncode, "escapes", res[-1]["escapes"], "|", seen[:90])
json.dump(dict(line=line, forms=res), open(out, "w"), indent=1, ensure_ascii=False)
