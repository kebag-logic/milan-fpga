"""R221 focused, reproducible probes; only run against exported scratch sources."""
import ast
import contextlib
import copy
import hashlib
import importlib
import io
import itertools
import json
import os
from pathlib import Path
import struct
import sys
import tempfile

root = Path(sys.argv[2]).resolve()
out = Path(sys.argv[3]).resolve()
assert '/scratch/' in str(root), 'Refuse to execute probes in review checkout'
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / 'sw/builder'))
os.chdir(root)
out.mkdir(parents=True, exist_ok=True)
tmp = out / 'tmp'
tmp.mkdir(exist_ok=True)
tempfile.tempdir = str(tmp)
tb = importlib.import_module('test_builder')
eb = tb.eb

NAMES = ['arty_current', 'arty_4x4', 'arty_8ch', 'ax7101_8x8', 'ax7101_1x1_tdm8']
GATES = ['test_audio_unit_rates_loader_contract', 'test_audio_unit_shipping_rates',
         'test_pp_shadow_audio_unit_rates_match_config']


def image_rows():
    rows = {}
    assert sorted(p.name for p in (root / 'configs').glob('endstation_*.yaml')) == sorted(
        'endstation_' + name + '.yaml' for name in NAMES)
    for name in NAMES:
        path = root / 'configs' / ('endstation_' + name + '.yaml')
        cfg = eb.load_config(path)
        blob = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))['aem_desc.bin']
        assert blob[:4] == b'AEMI'
        assert int.from_bytes(blob[4:6], 'big') == 1
        assert sum(struct.unpack_from('>8I', blob)) & 0xffffffff == 0xffffffff
        assert int.from_bytes(blob[20:24], 'big') == len(blob)
        n_entries = int.from_bytes(blob[8:10], 'big')
        index_off = int.from_bytes(blob[12:16], 'big')
        aus = []
        for k in range(n_entries):
            conf, dtype, count, length, pos, names, stride = struct.unpack_from(
                '>HHHHIHH', blob, index_off + 16*k)
            if dtype != 2:
                continue
            for j in range(count):
                desc = blob[pos + j*stride:pos + j*stride + length]
                assert len(desc) == length and int.from_bytes(desc[:2], 'big') == 2
                current, offset, count_rates = struct.unpack_from('>IHH', desc, 136)
                rates = list(struct.unpack_from('>' + str(count_rates) + 'I', desc, offset))
                want = [48000, 96000, 192000] if name == 'arty_current' else [48000]
                assert offset == 144 and length == 144 + 4*count_rates
                assert current == 48000 and current in rates and rates == want
                aus.append({'config': conf, 'index': j, 'length': length, 'offset': offset,
                            'count': count_rates, 'rates': rates, 'current': current})
        assert len(aus) == 1
        (out / (name + '.aem_desc.bin')).write_bytes(blob)
        rows[name] = {'config_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'image_sha256': hashlib.sha256(blob).hexdigest(),
                      'image_bytes': len(blob), 'audio_units': aus}
        print(name, json.dumps(rows[name]))
    (out / 'images.json').write_text(json.dumps(rows, indent=2) + '\n')


def focused():
    for name in GATES:
        print('PRISTINE:', name)
        getattr(tb, name)()
    base = tb.yaml.safe_load((root / 'configs/endstation_arty_current.yaml').read_text())
    checks = 0

    def load(values, current=48000, error=None):
        nonlocal checks
        cfg = copy.deepcopy(base)
        cfg['clocking']['sampling_rate_hz'] = current
        cfg['clocking']['audio_unit_rates_hz'] = values
        before = copy.deepcopy(cfg)
        try:
            got = eb._load_clocking(cfg, 'R221 independent loader probe')
        except eb.ConfigError as exc:
            assert error and error in str(exc), (values, error, str(exc))
        else:
            assert error is None, (values, 'unexpected acceptance')
            assert got['audio_unit_rates_hz'] == [int(x) for x in values]
        assert cfg == before, 'Loader changed the input document'
        checks += 1

    for current in (48000, 96000, 192000):
        others = [x for x in [192000, 96000, 44100, 88200, 176400, 32000, 24000, 48000, 22050]
                  if x != current]
        for n in range(1, 10):
            values = others[:n-1] + [current]
            load(values, current, None if n <= 8 else 'walk bound is 8 (L10')
        for left, right in itertools.combinations(range(8), 2):
            values = others[:7] + [current]
            values[left] = values[right]
            load(values, current, 'duplicate')
    load([48000, '48000'], error='duplicate')
    load([], error='must appear')
    load([96000, 192000], error='must appear')
    load([48000] * 9, error='walk bound is 8 (L10')
    print('INDEPENDENT loader checks:', checks)

    source = (root / 'sw/builder/endstation_builder.py').read_text()
    tree = ast.parse(source)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_load_clocking')
    original_function = eb._load_clocking
    loader_source = ast.get_source_segment(source, fn)
    original_bound = eb.MAX_AUDIO_UNIT_RATES
    mutations = [
        ('bound-nine', None, 9),
        ('bound-seven', None, 7),
        ('no-count-check', loader_source.replace('if len(rates) > MAX_AUDIO_UNIT_RATES:', 'if False:'), 8),
        ('no-duplicate-check', loader_source.replace('if len(set(rates)) != len(rates):', 'if False:'), 8),
        ('no-current-membership', loader_source.replace('if rate not in rates:', 'if False:'), 8),
        ('reverse-order', loader_source.replace('rates = clocking["audio_unit_rates_hz"]',
                                              'rates = clocking["audio_unit_rates_hz"]\n    rates.reverse()'), 8),
        ('wrong-default', loader_source.replace('clk.get("audio_unit_rates_hz", [rate])',
                                               'clk.get("audio_unit_rates_hz", [48000])'), 8),
    ]
    results = []
    for label, changed, bound in mutations:
        try:
            eb.MAX_AUDIO_UNIT_RATES = bound
            if changed:
                assert changed != loader_source
                ns = dict(vars(eb))
                exec(compile(changed, '<R221 ' + label + '>', 'exec'), ns)
                eb._load_clocking = ns['_load_clocking']
            try:
                tb.test_audio_unit_rates_loader_contract()
            except (AssertionError, eb.ConfigError) as exc:
                results.append({'mutation': label, 'detected': True, 'exception': type(exc).__name__, 'message': str(exc)})
                print('DETECTED:', label, type(exc).__name__, str(exc))
            else:
                raise AssertionError('Mutation escaped gate 36a: ' + label)
        finally:
            eb._load_clocking = original_function
            eb.MAX_AUDIO_UNIT_RATES = original_bound

    source_path = root / 'tb/verilator/pp_shadow/sim_main.cpp'
    original_cpp = source_path.read_text()
    assert original_cpp.count('48000u, 96000u, 192000u};') == 1
    plants = [
        ('cpp-value', original_cpp.replace('48000u, 96000u, 192000u};', '48000u, 88200u, 192000u};'), 'values'),
        ('cpp-order', original_cpp.replace('48000u, 96000u, 192000u};', '96000u, 48000u, 192000u};'), 'values'),
        ('cpp-length', original_cpp.replace('uint32_t AU_RATES_C[3]', 'uint32_t AU_RATES_C[4]'), 'declared length'),
        ('cpp-short-initializer', original_cpp.replace('48000u, 96000u, 192000u};', '48000u, 96000u};'), 'values'),
        ('cpp-commented', original_cpp.replace('static constexpr uint32_t AU_RATES_C[3] = {\n        48000u, 96000u, 192000u};',
                                               '/* static constexpr uint32_t AU_RATES_C[3] = {\n        48000u, 96000u, 192000u}; */'), 'declaration'),
    ]
    for label, changed, reason in plants:
        try:
            assert changed != original_cpp
            source_path.write_text(changed)
            try:
                tb.test_pp_shadow_audio_unit_rates_match_config()
            except AssertionError as exc:
                assert reason in str(exc)
                results.append({'mutation': label, 'detected': True, 'message': str(exc)})
                print('DETECTED actual scratch source drift:', label, str(exc))
            else:
                raise AssertionError('Mutation escaped pp_shadow gate: ' + label)
        finally:
            source_path.write_text(original_cpp)

    test_source = (root / 'sw/builder/test_builder.py').read_text()
    test_ast = ast.parse(test_source)
    main = next(n for n in test_ast.body if isinstance(n, ast.If) and ast.unparse(n.test) == "__name__ == '__main__'")
    dispatch = next(n for n in main.body if isinstance(n, ast.For))
    names = [n.id for n in dispatch.iter.elts]
    assert all(names.count(n) == 1 for n in GATES)
    dispatch_code = compile(ast.Module(body=[dispatch], type_ignores=[]), '<unchanged normal-run dispatch>', 'exec')

    # Run the exact main for-loop. Unrelated gates are explicitly stubbed;
    # this is a dispatch/failure-propagation probe, not a full builder pass.
    ns = dict(vars(tb))
    called = []
    for name in names:
        if name not in GATES:
            ns[name] = lambda: None
        else:
            def wrapped(name=name):
                called.append(name)
                getattr(tb, name)()
            ns[name] = wrapped
    with contextlib.redirect_stdout(io.StringIO()):
        exec(dispatch_code, ns)
    assert called == GATES
    pristine_called = called.copy()
    for target in GATES:
        failing = dict(ns)
        def fail():
            raise AssertionError('R221 dispatch sentinel ' + target)
        failing[target] = fail
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(dispatch_code, failing)
        except AssertionError as exc:
            assert str(exc) == 'R221 dispatch sentinel ' + target
        else:
            raise AssertionError('Normal dispatch swallowed failure: ' + target)
    print('NORMAL DISPATCH: all three real gates run; each independent assertion propagates')
    # Establish the explicit downstream boundary without widening it.
    cfg = eb.load_config(root / 'configs/endstation_arty_current.yaml')
    cfg['clocking']['audio_unit_rates_hz'] = [192000, 96000, 44100, 88200, 176400, 32000, 24000, 48000]
    try:
        eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))
    except ValueError as exc:
        assert 'unsupported sampling rates' in str(exc)
        print('EXPECTED downstream image refusal for loader-only fixture:', str(exc))
    else:
        raise AssertionError('Unexpected downstream supported-rate contract change')
    (out / 'focused-results.json').write_text(json.dumps({'loader_checks': checks,
        'mutations': results, 'normal_dispatch_real_gates': pristine_called,
        'normal_dispatch_failure_sentinels': GATES, 'result': 'PASS'}, indent=2) + '\n')
    print('FOCUSED RESULT: PASS')


if sys.argv[1] == 'images':
    image_rows()
elif sys.argv[1] == 'focused':
    focused()
elif sys.argv[1] == 'shipping-builds':
    tb.test_all_configs_build()
    tb.test_builder_doc_key_map()
    print('SHIPPING BUILDS AND SCHEMA MAP: PASS')
else:
    raise SystemExit('mode must be images, focused or shipping-builds')
