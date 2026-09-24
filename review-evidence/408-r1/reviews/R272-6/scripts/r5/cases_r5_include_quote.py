"""R272-5: a `#include` operand whose apostrophe pair the lexer reads as a
character literal while GCC reads one header-name token, hiding U+00E9 from
the allowlist (which judges code outside literals). At the mutation-loop
hook: S's verdict on reader-level texts, then the whole gate on the shipping
firmware with such an include added in live code and in a skipped group.
Expected: whatever S says, the whole gate refuses the live include (the
include name pin), and the skipped one is lexed the same way by both sides
(GCC does not form a header name in a skipped group)."""


def cases(ns):
    check = ns["assert_within_lexical_subset"]
    for label, text in (
            ("live", "#include <a'é'b.h>\nint z;\n"),
            ("skipped", "#ifdef NEVER\n#include <a'é'b.h>\n#endif\nint z;\n")):
        try:
            check(text)
            print(f"S ADMITTED include-quote {label}", flush=True)
        except AssertionError as exc:
            print(f"S REFUSED include-quote {label}: {str(exc)[:150]}",
                  flush=True)
    fw = ns["firmware_source"]
    first = fw.index("#include")
    yield {"label": "[r5] live #include <a'U+00E9'b.h> added before the first "
                    "#include", "firmware": fw[:first] +
           "#include <a'é'b.h>\n" + fw[first:]}
    yield {"label": "[r5] the same #include in an #ifdef MILAN_NEVER_DEFINED "
                    "group", "firmware": fw[:first] +
           "#ifdef MILAN_NEVER_DEFINED\n#include <a'é'b.h>\n#endif\n" +
           fw[first:]}
