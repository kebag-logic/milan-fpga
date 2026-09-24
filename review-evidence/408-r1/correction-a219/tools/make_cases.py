#!/usr/bin/env python3
"""Every hostile firmware and accepted case R272-1 and R273-1 graded, rebuilt
verbatim from their published case scripts (review-evidence/408-r1/reviews/
R272-1/scripts/cases_r{1,2,3,4}.py and R273-1/scripts/make_{,more_}cases.py)
over the tracked firmware, which is byte-identical at base 759da623 and at
every head of this lane. Labels keep each reviewer's own case id.

Usage: make_cases.py <out-dir>   (writes hostile.json, accepted.json)
"""

import json
import sys
from pathlib import Path

LANE = Path("$LANES/408-409-boot-gate-retire")
src = (LANE / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text(
    encoding="utf-8")
out = Path(sys.argv[1])

CSR_BASE, ADP, ADP_NAME = 0x9000_0000, 0x600, "MILAN_ADP_CTRL"
RAW = f"0x{CSR_BASE + ADP:08x}u"
UART_TAIL = "\tprint_tod(gettime_ns());\n}"
VERDICT = "\tif (!verified)\n\t\treturn;"
EID = "#define MILAN_ADP_EID_LO     0x604u\n"
STATIC = "static int aem_loaded;"
GUARD = "\tif (id != MILAN_ID_MAGIC) {"
FABRIC_TAIL = "\tmilan_write(MILAN_CRF_TX_CTRL, MILAN_CRF_TX_CTRL_BOOT);"


def first(text, old, new):
    assert old in text, f"anchor not found: {old!r}"
    return text.replace(old, new, 1)


hostile = []


def add(label, firmware, listing=None):
    hostile.append({"label": label, "firmware": firmware,
                    **({"listing": listing} if listing else {})})


# ---- R272-1 round 1 ---------------------------------------------------
page = f"static unsigned int csr_page = 0x{CSR_BASE >> 16:04x}u;\n\n"
for tag, lead in (("plain #", ""), ("form feed", "\f"),
                  ("vertical tab", "\v")):
    add(f"R272 r1 {tag}: product-only `0 &&` in the choke point verdict test",
        first(src, VERDICT, f"\tif (\n{lead}#ifdef CSR_UART_BASE\n\t    0 &&\n"
              f"{lead}#endif\n\t    !verified)\n\t\treturn;"))
for tag, lead in (("plain #", ""), ("form feed", "\f")):
    add(f"R272 r1 {tag}: product-only paged-base cast store to ADP_CTRL in a "
        "UART handler",
        first(first(src, STATIC, page + STATIC), UART_TAIL,
              f"{lead}#ifdef CSR_UART_BASE\n\t*(volatile unsigned int *)"
              f"((csr_page << 16) | {ADP_NAME}) = 1u;\n{lead}#endif\n"
              + UART_TAIL))
    add(f"R272 r1 {tag}: product-only literal-address cast store to ADP_CTRL "
        "in a UART handler",
        first(src, UART_TAIL, f"{lead}#ifdef CSR_UART_BASE\n\t*(volatile "
              f"unsigned int *){RAW} = 1u;\n{lead}#endif\n" + UART_TAIL))
    add(f"R272 r1 {tag}: product-only lui asm store to ADP_CTRL in a UART "
        "handler",
        first(src, UART_TAIL,
              f"{lead}#ifdef CSR_UART_BASE\n\t__asm__ volatile("
              f'"lui t0, 0x{CSR_BASE >> 12:05x}\\n\\t"\n'
              '\t                 "li t1, 1\\n\\t"\n'
              f'\t                 "sw t1, 0x{ADP:x}(t0)"\n'
              '\t                 ::: "t0", "t1", "memory");\n'
              f"{lead}#endif\n" + UART_TAIL))
    add(f"R272 r1 {tag}: product-only arm moving ADP_EID_LO onto ADP_CTRL "
        "(product arm first)",
        first(src, EID, f"{lead}#ifdef CSR_UART_BASE\n#define MILAN_ADP_EID_LO"
              f"     0x{ADP:03x}u\n{lead}#else\n{EID}{lead}#endif\n"))
    add(f"R272 r1 {tag}: product-only arm moving ADP_EID_LO onto ADP_CTRL "
        "(product arm last)",
        first(src, EID, f"{lead}#ifndef CSR_UART_BASE\n{EID}{lead}#else\n"
              f"#define MILAN_ADP_EID_LO     0x{ADP:03x}u\n{lead}#endif\n"))

# ---- R272-1 round 2 ---------------------------------------------------
store = f"\t*(volatile unsigned int *){RAW} = 1u;\n"
add("R272 r2 control: form feed arm around a SPELLED milan_write enable in a "
    "UART handler",
    first(src, UART_TAIL, f"\f#ifdef CSR_UART_BASE\n\tmilan_write({ADP_NAME}, "
          f"milan_read({ADP_NAME}) | 1u);\n\f#endif\n" + UART_TAIL))
add("R272 r2 NUL byte before #: product-only literal-address cast store in a "
    "UART handler",
    first(src, UART_TAIL, f"\0#ifdef CSR_UART_BASE\n{store}\0#endif\n"
          + UART_TAIL))
add("R272 r2 unterminated-quote defines around a product-only literal-address "
    "cast store in a UART handler",
    first(src, UART_TAIL, "#define MILAN_Q '\n#ifdef CSR_UART_BASE\n" + store
          + "#endif\n#define MILAN_R '\n" + UART_TAIL))
add("R272 r2 unterminated-quote defines around a product-only `0 &&` in the "
    "choke point verdict test",
    first(src, VERDICT, "#define MILAN_Q '\n\tif (\n#ifdef CSR_UART_BASE\n\t "
          "   0 &&\n#endif\n#define MILAN_R '\n\t    !verified)\n\t\treturn;"))
add("R272 r2 form feed: product-only literal-address cast store inside "
    "configure_fabric() (a boot-path body)",
    first(src, FABRIC_TAIL + "\n}", FABRIC_TAIL + "\n"
          f"\f#ifdef CSR_UART_BASE\n{store}\f#endif\n}}"))

# ---- R272-1 round 3 ---------------------------------------------------
add("R272 r3 identity forged through a plain function-like macro",
    first(first(src, STATIC, "#define MILAN_FORGE(x) x = MILAN_ID_MAGIC\n\n"
                + STATIC), GUARD, "\tMILAN_FORGE(id);\n" + GUARD))
add("R272 r3 identity forged through a token-joining splice of the local's "
    "name", first(src, GUARD, "\ti\\\nd = MILAN_ID_MAGIC;\n" + GUARD))
add("R272 r3 identity forged through a ## paste of the local's name",
    first(first(src, STATIC, "#define MILAN_CAT(a, b) a##b\n\n" + STATIC),
          GUARD, "\tMILAN_CAT(i, d) = MILAN_ID_MAGIC;\n" + GUARD))
typedef = "typedef struct { volatile uint32_t ctrl; } *milan_arm_blk;\n\n"
for tag, lead in (("plain #", ""), ("form feed", "\f")):
    add(f"R272 r3 {tag}: product-only struct-overlay store to ADP_CTRL in a "
        "UART handler",
        first(first(src, STATIC, typedef + STATIC), UART_TAIL,
              f"{lead}#ifdef CSR_UART_BASE\n\t((milan_arm_blk){RAW})->ctrl = "
              f"1u;\n{lead}#endif\n" + UART_TAIL))

# ---- R273-1 hostile H1-H15 and V1-V4 ---------------------------------
AEM = "static int aem_loaded;"
CAT = "#define MILAN_CAT(a, b) a##b"
VERIFIER_ELSE = ("\treturn 1;\n#else\n\tprintf(\"Milan baremetal: no QSPI AEM "
                 "slot; entity disabled.\\n\");\n\treturn 0;\n#endif\n}")


def in_uart(stmt, text=src):
    return first(text, UART_TAIL, stmt + "\n" + UART_TAIL)


def with_define(text, define):
    return first(text, AEM, define + "\n\n" + AEM)


add("R273 H1 function pointer to milan_write built by a SPLICE, called from "
    "a UART handler",
    in_uart("\t{\n\t\tvoid (*fp)(unsigned int, uint32_t) = milan_\\\nwrite;\n"
            f"\t\tfp({ADP_NAME}, 1u);\n\t}}"))
add("R273 H2 function pointer to milan_write built by a PASTE, called from a "
    "UART handler",
    with_define(in_uart("\t{\n\t\tvoid (*fp)(unsigned int, uint32_t) = "
                        f"MILAN_CAT(milan_, write);\n\t\tfp({ADP_NAME}, 1u);"
                        "\n\t}"), CAT))
add("R273 H3 second choke-point call built by a SPLICE, in a UART handler",
    in_uart("\tentity_\\\nadvertise(1);"))
add("R273 H4 verdict overwritten by a PASTE between the verifier and the "
    "choke point",
    with_define(first(src, "\taem_loaded = load_aem_image();\n",
                      "\taem_loaded = load_aem_image();\n"
                      "\tMILAN_CAT(aem_, loaded) = 1;\n"), CAT))
add("R273 H5 verdict overwritten by a SPLICE between the verifier and the "
    "choke point",
    first(src, "\taem_loaded = load_aem_image();\n",
          "\taem_loaded = load_aem_image();\n\taem_\\\nloaded = 1;\n"))
add("R273 H11 store through milan_reg() built by a PASTE, in a UART handler",
    with_define(in_uart(f"\t*MILAN_CAT(milan_, reg)({ADP_NAME}) = 1u;"), CAT))
add("R273 H6 second #define of MILAN_ID_MAGIC as a fresh milan_read(MILAN_ID)",
    first(src, "#define MILAN_ID_MAGIC       0x4d494c4eu\n",
          "#define MILAN_ID_MAGIC       0x4d494c4eu\n"
          "#define MILAN_ID_MAGIC (milan_read(MILAN_ID))\n"))
add("R273 H7 second #define of MILAN_ID_MAGIC as the sample itself",
    first(src, "#define MILAN_ID_MAGIC       0x4d494c4eu\n",
          "#define MILAN_ID_MAGIC       0x4d494c4eu\n"
          "#define MILAN_ID_MAGIC id\n"))
add("R273 H8 verifier QSPI-slot group with its #else arm deleted",
    first(src, VERIFIER_ELSE, "\treturn 1;\n#endif\n}"))
add("R273 H9 verifier #else behind a lone CR, its hidden arm returning 1",
    first(src, VERIFIER_ELSE, "\treturn 1;\r#else\r\treturn 1;\n#endif\n}"))
add("R273 H10 product-only 0 && in the choke point's verdict test",
    first(src, VERDICT, "\tif (\n#ifdef CSR_UART_BASE\n\t    0 &&\n#endif\n"
          "\t    !verified)\n\t\treturn;"))
add("R273 H12 the same product-only 0 && with its directives behind lone CRs",
    first(src, VERDICT, "\tif (\r#ifdef CSR_UART_BASE\r0 &&\r#endif\r!verified)"
          "\n\t\treturn;"))
add("R273 H13 the same product-only 0 && with its directives behind form "
    "feeds",
    first(src, VERDICT, "\tif (\n\f#ifdef CSR_UART_BASE\n\t    0 &&\n\f#endif"
          "\n\t    !verified)\n\t\treturn;"))
add("R273 H14 pre-AEM ADP clear behind a lone-CR #ifndef (census keeps it, "
    "product drops it)",
    first(src, f"\tmilan_write({ADP_NAME}, milan_read({ADP_NAME}) & ~1u);\n",
          f"\r#ifndef CSR_UART_BASE\r\tmilan_write({ADP_NAME}, "
          f"milan_read({ADP_NAME}) & ~1u);\r#endif\n"))
add("R273 H15 a LINK named init.h beside the firmware to a file outside",
    src, ["LINK:init.h"])

CAST = "*(volatile unsigned int *)0x90000600u = 1u;"
LUI = ('__asm__ volatile("lui t0, 0x90000\\n\\t" "li t1, 1\\n\\t" '
       '"sw t1, 0x600(t0)" ::: "t0", "t1", "memory");')


def arm(pre, body):
    return f"{pre}#ifdef CSR_UART_BASE\n\t{body}\n{pre}#endif"


def before_guard(stmt, text=src):
    return first(text, GUARD, "\t" + stmt + "\n" + GUARD)


add("R273 V1a form feed before #: product-only literal-address cast store in "
    "a UART handler", in_uart(arm("\f", CAST)))
add("R273 V1b vertical tab before #: the same store", in_uart(arm("\v", CAST)))
add("R273 V1c NUL before #: the same store", in_uart(arm("\0", CAST)))
add("R273 V1d lone CR before #: the same store",
    in_uart(f"\r#ifdef CSR_UART_BASE\r\t{CAST}\r#endif"))
add("R273 V1e form feed before #: product-only lui/sw asm store",
    in_uart(arm("\f", LUI)))
add("R273 V1f control: plain # product-only literal cast store",
    in_uart(arm("", CAST)))
add("R273 V2a identity local forged by a SPLICE between the read and the "
    "guard", before_guard("i\\\nd = MILAN_ID_MAGIC;"))
add("R273 V2b identity local forged by a PASTE between the read and the "
    "guard",
    before_guard("MILAN_CAT(i, d) = MILAN_ID_MAGIC;",
                 first(src, AEM, "#define MILAN_CAT(a, b) a##b\n\n" + AEM)))
add("R273 V2c identity local forged by a plain function-like macro",
    before_guard("MILAN_FORGE(id);", first(
        src, AEM, "#define MILAN_FORGE(x) ((x) = MILAN_ID_MAGIC)\n\n" + AEM)))
add("R273 V4 unterminated character literals in two #defines bracketing a "
    "product-only literal-address store",
    in_uart("#define MILAN_Q '\n" + arm("", CAST) + "\n#define MILAN_R '"))

# ---- the correlated-conditional shapes (R272 r4, R273 V3a/V3b) --------
accepted = []


def accept(label, firmware, listing=None):
    accepted.append({"label": label, "firmware": firmware,
                     **({"listing": listing} if listing else {})})


helper = ("#ifdef MILAN_DEBUG_TOD\nstatic void milan_debug_tod(void)\n{\n"
          "\tprintf(\"tod: debug\\n\");\n}\n#endif\n\n")
accept("R272 r4 a debug helper defined under #ifdef MILAN_DEBUG_TOD and "
       "called under a second #ifdef MILAN_DEBUG_TOD in a UART handler",
       first(first(src, STATIC, helper + STATIC), UART_TAIL,
             "#ifdef MILAN_DEBUG_TOD\n\tmilan_debug_tod();\n#endif\n"
             + UART_TAIL))
accept("R272 r4 control: the same debug printf in ONE #ifdef in a UART "
       "handler",
       first(src, UART_TAIL, "#ifdef MILAN_DEBUG_TOD\n\tprintf(\"tod: debug"
             "\\n\");\n#endif\n" + UART_TAIL))
accept("R272 r4 a debug-only static counter declared under #ifdef and "
       "incremented under a second #ifdef of the same macro",
       first(first(src, STATIC, "#ifdef MILAN_DEBUG_TOD\nstatic unsigned int "
                   "milan_tod_reads;\n#endif\n\n" + STATIC), UART_TAIL,
             "#ifdef MILAN_DEBUG_TOD\n\tmilan_tod_reads++;\n#endif\n"
             + UART_TAIL))
accept("R273 V3a correlated conditionals: debug helper defined and called "
       "under two #ifdef MILAN_DEBUG_TOD",
       in_uart("#ifdef MILAN_DEBUG_TOD\n\tmilan_debug_tod();\n#endif",
               first(src, AEM, AEM + "\n\n#ifdef MILAN_DEBUG_TOD\nstatic void "
                     "milan_debug_tod(void)\n{\n\tprintf(\"tod\\n\");\n}\n"
                     "#endif")))
accept("R273 V3b correlated conditionals: debug counter declared and "
       "incremented under two #ifdef MILAN_DEBUG_TOD",
       in_uart("#ifdef MILAN_DEBUG_TOD\n\tmilan_tod_count++;\n#endif",
               first(src, AEM, AEM + "\n\n#ifdef MILAN_DEBUG_TOD\nstatic "
                     "unsigned int milan_tod_count;\n#endif")))

# ---- R273-1 accepted ACC1-ACC11 and grader shapes E1-E6 ---------------
ADV = "\tentity_advertise(aem_loaded);\n}"
EN = "milan_write(MILAN_ADP_CTRL, milan_read(MILAN_ADP_CTRL) | 1u);"


def before_aem(stmt):
    return first(src, FABRIC_TAIL, FABRIC_TAIL + "\n\t" + stmt)


accept("R273 ACC1 an #ifdef around a debug printf INSIDE milan_init()",
       first(src, ADV, "\tentity_advertise(aem_loaded);\n#ifdef "
             "MILAN_DEBUG_BOOT\n\tprintf(\"boot: advertise decided\\n\");\n"
             "#endif\n}"))
accept("R273 ACC2 a benign statement in an arm the census tree drops, inside "
       "configure_fabric()",
       before_aem("#ifndef MILAN_CENSUS_SOC\n\tcdelay(1);\n#endif"))
accept("R273 ACC3 an #ifdef/#else choosing a #define, read in a UART command "
       "handler",
       first(with_define(src, "#ifdef MILAN_DEBUG_BOOT\n#define "
                         "MILAN_BOOT_TRACE 1\n#else\n#define MILAN_BOOT_TRACE "
                         "0\n#endif"),
             UART_TAIL, "\tif (MILAN_BOOT_TRACE)\n\t\tprintf(\"trace: tod\\n"
             "\");\n" + UART_TAIL))
accept("R273 ACC4 a ## token paste building a call outside the boot path",
       first(src, UART_TAIL, "#define MILAN_CAT(a, b) a##b\n"
             "\tMILAN_CAT(print, _tod)(gettime_ns());\n}"))
accept("R273 ACC5 a token-joining backslash-newline inside a macro body",
       with_define(src, "#define MILAN_BOOT_BANNER \"Milan bare\\\n"
                   "metal: fabric entity\""))
accept("R273 ACC6 a read-only #define accessor over milan_read()",
       with_define(first(src, f"(unsigned long)milan_read({ADP_NAME}),",
                         "(unsigned long)MILAN_ADP_STATE(),"),
                   f"#define MILAN_ADP_STATE() milan_read({ADP_NAME})"))
accept("R273 ACC7 a fifth cast to a pointer, resolving outside the window",
       first(before_aem("*(volatile unsigned int *)&milan_scratch = 1u;"), AEM,
             "static volatile uint32_t milan_scratch;\n\n" + AEM))
accept("R273 ACC8 a fifth store through a pointer, resolving outside the "
       "window",
       first(before_aem("milan_poke(&milan_shadow);"),
             "static void configure_fabric(void)",
             "static uint32_t milan_shadow;\n\n"
             "static void milan_poke(volatile uint32_t *reg)\n{\n\t*reg = 1u;"
             "\n}\n\nstatic void configure_fabric(void)"))
p, s, e = ("static int parse_u64(const char *text",
           "static int seconds_to_ns(uint64_t seconds", "/*\n * ---- Saved state:")
at, then, ends = (src.index(a) for a in (p, s, e))
accept("R273 ACC9 parse_u64() and seconds_to_ns() exchanged",
       src[:at] + src[then:ends] + src[at:then] + src[ends:])
accept("R273 ACC10 a fifth inline-asm statement, a fence in a UART handler",
       in_uart("\t__asm__ volatile(\"fence rw, rw\" ::: \"memory\");"))
accept("R273 ACC11 a README and a notes.txt beside the firmware", src,
       ["README", "notes.txt"])
TAIL = FABRIC_TAIL


def at_tail(s):
    return first(src, TAIL, TAIL + "\n" + s)


accept("R273 E1 #if/#elif/#else debug printfs after the choke-point call",
       first(src, ADV, "\tentity_advertise(aem_loaded);\n#if defined(MILAN_A)"
             "\n\tprintf(\"a\\n\");\n#elif defined(MILAN_B)\n\tprintf(\"b\\n\""
             ");\n#else\n\tprintf(\"c\\n\");\n#endif\n}"))
add("R273 E2 an #elif arm only the product takes enabling ADP before AEM",
    at_tail("#if defined(MILAN_A)\n\tcdelay(1);\n#elif defined(CSR_UART_BASE)"
            "\n\t" + EN + "\n#endif"))
add("R273 E3 nested groups, the inner arm enabling ADP before AEM",
    at_tail("#ifdef MILAN_A\n#ifdef CSR_UART_BASE\n\t" + EN + "\n#endif\n"
            "#endif"))
accept("R273 E4 #if 0 around a benign statement",
       at_tail("#if 0\n\tcdelay(1);\n#endif"))
add("R273 E5 #if 0 around an enable before AEM",
    at_tail("#if 0\n\t" + EN + "\n#endif"))
accept("R273 E6 four independent groups (16 selections, at the bound)",
       first(src, STATIC, "".join(
           f"#ifdef MILAN_DEBUG_{k}\n#define MILAN_TRACE_{k} 1\n#endif\n"
           for k in range(4)) + "\n" + STATIC))

out.mkdir(parents=True, exist_ok=True)
for name, cases in (("hostile", hostile), ("accepted", accepted)):
    (out / f"{name}.json").write_text(json.dumps(cases, indent=1) + "\n")
print(f"{len(hostile)} hostile, {len(accepted)} accepted -> {out}")
