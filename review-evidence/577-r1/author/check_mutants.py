"""Reproduce the #577 removed-refusal campaign without editing the worktree."""
import ast
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path('$LANES/577-image-l6-l10')
sys.path.insert(0, str(ROOT / 'sw/builder'))
import test_builder as test

source = ROOT / 'sw/builder/aem_image_checks.py'
reasons = ['L10_OFFSET', 'L10_COUNT', 'L10_COUNT_EXTENT', 'L10_PARTIAL_WORD',
           'L10_EXTRA_WORDS', 'L6_ORDER', 'L6_GAP', 'L6_DUPLICATE',
           'L10_HEADER', 'L6_HEADER', 'L6_EMPTY', 'L6_EXTENT']
results = []
for reason in reasons:
    tree = ast.parse(source.read_text())
    class RemoveRefusal(ast.NodeTransformer):
        count = 0
        def visit_Raise(self, node):
            if (isinstance(node.exc, ast.Call) and node.exc.args
                    and isinstance(node.exc.args[0], ast.JoinedStr)
                    and isinstance(node.exc.args[0].values[0], ast.Constant)
                    and node.exc.args[0].values[0].value.startswith(reason + ':')):
                self.count += 1
                return ast.copy_location(ast.Pass(), node)
            return node
    removal = RemoveRefusal()
    tree = removal.visit(tree)
    assert removal.count == 1, (reason, removal.count)
    with tempfile.TemporaryDirectory(prefix='milan-577-mutant-') as temporary:
        path = Path(temporary) / 'image_checks_mutant.py'
        path.write_text(ast.unparse(tree))
        spec = importlib.util.spec_from_file_location('image_checks_mutant', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.__file__ = str(source)
        captured = io.StringIO()
        with patch.object(test.eb, 'aem_image_checks', module), contextlib.redirect_stdout(captured):
            try:
                test.test_shipping_image_contract()
            except AssertionError as exc:
                result = dict(reason=reason, verdict='killed', failure=str(exc))
            else:
                raise AssertionError('survived: ' + reason)
        results.append(result)
        print(json.dumps(result), flush=True)
with patch.object(test.eb.aem_image_checks, 'validate_shipping_image', return_value=None):
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            test.test_shipping_image_contract()
        except AssertionError as exc:
            result = dict(reason='emitter hook removed', verdict='killed', failure=str(exc))
        else:
            raise AssertionError('emitter hook removal survived')
results.append(result)
print(json.dumps(result), flush=True)
Path(__file__).with_name('mutants.json').write_text(json.dumps(results, indent=2) + '\n')
