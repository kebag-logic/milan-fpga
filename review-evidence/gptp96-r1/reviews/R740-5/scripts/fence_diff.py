#!/usr/bin/env python3
"""Differential of unfenced_lines against two CommonMark parsers, sentinel by sentinel.

usage: python3 -I fence_diff.py <check_docs.py> <repo> <grammar> <docs> <seed>
grammar: pure  = no containers, HTML or lazy lines: the sec. 4.5 rules alone
         lists = list containers added, blank line before prose after a list (no lazy lines)
A sentinel is ESCAPE when a parser renders it as visible text and the scanner hides it.
"""
import collections, importlib.util, random, re, sys
sys.dont_write_bytecode = True
from markdown_it import MarkdownIt
import commonmark

spec = importlib.util.spec_from_file_location("check_docs", sys.argv[1])
checker = importlib.util.module_from_spec(spec)
sys.path.insert(0, sys.argv[2])
spec.loader.exec_module(checker)
md = MarkdownIt("commonmark")
cm = commonmark.Parser()
TOKEN = re.compile(r"S\d+E")

def mdit_view(text):
    code, shown = set(), set()
    for t in md.parse(text):
        (code if t.type in ("fence", "code_block") else shown).update(TOKEN.findall(t.content or ""))
    return code, shown

def cm_view(text):
    code, shown = set(), set()
    text = re.sub(r"[ \t]+$", lambda m: m.group(0).replace("\t", " "), text, flags=re.M)
    for node, entering in cm.parse(text).walker():
        if entering and node.literal:
            (code if node.t == "code_block" else shown).update(TOKEN.findall(node.literal))
    return code, shown

def fence_shape(rng):
    char = rng.choice("`~")
    run = char * rng.choice([1, 2, 3, 3, 3, 4, 4, 5, 6])
    indent = rng.choice(["", "", "", " ", "  ", "   ", "    ", "     ", "\t", " \t"])
    tail = rng.choice(["", "", "", " ", "  ", "\t", " \t", " x", "x", " a`b", " a~b", "`", "~", "\x0c", "\xa0", " ```", " ~~~"])
    return indent + run + tail

def pure(rng, n):
    lines = []
    for _ in range(n):
        r = rng.random()
        if r < 0.55: lines.append(fence_shape(rng))
        elif r < 0.65: lines.append("")
        elif r < 0.75: lines.append("text")
        else: lines.append(None)
    return lines

MARK = ["- ", "-  ", "-   ", "-    ", "-     ", "-      ", "-\t", "- \t", "+ ", "* ", "1. ", "1.  ", "1)   ", "12. ",
        "2. ", "-", "1.", "- - ", "1. - ", "  - ", "   - ", "    - "]

def lists(rng, n):
    lines, listed = [], False
    for _ in range(n):
        r = rng.random()
        if r < 0.30:
            lines.append(rng.choice(MARK) + rng.choice(["item", "", "```", "~~~", "````", "@"]))
            listed = True
        elif r < 0.55: lines.append(rng.choice(["", " ", "  ", "   ", "    ", "     ", "      ", "\t", "\t  "]) + rng.choice(["```", "~~~", "````", "~~~ x"]))
        elif r < 0.70: lines.append("")
        else:
            indent = rng.choice(["", "  ", "   ", "    ", "      ", "\t"])
            if listed and lines and lines[-1]:
                lines.append("")
            lines.append(indent + "@")
    return lines

def main():
    grammar, total, seed = sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    rng, tally, samples = random.Random(seed), collections.Counter(), collections.defaultdict(list)
    gen = {"pure": pure, "lists": lists}[grammar]
    for _ in range(total):
        raw, count, out = gen(rng, rng.randint(2, 7)), 0, []
        for line in raw:
            if line is None: line = "@"
            if "@" in line:
                count += 1
                line = line.replace("@", f"S{count}E")
            out.append(line)
        text = "\n".join(out) + "\n"
        kept = set(TOKEN.findall("\n".join(l for _, l in checker.unfenced_lines(text))))
        for name, view in (("mdit", mdit_view), ("cm", cm_view)):
            code, shown = view(text)
            for s in code | shown:
                if s in shown and s not in code and s not in kept: kind = "ESCAPE"
                elif s in code and s in kept: kind = "LOUD"
                else: kind = "agree"
                tally[name, kind] += 1
                if kind == "ESCAPE" and len(samples[name]) < 400:
                    samples[name].append(text)
    print(f"grammar {grammar} docs {total} seed {seed} " + " ".join(f"{k[0]}.{k[1]}={v}" for k, v in sorted(tally.items())))
    for name, texts in samples.items():
        print(f"-- {name} shortest ESCAPE samples")
        for t in sorted(set(texts), key=len)[:15]:
            print(repr(t))

main()
