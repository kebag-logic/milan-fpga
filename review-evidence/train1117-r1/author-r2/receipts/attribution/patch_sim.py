#!/usr/bin/env python3
"""patch_sim.py SIM_MAIN: a scratch-only measurement aid, never committed. With BUDGET_INSTR set, the testbench also
writes <script>.instr: for each traced span 'S <start cpu> <cycles> <committed instructions> <name>', for each traced
call 'C <cpu> <committed instructions so far> <name>'. The log it prints is unchanged, byte for byte, and nothing
the simulation does depends on the file, so every cycle figure is the unpatched testbench's. Idempotent."""
import sys
from pathlib import Path

p = Path(sys.argv[1])
s = p.read_text()
if 'instr_out_' in s:
    print('already patched'); sys.exit(0)
EDITS = [
    ('struct OpenSpan { bool active; std::uint32_t ret; std::uint64_t sys, cpu; };',
     'struct OpenSpan { bool active; std::uint32_t ret; std::uint64_t sys, cpu, instr; };\n'
     '    std::FILE* instr_out_ = nullptr;'),
    ('open = {true, prev_pc + 4u, sys_, cpu_};', 'open = {true, prev_pc + 4u, sys_, cpu_, instr_};'),
    ('open.ret - 4u, span_name[s]);',
     'open.ret - 4u, span_name[s]);\n'
     '                if (instr_out_) std::fprintf(instr_out_, "S %llu %llu %llu %s\\n", ull(open.cpu), '
     'ull(cpu_ - open.cpu), ull(instr_ - open.instr), span_name[s]);'),
    ('if (last_pc_ == call_pc[c]) std::printf("CALL %llu %llu %s\\n", ull(sys_), ull(cpu_), call_name[c]);',
     'if (last_pc_ == call_pc[c]) {\n'
     '                std::printf("CALL %llu %llu %s\\n", ull(sys_), ull(cpu_), call_name[c]);\n'
     '                if (instr_out_) std::fprintf(instr_out_, "C %llu %llu %s\\n", ull(cpu_), ull(instr_), call_name[c]);\n'
     '            }'),
    ('Bench(const char* script, const char* flash_image) : flash_(0, 0) {',
     'Bench(const char* script, const char* flash_image) : flash_(0, 0) {\n'
     '        if (std::getenv("BUDGET_INSTR")) instr_out_ = std::fopen((std::string(script) + ".instr").c_str(), "w");'),
]
for old, new in EDITS:
    assert s.count(old) == 1, f'anchor not unique: {old}'
    s = s.replace(old, new)
p.write_text(s)
print('patched', p)
