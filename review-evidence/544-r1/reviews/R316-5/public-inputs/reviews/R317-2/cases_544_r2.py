"""Reviewer case set for issue #544 round 2 (R317-2). build(fw) -> [(label, firmware)].

New near misses against the two delimited exceptions of decision 5824093785,
whole-unit escape spellings, compiler-free bounds and limit explorations.
Label prefixes (the expectation, not the result):
  EXC-OK  an authorized exception shape; expected ACCEPTED
  NEAR    a near miss of an exception; expected REFUSED (macro form reaches the
          compiled rule past the source-text rule)
  ESC     address-taking outside the interval; expected REFUSED with a compiler
  BOUND   a declared compiler-free bound; expected ACCEPTED without a compiler
          and REFUSED with one
  LIM     exploration of the design boundary; result recorded, no expectation
"""

READ = "\tuint32_t id = milan_read(MILAN_ID);\n"
GUARD = "\tif (id != MILAN_ID_MAGIC) {"
GUARD_END = ("\t\tprintf(\"Milan baremetal: CSR identity mismatch; fabric "
             "remains disabled.\\n\");\n\t\treturn;\n\t}\n")
STATIC = "static int aem_loaded;"
INIT = "static void milan_init(void)\n{"
MAGIC_DEF = "#define MILAN_ID_MAGIC       0x4d494c4eu"


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


def define(fw, definitions):
    return once(fw, STATIC, definitions + "\n\n" + STATIC)


def before_guard(fw, statement):
    return once(fw, GUARD, "\t" + statement + "\n" + GUARD)


def after_guard(fw, statement):
    return once(fw, GUARD_END, GUARD_END + "\t" + statement + "\n")


def forge(fw, replacement, call="MILAN_FORGE(id);", params="x"):
    return before_guard(define(fw, f"#define MILAN_FORGE({params}) {replacement}"),
                        call)


def build(fw):
    assert fw.count(READ) == 1 and fw.count(GUARD) == 1 and fw.count(INIT) == 1
    assert fw.count(GUARD_END) == 1 and fw.count(MAGIC_DEF) == 1
    cases = [
        ("CTRL unchanged firmware", fw),
        # ---- authorized shapes, other spellings -------------------------
        ("EXC-OK discarded mask hex literal (void)(id & 0xffu);",
         before_guard(fw, "(void)(id & 0xffu);")),
        ("EXC-OK discarded mask no blanks (void)(id&1);",
         before_guard(fw, "(void)(id&1);")),
        ("EXC-OK discarded mask ull suffix (void)(id & 0x1ull);",
         before_guard(fw, "(void)(id & 0x1ull);")),
        ("EXC-OK discarded mask macro literal (void)(id & MILAN_ID_MAGIC);",
         before_guard(fw, "(void)(id & MILAN_ID_MAGIC);")),
        ("EXC-OK second diagnostic call argument",
         before_guard(fw, 'printf("%lu\\n", (unsigned long)id);')),
        ("EXC-OK two sample arguments in one call",
         before_guard(fw, 'printf("%lu %lu\\n", (unsigned long)id, (unsigned long)id);')),
        # ---- near misses of the argument shape (macro form) --------------
        ("NEAR argument followed by + 1u",
         forge(fw, 'printf("%lu", (unsigned long)x + 1u)')),
        ("NEAR argument followed by conditional",
         forge(fw, 'printf("%lu", (unsigned long)x ? 1ul : 0ul)')),
        ("NEAR argument extra parentheses (unsigned long)(x)",
         forge(fw, 'printf("%lu", (unsigned long)(x))')),
        ("NEAR argument then comma assignment in a second statement expr",
         forge(fw, 'printf("%lu", (unsigned long)x), x = MILAN_ID_MAGIC')),
        ("NEAR argument postfix increment",
         forge(fw, 'printf("%lu", (unsigned long)x++)')),
        ("NEAR argument cast unsigned long int",
         forge(fw, 'printf("%lu", (unsigned long int)x)')),
        ("NEAR argument cast unsigned int",
         forge(fw, 'printf("%u", (unsigned int)x)')),
        ("NEAR argument via parenthesized callee (printf)(...)",
         forge(fw, '(printf)("%lu", (unsigned long)x)')),
        ("NEAR argument in statement expression that assigns",
         forge(fw, 'printf("%lu", ({ x = MILAN_ID_MAGIC; (unsigned long)x; }))')),
        ("NEAR argument in sizeof",
         forge(fw, '(void)sizeof((unsigned long)x, 0)')),
        ("NEAR argument in array subscript",
         forge(fw, '(void)"ab"[(unsigned long)x & 1ul]')),
        ("NEAR argument of __typeof__ declaration then assignment",
         forge(fw, '__typeof__((unsigned long)x) milan_t = 0; (void)milan_t; x = 1u')),
        # ---- near misses of the statement shape (macro form) -------------
        ("NEAR statement two masks (void)(x & 1u & 3u)",
         forge(fw, "(void)(x & 1u & 3u)")),
        ("NEAR statement negative literal (void)(x & -1)",
         forge(fw, "(void)(x & -1)")),
        ("NEAR statement char literal (void)(x & '\\1')",
         forge(fw, "(void)(x & '\\1')")),
        ("NEAR statement under if (1)",
         forge(fw, "if (1) (void)(x & 1u)")),
        ("NEAR statement followed by & 2u",
         forge(fw, "(void)(x & 1u) & 2u")),
        ("NEAR statement mask operand reversed (void)(1u & x)",
         forge(fw, "(void)(1u & x)")),
        ("NEAR statement mask then pre-increment in next statement",
         forge(fw, "(void)(x & 1u); ++x")),
        ("NEAR statement mask in comma with assignment",
         forge(fw, "(void)(x & 1u), (x = MILAN_ID_MAGIC)")),
        # ---- hostile printf macros reshaping the production diagnostic ---
        ("NEAR printf macro routes the argument into a conditional",
         define(fw, "#define printf(...) MILAN_DIAG(__VA_ARGS__, 0u, 0u)\n"
                    "#define MILAN_DIAG(f, a, ...) (printf)(f, 0 ? a : a, __VA_ARGS__)")),
        ("NEAR printf macro keeps a delimited argument and reuses it wrapped",
         define(fw, "int milan_hook(const char *, ...);\n"
                    "#define printf(...) MILAN_DIAG(__VA_ARGS__, 0u, 0u)\n"
                    "#define MILAN_DIAG(f, a, ...) "
                    "(milan_hook(f, a, __VA_ARGS__) + (int)(a))")),
        ("LIM printf macro forwards the argument to a benign identifier call",
         define(fw, "int milan_hook(const char *, ...);\n"
                    "#define printf(...) milan_hook(__VA_ARGS__)")),
        # ---- escape anywhere in the unit (after the guard) ---------------
        ("ESC sizeof &id after guard", after_guard(fw, "(void)sizeof(&id);")),
        ("ESC __typeof__(&id) after guard",
         after_guard(fw, "{ __typeof__(&id) milan_p = 0; (void)milan_p; }")),
        ("ESC asm m input after guard",
         after_guard(fw, '__asm__ volatile ("" :: "m"(id));')),
        ("ESC asm +m output after guard",
         after_guard(fw, '__asm__ volatile ("" : "+m"(id));')),
        ("ESC pointer initialised from &id after guard",
         after_guard(fw, "{ uint32_t *milan_p = &id; (void)milan_p; }")),
        ("ESC &id + 0 after guard", after_guard(fw, "(void)(&id + 0);")),
        ("ESC macro &(x) after guard",
         after_guard(define(fw, "#define MILAN_ADDR(x) ((void)&(x))"),
                     "MILAN_ADDR(id);")),
        ("LIM asm +r output after guard (no address, after the interval)",
         after_guard(fw, '__asm__ volatile ("" : "+r"(id));')),
        # ---- declared compiler-free bounds -------------------------------
        ("BOUND C03 header paste",
         before_guard(fw, "__CONCAT(i, d) = MILAN_ID_MAGIC;")),
        ("BOUND C05 macro using header paste",
         before_guard(define(fw, "#define MILAN_FORGE2(a) __CONCAT(a, d) = MILAN_ID_MAGIC"),
                      "MILAN_FORGE2(i);")),
        ("BOUND C13 object-like macro alias",
         before_guard(define(fw, "#define MILAN_FORGE(x) ((x) = MILAN_ID_MAGIC)\n"
                                 "#define MILAN_ALIAS MILAN_FORGE"), "MILAN_ALIAS(id);")),
        ("BOUND writer alias",
         before_guard(define(fw, "#define MILAN_SET(y) y = MILAN_ID_MAGIC\n"
                                 "#define MILAN_FORGE MILAN_SET"), "MILAN_FORGE(id);")),
        ("BOUND writer apply",
         before_guard(define(fw, "#define MILAN_SET(y) y = MILAN_ID_MAGIC\n"
                                 "#define MILAN_APPLY(f) f"), "MILAN_APPLY(MILAN_SET)(id);")),
        ("BOUND C16 parenthesized assignment", before_guard(fw, "(id) = MILAN_ID_MAGIC;")),
        ("BOUND C17 indirect assignment", before_guard(fw, "*&(id) = MILAN_ID_MAGIC;")),
        # ---- design-boundary explorations --------------------------------
        ("LIM callee asm clobbers a callee-saved register, called in interval",
         before_guard(once(fw, INIT,
                           "static void __attribute__((noinline)) milan_clobber(void)\n"
                           "{\n\t__asm__ volatile(\"li s1, 0x4d494c4e\");\n}\n\n" + INIT),
                      "milan_clobber();")),
        ("LIM frame-address store in interval",
         before_guard(fw, "*((volatile uint32_t *)__builtin_frame_address(0) - 5) = MILAN_ID_MAGIC;")),
        ("LIM backward goto writes after the guard",
         after_guard(before_guard(fw, "goto milan_skip; milan_again:"),
                     "if (0) { milan_skip: id = MILAN_ID_MAGIC; goto milan_again; }")),
        ("LIM backward goto hidden in macros",
         after_guard(before_guard(define(fw, "#define MILAN_J(l) goto l\n"
                                             "#define MILAN_W(x) x = MILAN_ID_MAGIC"),
                                  "MILAN_J(milan_skip); milan_again:"),
                     "if (0) { milan_skip: MILAN_W(id); MILAN_J(milan_again); }")),
        ("LIM magic definition assigns the sample",
         once(fw, MAGIC_DEF, "#define MILAN_ID_MAGIC       (id = 0x4d494c4eu)")),
        ("LIM forged system-header linemarker before a nested capture",
         after_guard(once(fw, INIT, '# 1 "/usr/include/milan-forged.h" 3\n' + INIT),
                     "void milan_nested(void) { id = MILAN_ID_MAGIC; } milan_nested();")),
    ]
    return cases
