"""R317-2 part c: prior public round-1 spellings of the other reviewer's F1/F2
(C08-C11), reproduced from their published text, with and without a macro."""
GUARD = "\tif (id != MILAN_ID_MAGIC) {"
STATIC = "static int aem_loaded;"


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


def build(fw):
    def macro(rep):
        fw2 = once(fw, STATIC, f"#define MILAN_FORGE(x) {rep}\n\n{STATIC}")
        return once(fw2, GUARD, "\tMILAN_FORGE(id);\n" + GUARD)

    def plain(stmt):
        return once(fw, GUARD, "\t" + stmt + "\n" + GUARD)
    return [
        ("CTRL unchanged firmware", fw),
        ("PRIOR C08 macro (*(__extension__ &(x)) = MAGIC)",
         macro("(*(__extension__ &(x)) = MILAN_ID_MAGIC)")),
        ("PRIOR C09 plain (*(__extension__ &(id)) = MAGIC)",
         plain("(*(__extension__ &(id)) = MILAN_ID_MAGIC);")),
        ("PRIOR C10 macro asm li %0 output",
         macro('__asm__ volatile("li %0, 0x4d494c4e" : "=r"(x))')),
        ("PRIOR C11 plain asm li %0 output",
         plain('__asm__ volatile("li %0, 0x4d494c4e" : "=r"(id));')),
    ]
