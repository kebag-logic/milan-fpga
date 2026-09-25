"""R317-2 part e: argument-exception delimiter tracking. The decision names a
complete call argument; the checker tracks parentheses, not braces."""
GUARD = "\tif (id != MILAN_ID_MAGIC) {"


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


def build(fw):
    def plain(stmt):
        return once(fw, GUARD, "\t" + stmt + "\n" + GUARD)
    return [
        ("CTRL unchanged firmware", fw),
        ("LIM cast sample as a compound-literal element inside a call",
         plain('printf("%lu\\n", ((unsigned long[]){ 0ul, (unsigned long)id, 1ul })[1]);')),
        ("LIM cast sample as the last compound-literal element inside a call",
         plain('printf("%lu\\n", ((unsigned long[]){ 0ul, (unsigned long)id })[1]);')),
        ("LIM cast sample as a compound-literal element, literal unparenthesized",
         plain('printf("%lu\\n", (unsigned long[]){ 0ul, (unsigned long)id, 1ul }[1]);')),
    ]
