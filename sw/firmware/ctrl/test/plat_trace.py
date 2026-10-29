# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""plat_trace.py - the split platform's CSR initialisation against milan_baremetal.c's (#665 S3).

S3's acceptance: the CSR initialisation writes exactly what milan_baremetal
writes for the same shape. For every shipped config this compiles both on the
host and compares their writes on the same register file:

  - milan_baremetal.c as shipped, through builder gate 35's own host run
    (sw/builder/test_builder.py: _boot_case, _fabric_host_header,
    _fabric_host_run): its configure_fabric() against the words
    boot_policy.fabric_constants() derives from the builder's outputs;
  - plat/ctrl_plat_csr.c's ctrl_plat_csr_policy() against
    ctrl_plat_gen.py's header for the same config, on gate 35's seeded file.

The lists must be equal, write for write. Three plants in a copy of
ctrl_plat_csr.c must each make the shipping config's lists differ: a write
skipped, two writes reordered, and a wrong word.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

from ctrl_build import C_FLAGS, CTRL, ROOT, Outcome, Refusal

FIRMWARE = ROOT / "sw/firmware/milan_baremetal/milan_baremetal.c"
SHIPPING = "endstation_ax7101_1x1_tdm8"
#: The platform's side: gate 35's register file and its print of each write.
HOST_C = r"""
#include <stdint.h>
#include <stdio.h>
#include "ctrl_plat_csr.h"
#include "ctrl_plat_io.h"
#include "ctrl_plat_policy_gen.h"
#define WORDS 0x4000u
static uint32_t csr[WORDS];
uint32_t ctrl_plat_io_read32(uintptr_t address) { return csr[address / 4u]; }
void ctrl_plat_io_write32(uintptr_t address, uint32_t value)
{
	printf("W 0x%03x 0x%08x\n", (unsigned int)address, (unsigned int)value);
	csr[address / 4u] = value;
}
int main(void)
{
	static const struct ctrl_plat_policy policy = CTRL_PLAT_POLICY_INIT;
	for (unsigned int i = 0; i < WORDS; ++i)
		csr[i] = 0x5a000001u | (i << 10);
	ctrl_plat_csr_policy(0, &policy);
	return 0;
}
"""
#: (name, old, new): each plant is one substitution in ctrl_plat_csr.c.
PLANTS = (
    ("a write skipped", "\twr(csr, CTRL_PLAT_CSR_LWSRP_VID, p->sr_vid);\n", ""),
    ("two writes reordered",
     "\twr(csr, CTRL_PLAT_CSR_ADP_EID_LO, p->entity_id_lo);\n\twr(csr, CTRL_PLAT_CSR_ADP_EID_HI, p->entity_id_hi);\n",
     "\twr(csr, CTRL_PLAT_CSR_ADP_EID_HI, p->entity_id_hi);\n\twr(csr, CTRL_PLAT_CSR_ADP_EID_LO, p->entity_id_lo);\n"),
    ("a wrong word", "p->lwsrp_ctrl_reset | CTRL_PLAT_LWSRP_LIVE", "p->lwsrp_ctrl_reset | 0x2u"),
)
WRITE = re.compile(r"(?m)^W 0x([0-9a-f]+) 0x([0-9a-f]{8})$")


def gate35():
    """The builder gate's module, for its host run of configure_fabric()."""
    sys.path.insert(0, str(ROOT / "sw/builder"))
    sys.path.insert(0, str(ROOT / "sw/litex"))
    import test_builder  # noqa: E402
    return test_builder


def baremetal_writes(config: Path, work: Path) -> list[tuple[int, int]]:
    """configure_fabric()'s writes for one config, by gate 35's method."""
    tb = gate35()
    import boot_policy  # noqa: E402
    case = tb._boot_case(config.stem, config, work / "builder")
    words = boot_policy.fabric_constants(case.overlay, case.lwsrp)
    return tb._fabric_host_run("gcc", FIRMWARE.read_text(encoding="utf-8"),
                               tb._fabric_host_header(words, case.overlay), work / "baremetal")


def platform_writes(src: Path, config: Path, work: Path) -> list[tuple[int, int]]:
    """ctrl_plat_csr_policy()'s writes for one config, from the platform tree `src`."""
    work.mkdir(parents=True, exist_ok=True)
    header = work / "ctrl_plat_policy_gen.h"
    # the checkout's generator, as every arm runs adp_entity.py and aecp_entity.py
    gen = subprocess.run([sys.executable, "-B", str(CTRL / "plat/ctrl_plat_gen.py"), "policy", str(config),
                          "-o", str(header)], capture_output=True, text=True)
    if gen.returncode:
        raise Refusal(f"ctrl_plat_gen.py {config.name}: {gen.stderr.strip()}")
    (work / "host.c").write_text(HOST_C, encoding="utf-8")
    binary = work / "platform"
    built = subprocess.run(["gcc", *C_FLAGS, f"-I{src / 'plat'}", f"-I{work}", str(src / "plat/ctrl_plat_csr.c"),
                            str(work / "host.c"), "-o", str(binary)], capture_output=True, text=True)
    if built.returncode:
        raise Refusal(f"the platform's host build failed:\n{built.stderr[-3000:]}")
    ran = subprocess.run([str(binary)], capture_output=True, text=True)
    if ran.returncode:
        raise Refusal(f"ctrl_plat_csr_policy() did not run to completion:\n{ran.stderr}")
    return [(int(a, 16), int(v, 16)) for a, v in WRITE.findall(ran.stdout)]


def planted(src: Path, work: Path, old: str, new: str) -> Path:
    """A copy of the platform tree with one substitution in ctrl_plat_csr.c."""
    copy = work / "plat-src"
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(src / "plat", copy / "plat", ignore=shutil.ignore_patterns("__pycache__"))
    target = copy / "plat/ctrl_plat_csr.c"
    text = target.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise Refusal(f"plant fixture occurs {text.count(old)} times in ctrl_plat_csr.c")
    target.write_text(text.replace(old, new), encoding="utf-8")
    return copy


def arm(src: Path, out: Path) -> Outcome:
    """Every shipped config's two lists, equal; every plant, caught."""
    lines, failures, checks = [], 0, 0
    reference: dict[str, list[tuple[int, int]]] = {}
    try:
        for config in sorted((ROOT / "configs").glob("endstation_*.yaml")):
            work = out / config.stem
            want = baremetal_writes(config, work)
            got = platform_writes(src, config, work / "platform")
            reference[config.stem] = want
            checks += 1
            same = got == want and len(want) == 15
            failures += not same
            lines.append(f"  {config.stem}: {len(got)} writes, {'equal to' if same else 'DIFFERENT FROM'} "
                         f"configure_fabric()'s {len(want)}")
            if not same:
                lines.append(f"    platform  {[(hex(a), hex(v)) for a, v in got]}")
                lines.append(f"    baremetal {[(hex(a), hex(v)) for a, v in want]}")
        shipping = ROOT / "configs" / f"{SHIPPING}.yaml"
        for name, old, new in PLANTS:
            checks += 1
            copy = planted(src, out / "plant", old, new)
            caught = platform_writes(copy, shipping, out / "plant" / "build") != reference[SHIPPING]
            failures += not caught
            lines.append(f"  plant {name}: {'caught' if caught else 'ESCAPED'}")
    except (Refusal, OSError, AssertionError, KeyError) as exc:
        return Outcome("plattrace", 2, f"  refused: {exc}")
    lines += [f"== ctrl split platform CSR initialisation against milan_baremetal: checks: {checks}   "
              f"failures: {failures} ==", f"RESULT: {'FAIL' if failures else 'PASS'}"]
    return Outcome("plattrace", 1 if failures else 0, "\n".join(lines))


if __name__ == "__main__":
    outcome = arm(CTRL, Path(sys.argv[1]))
    print(outcome.log)
    raise SystemExit(outcome.rc)
