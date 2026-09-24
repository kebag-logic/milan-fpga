#!/usr/bin/env python3
"""Measure the lexer spelling corpus with the pinned GCC 14.3 (-std=gnu99):
for each snippet, the `int` names -E keeps with no -D, or None on an error
exit. Prints the corpus as the Python tuple gate 1b embeds."""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

GCC = "$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin/riscv32-linux-gcc"


def c(if_lead, end_lead=None, nl="\n"):
    end_lead = if_lead if end_lead is None else end_lead
    return (f"int a;{nl}{if_lead}ifdef FOO{nl}int b;{nl}{end_lead}endif{nl}"
            f"int z;{nl}")


CORPUS = [
    ("a plain #ifdef", c("#")),
    ("spaces and tabs before #", c(" \t#")),
    ("a form feed before #", c("\f#")),
    ("a vertical tab before #", c("\v#")),
    ("a NUL before #", c("\0#")),
    ("a form feed after #", c("#\f")),
    ("a NUL after #", c("#\0")),
    ("lone CR line ends", c("#", nl="\r")),
    ("CRLF line ends", c("#", nl="\r\n")),
    ("an LF then a CR before #",
     "int a;\n\r#ifdef FOO\n\rint b;\n\r#endif\n\rint z;\n"),
    ("a form feed then a lone CR", "int a;\f\r#ifdef FOO\rint b;\r#endif\r"
     "int z;\n"),
    ("a comment before # on its line", c("/* c */ #")),
    ("a comment and a form feed before #", c("/* c */\f#")),
    ("a multi-line comment closing before #",
     "int a;\n/* c\n c */ #ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a token and a multi-line comment before #",
     "int a; /* c\n c */ #ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a // comment a splice continues over #",
     "int a;\n// c \\\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a // comment a splice with a space continues over #",
     "int a;\n// c \\ \n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a // comment a splice with a form feed continues over #",
     "int a;\n// c \\\f\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a // comment a splice with a vertical tab continues over #",
     "int a;\n// c \\\v\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a // comment a splice with a NUL continues over #",
     "int a;\n// c \\\0\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a // comment a splice with a lone CR continues over #",
     "int a;\n// c \\\r#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a comment opened across a splice",
     "int a;\n/\\\n* c\n#ifdef FOO\n*/\nint b;\nint z;\n"),
    ("a comment closed across a splice before #",
     "int a;\n/* c *\\\n/ #ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a comment whose close a splice splits over #",
     "int a;\n/* c *\\\n#ifdef FOO\n*/\nint b;\nint z;\n"),
    ("a # in a string a splice continues",
     "int a;\nconst char *s = \"a\\\n#ifdef FOO\";\nint b;\nint z;\n"),
    ("a # in a raw string", "int a;\nconst char *s = R\"x(\n#ifdef FOO\n)x\";"
     "\nint b;\nconst char *t = R\"x(\n#endif\n)x\";\nint z;\n"),
    ("a # in a u8 raw string", "int a;\nconst char *s = u8R\"x(\n#ifdef FOO\n"
     ")x\";\nint b;\nint z;\n"),
    ("an unterminated character literal before #",
     "#define Q '\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("an unterminated string before #",
     "#define Q \"\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("an escaped quote ending a line", "const char *s = \"a\\\"\n#ifdef FOO\n"
     "int b;\n#endif\nint z;\n"),
    ("the %: digraph", c("%:")),
    ("the ??= trigraph", c("??=")),
    ("a // comment ending in the ??/ trigraph",
     "int a;\n// c ??/\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a splice inside the directive name",
     "int a;\n#if\\\ndef FOO\nint b;\n#endif\nint z;\n"),
    ("a splice between # and the name",
     "int a;\n#\\\nifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a line holding only a splice before #",
     "int a;\n  \\\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a token and a splice before #",
     "int a; \\\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("## at the start of a line", c("##", "#")),
    ("an FS control before #", c("\x1c#")),
    ("a U+2028 before #", c(" #")),
    ("a no-break space before #", c(" #")),
    ("#elifdef", "#ifdef BAR\nint a;\n#elifdef FOO\nint b;\n#else\nint c;\n"
     "#endif\nint z;\n"),
    ("#elifndef", "#ifdef BAR\nint a;\n#elifndef FOO\nint b;\n#else\nint c;\n"
     "#endif\nint z;\n"),
    ("#else behind a form feed", "#ifdef FOO\nint a;\n\f#else\nint b;\n"
     "#endif\nint z;\n"),
    ("#else behind a lone CR", "#ifdef FOO\rint a;\r#else\rint b;\r#endif\r"
     "int z;\n"),
    ("#else split by a splice", "#ifdef FOO\nint a;\n#el\\\nse\nint b;\n"
     "#endif\nint z;\n"),
    ("#endif split by a splice", "int a;\n#ifdef FOO\nint b;\n#end\\\nif\n"
     "int z;\n"),
    ("#define behind a form feed",
     "\f#define FOO\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("#define behind a NUL",
     "\0#define FOO\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("#define behind a multi-line comment",
     "/* c\n */ #define FOO\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("#define after a token and a multi-line comment",
     "int a; /* c\n */ #define FOO\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("#define split by a splice",
     "#def\\\nine FOO\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("a #define whose name a splice splits",
     "#define F\\\nOO\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("#undef behind a form feed",
     "#define FOO\n\f#undef FOO\n#ifdef FOO\nint b;\n#endif\nint z;\n"),
    ("#undef behind a lone CR",
     "#define FOO\r#undef FOO\r#ifdef FOO\rint b;\r#endif\rint z;\n"),
]


def measure(text):
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "milan_baremetal.c"
        src.write_bytes(text.encode("utf-8"))
        run = subprocess.run([GCC, "-std=gnu99", "-E", str(src)],
                             capture_output=True)
        if run.returncode:
            return None
        out = run.stdout.decode("utf-8", "replace")
    own, keep = [], False
    for line in out.split("\n"):
        marker = re.match(r'^#\s+\d+\s+"([^"]*)"', line)
        if marker:
            keep = Path(marker.group(1)).name == "milan_baremetal.c"
            continue
        if keep:
            own.append(line)
    return tuple(re.findall(r"\bint\s+(\w+)\s*;", "\n".join(own)))


if __name__ == "__main__":
    for label, text in CORPUS:
        print(f"        ({label!r},\n         {text!r},\n"
              f"         {measure(text)!r}),")
    sys.exit(0)
