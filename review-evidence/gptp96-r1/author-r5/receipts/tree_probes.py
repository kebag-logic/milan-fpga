"""Plant each reviewed case and each neighbour in an archive of a commit; run the docs check.

usage: python3 -I tree_probes.py <repo> <commit> <scratch>
Each probe appends to a Current page of a fresh archive copy. The repository is never touched.
Kinds: copy must fail; noncopy must pass; open is an expected-failure self-test arm.
"""
import concurrent.futures
import shutil
import subprocess
import sys
from pathlib import Path

GUIDE = "docs/HDL_DEVELOPER.md"
P = "The Sync watch is 375 ms.\n"
F = "The Sync receipt timeout is 125 ms.\n"
PROBES = {
    "control": ("", "noncopy"),
    # R739-4 F1 and its fence cases.
    "r739_long_tilde": ("~~~~\n~~~\n~~~~\n\n" + P, "copy"),
    "r739_tilde_info_close": ("~~~text\nliteral\n~~~ not a close\nmore\n~~~\n\n" + P, "copy"),
    "r739_long_backtick": ("````\n```\n````\n\n" + P, "copy"),
    "r739_backtick_info_close": ("```\n``` x\n```\n\n" + P, "copy"),
    "r739_inside_long_tilde": ("~~~~\n~~~\n" + P + "~~~~\n", "noncopy"),
    # R739-4 F2.
    "r739_underscore_ms": ("The Sync watch is _375 ms_.\n", "copy"),
    "r739_underscore_digit": ("After _5 minutes_ it ceases.\n", "copy"),
    "r739_underscore_word": ("After _five minutes_ it ceases.\n", "copy"),
    # R739-4 underscore_boundary.txt, the six non-copies.
    "six_decimal_min": ("A 2.5 min hold.\n", "noncopy"),
    "six_twenty_five": ("A twenty-five minutes soak.\n", "noncopy"),
    "six_minimum": ("At least 5 minimum samples.\n", "noncopy"),
    "six_msec": ("A 375 msec gap.\n", "noncopy"),
    "six_1375": ("A 1375 ms gap.\n", "noncopy"),
    "six_snake": ("snake_5_min\n", "noncopy"),
    # R740-4 F1 and F2.
    "r740_fenced_copy": ("~~~~text\n~~~\n~~~~\n\n" + F, "copy"),
    "r740_tilde_trailing": ("~~~text\n~~~example\n~~~\n\n" + F, "copy"),
    "r740_four_marker_control": ("~~~~text\nexample\n~~~~\n\n" + F, "copy"),
    "r740_plain_control": (F, "copy"),
    "r740_underscore_ms": ("The Sync receipt timeout is _125 ms_.\n", "copy"),
    "r740_underscore_minutes": ("A _5 minutes_ countdown.\n", "copy"),
    "r740_underscore_word": ("A _five minutes_ countdown.\n", "copy"),
    "r740_asterisk_control": ("The Sync receipt timeout is *125 ms*.\n", "copy"),
    # Scanner cases beyond the reviews' plants.
    "list_marker_fence": ("- ```\n  x\n  ```\n\n" + P, "copy"),
    "list_end_closes_fence": ("- Item.\n  ```\n  x\n\n" + P, "copy"),
    "comment_fence_marker": ("<!--\n```\n-->\n\n" + P, "copy"),
    "fenced_list_content": ("1.  Item.\n\n    ```\n    " + P + "    ```\n", "noncopy"),
    "markup_value_alone": ("A **375** ms watch.\n", "copy"),
    "markup_hyphen": ("A **5**-minute countdown.\n", "copy"),
    # Earlier rounds' controls.
    "tilde_fence": ("~~~sh\nsleep 375 ms\n~~~\n", "noncopy"),
    "backtick_fence": ("```sh\nsleep 375 ms\n```\n", "noncopy"),
    "digits_5_min": ("A 5 min countdown.\n", "copy"),
    "word_five_minutes": ("A five minutes countdown.\n", "copy"),
    "five_minute": ("The five-minute countdown.\n", "copy"),
    "linked_name": ("The [`SYNC_RTO_MS_C`](INTEGRATION.md#protocol-constants) Sync watch.\n", "noncopy"),
    "blockquote_copy": ("> The Sync watch is 375 ms.\n", "copy"),
    # Expected-failure arms in the self-test: real copies the rule misses today.
    "open_decimal_seconds": ("A 0.375 s watch.\n", "open"),
    "open_unit_word": ("A 375 milliseconds watch.\n", "open"),
    "open_line_wrap": ("The Sync watch is 375\nms long.\n", "open"),
    "open_link_on_value": ("A [375](INTEGRATION.md) ms watch.\n", "open"),
    "open_html_on_value": ("A <b>375</b> ms watch.\n", "open"),
    "open_html_entity": ("A 375&nbsp;ms watch.\n", "open"),
    "open_strikethrough_value": ("A ~~375~~ ms watch.\n", "open"),
    "open_html_block_fence": ("<pre>\n```\n</pre>\n\n" + P, "open"),
    "open_indented_heading_home": ("", "open"),
    "open_lazy_list_fence": ("- Item.\nlazy\n  ```\n" + P, "open"),
}


def run(repo, commit, scratch, name):
    text, kind = PROBES[name]
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    tree.mkdir(parents=True)
    subprocess.run(f"git -C {repo} archive {commit} | tar -x -C {tree}", shell=True, check=True)
    if name == "open_indented_heading_home":
        page = tree / "docs/INTEGRATION.md"
        lines = page.read_text(encoding="utf-8").splitlines(True)
        at = next(i for i, line in enumerate(lines) if line.startswith("## Protocol constants"))
        lines.insert(at + 1, "\n  ## Aside\n\nThe Sync watch is 375 ms.\n\n")
        page.write_text("".join(lines), encoding="utf-8")
    elif text:
        page = tree / GUIDE
        page.write_text(page.read_text(encoding="utf-8") + "\n" + text, encoding="utf-8")
    result = subprocess.run([sys.executable, "-B", "scripts/check_docs.py"], cwd=tree,
                            capture_output=True, text=True)
    lines = (result.stdout + result.stderr).splitlines()
    first = next((l.strip() for l in lines if "restates" in l), lines[-1].strip() if lines else "")
    shutil.rmtree(tree)
    want = {"copy": 1, "noncopy": 0}.get(kind)
    verdict = "info" if want is None else ("ok" if result.returncode == want else "DIFFERS")
    return f"{name:30} {kind:8} rc={result.returncode} {verdict:8} | {first}", verdict == "DIFFERS"


def main():
    repo, commit, scratch = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    scratch.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        rows = list(pool.map(lambda n: run(repo, commit, scratch, n), PROBES))
    for row, _ in rows:
        print(row)
    differs = sum(bad for _, bad in rows)
    print(f"{len(rows)} probes at {commit}, {differs} differ from expectation")


if __name__ == "__main__":
    main()
