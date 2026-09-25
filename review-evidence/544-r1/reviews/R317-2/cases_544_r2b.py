"""Reviewer case set for issue #544 round 2, part b (R317-2).

Storage-class spellings of the real sample through the whole contract, and the
unit-wide nested-function refusal away from the sample. Prefixes as in
cases_544_r2.py; STORE rows record which rule answers.
"""

READ = "\tuint32_t id = milan_read(MILAN_ID);\n"
GUARD_END = ("\t\tprintf(\"Milan baremetal: CSR identity mismatch; fabric "
             "remains disabled.\\n\");\n\t\treturn;\n\t}\n")
STATUS = "static void milan_status_handler(int nb_params, char **params)\n{"


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


def build(fw):
    assert fw.count(READ) == 1 and fw.count(STATUS) == 1 and fw.count(GUARD_END) == 1
    cases = [("CTRL unchanged firmware", fw)]
    for storage in ("auto", "register", "const", "volatile", "static"):
        cases.append((f"STORE {storage} sample",
                      once(fw, READ, f"\t{storage} uint32_t id = milan_read(MILAN_ID);\n")))
    cases += [
        ("ESC nested function in another function, no sample",
         once(fw, STATUS, STATUS + "\n\tint milan_nested(void) { return 0; }\n"
              "\t(void)milan_nested();")),
        ("ESC nested function in milan_init before the read",
         once(fw, READ, "\tint milan_nested(void) { return 0; }\n" + READ)),
        ("ESC nested function after guard naming the sample",
         once(fw, GUARD_END, GUARD_END +
              "\tvoid milan_nested(void) { id = 0u; }\n\tmilan_nested();\n")),
    ]
    return cases
