#!/usr/bin/env python3
"""Build the reviewer's probe cases from the shipping firmware text.

The firmware (sw/firmware/milan_baremetal/milan_baremetal.c) is byte-identical
at dev 759da623 and at the reviewed head a13b6e2e, so one case list serves
both. Each case is {label, firmware[, listing]}; probe.py grades it through
gate 1b's whole boot contract.

Usage: make_cases.py <firmware.c> <out-dir>
Writes accepted.json (the retired rules' accepted cases, as the head gate
spells them), hostile.json (reviewer probes) and listing_base.json /
listing_head.json (the directory accepted case in each checkout's own
`listing` convention).
"""

import json
from pathlib import Path
import sys

fw_path, out = Path(sys.argv[1]), Path(sys.argv[2])
src = fw_path.read_text(encoding="utf-8")


def once(text: str, old: str, new: str) -> str:
    assert text.count(old) >= 1, f"anchor missing: {old!r}"
    return text.replace(old, new, 1)


FABRIC_TAIL = "\tmilan_write(MILAN_CRF_TX_CTRL, MILAN_CRF_TX_CTRL_BOOT);"
UART_TAIL = "\tprint_tod(gettime_ns());\n}"
AEM = "static int aem_loaded;"
ADP, PP = "MILAN_ADP_CTRL", "MILAN_PP_CTRL"
RAW = "0x90000600u"


def before_aem(stmt: str) -> str:
    """At the end of configure_fabric(), after the pre-AEM clears."""
    return once(src, FABRIC_TAIL, FABRIC_TAIL + "\n\t" + stmt)


def in_uart(stmt: str, text: str = src) -> str:
    """At the end of the first UART command handler."""
    return once(text, UART_TAIL, stmt + "\n" + UART_TAIL)


def with_define(text: str, define: str) -> str:
    return once(text, AEM, define + "\n\n" + AEM)


accepted = [
    ("ACC1 an #ifdef around a debug printf INSIDE milan_init()",
     once(src, "\tentity_advertise(aem_loaded);\n}",
          "\tentity_advertise(aem_loaded);\n#ifdef MILAN_DEBUG_BOOT\n"
          "\tprintf(\"boot: advertise decided\\n\");\n#endif\n}")),
    ("ACC2 a benign statement in an arm the census tree drops, inside "
     "configure_fabric()",
     before_aem("#ifndef MILAN_CENSUS_SOC\n\tcdelay(1);\n#endif")),
    ("ACC3 an #ifdef/#else choosing a #define, read in a UART command handler",
     once(with_define(src, "#ifdef MILAN_DEBUG_BOOT\n#define MILAN_BOOT_TRACE 1\n"
                      "#else\n#define MILAN_BOOT_TRACE 0\n#endif"),
          UART_TAIL, "\tif (MILAN_BOOT_TRACE)\n\t\tprintf(\"trace: tod\\n\");\n"
          + UART_TAIL)),
    ("ACC4 a ## token paste building a call outside the boot path",
     once(src, UART_TAIL, "#define MILAN_CAT(a, b) a##b\n"
          "\tMILAN_CAT(print, _tod)(gettime_ns());\n}")),
    ("ACC5 a token-joining backslash-newline inside a macro body",
     with_define(src, "#define MILAN_BOOT_BANNER \"Milan bare\\\n"
                 "metal: fabric entity\"")),
    ("ACC6 a read-only #define accessor over milan_read()",
     with_define(once(src, f"(unsigned long)milan_read({ADP}),",
                      "(unsigned long)MILAN_ADP_STATE(),"),
                 f"#define MILAN_ADP_STATE() milan_read({ADP})")),
    ("ACC7 a fifth cast to a pointer, resolving outside the window",
     once(before_aem("*(volatile unsigned int *)&milan_scratch = 1u;"), AEM,
          "static volatile uint32_t milan_scratch;\n\n" + AEM)),
    ("ACC8 a fifth store through a pointer, resolving outside the window",
     once(before_aem("milan_poke(&milan_shadow);"),
          "static void configure_fabric(void)",
          "static uint32_t milan_shadow;\n\n"
          "static void milan_poke(volatile uint32_t *reg)\n{\n\t*reg = 1u;\n}"
          "\n\nstatic void configure_fabric(void)")),
    ("ACC10 a fifth inline-asm statement, a fence in a UART command handler",
     in_uart("\t__asm__ volatile(\"fence rw, rw\" ::: \"memory\");")),
]
# ACC9: parse_u64() and seconds_to_ns() exchanged (the gate's own
# swapped_definitions() anchors).
first, second, after = ("static int parse_u64(const char *text",
                        "static int seconds_to_ns(uint64_t seconds",
                        "/*\n * ---- Saved state:")
at, then, ends = (src.index(a) for a in (first, second, after))
assert at < then < ends
accepted.insert(8, ("ACC9 parse_u64() and seconds_to_ns() exchanged, with "
                    "nothing added or removed",
                    src[:at] + src[then:ends] + src[at:then] + src[ends:]))

CAT = "#define MILAN_CAT(a, b) a##b"
VERDICT_TEST = "\tif (!verified)\n\t\treturn;"
VERIFIER_ELSE = ("\treturn 1;\n#else\n\tprintf(\"Milan baremetal: no QSPI AEM "
                 "slot; entity disabled.\\n\");\n\treturn 0;\n#endif\n}")
hostile = [
    # splice / paste outside the six compared bodies, against text rules the
    # resolver must still back
    ("H1 function pointer to milan_write built by a SPLICE, called from a "
     "UART handler",
     in_uart("\t{\n\t\tvoid (*fp)(unsigned int, uint32_t) = milan_\\\nwrite;\n"
             f"\t\tfp({ADP}, 1u);\n\t}}")),
    ("H2 function pointer to milan_write built by a PASTE, called from a "
     "UART handler",
     with_define(in_uart("\t{\n\t\tvoid (*fp)(unsigned int, uint32_t) = "
                         f"MILAN_CAT(milan_, write);\n\t\tfp({ADP}, 1u);\n\t}}"),
                 CAT)),
    ("H3 second choke-point call built by a SPLICE, in a UART handler",
     in_uart("\tentity_\\\nadvertise(1);")),
    ("H4 verdict overwritten by a PASTE between the verifier and the choke "
     "point",
     with_define(once(src, "\taem_loaded = load_aem_image();\n",
                      "\taem_loaded = load_aem_image();\n"
                      "\tMILAN_CAT(aem_, loaded) = 1;\n"), CAT)),
    ("H5 verdict overwritten by a SPLICE between the verifier and the choke "
     "point",
     once(src, "\taem_loaded = load_aem_image();\n",
          "\taem_loaded = load_aem_image();\n\taem_\\\nloaded = 1;\n")),
    ("H11 store through milan_reg() built by a PASTE, in a UART handler",
     with_define(in_uart(f"\t*MILAN_CAT(milan_, reg)({ADP}) = 1u;"), CAT)),
    # macro-body narrowing: a read hidden in the identity magic
    ("H6 second #define of MILAN_ID_MAGIC as a fresh milan_read(MILAN_ID)",
     once(src, "#define MILAN_ID_MAGIC       0x4d494c4eu\n",
          "#define MILAN_ID_MAGIC       0x4d494c4eu\n"
          "#define MILAN_ID_MAGIC (milan_read(MILAN_ID))\n")),
    ("H7 second #define of MILAN_ID_MAGIC as the sample itself (control)",
     once(src, "#define MILAN_ID_MAGIC       0x4d494c4eu\n",
          "#define MILAN_ID_MAGIC       0x4d494c4eu\n"
          "#define MILAN_ID_MAGIC id\n")),
    # the verifier group the per-selection grading leaves as written
    ("H8 verifier QSPI-slot group with its #else arm deleted (the no-slot "
     "build falls off the end of load_aem_image())",
     once(src, VERIFIER_ELSE, "\treturn 1;\n#endif\n}")),
    ("H9 verifier #else behind a lone CR, its hidden arm returning 1",
     once(src, VERIFIER_ELSE, "\treturn 1;\r#else\r\treturn 1;\n#endif\n}")),
    # product-only conditionals
    ("H10 product-only 0 && in the choke point's verdict test (the gate's own "
     "control, graded here in both environments)",
     once(src, VERDICT_TEST,
          "\tif (\n#ifdef CSR_UART_BASE\n\t    0 &&\n#endif\n\t    !verified)"
          "\n\t\treturn;")),
    ("H12 the same product-only 0 && with its directives behind lone CRs",
     once(src, VERDICT_TEST,
          "\tif (\r#ifdef CSR_UART_BASE\r0 &&\r#endif\r!verified)\n\t\treturn;")),
    ("H13 the same product-only 0 && with its directives behind form feeds",
     once(src, VERDICT_TEST,
          "\tif (\n\f#ifdef CSR_UART_BASE\n\t    0 &&\n\f#endif\n\t    "
          "!verified)\n\t\treturn;")),
    ("H14 a product-only arm clearing nothing: pre-AEM ADP clear behind a "
     "lone-CR #ifndef (census keeps it, product drops it)",
     once(src, f"\tmilan_write({ADP}, milan_read({ADP}) & ~1u);\n",
          f"\r#ifndef CSR_UART_BASE\r\tmilan_write({ADP}, milan_read({ADP}) & ~1u);"
          "\r#endif\n")),
]

out.mkdir(parents=True, exist_ok=True)
for name, cases in (("accepted", accepted), ("hostile", hostile)):
    (out / f"{name}.json").write_text(json.dumps(
        [{"label": label, "firmware": text} for label, text in cases],
        indent=1) + "\n")
# the directory accepted case: base's `listing` is what the directory pin
# compares against the pinned directory; head's is what is planted.
(out / "listing_base.json").write_text(json.dumps(
    [{"label": "ACC11 a README and a notes.txt beside the firmware",
      "firmware": src, "listing": ["README", "notes.txt"]}], indent=1) + "\n")
(out / "listing_head.json").write_text(json.dumps(
    [{"label": "ACC11 a README and a notes.txt beside the firmware",
      "firmware": src, "listing": ["README", "notes.txt"]},
     {"label": "H15 a LINK named init.h beside the firmware to a file outside",
      "firmware": src, "listing": ["LINK:init.h"]}], indent=1) + "\n")
print(f"{len(accepted)} accepted, {len(hostile)} hostile cases -> {out}")
