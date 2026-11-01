"""Compare the delta's checker with the previous head's on list and paragraph forms.

usage: python3 -I compare_heads.py <check_docs-head.py> <check_docs-previous.py> <repo-root>
A form hides a real copy at a head when copy_findings reports nothing there.
"""
import importlib.util
import sys
import types

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[3])


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    module.__dict__["__file__"] = sys.argv[3] + "/scripts/check_docs.py"
    spec.loader.exec_module(module)
    return module


fixture = types.SimpleNamespace(SYNC_RTO_MS_C=375)
FORMS = {
    "lazy_list_line_recorded": "- Item.\nlazy\n  ```\nA 375 ms watch.\n",
    "item_five_spaces": "-      x\n  ```\n  y\nA 375 ms watch.\n",
    "item_trailing_spaces": "-   \n  ```\n  y\nA 375 ms watch.\n",
    "ordered_two_in_paragraph": "text\n2. ```\n   A 375 ms watch.\n",
    "thematic_break_spaced": "* * *\n  ```\n  x\ny\n```\nA 375 ms watch.\n",
    "ordered_two_then_fence": "text\n2. item\n   ```\n   x\ny\n```\nA 375 ms watch.\n",
    "control_plain": "A 375 ms watch.\n",
}
for name, path in (("head", sys.argv[1]), ("previous", sys.argv[2])):
    module = load(name, path)
    table = (f"{module.CONSTANTS_HEADING}\n\n| Constant | Value | Meaning |\n|---|---:|---|\n"
             "| `SYNC_RTO_MS_C` | 375 | syncReceiptTimeout, ms |\n")
    for form, text in FORMS.items():
        found = module.copy_findings({"docs/GUIDE.md": text}, table, fixture)
        print(f"{name} {form}: {'reported' if found else 'HIDDEN'}")
