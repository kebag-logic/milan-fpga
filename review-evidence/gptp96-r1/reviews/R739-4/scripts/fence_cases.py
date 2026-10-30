"""Run fence cases through copy_findings of a given check_docs.py copy.
Usage: python3 -I fence_cases.py <check_docs.py> <repo-root>
Prints, per case, whether the checker reports the copy, against CommonMark."""
import importlib.util, sys, types
spec = importlib.util.spec_from_file_location("cd", sys.argv[1])
cd = importlib.util.module_from_spec(spec); sys.path.insert(0, sys.argv[2]); spec.loader.exec_module(cd)
fixture = types.SimpleNamespace(SYNC_RTO_MS_C=375)
table = (f"{cd.CONSTANTS_HEADING}\n\n| Constant | Value | Meaning |\n|---|---:|---|\n"
         "| `SYNC_RTO_MS_C` | 375 | syncReceiptTimeout, ms |\n")
# (label, text, CommonMark: is the final 375 ms line prose that must be reported?)
cases = [
    ("copy after tilde fence", "~~~\nx\n~~~\nA 375 ms watch.\n", True),
    ("copy inside tilde fence", "~~~\nA 375 ms watch.\n~~~\n", False),
    ("copy after 4-tilde fence holding ~~~", "~~~~\n~~~\n~~~~\nA 375 ms watch.\n", True),
    ("copy after tilde fence holding '~~~ x'", "~~~sh\n~~~ x\n~~~\nA 375 ms watch.\n", True),
    ("copy after 4-backtick fence holding ```", "````\n```\n````\nA 375 ms watch.\n", True),
    ("copy after backtick fence holding '``` x'", "```\n``` x\n```\nA 375 ms watch.\n", True),
    ("copy after mixed fences", "~~~\n```\n~~~\nA 375 ms watch.\n", True),
    ("copy inside 4-tilde fence", "~~~~\n~~~\nA 375 ms watch.\n~~~~\n", False),
]
bad = 0
for label, text, prose in cases:
    got = bool(cd.copy_findings({"docs/GUIDE.md": text}, table, fixture))
    ok = got == prose; bad += not ok
    print(f"{'ok  ' if ok else 'BAD '} reported={got!s:5} commonmark_prose={prose!s:5} {label}")
print(f"{bad} disagreements")
