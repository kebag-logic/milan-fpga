"""R272-6: the shipping firmware with a `#` alone at its end (no line end),
after a line end, and as a null directive line; graded through
assert_boot_contract() (probe_gate1b.py, anchor accepted). Expected: each
refused, the end-of-file ones on the directive-set closure's pin."""


def cases(ns):
    fw = ns["firmware_source"]
    pin = "preprocessing directives are pinned"
    body = fw if fw.endswith("\n") else fw + "\n"
    yield {"label": "[r6] `#` alone at the end of the file, no line end",
           "firmware": body + "#", "because": pin}
    yield {"label": "[r6] `#` alone at the end of the file, after a blank "
                    "line", "firmware": body + "\n#", "because": pin}
    yield {"label": "[r6] `#` alone on the last line, with its line end",
           "firmware": body + "#\n"}
    yield {"label": "[r6] control: the shipping firmware unchanged",
           "firmware": fw}
