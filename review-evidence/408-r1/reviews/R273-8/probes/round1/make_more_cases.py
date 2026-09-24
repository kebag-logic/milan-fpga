#!/usr/bin/env python3
"""Build the grader-shape cases and the cases that re-measure another
review's findings, from the shipping firmware text (identical at dev
759da623 and at head a13b6e2e).

Usage: make_more_cases.py <firmware.c> <out-dir>
Writes grader.json (E1-E6) and verify_r272.json (V1a-V4).
"""

import json
from pathlib import Path
import sys

src = Path(sys.argv[1]).read_text(encoding="utf-8")
out = Path(sys.argv[2])

# ---- grader shapes: #elif, nesting, #if 0 and the 16-selection bound ----
TAIL = "\tmilan_write(MILAN_CRF_TX_CTRL, MILAN_CRF_TX_CTRL_BOOT);"
ADV = "\tentity_advertise(aem_loaded);\n}"
EN = "milan_write(MILAN_ADP_CTRL, milan_read(MILAN_ADP_CTRL) | 1u);"


def at_tail(s):
    return src.replace(TAIL, TAIL + "\n" + s, 1)


grader = [
    ("E1 #if/#elif/#else debug printfs after the choke-point call (three "
     "selections, benign)",
     src.replace(ADV, "\tentity_advertise(aem_loaded);\n#if defined(MILAN_A)\n"
                 "\tprintf(\"a\\n\");\n#elif defined(MILAN_B)\n\tprintf(\"b\\n\");"
                 "\n#else\n\tprintf(\"c\\n\");\n#endif\n}", 1)),
    ("E2 an #elif arm only the product takes enabling ADP before AEM",
     at_tail("#if defined(MILAN_A)\n\tcdelay(1);\n#elif defined(CSR_UART_BASE)"
             "\n\t" + EN + "\n#endif")),
    ("E3 nested groups, the inner arm enabling ADP before AEM",
     at_tail("#ifdef MILAN_A\n#ifdef CSR_UART_BASE\n\t" + EN + "\n#endif\n#endif")),
    ("E4 #if 0 around a benign statement (graded as code, benign)",
     at_tail("#if 0\n\tcdelay(1);\n#endif")),
    ("E5 #if 0 around an enable before AEM (graded as the code it would be)",
     at_tail("#if 0\n\t" + EN + "\n#endif")),
    ("E6 four independent groups (16 selections, at the bound, benign)",
     src.replace("static int aem_loaded;", "".join(
         f"#ifdef MILAN_DEBUG_{k}\n#define MILAN_TRACE_{k} 1\n#endif\n"
         for k in range(4)) + "\nstatic int aem_loaded;", 1)),
]

# ---- another review's findings, re-measured ----------------------------
UART_TAIL = "\tprint_tod(gettime_ns());\n}"
AEM = "static int aem_loaded;"
CAST = "*(volatile unsigned int *)0x90000600u = 1u;"
LUI = ('__asm__ volatile("lui t0, 0x90000\\n\\t" "li t1, 1\\n\\t" '
       '"sw t1, 0x600(t0)" ::: "t0", "t1", "memory");')
GUARD = "\tif (id != MILAN_ID_MAGIC) {"


def uart(stmt, text=src):
    assert UART_TAIL in text
    return text.replace(UART_TAIL, stmt + "\n" + UART_TAIL, 1)


def arm(pre, body):
    return f"{pre}#ifdef CSR_UART_BASE\n\t{body}\n{pre}#endif"


def before_guard(stmt, text=src):
    assert GUARD in text
    return text.replace(GUARD, "\t" + stmt + "\n" + GUARD, 1)


verify = [
    ("V1a form feed before #: product-only arm with a literal-address cast "
     "store in a UART handler", uart(arm("\f", CAST))),
    ("V1b vertical tab before #: the same store", uart(arm("\v", CAST))),
    ("V1c NUL before #: the same store", uart(arm("\0", CAST))),
    ("V1d lone CR before #: the same store",
     uart(f"\r#ifdef CSR_UART_BASE\r\t{CAST}\r#endif")),
    ("V1e form feed before #: product-only arm with a lui/sw asm store",
     uart(arm("\f", LUI))),
    ("V1f control: plain # product-only arm with the literal cast store",
     uart(arm("", CAST))),
    ("V2a identity local forged by a SPLICE between the read and the guard",
     before_guard("i\\\nd = MILAN_ID_MAGIC;")),
    ("V2b identity local forged by a PASTE between the read and the guard",
     before_guard("MILAN_CAT(i, d) = MILAN_ID_MAGIC;",
                  src.replace(AEM, "#define MILAN_CAT(a, b) a##b\n\n" + AEM, 1))),
    ("V2c identity local forged by a plain function-like macro (pre-existing "
     "control)",
     before_guard("MILAN_FORGE(id);", src.replace(
         AEM, "#define MILAN_FORGE(x) ((x) = MILAN_ID_MAGIC)\n\n" + AEM, 1))),
    ("V3a correlated conditionals: debug helper defined and called under two "
     "#ifdef MILAN_DEBUG_TOD",
     uart("#ifdef MILAN_DEBUG_TOD\n\tmilan_debug_tod();\n#endif",
          src.replace(AEM, AEM + "\n\n#ifdef MILAN_DEBUG_TOD\nstatic void "
                      "milan_debug_tod(void)\n{\n\tprintf(\"tod\\n\");\n}\n"
                      "#endif", 1))),
    ("V3b correlated conditionals: debug counter declared and incremented "
     "under two #ifdef MILAN_DEBUG_TOD",
     uart("#ifdef MILAN_DEBUG_TOD\n\tmilan_tod_count++;\n#endif",
          src.replace(AEM, AEM + "\n\n#ifdef MILAN_DEBUG_TOD\nstatic unsigned "
                      "int milan_tod_count;\n#endif", 1))),
    ("V4 unterminated character literals in two #defines bracketing a "
     "product-only literal-address store",
     uart("#define MILAN_Q '\n" + arm("", CAST) + "\n#define MILAN_R '")),
]

out.mkdir(parents=True, exist_ok=True)
for name, cases in (("grader", grader), ("verify_r272", verify)):
    (out / f"{name}.json").write_text(json.dumps(
        [{"label": label, "firmware": text} for label, text in cases],
        indent=1) + "\n")
print(f"{len(grader)} grader, {len(verify)} verification cases -> {out}")
