"""Ask the pinned GCC 14.3 at -std=gnu99 -E what it keeps of small texts."""
import re, subprocess, sys, tempfile, os
from pathlib import Path
GCC = os.path.expanduser("~/br-milan-rv32/host/bin/riscv32-linux-gcc")
cases = {
 "dollar after #if in skipped": "#ifdef NEVER\n#if$a\n#endif\nint b;\n#ifdef N2\n#endif$b\n#endif\nint z;\n",
 "ucn after #if in skipped": "#ifdef NEVER\n#if\\u0061\n#endif\nint b;\n#ifdef N2\n#endif\\u0062\n#endif\nint z;\n",
 "utf8 ident after #if in skipped": "#ifdef NEVER\n#ifé\n#endif\nint b;\n#ifdef N2\n#endifé\n#endif\nint z;\n",
 "has_include angled comment": "int a;\n#if !__has_include(<x/*y>)\nint b; // */\n#endif\nint z;\n",
 "include_next angled comment skipped": "int a;\n#ifdef NEVER\n#include_next <x/*y>\n#endif\nint b; // */\nint z;\n",
 "import angled comment skipped": "int a;\n#ifdef NEVER\n#import <x/*y>\n#endif\nint b; // */\nint z;\n",
 "include angled comment skipped": "int a;\n#ifdef NEVER\n#include <x/*y>\n#endif\nint b; // */\nint z;\n",
 "include second angled skipped": "int a;\n#ifdef NEVER\n#include <a.h> <x/*y>\n#endif\nint b; // */\nint z;\n",
 "include macro then angled skipped": "int a;\n#ifdef NEVER\n#include H <x/*y>\n#endif\nint b; // */\nint z;\n",
 "include quoted backslash skipped": "int a;\n#ifdef NEVER\n#include \"a\\\" /* \"\n#endif\nint b; // */\nint z;\n",
 "digraph <% %>": "int a;\nint f(void) <% return 0; %>\nint z;\n",
 "at sign in skipped #if": "#ifdef NEVER\n#if@x\n#endif\nint b;\n#endif\nint z;\n",
 "pragma in skipped with angled": "int a;\n#ifdef NEVER\n#pragma GCC dependency <x/*y>\n#endif\nint b; // */\nint z;\n",
 "ucn in pp-number": "#define X 1\\u00e9\nint z;\n",
 "dollar ident": "int a$b;\nint z;\n",
}
with tempfile.TemporaryDirectory() as tmp:
    for label, text in cases.items():
        f = Path(tmp) / "t.c"
        f.write_bytes(text.encode())
        r = subprocess.run([GCC, "-std=gnu99", "-E", "-P", str(f)], capture_output=True, text=True, errors="replace")
        kept = re.findall(r"\bint\s+([\w$]+)", r.stdout)
        err = [l for l in r.stderr.splitlines() if "error" in l or "warning" in l][:2]
        print(f"{label!r}: rc={r.returncode} kept={kept} {err}")
