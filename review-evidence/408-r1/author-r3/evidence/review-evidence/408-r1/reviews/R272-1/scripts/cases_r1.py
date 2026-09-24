"""R272-1 probe cases, round 1: conditionals whose `#` a form feed or a
vertical tab precedes. GCC 14.3 (-std=gnu99) honours such a line as a
directive; the gate's directive readers anchor on `^[ \\t]*#`.

Each hostile case has a control spelled with a plain `#`."""

UART_TAIL = "\tprint_tod(gettime_ns());\n}"
VERDICT = "\tif (!verified)\n\t\treturn;"
EID = "#define MILAN_ADP_EID_LO     0x604u\n"
STATIC = "static int aem_loaded;"


def first(text, old, new):
    """`text` with the FIRST `old` replaced; refuse a no-op."""
    assert old in text, f"anchor not found: {old!r}"
    return text.replace(old, new, 1)


def _cases(ns):
    fw = ns["firmware_source"]
    csr_base = ns["csr_base"]
    adp = ns["source_model"].adp
    adp_name = ns["adp_name"]
    raw = f"0x{csr_base + adp:08x}u"
    page = f"static unsigned int csr_page = 0x{csr_base >> 16:04x}u;\n\n"
    yield "control: shipping firmware", fw, None
    for tag, lead in (("plain #", ""), ("form feed", "\f"),
                      ("vertical tab", "\v")):
        yield (f"{tag}: product-only `0 &&` in the choke point verdict test",
               first(fw, VERDICT,
                     f"\tif (\n{lead}#ifdef CSR_UART_BASE\n\t    0 &&\n"
                     f"{lead}#endif\n\t    !verified)\n\t\treturn;"), None)
    for tag, lead in (("plain #", ""), ("form feed", "\f")):
        yield (f"{tag}: product-only paged-base cast store to ADP_CTRL in a "
               "UART handler",
               first(first(fw, STATIC, page + STATIC), UART_TAIL,
                     f"{lead}#ifdef CSR_UART_BASE\n\t*(volatile unsigned int *)"
                     f"((csr_page << 16) | {adp_name}) = 1u;\n{lead}#endif\n"
                     + UART_TAIL), None)
        yield (f"{tag}: product-only literal-address cast store to ADP_CTRL "
               "in a UART handler",
               first(fw, UART_TAIL,
                     f"{lead}#ifdef CSR_UART_BASE\n\t*(volatile unsigned int *)"
                     f"{raw} = 1u;\n{lead}#endif\n" + UART_TAIL), None)
        yield (f"{tag}: product-only lui asm store to ADP_CTRL in a UART "
               "handler",
               first(fw, UART_TAIL,
                     f"{lead}#ifdef CSR_UART_BASE\n\t__asm__ volatile("
                     f'"lui t0, 0x{csr_base >> 12:05x}\\n\\t"\n'
                     '\t                 "li t1, 1\\n\\t"\n'
                     f'\t                 "sw t1, 0x{adp:x}(t0)"\n'
                     '\t                 ::: "t0", "t1", "memory");\n'
                     f"{lead}#endif\n" + UART_TAIL), None)
        yield (f"{tag}: product-only arm moving ADP_EID_LO onto ADP_CTRL "
               "(product arm first)",
               first(fw, EID,
                     f"{lead}#ifdef CSR_UART_BASE\n#define MILAN_ADP_EID_LO     "
                     f"0x{adp:03x}u\n{lead}#else\n{EID}{lead}#endif\n"), None)
        yield (f"{tag}: product-only arm moving ADP_EID_LO onto ADP_CTRL "
               "(product arm last)",
               first(fw, EID,
                     f"{lead}#ifndef CSR_UART_BASE\n{EID}{lead}#else\n"
                     f"#define MILAN_ADP_EID_LO     0x{adp:03x}u\n"
                     f"{lead}#endif\n"), None)


def cases(ns):
    """The probe driver's dict form of each case."""
    for label, firmware, listing in _cases(ns):
        yield {"label": label, "firmware": firmware, "listing": listing}
