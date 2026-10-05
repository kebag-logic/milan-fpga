#!/usr/bin/env python3
"""Prove the default-off SoC source reduces to the merged dev parent's AST."""
import argparse
import ast
from pathlib import Path
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--base', default='510fae60b26bef1db138de5cf2ac72b17b5011a5')
args = ap.parse_args()
repo = args.repo.resolve()
def git(*words):
    return subprocess.check_output(['git', *words], cwd=repo)

head = ast.parse((repo / 'sw/litex/milan_soc.py').read_text())
base = ast.parse(git('show', args.base + ':sw/litex/milan_soc.py'))
changes = []

class DefaultOff(ast.NodeTransformer):
    def visit_Module(self, node):
        out = []
        for item in node.body:
            if isinstance(item, (ast.ClassDef, ast.FunctionDef)) and item.name in {
                    'CtrlMailbox', 'ctrl_mailbox_contract', 'add_ctrl_mailbox'}:
                changes.append('unused definition ' + item.name)
                continue
            if isinstance(item, ast.Assign) and len(item.targets) == 1 and isinstance(item.targets[0], ast.Name) and item.targets[0].id in {'CTRL_MBX_BASE', '_CTRL_MAILBOX_SOURCES'}:
                changes.append('inert mailbox constant ' + item.targets[0].id)
                continue
            out.append(item)
        node.body = out
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        names = [a.arg for a in node.args.args]
        if 'ctrl_mailbox' in names:
            i = names.index('ctrl_mailbox')
            j = i - (len(names) - len(node.args.defaults))
            assert j >= 0 and isinstance(node.args.defaults[j], ast.Constant) and node.args.defaults[j].value is False
            del node.args.args[i]
            del node.args.defaults[j]
            changes.append('default-false constructor argument')
        return self.generic_visit(node)

    def visit_If(self, node):
        if isinstance(node.test, ast.Name) and node.test.id == 'ctrl_mailbox':
            assert not node.orelse
            assert ast.unparse(node.body[0]) == 'add_ctrl_mailbox(self, platform, sys_clk_freq)'
            assert len(node.body) == 1
            changes.append('disabled instance/source/region/CSR/IRQ call')
            return None
        return self.generic_visit(node)

    def visit_Expr(self, node):
        call = node.value
        if isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute) and call.func.attr == 'add_argument' and call.args and isinstance(call.args[0], ast.Constant) and call.args[0].value == '--ctrl-mailbox':
            assert next(k.value.value for k in call.keywords if k.arg == 'action') == 'store_true'
            assert not any(k.arg == 'default' and not (isinstance(k.value, ast.Constant) and k.value.value is False) for k in call.keywords)
            changes.append('default-off CLI argument')
            return None
        return self.generic_visit(node)

    def visit_Call(self, node):
        kept = []
        for kw in node.keywords:
            if kw.arg == 'ctrl_mailbox':
                assert ast.unparse(kw.value) == 'args.ctrl_mailbox'
                changes.append('default-false CLI-to-constructor argument')
            else:
                kept.append(kw)
        node.keywords = kept
        return self.generic_visit(node)

reduced = DefaultOff().visit(head)
assert len(changes) == 9, changes
assert ast.dump(reduced, include_attributes=False) == ast.dump(base, include_attributes=False)
print('PASS: exact AST equality after specializing only the explicit default-off additions')
for change in changes:
    print('  ' + change)
for path in ['configs', 'sw/builder', 'avdecc', 'sw/firmware/milan_baremetal', 'protocol-processor', 'gptp-processor', 'third_party/verilog-axis']:
    a = git('rev-parse', args.base + ':' + path).decode().strip()
    b = git('rev-parse', 'HEAD:' + path).decode().strip()
    assert a == b, path
    print(f'PASS: {path} exact object identity {a}')
print('This source proof is not an independently executed netlist export or hardware build.')
