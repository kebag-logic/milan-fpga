#!/usr/bin/env bash
# Which line spellings the pinned RV32 GCC treats as a preprocessing directive.
# Usage: cpp_directive_check.sh <sdk-dir> <out-dir>
set -u
cc="$1/bin/riscv32-linux-gcc"
out=$2
mkdir -p "$out"
cd "$out" || exit 2
"$cc" --version | head -n 1 > cpp-version.txt
printf 'int a;\n\f#ifdef FOO\nint b;\n\f#endif\n\v#ifdef FOO\nint c;\n\v#endif\nint d;\n' > ff-vt.c
printf 'int a;\n\000#ifdef FOO\nint b;\n\000#endif\nint c;\n' > nul.c
printf 'int a;\n#\fifdef FOO\nint b;\n#endif\nint c;\n' > ff-after-hash.c
printf 'int a;\n#ifdef FOO\nint b;\n#elifdef BAR\nint c;\n#else\nint d;\n#endif\n' > elifdef.c
printf 'int a;\r#ifdef FOO\rint b;\r#endif\rint c; // x\rint d;\n' > lone-cr.c
printf '#define R 0x604u\n\f#undef R\n#define R 0x600u\nint x = R;\n' > ff-undef.c
printf '#define R 0x600u\n_Pragma("push_macro(\\"R\\")")\n#define R 0x604u\n_Pragma("pop_macro(\\"R\\")")\nint x = R;\n' > pragma-pop.c
{
  for f in ff-vt.c nul.c ff-after-hash.c elifdef.c lone-cr.c ff-undef.c pragma-pop.c; do
    for def in "" "-DFOO" "-DBAR"; do
      echo "== $f ${def:-(no -D)}"
      "$cc" -std=gnu99 -E -P $def "$f" 2>/dev/null
      echo "exit=$?"
    done
  done
} > cpp-results.txt
cat cpp-results.txt
