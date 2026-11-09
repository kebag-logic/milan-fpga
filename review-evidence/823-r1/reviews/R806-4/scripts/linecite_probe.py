"""Feed the 32x32 format page's drift gate the page plus one extra citation per form; print which it refuses.
Usage: python3 -I linecite_probe.py <tree>"""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
import check_nvm_format_32x32 as g
import nvm_format_32x32_tables as t
page, index = g.PAGE.read_text(), g.INDEX.read_text()
r = g.compute()
anchors = t.LAYERS + t.VERSION_CHAIN + t.CITED
base = g.findings(page, index, r, anchors)
print(f"clean page: {len(base)} finding(s)")
forms = {
    "single (the self-test's form)": "See `sw/litex/milan_soc.py:179`.",
    "range": "See `sw/litex/milan_soc.py:179-181`.",
    "list": "See `sw/firmware/ctrl_nvm/nvm_store.c:408,465`.",
    "unquoted": "See sw/litex/milan_soc.py:179.",
    "quoted path, bare line": "See `sw/litex/milan_soc.py` line 179.",
    "link with line anchor": "See [the map](../../sw/litex/milan_soc.py#L179).",
}
for name, text in forms.items():
    got = g.findings(page + "\n" + text + "\n", index, r, anchors)
    print(f"{name:32s} {'REFUSED' if len(got) > len(base) else 'accepted'}  {text}")
