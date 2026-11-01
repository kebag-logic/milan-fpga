"""Plant one change per round-5 rule in a scratch copy; --selftest must fail at its arm.

usage: python3 -I checker_mutants.py <repo> <scratch>
The first three are the mutants the ruling names. A control run must pass.
"""
import shutil
import subprocess
import sys
from pathlib import Path

OLD_WITHOUT_FENCES = '''    return "\\n".join(line for _, line in unfenced_lines(HTML_COMMENT_RE.sub("", text)))'''
BACKTICK_TOGGLE = '''    output, fenced = [], False
    for line in HTML_COMMENT_RE.sub("", text).splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced:
            output.append(line)
    return "\\n".join(output)'''

MUTANTS = {
    # The ruling's three.
    "fence_length_ignored": (
        "\n                    and len(run.group(1)) >= len(fence)):", "):",
        "content of a longer tilde fence failed"),
    "fence_char_ignored": (
        "run.group(1)[0] == fence[0]\n                    and ", "",
        "backtick line in a tilde fence failed"),
    "markup_not_stripped": (
        'INLINE_MARKUP_RE.sub(gap, line).split()', 'line.split()',
        "underscore unit copy constant copy escaped"),
    # Closing fence.
    "close_allows_trailing_text": (
        r'''FENCE_CLOSE_RE = re.compile(r"(`{3,}|~{3,})[ \t]*$")''',
        r'''FENCE_CLOSE_RE = re.compile(r"(`{3,}|~{3,})")''',
        "close marker with text failed"),
    "close_rejects_trailing_blanks": (
        r'''FENCE_CLOSE_RE = re.compile(r"(`{3,}|~{3,})[ \t]*$")''',
        r'''FENCE_CLOSE_RE = re.compile(r"(`{3,}|~{3,})$")''',
        "copy after a close with trailing blanks constant copy escaped"),
    "close_indent_unlimited": (
        "if (column - base <= 3 and run and", "if (run and",
        "close marker indented four failed"),
    "close_must_be_flush": (
        "if (column - base <= 3 and run and", "if (column == base and run and",
        "copy after a close indented three constant copy escaped"),
    "close_indent_ignores_container": (
        "if (column - base <= 3 and run and", "if (column <= 3 and run and",
        "copy after a list-item fence constant copy escaped"),
    # Opening fence.
    "open_two_characters": (
        'FENCE_OPEN_RE = re.compile(r"(`{3,})[^`]*$|(~{3,})")',
        'FENCE_OPEN_RE = re.compile(r"(`{3,})[^`]*$|(~{2,})")',
        "copy after a two-character run constant copy escaped"),
    "open_backtick_info_any": (
        'FENCE_OPEN_RE = re.compile(r"(`{3,})[^`]*$|(~{3,})")',
        'FENCE_OPEN_RE = re.compile(r"(`{3,})|(~{3,})")',
        "copy after a backtick info with a backtick constant copy escaped"),
    "open_tilde_info_restricted": (
        'FENCE_OPEN_RE = re.compile(r"(`{3,})[^`]*$|(~{3,})")',
        'FENCE_OPEN_RE = re.compile(r"(`{3,})[^`]*$|(~{3,})[^`~]*$")',
        "tilde info string holding markers failed"),
    "open_indent_unlimited": (
        "if column - base <= 3 and run:", "if run:",
        "copy after a marker indented four constant copy escaped"),
    "open_indent_ignores_container": (
        "if column - base <= 3 and run:", "if column <= 3 and run:",
        "fence inside a list item failed"),
    # Line splitting and tabs.
    "split_on_form_feed": (
        r'''enumerate(re.split(r"\r\n?|\n", text), start=1)''', "enumerate(text.splitlines(), start=1)",
        "close marker before a form feed failed"),
    "tabs_not_expanded": (
        "line = raw.expandtabs(4)", "line = raw",
        "tab-indented fence in a list item failed"),
    # List containers.
    "list_end_keeps_fence": (
        '            items.pop()\n            fence = ""\n', "            items.pop()\n",
        "copy after a list item ended its fence constant copy escaped"),
    "blank_line_ends_list": (
        "while items and line.strip() and column < items[-1]:", "while items and column < items[-1]:",
        "fence inside a list item failed"),
    "list_markers_ignored": (
        "        while column - base <= 3:\n            item =", "        while False:\n            item =",
        "fence inside a list item failed"),
    "one_list_marker_per_line": (
        "            column = item.end()\n", "            column = item.end()\n            break\n",
        "fence on a nested list marker failed"),
    "list_marker_indent_unlimited": (
        "        while column - base <= 3:\n            item =", "        while True:\n            item =",
        "copy under a list marker indented four constant copy escaped"),
    "empty_item_offset": (
        "base = max(item.end(), item.start(1) + 1)", "base = item.end()",
        "fence after an empty list item failed"),
    # HTML comments.
    "comment_marker_opens_fence": (
        'if comment or (column - base <= 3 and line.startswith("<!--", column)):', "if False:",
        "copy after a marker in an HTML comment constant copy escaped"),
    "comment_never_ends": (
        '            comment = "-->" not in line\n', "            comment = True\n",
        "fence after an HTML comment failed"),
    "comment_indent_unlimited": (
        'if comment or (column - base <= 3 and line.startswith("<!--", column)):',
        'if comment or line.startswith("<!--", column):',
        "fence after an indented comment marker failed"),
    # Inline markup.
    "underscore_always_stripped": (
        r'''INLINE_MARKUP_RE = re.compile(r"[*`]+|(?<!\w)_+|_+(?!\w)")''',
        r'''INLINE_MARKUP_RE = re.compile(r"[*`_]+")''',
        "underscores between word characters failed"),
    "underscore_never_stripped": (
        r'''INLINE_MARKUP_RE = re.compile(r"[*`]+|(?<!\w)_+|_+(?!\w)")''',
        r'''INLINE_MARKUP_RE = re.compile(r"[*`]+")''',
        "underscore unit copy constant copy escaped"),
    "underscore_opening_only": (
        r'''INLINE_MARKUP_RE = re.compile(r"[*`]+|(?<!\w)_+|_+(?!\w)")''',
        r'''INLINE_MARKUP_RE = re.compile(r"[*`]+|(?<!\w)_+")''',
        "underscore unit copy constant copy escaped"),
    "underscore_closing_only": (
        r'''INLINE_MARKUP_RE = re.compile(r"[*`]+|(?<!\w)_+|_+(?!\w)")''',
        r'''INLINE_MARKUP_RE = re.compile(r"[*`]+|_+(?!\w)")''',
        "underscore digit minutes constant copy escaped"),
    "asterisk_kept": (
        r'''INLINE_MARKUP_RE = re.compile(r"[*`]+|(?<!\w)_+|_+(?!\w)")''',
        r'''INLINE_MARKUP_RE = re.compile(r"`+|(?<!\w)_+|_+(?!\w)")''',
        "markup on the value alone constant copy escaped"),
    "backtick_kept": (
        r'''INLINE_MARKUP_RE = re.compile(r"[*`]+|(?<!\w)_+|_+(?!\w)")''',
        r'''INLINE_MARKUP_RE = re.compile(r"\*+|(?<!\w)_+|_+(?!\w)")''',
        "code span on the value alone constant copy escaped"),
    "spaced_view_dropped": (
        "pattern.search(spaced) or pattern.search(joined)", "pattern.search(joined)",
        "code span against the value constant copy escaped"),
    "joined_view_dropped": (
        "pattern.search(spaced) or pattern.search(joined)", "pattern.search(spaced)",
        "markup on digit minutes before a hyphen constant copy escaped"),
    "spaces_not_collapsed": (
        '''" ".join(INLINE_MARKUP_RE.sub(gap, line).split())''', "INLINE_MARKUP_RE.sub(gap, line)",
        "two spaces before the unit constant copy escaped"),
    # Callers of the one scanner.
    "copy_rule_ignores_fences": (
        "for number, line in unfenced_lines(text):", "for number, line in enumerate(text.split(chr(10)), 1):",
        "fenced command failed"),
    "style_rule_old_toggle": (
        OLD_WITHOUT_FENCES, BACKTICK_TOGGLE,
        "long sentence after a longer fence escaped"),
    "fenced_heading_moves_home": (
        "for number, line in unfenced_lines(text):\n            if line.startswith(\"## \"):\n"
        "                home = relative == CONSTANTS_PAGE and line.strip() == CONSTANTS_HEADING\n",
        "visible = {n for n, _ in unfenced_lines(text)}\n"
        "        for number, line in enumerate(text.split(chr(10)), 1):\n"
        "            if line.startswith(\"## \"):\n"
        "                home = relative == CONSTANTS_PAGE and line.strip() == CONSTANTS_HEADING\n"
        "            if number not in visible:\n                continue\n",
        "heading inside a fence"),
    # Expected-failure arms: a change that catches the case must trip its arm.
    "xfail_decimal_seconds": (
        "    minutes = value // 60000 if unit",
        '    patterns += [rf"(?<![\\d.,]){value / 1000}[\\s-]?s\\b"] if unit == "ms" else []\n    minutes = value // 60000 if unit',
        "expected failure now caught: decimal seconds"),
    "xfail_spelled_unit": (
        "    numbers = [(value, unit)]\n",
        '    numbers = [(value, "(?:ms|milliseconds)" if unit == "ms" else unit)]\n',
        "expected failure now caught: spelled unit"),
    "xfail_wrapped_line": (
        "spaced, joined = without_markup(line)",
        'spaced, joined = without_markup(dict(unfenced_lines(text)).get(number - 1, "") + " " + line)',
        "expected failure now caught: wrapped line"),
    "xfail_link_on_value": (
        "    spaced, joined = (\n",
        '    line = LINK_RE.sub(lambda m: m.group(1), line)\n    spaced, joined = (\n',
        "expected failure now caught: link on the value"),
    "xfail_html_on_value": (
        "    spaced, joined = (\n",
        '    line = HTML_TAG_RE.sub("", line)\n    spaced, joined = (\n',
        "expected failure now caught: HTML tag on the value"),
    "xfail_html_entity": (
        "    spaced, joined = (\n",
        '    line = line.replace("&nbsp;", " ")\n    spaced, joined = (\n',
        "expected failure now caught: HTML entity as the space"),
    "xfail_strikethrough": (
        '''re.compile(r"[*`]+|(?<!\\w)_+|_+(?!\\w)")''',
        '''re.compile(r"[*`~]+|(?<!\\w)_+|_+(?!\\w)")''',
        "expected failure now caught: strikethrough on the value"),
    "xfail_html_block_marker": (
        'line.startswith("<!--", column)',
        'line.startswith(("<!--", "<pre"), column)',
        "expected failure now caught: marker in an HTML block"),
    "xfail_indented_heading": (
        '            if line.startswith("## "):\n                home = relative',
        '            if line.lstrip().startswith("## "):\n                home = relative',
        "expected failure now caught: indented heading"),
    "xfail_lazy_list_line": (
        "while items and line.strip() and column < items[-1]:",
        'while items and line.strip() and line != "lazy" and column < items[-1]:',
        "expected failure now caught: fence after a lazy list line"),
}


def selftest(tree: Path) -> tuple[int, str]:
    result = subprocess.run([sys.executable, "-B", "scripts/check_docs.py", "--selftest"],
                            cwd=tree, capture_output=True, text=True)
    return result.returncode, (result.stdout + result.stderr).strip()


def main() -> int:
    repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    source = (repo / "scripts/check_docs.py").read_text(encoding="utf-8")
    tree = scratch / "mutant-tree"
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(repo, tree, ignore=shutil.ignore_patterns(".git", "obj_dir", "__pycache__"))
    target = tree / "scripts/check_docs.py"
    bad = 0
    rc, out = selftest(tree)
    print(f"control rc={rc} {out}")
    bad += rc != 0
    for label, (old, new, expected) in MUTANTS.items():
        if source.count(old) < 1:
            print(f"{label} NOT PLANTED: anchor absent")
            bad += 1
            continue
        target.write_text(source.replace(old, new, 1), encoding="utf-8")
        rc, out = selftest(tree)
        last = out.splitlines()[-1] if out else ""
        killed = rc != 0 and expected in out
        print(f"{label} rc={rc} {'killed-at-own-arm' if killed else 'UNEXPECTED'} | {last}")
        bad += not killed
    target.write_text(source, encoding="utf-8")
    print(f"{len(MUTANTS)} planted, {bad} unexpected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
