"""Reviewer case set for issue #544 (R317-1). build(fw) -> [(label, firmware)].

Label prefixes: CTRL = published or expected control, HOST = reviewer hostile
variant (should be REFUSED), LEGIT = legitimate edit (should be ACCEPTED),
S3 = R273-S3 reported as-is.
"""

READ = "\tuint32_t id = milan_read(MILAN_ID);\n"
GUARD = "\tif (id != MILAN_ID_MAGIC) {"
GUARD_END = ("\t\tprintf(\"Milan baremetal: CSR identity mismatch; fabric "
             "remains disabled.\\n\");\n\t\treturn;\n\t}\n")
STATIC = "static int aem_loaded;"
ELSE_ARM = ('\treturn 1;\n#else\n\tprintf("Milan baremetal: no QSPI AEM slot; '
            'entity disabled.\\n");\n\treturn 0;\n#endif\n}')


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
    assert fw.count(READ) == 1 and fw.count(GUARD) == 1
    assert fw.count(GUARD_END) == 1 and fw.count(ELSE_ARM) == 1
    cases = [
        ("CTRL unchanged firmware", fw),
        ("CTRL published R272 macro x = MILAN_ID_MAGIC",
         forge(fw, "x = MILAN_ID_MAGIC")),
        ("CTRL published R273 macro ((x) = MILAN_ID_MAGIC)",
         forge(fw, "((x) = MILAN_ID_MAGIC)")),
        ("CTRL plain source assignment",
         before_guard(fw, "id = MILAN_ID_MAGIC;")),
        # token pasting
        ("HOST paste local macro MILAN_CAT(i, d) = MAGIC",
         before_guard(define(fw, "#define MILAN_CAT(a, b) a##b"),
                      "MILAN_CAT(i, d) = MILAN_ID_MAGIC;")),
        ("HOST paste header macro __CONCAT(i, d) = MAGIC",
         before_guard(fw, "__CONCAT(i, d) = MILAN_ID_MAGIC;")),
        ("HOST paste builds writer name MILAN_CAT(MILAN_, W)(id)",
         before_guard(define(fw, "#define MILAN_W(x) x = MILAN_ID_MAGIC\n"
                                 "#define MILAN_CAT(a, b) a##b"),
                      "MILAN_CAT(MILAN_, W)(id);")),
        # address-taking macros and pointer aliases
        ("HOST macro takes address and stores",
         forge(fw, "(*(volatile uint32_t *)&(x) = MILAN_ID_MAGIC)")),
        ("HOST macro sets local pointer alias then stores",
         forge(fw, "do { uint32_t *milan_p = &(x); *milan_p = MILAN_ID_MAGIC; "
                   "} while (0)")),
        ("HOST pointer alias declared before the sample, set by macro",
         before_guard(once(define(fw, "#define MILAN_FORGE(x) (milan_p = &(x))"),
                           READ, "\tuint32_t *milan_p = 0;\n" + READ),
                      "MILAN_FORGE(id); *milan_p = MILAN_ID_MAGIC;")),
        ("HOST file-scope pointer alias set by macro",
         before_guard(define(fw, "static uint32_t *milan_p;\n"
                                 "#define MILAN_FORGE(x) (milan_p = &(x))"),
                      "MILAN_FORGE(id); *milan_p = MILAN_ID_MAGIC;")),
        # nested blocks
        ("HOST macro write in nested block",
         forge(fw, "((x) = MILAN_ID_MAGIC)", call="{ { MILAN_FORGE(id); } }")),
        ("HOST macro write in if-block",
         forge(fw, "((x) = MILAN_ID_MAGIC)", call="if (1) { MILAN_FORGE(id); }")),
        ("HOST plain write in nested block",
         before_guard(fw, "{ { id = MILAN_ID_MAGIC; } }")),
        # GNU lvalue-preserving wrappers
        ("HOST macro __builtin_choose_expr lvalue store",
         forge(fw, "__builtin_choose_expr(1, x, x) = MILAN_ID_MAGIC")),
        ("HOST macro _Generic lvalue store",
         forge(fw, "_Generic(0, default: x) = MILAN_ID_MAGIC")),
        ("HOST macro (__real__ x) store",
         forge(fw, "(__real__ x) = MILAN_ID_MAGIC")),
        ("HOST macro (__extension__ x) store",
         forge(fw, "(__extension__ x) = MILAN_ID_MAGIC")),
        ("HOST macro inline asm output operand",
         forge(fw, '__asm__ volatile ("" : "=r"(x) : "0"(MILAN_ID_MAGIC))')),
        ("HOST plain __builtin_choose_expr lvalue store",
         before_guard(fw, "__builtin_choose_expr(1, id, id) = MILAN_ID_MAGIC;")),
        ("HOST plain inline asm output operand",
         before_guard(fw, '__asm__ volatile ("" : "=r"(id) : "0"(MILAN_ID_MAGIC));')),
        # compiler-free reader shapes
        ("HOST object-like alias of a function-like writer",
         before_guard(define(fw, "#define MILAN_SET(y) y = MILAN_ID_MAGIC\n"
                                 "#define MILAN_FORGE MILAN_SET"),
                      "MILAN_FORGE(id);")),
        ("HOST writer name passed through a macro argument",
         before_guard(define(fw, "#define MILAN_SET(y) y = MILAN_ID_MAGIC\n"
                                 "#define MILAN_APPLY(f) f"),
                      "MILAN_APPLY(MILAN_SET)(id);")),
        ("HOST #define of the sample name between read and guard",
         before_guard(define(fw, "static uint32_t milan_forged = MILAN_ID_MAGIC;"),
                      "\n#define id milan_forged\n")),
        ("HOST string argument with ) before the sample",
         forge(fw, "x = MILAN_ID_MAGIC", params="s, x",
               call='MILAN_FORGE(")", id);')),
        # after the guard: must stay accepted where base accepted it
        ("LEGIT plain write after the guard",
         after_guard(fw, "id = 0u;")),
        ("LEGIT macro write after the guard",
         after_guard(define(fw, "#define MILAN_FORGE(x) ((x) = 0u)"),
                     "MILAN_FORGE(id);")),
        # legitimate reads
        ("LEGIT binary and with a constant on the left",
         before_guard(fw, "(void)(1u & id);")),
        ("LEGIT read through a function-like macro",
         forge(fw, "((x) & 0xffu)", call="(void)MILAN_FORGE(id);")),
        ("S3 verifier #else deleted", once(fw, ELSE_ARM, "\treturn 1;\n#endif\n}")),
    ]
    return cases
