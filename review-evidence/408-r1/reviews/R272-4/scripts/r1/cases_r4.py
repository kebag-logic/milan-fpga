"""R272-1 probe cases, round 4: legitimate edits the per-selection grading
might newly refuse because it grades every COMBINATION of arms, including
combinations no build can select (two groups testing the same macro)."""

UART_TAIL = "\tprint_tod(gettime_ns());\n}"
STATIC = "static int aem_loaded;"


def first(text, old, new):
    """`text` with the FIRST `old` replaced; refuse a no-op."""
    assert old in text, f"anchor not found: {old!r}"
    return text.replace(old, new, 1)


def cases(ns):
    fw = ns["firmware_source"]
    helper = ("#ifdef MILAN_DEBUG_TOD\nstatic void milan_debug_tod(void)\n{\n"
              "\tprintf(\"tod: debug\\n\");\n}\n#endif\n\n")
    yield {"label": "a debug helper defined under #ifdef MILAN_DEBUG_TOD and "
                    "called under a second #ifdef MILAN_DEBUG_TOD in a UART "
                    "handler",
           "firmware": first(first(fw, STATIC, helper + STATIC), UART_TAIL,
                             "#ifdef MILAN_DEBUG_TOD\n\tmilan_debug_tod();\n"
                             "#endif\n" + UART_TAIL)}
    yield {"label": "control: the same debug printf in ONE #ifdef in a UART "
                    "handler",
           "firmware": first(fw, UART_TAIL,
                             "#ifdef MILAN_DEBUG_TOD\n\tprintf(\"tod: debug\\n\");"
                             "\n#endif\n" + UART_TAIL)}
    yield {"label": "a debug-only static counter declared under #ifdef and "
                    "incremented under a second #ifdef of the same macro",
           "firmware": first(first(fw, STATIC,
                                   "#ifdef MILAN_DEBUG_TOD\nstatic unsigned int "
                                   "milan_tod_reads;\n#endif\n\n" + STATIC),
                             UART_TAIL,
                             "#ifdef MILAN_DEBUG_TOD\n\tmilan_tod_reads++;\n"
                             "#endif\n" + UART_TAIL)}
