"""Run the declaration controls, record cases, and kill three historical mutants."""
from pathlib import Path
import contextlib
import hashlib
import inspect
import io
import json
import sys
from unittest.mock import patch

ROOT = Path("$LANES/595-yaml-int-refusal")
OUT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "sw/builder"))
import test_declarations as checks
import endstation_builder as eb
import yaml

TESTS = (checks.test_station_mac_string_contract,
         checks.test_declared_hex_string_contract,
         checks.test_formats_list_contract)
active = []
rows = []
real_template, real_load = checks._yaml_template, eb.load_config


def template(raw, keys):
    active[:] = keys
    return real_template(raw, keys)


def measured_load(path):
    text = Path(path).read_text()
    node = yaml.compose(text)
    field = ""
    for key in active:
        field += f"[{key}]" if isinstance(key, int) else ("." if field else "") + key
        if node is None:
            continue
        if isinstance(key, int):
            node = node.value[key]
        else:
            node = next((value for name, value in node.value if name.value == key), None)
    spelling = "<omitted>" if node is None else text[node.start_mark.index:node.end_mark.index]
    row = dict(field=field, input=spelling)
    try:
        cfg = real_load(path)
    except eb.ConfigError as exc:
        row.update(message=str(exc), resolved=None)
        rows.append(row)
        raise
    if active[0] == "platform":
        resolved = cfg["platform"]["mac_address"]
    elif active[-1] == "vendor_oui":
        resolved = f"0x{int(cfg['entity']['entity_model_id'],16) >> 40:06X}"
    elif active[-1] == "entity_capabilities":
        blob = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))["aem_desc.bin"]
        directory = int.from_bytes(blob[12:16], "big")
        offset = int.from_bytes(blob[directory + 8:directory + 12], "big")
        resolved = f"0x{int.from_bytes(blob[offset + 20:offset + 24], 'big'):08X}"
    else:
        resolved = cfg[active[1]][active[2]]["formats"]
    row.update(message="accepted", resolved=resolved)
    rows.append(row)
    return cfg


with patch.object(checks, "_yaml_template", template), patch.object(eb, "load_config", measured_load):
    for test in TESTS:
        test()
(OUT / "cases.json").write_text(json.dumps(rows, indent=2) + "\n")

source = Path(eb.__file__)
before = hashlib.sha256(source.read_bytes()).hexdigest()
guard = ('    if not isinstance(v, str):\n'
         '        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n')
mac = inspect.getsource(eb._mac48)
assert mac.count(guard) == 1
mac = mac.replace(guard, "").replace('s = v.replace', 's = str(v).replace')
uint = inspect.getsource(eb._declared_uint)
assert uint.count(guard) == 1
uint = uint.replace(guard, '    if isinstance(v, bool) or not isinstance(v, (int, str)):\n'
                          '        raise ConfigError(f"{ctx}: {v!r} is not an integer")\n')
uint = uint.replace('n = int(v, 16)', 'n = v if isinstance(v, int) else int(v, 16)')
streams = inspect.getsource(eb._streams)
old = ('        fmts = s.get("formats", [])\n'
       '        if not isinstance(fmts, list):\n'
       '            raise ConfigError(f"{sctx}.formats: must be a list of quoted hexadecimal strings")\n'
       '        fmts = fmts or [f"0x{aaf_pcm32(ch, rate_hz):016X}"]')
assert streams.count(old) == 1
streams = streams.replace(old, '        fmts = s.get("formats") or [f"0x{aaf_pcm32(ch, rate_hz):016X}"]')
mutants = []
for name, function, text, test in (
        ("MAC integer decimal-text reread as hex", "_mac48", mac, TESTS[0]),
        ("Declared uint accepts integers", "_declared_uint", uint, TESTS[1]),
        ("Scalar formats iterates or defaults", "_streams", streams, TESTS[2])):
    namespace = dict(eb.__dict__)
    # Only the inspected local function and the exact substitutions above run.
    exec(compile(text, f"<mutant {function}>", "exec"), namespace)
    with patch.object(eb, function, namespace[function]):
        try:
            test()
        except AssertionError as exc:
            frames = []
            tb = exc.__traceback__
            while tb is not None:
                frames.append(f"{Path(tb.tb_frame.f_code.co_filename).name}:{tb.tb_lineno} "
                              f"{tb.tb_frame.f_code.co_name}")
                tb = tb.tb_next
            mutants.append(dict(name=name, test=test.__name__, result="KILLED",
                                assertion=frames[-1], diagnostic=str(exc)))
        else:
            raise AssertionError(f"surviving mutant: {name}")
    test()
assert hashlib.sha256(source.read_bytes()).hexdigest() == before
(OUT / "mutants.json").write_text(json.dumps(mutants, indent=2) + "\n")
print(f"{len(rows)} loader cases recorded; {len(mutants)}/3 mutants killed; restored controls pass")
for row in mutants:
    print(row)
