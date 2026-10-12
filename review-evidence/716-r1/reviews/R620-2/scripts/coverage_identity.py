#!/usr/bin/env python3
"""Coverage path identity, dev 09c7231e vs head: AST of the driver's coverage()
and the --coverage early return, plus byte identity of fw_coverage.py and every file
under sw/firmware/gtest. Usage: coverage_identity.py CLONE DEV HEAD"""
import ast, subprocess, sys
clone, dev, head = sys.argv[1:4]
def show(sha, path):
    return subprocess.run(["git", "-C", clone, "show", f"{sha}:{path}"], check=True, capture_output=True, text=True).stdout
D = "sw/firmware/ctrl/test/test_ctrl_firmware.py"
def fn(src, name):
    return next(ast.dump(n) for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == name)
cov_equal = fn(show(dev, D), "coverage") == fn(show(head, D), "coverage")
early = all("if args.coverage is not None:\n        return coverage(args.coverage.resolve(), args.lwsrp, args.jobs)" in show(s, D) for s in (dev, head))
tree_diff = subprocess.run(["git", "-C", clone, "diff", "--name-only", dev, head, "--", "sw/firmware/gtest", "sw/firmware/ctrl_nvm", "sw/firmware/ctrl/README.md"], capture_output=True, text=True, check=True).stdout.split()
print({"coverage_function_ast_equal": cov_equal, "coverage_early_return_both": early, "gtest_nvm_readme_changed_files": tree_diff})
raise SystemExit(0 if cov_equal and early and not tree_diff else 1)
