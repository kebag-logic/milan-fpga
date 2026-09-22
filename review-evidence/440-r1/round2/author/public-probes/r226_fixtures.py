"""R226 independent fixture population for issue #440 closing conditions.

Designed by the reviewer, not copied from the author's measure.py. Every
fixture is synthetic text; each places exactly one `## Probe` heading after
(or, for the EOF controls, inside) the delimiter under test, so the rendered
<h2> count is 0 or 1 and is directly comparable with the walk's heading count.
"""

REFUSED_26 = [0x0b, 0x0c, 0x0d, 0x1c, 0x1d, 0x1e, 0x1f, 0x85, 0xa0, 0x1680,
              *range(0x2000, 0x200b), 0x2028, 0x2029, 0x202f, 0x205f, 0x3000]
# Characters that are neither blank nor refused: a page carrying one IS walked,
# so the raw decision itself is the shipped answer.
UNREFUSED_NONBLANK = [0x00, 0x200b, 0xfeff, 0x180e, 0x2060]
NAMES = ("pre", "script", "style", "textarea")


def alt_case(name: str) -> str:
    return "".join(c.upper() if i % 2 else c for i, c in enumerate(name))


def fixtures() -> list[dict]:
    rows: list[dict] = []

    def add(rid: str, family: str, source: str) -> None:
        rows.append({"id": rid, "family": family, "source": source})

    # ---- fence trailers -------------------------------------------------
    for fname, f in (("bt", "```"), ("tl", "~~~")):
        other = "~" if f[0] == "`" else "`"
        trailers = [("empty", ""), ("sp", " "), ("tab", "\t"), ("sp2", "  "),
                    ("sp-tab-sp", " \t "), ("tab2", "\t\t")]
        trailers += [(f"U{c:04X}", chr(c)) for c in REFUSED_26]
        trailers += [(f"U{c:04X}", chr(c)) for c in UNREFUSED_NONBLANK]
        trailers += [("x", "x"), ("sp-x", " x"), ("tab-x", "\tx"),
                     ("other", other), ("sp-other", " " + other),
                     ("sp-ff", " \f"), ("tab-nbsp", "\t ")]
        for key, t in trailers:
            add(f"R226-F-{fname}-{key}", "fence-trailer", f"{f}\n{f}{t}\n## Probe\n")
        # longer and shorter runs
        for key, t in (("empty", ""), ("sp", " "), ("tab", "\t"), ("ff", "\f"), ("x", "x")):
            add(f"R226-F-{fname}-longer-{key}", "fence-length", f"{f}\n{f}{f[0]}{t}\n## Probe\n")
        add(f"R226-F-{fname}-shorter", "fence-length", f"{f}{f[0]}\n{f}\n## Probe\n")
        add(f"R226-F-{fname}-much-longer", "fence-length", f"{f}\n{f[0] * 40}\t \n## Probe\n")
        # indentation of the closer
        for key, ind in (("1sp", " "), ("3sp", "   "), ("4sp", "    "), ("tab", "\t"), ("sp-tab", " \t")):
            add(f"R226-F-{fname}-indent-{key}", "fence-indent", f"{f}\n{ind}{f}\n## Probe\n")
        add(f"R226-F-{fname}-other-char", "fence-kind", f"{f}\n{other * 3}\n## Probe\n")
        # EOF boundaries
        add(f"R226-F-{fname}-eof-heading-nolf", "fence-eof", f"{f}\n{f}\n## Probe")
        add(f"R226-F-{fname}-eof-trailer-nolf", "fence-eof", f"{f}\n{f} \t\n## Probe")
        add(f"R226-F-{fname}-eof-unclosed", "fence-eof", f"{f}\n## Probe\n")
        add(f"R226-F-{fname}-eof-unclosed-nolf", "fence-eof", f"{f}\n## Probe")
        add(f"R226-F-{fname}-eof-closer-after", "fence-eof", f"{f}\n## Probe\n{f}")

    # ---- type-1 closing names ---------------------------------------------
    for opener in NAMES:
        for closer in NAMES:
            add(f"R226-T-name-later-{opener}-{closer}", "type1-name",
                f"<{opener}>\n</{closer}>\n## Probe\n")
            add(f"R226-T-name-later-{opener}-{alt_case(closer)}", "type1-name",
                f"<{opener}>\n</{alt_case(closer)}>\n## Probe\n")
            add(f"R226-T-name-opening-{opener}-{alt_case(closer)}", "type1-name",
                f"<{opener}>x</{alt_case(closer)}>\n## Probe\n")
    # inner characters before '>' for every name
    inner = [("sp", " "), ("tab", "\t"), ("sp2", "  "), ("ff", "\f"), ("vt", "\v"),
             ("nbsp", " "), ("ideo", "　"), ("nul", "\x00"), ("zwsp", "​")]
    for name in NAMES:
        for key, ch in inner:
            add(f"R226-T-inner-{name}-{key}", "type1-inner", f"<{name}>\n</{name}{ch}>\n## Probe\n")
    add("R226-T-inner-opening-sp", "type1-inner", "<pre></pre >\n## Probe\n")
    add("R226-T-inner-opening-tab", "type1-inner", "<script>x</script\t>\n## Probe\n")
    add("R226-T-slash-sp", "type1-malformed", "<pre>\n</ pre>\n## Probe\n")
    add("R226-T-slash-tab", "type1-malformed", "<pre>\n</\tpre>\n## Probe\n")
    add("R226-T-attr", "type1-malformed", "<pre>\n</pre x>\n## Probe\n")
    add("R226-T-selfclose", "type1-malformed", "<pre>\n</pre/>\n## Probe\n")
    add("R226-T-split", "type1-malformed", "<pre>\n</pre\n>\n## Probe\n")
    add("R226-T-no-slash", "type1-malformed", "<pre>\n<pre>\n## Probe\n")
    for key, bad in (("prelude", "prelude"), ("pres", "pres"), ("scripts", "scripts"),
                     ("styles", "styles"), ("textareas", "textareas"), ("pr", "pr"),
                     ("scrip", "scrip"), ("textare", "textare")):
        add(f"R226-T-longer-shorter-{key}", "type1-malformed", f"<pre>\n</{bad}>\n## Probe\n")
    # deliberately constrained case folding
    for key, bad in (("longs-script", "ſcript"), ("longs-style", "ſtyle"),
                     ("dotless-script", "scrıpt"), ("dotted-script", "scrİpt"),
                     ("longs-upper", "ſCRIPT"), ("dotted-upper", "SCRİPT"),
                     ("fullwidth-pre", "ｐｒｅ")):
        add(f"R226-T-fold-{key}", "type1-fold", f"<script>\n</{bad}>\n## Probe\n")
    add("R226-T-fold-upper-opener", "type1-fold", "<SCRIPT>\n</sCrIpT>\n## Probe\n")
    # embedded closers
    add("R226-T-embedded-mid", "type1-embedded", "<pre>\nfoo </textarea> bar\n## Probe\n")
    add("R226-T-embedded-twice", "type1-embedded", "<pre>\n</pre></pre>\n## Probe\n")
    add("R226-T-embedded-opening-attr", "type1-embedded", "<pre title=\"</style>\">\n## Probe\n")
    add("R226-T-embedded-backslash", "type1-embedded", "<pre>\n\\</pre>\n## Probe\n")
    # opener variants
    add("R226-T-opener-upper", "type1-opener", "<PRE>\n</pre>\n## Probe\n")
    add("R226-T-opener-attr-cross", "type1-opener", "<pre class=\"x\">\n</style>\n## Probe\n")
    add("R226-T-opener-eol-cross", "type1-opener", "<textarea\n</script>\n## Probe\n")
    # reset and precedence
    add("R226-T-reset-second-open", "type1-reset", "<pre>\n</pre>\n<style>\n## Probe\n")
    add("R226-T-reset-same-line", "type1-reset", "<pre></pre>\n## Probe\n")
    add("R226-T-prec-type6", "type1-precedence", "<div>\n</pre>\n## Probe\n")
    add("R226-T-prec-comment", "type1-precedence", "<!--\n</pre>\n## Probe\n")
    add("R226-T-prec-fence", "type1-precedence", "~~~\n</textarea>\n## Probe\n")
    add("R226-T-prec-fence-in-type1", "type1-precedence", "<pre>\n```\n## Probe\n")
    add("R226-T-prec-blank-survives", "type1-precedence", "<pre>\n\n## Probe\n")
    # EOF
    add("R226-T-eof-heading-nolf", "type1-eof", "<pre>\n</pre>\n## Probe")
    add("R226-T-eof-unclosed", "type1-eof", "<pre>\n## Probe\n")
    add("R226-T-eof-truncated-closer", "type1-eof", "<pre>\n## Probe\n</pre")

    # ---- closing tags of names outside the four (negative space of the set) --
    for opener in ("pre", "script"):
        for other in ("div", "title", "xmp", "plaintext", "p", "span", "noscript",
                      "iframe", "listing", "noembed", "noframes", "code"):
            add(f"R226-T-othername-{opener}-{other}", "type1-othername",
                f"<{opener}>\n</{other}>\n## Probe\n")

    # ---- carriage returns (raw helper vs shipped readers) -------------------
    for rid, src in (
        ("crlf-fence", "```\r\n```\r\n## Probe\r\n"),
        ("cr-fence", "```\r```\r## Probe\r"),
        ("mixed-fence", "```\n```\r\n## Probe\n"),
        ("crlf-fence-trailer", "```\r\n``` \t\r\n## Probe\r\n"),
        ("cr-then-text", "```\n```\r x\n## Probe\n"),
        ("crlf-type1-same", "<pre>\r\n</pre>\r\n## Probe\r\n"),
        ("cr-type1-cross", "<pre>\r</style>\r## Probe\r"),
        ("cr-inside-closer", "<pre>\n</pre\r>\n## Probe\n"),
        ("crlf-inner-blank", "<pre>\r\n</pre >\r\n## Probe\r\n"),
        ("crlf-eof-nolf", "~~~\r\n~~~\r\n## Probe"),
    ):
        add(f"R226-C-{rid}", "cr", src)
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate fixture id"
    return rows
