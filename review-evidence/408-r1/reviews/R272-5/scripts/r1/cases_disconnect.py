"""R272-1 disconnect cases: every hostile control the retired rules' replacements
carry, taken from the gate's OWN tables at the mutation-loop hook.

  * every entry of `retired_rule_mutations` (the entries the retired splice,
    paste, reach, directory and cast/store/asm rules used to be pinned on,
    re-pinned on their replacements, plus the file-wide and arm shapes);
  * every entry of the main `mutations` tuple whose reason pin is a tuple
    carrying SELECTION_PIN (the per-selection grading's own controls);
  * the two exempted-helper mutants (#409 acceptance 4).

Each is graded through assert_boot_contract() with its recorded reason pin,
so a run with one instrument disconnected reports, per control, whether it
is still refused on its pin, refused for another reason, or accepted."""


def _entry(ns, mutation, group):
    label, firmware, docs, csr, because = mutation[:5]
    files = mutation[5] if len(mutation) > 5 else None
    assert docs is ns["docs_source"] and csr is ns["csr_source"], label
    return {"label": f"[{group}] {label}", "firmware": firmware,
            "because": list(because) if isinstance(because, tuple) else because,
            "makefile": getattr(files, "makefile", None),
            "listing": getattr(files, "listing", None),
            "datapath": getattr(files, "datapath", None)}


def cases(ns):
    selection = ns["SELECTION_PIN"]
    for mutation in ns["retired_rule_mutations"]:
        yield _entry(ns, mutation, "retired")
    retired_labels = {m[0] for m in ns["retired_rule_mutations"]}
    for mutation in ns["mutations"]:
        because = mutation[4]
        if mutation[0] in retired_labels:
            continue
        if isinstance(because, tuple) and selection in because:
            yield _entry(ns, mutation, "selection")
        elif "exempted address helper" in mutation[0]:
            yield _entry(ns, mutation, "helper")
