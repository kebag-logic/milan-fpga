"""R317-2 part d: macro-free lvalue-wrapper and asm-output forgeries of the
sample, written directly before the guard, graded in both modes. These are
the gate's own `plain ...` bypass spellings (sw/builder/test_builder.py
identity_bypass_bodies with x -> id), which the gate grades only with a compiler."""
GUARD = "\tif (id != MILAN_ID_MAGIC) {"


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


def build(fw):
    forms = {
        "extension address": "(*(__extension__ &(id)) = MILAN_ID_MAGIC)",
        "asm immediate output": '__asm__ volatile("li %0, 0x4d494c4e" : "=r"(id))',
        "choose lvalue": "__builtin_choose_expr(1, id, id) = MILAN_ID_MAGIC",
        "generic lvalue": "_Generic(0, int: id) = MILAN_ID_MAGIC",
        "real lvalue": "(__real__ id) = MILAN_ID_MAGIC",
        "extension lvalue": "(__extension__ id) = MILAN_ID_MAGIC",
        "asm tied output": '__asm__ volatile ("" : "=r"(id) : "0"(MILAN_ID_MAGIC))',
    }
    return [("CTRL unchanged firmware", fw)] + [
        ("PLAIN " + label, once(fw, GUARD, "\t" + stmt + ";\n" + GUARD))
        for label, stmt in forms.items()]
