#!/usr/bin/env python3
"""Compile independent comment controls and compare their scanner result."""
import argparse,importlib.util,json,pathlib,subprocess,sys,shutil
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--work',type=pathlib.Path,required=True);a=ap.parse_args();a.work.mkdir(parents=True,exist_ok=True);sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('gate',a.repo/'scripts/check_comments.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
rows=[]
cases={
 'asm-double-quote-character': ('.S',True,'.text\n.globl example\nexample:\n    li a0, \'" # narrative "\n    ret\n'),
 'asm-define-double-quote-character': ('.S',True,'#define VALUE \'" # narrative "\n.text\n.globl example\nexample:\n    li a0, VALUE\n    ret\n'),
 'cpp-digit-prose':('.cpp',True,"int a=1'000; // narrative\nint b=2'000;\n"),
 'cpp-hex-prose':('.cpp',True,"int a=0xA'B; // narrative\nint b=0xC'D;\n"),
 'cpp-zero-hex':('.cpp',True,'#if (0x00ULL)\nnarrative\n#endif\nint a;\n'),
 'cpp-zero-binary':('.cpp',True,"#if 0b0'0\nnarrative\n#endif\nint a;\n"),
 'cpp-elif-false':('.cpp',True,'#if 1\nint a;\n#elif false\nnarrative\n#endif\n'),
 'asm-define-prose':('.S',True,'#define VALUE 4 # narrative\n.text\n.word VALUE\n'),
 'cpp-tracing':('.cpp',False,"int a=1'000; // REQ: PORT-01\nchar b='\\\''; // IEEE 1722-2016 Figure 5\n"),
 'asm-tracing':('.S',False,'.text\nli a0, \'A # REQ: PORT-01\n'),
 'cpp-zero-plus':('.cpp',True,'#if +0\nnarrative\n#endif\nint a;\n'),
 'cpp-zero-minus':('.cpp',True,'#if -0\nnarrative\n#endif\nint a;\n'),
}
for name,(suffix,refuse,source) in cases.items():
 path=a.work/(name+suffix);path.write_text(source);out=a.work/(name+'.o')
 cmd=([shutil.which('riscv64-unknown-elf-gcc') or shutil.which('riscv64-elf-gcc'),'-march=rv32i','-mabi=ilp32'] if suffix=='.S' else ['g++','-std=c++20'])+['-Wall','-Wextra','-Werror','-c',str(path),'-o',str(out)]
 result=subprocess.run(cmd,capture_output=True,text=True)
 errors=gate.check(source,suffix=='.S')
 row={'name':name,'source':source,'compile_rc':result.returncode,'compiler_output':result.stdout+result.stderr,'expected_refusal':refuse,'scanner_errors':errors,'gap':result.returncode==0 and refuse and not errors};rows.append(row);print(json.dumps(row))
(a.work/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
