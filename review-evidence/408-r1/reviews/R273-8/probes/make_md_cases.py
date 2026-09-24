#!/usr/bin/env python3
"""R273-5 cases: an extended identifier character in a directive name.

GCC 14.3 at -std=gnu99 takes U+00B7 (and U+0387, U+203F) as an identifier
character, as it takes `$`: `#if·x` is ONE unknown directive, ignored in
skipped code. S refuses `$` and `\\` but not a non-ASCII character; the
directive readers stop a name at `\\b`, so they read `#if`. The shape below
is balanced for BOTH readings: GCC compiles LINE, the readers put it in an arm
of a macro that nothing defines.

usage: make_md_cases.py <repo-root> <out.json>
"""
import json
from pathlib import Path
import sys


def hidden(line, ch):
    return ("#ifdef MILAN_NEVER_DEFINED\n#if" + ch + "x\n#endif\n" + line +
            "\n#ifdef MILAN_NEVER_DEFINED\n#endif" + ch + "y\n#endif\n")


def once(text, old, new):
    assert text.count(old) >= 1, old  # first occurrence, as round four
    return text.replace(old, new, 1)


def main():
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    fw = (root / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text(
        encoding="utf-8")
    id_read = "\tuint32_t id = milan_read(MILAN_ID);\n"
    verdict = "\taem_loaded = load_aem_image();\n"
    uart_tail = "\tprint_tod(gettime_ns());\n}"
    forge = "\tid = MILAN_ID_MAGIC;"
    enable = "\tmilan_write(MILAN_ADP_CTRL, milan_read(MILAN_ADP_CTRL) | 1u);"
    poke = "\t*(volatile unsigned int *)0x90000600u = 1u;"
    md = "·"
    cases = [
        {"label": "MD1 literal-address cast store into the CSR window in a "
                  "UART handler, hidden by U+00B7 in two directive names",
         "firmware": once(fw, uart_tail, hidden(poke, md) + uart_tail)},
        {"label": "MD1a the same store hidden by U+0387",
         "firmware": once(fw, uart_tail, hidden(poke, "·") + uart_tail)},
        {"label": "MD1b the same store hidden by U+203F",
         "firmware": once(fw, uart_tail, hidden(poke, "‿") + uart_tail)},
        {"label": "MD1c control: the same store hidden by `$` (S refuses)",
         "firmware": once(fw, uart_tail, hidden(poke, "$") + uart_tail)},
        {"label": "MD1p control: the same store, plain",
         "firmware": once(fw, uart_tail, poke + "\n" + uart_tail)},
        {"label": "MD2 identity sample forged in milan_init(), hidden by "
                  "U+00B7",
         "firmware": once(fw, id_read, id_read + hidden(forge, md))},
        {"label": "MD3 ADP enable in a UART handler, hidden by U+00B7",
         "firmware": once(fw, uart_tail, hidden(enable, md) + uart_tail)},
        {"label": "MD4 AEM verdict overwritten after the verifier, hidden "
                  "by U+00B7",
         "firmware": once(fw, verdict, verdict + hidden("\taem_loaded = 1;",
                                                        md))},
        {"label": "MD5 benign control: a printf in a UART handler, hidden "
                  "by U+00B7",
         "firmware": once(fw, uart_tail,
                          hidden("\tprintf(\"r273\\n\");", md) + uart_tail)},
        {"label": "MD6 benign control: U+00B7 in a comment only",
         "firmware": once(fw, uart_tail,
                          "\t/* r273 · */\n" + uart_tail)},
    ]
    out.write_text(json.dumps(cases, indent=1, ensure_ascii=True) + "\n",
                   encoding="utf-8")
    print(f"{len(cases)} cases -> {out}")


if __name__ == "__main__":
    main()
