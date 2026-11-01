"""Compare the docs gate's fence scanner with a CommonMark parser, line by line.

usage: python -I fence_oracle.py <repo-root> <spec|specjson file|fuzz N seed|tree|forms>
spec: the fenced-code examples of CommonMark 0.31.2 section 4.5, sentinel per content line.
specjson: the same section's examples read from the published spec.json.
fuzz: fence shapes only (no list, no comment), every char, run, indent and trailer mix.
tree: every Markdown page of the repository, parser's code lines against scanner's hidden lines.
forms: named list and comment documents outside the fuzz grammar.
ESCAPE: parser shows a line as text and the scanner hides it.
LOUD: parser puts a line in a fence and the scanner returns it.
"""
import collections
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("check_docs", ROOT / "scripts/check_docs.py")
checker = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(ROOT))
spec.loader.exec_module(checker)
parser = MarkdownIt("commonmark")
TOKEN = re.compile(r"S\d+E")

SPEC = {
    119: "```\nS1E\n >S2E\n```", 120: "~~~\nS1E\n >S2E\n~~~", 121: "``\nS1E\n``",
    122: "```\nS1E\n~~~\n```", 123: "~~~\nS1E\n```\n~~~", 124: "````\nS1E\n```\n``````",
    125: "~~~~\nS1E\n~~~\n~~~~", 126: "```", 127: "`````\n\n```\nS1E",
    128: "> ```\n> S1E\n\nS2E", 129: "```\n\n  \n```", 130: "```\n```",
    131: " ```\n S1E\nS2E\n```", 132: "  ```\nS1E\n  S2E\nS3E\n  ```",
    133: "   ```\n   S1E\n    S2E\n  S3E\n   ```", 134: "    ```\n    S1E\n    ```",
    135: "```\nS1E\n  ```", 136: "   ```\nS1E\n  ```", 137: "```\nS1E\n    ```",
    138: "``` ```\nS1E", 139: "~~~~~~\nS1E\n~~~ ~~", 140: "S1E\n```\nS2E\n```\nS3E",
    141: "S1E\n---\n~~~\nS2E\n~~~\n# S3E", 142: "```ruby\nS1E\n  S2E\nS3E\n```",
    143: "~~~~    ruby startline=3 $%@#$\nS1E\n  S2E\nS3E\n~~~~~~~", 144: "````;\n````",
    145: "``` aa ```\nS1E", 146: "~~~ aa ``` ~~~\nS1E\n~~~", 147: "```\n``` aaa\nS1E\n```",
}
FORMS = {
    "lazy_list_line_recorded": "- Item.\nlazy\n  ```\nS1E\n",
    "item_five_spaces": "-      x\n  ```\n  y\nS1E\n",
    "item_trailing_spaces": "-   \n  ```\n  y\nS1E\n",
    "ordered_two_in_paragraph": "text\n2. ```\n   S1E\n",
    "thematic_break_spaced": "* * *\n  ```\n  x\ny\n```\nS1E\n",
    "ordered_two_then_fence": "text\n2. item\n   ```\n   x\ny\n```\nS1E\n",
    "fence_in_blockquote": "> ```\n> S1E\n> ```\n",
    "comment_in_list_item": "- <!--\n  x\nS1E\n",
    "plain_nested_list": "- a\n  - b\n\n    ```\n    S1E\n    ```\n\nS2E\n",
    "ordered_list_step": "1. Step.\n\n   ```sh\n   S1E\n   ```\n\n2. Next.\n\nS2E\n",
}


def view(text):
    fence, indented, shown = set(), set(), set()
    for token in parser.parse(text):
        found = set(TOKEN.findall(token.content or ""))
        {"fence": fence, "code_block": indented}.get(token.type, shown).update(found)
    return fence, indented, shown


def compare(text):
    fence, indented, shown = view(text)
    kept = set(TOKEN.findall("\n".join(line for _, line in checker.unfenced_lines(text))))
    return sorted(shown - kept), sorted(fence & kept), sorted(indented & kept)


def run_spec():
    bad = 0
    for number, text in SPEC.items():
        escape, loud, indent = compare(text + "\n")
        state = "agree"
        if escape:
            state, bad = f"ESCAPE {escape}", bad + 1
        elif loud:
            state = f"LOUD {loud}"
        print(f"example {number}: {state}" + (f" indented-kept {indent}" if indent else ""))
    print(f"{len(SPEC)} examples, {bad} escapes")


def run_fuzz(total, seed):
    rng = random.Random(seed)
    tally, samples = collections.Counter(), {}
    for _ in range(total):
        lines, count = [], 0
        for _ in range(rng.randint(2, 8)):
            if rng.random() < 0.3:
                count += 1
                lines.append(" " * rng.choice((0, 0, 1, 3)) + f"S{count}E")
            elif rng.random() < 0.12:
                lines.append(rng.choice(("", "text", "# h")))
            else:
                char = rng.choice("`~")
                trailer = rng.choice(("", "", "  ", "\t", " x", "x", " a`b", " a~b", "\x0c"))
                lines.append(" " * rng.choice((0, 0, 0, 1, 2, 3, 4)) + char * rng.randint(2, 6) + trailer)
        fence, _, shown = view("\n".join(lines) + "\n")
        escape, loud, _ = compare("\n".join(lines) + "\n")
        tally["sentinels"] += len(fence | shown)
        for kind, found in (("ESCAPE", escape), ("LOUD", loud)):
            tally[kind] += len(found)
            if found:
                samples.setdefault(kind, repr("\n".join(lines)))
    print(f"documents {total} seed {seed} " + " ".join(f"{k}={tally[k]}" for k in ("sentinels", "ESCAPE", "LOUD")))
    for kind, text in samples.items():
        print(f"first {kind}: {text}")


def code_lines(text):
    lines = {"fence": set(), "code_block": set()}
    for token in parser.parse(text):
        if token.type in lines and token.map:
            lines[token.type].update(range(token.map[0] + 1, token.map[1] + 1))
    return lines


def run_tree():
    pages = sorted(ROOT.rglob("*.md"))
    escape_total = loud_total = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        total = len(re.split(r"\r\n?|\n", text))
        kept = {number for number, _ in checker.unfenced_lines(text)}
        hidden = set(range(1, total + 1)) - kept
        code = code_lines(text)
        # A fence's own marker lines are in the parser's range and hidden by the scanner.
        escape = sorted(hidden - code["fence"] - code["code_block"])
        loud = sorted(code["fence"] & kept)
        escape_total += len(escape)
        loud_total += len(loud)
        print(f"{page.relative_to(ROOT)} lines={total} hidden={len(hidden)} "
              f"parser_fence={len(code['fence'])} escape={escape} loud={loud}")
    print(f"{len(pages)} pages, {escape_total} hidden outside the parser's code, {loud_total} fence lines returned")


def run_forms():
    for name, text in FORMS.items():
        escape, loud, indent = compare(text)
        print(f"{name}: escape={escape} loud={loud} indented-kept={indent} | {text!r}")


def run_specjson(path):
    """Run the published examples of the Fenced code blocks section, line by line."""
    examples = [e for e in json.loads(Path(path).read_text(encoding="utf-8")) if e["section"] == "Fenced code blocks"]
    escapes = 0
    for example in examples:
        text = example["markdown"]
        total = len(re.split(r"\r\n?|\n", text))
        kept = {number for number, _ in checker.unfenced_lines(text)}
        code = code_lines(text)
        hidden = set(range(1, total + 1)) - kept
        blank = {n for n, line in enumerate(re.split(r"\r\n?|\n", text), 1) if not line.strip()}
        escape = sorted(hidden - code["fence"] - code["code_block"] - blank)
        loud = sorted((code["fence"] & kept) - blank)
        escapes += bool(escape)
        print(f"example {example['example']}: escape-lines={escape} fence-lines-returned={loud}")
    print(f"{len(examples)} published examples, {escapes} with a hidden line outside the parser's code")


mode = sys.argv[2]
if mode == "specjson":
    run_specjson(sys.argv[3])
elif mode == "spec":
    run_spec()
elif mode == "fuzz":
    run_fuzz(int(sys.argv[3]), int(sys.argv[4]))
elif mode == "tree":
    run_tree()
else:
    run_forms()
