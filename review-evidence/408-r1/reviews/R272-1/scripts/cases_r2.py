"""R272-1 probe cases, round 2: other ways a conditional the compiler
honours is not a conditional to the gate's text readers, and a control
showing that a store the TEXT rules can read is still refused whatever the
directive spelling."""

UART_TAIL = "\tprint_tod(gettime_ns());\n}"


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
    store = f"\t*(volatile unsigned int *){raw} = 1u;\n"
    yield ("control: form feed arm around a SPELLED milan_write enable in a "
           "UART handler",
           first(fw, UART_TAIL,
                 f"\f#ifdef CSR_UART_BASE\n\tmilan_write({adp_name}, "
                 f"milan_read({adp_name}) | 1u);\n\f#endif\n" + UART_TAIL),
           None)
    yield ("NUL byte before #: product-only literal-address cast store in a "
           "UART handler",
           first(fw, UART_TAIL,
                 f"\0#ifdef CSR_UART_BASE\n{store}\0#endif\n" + UART_TAIL),
           None)
    yield ("unterminated-quote defines around a product-only literal-address "
           "cast store in a UART handler",
           first(fw, UART_TAIL,
                 "#define MILAN_Q '\n#ifdef CSR_UART_BASE\n" + store +
                 "#endif\n#define MILAN_R '\n" + UART_TAIL), None)
    yield ("unterminated-quote defines around a product-only `0 &&` in the "
           "choke point verdict test",
           first(fw, "\tif (!verified)\n\t\treturn;",
                 "#define MILAN_Q '\n\tif (\n#ifdef CSR_UART_BASE\n\t    0 &&\n"
                 "#endif\n#define MILAN_R '\n\t    !verified)\n\t\treturn;"),
           None)
    yield ("form feed: product-only literal-address cast store inside "
           "configure_fabric() (a boot-path body)",
           first(fw, "\tmilan_write(MILAN_CRF_TX_CTRL, MILAN_CRF_TX_CTRL_BOOT);\n}",
                 "\tmilan_write(MILAN_CRF_TX_CTRL, MILAN_CRF_TX_CTRL_BOOT);\n"
                 f"\f#ifdef CSR_UART_BASE\n{store}\f#endif\n}}"), None)


def cases(ns):
    """The probe driver's dict form of each case."""
    for label, firmware, listing in _cases(ns):
        yield {"label": label, "firmware": firmware, "listing": listing}
