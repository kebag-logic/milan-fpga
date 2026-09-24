"""R272-1 probe cases, round 3: what base ALREADY let through, so that each
head/base difference is read against base's own exposure rather than against
a protection base never had.

  * the CSR identity sample forged in milan_init() three ways: a plain
    function-like macro (no splice, no paste), a token-joining splice of the
    local's name, and a `##` paste of it. The `-E` comparison reads only the
    eight boot tokens and the statement count, so a name a splice or a paste
    rebuilds outside those tokens is not compared.
  * a struct-overlay store to ADP_CTRL in a product-only arm of a UART
    handler, spelled with a plain `#` and with a form feed before `#`."""

UART_TAIL = "\tprint_tod(gettime_ns());\n}"
GUARD = "\tif (id != MILAN_ID_MAGIC) {"
STATIC = "static int aem_loaded;"


def first(text, old, new):
    """`text` with the FIRST `old` replaced; refuse a no-op."""
    assert old in text, f"anchor not found: {old!r}"
    return text.replace(old, new, 1)


def cases(ns):
    fw = ns["firmware_source"]
    csr_base = ns["csr_base"]
    adp = ns["source_model"].adp
    raw = f"0x{csr_base + adp:08x}u"
    yield {"label": "identity forged through a plain function-like macro",
           "firmware": first(first(fw, STATIC,
                                   "#define MILAN_FORGE(x) x = MILAN_ID_MAGIC\n\n"
                                   + STATIC),
                             GUARD, "\tMILAN_FORGE(id);\n" + GUARD)}
    yield {"label": "identity forged through a token-joining splice of the "
                    "local's name",
           "firmware": first(fw, GUARD, "\ti\\\nd = MILAN_ID_MAGIC;\n" + GUARD)}
    yield {"label": "identity forged through a ## paste of the local's name",
           "firmware": first(first(fw, STATIC,
                                   "#define MILAN_CAT(a, b) a##b\n\n" + STATIC),
                             GUARD,
                             "\tMILAN_CAT(i, d) = MILAN_ID_MAGIC;\n" + GUARD)}
    typedef = "typedef struct { volatile uint32_t ctrl; } *milan_arm_blk;\n\n"
    for tag, lead in (("plain #", ""), ("form feed", "\f")):
        yield {"label": f"{tag}: product-only struct-overlay store to ADP_CTRL "
                        "in a UART handler",
               "firmware": first(first(fw, STATIC, typedef + STATIC), UART_TAIL,
                                 f"{lead}#ifdef CSR_UART_BASE\n\t((milan_arm_blk)"
                                 f"{raw})->ctrl = 1u;\n{lead}#endif\n"
                                 + UART_TAIL)}
