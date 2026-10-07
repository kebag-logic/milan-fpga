#!/usr/bin/env python3
"""Independent linked RV32 image of the composed ctrl_app (reviewer probe).

Usage: link_image.py <repo> <rev> <work> <out.json> [--cc riscv64-elf-gcc]

For <rev> (exported with git archive into <work>/<rev>), every
configs/endstation_*.yaml and both mailbox interface counts (the committed
one-interface contract and gen_mailbox.py --variant-interfaces 2), this:
  * generates the ADP entity header with the tree's own adp_entity.py;
  * compiles the tree's own PORTABLE set (read from ctrl_build.py) plus
    plat/mbx_plat_mmio.c with its RV32_FLAGS (minus -fstack-usage) plus
    -ffunction-sections -fdata-sections, against the gate's freestanding
    include set;
  * compiles a reviewer-written entry that calls ctrl_app_start_maap with
    maap_csr_allocation (or ctrl_app_start when the tree has no MAAP) and then
    ctrl_loop_run, with static app/arena/CSR context;
  * links a static executable with a reviewer linker script, --gc-sections,
    -nostdlib, newlib libc.a and libgcc.a for rv32i/ilp32, and a 4 KiB NOLOAD
    stack; an unresolved symbol fails the link;
  * records section sizes, selected symbol sizes and proof the MAAP code is
    linked (symbol presence) in <out.json>.
This is a size measurement, not a bootable board image.
"""
import argparse, hashlib, io, json, re, subprocess, sys, tarfile
from pathlib import Path

LD = """ENTRY(_start)
MEMORY { RAM (rwx) : ORIGIN = 0x00000000, LENGTH = 1M }
SECTIONS {
  .text : { KEEP(*(.text.start)) *(.text .text.*) } > RAM
  .rodata : { *(.rodata .rodata.* .srodata .srodata.*) } > RAM
  .data : { *(.data .data.* .sdata .sdata.*) } > RAM
  .bss (NOLOAD) : { *(.bss .bss.* .sbss .sbss.* COMMON) } > RAM
  .stack (NOLOAD) : ALIGN(16) { . += 4096; __stack_top = .; } > RAM
  /DISCARD/ : { *(.comment) *(.note*) *(.riscv.attributes) }
}
"""

ENTRY = r"""
#include <stdint.h>
#include <stddef.h>
#include "ctrl_app.h"
#ifdef WITH_MAAP
#include "maap_csr.h"
#endif
__attribute__((naked, section(".text.start"))) void _start(void)
{
	__asm__ volatile("la sp, __stack_top\n call ctrl_main\n 1: j 1b\n");
}
static const struct adp_entity entity = ADP_ENTITY_GEN_INIT;
static const struct ctrl_pool_class classes[] = {{16u, 1u}};
static uint64_t arena[8];
static struct ctrl_app app;
#ifdef WITH_MAAP
static struct maap_csr csr;
static uint32_t csr_read(void *ctx, unsigned i, uint32_t off)
{
	(void)ctx;
	return *(volatile uint32_t *)(uintptr_t)(0x90000000u + i * 0x10000u + off);
}
static void csr_write(void *ctx, unsigned i, uint32_t off, uint32_t v)
{
	(void)ctx;
	*(volatile uint32_t *)(uintptr_t)(0x90000000u + i * 0x10000u + off) = v;
}
#endif
void ctrl_main(void);
void ctrl_main(void)
{
	struct ctrl_app_config cfg = {&entity, 0u, arena, sizeof arena, classes, 1u, NULL, NULL};
#ifdef WITH_MAAP
	struct maap_csr_port port = {NULL, csr_read, csr_write};
	unsigned aaf = entity.talker_stream_sources > 0u ? entity.talker_stream_sources - 1u : 0u;
	if (maap_csr_init(&csr, port, aaf, true, 1u, 1u) &&
	    ctrl_app_start_maap(&app, &cfg, maap_csr_allocation, &csr, 0u)) {
		ctrl_loop_run(&app.loop);
	}
#else
	if (ctrl_app_start(&app, &cfg)) {
		ctrl_loop_run(&app.loop);
	}
#endif
	for (;;) {
	}
}
"""


def run(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode:
        raise SystemExit(f"FAILED: {' '.join(map(str, cmd))}\n{r.stdout}\n{r.stderr}")
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo"); ap.add_argument("rev"); ap.add_argument("work"); ap.add_argument("out")
    ap.add_argument("--cc", default="riscv64-elf-gcc")
    ap.add_argument("--debug", action="store_true",
                    help="drop -DNDEBUG (assertions on); a link failure is recorded, not fatal")
    a = ap.parse_args()
    work = Path(a.work).resolve() / a.rev
    tree = work / "tree"
    if not tree.exists():
        tree.mkdir(parents=True)
        data = subprocess.run(["git", "-C", a.repo, "archive", a.rev], check=True, capture_output=True).stdout
        tarfile.open(fileobj=io.BytesIO(data)).extractall(tree, filter="data")
        # git archive leaves submodules empty; the generators read them. Link the
        # repo's checkouts after proving the gitlink equals the checked-out HEAD.
        for sub in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
            pin = subprocess.run(["git", "-C", a.repo, "ls-tree", a.rev, sub], check=True, capture_output=True,
                                 text=True).stdout.split()[2]
            head = subprocess.run(["git", "-C", str(Path(a.repo) / sub), "rev-parse", "HEAD"], check=True,
                                  capture_output=True, text=True).stdout.strip()
            if pin != head:
                raise SystemExit(f"{sub}: checkout {head} is not the pin {pin} of {a.rev}")
            (tree / sub).rmdir()
            (tree / sub).symlink_to(Path(a.repo).resolve() / sub)
    ctrl = tree / "sw/firmware/ctrl"
    build_src = (ctrl / "test/ctrl_build.py").read_text()
    portable = re.findall(r'"([a-z_]+/[a-z_0-9]+\.c)"', build_src.split("PORTABLE", 1)[1].split(")", 1)[0])
    rv32_flags = re.findall(r'"([^"]+)"', build_src.split("RV32_FLAGS", 1)[1].split(")", 1)[0])
    rv32_flags = [f for f in rv32_flags if f != "-fstack-usage"]
    # Release profile for every measured tree (dev's RV32_FLAGS keep assertions).
    if a.debug:
        rv32_flags = [f for f in rv32_flags if f != "-DNDEBUG"]
    elif "-DNDEBUG" not in rv32_flags:
        rv32_flags.append("-DNDEBUG")
    inc_dirs = re.findall(r'"([a-z_]+)"', build_src.split("INCLUDE_DIRS", 1)[1].split(")", 1)[0])
    has_maap = "maap/maap.c" in portable
    gcc_inc = run([a.cc, "-march=rv32i", "-mabi=ilp32", "-print-file-name=include"]).strip()
    incs = ["-nostdinc", "-isystem", gcc_inc, "-I", tree / "sw/firmware/gtest/rv32_include"]
    incs += [x for d in inc_dirs for x in ("-I", ctrl / d)]
    libdir = Path(run([a.cc, "-march=rv32i", "-mabi=ilp32", "-print-file-name=libc.a"]).strip()).parent
    libgcc = run([a.cc, "-march=rv32i", "-mabi=ilp32", "-print-libgcc-file-name"]).strip()
    (work / "link.ld").write_text(LD)
    (work / "entry.c").write_text(ENTRY)
    results = {"rev": a.rev, "cc": run([a.cc, "--version"]).splitlines()[0], "portable": portable,
               "rv32_flags": rv32_flags, "has_maap": has_maap, "libc": str(libdir / "libc.a"),
               "libgcc": libgcc, "images": []}
    for n_if in (1, 2):
        extra = []
        if n_if == 2:
            gen = work / "gen_if2"
            run([sys.executable, tree / "sw/mailbox/gen_mailbox.py", "--variant-interfaces", "2", "--out", gen])
            extra = [f"-include{gen / 'mbx_contract.h'}"]
        for cfg in sorted((tree / "configs").glob("endstation_*.yaml")):
            tag = f"if{n_if}_{cfg.stem}"
            od = work / tag
            od.mkdir(exist_ok=True)
            ent = od / "entity.h"
            run([sys.executable, ctrl / "adp/adp_entity.py", cfg, "-o", ent])
            flags = [*rv32_flags, "-ffunction-sections", "-fdata-sections", *incs, *extra]
            objs = []
            for src in portable + ["plat/mbx_plat_mmio.c"]:
                o = od / (src.replace("/", "_") + ".o")
                run([a.cc, *flags, "-c", ctrl / src, "-o", o])
                objs.append(o)
            eo = od / "entry.o"
            run([a.cc, *flags, f"-include{ent}", *(["-DWITH_MAAP"] if has_maap else []),
                 "-c", work / "entry.c", "-o", eo])
            elf = od / "ctrl_app.elf"
            link = [a.cc, "-march=rv32i", "-mabi=ilp32", "-nostdlib", "-static", "-T", work / "link.ld",
                 "-Wl,--gc-sections", "-Wl,--no-undefined", f"-Wl,-Map={od / 'ctrl_app.map'}",
                 eo, *objs, libdir / "libc.a", libgcc, "-o", elf]
            if a.debug:
                r = subprocess.run([str(c) for c in link], capture_output=True, text=True)
                results["images"].append({"config": cfg.name, "interfaces": n_if, "debug_link_rc": r.returncode,
                                          "undefined_references": sorted(set(re.findall(r"undefined reference to `([^']+)'", r.stderr)))})
                print(f"{a.rev[:8]} debug if{n_if} {cfg.name}: link rc {r.returncode} undefined "
                      f"{results['images'][-1]['undefined_references']}")
                continue
            run(link)
            tool = a.cc.removesuffix("gcc")
            sec = {}
            for line in run([tool + "size", "-A", elf]).splitlines():
                p = line.split()
                if len(p) >= 2 and p[0].startswith(".") and p[1].isdigit():
                    sec[p[0]] = int(p[1])
            nm = run([tool + "nm", "-S", "--size-sort", elf])
            syms = {}
            for line in nm.splitlines():
                p = line.split()
                if len(p) == 4:
                    syms[p[3]] = int(p[1], 16)
            und = [l for l in run([tool + "nm", "-u", elf]).splitlines() if l.strip()]
            want = ["app", "csr", "ctrl_app_start", "ctrl_app_start_maap", "maap_mbx_init", "maap_csr_allocation",
                    "ctrl_loop_run", "vsnprintf", "_vfprintf_r", "memset", "memcpy"]
            results["images"].append({
                "config": cfg.name, "interfaces": n_if, "sections": sec,
                "sum_text_rodata_data_bss": sum(sec.get(k, 0) for k in (".text", ".rodata", ".data", ".bss")),
                "stack_reserve": sec.get(".stack", 0), "undefined": und,
                "symbols": {k: syms.get(k) for k in want},
                "maap_symbols_linked": sorted(k for k in syms if k.startswith("maap_")),
                "elf_bytes": elf.stat().st_size, "elf_sha256": hashlib.sha256(elf.read_bytes()).hexdigest(),
                "talker_stream_sources": re.search(r"talker_stream_sources = (0x[0-9A-F]+)u", ent.read_text()).group(1),
            })
    Path(a.out).write_text(json.dumps(results, indent=1) + "\n")
    for im in results["images"]:
        if "sections" not in im:
            continue
        s = im["sections"]
        print(f"{a.rev[:8]} if{im['interfaces']} {im['config']:34s} text {s.get('.text', 0):6d} rodata "
              f"{s.get('.rodata', 0):4d} data {s.get('.data', 0):3d} bss {s.get('.bss', 0):5d} sum "
              f"{im['sum_text_rodata_data_bss']:6d} app {im['symbols']['app']} csr {im['symbols']['csr']} "
              f"vsnprintf {im['symbols']['vsnprintf']} maap_syms {len(im['maap_symbols_linked'])} und {len(im['undefined'])}")


if __name__ == "__main__":
    main()
