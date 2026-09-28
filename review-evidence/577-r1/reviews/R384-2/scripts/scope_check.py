#!/usr/bin/env python3
"""Scope receipts for PR #612 at a head: changed files, gitlinks, loader-function
source identity, processor tree identity, and the SoC hook placement.
Usage: scope_check.py <clone> <base> <round1> <head>"""
import ast, hashlib, subprocess, sys
clone, base, r1, head = sys.argv[1:5]
def git(*a):
    return subprocess.run(["git", "-C", clone, *a], capture_output=True, text=True, check=True).stdout
def show(rev, path):
    return git("show", f"{rev}:{path}")
print("files base..head:"); print(git("diff", "--name-status", base, head), end="")
print("files r1..head:"); print(git("diff", "--name-status", r1, head), end="")
for rev in (base, head):
    print(f"gitlinks {rev[:10]}:", " ".join(l.split()[2][:10] + ":" + l.split()[3]
          for l in git("ls-tree", rev).splitlines() if l.startswith("160000")))
subs = git("diff", "--name-only", base, head, "--", "protocol-processor", "gptp-processor",
           "third_party", "external", "avdecc")
print("submodule/avdecc paths changed base..head:", subs.split() or "none")
def fn_hash(rev, path, name):
    src = show(rev, path)
    node = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == name)
    return hashlib.sha256(ast.get_source_segment(src, node).encode()).hexdigest()[:16]
B = "sw/builder/endstation_builder.py"
for name in ("_load_clocking", "_validate_output_clock_sources", "load_config", "emit_aem_overlay"):
    a, b = fn_hash(base, B, name), fn_hash(head, B, name)
    print(f"{name}: base {a} head {b} {'UNCHANGED' if a == b else 'CHANGED'}")
S = "sw/litex/milan_soc.py"
diff = git("diff", "-U0", base, head, "--", S)
print("milan_soc.py hunks base..head:", diff.count("\n@@"), "; lines +", sum(1 for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")),
      "-", sum(1 for l in diff.splitlines() if l.startswith("-") and not l.startswith("---")))
src = show(head, S)
fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "build_desc_image")
body = ast.get_source_segment(src, fn).splitlines()
i_pack = next(i for i, l in enumerate(body) if "_img.build(" in l)
i_chk = next(i for i, l in enumerate(body) if "validate_shipping_image(blob)" in l)
i_ret = next(i for i, l in enumerate(body) if l.strip().startswith("return blob"))
print(f"build_desc_image: pack at +{i_pack}, check at +{i_chk}, return at +{i_ret}; order pack<check<return: {i_pack < i_chk < i_ret}")
assigns = [l.strip() for l in body if l.strip().startswith("blob") or " blob =" in l or "blob, report =" in l]
print("blob assignments in build_desc_image:", assigns)
main = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "main")
m = ast.get_source_segment(src, main)
srcs = [ast.get_source_segment(src, a).split("\n")[0] for a in ast.walk(main) if isinstance(a, ast.Assign)
        and any("_desc_blob" in ast.unparse(t) for t in a.targets)]
print("main(): assignments binding _desc_blob:", srcs)
print("main(): build_desc_image call precedes CRC32 and write_bytes:",
      m.index("build_desc_image(") < m.index("binascii.crc32(_desc_blob)") < m.index("write_bytes(_desc_blob)"))
