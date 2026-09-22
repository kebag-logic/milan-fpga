"""Focused source tests only; invoked in an isolated exported source tree."""
import ast
import copy
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import re
import struct
import sys

root, out, mode = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
out.mkdir(parents=True, exist_ok=True)
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / 'sw/builder'))
import test_builder as tb
eb = tb.eb
results = []

def record(name, **kw):
    results.append(dict(name=name, **kw))
    (out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')

if mode == 'focused':
    gates = ['test_audio_unit_rates_loader_contract',
             'test_audio_unit_shipping_rates',
             'test_pp_shadow_audio_unit_rates_match_config']
    for name in gates + ['test_all_configs_build', 'test_builder_doc_key_map']:
        getattr(tb, name)()
        record(name, passed=True)

    base = tb.yaml.safe_load(tb.CONFIGS['arty_current'].read_text())
    extra = [192000, 96000, 44100, 88200, 176400, 32000, 24000]
    checks = 0
    for n in range(1, 9):
        for position in range(n):
            values = extra[:n - 1]
            values.insert(position, 48000)
            cfg = copy.deepcopy(base)
            cfg['clocking']['audio_unit_rates_hz'] = [str(v) for v in values]
            assert eb._load_clocking(cfg, 'R221')['audio_unit_rates_hz'] == values
            checks += 1
    for pos in range(9):
        values = extra + [22050]
        values.insert(pos, 48000)
        cfg = copy.deepcopy(base)
        cfg['clocking']['audio_unit_rates_hz'] = values
        try:
            eb._load_clocking(cfg, 'R221')
        except eb.ConfigError as exc:
            assert all(s in str(exc) for s in ('9 entries', '8', 'walk', 'L10'))
        else:
            raise AssertionError('accepted distinct ninth')
        checks += 1
    for values in ([48000, '48000'], [48000, 48000.0], [48000, '048000'],
                   [96000, 48000, '96000']):
        cfg = copy.deepcopy(base)
        cfg['clocking']['audio_unit_rates_hz'] = values
        try:
            eb._load_clocking(cfg, 'R221')
        except eb.ConfigError as exc:
            assert 'duplicate' in str(exc)
        else:
            raise AssertionError('accepted converted duplicate')
        checks += 1
    record('independent loader positions and normalized duplicates', checks=checks)

    original = eb._load_clocking
    source = inspect.getsource(original)
    mutations = {
        'max nine': ('len(rates) > MAX_AUDIO_UNIT_RATES', 'len(rates) > 9'),
        'max seven': ('len(rates) > MAX_AUDIO_UNIT_RATES', 'len(rates) > 7'),
        'missing count refusal': ('len(rates) > MAX_AUDIO_UNIT_RATES', 'False'),
        'missing duplicate refusal': ('len(set(rates)) != len(rates)', 'False'),
        'missing membership refusal': ('if rate not in rates:', 'if False:'),
        'reverse order': ('rates = clocking["audio_unit_rates_hz"]',
                          'clocking["audio_unit_rates_hz"].reverse()\n    rates = clocking["audio_unit_rates_hz"]'),
        'wrong default': ('clk.get("audio_unit_rates_hz", [rate])',
                          'clk.get("audio_unit_rates_hz", [48000])'),
    }
    for name, (old, new) in mutations.items():
        assert source.count(old) == 1, name
        namespace = dict(eb.__dict__)
        exec(compile(source.replace(old, new), '<R221 loader mutation>', 'exec'), namespace)
        eb._load_clocking = namespace['_load_clocking']
        try:
            try:
                tb.test_audio_unit_rates_loader_contract()
            except (AssertionError, eb.ConfigError) as exc:
                record(name, caught=True, exception=type(exc).__name__, detail=str(exc))
            else:
                raise AssertionError('surviving loader mutation: ' + name)
        finally:
            eb._load_clocking = original

    cpp = root / 'tb/verilator/pp_shadow/sim_main.cpp'
    original_cpp = cpp.read_text()
    match = re.search(r'static constexpr uint32_t AU_RATES_C\[3\] = \{\s*48000u, 96000u, 192000u\};', original_cpp)
    assert match
    decl = match.group()
    cpp_mutations = {
        'actual value drift': decl.replace('96000u', '88200u'),
        'actual order drift': decl.replace('48000u, 96000u', '96000u, 48000u'),
        'actual length drift': decl.replace('[3]', '[4]'),
        'actual initializer drift': decl.replace(', 192000u', ''),
        'actual commented declaration': '/*' + decl + '*/',
        'actual duplicate declaration': decl + '\n' + decl,
    }
    try:
        for name, mutant in cpp_mutations.items():
            cpp.write_text(original_cpp[:match.start()] + mutant + original_cpp[match.end():])
            try:
                tb.test_pp_shadow_audio_unit_rates_match_config()
            except AssertionError as exc:
                record(name, caught=True, detail=str(exc))
            else:
                raise AssertionError('surviving actual C++ mutation: ' + name)
    finally:
        cpp.write_text(original_cpp)
    tb.test_pp_shadow_audio_unit_rates_match_config()

    cfg = copy.deepcopy(base)
    eight = [192000, 96000, 44100, 88200, 176400, 32000, 24000, 48000]
    cfg['clocking']['audio_unit_rates_hz'] = eight
    assert eb._load_clocking(cfg, 'R221')['audio_unit_rates_hz'] == eight
    path = root / 'configs/r221-eight.yaml'
    path.write_text(tb.yaml.safe_dump(cfg))
    try:
        try:
            model = eb.load_config(path)
            eb._entity_model_image(model, eb.emit_aem_overlay(model))
        except (ValueError, eb.ConfigError) as exc:
            assert 'unsupported sampling rates' in str(exc), str(exc)
            record('eight loader entries are not an eight-rate image claim', detail=str(exc))
        else:
            raise AssertionError('unexpected eight-rate image acceptance')
    finally:
        path.unlink()

    # Execute the exact main dispatch loop with unrelated gates stubbed.
    # Only gate 36a runs, and assertion sentinels must escape the loop.
    parsed = ast.parse((root / 'sw/builder/test_builder.py').read_text())
    main = next(n for n in parsed.body if isinstance(n, ast.If)
                and '__name__' in ast.unparse(n.test))
    loop = next(n for n in main.body if isinstance(n, ast.For)
                and isinstance(n.iter, ast.Tuple) and len(n.iter.elts) > 3)
    names = [n.id for n in loop.iter.elts]
    assert all(name in names for name in gates)
    compiled = compile(ast.Module(body=[loop], type_ignores=[]), '<exact main loop>', 'exec')
    seen = []
    ns = {name: (lambda: None) for name in names}
    def wrap(name):
        def call():
            seen.append(name)
            getattr(tb, name)()
        call.__name__ = name
        return call
    for name in gates:
        ns[name] = wrap(name)
    exec(compiled, ns)
    assert seen == gates
    for victim in gates:
        ns = {name: (lambda: None) for name in names}
        def sentinel():
            raise AssertionError('R221 dispatch sentinel')
        ns[victim] = sentinel
        try:
            exec(compiled, ns)
        except AssertionError as exc:
            assert str(exc) == 'R221 dispatch sentinel'
        else:
            raise AssertionError('dispatch suppressed assertion')
    record('exact dispatch loop', gates_seen=seen, sentinel_failures_propagated=3,
           unrelated_gates='explicitly stubbed; not full-suite evidence')

# Independently decode the packed descriptor output, not the test helper.
images = {}
for name, path in tb.CONFIGS.items():
    cfg = eb.load_config(path)
    blob = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))['aem_desc.bin']
    u16 = lambda offset: int.from_bytes(blob[offset:offset+2], 'big')
    u32 = lambda offset: int.from_bytes(blob[offset:offset+4], 'big')
    assert blob[:4] == b'AEMI' and u16(4) == 1
    assert u32(20) == len(blob)
    assert sum(u32(i) for i in range(0, 32, 4)) & 0xffffffff == 0xffffffff
    rows = []
    for k in range(u16(8)):
        off = u32(12) + k * 16
        if u16(off) == 0 and u16(off + 2) == 2:
            rows.append(off)
    assert len(rows) == 1
    row = rows[0]
    assert u16(row + 4) == 1
    start, length = u32(row + 8), u16(row + 6)
    desc = blob[start:start + length]
    assert len(desc) == length and desc[:4] == b'\x00\x02\x00\x00'
    rate_offset = int.from_bytes(desc[140:142], 'big')
    count = int.from_bytes(desc[142:144], 'big')
    current = int.from_bytes(desc[136:140], 'big')
    expected = [48000, 96000, 192000] if name == 'arty_current' else [48000]
    rates = [int.from_bytes(desc[144+4*k:148+4*k], 'big') for k in range(count)]
    assert rate_offset == 144 and count == len(expected) and length == 144 + 4 * count
    assert rates == expected and current == 48000
    (out / (name + '.bin')).write_bytes(blob)
    images[name] = dict(config_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                        image_sha256=hashlib.sha256(blob).hexdigest(), image_bytes=len(blob),
                        audio_unit_bytes=length, rates=rates, current=current, offset=rate_offset)
(out / 'images.json').write_text(json.dumps(images, indent=2) + '\n')
print(json.dumps(images, indent=2))
