"""R272-5 allowlist cases, taken at the mutation-loop hook
(probe_gate1b.py --anchor mutations):

  * every entry of the gate's own `mutations` tuple pinned on
    SUBSET_CHARACTER_PIN (the round-four allowlist entries and the three
    byte-order-mark entries re-pinned on it), graded with that pin;
  * this reviewer's round-three/four reader-level shapes (U+00B2, U+00E9,
    U+00B7, U+0301 after `#if`) lifted into the balanced whole-firmware
    misnest around a CSR-window store in a UART handler, plus U+2028 and
    U+00A0 variants, each expected refused on the allowlist;
  * the unmodified shipping firmware as a control (expected ACCEPTED).

Run once connected and once with the allowlist disconnected (patch
r5/patches/disconnect-allowlist.json), in both compiler modes."""


def cases(ns):
    import os
    pin = ns["SUBSET_CHARACTER_PIN"]
    only_r5 = os.environ.get("R272_ONLY_R5") == "1"
    for mutation in () if only_r5 else ns["mutations"]:
        if len(mutation) >= 5 and mutation[4] == pin:
            label, firmware, docs, csr, because = mutation[:5]
            assert docs is ns["docs_source"] and csr is ns["csr_source"]
            yield {"label": "[gate] " + label, "firmware": firmware,
                   "because": because}
    fw = ns["firmware_source"]
    store = f"\t*(volatile unsigned int *){ns['raw_address']} = 1u;"
    for code in (0xB2, 0xE9, 0xB7, 0x301, 0x2028, 0xA0):
        ch = chr(code)
        # the gate's own helper places the text in a UART command handler
        text = ns["in_uart_handler"](
            f"#ifdef MILAN_NEVER_DEFINED\n#if{ch}a\n#endif\n{store}\n"
            f"#ifdef MILAN_NEVER_DEFINED\n#endif{ch}b\n#endif",
            f"r5 misnest U+{code:04X}")
        yield {"label": f"[r5] window store between two directive names "
                        f"spelled with U+{code:04X}", "firmware": text,
               "because": pin}
    yield {"label": "[r5] control: the shipping firmware unchanged",
           "firmware": fw}
