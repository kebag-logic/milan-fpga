#!/usr/bin/env python3
"""pma_sweep.py <netlist.v> <regions.json> <workdir> [--args 0bNNN]: an exhaustive, simulator-evaluated check of
a VexiiRiscv netlist's fetch and load PMA fault terms at every one of the 2^32 addresses.

Independent of tb/verilator/ctrl_region_decode/decode.py: no mask-bit reasoning and no expression evaluator of
its own. It copies each fault term's combinational cone (every continuous assign it reaches, with the netlist's
own declarations) verbatim into a small module, compiles it with Verilator, and evaluates the compiled model at
every 32-bit address. The admitted addresses are printed as [start, end) spans and compared with the regions of
the port's mode (x for a fetch, r for a load) from regions.json ([[origin, size, mode, bus], ...]).
Exit 0 when both ports are exact, 1 when one is not, 2 on a cone it cannot extract.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

PORTS = {
    'fetch': ('FetchL1Plugin_logic_ctrl_pmaPort_rsp_fault', 'FetchL1Plugin_pmaBuilder_addressBits', None, 'x'),
    'load': ('LsuCachelessPlugin_logic_onPma_port_rsp_fault', 'LsuCachelessPlugin_pmaBuilder_addressBits',
             'LsuCachelessPlugin_pmaBuilder_argsBits', 'r'),
}
#: Address chunks evaluated in parallel.
JOBS = 16
IDENT = re.compile(r"(?<!')\b([A-Za-z_]\w*)\b")


def cone(text, signal, free):
    assigns = dict(re.findall(r'^\s*assign (\w+) = (.*);\s*$', text, re.M))
    decls = {m.group(3): m.group(0).strip() for m in
             re.finditer(r'^\s*(wire|reg)\s+(\[\d+:\d+\]\s+)?(\w+)\s*;', text, re.M)}
    order, todo, seen = [], [signal], set()
    while todo:
        name = todo.pop()
        if name in seen or name in free:
            continue
        seen.add(name)
        if name not in assigns:
            raise SystemExit(f'cone: {name} has no one-line continuous assign')
        order.append(name)
        for ref in IDENT.findall(re.sub(r"\d+'[bhd][0-9a-fA-F_]+", ' ', assigns[name])):
            todo.append(ref)
    return order, assigns, decls


def width(decl):
    m = re.search(r'\[(\d+):(\d+)\]', decl)
    return int(m.group(1)) - int(m.group(2)) + 1 if m else 1


def main():
    netlist, regions_path, work = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]).resolve()
    args_value = int(sys.argv[sys.argv.index('--args') + 1], 0) if '--args' in sys.argv else 0b100
    text = netlist.read_text()
    regions = json.loads(regions_path.read_text())
    work.mkdir(parents=True, exist_ok=True)
    ok_all = True
    for port, (signal, address, argument, mode) in PORTS.items():
        free = {address, *([argument] if argument else [])}
        order, assigns, decls = cone(text, signal, free)
        aw = width(decls[address])
        lines = ['module pma_cone(', f'  input wire [{aw - 1}:0] {address},']
        if argument:
            lines.append(f'  input wire [{width(decls[argument]) - 1}:0] {argument},')
        lines += [f'  output wire fault_o', ');']
        lines += ['  ' + decls[n].replace('reg ', 'wire ', 1) for n in order]
        lines += [f'  assign {n} = {assigns[n]};' for n in order]
        lines += [f'  assign fault_o = {signal};', 'endmodule']
        d = work / port
        d.mkdir(exist_ok=True)
        (d / 'pma_cone.v').write_text('\n'.join(lines) + '\n')
        drive = f'm.{argument} = {args_value};' if argument else ''
        (d / 'sweep.cpp').write_text(f'''#include "Vpma_cone.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
int main(int argc, char** argv) {{
    const std::uint64_t lo = std::strtoull(argv[1], nullptr, 0), hi = std::strtoull(argv[2], nullptr, 0);
    Vpma_cone m;
    {drive}
    bool in = false;
    std::uint64_t start = 0, admitted = 0;
    for (std::uint64_t a = lo; a < hi; ++a) {{
        m.{address} = static_cast<std::uint32_t>(a);
        m.eval();
        const bool ok = !m.fault_o;
        admitted += ok;
        if (ok && !in) {{ start = a; in = true; }}
        if (!ok && in) {{ std::printf("SPAN %08llx %09llx\\n", (unsigned long long)start, (unsigned long long)a); in = false; }}
    }}
    if (in) std::printf("SPAN %08llx %09llx\\n", (unsigned long long)start, (unsigned long long)hi);
    std::printf("ADMITTED %llu\\n", (unsigned long long)admitted);
    return 0;
}}
''')
        subprocess.run(['verilator', '--cc', '--exe', '--build', '-O3', '-Wno-fatal', '-Wno-WIDTH', '--top-module',
                        'pma_cone', '-CFLAGS', '-O2', '--Mdir', str(d / 'obj'), 'pma_cone.v', 'sweep.cpp', '-j', '1'],
                       cwd=d, check=True, stdout=(d / 'build.log').open('w'), stderr=subprocess.STDOUT)
        chunk = (1 << 32) // JOBS
        procs = [subprocess.Popen([str(d / 'obj/Vpma_cone'), str(i * chunk), str((i + 1) * chunk)],
                                  stdout=subprocess.PIPE, text=True) for i in range(JOBS)]
        outs = [p.communicate()[0] for p in procs]
        if any(p.returncode for p in procs):
            raise SystemExit('a sweep chunk failed')
        out = ''.join(outs)
        (d / 'sweep.out').write_text(out)
        spans = []
        for _, a, b in (ln.split() for ln in out.splitlines() if ln.startswith('SPAN')):
            a, b = int(a, 16), int(b, 16)
            if spans and spans[-1][1] == a:      # a span cut at a chunk boundary
                spans[-1] = (spans[-1][0], b)
            else:
                spans.append((a, b))
        want = sorted((o, o + s) for o, s, m, *_ in regions if mode in m)
        merged = []
        for a, b in want:
            if merged and a <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        ok = spans == merged
        ok_all &= ok
        print(f'PMA-SWEEP {"PASS" if ok else "FAIL"} {port}: {len(order)} assigns in its cone; 2^32 addresses '
              f'evaluated; admits {", ".join(f"[0x{a:08x}, 0x{b:08x})" for a, b in spans)}; wants the {mode} '
              f'regions {", ".join(f"[0x{a:08x}, 0x{b:08x})" for a, b in merged)}')
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
