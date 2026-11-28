#!/usr/bin/env python3
"""Reviewer mutation probes for src/pbaem.c (round 2: the round-1 probes plus the remaining format fields).

Usage: probe_pbaem.py <clone> <work> <gtest-prefix> [--jobs N]

Each probe replaces one exact source line in a scratch copy of src/pbaem.c,
builds the hosted pbaem and entity test binaries against it, and runs both.
A probe is KILLED when at least one test fails, SURVIVED when both binaries
pass.  The clone is never written.  Output: <work>/probes.json and a table on
stdout.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import subprocess
import sys

PROBES = [
    # name, old, new, note
    ("control-none", None, None, "unmodified source: both binaries must pass"),
    ("name-copy-32", "\tmemcpy(d + 48u, id->name, 64u);", "\tmemcpy(d + 48u, id->name, 32u);",
     "ENTITY entity_name truncated to 32 octets"),
    ("firmware-copy-32", "\tmemcpy(d + 116u, id->firmware, 64u);", "\tmemcpy(d + 116u, id->firmware, 32u);",
     "ENTITY firmware_version truncated to 32 octets"),
    ("group-copy-32", "\tmemcpy(d + 180u, id->group, 64u);", "\tmemcpy(d + 180u, id->group, 32u);",
     "ENTITY group_name truncated to 32 octets"),
    ("serial-copy-32", "\tmemcpy(d + 244u, id->serial, 64u);", "\tmemcpy(d + 244u, id->serial, 32u);",
     "ENTITY serial_number truncated to 32 octets"),
    ("model-id-constant", "\tput(d, 12u, id->model_id, 8u);", "\tput(d, 12u, UINT64_C(0x001bc5c52e47a158), 8u);",
     "ENTITY entity_model_id ignores the caller identity"),
    ("aaf-ignore-samples-per-frame",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~(UINT64_C(0x3ff) << 12)) == (AAF_BASE & ~(UINT64_C(0x3ff) << 12))",
     "AAF input accepts any samples_per_frame (for example 12 at 48 kHz)"),
    ("aaf-ignore-format-field",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~(UINT64_C(0xff) << 40)) == (AAF_BASE & ~(UINT64_C(0xff) << 40))",
     "AAF input accepts any AAF format code (float, 24-bit, 16-bit, AES3)"),
    ("aaf-ignore-bit-depth",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~(UINT64_C(0xff) << 32)) == (AAF_BASE & ~(UINT64_C(0xff) << 32))",
     "AAF input accepts any bit_depth (expected killed by the 24-bit assertion)"),
    ("aaf-ignore-up-to-bit",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~(UINT64_C(1) << 52)) == AAF_BASE",
     "AAF input accepts the up-to family entry (expected killed)"),
    ("aaf-ignore-reserved-low",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~UINT64_C(0xfff)) == AAF_BASE",
     "AAF input accepts nonzero reserved low bits"),
    ("aaf-ignore-subtype",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~(UINT64_C(0xff) << 56)) == (AAF_BASE & ~(UINT64_C(0xff) << 56))",
     "AAF input accepts any version and subtype octet"),
    ("aaf-stream-bound-off-by-one-supported",
     "bool pbaem_input_format_supported(unsigned stream, uint64_t format)\n{\n\tif (stream >= PBAEM_STREAMS) {",
     "bool pbaem_input_format_supported(unsigned stream, uint64_t format)\n{\n\tif (stream > PBAEM_STREAMS) {",
     "stream 5 reaches the AAF check: an AAF format is then supported on an absent input"),
    ("set-format-wrong-stream", "\tmodel->input_formats[stream] = format;", "\tmodel->input_formats[0] = format;",
     "accepted format stored on stream 0 (expected killed)"),
    ("init-keeps-old-state", "\tmemset(model, 0, sizeof *model);\n", "",
     "pbaem_init leaves available_index, clock_source and identify of a reused model"),
    ("init-clock-default", "\tmodel->identity = *identity;", "\tmodel->identity = *identity;\n\tmodel->clock_source = 0u;",
     "equivalent control (expected SURVIVED: no behaviour change)"),
    ("descriptor-not-zeroed", "\tmemset(d, 0, sizeof d);\n", "",
     "descriptor padding left as stack bytes (expected killed)"),
    ("output-format-bound", "uint64_t pbaem_output_format(unsigned stream)\n{\n\tif (stream >= PBAEM_STREAMS) {",
     "uint64_t pbaem_output_format(unsigned stream)\n{\n\tif (stream > PBAEM_STREAMS) {",
     "stream 5 reads past the channel table (expected killed)"),
    ("crf-output-not-sync", "\tput(d, 72u, input || clock ? 3u : 2u, 2u);", "\tput(d, 72u, input ? 3u : 2u, 2u);",
     "CRF output loses CLOCK_SYNC_SOURCE (expected killed)"),
    ("strings-model-name", "\ttext(d, 4u, \"PocketBeagle 2 bridge\");", "\ttext(d, 4u, \"PocketBeagle 2 Bridge\");",
     "STRINGS string 0 changed by one letter (expected killed by the golden only)"),
    ("locale-count", "\tput(d, 68u, 1u, 2u);\n\treturn 72u;", "\tput(d, 68u, 2u, 2u);\n\treturn 72u;",
     "LOCALE number_of_strings 2 (expected killed by the golden only)"),
    # Round-2 additions: the remaining fields of the AAF format word, and controls.
    ("aaf-ignore-reserved-high",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~(UINT64_C(0x7) << 53)) == AAF_BASE",
     "AAF input accepts nonzero reserved bits 53 to 55, beside the up-to bit"),
    ("aaf-ignore-reserved-low-bits-1-to-11",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~UINT64_C(0xffe)) == AAF_BASE",
     "AAF input accepts reserved low bits 1 to 11 (sub-field probe: only bit 0 is asserted)"),
    ("aaf-ignore-version-bit",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~(UINT64_C(1) << 63)) == AAF_BASE",
     "AAF input accepts the vendor/version bit (expected killed)"),
    ("aaf-ignore-rate",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE",
     "\treturn (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~(UINT64_C(0xf) << 48)) == (AAF_BASE & ~(UINT64_C(0xf) << 48))",
     "AAF input accepts any nominal sample rate (expected killed)"),
    ("set-format-unchecked", "\tif (!pbaem_input_format_supported(stream, format)) {", "\tif (stream >= PBAEM_STREAMS) {",
     "pbaem_set_input_format stores any format on a present input (expected killed)"),
    ("init-skips-formats", "\t\tmodel->input_formats[k] = pbaem_default_input_format(k);", "\t\t(void)k;",
     "pbaem_init leaves the input formats zero (expected killed)"),
    ("locale-en-EN", "\ttext(d, 4u, \"en-US\");", "\ttext(d, 4u, \"en-EN\");",
     "LOCALE identifier back to the round-1 value (expected killed by the unit test and the golden)"),
]


def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, **kw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('clone', type=Path)
    parser.add_argument('work', type=Path)
    parser.add_argument('gtest', type=Path)
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
    root, work = args.clone.resolve(), args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    cflags = ['-std=c11', '-Wall', '-Wextra', '-Werror', '-O0', '-g', '-DNDEBUG', '-DCTRL_REENTRY_ASSERT',
              '-I' + str(root / 'include'), '-I' + str(root / 'examples')]
    cxxflags = ['-std=c++20', '-Wall', '-Wextra', '-Werror', '-O0', '-g', '-I' + str(root / 'include'),
                '-I' + str(root / 'examples'), '-isystem', str(args.gtest / 'include'), '-DGTEST_HAS_PTHREAD=1']
    libs = ['-L' + str(args.gtest / 'lib'), '-lgmock', '-lgtest', '-lpthread']
    base = work / 'base'
    base.mkdir(exist_ok=True)
    csrc = ['src/adp.c', 'src/acmp.c', 'src/maap.c', 'examples/entity_roundtrip.c'] + [
        f'examples/entities/{p}/entity_config.c' for p in ('listener', 'talker', 'duplex', 'ax7101', 'pocketbeagle')]
    cobj = []
    for i, s in enumerate(csrc):
        o = base / f'c{i}.o'
        r = run(['gcc', *cflags, '-c', str(root / s), '-o', str(o)])
        if r.returncode:
            sys.exit('baseline C build failed: ' + r.stderr)
        cobj.append(str(o))
    xobj = {}
    for s in ('tests/main.cpp', 'tests/test_pbaem.cpp', 'tests/test_entity.cpp'):
        o = base / (Path(s).stem + '.o')
        r = run(['g++', *cxxflags, '-c', str(root / s), '-o', str(o)])
        if r.returncode:
            sys.exit('baseline C++ build failed: ' + r.stderr)
        xobj[Path(s).stem] = str(o)
    source = (root / 'src/pbaem.c').read_text()

    def probe(item):
        name, old, new, note = item
        d = work / name
        d.mkdir(exist_ok=True)
        text = source
        if old is not None:
            if text.count(old) != 1:
                return {'name': name, 'verdict': 'ERROR', 'detail': f'old text occurs {text.count(old)} times', 'note': note}
            text = text.replace(old, new)
        (d / 'pbaem.c').write_text(text)
        r = run(['gcc', *cflags, '-c', str(d / 'pbaem.c'), '-o', str(d / 'pbaem.o')])
        if r.returncode:
            return {'name': name, 'verdict': 'BUILD-FAIL', 'detail': r.stderr[-400:], 'note': note}
        failed, rcs = [], {}
        # The model binary links the model alone, as the static test library does; the entity binary links every core.
        for binary, objs in (('pbaem_tests', [xobj['test_pbaem']]),
                             ('entity_tests', [xobj['test_entity'], *cobj[3:], *cobj[:3]])):
            exe = d / binary
            r = run(['g++', '-o', str(exe), xobj['main'], *objs, str(d / 'pbaem.o'), *libs])
            if r.returncode:
                return {'name': name, 'verdict': 'LINK-FAIL', 'detail': r.stderr[-400:], 'note': note}
            try:
                r = run([str(exe), '--gtest_color=no'], timeout=120)
            except subprocess.TimeoutExpired:
                rcs[binary] = 'timeout'
                failed.append(binary + ':timeout')
                continue
            (d / (binary + '.log')).write_text(r.stdout + r.stderr)
            rcs[binary] = r.returncode
            failed += sorted(set(re.findall(r'^\[  FAILED  \] (\w+\.\w+)', r.stdout, re.M)))
            if r.returncode and not failed:
                failed.append(binary + ':rc' + str(r.returncode))
        return {'name': name, 'verdict': 'KILLED' if failed else 'SURVIVED', 'failed': failed, 'rc': rcs, 'note': note}

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(probe, PROBES))
    (work / 'probes.json').write_text(json.dumps(results, indent=2) + '\n')
    for r in results:
        print(f"{r['verdict']:10} {r['name']:40} {','.join(r.get('failed', [])) or r.get('detail', '')}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
