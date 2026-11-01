"""Fuzz the fence scanner against a CommonMark parser.

usage: python -I commonmark_diff.py <check_docs.py> <repo-root> <documents> <seed> [no-lazy]
Each sentinel line is rendered by the parser as code or as visible text.
ESCAPE: the parser shows the line and the scanner hides it, so a copy would pass.
LOUD-FENCE: the parser puts the line in a fence and the scanner returns it, so a copy is reported.
LOUD-INDENT: the same for an indented code block, which the copy rule has always scanned.
no-lazy: a blank line separates text from any earlier line once a list has been seen, so no
line can be a lazy paragraph continuation of a list item.
"""
import collections
import importlib.util
import random
import re
import sys

from markdown_it import MarkdownIt

spec = importlib.util.spec_from_file_location("check_docs", sys.argv[1])
checker = importlib.util.module_from_spec(spec)
sys.path.insert(0, sys.argv[2])
sys.dont_write_bytecode = True
spec.loader.exec_module(checker)
parser = MarkdownIt("commonmark")
SHAPES = ["```", "````", "~~~", "~~~~", "``` x", "~~~ x", "~~~ a`b", "``` a`b", "```  ", "~~~\t",
          "  ```", "   ```", "    ```", "  ~~~", "\t```", "- ```", "1. ```", "- - ```", "- item", "1. item",
          "1.  item", "  - item", "<!--", "-->", "<!-- x -->", "", "", "text", "  text"]
SENTINELS = ["@", "  @", "    @", "   @", "\t@", "- @", "text @"]
TOKEN = re.compile(r"S\d+E")


def parser_view(text):
    fence, indented, shown = set(), set(), set()
    for token in parser.parse(text):
        found = set(TOKEN.findall(token.content or ""))
        {"fence": fence, "code_block": indented}.get(token.type, shown).update(found)
    return fence, indented, shown


def separate_text(lines):
    output, listed = [], False
    for line in lines:
        block = re.match(r" {0,3}(?:[-+*] |\d+[.)] |`{3,}[^`]*$|~{3,})", line.expandtabs(4))
        if listed and output and output[-1] and line and not block:
            output.append("")
        listed = listed or bool(re.match(r" *(?:[-+*] |\d+[.)] )", line))
        output.append(line)
    return output


def main():
    total, seed = int(sys.argv[3]), int(sys.argv[4])
    rng = random.Random(seed)
    tally, samples = collections.Counter(), collections.defaultdict(list)
    for _ in range(total):
        lines, count = [], 0
        for _ in range(rng.randint(2, 7)):
            if rng.random() < 0.3:
                count += 1
                lines.append(rng.choice(SENTINELS).replace("@", f"S{count}E"))
            else:
                lines.append(rng.choice(SHAPES))
        if len(sys.argv) > 5:
            lines = separate_text(lines)
        text = "\n".join(lines) + "\n"
        fence, indented, shown = parser_view(text)
        kept = set(TOKEN.findall("\n".join(line for _, line in checker.unfenced_lines(text))))
        for sentinel in fence | indented | shown:
            hidden = sentinel not in kept
            if sentinel in shown and hidden:
                kind = "ESCAPE"
            elif sentinel in fence and not hidden:
                kind = "LOUD-FENCE"
            elif sentinel in indented and not hidden:
                kind = "LOUD-INDENT"
            else:
                kind = "agree"
            tally[kind] += 1
            if kind != "agree" and len(samples[kind]) < 12:
                samples[kind].append(text)
    print(f"documents {total} seed {seed} " + " ".join(f"{k}={v}" for k, v in sorted(tally.items())))
    for kind, texts in samples.items():
        print(f"-- first {kind} samples")
        for text in sorted(texts, key=len)[:12]:
            print(repr(text))


if __name__ == "__main__":
    main()
