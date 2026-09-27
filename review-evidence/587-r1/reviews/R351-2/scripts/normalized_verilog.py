#!/usr/bin/env python3
"""Apply the committed export_comparison normalization rule verbatim and hash the result.

Usage: normalized_verilog.py VERILOG BUILD_ROOT CHECKOUT_ROOT

Rule, as committed in docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json at ce654301:
  "Replace each absolute build root with $BUILD, then the absolute checkout root with $REPO
   (including GPTP_UCODE_HEX_P, PP_TROM_HEX_P and PP_UCODE_HEX_P paths). Strip block comments
   with /\\*.*?\\*/ in DOTALL mode, then line comments with //[^\\n]*; preserve all other
   whitespace and hash UTF-8 bytes."
Written from that text only, before any export at this head existed; it is not tuned to a value.
Prints the digest, the byte count, and any absolute path that survives normalization.
"""
import hashlib
import re
import sys

verilog, build_root, checkout_root = sys.argv[1:4]
for root in (build_root, checkout_root):
    if not root.startswith("/") or root.endswith("/"):
        sys.exit(f"root must be absolute without a trailing slash: {root}")
with open(verilog, encoding="utf-8", newline="") as stream:
    text = stream.read()
counts = {"$BUILD": text.count(build_root)}
text = text.replace(build_root, "$BUILD")
counts["$REPO"] = text.count(checkout_root)
text = text.replace(checkout_root, "$REPO")
text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
text = re.sub(r"//[^\n]*", "", text)
data = text.encode("utf-8")
print(f"sha256={hashlib.sha256(data).hexdigest()} bytes={len(data)} "
      f"replaced_build={counts['$BUILD']} replaced_repo={counts['$REPO']}")
for name in ("GPTP_UCODE_HEX_P", "PP_TROM_HEX_P", "PP_UCODE_HEX_P"):
    for match in re.finditer(rf"\.{name}\s*\(\s*\"([^\"]*)\"", text):
        print(f"  {name} = {match.group(1)}")
residual = sorted(set(re.findall(r"\"(/[^\"]*)\"", text)))
print(f"  residual absolute string literals: {len(residual)}")
for item in residual:
    print(f"    {item}")
