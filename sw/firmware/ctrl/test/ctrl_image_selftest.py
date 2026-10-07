#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_image_selftest.py - the controls of the linked image's checks (#665, R531-3-F1 and R530-3-F1).

ctrl_image.py links the composed app with no library, its arithmetic helpers
from rv32_image/image_arith.c, and refuses an image that is not RV32I with the
soft-float ILP32 ABI. Each part of that is shown to hold and to fail:

  arith    image_arith.c compiled for the host and checked against the host's
           own arithmetic: every helper at the edges (0, 1, the 32- and
           64-bit sign and carry boundaries, every shift count) and on 200,000
           pseudo-random operand pairs of every length;
  leaves   the helpers' RV32I object defines exactly fw_rv32.HELPERS, leaves
           nothing open and calls no helper; a helper written with `*` (GCC
           lowers it into a call to that helper) and one calling out are
           refused;
  audit    a probe linked as ctrl_image.py links passes, and so does every
           RV32I base instruction form; refused by name: a word of M (mul,
           divu), C, Zifencei, Zicsr, A, F, the privileged set, a 6-bit shift
           and an all-zero word; an object built for RV32IM (the attribute
           alone); each e_flags bit, another machine, a relocatable file, a
           64-bit or big-endian file; a weak symbol left undefined;
  measure  ctrl_image.measure() at the shipping shape: passes as shipped; with
           the helpers taken from a library built for RV32IM with the
           soft-float ABI (as another toolchain's libgcc can be), refused by
           the audit; from one built for the pinned SDK's own multilib
           (rv32imafd, ilp32d), refused at the link; with a helper that calls
           itself, refused by the leaf check.

Usage:
    python3 sw/firmware/ctrl/test/ctrl_image_selftest.py [--require-rv32]

Exit 0 = every control passed (or, without --require-rv32, SKIPPED for want of
an RV32 compiler); 1 = a control failed; 2 = refused.
"""

from __future__ import annotations

import argparse
import struct
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import ctrl_image  # noqa: E402
import fw_gtest  # noqa: E402
import fw_rv32  # noqa: E402
from ctrl_build import RV32_FLAGS, Refusal  # noqa: E402

SHIPPING = ctrl_image.SHAPES[0]
FIRMWARE = ctrl_image.ROOT / "sw/firmware"
START = ctrl_image.IMAGE / "image_start.S"
SCRIPT = ctrl_image.IMAGE / "image.ld"
ASM_FLAGS = ("-march=rv32i", "-mabi=ilp32")

ARITH_CHECK = r"""#include <stdint.h>
#include <stdio.h>

uint32_t __mulsi3(uint32_t a, uint32_t b);
int32_t __divsi3(int32_t a, int32_t b);
int32_t __modsi3(int32_t a, int32_t b);
uint32_t __udivsi3(uint32_t a, uint32_t b);
uint32_t __umodsi3(uint32_t a, uint32_t b);
int64_t __muldi3(int64_t a, int64_t b);
int64_t __divdi3(int64_t a, int64_t b);
int64_t __moddi3(int64_t a, int64_t b);
uint64_t __udivdi3(uint64_t a, uint64_t b);
uint64_t __umoddi3(uint64_t a, uint64_t b);
int64_t __lshrdi3(int64_t a, int b);
int64_t __ashldi3(int64_t a, int b);
int64_t __ashrdi3(int64_t a, int b);

static unsigned failures;
static uint64_t state = 0x9e3779b97f4a7c15u;

static uint64_t next(void)
{
	state ^= state << 13;
	state ^= state >> 7;
	state ^= state << 17;
	return state;
}

static void check(const char *name, uint64_t x, uint64_t y, uint64_t got, uint64_t want)
{
	if (got != want && failures++ < 8u) {
		printf("MISMATCH %s(%016llx, %016llx): %016llx, not %016llx\n", name, (unsigned long long)x,
		       (unsigned long long)y, (unsigned long long)got, (unsigned long long)want);
	}
}

static void pair(uint64_t x, uint64_t y)
{
	uint32_t a = (uint32_t)x, b = (uint32_t)y;
	int32_t sa = (int32_t)a, sb = (int32_t)b;
	int64_t sx = (int64_t)x, sy = (int64_t)y;
	int s = (int)(y & 63u);
	check("__mulsi3", x, y, __mulsi3(a, b), (uint32_t)(a * b));
	check("__muldi3", x, y, (uint64_t)__muldi3(sx, sy), x * y);
	if (b != 0u) {
		check("__udivsi3", x, y, __udivsi3(a, b), a / b);
		check("__umodsi3", x, y, __umodsi3(a, b), a % b);
		if (!(sa == INT32_MIN && sb == -1)) {
			check("__divsi3", x, y, (uint32_t)__divsi3(sa, sb), (uint32_t)(sa / sb));
			check("__modsi3", x, y, (uint32_t)__modsi3(sa, sb), (uint32_t)(sa % sb));
		}
	}
	if (y != 0u) {
		check("__udivdi3", x, y, __udivdi3(x, y), x / y);
		check("__umoddi3", x, y, __umoddi3(x, y), x % y);
		if (!(sx == INT64_MIN && sy == -1)) {
			check("__divdi3", x, y, (uint64_t)__divdi3(sx, sy), (uint64_t)(sx / sy));
			check("__moddi3", x, y, (uint64_t)__moddi3(sx, sy), (uint64_t)(sx % sy));
		}
	}
	check("__lshrdi3", x, y, (uint64_t)__lshrdi3(sx, s), x >> s);
	check("__ashldi3", x, y, (uint64_t)__ashldi3(sx, s), x << s);
	check("__ashrdi3", x, y, (uint64_t)__ashrdi3(sx, s), (uint64_t)(sx >> s));
}

int main(void)
{
	static const uint64_t edge[] = {
		0u, 1u, 2u, 3u, 7u, 0x7fu, 0x80u, 0xffu, 0x7fffffffu, 0x80000000u, 0x80000001u, 0xfffffffeu,
		0xffffffffu, 0x100000000u, 0x100000001u, 0x1ffffffffu, 0x7fffffffffffffffu, 0x8000000000000000u,
		0x8000000000000001u, 0xffffffff00000000u, 0xffffffff80000000u, 0xfffffffffffffffeu,
		0xffffffffffffffffu, 0x0123456789abcdefu,
	};
	unsigned n = (unsigned)(sizeof edge / sizeof edge[0]);
	for (unsigned i = 0u; i < n; ++i) {
		for (unsigned j = 0u; j < n; ++j) {
			pair(edge[i], edge[j]);
		}
		for (uint64_t s = 0u; s < 64u; ++s) {
			pair(edge[i], s);
		}
	}
	for (unsigned k = 0u; k < 200000u; ++k) {
		uint64_t x = next() >> (next() & 63u);
		uint64_t y = next() >> (next() & 63u);
		pair(x, y);
	}
	printf("%u mismatches\n", failures);
	return failures != 0u;
}
"""

# An incompatible library's helpers: what they compute does not matter, only the
# instructions and the ABI they are built with.
BAD_LIBRARY = """#include <stdint.h>
uint32_t __mulsi3(uint32_t a, uint32_t b) { return a * b; }
uint32_t __udivsi3(uint32_t a, uint32_t b) { return a / b; }
uint32_t __umodsi3(uint32_t a, uint32_t b) { return a % b; }
int32_t __divsi3(int32_t a, int32_t b) { return a / b; }
int32_t __modsi3(int32_t a, int32_t b) { return a % b; }
int64_t __muldi3(int64_t a, int64_t b) { return a * b; }
uint64_t __udivdi3(uint64_t a, uint64_t b) { return (uint32_t)a / (uint32_t)b; }
uint64_t __umoddi3(uint64_t a, uint64_t b) { return (uint32_t)a % (uint32_t)b; }
int64_t __divdi3(int64_t a, int64_t b) { return (int32_t)a / (int32_t)b; }
int64_t __moddi3(int64_t a, int64_t b) { return (int32_t)a % (int32_t)b; }
int64_t __lshrdi3(int64_t a, int b) { return (uint32_t)a >> (b & 31); }
int64_t __ashldi3(int64_t a, int b) { return (uint32_t)a << (b & 31); }
int64_t __ashrdi3(int64_t a, int b) { return (int32_t)a >> (b & 31); }
"""

# Reaches __lshrdi3, __udivdi3, __muldi3 and __mulsi3, as the composition does.
PROBE = """#include <stdint.h>
volatile uint64_t image_probe_x = 0x0123456789abcdefu;
volatile uint32_t image_probe_n = 7u;
int main(void);
int main(void)
{
	uint64_t x = image_probe_x;
	uint32_t n = image_probe_n;
	image_probe_x = (x >> n) + x / n + x * x + (uint64_t)(n * n);
	return 0;
}
"""

# Every RV32I base instruction form, assembled for RV32I alone.
EVERY_FORM = """	.section .text.start, "ax"
	.global _start
_start:
	lui a0, 1
	auipc a0, 0
	jal ra, 1f
1:	jalr zero, 0(ra)
	beq a0, a1, 2f
	bne a0, a1, 2f
	blt a0, a1, 2f
	bge a0, a1, 2f
	bltu a0, a1, 2f
	bgeu a0, a1, 2f
2:	lb a0, 0(sp)
	lh a0, 0(sp)
	lw a0, 0(sp)
	lbu a0, 0(sp)
	lhu a0, 0(sp)
	sb a0, 0(sp)
	sh a0, 0(sp)
	sw a0, 0(sp)
	addi a0, a0, 1
	slti a0, a0, 1
	sltiu a0, a0, 1
	xori a0, a0, 1
	ori a0, a0, 1
	andi a0, a0, 1
	slli a0, a0, 31
	srli a0, a0, 31
	srai a0, a0, 31
	add a0, a0, a1
	sub a0, a0, a1
	sll a0, a0, a1
	slt a0, a0, a1
	sltu a0, a0, a1
	xor a0, a0, a1
	srl a0, a0, a1
	sra a0, a0, a1
	or a0, a0, a1
	and a0, a0, a1
	fence
	ecall
	ebreak
"""

#: __mulsi3's loop, and the plant that writes it with `*`: GCC lowers that into a call to __mulsi3, from itself.
MULSI3_LOOP = ("\tuint32_t p = 0u;\n\twhile (b != 0u) {\n\t\tp += a & image_mask(b & 1u);\n\t\ta <<= 1;\n"
               "\t\tb >>= 1;\n\t}\n")
MULSI3_STAR = "\treturn a * b;\n"

#: Words no RV32I image holds, each refused by the instruction check alone.
FOREIGN_WORDS = (("mul a0, a0, a1 (M)", 0x02B50533), ("divu a0, a4, a2 (M)", 0x02C75533),
                 ("c.nop, c.nop (C)", 0x00010001), ("fence.i (Zifencei)", 0x0000100F),
                 ("csrrs a0, cycle, zero (Zicsr)", 0xC0002573), ("amoadd.w a0, a1, (a0) (A)", 0x00B5252F),
                 ("flw fa0, 0(a0) (F)", 0x00052507), ("fadd.s fa0, fa0, fa1 (F)", 0x00B57553),
                 ("wfi (privileged)", 0x10500073), ("slli a0, a0, 32 (a 6-bit shift)", 0x02051513),
                 ("an all-zero word", 0x00000000))

#: Header fields set to what an RV32I ILP32 executable never has: (what, offset, format, value, words refused by).
FOREIGN_HEADERS = (("RVC", 36, "<I", 0x1, "RVC"), ("single-float ABI", 36, "<I", 0x2, "hardware-float"),
                   ("double-float ABI", 36, "<I", 0x4, "hardware-float"), ("RVE", 36, "<I", 0x8, "RVE"),
                   ("Ztso", 36, "<I", 0x10, "Ztso"), ("an unnamed e_flags bit", 36, "<I", 0x20, "does not set"),
                   ("x86-64 machine", 18, "<H", 62, "not RISC-V"), ("relocatable", 16, "<H", 1, "not an executable"),
                   ("64-bit class", 4, "B", 2, "not a little-endian ELF32"),
                   ("big-endian", 5, "B", 2, "not a little-endian ELF32"))


def rv32_object(cc: str, src: Path, obj: Path, flags: tuple[str, ...] = RV32_FLAGS) -> Path:
    """One source compiled as ctrl_image.py compiles the composition."""
    obj.parent.mkdir(parents=True, exist_ok=True)
    ctrl_image.run([cc, *flags, *ctrl_image.IMAGE_FLAGS, *fw_rv32.includes(cc), "-c", str(src), "-o", str(obj)])
    return obj


def audit_probe(cc: str, elf: Path, objs: list[Path]) -> tuple[list[str], str]:
    """Objects linked as ctrl_image.py links the composition, and the audit of the image and its inputs."""
    ctrl_image.run([cc, *ctrl_image.LINK_FLAGS, "-T", str(SCRIPT), *map(str, objs), "-o", str(elf)])
    return ctrl_image.audit(cc.removesuffix("gcc"), elf, [str(o) for o in objs])


def written(path: Path, text: str) -> Path:
    """`text` written to `path`, its directory made."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def planted(work: Path, name: str, old: str, new: str) -> Path:
    """A copy of the helpers with `old` replaced by `new` once; the plant must find `old`."""
    text = ctrl_image.HELPERS.read_text(encoding="utf-8")
    assert text.count(old) == 1, f"{name}: the plant's text is not in {ctrl_image.HELPERS.name} once"
    return written(work / name / ctrl_image.HELPERS.name, text.replace(old, new))


def arith_cases(work: Path) -> int:
    """The helpers, compiled for the host, against the host's own arithmetic."""
    exe = work / "arith_check"
    src = written(work / "arith_check.c", ARITH_CHECK)
    ctrl_image.run([fw_gtest.Build().cc, "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic", str(src),
                    str(ctrl_image.HELPERS), "-o", str(exe)])
    res = fw_gtest.run([str(exe)])
    assert res.returncode == 0 and res.stdout.strip().endswith("0 mismatches"), res.stdout
    print(f"PASS: arith: every helper against the host's arithmetic, {res.stdout.strip()}")
    return 1


def leaf_cases(cc: str, work: Path) -> int:
    """The helpers' object is a set of leaves defining fw_rv32.HELPERS; a call to a helper or out is refused."""
    tool = cc.removesuffix("gcc")
    obj = rv32_object(cc, ctrl_image.HELPERS, work / "arith.o")
    assert not ctrl_image.helper_findings(tool, obj), ctrl_image.helper_findings(tool, obj)
    defined = {n for n, (t, _) in ctrl_image.symbol_sizes(tool, obj).items() if t == "T"}
    assert defined == fw_rv32.HELPERS, sorted(defined ^ fw_rv32.HELPERS)
    print("PASS: leaves: the helpers define fw_rv32.HELPERS, leave nothing open and call no helper")
    for name, old, new, needle in (
            ("mulsi3-star", MULSI3_LOOP + "\treturn p;\n", MULSI3_STAR, "calls helpers: __mulsi3"),
            ("udivsi3-out", "\tuint32_t r;\n\treturn image_udivmod32(a, b, &r);",
             "\tuint32_t image_elsewhere(uint32_t, uint32_t);\n\treturn image_elsewhere(a, b);",
             "leaves symbols open: image_elsewhere")):
        bad = rv32_object(cc, planted(work, name, old, new), work / f"{name}.o")
        found = ctrl_image.helper_findings(tool, bad)
        assert any(needle in f for f in found), (name, found)
        print(f"PASS: leaves: refused {name}: {'; '.join(found)}")
    return 3


def probe_cases(cc: str, work: Path) -> int:
    """The probe as linked passes; every RV32I form passes; an RV32IM object and a weak hole are refused."""
    start = rv32_object(cc, START, work / "start.o", ASM_FLAGS)
    probe = rv32_object(cc, written(work / "probe.c", PROBE), work / "probe.o")
    arith = rv32_object(cc, ctrl_image.HELPERS, work / "arith.o")
    found, line = audit_probe(cc, work / "clean.elf", [start, probe, arith])
    assert not found and line.startswith("RV32I audit: e_flags 0, rv32i"), (found, line)
    print(f"PASS: audit: the probe linked as the image is passes ({line})")
    forms = rv32_object(cc, written(work / "forms.S", EVERY_FORM), work / "forms.o", ASM_FLAGS)
    found, _ = audit_probe(cc, work / "forms.elf", [forms])
    assert not found, found
    print("PASS: audit: every RV32I base instruction form passes")
    rv32im = rv32_object(cc, written(work / "rv32im.c", "int image_probe_id(int v);\nint image_probe_id(int v)\n"
                                     "{\n\treturn v;\n}\n"), work / "rv32im.o", ("-march=rv32im", "-mabi=ilp32"))
    found, _ = audit_probe(cc, work / "rv32im.elf", [start, probe, arith, rv32im])
    assert len(found) == 1 and "architecture attribute" in found[0] and "_m2p0" in found[0], found
    print(f"PASS: audit: refused an RV32IM object with no M instruction: {found[0]}")
    weak = written(work / "weak.c", "extern void image_probe_hook(void) __attribute__((weak));\nint main(void);\n"
                   "int main(void)\n{\n\tif (image_probe_hook) {\n\t\timage_probe_hook();\n\t}\n\treturn 0;\n}\n")
    found, _ = audit_probe(cc, work / "weak.elf", [start, rv32_object(cc, weak, work / "weak.o")])
    assert found == ["symbols left undefined: image_probe_hook"], found
    print(f"PASS: audit: refused a weak symbol left undefined: {found[0]}")
    return 4


def word_cases(cc: str, work: Path) -> int:
    """Each foreign word, alone in an image whose attribute and header are RV32I's, is refused by its value."""
    for i, (name, word) in enumerate(FOREIGN_WORDS):
        src = written(work / f"word{i}.S", f'\t.section .text.start, "ax"\n\t.global _start\n_start:\n'
                                           f"\taddi a0, a0, 1\n\t.word {word:#010x}\n")
        found, _ = audit_probe(cc, work / f"word{i}.elf", [rv32_object(cc, src, work / f"word{i}.o", ASM_FLAGS)])
        assert len(found) == 1 and f"1 words outside RV32I, the first {word:#010x}" in found[0], (name, found)
        print(f"PASS: audit: refused {name}: {found[0]}")
    return len(FOREIGN_WORDS)


def header_cases(cc: str, work: Path) -> int:
    """The clean probe with one header field changed is refused for that field."""
    tool = cc.removesuffix("gcc")
    data = (work / "clean.elf").read_bytes()
    for i, (name, offset, fmt, value, needle) in enumerate(FOREIGN_HEADERS):
        changed = bytearray(data)
        struct.pack_into(fmt, changed, offset, value)
        elf = work / f"header{i}.elf"
        elf.write_bytes(bytes(changed))
        found, _ = ctrl_image.audit(tool, elf, [])
        assert any(needle in f for f in found), (name, found)
        print(f"PASS: audit: refused {name}: {'; '.join(found)}")
    return len(FOREIGN_HEADERS)


def bad_library(cc: str, work: Path, march: str, mabi: str) -> Path:
    """BAD_LIBRARY built for `march` and `mabi`, as an archive."""
    obj = work / "bad.o"
    ctrl_image.run([cc, f"-march={march}", f"-mabi={mabi}", "-ffreestanding", "-Os", "-std=c11", "-Wall", "-Werror",
                    *fw_rv32.includes(cc), "-c", str(written(work / "bad.c", BAD_LIBRARY)), "-o", str(obj)])
    lib = work / "libbad.a"
    ctrl_image.run([cc.removesuffix("gcc") + "ar", "rcs", str(lib), str(obj)])
    return lib


def refusal(cc: str, work: Path, what: str, needles: tuple[str, ...]) -> str:
    """The measurement at the shipping shape, which must refuse naming every needle: the refusal's line that
    names the last needle, from its last path separator on."""
    try:
        ctrl_image.measure(cc, FIRMWARE, SHIPPING, work)
    except Refusal as exc:
        text = str(exc)
        assert all(n in text for n in needles), (what, text)
        return next(line for line in text.splitlines() if needles[-1] in line).rsplit("/", 1)[-1]
    raise AssertionError(f"{what} was measured")


def measure_cases(cc: str, work: Path) -> int:
    """The measurement itself, at the shipping shape: passes as shipped, refuses each incompatible helper set."""
    image = ctrl_image.measure(cc, FIRMWARE, SHIPPING, work / "shipped")
    assert image.audited.startswith("RV32I audit") and image.helpers, image
    print(f"PASS: measure: {SHIPPING} as shipped ({image.audited})")
    none = written(work / "none" / "no_helpers.c", "int image_no_helpers(void);\nint image_no_helpers(void)\n"
                                                   "{\n\treturn 0;\n}\n")
    for what, march, mabi, needles in (
            ("an RV32IM soft-float library", "rv32im", "ilp32", ("not RV32I ILP32", "words outside RV32I")),
            ("a library of the pinned SDK's multilib (rv32imafd, ilp32d)", "rv32imafd", "ilp32d",
             ("double-float",))):
        lib = bad_library(cc, work / march, march, mabi)
        with patch.object(ctrl_image, "HELPERS", none), patch.object(ctrl_image, "LIBRARIES", (str(lib),)):
            print(f"PASS: measure: refused {what}: {refusal(cc, work / f'measure-{march}', what, needles)}")
    recursive = planted(work, "mulsi3-star", MULSI3_LOOP + "\treturn p;\n", MULSI3_STAR)
    with patch.object(ctrl_image, "HELPERS", recursive):
        found = refusal(cc, work / "measure-recursive", "a helper that calls itself", ("calls helpers: __mulsi3",))
    print(f"PASS: measure: refused a helper that calls itself: {found}")
    return 4


def main(argv: list[str] | None = None) -> int:
    """Run every control; any failure is an AssertionError."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--require-rv32", action="store_true", help="refuse, not skip, when no RV32 compiler is found")
    ap.add_argument("--out", type=Path, help="keep the probes here (default: a temporary directory)")
    args = ap.parse_args(argv)
    cc = fw_rv32.compiler()
    if cc is None:
        print("REFUSED: no RV32 compiler" if args.require_rv32 else "SKIPPED: no RV32 compiler")
        return 2 if args.require_rv32 else 0
    print(f"compiler: {cc}, {ctrl_image.identity(cc)}")
    with tempfile.TemporaryDirectory(prefix="ctrl-image-selftest-") as tmp:
        work = args.out.resolve() if args.out else Path(tmp)
        try:
            checks = (arith_cases(work / "arith") + leaf_cases(cc, work / "leaves") +
                      probe_cases(cc, work / "audit") + word_cases(cc, work / "audit") +
                      header_cases(cc, work / "audit") + measure_cases(cc, work / "measure"))
        except Refusal as exc:
            print(f"REFUSED: {exc}")
            return 2
    print(f"ctrl_image self-test: {checks} checks PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
